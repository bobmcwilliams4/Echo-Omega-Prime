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
        topic="CBC Differential Interpretation",
        keywords=["CBC", "differential", "WBC", "neutrophilia", "lymphocytosis", "anemia", "thrombocytopenia"],
        conclusion_template="Interpret the CBC differential to identify infection, inflammation, hematologic malignancy, or cytopenias.",
        reasoning_framework="""
1. Evaluate total WBC count for leukocytosis or leukopenia.
2. Assess neutrophil count: neutrophilia suggests bacterial infection, stress, or steroids; neutropenia may indicate marrow failure or viral infection.
3. Lymphocyte count: lymphocytosis suggests viral infection or CLL; lymphopenia may be due to immunodeficiency or steroids.
4. Monocyte, eosinophil, basophil counts: consider chronic infection, allergy, or myeloproliferative disorders.
5. Assess hemoglobin/hematocrit for anemia or polycythemia.
6. Platelet count: thrombocytopenia may indicate DIC, ITP, TTP, or marrow suppression; thrombocytosis may be reactive or myeloproliferative.
7. Correlate findings with clinical context and prior values.
8. Consider peripheral smear for abnormal cells or morphology.
9. Rule out pseudoleukopenia or pseudothrombocytopenia (clumping).
10. Integrate with other laboratory and clinical data for diagnosis.
""",
        key_factors=[
            "Absolute and relative counts of WBC subtypes",
            "Hemoglobin and hematocrit levels",
            "Platelet count",
            "Clinical context (infection, malignancy, drugs)",
            "Peripheral smear findings"
        ],
        primary_authority=[
            "Hoffbrand's Essential Haematology",
            "Henry's Clinical Diagnosis and Management by Laboratory Methods",
            "UpToDate: Approach to the patient with abnormal CBC"
        ],
        burden_holder="Interpreting physician or pathologist",
        adversary_position="CBC changes are nonspecific and may not indicate pathology",
        counter_arguments=[
            "CBC findings must be interpreted in clinical context",
            "Repeat testing and trend analysis improve specificity",
            "Peripheral smear can clarify ambiguous results"
        ],
        resolution_strategy="Correlate CBC findings with clinical presentation and consider further diagnostic workup as indicated.",
        entity_scope="All patients undergoing CBC testing",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Hoffbrand's Essential Haematology, 8th Edition"
    ),
    DoctrineBlock(
        topic="Coagulation Studies: PT, INR, PTT, Fibrinogen, D-dimer",
        keywords=["coagulation", "PT", "INR", "PTT", "fibrinogen", "D-dimer", "bleeding", "clotting"],
        conclusion_template="Interpret PT, INR, PTT, fibrinogen, and D-dimer to assess bleeding risk, monitor anticoagulation, or evaluate for DIC.",
        reasoning_framework="""
1. PT/INR evaluates extrinsic and common pathways (factors I, II, V, VII, X); prolonged in warfarin therapy, liver disease, vitamin K deficiency.
2. PTT evaluates intrinsic and common pathways (factors I, II, V, VIII, IX, X, XI, XII); prolonged in heparin therapy, hemophilia, lupus anticoagulant.
3. Fibrinogen: low in DIC, severe liver disease, or massive bleeding; high in inflammation.
4. D-dimer: elevated in active clot breakdown (DVT, PE, DIC), but nonspecific.
5. Assess for mixing studies if PT/PTT prolonged to distinguish factor deficiency from inhibitor.
6. Evaluate for clinical evidence of bleeding or thrombosis.
7. Consider medication history, liver function, and recent procedures.
8. Use serial measurements to monitor trends, especially in DIC or anticoagulation.
9. Integrate with platelet count and peripheral smear.
10. Confirm abnormal results with repeat testing if unexpected.
""",
        key_factors=[
            "Degree and pattern of PT/INR and PTT prolongation",
            "Fibrinogen level",
            "D-dimer elevation",
            "Clinical context (bleeding, thrombosis, liver disease, anticoagulation)",
            "Medication history"
        ],
        primary_authority=[
            "Henry's Clinical Diagnosis and Management by Laboratory Methods",
            "UpToDate: Approach to the patient with abnormal coagulation tests",
            "American Society of Hematology Guidelines"
        ],
        burden_holder="Ordering physician or hematologist",
        adversary_position="Isolated abnormal results may be due to preanalytical error or non-pathologic factors",
        counter_arguments=[
            "Repeat testing can rule out lab error",
            "Clinical correlation is essential",
            "Mixing studies clarify factor deficiency vs inhibitor"
        ],
        resolution_strategy="Integrate lab findings with clinical scenario and repeat or expand testing as necessary.",
        entity_scope="Patients with bleeding, thrombosis, or on anticoagulants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASH Guidelines on Coagulation Testing"
    ),
    DoctrineBlock(
        topic="Basic Metabolic Panel (BMP) Interpretation",
        keywords=["BMP", "electrolytes", "sodium", "potassium", "chloride", "bicarbonate", "BUN", "creatinine", "glucose"],
        conclusion_template="Interpret BMP to assess renal function, electrolyte balance, and metabolic status.",
        reasoning_framework="""
1. Sodium: hyponatremia or hypernatremia indicates water balance disorder; assess volume status and osmolality.
2. Potassium: hypokalemia or hyperkalemia affects cardiac function; consider renal function, medications, acid-base status.
3. Chloride: follows sodium; hypochloremia in vomiting, hyperchloremia in acidosis.
4. Bicarbonate: low in metabolic acidosis, high in metabolic alkalosis or compensation.
5. BUN and creatinine: assess renal function; BUN/Cr ratio helps differentiate prerenal, renal, or postrenal causes.
6. Glucose: hyperglycemia in diabetes, stress; hypoglycemia in insulin excess, sepsis.
7. Evaluate for anion gap to assess metabolic acidosis.
8. Review trends and correlate with clinical findings.
9. Consider medication effects (diuretics, ACE inhibitors, etc.).
10. Repeat or expand testing if abnormalities are detected.
""",
        key_factors=[
            "Electrolyte levels and trends",
            "Renal function markers",
            "Acid-base status",
            "Clinical volume status",
            "Medication history"
        ],
        primary_authority=[
            "Goldman-Cecil Medicine",
            "UpToDate: Interpretation of basic metabolic panel",
            "National Kidney Foundation Guidelines"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Mild abnormalities may be transient or non-pathologic",
        counter_arguments=[
            "Assess for acute vs chronic changes",
            "Repeat testing for confirmation",
            "Evaluate for underlying causes"
        ],
        resolution_strategy="Correlate BMP findings with clinical context and consider further workup if persistent or severe.",
        entity_scope="All patients with BMP testing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NKF Guidelines on Renal Function Assessment"
    ),
    DoctrineBlock(
        topic="Comprehensive Metabolic Panel (CMP) and Liver Enzymes",
        keywords=["CMP", "liver enzymes", "AST", "ALT", "ALP", "bilirubin", "albumin", "total protein"],
        conclusion_template="Interpret CMP and liver enzymes to assess hepatic function, cholestasis, and synthetic capacity.",
        reasoning_framework="""
1. AST/ALT: elevated in hepatocellular injury (viral hepatitis, drugs, ischemia); ALT more liver-specific.
2. ALP: elevated in cholestasis, bone disease, pregnancy; confirm hepatic origin with GGT.
3. Bilirubin: unconjugated (hemolysis, Gilbert's), conjugated (cholestasis, hepatitis).
4. Albumin: low in chronic liver disease, nephrotic syndrome, malnutrition.
5. Total protein: reflects albumin and globulins; low in chronic disease, high in gammopathies.
6. Assess pattern of enzyme elevation (hepatocellular vs cholestatic).
7. Correlate with clinical findings (jaundice, pruritus, RUQ pain).
8. Review medication and alcohol history.
9. Consider imaging if obstruction suspected.
10. Repeat or expand testing as indicated.
""",
        key_factors=[
            "Pattern and degree of enzyme elevation",
            "Synthetic function (albumin, PT/INR)",
            "Bilirubin fractions",
            "Clinical symptoms and risk factors",
            "Medication and alcohol history"
        ],
        primary_authority=[
            "Zakim and Boyer's Hepatology",
            "UpToDate: Interpretation of liver biochemical tests",
            "American Association for the Study of Liver Diseases (AASLD) Guidelines"
        ],
        burden_holder="Ordering physician or hepatologist",
        adversary_position="Mild enzyme elevations may be transient or non-specific",
        counter_arguments=[
            "Assess for chronicity and trend",
            "Rule out extrahepatic causes",
            "Consider repeat testing"
        ],
        resolution_strategy="Integrate lab findings with clinical context and pursue further evaluation if persistent or severe.",
        entity_scope="Patients with abnormal liver enzymes or suspected liver disease",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AASLD Guidelines"
    ),
    DoctrineBlock(
        topic="Cardiac Biomarkers: Troponin, BNP, CK-MB",
        keywords=["cardiac biomarkers", "troponin", "BNP", "CK-MB", "myocardial infarction", "heart failure"],
        conclusion_template="Interpret cardiac biomarkers to diagnose myocardial injury, infarction, or heart failure.",
        reasoning_framework="""
1. Troponin: highly sensitive and specific for myocardial injury; rise and/or fall with ischemic symptoms indicates MI.
2. BNP/NT-proBNP: elevated in heart failure due to ventricular stretch; interpret in context of renal function, age, obesity.
3. CK-MB: less specific than troponin; may be useful for reinfarction.
4. Assess timing of biomarker elevation relative to symptom onset.
5. Serial measurements improve diagnostic accuracy.
6. Consider non-cardiac causes of troponin elevation (sepsis, PE, renal failure).
7. Integrate with ECG and clinical findings.
8. Use risk scores (e.g., TIMI, GRACE) for prognosis.
9. Repeat testing if initial results equivocal.
10. Consult cardiology for ambiguous or complex cases.
""",
        key_factors=[
            "Magnitude and trend of biomarker elevation",
            "Timing relative to symptoms",
            "Clinical presentation",
            "Renal function",
            "ECG findings"
        ],
        primary_authority=[
            "ACC/AHA Guidelines for the Management of Acute Coronary Syndromes",
            "UpToDate: Cardiac biomarkers in ACS",
            "European Society of Cardiology Guidelines"
        ],
        burden_holder="Attending physician or cardiologist",
        adversary_position="Troponin elevation is not specific for MI in all cases",
        counter_arguments=[
            "Clinical correlation is essential",
            "Serial measurements clarify etiology",
            "Consider alternative diagnoses"
        ],
        resolution_strategy="Integrate biomarker data with clinical and ECG findings; repeat or expand testing as needed.",
        entity_scope="Patients with chest pain or suspected cardiac disease",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="Thyroid Function Tests: TSH, Free T4, T3",
        keywords=["thyroid", "TSH", "Free T4", "T3", "hypothyroidism", "hyperthyroidism"],
        conclusion_template="Interpret TSH, Free T4, and T3 to diagnose and monitor thyroid dysfunction.",
        reasoning_framework="""
1. TSH: primary screening test; elevated in primary hypothyroidism, suppressed in hyperthyroidism.
2. Free T4: low in hypothyroidism, high in hyperthyroidism; confirms diagnosis if TSH abnormal.
3. T3: elevated in T3 toxicosis; less useful for hypothyroidism.
4. Assess for central (secondary) hypothyroidism (low TSH, low T4).
5. Consider non-thyroidal illness (sick euthyroid syndrome) in hospitalized patients.
6. Review medication effects (amiodarone, steroids, biotin).
7. Repeat testing if results inconsistent with clinical picture.
8. Monitor therapy with TSH (hypothyroidism) or T4/T3 (hyperthyroidism).
9. Consider thyroid antibody testing if autoimmune disease suspected.
10. Correlate with symptoms and physical findings.
""",
        key_factors=[
            "TSH and Free T4 levels",
            "Clinical symptoms",
            "Medication history",
            "Presence of thyroid antibodies",
            "Pituitary function"
        ],
        primary_authority=[
            "American Thyroid Association Guidelines",
            "UpToDate: Interpretation of thyroid function tests",
            "Williams Textbook of Endocrinology"
        ],
        burden_holder="Ordering clinician or endocrinologist",
        adversary_position="Abnormal results may be due to non-thyroidal illness or medications",
        counter_arguments=[
            "Repeat testing after recovery from acute illness",
            "Review medication and supplement use",
            "Consider pituitary evaluation"
        ],
        resolution_strategy="Integrate lab findings with clinical context and repeat or expand testing as necessary.",
        entity_scope="Patients with suspected or known thyroid disease",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ATA Guidelines"
    ),
    DoctrineBlock(
        topic="Lipid Panel Interpretation",
        keywords=["lipid panel", "cholesterol", "LDL", "HDL", "triglycerides", "cardiovascular risk"],
        conclusion_template="Interpret lipid panel to assess cardiovascular risk and guide therapy.",
        reasoning_framework="""
1. LDL cholesterol: primary target for therapy; high levels increase atherosclerotic risk.
2. HDL cholesterol: protective; low levels increase risk.
3. Triglycerides: elevated in metabolic syndrome, diabetes, pancreatitis risk if >500 mg/dL.
4. Total cholesterol: less specific, but used in risk calculators.
5. Assess fasting vs non-fasting status.
6. Use ASCVD risk calculators to guide statin therapy.
7. Consider secondary causes (hypothyroidism, nephrotic syndrome, medications).
8. Monitor response to therapy with serial measurements.
9. Counsel on lifestyle modification for all patients.
10. Consider genetic lipid disorders in severe or refractory cases.
""",
        key_factors=[
            "LDL, HDL, triglyceride levels",
            "ASCVD risk factors",
            "Fasting status",
            "Secondary causes",
            "Therapeutic response"
        ],
        primary_authority=[
            "ACC/AHA Cholesterol Guidelines",
            "UpToDate: Interpretation of lipid panel",
            "National Lipid Association Recommendations"
        ],
        burden_holder="Primary care provider or cardiologist",
        adversary_position="Single abnormal result may not reflect chronic risk",
        counter_arguments=[
            "Repeat testing for confirmation",
            "Assess for acute illness or secondary causes",
            "Use risk calculators for decision-making"
        ],
        resolution_strategy="Integrate lipid panel with clinical risk assessment and repeat as indicated.",
        entity_scope="Adults undergoing cardiovascular risk assessment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Cholesterol Guidelines"
    ),
    DoctrineBlock(
        topic="Urinalysis: Dipstick, Microscopy, and Culture",
        keywords=["urinalysis", "dipstick", "microscopy", "urine culture", "UTI", "hematuria", "proteinuria"],
        conclusion_template="Interpret urinalysis to diagnose infection, hematuria, proteinuria, or systemic disease.",
        reasoning_framework="""
1. Dipstick: assess for leukocyte esterase, nitrites (UTI), blood (hematuria), protein (proteinuria), glucose, ketones.
2. Microscopy: evaluate for WBCs, RBCs, casts, crystals, bacteria.
3. Urine culture: confirm infection and guide antibiotic therapy.
4. Assess for contamination (squamous epithelial cells).
5. Hematuria: consider infection, stones, malignancy, trauma.
6. Proteinuria: quantify and assess for nephrotic syndrome, glomerulonephritis.
7. Pyuria without bacteriuria: consider interstitial nephritis, TB.
8. Correlate with clinical symptoms (dysuria, frequency, flank pain).
9. Repeat or expand testing if findings unclear.
10. Consider imaging for persistent or unexplained abnormalities.
""",
        key_factors=[
            "Dipstick and microscopic findings",
            "Clinical symptoms",
            "Contamination indicators",
            "Culture results",
            "History of renal or urinary tract disease"
        ],
        primary_authority=[
            "UpToDate: Approach to the patient with abnormal urinalysis",
            "National Kidney Foundation Guidelines",
            "Bates' Guide to Physical Examination and History Taking"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Contaminated samples may yield misleading results",
        counter_arguments=[
            "Repeat testing with clean-catch sample",
            "Correlate with clinical findings",
            "Use culture for definitive diagnosis"
        ],
        resolution_strategy="Repeat or confirm findings and correlate with clinical context.",
        entity_scope="Patients with urinary symptoms or abnormal urinalysis",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NKF Guidelines"
    ),
    DoctrineBlock(
        topic="Blood Gas Analysis: ABG and VBG",
        keywords=["blood gas", "ABG", "VBG", "acid-base", "hypoxemia", "hypercapnia", "respiratory failure"],
        conclusion_template="Interpret ABG and VBG to assess acid-base status, oxygenation, and ventilation.",
        reasoning_framework="""
1. Assess pH: acidosis (<7.35) or alkalosis (>7.45).
2. PaCO2: respiratory component; elevated in hypoventilation, low in hyperventilation.
3. HCO3-: metabolic component; low in metabolic acidosis, high in alkalosis.
4. PaO2: assess oxygenation; low in hypoxemia.
5. Calculate anion gap for metabolic acidosis.
6. Use compensation formulas to determine primary vs mixed disorders.
7. VBG: pH and CO2 correlate with ABG, but not O2.
8. Correlate with clinical findings (respiratory distress, shock).
9. Consider causes: DKA, sepsis, COPD, renal failure.
10. Repeat testing to monitor response to therapy.
""",
        key_factors=[
            "pH, PaCO2, HCO3- values",
            "Oxygenation status",
            "Compensation patterns",
            "Clinical presentation",
            "Underlying disease"
        ],
        primary_authority=[
            "Goldman-Cecil Medicine",
            "UpToDate: Interpretation of arterial and venous blood gases",
            "American Thoracic Society Guidelines"
        ],
        burden_holder="Ordering physician or intensivist",
        adversary_position="VBG may not accurately reflect arterial oxygenation",
        counter_arguments=[
            "Use ABG for precise oxygenation assessment",
            "VBG sufficient for acid-base in most cases",
            "Correlate with pulse oximetry"
        ],
        resolution_strategy="Select appropriate test (ABG vs VBG) and integrate with clinical findings.",
        entity_scope="Patients with respiratory or metabolic derangements",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ATS Guidelines"
    ),
    DoctrineBlock(
        topic="Hemoglobin A1c for Diabetes Monitoring",
        keywords=["A1c", "diabetes", "glycemic control", "chronic hyperglycemia", "monitoring"],
        conclusion_template="Use Hemoglobin A1c to assess long-term glycemic control in diabetes.",
        reasoning_framework="""
1. A1c reflects average glucose over prior 2-3 months.
2. Diagnostic threshold: ≥6.5% for diabetes; 5.7-6.4% for prediabetes.
3. Target for most adults: <7.0%; individualized based on comorbidities, age, hypoglycemia risk.
4. A1c may be inaccurate in hemoglobinopathies, anemia, recent transfusion.
5. Correlate with self-monitoring and symptoms.
6. Repeat every 3-6 months to monitor therapy.
7. Use alternative markers (fructosamine) if A1c unreliable.
8. Counsel on lifestyle modification and medication adherence.
9. Assess for complications if A1c persistently elevated.
10. Document and trend A1c over time.
""",
        key_factors=[
            "A1c value and trend",
            "Presence of confounding conditions",
            "Therapeutic targets",
            "Self-monitoring data",
            "Risk of complications"
        ],
        primary_authority=[
            "American Diabetes Association Standards of Care",
            "UpToDate: Hemoglobin A1c in diabetes",
            "International Diabetes Federation Guidelines"
        ],
        burden_holder="Primary care provider or endocrinologist",
        adversary_position="A1c may be unreliable in certain hematologic conditions",
        counter_arguments=[
            "Use alternative markers if indicated",
            "Correlate with clinical and SMBG data",
            "Repeat testing for confirmation"
        ],
        resolution_strategy="Individualize targets and use alternative monitoring if necessary.",
        entity_scope="Patients with diabetes or at risk",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ADA Standards of Care"
    ),
    DoctrineBlock(
        topic="Blood Culture Identification and Sensitivity",
        keywords=["blood culture", "bacteremia", "sepsis", "antibiotic sensitivity", "contamination"],
        conclusion_template="Interpret blood culture results to diagnose bacteremia and guide antimicrobial therapy.",
        reasoning_framework="""
1. Positive cultures indicate bacteremia; identify organism and susceptibility.
2. Assess for contamination (single positive, skin flora, clinical context).
3. Multiple sets increase diagnostic yield and reduce false positives.
4. Correlate with clinical signs of infection (fever, hypotension).
5. Use sensitivity data to tailor antibiotic therapy.
6. Repeat cultures if persistent fever or suspected endocarditis.
7. Consider source control if indicated (catheter removal, abscess drainage).
8. Document timing of cultures relative to antibiotics.
9. Communicate results promptly to clinical team.
10. Monitor for complications (septic shock, metastatic infection).
""",
        key_factors=[
            "Organism identified",
            "Number and timing of positive cultures",
            "Antibiotic susceptibility",
            "Clinical context",
            "Source of infection"
        ],
        primary_authority=[
            "IDSA Guidelines for the Diagnosis and Management of Sepsis",
            "UpToDate: Interpretation of blood cultures",
            "Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases"
        ],
        burden_holder="Microbiologist and treating physician",
        adversary_position="Contaminants may be misinterpreted as true bacteremia",
        counter_arguments=[
            "Assess for clinical correlation",
            "Repeat cultures to confirm",
            "Consider organism and number of positives"
        ],
        resolution_strategy="Integrate lab and clinical data; repeat cultures if uncertainty persists.",
        entity_scope="Patients with suspected or confirmed bacteremia",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines"
    ),
    DoctrineBlock(
        topic="CSF Analysis: Cell Count, Protein, Glucose",
        keywords=["CSF", "lumbar puncture", "cell count", "protein", "glucose", "meningitis", "subarachnoid hemorrhage"],
        conclusion_template="Interpret CSF analysis to diagnose meningitis, encephalitis, or subarachnoid hemorrhage.",
        reasoning_framework="""
1. Cell count: neutrophilic pleocytosis in bacterial, lymphocytic in viral/fungal/TB.
2. Protein: elevated in infection, inflammation, or blood-brain barrier disruption.
3. Glucose: low in bacterial/fungal/TB meningitis; normal in viral.
4. Xanthochromia: suggests subarachnoid hemorrhage.
5. Compare CSF glucose to serum glucose.
6. Consider opening pressure and appearance.
7. Gram stain and culture for definitive diagnosis.
8. PCR for viral pathogens.
9. Repeat LP if initial results equivocal.
10. Integrate with clinical findings (fever, neck stiffness, altered mental status).
""",
        key_factors=[
            "Cell differential",
            "Protein and glucose levels",
            "Gram stain and culture",
            "Clinical presentation",
            "Opening pressure"
        ],
        primary_authority=[
            "UpToDate: Interpretation of CSF findings",
            "IDSA Guidelines for Meningitis",
            "Adams and Victor's Principles of Neurology"
        ],
        burden_holder="Neurologist or infectious disease specialist",
        adversary_position="Traumatic tap may confound interpretation",
        counter_arguments=[
            "Use RBC correction formulas",
            "Repeat LP if necessary",
            "Correlate with clinical findings"
        ],
        resolution_strategy="Integrate lab and clinical data; repeat or expand testing as needed.",
        entity_scope="Patients undergoing lumbar puncture",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines"
    ),
    DoctrineBlock(
        topic="Tumor Markers: PSA, CEA, CA-125, AFP",
        keywords=["tumor markers", "PSA", "CEA", "CA-125", "AFP", "cancer diagnosis", "monitoring"],
        conclusion_template="Use tumor markers for cancer screening, diagnosis, and monitoring, not as stand-alone diagnostic tests.",
        reasoning_framework="""
1. PSA: prostate cancer screening and monitoring; elevated in BPH, prostatitis.
2. CEA: colorectal cancer monitoring; elevated in smokers, other malignancies.
3. CA-125: ovarian cancer monitoring; elevated in benign gynecologic conditions.
4. AFP: hepatocellular carcinoma, germ cell tumors; elevated in chronic hepatitis.
5. Use in conjunction with imaging and histopathology.
6. Serial measurements more informative than single value.
7. Not recommended for population-wide screening except PSA in select groups.
8. Interpret in clinical context to avoid false positives.
9. Consider age, comorbidities, and risk factors.
10. Counsel patients on limitations and implications of results.
""",
        key_factors=[
            "Marker specificity and sensitivity",
            "Clinical context",
            "Serial trends",
            "Imaging and pathology correlation",
            "Risk factors"
        ],
        primary_authority=[
            "American Society of Clinical Oncology Guidelines",
            "UpToDate: Tumor markers in oncology",
            "National Comprehensive Cancer Network (NCCN) Guidelines"
        ],
        burden_holder="Oncologist or ordering physician",
        adversary_position="Tumor markers lack specificity and may yield false positives",
        counter_arguments=[
            "Use as adjunct to other diagnostic modalities",
            "Serial trends improve utility",
            "Counsel on limitations"
        ],
        resolution_strategy="Integrate with clinical, imaging, and histopathologic data.",
        entity_scope="Patients with known or suspected malignancy",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="ASCO Guidelines"
    ),
    DoctrineBlock(
        topic="Iron Studies: Ferritin, TIBC, Transferrin Saturation",
        keywords=["iron studies", "ferritin", "TIBC", "transferrin", "iron deficiency", "anemia"],
        conclusion_template="Interpret iron studies to diagnose iron deficiency, overload, or anemia of chronic disease.",
        reasoning_framework="""
1. Ferritin: low in iron deficiency; acute phase reactant, may be elevated in inflammation.
2. Serum iron: low in iron deficiency or chronic disease; high in overload.
3. TIBC: high in iron deficiency; low in chronic disease.
4. Transferrin saturation: low in iron deficiency; high in overload.
5. Correlate with CBC and reticulocyte count.
6. Consider chronic inflammation, liver disease, or hemolysis.
7. Repeat testing if results equivocal.
8. Assess for GI blood loss in adults with iron deficiency.
9. Consider genetic testing for hemochromatosis if overload suspected.
10. Integrate with clinical findings and history.
""",
        key_factors=[
            "Ferritin, iron, TIBC, transferrin saturation",
            "CBC findings",
            "Inflammatory markers",
            "Clinical history",
            "Risk factors for blood loss or overload"
        ],
        primary_authority=[
            "UpToDate: Evaluation of anemia",
            "World Health Organization Guidelines",
            "Williams Hematology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Ferritin may be falsely elevated in inflammation",
        counter_arguments=[
            "Use multiple parameters for diagnosis",
            "Assess for acute phase response",
            "Repeat testing after inflammation resolves"
        ],
        resolution_strategy="Integrate all iron parameters and clinical context.",
        entity_scope="Patients with suspected anemia or iron overload",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Autoimmune Panel: ANA, anti-dsDNA, RF, CCP",
        keywords=["autoimmune", "ANA", "anti-dsDNA", "RF", "CCP", "lupus", "rheumatoid arthritis"],
        conclusion_template="Interpret autoimmune panel to diagnose or monitor systemic autoimmune diseases.",
        reasoning_framework="""
1. ANA: sensitive for SLE, but not specific; positive in other autoimmune diseases.
2. Anti-dsDNA: specific for SLE; correlates with disease activity.
3. RF: sensitive but not specific for RA; positive in other diseases.
4. Anti-CCP: highly specific for RA.
5. Interpret in clinical context; positive tests alone do not confirm diagnosis.
6. Consider titer and pattern of ANA.
7. Repeat testing if initial results equivocal.
8. Use additional antibodies as indicated (ENA, anti-Smith, anti-RNP).
9. Monitor for disease activity and response to therapy.
10. Counsel patients on implications and limitations.
""",
        key_factors=[
            "Antibody specificity and sensitivity",
            "Titer and pattern",
            "Clinical presentation",
            "Other laboratory findings",
            "Family history"
        ],
        primary_authority=[
            "American College of Rheumatology Guidelines",
            "UpToDate: Interpretation of autoimmune serologies",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Rheumatologist or ordering physician",
        adversary_position="Positive serology without symptoms may not indicate disease",
        counter_arguments=[
            "Correlate with clinical findings",
            "Repeat or expand testing",
            "Monitor for disease development"
        ],
        resolution_strategy="Integrate serology with clinical and other laboratory data.",
        entity_scope="Patients with suspected autoimmune disease",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="ACR Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatitis Serology: HBsAg, anti-HBs, anti-HCV",
        keywords=["hepatitis", "serology", "HBsAg", "anti-HBs", "anti-HCV", "chronic hepatitis"],
        conclusion_template="Interpret hepatitis serology to diagnose acute, chronic, or resolved infection.",
        reasoning_framework="""
1. HBsAg: indicates active hepatitis B infection.
2. Anti-HBs: indicates immunity (vaccination or recovery).
3. Anti-HBc: indicates prior or current infection.
4. IgM anti-HBc: acute infection.
5. HBeAg and anti-HBe: assess infectivity.
6. Anti-HCV: screening for hepatitis C; confirm with HCV RNA.
7. Interpret combinations to distinguish acute, chronic, resolved, or vaccinated status.
8. Repeat testing if results discordant.
9. Counsel on transmission and management.
10. Consider risk factors and clinical presentation.
""",
        key_factors=[
            "Pattern of serologic markers",
            "Clinical history and risk factors",
            "Liver function tests",
            "HCV RNA confirmation",
            "Vaccination status"
        ],
        primary_authority=[
            "CDC Guidelines for Viral Hepatitis",
            "UpToDate: Interpretation of hepatitis serology",
            "AASLD Guidelines"
        ],
        burden_holder="Ordering clinician",
        adversary_position="False positives or negatives may occur",
        counter_arguments=[
            "Repeat or confirmatory testing",
            "Correlate with clinical findings",
            "Use nucleic acid testing if needed"
        ],
        resolution_strategy="Integrate serology with clinical and laboratory data.",
        entity_scope="Patients with risk factors or abnormal liver tests",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CDC Guidelines"
    ),
    DoctrineBlock(
        topic="HIV Testing Algorithm: 4th Generation Combo",
        keywords=["HIV", "testing", "4th generation", "antigen", "antibody", "window period"],
        conclusion_template="Use 4th generation HIV test for early detection; confirm positives with supplemental testing.",
        reasoning_framework="""
1. 4th generation tests detect HIV-1/2 antibodies and p24 antigen; window period ~2 weeks.
2. Reactive screening requires confirmatory differentiation assay.
3. Indeterminate results may require nucleic acid testing (NAT).
4. Negative test does not exclude infection if within window period.
5. Counsel on risk reduction and retesting if recent exposure.
6. Use rapid tests for point-of-care, but confirm positives.
7. Document consent and provide pre/post-test counseling.
8. Repeat testing for high-risk individuals.
9. Report results per public health requirements.
10. Integrate with clinical presentation and risk assessment.
""",
        key_factors=[
            "Test type and timing",
            "Risk factors and exposure history",
            "Confirmatory testing",
            "Counseling and consent",
            "Reporting requirements"
        ],
        primary_authority=[
            "CDC HIV Testing Guidelines",
            "UpToDate: HIV testing and diagnosis",
            "World Health Organization HIV Testing Guidelines"
        ],
        burden_holder="Ordering clinician or public health provider",
        adversary_position="False negatives possible during window period",
        counter_arguments=[
            "Repeat testing after window period",
            "Use NAT if acute infection suspected",
            "Counsel on ongoing risk"
        ],
        resolution_strategy="Follow algorithm and retest as indicated.",
        entity_scope="Individuals at risk for HIV",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="CDC HIV Testing Algorithm"
    ),
    DoctrineBlock(
        topic="Drug Screening: Immunoassay and GC-MS Confirmation",
        keywords=["drug screening", "immunoassay", "GC-MS", "toxicology", "false positive"],
        conclusion_template="Use immunoassay for initial drug screening; confirm positives with GC-MS.",
        reasoning_framework="""
1. Immunoassays are rapid but may yield false positives (cross-reactivity).
2. GC-MS is gold standard for confirmation.
3. Interpret results in clinical context (symptoms, exposure history).
4. Document chain of custody for forensic cases.
5. Consider detection windows for different substances.
6. Counsel patients on limitations and implications.
7. Repeat or expand testing if results unexpected.
8. Use confirmatory testing before making clinical or legal decisions.
9. Communicate results promptly to care team.
10. Monitor for withdrawal or toxicity as indicated.
""",
        key_factors=[
            "Test method and specificity",
            "Clinical context",
            "Chain of custody",
            "Detection window",
            "Confirmatory testing"
        ],
        primary_authority=[
            "SAMHSA Guidelines for Drug Testing",
            "UpToDate: Drug screening in clinical practice",
            "Goldfrank's Toxicologic Emergencies"
        ],
        burden_holder="Ordering clinician or toxicologist",
        adversary_position="Immunoassay false positives may lead to misdiagnosis",
        counter_arguments=[
            "Confirm with GC-MS",
            "Correlate with clinical findings",
            "Repeat testing if necessary"
        ],
        resolution_strategy="Confirm all positives with GC-MS before action.",
        entity_scope="Patients with suspected substance use or overdose",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SAMHSA Guidelines"
    ),
    DoctrineBlock(
        topic="Molecular Diagnostics: PCR, FISH, NGS",
        keywords=["molecular diagnostics", "PCR", "FISH", "NGS", "genetic testing", "mutation"],
        conclusion_template="Use molecular diagnostics for pathogen detection, genetic mutations, and cancer profiling.",
        reasoning_framework="""
1. PCR: highly sensitive for pathogen detection (viruses, bacteria, fungi).
2. FISH: detects chromosomal abnormalities (leukemia, lymphoma).
3. NGS: broad genetic profiling for inherited or somatic mutations.
4. Interpret in clinical context; positive result does not always indicate disease.
5. Confirm unexpected findings with alternative methods.
6. Counsel patients on implications of genetic results.
7. Document consent for genetic testing.
8. Use results to guide targeted therapy or prognosis.
9. Consider incidental findings and ethical implications.
10. Integrate with other laboratory and clinical data.
""",
        key_factors=[
            "Test method and sensitivity",
            "Clinical indication",
            "Consent and counseling",
            "Confirmation of results",
            "Therapeutic implications"
        ],
        primary_authority=[
            "ACMG Guidelines for Genetic Testing",
            "UpToDate: Molecular diagnostics in clinical practice",
            "WHO Guidelines on Molecular Diagnostics"
        ],
        burden_holder="Geneticist or ordering physician",
        adversary_position="Variants of uncertain significance may cause confusion",
        counter_arguments=[
            "Use expert interpretation",
            "Correlate with phenotype",
            "Provide genetic counseling"
        ],
        resolution_strategy="Consult genetics and use multidisciplinary approach.",
        entity_scope="Patients undergoing molecular testing",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="ACMG Guidelines"
    ),
    DoctrineBlock(
        topic="Flow Cytometry: Immunophenotyping in Lymphoma/Leukemia",
        keywords=["flow cytometry", "immunophenotyping", "lymphoma", "leukemia", "CD markers"],
        conclusion_template="Use flow cytometry to classify hematologic malignancies and guide therapy.",
        reasoning_framework="""
1. Flow cytometry identifies cell surface and cytoplasmic markers (CD antigens).
2. Distinguishes between B-cell, T-cell, and myeloid neoplasms.
3. Guides diagnosis, prognosis, and treatment selection.
4. Requires adequate sample and proper handling.
5. Correlate with morphology, cytogenetics, and molecular studies.
6. Repeat testing if initial results inconclusive.
7. Use standardized panels for common malignancies.
8. Interpret in context of clinical and laboratory findings.
9. Document findings in pathology report.
10. Consult hematopathology for complex cases.
""",
        key_factors=[
            "Immunophenotypic profile",
            "Sample quality",
            "Correlation with morphology",
            "Clinical presentation",
            "Standardized panels"
        ],
        primary_authority=[
            "WHO Classification of Tumours of Haematopoietic and Lymphoid Tissues",
            "UpToDate: Flow cytometry in hematologic malignancies",
            "College of American Pathologists Guidelines"
        ],
        burden_holder="Hematopathologist",
        adversary_position="Immunophenotype may overlap between entities",
        counter_arguments=[
            "Use integrated diagnostic approach",
            "Repeat or expand panel if needed",
            "Correlate with clinical data"
        ],
        resolution_strategy="Multidisciplinary review and consensus diagnosis.",
        entity_scope="Patients with suspected hematologic malignancy",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="WHO Classification"
    ),
    # Additional doctrine blocks to reach 40+ (abbreviated for brevity)
    DoctrineBlock(
        topic="Erythrocyte Sedimentation Rate (ESR) and C-Reactive Protein (CRP)",
        keywords=["ESR", "CRP", "inflammation", "acute phase reactants"],
        conclusion_template="Use ESR and CRP as nonspecific markers of inflammation.",
        reasoning_framework="""
1. ESR and CRP rise in response to inflammation, infection, or tissue injury.
2. CRP rises and falls more rapidly than ESR.
3. High ESR/CRP suggest active inflammation but do not localize disease.
4. Use to monitor disease activity in rheumatologic conditions.
5. Mild elevations may be nonspecific.
6. Consider age, anemia, and other factors affecting ESR.
7. Correlate with clinical findings and other labs.
8. Repeat testing to monitor trends.
9. Do not use as sole diagnostic tool.
10. Counsel patients on limitations.
""",
        key_factors=[
            "Degree of elevation",
            "Clinical context",
            "Other inflammatory markers",
            "Trends over time",
            "Underlying disease"
        ],
        primary_authority=[
            "UpToDate: Acute phase reactants",
            "ACR Guidelines",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Nonspecificity may lead to overdiagnosis",
        counter_arguments=[
            "Use in conjunction with other data",
            "Monitor trends, not single values",
            "Correlate with clinical findings"
        ],
        resolution_strategy="Use as adjunctive markers only.",
        entity_scope="Patients with suspected inflammation",
        confidence=0.94,
        confidence_zone="Moderate",
        controlling_precedent="ACR Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Protein Electrophoresis (SPEP) and Immunofixation",
        keywords=["SPEP", "immunofixation", "monoclonal gammopathy", "multiple myeloma"],
        conclusion_template="Use SPEP and immunofixation to detect monoclonal gammopathies.",
        reasoning_framework="""
1. SPEP separates serum proteins into fractions; M-spike indicates monoclonal protein.
2. Immunofixation identifies immunoglobulin type.
3. Use in diagnosis and monitoring of multiple myeloma, MGUS, and related disorders.
4. Correlate with clinical findings (anemia, bone pain, renal dysfunction).
5. Quantify M-protein for disease burden.
6. Repeat testing to monitor progression.
7. Consider urine protein electrophoresis for light chains.
8. Integrate with bone marrow biopsy and imaging.
9. Counsel patients on implications.
10. Use standardized reporting.
""",
        key_factors=[
            "Presence and size of M-spike",
            "Immunoglobulin type",
            "Clinical features",
            "Other laboratory findings",
            "Disease progression"
        ],
        primary_authority=[
            "IMWG Guidelines",
            "UpToDate: Monoclonal gammopathy",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Hematologist",
        adversary_position="Small M-spike may be benign (MGUS)",
        counter_arguments=[
            "Monitor over time",
            "Correlate with symptoms",
            "Use additional diagnostics"
        ],
        resolution_strategy="Serial monitoring and multidisciplinary evaluation.",
        entity_scope="Patients with suspected monoclonal gammopathy",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IMWG Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Calcium and Parathyroid Function",
        keywords=["calcium", "parathyroid", "PTH", "hypercalcemia", "hypocalcemia"],
        conclusion_template="Interpret serum calcium and PTH to diagnose disorders of calcium metabolism.",
        reasoning_framework="""
1. Correct total calcium for albumin level.
2. Hypercalcemia: consider primary hyperparathyroidism, malignancy, vitamin D intoxication.
3. Hypocalcemia: consider hypoparathyroidism, CKD, vitamin D deficiency.
4. Measure PTH to distinguish PTH-mediated from non-PTH-mediated hypercalcemia.
5. Assess for symptoms (stones, bones, groans, psychiatric overtones).
6. Consider additional labs (phosphate, vitamin D, magnesium).
7. Repeat testing to confirm abnormalities.
8. Correlate with clinical findings.
9. Monitor for complications (arrhythmias, seizures).
10. Refer to endocrinology if unclear.
""",
        key_factors=[
            "Corrected calcium",
            "PTH level",
            "Clinical symptoms",
            "Associated lab findings",
            "Underlying conditions"
        ],
        primary_authority=[
            "Endocrine Society Guidelines",
            "UpToDate: Disorders of calcium metabolism",
            "Williams Textbook of Endocrinology"
        ],
        burden_holder="Ordering clinician or endocrinologist",
        adversary_position="Albumin changes may confound total calcium",
        counter_arguments=[
            "Use ionized calcium if available",
            "Correct for albumin",
            "Repeat testing"
        ],
        resolution_strategy="Integrate with clinical and laboratory context.",
        entity_scope="Patients with abnormal calcium",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Endocrine Society Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Osmolality and Osmolar Gap",
        keywords=["osmolality", "osmolar gap", "toxic alcohols", "hyponatremia", "hypernatremia"],
        conclusion_template="Use serum osmolality and osmolar gap to evaluate water balance and toxic ingestions.",
        reasoning_framework="""
1. Calculate osmolality: 2[Na] + glucose/18 + BUN/2.8.
2. Measured osmolality > calculated by >10 = osmolar gap.
3. Elevated gap suggests toxic alcohols (methanol, ethylene glycol).
4. Assess for symptoms (confusion, ataxia, visual changes).
5. Correlate with anion gap and acid-base status.
6. Use in evaluation of hyponatremia/hypernatremia.
7. Repeat testing to monitor therapy.
8. Integrate with clinical history.
9. Consult toxicology if ingestion suspected.
10. Use as adjunct to other diagnostics.
""",
        key_factors=[
            "Measured and calculated osmolality",
            "Osmolar gap",
            "Clinical presentation",
            "Associated labs",
            "Exposure history"
        ],
        primary_authority=[
            "Goldfrank's Toxicologic Emergencies",
            "UpToDate: Osmolality and osmolar gap",
            "American Association of Poison Control Centers"
        ],
        burden_holder="Ordering clinician or toxicologist",
        adversary_position="Osmolar gap may be elevated in other conditions",
        counter_arguments=[
            "Correlate with exposure history",
            "Repeat testing",
            "Use confirmatory diagnostics"
        ],
        resolution_strategy="Integrate with clinical and laboratory context.",
        entity_scope="Patients with altered mental status or suspected ingestion",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAPCC Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Amylase and Lipase in Pancreatitis",
        keywords=["amylase", "lipase", "pancreatitis", "abdominal pain"],
        conclusion_template="Use serum amylase and lipase to diagnose acute pancreatitis.",
        reasoning_framework="""
1. Lipase is more specific and remains elevated longer than amylase.
2. Elevation >3x upper limit of normal supports diagnosis.
3. Consider timing of symptom onset.
4. Mild elevations may occur in other conditions (renal failure, perforation).
5. Correlate with clinical findings (epigastric pain, nausea, vomiting).
6. Use imaging (CT, US) to confirm and assess complications.
7. Repeat testing if diagnosis uncertain.
8. Monitor for complications (necrosis, pseudocyst).
9. Counsel on alcohol and gallstone risk factors.
10. Document findings and management plan.
""",
        key_factors=[
            "Degree of enzyme elevation",
            "Timing relative to symptoms",
            "Clinical presentation",
            "Imaging findings",
            "Risk factors"
        ],
        primary_authority=[
            "American College of Gastroenterology Guidelines",
            "UpToDate: Diagnosis of acute pancreatitis",
            "Sleisenger and Fordtran's Gastrointestinal and Liver Disease"
        ],
        burden_holder="Ordering clinician or gastroenterologist",
        adversary_position="Mild elevations are nonspecific",
        counter_arguments=[
            "Use clinical criteria",
            "Confirm with imaging",
            "Repeat testing"
        ],
        resolution_strategy="Integrate lab, clinical, and imaging data.",
        entity_scope="Patients with abdominal pain",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ACG Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Lactate in Sepsis and Shock",
        keywords=["lactate", "sepsis", "shock", "tissue hypoperfusion"],
        conclusion_template="Use serum lactate to assess severity and guide resuscitation in sepsis and shock.",
        reasoning_framework="""
1. Elevated lactate indicates tissue hypoperfusion or impaired clearance.
2. Use as marker of severity and prognosis.
3. Serial measurements guide resuscitation and therapy.
4. Consider other causes (seizure, liver failure, metformin).
5. Correlate with clinical findings and other labs.
6. Initiate early goal-directed therapy if elevated.
7. Repeat testing to assess response.
8. Integrate with SOFA or qSOFA scores.
9. Document trends and management.
10. Consult critical care as indicated.
""",
        key_factors=[
            "Degree and trend of lactate elevation",
            "Clinical context",
            "Other causes of elevation",
            "Response to therapy",
            "Severity scores"
        ],
        primary_authority=[
            "Surviving Sepsis Campaign Guidelines",
            "UpToDate: Lactate in sepsis",
            "Society of Critical Care Medicine"
        ],
        burden_holder="Critical care provider",
        adversary_position="Lactate may be elevated for non-septic reasons",
        counter_arguments=[
            "Correlate with clinical findings",
            "Repeat testing",
            "Assess for alternative causes"
        ],
        resolution_strategy="Use as adjunct to clinical assessment.",
        entity_scope="Patients with suspected sepsis or shock",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Surviving Sepsis Campaign"
    ),
    DoctrineBlock(
        topic="Serum Procalcitonin in Infection",
        keywords=["procalcitonin", "infection", "sepsis", "antibiotic stewardship"],
        conclusion_template="Use procalcitonin to support diagnosis of bacterial infection and guide antibiotic therapy.",
        reasoning_framework="""
1. Procalcitonin rises in bacterial infection; low in viral or non-infectious inflammation.
2. Use as adjunct to clinical and laboratory findings.
3. Serial measurements guide initiation and discontinuation of antibiotics.
4. Not a stand-alone diagnostic test.
5. Consider renal dysfunction and other factors affecting levels.
6. Use in antibiotic stewardship programs.
7. Repeat testing to monitor trends.
8. Integrate with clinical severity scores.
9. Document rationale for antibiotic decisions.
10. Counsel on limitations.
""",
        key_factors=[
            "Degree and trend of elevation",
            "Clinical context",
            "Other causes of elevation",
            "Antibiotic use",
            "Severity of illness"
        ],
        primary_authority=[
            "UpToDate: Procalcitonin in infection",
            "Surviving Sepsis Campaign",
            "Infectious Diseases Society of America"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Procalcitonin may be elevated in non-infectious states",
        counter_arguments=[
            "Correlate with clinical findings",
            "Repeat testing",
            "Use as adjunct, not replacement"
        ],
        resolution_strategy="Integrate with other data for decision-making.",
        entity_scope="Patients with suspected bacterial infection",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="IDSA Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Creatine Kinase (CK) in Rhabdomyolysis",
        keywords=["CK", "rhabdomyolysis", "muscle injury", "myoglobinuria"],
        conclusion_template="Use CK to diagnose and monitor rhabdomyolysis.",
        reasoning_framework="""
1. CK rises rapidly after muscle injury; peaks in 24-72 hours.
2. Levels >5x normal suggest rhabdomyolysis.
3. Correlate with clinical findings (muscle pain, weakness, dark urine).
4. Monitor for complications (AKI, hyperkalemia).
5. Repeat testing to assess trend.
6. Assess for causes (trauma, drugs, seizures, exercise).
7. Monitor renal function and electrolytes.
8. Initiate aggressive hydration if rhabdomyolysis confirmed.
9. Document findings and management.
10. Consult nephrology if AKI develops.
""",
        key_factors=[
            "Degree and trend of CK elevation",
            "Clinical presentation",
            "Renal function",
            "Electrolyte abnormalities",
            "Etiology of muscle injury"
        ],
        primary_authority=[
            "UpToDate: Rhabdomyolysis",
            "American Society of Nephrology",
            "Goldman-Cecil Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="CK may be mildly elevated in exercise or trauma",
        counter_arguments=[
            "Use clinical criteria",
            "Monitor for complications",
            "Repeat testing"
        ],
        resolution_strategy="Integrate lab and clinical findings.",
        entity_scope="Patients with muscle injury or symptoms",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASN Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Uric Acid in Gout and Tumor Lysis",
        keywords=["uric acid", "gout", "tumor lysis", "hyperuricemia"],
        conclusion_template="Use uric acid to diagnose gout and monitor tumor lysis syndrome.",
        reasoning_framework="""
1. Hyperuricemia supports diagnosis of gout but is not specific.
2. Use in monitoring tumor lysis in chemotherapy.
3. Correlate with clinical findings (joint pain, swelling).
4. Repeat testing to monitor therapy.
5. Consider renal function and medications.
6. Use uric acid lowering therapy as indicated.
7. Monitor for complications (nephropathy).
8. Document findings and management.
9. Counsel on dietary and medication factors.
10. Use as adjunct to clinical diagnosis.
""",
        key_factors=[
            "Degree of uric acid elevation",
            "Clinical presentation",
            "Renal function",
            "Therapy response",
            "Risk factors"
        ],
        primary_authority=[
            "ACR Guidelines for Gout",
            "UpToDate: Uric acid disorders",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Hyperuricemia may be asymptomatic",
        counter_arguments=[
            "Correlate with symptoms",
            "Monitor for complications",
            "Repeat testing"
        ],
        resolution_strategy="Use as adjunct to clinical assessment.",
        entity_scope="Patients with gout or at risk for tumor lysis",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ACR Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Vitamin B12 and Folate in Anemia",
        keywords=["B12", "folate", "anemia", "macrocytosis", "neuropathy"],
        conclusion_template="Use B12 and folate to diagnose macrocytic anemia and prevent complications.",
        reasoning_framework="""
1. Low B12 or folate causes macrocytic anemia and neurologic symptoms.
2. Assess for risk factors (malabsorption, diet, medications).
3. Repeat testing if results equivocal.
4. Correlate with CBC and reticulocyte count.
5. Consider methylmalonic acid and homocysteine for confirmation.
6. Initiate replacement therapy if deficient.
7. Monitor response to therapy.
8. Counsel on dietary sources and adherence.
9. Document findings and management.
10. Screen for other deficiencies if indicated.
""",
        key_factors=[
            "B12 and folate levels",
            "CBC findings",
            "Clinical symptoms",
            "Risk factors",
            "Therapeutic response"
        ],
        primary_authority=[
            "WHO Guidelines on Anemia",
            "UpToDate: Macrocytic anemia",
            "Williams Hematology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Borderline values may be inconclusive",
        counter_arguments=[
            "Use additional markers",
            "Repeat testing",
            "Correlate with clinical findings"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with macrocytic anemia or neuropathy",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="WHO Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Albumin in Nutritional and Hepatic Assessment",
        keywords=["albumin", "nutrition", "liver function", "hypoalbuminemia"],
        conclusion_template="Use serum albumin to assess nutritional and hepatic status.",
        reasoning_framework="""
1. Low albumin suggests chronic liver disease, nephrotic syndrome, or malnutrition.
2. Not a marker of acute nutritional status.
3. Correlate with clinical findings and other labs.
4. Repeat testing to monitor trends.
5. Assess for edema, ascites, or other complications.
6. Consider acute phase response (albumin is negative acute phase reactant).
7. Integrate with prealbumin and transferrin if indicated.
8. Document findings and management.
9. Counsel on dietary and disease factors.
10. Refer to nutrition or hepatology as needed.
""",
        key_factors=[
            "Degree of hypoalbuminemia",
            "Clinical context",
            "Other laboratory findings",
            "Trends over time",
            "Underlying disease"
        ],
        primary_authority=[
            "UpToDate: Albumin in clinical practice",
            "AASLD Guidelines",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Albumin is not a marker of acute nutrition",
        counter_arguments=[
            "Use with other markers",
            "Correlate with clinical findings",
            "Repeat testing"
        ],
        resolution_strategy="Use as adjunct to broader assessment.",
        entity_scope="Patients with chronic disease or malnutrition",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="AASLD Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Total Protein and Globulin Gap",
        keywords=["total protein", "globulin gap", "hypogammaglobulinemia", "hypergammaglobulinemia"],
        conclusion_template="Use total protein and globulin gap to screen for gammopathies and immune disorders.",
        reasoning_framework="""
1. Total protein = albumin + globulins.
2. Elevated gap (>4 g/dL) suggests polyclonal or monoclonal gammopathy.
3. Low total protein may indicate immunodeficiency or protein loss.
4. Correlate with SPEP, immunofixation, and clinical findings.
5. Repeat testing to monitor trends.
6. Assess for symptoms (infections, edema).
7. Integrate with other laboratory data.
8. Document findings and management.
9. Counsel on implications.
10. Refer to hematology or immunology as needed.
""",
        key_factors=[
            "Degree of elevation or reduction",
            "Clinical context",
            "Other laboratory findings",
            "Trends over time",
            "Underlying disease"
        ],
        primary_authority=[
            "UpToDate: Serum protein and globulin gap",
            "IMWG Guidelines",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Globulin gap is nonspecific",
        counter_arguments=[
            "Use as screening tool",
            "Correlate with other findings",
            "Repeat testing"
        ],
        resolution_strategy="Use as adjunct to further diagnostics.",
        entity_scope="Patients with abnormal protein levels",
        confidence=0.94,
        confidence_zone="Moderate",
        controlling_precedent="IMWG Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Bilirubin: Direct and Indirect",
        keywords=["bilirubin", "direct", "indirect", "jaundice", "hemolysis"],
        conclusion_template="Interpret direct and indirect bilirubin to differentiate causes of jaundice.",
        reasoning_framework="""
1. Indirect (unconjugated) bilirubin: elevated in hemolysis, Gilbert's syndrome.
2. Direct (conjugated) bilirubin: elevated in cholestasis, hepatitis.
3. Assess for clinical findings (jaundice, dark urine, pale stools).
4. Correlate with liver enzymes and hemolysis labs.
5. Repeat testing to monitor trends.
6. Use imaging if obstruction suspected.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to hepatology or hematology as needed.
10. Integrate with other laboratory data.
""",
        key_factors=[
            "Pattern of bilirubin elevation",
            "Clinical presentation",
            "Associated laboratory findings",
            "Imaging results",
            "Underlying disease"
        ],
        primary_authority=[
            "AASLD Guidelines",
            "UpToDate: Bilirubin metabolism",
            "Zakim and Boyer's Hepatology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Mild isolated indirect hyperbilirubinemia may be benign",
        counter_arguments=[
            "Correlate with clinical findings",
            "Repeat testing",
            "Use additional diagnostics"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with jaundice or abnormal bilirubin",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AASLD Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Electrolytes: Magnesium and Phosphate",
        keywords=["magnesium", "phosphate", "electrolytes", "hypomagnesemia", "hypophosphatemia"],
        conclusion_template="Interpret magnesium and phosphate to diagnose and manage electrolyte disorders.",
        reasoning_framework="""
1. Hypomagnesemia: common in alcoholism, diuretics, GI loss; causes arrhythmias, neuromuscular symptoms.
2. Hypermagnesemia: rare, usually in renal failure.
3. Hypophosphatemia: seen in refeeding, DKA, alcoholism; causes weakness, respiratory failure.
4. Hyperphosphatemia: in CKD, tumor lysis.
5. Correlate with other electrolytes and clinical findings.
6. Repeat testing to monitor therapy.
7. Document findings and management.
8. Counsel on dietary and medication factors.
9. Refer to nephrology if persistent or severe.
10. Integrate with overall metabolic assessment.
""",
        key_factors=[
            "Degree of electrolyte abnormality",
            "Clinical symptoms",
            "Associated laboratory findings",
            "Therapeutic response",
            "Underlying conditions"
        ],
        primary_authority=[
            "National Kidney Foundation Guidelines",
            "UpToDate: Disorders of magnesium and phosphate",
            "Goldman-Cecil Medicine"
        ],
        burden_holder="Ordering clinician or nephrologist",
        adversary_position="Mild abnormalities may be asymptomatic",
        counter_arguments=[
            "Monitor for symptoms",
            "Repeat testing",
            "Correlate with clinical findings"
        ],
        resolution_strategy="Integrate with clinical and laboratory context.",
        entity_scope="Patients with electrolyte disorders",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NKF Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Transaminases: AST and ALT",
        keywords=["AST", "ALT", "transaminases", "liver injury", "hepatitis"],
        conclusion_template="Use AST and ALT to assess hepatocellular injury.",
        reasoning_framework="""
1. ALT is more liver-specific than AST.
2. Marked elevation (>1000 U/L) suggests acute hepatitis (viral, ischemic, toxin).
3. Mild-moderate elevation: consider NAFLD, alcohol, medications.
4. AST>ALT suggests alcoholic liver disease.
5. Correlate with clinical findings and history.
6. Repeat testing to monitor trends.
7. Use in conjunction with other liver tests.
8. Document findings and management.
9. Counsel on risk factors and follow-up.
10. Refer to hepatology if unclear.
""",
        key_factors=[
            "Degree and pattern of elevation",
            "Clinical context",
            "Associated laboratory findings",
            "Trends over time",
            "Risk factors"
        ],
        primary_authority=[
            "AASLD Guidelines",
            "UpToDate: Transaminase elevation",
            "Zakim and Boyer's Hepatology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Mild elevations may be nonspecific",
        counter_arguments=[
            "Monitor trends",
            "Correlate with clinical findings",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with abnormal liver enzymes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AASLD Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Alkaline Phosphatase (ALP) and Gamma-Glutamyl Transferase (GGT)",
        keywords=["ALP", "GGT", "cholestasis", "bone disease"],
        conclusion_template="Use ALP and GGT to differentiate hepatic from bone sources of elevation.",
        reasoning_framework="""
1. ALP elevated in cholestasis, bone disease, pregnancy.
2. GGT elevated in hepatic but not bone disease.
3. Use both to localize source of ALP elevation.
4. Correlate with clinical findings and other labs.
5. Repeat testing to monitor trends.
6. Use imaging if obstruction suspected.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to hepatology or endocrinology as needed.
10. Integrate with other laboratory data.
""",
        key_factors=[
            "Degree of ALP and GGT elevation",
            "Clinical context",
            "Associated laboratory findings",
            "Imaging results",
            "Underlying disease"
        ],
        primary_authority=[
            "AASLD Guidelines",
            "UpToDate: ALP and GGT",
            "Zakim and Boyer's Hepatology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="ALP may be elevated in multiple conditions",
        counter_arguments=[
            "Use GGT to localize",
            "Correlate with clinical findings",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with elevated ALP",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AASLD Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Troponin in Non-ACS Conditions",
        keywords=["troponin", "myocardial injury", "non-ACS", "renal failure"],
        conclusion_template="Interpret troponin elevation in non-ACS conditions with caution.",
        reasoning_framework="""
1. Troponin may be elevated in sepsis, renal failure, PE, myocarditis.
2. Clinical correlation is essential.
3. Use serial measurements to assess trend.
4. Do not diagnose MI based on troponin alone.
5. Correlate with ECG and symptoms.
6. Repeat testing if unclear.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to cardiology if needed.
10. Integrate with overall clinical assessment.
""",
        key_factors=[
            "Degree and trend of elevation",
            "Clinical context",
            "ECG findings",
            "Symptoms",
            "Underlying disease"
        ],
        primary_authority=[
            "ACC/AHA Guidelines",
            "UpToDate: Troponin elevation",
            "European Society of Cardiology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Troponin is not specific for MI",
        counter_arguments=[
            "Use clinical criteria",
            "Monitor trends",
            "Correlate with other findings"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with elevated troponin",
        confidence=0.95,
        confidence_zone="Moderate",
        controlling_precedent="ACC/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="Serum BNP and NT-proBNP in Heart Failure",
        keywords=["BNP", "NT-proBNP", "heart failure", "volume overload"],
        conclusion_template="Use BNP and NT-proBNP to support diagnosis and management of heart failure.",
        reasoning_framework="""
1. Elevated BNP/NT-proBNP indicates ventricular stretch and volume overload.
2. Use to support diagnosis in dyspnea.
3. Correlate with clinical findings and echocardiography.
4. Serial measurements guide therapy.
5. Levels affected by age, renal function, obesity.
6. Repeat testing to monitor trends.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to cardiology as needed.
10. Integrate with overall clinical assessment.
""",
        key_factors=[
            "Degree and trend of elevation",
            "Clinical context",
            "Echocardiography findings",
            "Renal function",
            "Therapeutic response"
        ],
        primary_authority=[
            "ACC/AHA Guidelines",
            "UpToDate: BNP in heart failure",
            "European Society of Cardiology"
        ],
        burden_holder="Ordering clinician",
        adversary_position="BNP may be elevated in renal failure or other conditions",
        counter_arguments=[
            "Correlate with clinical findings",
            "Monitor trends",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with suspected heart failure",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="Serum D-dimer in Thrombosis and DIC",
        keywords=["D-dimer", "thrombosis", "DIC", "PE", "DVT"],
        conclusion_template="Use D-dimer to rule out thrombosis in low-risk patients and monitor DIC.",
        reasoning_framework="""
1. D-dimer elevated in active clot breakdown.
2. High sensitivity, low specificity; many false positives.
3. Use to rule out PE/DVT in low pretest probability.
4. Use in diagnosis and monitoring of DIC.
5. Correlate with clinical findings and risk scores.
6. Repeat testing if indicated.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to hematology if needed.
10. Integrate with overall clinical assessment.
""",
        key_factors=[
            "Degree of elevation",
            "Clinical context",
            "Pretest probability",
            "Associated laboratory findings",
            "Underlying disease"
        ],
        primary_authority=[
            "ASH Guidelines",
            "UpToDate: D-dimer in thrombosis",
            "Harrison's Principles of Internal Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="D-dimer is nonspecific",
        counter_arguments=[
            "Use in appropriate clinical context",
            "Correlate with risk scores",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with suspected thrombosis or DIC",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASH Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Creatinine and Estimated GFR",
        keywords=["creatinine", "GFR", "renal function", "CKD"],
        conclusion_template="Use serum creatinine and eGFR to assess renal function.",
        reasoning_framework="""
1. Creatinine reflects glomerular filtration; affected by muscle mass, diet.
2. Use eGFR equations (CKD-EPI, MDRD) for estimation.
3. Serial measurements monitor progression.
4. Correlate with BUN, electrolytes, urinalysis.
5. Repeat testing to confirm abnormalities.
6. Assess for acute vs chronic changes.
7. Document findings and management.
8. Counsel on implications and follow-up.
9. Refer to nephrology if CKD or rapid decline.
10. Integrate with overall clinical assessment.
""",
        key_factors=[
            "Degree and trend of elevation",
            "eGFR calculation",
            "Clinical context",
            "Associated laboratory findings",
            "Underlying disease"
        ],
        primary_authority=[
            "National Kidney Foundation Guidelines",
            "UpToDate: Assessment of renal function",
            "Goldman-Cecil Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Creatinine affected by non-renal factors",
        counter_arguments=[
            "Use eGFR equations",
            "Correlate with clinical findings",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with suspected renal dysfunction",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NKF Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Bicarbonate in Acid-Base Disorders",
        keywords=["bicarbonate", "acid-base", "metabolic acidosis", "alkalosis"],
        conclusion_template="Use serum bicarbonate to assess and monitor acid-base disorders.",
        reasoning_framework="""
1. Low bicarbonate indicates metabolic acidosis or compensation for respiratory alkalosis.
2. High bicarbonate indicates metabolic alkalosis or compensation for respiratory acidosis.
3. Correlate with ABG and clinical findings.
4. Assess for underlying causes (DKA, renal failure, vomiting).
5. Repeat testing to monitor therapy.
6. Document findings and management.
7. Counsel on implications and follow-up.
8. Refer to nephrology or critical care as needed.
9. Integrate with overall metabolic assessment.
10. Use as adjunct to other laboratory data.
""",
        key_factors=[
            "Degree of abnormality",
            "Clinical context",
            "Associated laboratory findings",
            "Underlying disease",
            "Therapeutic response"
        ],
        primary_authority=[
            "UpToDate: Acid-base disorders",
            "American Society of Nephrology",
            "Goldman-Cecil Medicine"
        ],
        burden_holder="Ordering clinician",
        adversary_position="Bicarbonate may be affected by non-metabolic factors",
        counter_arguments=[
            "Correlate with ABG",
            "Monitor trends",
            "Repeat testing"
        ],
        resolution_strategy="Integrate all data for diagnosis.",
        entity_scope="Patients with acid-base disorders",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASN Guidelines"
    ),
    DoctrineBlock(
        topic="Serum Anion Gap in Metabolic Acidosis",
        keywords=["anion gap", "metabolic acidosis", "MUDPILES", "anion gap calculation"],
        conclusion_template="Use anion gap to differentiate causes of metabolic acidosis.",
        reasoning_framework="""
1. Calculate anion gap: Na - (Cl + HCO3).
2. High gap: MUDPILES (methanol, uremia, DKA, paraldehyde, isoniazid/iron, lactic acidosis, ethylene glycol, salicylates).
3. Normal gap: diarrhea, RTA.
4. Correlate with clinical findings and history.
5. Repeat testing to monitor therapy.
6. Document findings and management.
7. Counsel on implications and follow