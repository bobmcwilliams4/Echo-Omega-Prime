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
        topic="Growth Chart Percentile Interpretation",
        keywords=["growth chart", "percentile", "pediatric", "height", "weight", "head circumference", "CDC", "WHO"],
        conclusion_template="Child's growth percentile is interpreted relative to population norms, considering age and sex.",
        reasoning_framework=(
            "1. Obtain accurate anthropometric measurements (height, weight, head circumference).\n"
            "2. Plot measurements on standardized growth charts (CDC or WHO).\n"
            "3. Determine percentile ranking for each parameter.\n"
            "4. Assess trends over time rather than isolated values.\n"
            "5. Identify deviations from expected growth patterns (crossing percentiles, persistent low/high percentiles).\n"
            "6. Consider familial/genetic factors, nutritional status, and underlying medical conditions.\n"
            "7. Evaluate for possible growth disorders if abnormal patterns are observed.\n"
            "8. Communicate findings to caregivers in context of overall health.\n"
            "9. Document interpretation and plan for follow-up if indicated.\n"
            "10. Use percentiles as screening, not diagnostic, tools.\n"
            "11. Recognize limitations of charts for diverse populations.\n"
            "12. Integrate clinical judgment with chart data.\n"
            "13. Refer to endocrinology if persistent abnormal growth.\n"
            "14. Reassess measurements at regular intervals.\n"
            "15. Consider environmental and socioeconomic factors impacting growth."
        ),
        key_factors=[
            "Age", "Sex", "Measurement accuracy", "Growth chart type", "Trend over time", "Familial growth patterns", "Nutritional status"
        ],
        primary_authority=[
            "CDC Growth Charts", "WHO Growth Standards", "AAP Guidelines"
        ],
        burden_holder="Clinician",
        adversary_position="Percentiles may not reflect individual health; charts may not fit all populations.",
        counter_arguments=[
            "Percentiles are screening tools, not definitive diagnoses.",
            "Growth charts are regularly updated to reflect population diversity.",
            "Clinical context is always considered alongside chart data."
        ],
        resolution_strategy="Integrate percentile data with clinical assessment and follow-up.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC/WHO Growth Chart Standards"
    ),
    DoctrineBlock(
        topic="Developmental Milestone Assessment",
        keywords=["developmental milestones", "motor", "language", "social", "cognitive", "screening", "Denver II", "ASQ"],
        conclusion_template="Child's developmental progress is evaluated against age-specific milestones using standardized tools.",
        reasoning_framework=(
            "1. Review age-appropriate milestones across motor, language, social, and cognitive domains.\n"
            "2. Use standardized screening tools (e.g., Denver II, Ages & Stages Questionnaire).\n"
            "3. Obtain history from caregivers regarding observed behaviors.\n"
            "4. Directly observe child during clinical visit.\n"
            "5. Identify delays or regressions in milestone attainment.\n"
            "6. Consider cultural and environmental influences on development.\n"
            "7. Assess for risk factors (prematurity, perinatal complications, genetic disorders).\n"
            "8. Document findings and compare to normative data.\n"
            "9. Refer for further evaluation if significant delays are noted.\n"
            "10. Provide anticipatory guidance to caregivers.\n"
            "11. Reassess at regular intervals.\n"
            "12. Collaborate with multidisciplinary teams as needed.\n"
            "13. Recognize variability in milestone attainment.\n"
            "14. Integrate findings with overall health and growth.\n"
            "15. Support early intervention when indicated."
        ),
        key_factors=[
            "Age", "Milestone domains", "Screening tool used", "Caregiver report", "Direct observation", "Risk factors"
        ],
        primary_authority=[
            "AAP Developmental Surveillance Guidelines", "CDC Milestone Checklist", "Denver II"
        ],
        burden_holder="Clinician",
        adversary_position="Milestones vary by culture and environment; screening tools may not capture all delays.",
        counter_arguments=[
            "Standardized tools are validated across diverse populations.",
            "Clinical judgment supplements screening results.",
            "Early intervention is prioritized when delays are suspected."
        ],
        resolution_strategy="Combine standardized assessment with clinical observation and caregiver input.",
        entity_scope="Children ages 0-5",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Developmental Surveillance"
    ),
    DoctrineBlock(
        topic="Routine Childhood Immunization Schedule",
        keywords=["immunization", "vaccination", "schedule", "CDC", "AAP", "MMR", "DTaP", "polio", "hepatitis", "HPV"],
        conclusion_template="Childhood immunizations are administered according to recommended schedules to prevent infectious diseases.",
        reasoning_framework=(
            "1. Review current CDC/AAP immunization schedule for age and risk factors.\n"
            "2. Assess child's immunization history and identify missed or due vaccines.\n"
            "3. Screen for contraindications and precautions.\n"
            "4. Educate caregivers on vaccine benefits, risks, and common side effects.\n"
            "5. Obtain informed consent prior to administration.\n"
            "6. Administer vaccines per recommended route and dosage.\n"
            "7. Document vaccine type, lot number, site, and date.\n"
            "8. Monitor for immediate adverse reactions.\n"
            "9. Schedule follow-up for subsequent doses if needed.\n"
            "10. Address vaccine hesitancy with evidence-based information.\n"
            "11. Report adverse events to VAERS as required.\n"
            "12. Maintain up-to-date records for school and public health compliance.\n"
            "13. Adapt schedule for special populations (immunocompromised, preterm).\n"
            "14. Use catch-up schedules when indicated.\n"
            "15. Collaborate with public health agencies for outbreak management."
        ),
        key_factors=[
            "Age", "Vaccine type", "Immunization history", "Contraindications", "Caregiver consent", "Public health requirements"
        ],
        primary_authority=[
            "CDC Immunization Schedule", "AAP Red Book", "WHO Vaccine Guidelines"
        ],
        burden_holder="Clinician",
        adversary_position="Vaccines may cause adverse effects; some caregivers refuse immunization.",
        counter_arguments=[
            "Vaccines are extensively tested for safety and efficacy.",
            "Adverse effects are rare and monitored.",
            "Herd immunity protects vulnerable populations."
        ],
        resolution_strategy="Educate, document, and follow evidence-based schedule; address hesitancy respectfully.",
        entity_scope="Children ages 0-18",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="CDC Immunization Schedule"
    ),
    DoctrineBlock(
        topic="Neonatal Jaundice Management",
        keywords=["neonatal jaundice", "bilirubin", "phototherapy", "kernicterus", "hyperbilirubinemia", "TSB", "TcB"],
        conclusion_template="Neonatal jaundice is managed based on bilirubin levels, age, and risk factors using phototherapy or exchange transfusion.",
        reasoning_framework=(
            "1. Assess for clinical signs of jaundice in newborns.\n"
            "2. Measure total serum bilirubin (TSB) or transcutaneous bilirubin (TcB).\n"
            "3. Plot bilirubin values on nomograms according to age in hours.\n"
            "4. Identify risk factors (prematurity, hemolysis, G6PD deficiency, sepsis).\n"
            "5. Determine need for phototherapy based on guidelines (AAP).\n"
            "6. Initiate phototherapy if indicated; monitor bilirubin levels.\n"
            "7. Consider exchange transfusion for severe hyperbilirubinemia or signs of acute bilirubin encephalopathy.\n"
            "8. Monitor hydration and feeding.\n"
            "9. Educate caregivers on signs of worsening jaundice.\n"
            "10. Document interventions and response.\n"
            "11. Discontinue phototherapy when bilirubin falls below threshold.\n"
            "12. Evaluate for underlying causes if jaundice persists.\n"
            "13. Prevent kernicterus by timely intervention.\n"
            "14. Reassess at follow-up visits.\n"
            "15. Collaborate with neonatology for complex cases."
        ),
        key_factors=[
            "Age in hours", "Bilirubin level", "Risk factors", "Feeding status", "Clinical signs"
        ],
        primary_authority=[
            "AAP Hyperbilirubinemia Guidelines", "WHO Neonatal Jaundice Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Phototherapy may be overused; exchange transfusion carries risks.",
        counter_arguments=[
            "Guidelines provide clear thresholds for intervention.",
            "Benefits outweigh risks when managed appropriately.",
            "Close monitoring reduces complications."
        ],
        resolution_strategy="Follow evidence-based thresholds and monitor response.",
        entity_scope="Neonates (0-28 days)",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAP Hyperbilirubinemia Guidelines"
    ),
    DoctrineBlock(
        topic="Neonatal Sepsis Evaluation",
        keywords=["neonatal sepsis", "infection", "blood culture", "CBC", "CRP", "antibiotics", "fever", "risk factors"],
        conclusion_template="Neonatal sepsis is evaluated using clinical signs, laboratory tests, and risk assessment to guide antibiotic therapy.",
        reasoning_framework=(
            "1. Identify clinical signs of sepsis (fever, lethargy, poor feeding, respiratory distress).\n"
            "2. Assess perinatal risk factors (prematurity, maternal infection, prolonged rupture of membranes).\n"
            "3. Obtain blood, urine, and CSF cultures prior to antibiotics.\n"
            "4. Order CBC, CRP, and other relevant labs.\n"
            "5. Initiate empiric antibiotics if sepsis is suspected.\n"
            "6. Monitor for clinical improvement and laboratory normalization.\n"
            "7. Adjust antibiotics based on culture results.\n"
            "8. Discontinue antibiotics if cultures are negative and clinical suspicion is low.\n"
            "9. Document findings and interventions.\n"
            "10. Educate caregivers on signs of infection.\n"
            "11. Collaborate with neonatology and infectious disease specialists.\n"
            "12. Reassess at regular intervals.\n"
            "13. Consider early discharge if criteria are met.\n"
            "14. Prevent nosocomial infections through hygiene.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Clinical signs", "Risk factors", "Culture results", "Laboratory findings", "Response to therapy"
        ],
        primary_authority=[
            "AAP Neonatal Sepsis Guidelines", "WHO Neonatal Infection Protocols"
        ],
        burden_holder="Clinician",
        adversary_position="Empiric antibiotics may lead to resistance; cultures may be falsely negative.",
        counter_arguments=[
            "Early treatment reduces mortality.",
            "Cultures are interpreted alongside clinical findings.",
            "Antibiotics are adjusted based on results."
        ],
        resolution_strategy="Combine clinical assessment with laboratory data and adjust therapy as needed.",
        entity_scope="Neonates (0-28 days)",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AAP Neonatal Sepsis Guidelines"
    ),
    DoctrineBlock(
        topic="Weight-Based Medication Dosing",
        keywords=["medication dosing", "weight-based", "mg/kg", "pediatric", "drug safety", "dose calculation"],
        conclusion_template="Pediatric medication dosing is calculated based on weight (mg/kg) to ensure safety and efficacy.",
        reasoning_framework=(
            "1. Obtain accurate current weight in kilograms.\n"
            "2. Review recommended dosing range for medication.\n"
            "3. Calculate dose using mg/kg formula.\n"
            "4. Consider maximum allowable dose per administration and per day.\n"
            "5. Adjust for renal/hepatic function if indicated.\n"
            "6. Double-check calculations for high-risk medications.\n"
            "7. Document dose, route, and frequency.\n"
            "8. Monitor for adverse effects and therapeutic response.\n"
            "9. Educate caregivers on administration and dosing intervals.\n"
            "10. Reassess weight and adjust dose as child grows.\n"
            "11. Use electronic prescribing tools when available.\n"
            "12. Consult pharmacy for complex cases.\n"
            "13. Avoid rounding errors in calculations.\n"
            "14. Report medication errors promptly.\n"
            "15. Maintain up-to-date references for drug dosing."
        ),
        key_factors=[
            "Weight in kg", "Medication type", "Dosing range", "Renal/hepatic function", "Maximum dose"
        ],
        primary_authority=[
            "AAP Pediatric Dosage Handbook", "Lexicomp", "FDA Pediatric Drug Guidelines"
        ],
        burden_holder="Clinician",
        adversary_position="Weight-based dosing may lead to errors; caregivers may miscalculate doses.",
        counter_arguments=[
            "Electronic tools reduce calculation errors.",
            "Caregiver education improves safety.",
            "Double-checking is standard practice."
        ],
        resolution_strategy="Use validated tools and educate caregivers; monitor closely.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Pediatric Dosage Handbook"
    ),
    DoctrineBlock(
        topic="Acute Otitis Media Diagnosis and Treatment",
        keywords=["otitis media", "ear infection", "antibiotics", "pediatric", "diagnosis", "tympanic membrane", "pain management"],
        conclusion_template="Acute otitis media is diagnosed clinically and treated with antibiotics or observation based on severity and age.",
        reasoning_framework=(
            "1. Assess for symptoms (ear pain, fever, irritability).\n"
            "2. Examine tympanic membrane for bulging, erythema, and decreased mobility.\n"
            "3. Differentiate from otitis media with effusion.\n"
            "4. Determine age and risk factors for complications.\n"
            "5. Decide on antibiotic therapy versus observation (AAP guidelines).\n"
            "6. Use amoxicillin as first-line therapy unless contraindicated.\n"
            "7. Provide pain management (acetaminophen, ibuprofen).\n"
            "8. Educate caregivers on signs of worsening infection.\n"
            "9. Schedule follow-up if symptoms persist.\n"
            "10. Document diagnosis and treatment plan.\n"
            "11. Avoid unnecessary antibiotics to reduce resistance.\n"
            "12. Consider tympanostomy tubes for recurrent cases.\n"
            "13. Address environmental risk factors (smoke exposure).\n"
            "14. Collaborate with ENT for complex cases.\n"
            "15. Monitor for hearing loss."
        ),
        key_factors=[
            "Symptoms", "Tympanic membrane findings", "Age", "Severity", "Risk factors"
        ],
        primary_authority=[
            "AAP Otitis Media Guidelines", "CDC Ear Infection Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Antibiotics may be overused; observation may delay treatment.",
        counter_arguments=[
            "Guidelines support observation in select cases.",
            "Pain management is prioritized.",
            "Follow-up ensures timely intervention."
        ],
        resolution_strategy="Follow evidence-based guidelines and monitor response.",
        entity_scope="Children ages 6 months-12 years",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Otitis Media Guidelines"
    ),
    DoctrineBlock(
        topic="Streptococcal Pharyngitis Management",
        keywords=["strep throat", "pharyngitis", "rapid strep test", "antibiotics", "pediatric", "penicillin", "complications"],
        conclusion_template="Streptococcal pharyngitis is diagnosed with rapid testing and treated with antibiotics to prevent complications.",
        reasoning_framework=(
            "1. Assess for symptoms (sore throat, fever, tonsillar exudate, cervical lymphadenopathy).\n"
            "2. Use Centor criteria to estimate likelihood of streptococcal infection.\n"
            "3. Perform rapid antigen detection test (RADT).\n"
            "4. Confirm with throat culture if RADT is negative and suspicion remains high.\n"
            "5. Initiate antibiotics (penicillin or amoxicillin) if positive.\n"
            "6. Educate caregivers on importance of completing course.\n"
            "7. Monitor for complications (rheumatic fever, peritonsillar abscess).\n"
            "8. Provide symptomatic relief (analgesics, hydration).\n"
            "9. Document diagnosis and treatment.\n"
            "10. Avoid antibiotics for viral pharyngitis.\n"
            "11. Address recurrent infections with further evaluation.\n"
            "12. Collaborate with ENT for severe cases.\n"
            "13. Prevent transmission through hygiene.\n"
            "14. Report outbreaks to public health.\n"
            "15. Reassess if symptoms persist."
        ),
        key_factors=[
            "Symptoms", "RADT result", "Centor criteria", "Antibiotic choice", "Complications"
        ],
        primary_authority=[
            "CDC Strep Throat Guidelines", "AAP Infectious Disease Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Antibiotics may be overprescribed; RADT may miss cases.",
        counter_arguments=[
            "Guidelines support testing before treatment.",
            "Culture confirms diagnosis when needed.",
            "Antibiotics prevent serious complications."
        ],
        resolution_strategy="Test before treating; monitor for complications.",
        entity_scope="Children ages 3-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Strep Throat Guidelines"
    ),
    DoctrineBlock(
        topic="Asthma Severity Classification and Management",
        keywords=["asthma", "severity", "classification", "management", "inhaled corticosteroids", "bronchodilators", "spirometry", "pediatric"],
        conclusion_template="Asthma is classified by severity and managed with stepwise pharmacotherapy and environmental control.",
        reasoning_framework=(
            "1. Assess frequency and severity of symptoms (daytime, nighttime, activity limitation).\n"
            "2. Perform spirometry or peak flow measurement.\n"
            "3. Classify asthma (intermittent, mild persistent, moderate persistent, severe persistent).\n"
            "4. Initiate stepwise therapy per NHLBI guidelines.\n"
            "5. Use inhaled corticosteroids as first-line for persistent asthma.\n"
            "6. Add long-acting bronchodilators or leukotriene modifiers as needed.\n"
            "7. Educate caregivers on inhaler technique and adherence.\n"
            "8. Develop asthma action plan.\n"
            "9. Address environmental triggers (allergens, smoke).\n"
            "10. Monitor response and adjust therapy.\n"
            "11. Document classification and management plan.\n"
            "12. Refer to pulmonology for severe or uncontrolled asthma.\n"
            "13. Provide emergency instructions for exacerbations.\n"
            "14. Reassess at regular intervals.\n"
            "15. Support school accommodations as needed."
        ),
        key_factors=[
            "Symptom frequency", "Spirometry", "Severity classification", "Medication adherence", "Environmental triggers"
        ],
        primary_authority=[
            "NHLBI Asthma Guidelines", "AAP Asthma Management Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Stepwise therapy may be complex; inhaler adherence is challenging.",
        counter_arguments=[
            "Education improves adherence.",
            "Action plans reduce exacerbations.",
            "Regular follow-up optimizes management."
        ],
        resolution_strategy="Classify severity, educate, and adjust therapy as needed.",
        entity_scope="Children ages 2-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NHLBI Asthma Guidelines"
    ),
    DoctrineBlock(
        topic="Bronchiolitis Clinical Management",
        keywords=["bronchiolitis", "RSV", "infant", "respiratory distress", "supportive care", "oxygen", "hydration"],
        conclusion_template="Bronchiolitis is managed with supportive care, monitoring, and hospitalization if severe.",
        reasoning_framework=(
            "1. Assess for symptoms (cough, wheezing, respiratory distress, poor feeding).\n"
            "2. Evaluate for risk factors (prematurity, chronic lung disease, congenital heart disease).\n"
            "3. Monitor oxygen saturation and respiratory effort.\n"
            "4. Provide supportive care (hydration, suctioning, oxygen if needed).\n"
            "5. Avoid routine use of bronchodilators or steroids.\n"
            "6. Hospitalize if severe distress, hypoxemia, or dehydration.\n"
            "7. Educate caregivers on home management and warning signs.\n"
            "8. Document clinical findings and interventions.\n"
            "9. Prevent transmission through hygiene.\n"
            "10. Reassess regularly during illness.\n"
            "11. Collaborate with pulmonology for complex cases.\n"
            "12. Avoid unnecessary imaging or antibiotics.\n"
            "13. Support breastfeeding during illness.\n"
            "14. Provide anticipatory guidance.\n"
            "15. Report severe cases to public health if indicated."
        ),
        key_factors=[
            "Symptoms", "Oxygen saturation", "Risk factors", "Severity", "Caregiver education"
        ],
        primary_authority=[
            "AAP Bronchiolitis Guidelines", "CDC RSV Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Supportive care may be insufficient; hospitalization may be overused.",
        counter_arguments=[
            "Guidelines support outpatient care for mild cases.",
            "Hospitalization is reserved for severe illness.",
            "Caregiver education improves outcomes."
        ],
        resolution_strategy="Monitor severity and provide evidence-based supportive care.",
        entity_scope="Infants ages 0-24 months",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAP Bronchiolitis Guidelines"
    ),
    DoctrineBlock(
        topic="Infant Feeding and Breastfeeding Support",
        keywords=["infant feeding", "breastfeeding", "formula", "nutrition", "latch", "milk supply", "AAP", "WHO"],
        conclusion_template="Infant feeding is supported with breastfeeding as preferred, supplemented as needed, and monitored for adequacy.",
        reasoning_framework=(
            "1. Encourage exclusive breastfeeding for first 6 months (AAP/WHO).\n"
            "2. Assess latch, milk supply, and infant weight gain.\n"
            "3. Address common breastfeeding challenges (pain, engorgement, low supply).\n"
            "4. Provide education and support to caregivers.\n"
            "5. Supplement with formula if medically indicated.\n"
            "6. Monitor for adequate hydration and nutrition.\n"
            "7. Document feeding method and progress.\n"
            "8. Refer to lactation consultant for complex issues.\n"
            "9. Support maternal health and nutrition.\n"
            "10. Introduce complementary foods at 6 months.\n"
            "11. Avoid cow's milk before 12 months.\n"
            "12. Educate on safe formula preparation.\n"
            "13. Address cultural and socioeconomic factors.\n"
            "14. Reassess feeding at regular intervals.\n"
            "15. Promote skin-to-skin and bonding."
        ),
        key_factors=[
            "Feeding method", "Latch", "Milk supply", "Infant weight gain", "Maternal health"
        ],
        primary_authority=[
            "AAP Breastfeeding Guidelines", "WHO Infant Feeding Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Breastfeeding may not be feasible; formula may be stigmatized.",
        counter_arguments=[
            "Support is provided for all feeding choices.",
            "Formula is safe and nutritionally adequate.",
            "Education reduces stigma and improves outcomes."
        ],
        resolution_strategy="Support caregiver choice and monitor infant nutrition.",
        entity_scope="Infants ages 0-12 months",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="AAP Breastfeeding Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Febrile Seizure Management",
        keywords=["febrile seizure", "fever", "seizure", "pediatric", "benign", "antipyretics", "EEG", "LP"],
        conclusion_template="Febrile seizures are managed with reassurance, antipyretics, and further evaluation if atypical.",
        reasoning_framework=(
            "1. Assess seizure characteristics (duration, focality, recurrence).\n"
            "2. Obtain history of fever and illness.\n"
            "3. Perform physical exam to rule out CNS infection.\n"
            "4. Classify as simple or complex febrile seizure.\n"
            "5. Provide reassurance to caregivers.\n"
            "6. Use antipyretics for comfort, not seizure prevention.\n"
            "7. Avoid routine EEG or neuroimaging for simple seizures.\n"
            "8. Consider lumbar puncture if signs of meningitis.\n"
            "9. Educate caregivers on seizure first aid.\n"
            "10. Document event and management plan.\n"
            "11. Refer to neurology for complex or recurrent seizures.\n"
            "12. Monitor for recurrence during illness.\n"
            "13. Avoid chronic anticonvulsants for simple febrile seizures.\n"
            "14. Support follow-up for ongoing concerns.\n"
            "15. Address caregiver anxiety with evidence-based information."
        ),
        key_factors=[
            "Seizure characteristics", "Fever history", "Physical exam", "Classification", "Caregiver education"
        ],
        primary_authority=[
            "AAP Febrile Seizure Guidelines", "CDC Seizure Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Seizures may indicate serious illness; antipyretics may not prevent recurrence.",
        counter_arguments=[
            "Simple febrile seizures are benign.",
            "Evaluation rules out serious causes.",
            "Education reduces anxiety and improves outcomes."
        ],
        resolution_strategy="Classify seizure, reassure, and evaluate as needed.",
        entity_scope="Children ages 6 months-5 years",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Febrile Seizure Guidelines"
    ),
    DoctrineBlock(
        topic="Attention-Deficit/Hyperactivity Disorder Diagnosis",
        keywords=["ADHD", "diagnosis", "behavior", "school", "DSM-5", "pediatric", "assessment"],
        conclusion_template="ADHD is diagnosed using DSM-5 criteria, multi-informant assessment, and exclusion of other causes.",
        reasoning_framework=(
            "1. Obtain detailed history from caregivers and teachers.\n"
            "2. Assess for symptoms of inattention, hyperactivity, and impulsivity.\n"
            "3. Use standardized rating scales (Vanderbilt, Conners).\n"
            "4. Apply DSM-5 diagnostic criteria.\n"
            "5. Rule out other medical, psychiatric, and environmental causes.\n"
            "6. Evaluate impact on academic and social functioning.\n"
            "7. Document findings and diagnosis.\n"
            "8. Educate caregivers on ADHD and management options.\n"
            "9. Refer to psychology or psychiatry for complex cases.\n"
            "10. Collaborate with school for accommodations.\n"
            "11. Support ongoing assessment and follow-up.\n"
            "12. Address comorbidities (anxiety, learning disorders).\n"
            "13. Avoid overdiagnosis by thorough evaluation.\n"
            "14. Use multidisciplinary approach.\n"
            "15. Monitor response to interventions."
        ),
        key_factors=[
            "History", "Symptoms", "Rating scales", "DSM-5 criteria", "Exclusion of other causes"
        ],
        primary_authority=[
            "DSM-5", "AAP ADHD Guidelines", "CDC ADHD Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="ADHD may be overdiagnosed; symptoms may be situational.",
        counter_arguments=[
            "Multi-informant assessment reduces bias.",
            "DSM-5 criteria are specific.",
            "Exclusion of other causes is standard practice."
        ],
        resolution_strategy="Use standardized criteria and multi-informant assessment.",
        entity_scope="Children ages 4-18",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="DSM-5"
    ),
    DoctrineBlock(
        topic="Pediatric Dehydration Assessment and Fluid Management",
        keywords=["dehydration", "fluid management", "oral rehydration", "IV fluids", "pediatric", "electrolytes", "assessment"],
        conclusion_template="Dehydration is assessed clinically and managed with oral or IV fluids based on severity.",
        reasoning_framework=(
            "1. Assess for signs of dehydration (dry mucosa, poor skin turgor, tachycardia, sunken eyes).\n"
            "2. Estimate severity (mild, moderate, severe) based on clinical findings.\n"
            "3. Obtain history of fluid losses (vomiting, diarrhea, fever).\n"
            "4. Monitor vital signs and urine output.\n"
            "5. Use oral rehydration for mild-moderate dehydration.\n"
            "6. Initiate IV fluids for severe dehydration or inability to tolerate oral intake.\n"
            "7. Calculate fluid requirements based on weight and deficit.\n"
            "8. Monitor for electrolyte abnormalities.\n"
            "9. Document assessment and interventions.\n"
            "10. Educate caregivers on prevention and home management.\n"
            "11. Reassess hydration status regularly.\n"
            "12. Avoid rapid correction to prevent complications.\n"
            "13. Collaborate with nephrology for complex cases.\n"
            "14. Address underlying cause of dehydration.\n"
            "15. Support follow-up for ongoing needs."
        ),
        key_factors=[
            "Clinical signs", "Severity", "Fluid losses", "Weight", "Electrolytes"
        ],
        primary_authority=[
            "AAP Dehydration Guidelines", "WHO Oral Rehydration Protocols"
        ],
        burden_holder="Clinician",
        adversary_position="Oral rehydration may be insufficient; IV fluids may cause complications.",
        counter_arguments=[
            "Severity guides management choice.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Assess severity, choose appropriate therapy, and monitor closely.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Dehydration Guidelines"
    ),
    DoctrineBlock(
        topic="Sudden Infant Death Syndrome Prevention",
        keywords=["SIDS", "prevention", "safe sleep", "back to sleep", "crib", "smoke exposure", "AAP"],
        conclusion_template="SIDS risk is reduced by safe sleep practices, environmental control, and caregiver education.",
        reasoning_framework=(
            "1. Educate caregivers on placing infants on their backs to sleep.\n"
            "2. Use firm sleep surfaces without soft bedding or toys.\n"
            "3. Avoid bed-sharing; room-sharing is preferred.\n"
            "4. Maintain smoke-free environment.\n"
            "5. Encourage breastfeeding.\n"
            "6. Avoid overheating during sleep.\n"
            "7. Use pacifier at sleep time if desired.\n"
            "8. Document education and practices.\n"
            "9. Monitor for adherence to safe sleep guidelines.\n"
            "10. Address cultural and socioeconomic factors.\n"
            "11. Support caregiver anxiety with evidence-based information.\n"
            "12. Collaborate with public health for outreach.\n"
            "13. Reassess at well-child visits.\n"
            "14. Provide anticipatory guidance.\n"
            "15. Report SIDS cases to public health."
        ),
        key_factors=[
            "Sleep position", "Sleep environment", "Smoke exposure", "Caregiver education", "Breastfeeding"
        ],
        primary_authority=[
            "AAP SIDS Prevention Guidelines", "CDC Safe Sleep Recommendations"
        ],
        burden_holder="Caregiver",
        adversary_position="Safe sleep practices may be difficult to implement; cultural norms may conflict.",
        counter_arguments=[
            "Education improves adherence.",
            "Guidelines are evidence-based.",
            "Room-sharing is a compromise."
        ],
        resolution_strategy="Educate, support, and monitor safe sleep practices.",
        entity_scope="Infants ages 0-12 months",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="AAP SIDS Prevention Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Hypertension Screening and Management",
        keywords=["hypertension", "blood pressure", "screening", "management", "pediatric", "lifestyle", "medication"],
        conclusion_template="Pediatric hypertension is screened using age-appropriate norms and managed with lifestyle changes and medication if needed.",
        reasoning_framework=(
            "1. Measure blood pressure using appropriate cuff size and technique.\n"
            "2. Compare readings to normative tables by age, sex, and height.\n"
            "3. Repeat measurements to confirm diagnosis.\n"
            "4. Assess for secondary causes (renal, endocrine, cardiac).\n"
            "5. Initiate lifestyle modifications (diet, exercise, weight management).\n"
            "6. Start pharmacologic therapy if lifestyle changes fail or if severe hypertension.\n"
            "7. Monitor for target organ damage (heart, kidneys, eyes).\n"
            "8. Educate caregivers on home monitoring and adherence.\n"
            "9. Document diagnosis and management plan.\n"
            "10. Collaborate with nephrology or cardiology for complex cases.\n"
            "11. Reassess blood pressure at regular intervals.\n"
            "12. Support school accommodations as needed.\n"
            "13. Address comorbidities (obesity, diabetes).\n"
            "14. Use multidisciplinary approach.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Blood pressure readings", "Normative tables", "Secondary causes", "Lifestyle factors", "Medication adherence"
        ],
        primary_authority=[
            "AAP Hypertension Guidelines", "CDC Blood Pressure Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Blood pressure norms may not fit all populations; medication may have side effects.",
        counter_arguments=[
            "Norms are regularly updated.",
            "Lifestyle changes are prioritized.",
            "Monitoring reduces risks."
        ],
        resolution_strategy="Screen, confirm, and manage with evidence-based approach.",
        entity_scope="Children ages 3-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Hypertension Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Diabetes Mellitus Diagnosis and Management",
        keywords=["diabetes", "type 1", "type 2", "diagnosis", "management", "insulin", "glucose", "HbA1c", "pediatric"],
        conclusion_template="Pediatric diabetes is diagnosed with glucose and HbA1c testing and managed with insulin or lifestyle interventions.",
        reasoning_framework=(
            "1. Assess for symptoms (polyuria, polydipsia, weight loss).\n"
            "2. Obtain fasting glucose, random glucose, and HbA1c.\n"
            "3. Diagnose per ADA criteria.\n"
            "4. Differentiate between type 1 and type 2 diabetes.\n"
            "5. Initiate insulin therapy for type 1; lifestyle and oral agents for type 2.\n"
            "6. Educate caregivers and child on glucose monitoring and management.\n"
            "7. Monitor for complications (DKA, hypoglycemia).\n"
            "8. Document diagnosis and management plan.\n"
            "9. Collaborate with endocrinology for ongoing care.\n"
            "10. Support school accommodations.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address comorbidities (obesity, hypertension).\n"
            "13. Use multidisciplinary approach.\n"
            "14. Provide psychosocial support.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Glucose levels", "HbA1c", "Type of diabetes", "Management plan", "Education"
        ],
        primary_authority=[
            "ADA Diabetes Guidelines", "AAP Diabetes Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Insulin therapy is complex; lifestyle changes may be difficult.",
        counter_arguments=[
            "Education improves adherence.",
            "Multidisciplinary support is available.",
            "Monitoring reduces complications."
        ],
        resolution_strategy="Diagnose accurately and manage with evidence-based interventions.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ADA Diabetes Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Obesity Assessment and Intervention",
        keywords=["obesity", "BMI", "assessment", "intervention", "nutrition", "exercise", "pediatric"],
        conclusion_template="Pediatric obesity is assessed using BMI and managed with lifestyle interventions and multidisciplinary support.",
        reasoning_framework=(
            "1. Measure height and weight; calculate BMI.\n"
            "2. Compare BMI to age- and sex-specific percentiles.\n"
            "3. Assess for comorbidities (hypertension, diabetes, dyslipidemia).\n"
            "4. Obtain dietary and activity history.\n"
            "5. Initiate lifestyle interventions (nutrition, exercise).\n"
            "6. Refer to dietitian and behavioral health as needed.\n"
            "7. Monitor progress and adjust interventions.\n"
            "8. Educate caregivers and child on healthy habits.\n"
            "9. Document assessment and management plan.\n"
            "10. Support school and community resources.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address socioeconomic and cultural factors.\n"
            "13. Use multidisciplinary approach.\n"
            "14. Avoid stigmatization.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "BMI percentile", "Comorbidities", "Dietary history", "Activity level", "Intervention plan"
        ],
        primary_authority=[
            "AAP Obesity Guidelines", "CDC BMI Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Lifestyle changes may be difficult; BMI may not reflect health in all populations.",
        counter_arguments=[
            "Multidisciplinary support improves outcomes.",
            "BMI is a screening tool.",
            "Education reduces barriers."
        ],
        resolution_strategy="Assess, intervene, and support with evidence-based approach.",
        entity_scope="Children ages 2-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Obesity Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Anemia Diagnosis and Management",
        keywords=["anemia", "hemoglobin", "iron deficiency", "diagnosis", "management", "pediatric"],
        conclusion_template="Pediatric anemia is diagnosed with hemoglobin testing and managed with iron supplementation and investigation of causes.",
        reasoning_framework=(
            "1. Assess for symptoms (fatigue, pallor, tachycardia).\n"
            "2. Obtain CBC and reticulocyte count.\n"
            "3. Diagnose anemia per age-specific hemoglobin norms.\n"
            "4. Identify cause (iron deficiency, chronic disease, hemolysis).\n"
            "5. Initiate iron supplementation for iron deficiency.\n"
            "6. Monitor response to therapy.\n"
            "7. Investigate for underlying causes if anemia persists.\n"
            "8. Educate caregivers on dietary sources of iron.\n"
            "9. Document diagnosis and management plan.\n"
            "10. Collaborate with hematology for complex cases.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address comorbidities.\n"
            "13. Use multidisciplinary approach.\n"
            "14. Avoid unnecessary transfusions.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Hemoglobin level", "Cause of anemia", "Response to therapy", "Dietary history", "Comorbidities"
        ],
        primary_authority=[
            "AAP Anemia Guidelines", "CDC Hematology Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Iron supplementation may cause side effects; anemia may be secondary to chronic disease.",
        counter_arguments=[
            "Monitoring reduces risks.",
            "Investigation identifies underlying causes.",
            "Education improves adherence."
        ],
        resolution_strategy="Diagnose accurately, treat, and monitor response.",
        entity_scope="Children ages 6 months-18 years",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Anemia Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Allergy Diagnosis and Management",
        keywords=["allergy", "diagnosis", "management", "skin testing", "IgE", "anaphylaxis", "pediatric"],
        conclusion_template="Allergies are diagnosed with history and testing and managed with avoidance, medication, and emergency planning.",
        reasoning_framework=(
            "1. Obtain detailed history of symptoms and exposures.\n"
            "2. Perform skin prick testing or serum IgE measurement.\n"
            "3. Identify specific allergens.\n"
            "4. Educate caregivers and child on avoidance strategies.\n"
            "5. Initiate pharmacotherapy (antihistamines, corticosteroids).\n"
            "6. Develop emergency action plan for anaphylaxis.\n"
            "7. Prescribe epinephrine auto-injector if indicated.\n"
            "8. Document diagnosis and management plan.\n"
            "9. Collaborate with allergy/immunology for complex cases.\n"
            "10. Support school accommodations.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address comorbidities (asthma, eczema).\n"
            "13. Use multidisciplinary approach.\n"
            "14. Avoid unnecessary testing.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Testing results", "Allergen identification", "Management plan", "Emergency preparedness"
        ],
        primary_authority=[
            "AAAAI Allergy Guidelines", "AAP Allergy Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Testing may be inconclusive; avoidance may be difficult.",
        counter_arguments=[
            "Education improves outcomes.",
            "Emergency planning reduces risks.",
            "Multidisciplinary support is available."
        ],
        resolution_strategy="Diagnose, educate, and manage with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAAAI Allergy Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Infectious Disease Outbreak Management",
        keywords=["infectious disease", "outbreak", "management", "public health", "reporting", "pediatric"],
        conclusion_template="Outbreaks are managed with identification, reporting, isolation, and public health collaboration.",
        reasoning_framework=(
            "1. Identify cases and confirm diagnosis.\n"
            "2. Report outbreak to public health authorities.\n"
            "3. Implement isolation and infection control measures.\n"
            "4. Educate caregivers and community on prevention.\n"
            "5. Collaborate with public health for investigation and response.\n"
            "6. Monitor for additional cases.\n"
            "7. Document interventions and outcomes.\n"
            "8. Support school and community accommodations.\n"
            "9. Reassess at regular intervals.\n"
            "10. Address socioeconomic and cultural factors.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Provide anticipatory guidance.\n"
            "13. Avoid stigmatization.\n"
            "14. Support vaccination campaigns.\n"
            "15. Report outcomes to public health."
        ),
        key_factors=[
            "Case identification", "Reporting", "Isolation", "Education", "Collaboration"
        ],
        primary_authority=[
            "CDC Outbreak Management Guidelines", "AAP Infectious Disease Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Isolation may be difficult; reporting may cause anxiety.",
        counter_arguments=[
            "Collaboration improves outcomes.",
            "Education reduces anxiety.",
            "Guidelines support evidence-based response."
        ],
        resolution_strategy="Identify, report, and collaborate for outbreak management.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Outbreak Management Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Mental Health Screening and Referral",
        keywords=["mental health", "screening", "referral", "depression", "anxiety", "behavior", "pediatric"],
        conclusion_template="Mental health is screened using standardized tools and referred to specialists as needed.",
        reasoning_framework=(
            "1. Use standardized screening tools (PHQ-9, GAD-7, PSC).\n"
            "2. Obtain history from caregivers and child.\n"
            "3. Assess for symptoms of depression, anxiety, behavioral issues.\n"
            "4. Rule out medical causes.\n"
            "5. Document findings and screening results.\n"
            "6. Educate caregivers on mental health and resources.\n"
            "7. Refer to psychology or psychiatry for positive screens.\n"
            "8. Collaborate with school for accommodations.\n"
            "9. Support ongoing assessment and follow-up.\n"
            "10. Address comorbidities.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Avoid stigmatization.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Reassess at regular intervals.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Screening tool", "Symptoms", "History", "Referral", "Follow-up"
        ],
        primary_authority=[
            "AAP Mental Health Guidelines", "CDC Mental Health Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Screening may be insufficient; referral may be delayed.",
        counter_arguments=[
            "Standardized tools improve detection.",
            "Collaboration supports timely referral.",
            "Education reduces barriers."
        ],
        resolution_strategy="Screen, educate, and refer as needed.",
        entity_scope="Children ages 4-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Mental Health Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Emergency Triage and Stabilization",
        keywords=["emergency", "triage", "stabilization", "ABC", "pediatric", "resuscitation", "assessment"],
        conclusion_template="Pediatric emergencies are triaged and stabilized using ABC approach and rapid assessment.",
        reasoning_framework=(
            "1. Assess airway, breathing, and circulation (ABC).\n"
            "2. Perform rapid primary survey.\n"
            "3. Initiate stabilization measures (oxygen, IV access, fluids).\n"
            "4. Monitor vital signs and response.\n"
            "5. Identify life-threatening conditions.\n"
            "6. Document interventions and outcomes.\n"
            "7. Collaborate with emergency medicine and critical care.\n"
            "8. Support caregiver communication.\n"
            "9. Reassess at regular intervals.\n"
            "10. Address comorbidities.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Provide anticipatory guidance.\n"
            "13. Avoid unnecessary delays.\n"
            "14. Support follow-up for ongoing needs.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "ABC assessment", "Stabilization", "Vital signs", "Life-threatening conditions", "Collaboration"
        ],
        primary_authority=[
            "AAP Emergency Guidelines", "PALS Protocols"
        ],
        burden_holder="Clinician",
        adversary_position="Triage may miss subtle cases; stabilization may be delayed.",
        counter_arguments=[
            "ABC approach is rapid and effective.",
            "Collaboration improves outcomes.",
            "Education reduces errors."
        ],
        resolution_strategy="Use ABC approach and collaborate for stabilization.",
        entity_scope="Children ages 0-18",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="PALS Protocols"
    ),
    DoctrineBlock(
        topic="Pediatric Pain Assessment and Management",
        keywords=["pain", "assessment", "management", "scale", "analgesics", "pediatric"],
        conclusion_template="Pain is assessed using age-appropriate scales and managed with pharmacologic and non-pharmacologic interventions.",
        reasoning_framework=(
            "1. Use age-appropriate pain scales (FLACC, Wong-Baker, Numeric).\n"
            "2. Obtain history of pain and impact on function.\n"
            "3. Assess for underlying cause.\n"
            "4. Initiate pharmacologic therapy (acetaminophen, ibuprofen, opioids if indicated).\n"
            "5. Use non-pharmacologic interventions (distraction, comfort measures).\n"
            "6. Monitor response and adjust therapy.\n"
            "7. Educate caregivers and child on pain management.\n"
            "8. Document assessment and interventions.\n"
            "9. Collaborate with pain management specialists for complex cases.\n"
            "10. Support school and activity accommodations.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address comorbidities.\n"
            "13. Use multidisciplinary approach.\n"
            "14. Avoid overuse of opioids.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Pain scale", "History", "Cause", "Management plan", "Response"
        ],
        primary_authority=[
            "AAP Pain Management Guidelines", "WHO Pediatric Pain Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Pain scales may be subjective; analgesics may have side effects.",
        counter_arguments=[
            "Multiple scales improve accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Assess, manage, and monitor pain with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Pain Management Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Vaccination Adverse Event Management",
        keywords=["vaccination", "adverse event", "management", "reporting", "VAERS", "pediatric"],
        conclusion_template="Adverse events are managed with clinical assessment, reporting, and supportive care.",
        reasoning_framework=(
            "1. Assess for symptoms following vaccination (fever, rash, anaphylaxis).\n"
            "2. Obtain history of timing and severity.\n"
            "3. Provide supportive care as indicated.\n"
            "4. Report adverse events to VAERS.\n"
            "5. Document findings and interventions.\n"
            "6. Educate caregivers on expected and serious reactions.\n"
            "7. Collaborate with infectious disease and allergy specialists for severe cases.\n"
            "8. Monitor for recurrence with future vaccinations.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary delays in vaccination.\n"
            "15. Report outcomes to public health."
        ),
        key_factors=[
            "Symptoms", "Timing", "Severity", "Reporting", "Supportive care"
        ],
        primary_authority=[
            "CDC Vaccine Adverse Event Guidelines", "AAP Immunization Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Reporting may cause anxiety; adverse events may be misattributed.",
        counter_arguments=[
            "Reporting improves safety.",
            "Education reduces anxiety.",
            "Guidelines support evidence-based management."
        ],
        resolution_strategy="Assess, report, and manage adverse events with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Vaccine Adverse Event Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Dermatologic Disorder Diagnosis and Management",
        keywords=["dermatology", "disorder", "diagnosis", "management", "eczema", "psoriasis", "impetigo", "pediatric"],
        conclusion_template="Dermatologic disorders are diagnosed clinically and managed with topical or systemic therapy as indicated.",
        reasoning_framework=(
            "1. Obtain history of skin symptoms and exposures.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Diagnose per clinical criteria (eczema, psoriasis, impetigo).\n"
            "4. Initiate topical therapy (steroids, antibiotics, emollients).\n"
            "5. Use systemic therapy for severe cases.\n"
            "6. Educate caregivers and child on skin care.\n"
            "7. Monitor response and adjust therapy.\n"
            "8. Collaborate with dermatology for complex cases.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary antibiotics.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Therapy", "Response"
        ],
        primary_authority=[
            "AAP Dermatology Guidelines", "CDC Skin Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Clinical criteria improve accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Dermatology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Gastrointestinal Disorder Diagnosis and Management",
        keywords=["gastrointestinal", "disorder", "diagnosis", "management", "constipation", "GERD", "pediatric"],
        conclusion_template="GI disorders are diagnosed clinically and managed with dietary, pharmacologic, and behavioral interventions.",
        reasoning_framework=(
            "1. Obtain history of GI symptoms and dietary habits.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Diagnose per clinical criteria (constipation, GERD).\n"
            "4. Initiate dietary interventions (fiber, hydration).\n"
            "5. Use pharmacologic therapy as indicated.\n"
            "6. Educate caregivers and child on management.\n"
            "7. Monitor response and adjust therapy.\n"
            "8. Collaborate with gastroenterology for complex cases.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary medications.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Therapy", "Response"
        ],
        primary_authority=[
            "AAP GI Guidelines", "NASPGHAN Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Clinical criteria improve accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP GI Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Neurologic Disorder Diagnosis and Management",
        keywords=["neurology", "disorder", "diagnosis", "management", "seizure", "migraine", "pediatric"],
        conclusion_template="Neurologic disorders are diagnosed clinically and managed with pharmacologic and supportive interventions.",
        reasoning_framework=(
            "1. Obtain history of neurologic symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Diagnose per clinical criteria (seizure, migraine).\n"
            "4. Initiate pharmacologic therapy as indicated.\n"
            "5. Use supportive interventions (education, accommodations).\n"
            "6. Monitor response and adjust therapy.\n"
            "7. Collaborate with neurology for complex cases.\n"
            "8. Support school and activity accommodations.\n"
            "9. Reassess at regular intervals.\n"
            "10. Address comorbidities.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Provide anticipatory guidance.\n"
            "13. Avoid unnecessary medications.\n"
            "14. Support follow-up for ongoing needs.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Therapy", "Response"
        ],
        primary_authority=[
            "AAP Neurology Guidelines", "CDC Neurologic Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Clinical criteria improve accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Neurology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Rheumatologic Disorder Diagnosis and Management",
        keywords=["rheumatology", "disorder", "diagnosis", "management", "juvenile arthritis", "pediatric"],
        conclusion_template="Rheumatologic disorders are diagnosed clinically and managed with pharmacologic and supportive interventions.",
        reasoning_framework=(
            "1. Obtain history of joint symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Diagnose per clinical criteria (juvenile arthritis).\n"
            "4. Initiate pharmacologic therapy (NSAIDs, DMARDs).\n"
            "5. Use supportive interventions (physical therapy, education).\n"
            "6. Monitor response and adjust therapy.\n"
            "7. Collaborate with rheumatology for complex cases.\n"
            "8. Support school and activity accommodations.\n"
            "9. Reassess at regular intervals.\n"
            "10. Address comorbidities.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Provide anticipatory guidance.\n"
            "13. Avoid unnecessary medications.\n"
            "14. Support follow-up for ongoing needs.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Therapy", "Response"
        ],
        primary_authority=[
            "AAP Rheumatology Guidelines", "CDC Rheumatologic Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Clinical criteria improve accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Rheumatology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Cardiac Disorder Diagnosis and Management",
        keywords=["cardiology", "disorder", "diagnosis", "management", "congenital heart disease", "pediatric"],
        conclusion_template="Cardiac disorders are diagnosed clinically and managed with pharmacologic, surgical, and supportive interventions.",
        reasoning_framework=(
            "1. Obtain history of cardiac symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Use diagnostic testing (ECG, echocardiogram).\n"
            "4. Diagnose per clinical criteria (congenital heart disease).\n"
            "5. Initiate pharmacologic therapy as indicated.\n"
            "6. Refer for surgical intervention if needed.\n"
            "7. Use supportive interventions (education, accommodations).\n"
            "8. Monitor response and adjust therapy.\n"
            "9. Collaborate with cardiology for complex cases.\n"
            "10. Support school and activity accommodations.\n"
            "11. Reassess at regular intervals.\n"
            "12. Address comorbidities.\n"
            "13. Use multidisciplinary approach.\n"
            "14. Provide anticipatory guidance.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Testing", "Therapy"
        ],
        primary_authority=[
            "AAP Cardiology Guidelines", "CDC Cardiac Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Diagnostic testing improves accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Cardiology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Renal Disorder Diagnosis and Management",
        keywords=["nephrology", "disorder", "diagnosis", "management", "nephrotic syndrome", "pediatric"],
        conclusion_template="Renal disorders are diagnosed clinically and managed with pharmacologic and supportive interventions.",
        reasoning_framework=(
            "1. Obtain history of renal symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Use diagnostic testing (urinalysis, renal function).\n"
            "4. Diagnose per clinical criteria (nephrotic syndrome).\n"
            "5. Initiate pharmacologic therapy as indicated.\n"
            "6. Use supportive interventions (education, accommodations).\n"
            "7. Monitor response and adjust therapy.\n"
            "8. Collaborate with nephrology for complex cases.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary medications.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Testing", "Therapy"
        ],
        primary_authority=[
            "AAP Nephrology Guidelines", "CDC Renal Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Diagnostic testing improves accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Nephrology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Immunodeficiency Diagnosis and Management",
        keywords=["immunodeficiency", "diagnosis", "management", "testing", "infection", "pediatric"],
        conclusion_template="Immunodeficiency is diagnosed with history and testing and managed with infection prevention and supportive care.",
        reasoning_framework=(
            "1. Obtain history of recurrent infections and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Use diagnostic testing (CBC, immunoglobulin levels).\n"
            "4. Diagnose per clinical criteria.\n"
            "5. Initiate infection prevention strategies (vaccination, hygiene).\n"
            "6. Use supportive interventions (education, accommodations).\n"
            "7. Monitor response and adjust therapy.\n"
            "8. Collaborate with immunology for complex cases.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary antibiotics.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Testing", "Infection prevention"
        ],
        primary_authority=[
            "AAP Immunology Guidelines", "CDC Immunodeficiency Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; infection prevention may be difficult.",
        counter_arguments=[
            "Testing improves accuracy.",
            "Education improves outcomes.",
            "Monitoring reduces risks."
        ],
        resolution_strategy="Diagnose, prevent infection, and support with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Immunology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Endocrine Disorder Diagnosis and Management",
        keywords=["endocrinology", "disorder", "diagnosis", "management", "thyroid", "growth", "pediatric"],
        conclusion_template="Endocrine disorders are diagnosed clinically and managed with pharmacologic and supportive interventions.",
        reasoning_framework=(
            "1. Obtain history of endocrine symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Use diagnostic testing (TSH, growth hormone, glucose).\n"
            "4. Diagnose per clinical criteria (thyroid disorder, growth disorder).\n"
            "5. Initiate pharmacologic therapy as indicated.\n"
            "6. Use supportive interventions (education, accommodations).\n"
            "7. Monitor response and adjust therapy.\n"
            "8. Collaborate with endocrinology for complex cases.\n"
            "9. Support school and activity accommodations.\n"
            "10. Reassess at regular intervals.\n"
            "11. Address comorbidities.\n"
            "12. Use multidisciplinary approach.\n"
            "13. Provide anticipatory guidance.\n"
            "14. Avoid unnecessary medications.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "History", "Physical exam", "Diagnosis", "Testing", "Therapy"
        ],
        primary_authority=[
            "AAP Endocrinology Guidelines", "CDC Endocrine Disorder Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be uncertain; therapy may cause side effects.",
        counter_arguments=[
            "Testing improves accuracy.",
            "Monitoring reduces risks.",
            "Education improves outcomes."
        ],
        resolution_strategy="Diagnose, manage, and monitor with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Endocrinology Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Immunization Catch-Up Schedule",
        keywords=["immunization", "catch-up", "schedule", "vaccination", "pediatric"],
        conclusion_template="Catch-up immunizations are administered per CDC schedule to ensure protection against vaccine-preventable diseases.",
        reasoning_framework=(
            "1. Review immunization history and identify missed vaccines.\n"
            "2. Consult CDC catch-up schedule for age and vaccine type.\n"
            "3. Screen for contraindications and precautions.\n"
            "4. Educate caregivers on importance of catch-up immunization.\n"
            "5. Obtain informed consent prior to administration.\n"
            "6. Administer vaccines per recommended route and dosage.\n"
            "7. Document vaccine type, lot number, site, and date.\n"
            "8. Monitor for immediate adverse reactions.\n"
            "9. Schedule follow-up for subsequent doses if needed.\n"
            "10. Address vaccine hesitancy with evidence-based information.\n"
            "11. Report adverse events to VAERS as required.\n"
            "12. Maintain up-to-date records for school and public health compliance.\n"
            "13. Adapt schedule for special populations.\n"
            "14. Use multidisciplinary approach.\n"
            "15. Collaborate with public health agencies for outbreak management."
        ),
        key_factors=[
            "Immunization history", "Catch-up schedule", "Contraindications", "Caregiver consent", "Public health requirements"
        ],
        primary_authority=[
            "CDC Catch-Up Immunization Schedule", "AAP Red Book"
        ],
        burden_holder="Clinician",
        adversary_position="Catch-up schedule may be complex; caregivers may be hesitant.",
        counter_arguments=[
            "Education improves adherence.",
            "Schedule is evidence-based.",
            "Monitoring reduces risks."
        ],
        resolution_strategy="Follow catch-up schedule and educate caregivers.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Catch-Up Immunization Schedule"
    ),
    DoctrineBlock(
        topic="Pediatric Surgical Referral Criteria",
        keywords=["surgery", "referral", "criteria", "pediatric", "indications"],
        conclusion_template="Surgical referral is made based on clinical criteria, severity, and failure of medical management.",
        reasoning_framework=(
            "1. Assess for symptoms and impact on function.\n"
            "2. Perform physical exam and document findings.\n"
            "3. Identify indications for surgical intervention (failure of medical management, severity, anatomical abnormality).\n"
            "4. Consult surgical referral guidelines.\n"
            "5. Educate caregivers on referral process and expectations.\n"
            "6. Collaborate with surgical team for evaluation.\n"
            "7. Support school and activity accommodations.\n"
            "8. Document referral and rationale.\n"
            "9. Reassess at regular intervals.\n"
            "10. Address comorbidities.\n"
            "11. Use multidisciplinary approach.\n"
            "12. Provide anticipatory guidance.\n"
            "13. Avoid unnecessary referrals.\n"
            "14. Support follow-up for ongoing needs.\n"
            "15. Report cases to public health if indicated."
        ),
        key_factors=[
            "Symptoms", "Physical exam", "Indications", "Referral guidelines", "Caregiver education"
        ],
        primary_authority=[
            "AAP Surgical Referral Guidelines", "CDC Surgical Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Referral may be delayed; criteria may be unclear.",
        counter_arguments=[
            "Guidelines clarify indications.",
            "Education improves outcomes.",
            "Collaboration supports timely referral."
        ],
        resolution_strategy="Assess, refer, and support with evidence-based approach.",
        entity_scope="Children ages 0-18",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAP Surgical Referral Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Preventive Health Screening",
        keywords=["preventive", "health", "screening", "well-child", "vision", "hearing", "pediatric"],
        conclusion_template="Preventive health screening is performed at well-child visits using standardized tools and guidelines.",
        reasoning_framework=(
            "1. Use standardized screening tools for vision, hearing, and development.\n"
            "2. Obtain history from caregivers and child.\n"
            "3. Assess for risk factors and comorbidities.\n"
            "4. Document findings and screening results.\n"
            "5. Educate caregivers on preventive health and resources.\n"
            "6. Refer to specialists for positive screens.\n"
            "7. Support school and activity accommodations.\n"
            "8. Reassess at regular intervals.\n"
            "9. Address socioeconomic and cultural factors.\n"
            "10. Use multidisciplinary approach.\n"
            "11. Provide anticipatory guidance.\n"
            "12. Avoid unnecessary testing.\n"
            "13. Support follow-up for ongoing needs.\n"
            "14. Report cases to public health if indicated.\n"
            "15. Monitor for adherence to screening guidelines."
        ),
        key_factors=[
            "Screening tool", "History", "Risk factors", "Referral", "Follow-up"
        ],
        primary_authority=[
            "AAP Preventive Health Guidelines", "CDC Screening Recommendations"
        ],
        burden_holder="Clinician",
        adversary_position="Screening may be insufficient; referral may be delayed.",
        counter_arguments=[
            "Standardized tools improve detection.",
            "Collaboration supports timely referral.",
            "Education reduces barriers."
        ],
        resolution_strategy="Screen, educate, and refer as needed.",
        entity_scope="Children ages 0-18",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAP Preventive Health Guidelines"
    ),
    DoctrineBlock(
        topic="Pediatric Environmental Health Risk Assessment",
        keywords=["environmental", "health", "risk", "assessment", "lead", "smoke", "pediatric"],
        conclusion_template="Environmental health risks are assessed and managed with screening, education, and mitigation strategies.",
        reasoning_framework=(
            "1. Screen for environmental risk factors (lead, smoke, toxins).\n"
            "2. Obtain history from caregivers and child.\n"
            "3. Assess for symptoms and impact on health.\n"
            "4. Document findings and screening results.\n"
            "5. Educate caregivers on environmental risks and mitigation.\n"
            "6. Refer to specialists for positive screens.\n"
            "7. Collaborate with public health for investigation and response.\n"
            "8. Support school and activity accommodations.\