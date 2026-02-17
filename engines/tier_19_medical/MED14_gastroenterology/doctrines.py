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
        topic="Upper Endoscopy: Barrett's Esophagus Identification",
        keywords=["upper endoscopy", "Barrett's esophagus", "columnar epithelium", "esophageal adenocarcinoma"],
        conclusion_template="Barrett's esophagus is diagnosed when salmon-colored mucosa extends ≥1 cm above the gastroesophageal junction and is confirmed by histology showing intestinal metaplasia.",
        reasoning_framework="""
        1. Review endoscopic images for salmon-colored mucosa above the gastroesophageal junction.
        2. Measure the circumferential and maximal extent using Prague criteria.
        3. Obtain biopsies from suspected areas and confirm intestinal metaplasia histologically.
        4. Exclude mimics (e.g., gastric inlet patch, erosive esophagitis).
        5. Assess risk factors: chronic GERD, male sex, age >50, obesity.
        6. Consider surveillance intervals based on dysplasia grade.
        7. Reference guidelines: AGA, ASGE, BSG.
        8. Document findings and rationale for diagnosis.
        """,
        key_factors=["Endoscopic appearance", "Histologic confirmation", "Prague criteria", "Risk factors"],
        primary_authority=["American Gastroenterological Association", "British Society of Gastroenterology"],
        burden_holder="Endoscopist",
        adversary_position="Columnar epithelium may be due to gastric inlet patch or inflammation",
        counter_arguments=["Histology may not confirm intestinal metaplasia", "Sampling error"],
        resolution_strategy="Repeat biopsies, expert pathology review, adherence to guidelines",
        entity_scope="Adult patients undergoing upper endoscopy",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AGA Clinical Practice Update 2020"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Helicobacter pylori Detection",
        keywords=["upper endoscopy", "Helicobacter pylori", "gastritis", "biopsy", "urease test"],
        conclusion_template="H. pylori infection is confirmed by positive rapid urease test, histology, or culture from gastric biopsies.",
        reasoning_framework="""
        1. Obtain biopsies from antrum and corpus during endoscopy.
        2. Perform rapid urease test and send samples for histology.
        3. Interpret positive test as evidence of infection.
        4. Consider false negatives in patients on PPIs, antibiotics, or bismuth.
        5. Use culture or PCR in refractory cases.
        6. Reference guidelines: Maastricht V/Florence Consensus, ACG.
        7. Document findings and recommend eradication therapy if positive.
        """,
        key_factors=["Biopsy site", "Test sensitivity", "Medication interference", "Clinical suspicion"],
        primary_authority=["Maastricht V/Florence Consensus", "American College of Gastroenterology"],
        burden_holder="Endoscopist",
        adversary_position="False negatives due to recent medication use",
        counter_arguments=["Sampling error", "Test sensitivity limitations"],
        resolution_strategy="Repeat testing after medication washout, alternative diagnostic methods",
        entity_scope="Patients with suspected gastritis or ulcer",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Maastricht V Consensus Report"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Gastric Cancer Staging",
        keywords=["upper endoscopy", "gastric cancer", "staging", "biopsy", "EUS"],
        conclusion_template="Gastric cancer staging requires endoscopic visualization, biopsy confirmation, and EUS for depth and nodal involvement.",
        reasoning_framework="""
        1. Identify suspicious lesions during endoscopy.
        2. Obtain multiple biopsies for histologic confirmation.
        3. Use endoscopic ultrasound (EUS) to assess tumor depth (T stage) and lymph node involvement (N stage).
        4. Reference AJCC staging system.
        5. Consider CT/PET for distant metastases.
        6. Document findings and multidisciplinary discussion.
        """,
        key_factors=["Lesion appearance", "Histology", "EUS findings", "AJCC staging"],
        primary_authority=["AJCC Cancer Staging Manual", "ASGE"],
        burden_holder="Endoscopist and pathologist",
        adversary_position="Sampling error, submucosal spread not visualized",
        counter_arguments=["Biopsy may miss cancer", "EUS operator variability"],
        resolution_strategy="Repeat biopsies, second opinion, multidisciplinary review",
        entity_scope="Patients with suspected gastric malignancy",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AJCC 8th Edition"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Polyp Classification and Management",
        keywords=["colonoscopy", "polyp", "adenoma", "sessile serrated", "management"],
        conclusion_template="Polyps are classified by histology and size; adenomas and sessile serrated polyps require removal and surveillance per guidelines.",
        reasoning_framework="""
        1. Identify and document polyp size, morphology, and location.
        2. Remove polyps using appropriate technique (snare, cold biopsy).
        3. Send for histology to classify as adenoma, hyperplastic, or sessile serrated.
        4. Reference US Multi-Society Task Force guidelines for surveillance intervals.
        5. Consider patient's family history and risk factors.
        6. Document findings and plan for follow-up.
        """,
        key_factors=["Polyp size", "Histology", "Morphology", "Location"],
        primary_authority=["US Multi-Society Task Force", "ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Incomplete resection, misclassification",
        counter_arguments=["Histology may be ambiguous", "Polyp fragmentation"],
        resolution_strategy="Repeat colonoscopy, expert pathology review",
        entity_scope="Patients undergoing colonoscopy",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="USMSTF 2020 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Surveillance After Polypectomy",
        keywords=["colonoscopy", "polypectomy", "surveillance", "adenoma", "interval"],
        conclusion_template="Surveillance intervals after polypectomy are determined by number, size, and histology of polyps removed.",
        reasoning_framework="""
        1. Review pathology report for number, size, and type of polyps.
        2. Reference USMSTF guidelines for recommended surveillance intervals.
        3. Adjust interval for high-risk features (villous histology, high-grade dysplasia).
        4. Consider patient comorbidities and family history.
        5. Document rationale for chosen interval.
        """,
        key_factors=["Number of polyps", "Size", "Histology", "High-risk features"],
        primary_authority=["US Multi-Society Task Force", "ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Interval may be too short or too long based on risk",
        counter_arguments=["Guidelines may not fit all patients", "Missed lesions"],
        resolution_strategy="Individualized risk assessment, guideline adherence",
        entity_scope="Patients post-polypectomy",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="USMSTF 2020 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Incomplete Colonoscopy Management",
        keywords=["colonoscopy", "incomplete", "management", "bowel prep", "anatomy"],
        conclusion_template="Incomplete colonoscopy requires repeat procedure or alternative imaging, depending on cause.",
        reasoning_framework="""
        1. Identify reason for incompleteness (poor prep, anatomy, technical difficulty).
        2. Assess risk of missed lesions.
        3. Consider repeat colonoscopy with improved prep or use CT colonography.
        4. Document findings and plan.
        5. Reference ASGE guidelines.
        """,
        key_factors=["Reason for incompleteness", "Risk of missed lesions", "Alternative imaging"],
        primary_authority=["ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Patient may refuse repeat procedure",
        counter_arguments=["Alternative imaging may miss flat lesions", "Radiation exposure"],
        resolution_strategy="Patient counseling, shared decision-making",
        entity_scope="Patients with incomplete colonoscopy",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="ASGE 2012 Position Statement"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Fibrosis Assessment",
        keywords=["chronic liver disease", "fibrosis", "assessment", "elastography", "biopsy"],
        conclusion_template="Fibrosis is staged by non-invasive elastography or liver biopsy, with clinical context guiding interpretation.",
        reasoning_framework="""
        1. Use transient elastography (FibroScan) or MR elastography for non-invasive assessment.
        2. Interpret values according to etiology (e.g., hepatitis C, NAFLD).
        3. Reference METAVIR or Ishak scoring for biopsy.
        4. Consider confounders: inflammation, cholestasis, congestion.
        5. Document findings and implications for management.
        """,
        key_factors=["Elastography value", "Biopsy score", "Clinical context", "Etiology"],
        primary_authority=["EASL", "AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Elastography may be confounded by acute inflammation",
        counter_arguments=["Biopsy sampling error", "Non-invasive test limitations"],
        resolution_strategy="Repeat testing, combine modalities, expert review",
        entity_scope="Patients with chronic liver disease",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EASL 2015 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Cirrhosis Diagnosis",
        keywords=["chronic liver disease", "cirrhosis", "diagnosis", "imaging", "biopsy"],
        conclusion_template="Cirrhosis is diagnosed by clinical, laboratory, imaging, and histologic findings.",
        reasoning_framework="""
        1. Assess clinical signs: ascites, encephalopathy, varices.
        2. Review labs: low platelets, elevated INR, low albumin.
        3. Imaging: nodular liver, splenomegaly, portal hypertension.
        4. Biopsy if diagnosis unclear.
        5. Reference AASLD guidelines.
        6. Document findings and rationale.
        """,
        key_factors=["Clinical signs", "Laboratory values", "Imaging", "Histology"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Early cirrhosis may lack overt findings",
        counter_arguments=["Imaging may be inconclusive", "Biopsy risks"],
        resolution_strategy="Serial assessment, multidisciplinary review",
        entity_scope="Patients with suspected cirrhosis",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Hepatic Encephalopathy Monitoring",
        keywords=["chronic liver disease", "hepatic encephalopathy", "monitoring", "ammonia", "mental status"],
        conclusion_template="Hepatic encephalopathy is monitored clinically, with ammonia levels as adjunct; management is guided by severity.",
        reasoning_framework="""
        1. Assess mental status using West Haven criteria.
        2. Monitor for precipitating factors (infection, GI bleeding, medications).
        3. Ammonia levels may support diagnosis but are not definitive.
        4. Reference AASLD guidelines for management.
        5. Document findings and interventions.
        """,
        key_factors=["Mental status", "Precipitating factors", "Ammonia level", "Severity"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Ammonia levels may not correlate with clinical severity",
        counter_arguments=["Other causes of altered mental status", "Lab variability"],
        resolution_strategy="Clinical assessment prioritized, treat precipitating factors",
        entity_scope="Patients with cirrhosis",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2014 Guidance"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Portal Hypertension Assessment",
        keywords=["chronic liver disease", "portal hypertension", "assessment", "HVPG", "varices"],
        conclusion_template="Portal hypertension is assessed by clinical signs, imaging, and hepatic venous pressure gradient (HVPG) measurement.",
        reasoning_framework="""
        1. Identify clinical signs: splenomegaly, ascites, varices.
        2. Use Doppler ultrasound or CT/MRI for portal vein patency and varices.
        3. HVPG measurement is gold standard but invasive.
        4. Reference Baveno VI Consensus.
        5. Document findings and management plan.
        """,
        key_factors=["Clinical signs", "Imaging", "HVPG", "Varices"],
        primary_authority=["Baveno VI Consensus", "AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Non-invasive tests may miss early portal hypertension",
        counter_arguments=["HVPG not widely available", "Imaging limitations"],
        resolution_strategy="Combine clinical and imaging findings, refer for HVPG if needed",
        entity_scope="Patients with chronic liver disease",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="Baveno VI Consensus"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Disease Activity Monitoring",
        keywords=["IBD", "Crohn's", "ulcerative colitis", "activity", "monitoring", "fecal calprotectin"],
        conclusion_template="IBD activity is monitored by symptoms, biomarkers (CRP, fecal calprotectin), and endoscopic findings.",
        reasoning_framework="""
        1. Assess patient-reported symptoms (stool frequency, bleeding, pain).
        2. Monitor CRP and fecal calprotectin for inflammation.
        3. Use endoscopy to assess mucosal healing.
        4. Reference ECCO and ACG guidelines.
        5. Document findings and adjust therapy as needed.
        """,
        key_factors=["Symptoms", "Biomarkers", "Endoscopic findings", "Therapy response"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Biomarkers may not correlate with symptoms",
        counter_arguments=["Endoscopy may not be feasible", "Non-specific symptoms"],
        resolution_strategy="Combine modalities, individualized assessment",
        entity_scope="Patients with IBD",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Escalation of Therapy",
        keywords=["IBD", "Crohn's", "ulcerative colitis", "therapy escalation", "biologics"],
        conclusion_template="Escalation of therapy is indicated for moderate to severe disease activity or failure of standard treatment.",
        reasoning_framework="""
        1. Assess disease activity and response to current therapy.
        2. Consider escalation to immunomodulators or biologics per guidelines.
        3. Reference ACG and ECCO recommendations.
        4. Monitor for adverse effects and contraindications.
        5. Document rationale and patient consent.
        """,
        key_factors=["Disease activity", "Response to therapy", "Contraindications", "Guidelines"],
        primary_authority=["ACG", "ECCO"],
        burden_holder="Gastroenterologist",
        adversary_position="Escalation may increase risk of infection or malignancy",
        counter_arguments=["Patient preference", "Cost", "Adverse effects"],
        resolution_strategy="Shared decision-making, risk-benefit analysis",
        entity_scope="Patients with IBD",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ACG 2021 Guidelines"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Surgical Referral Criteria",
        keywords=["IBD", "Crohn's", "ulcerative colitis", "surgery", "referral"],
        conclusion_template="Surgical referral is indicated for refractory disease, complications, or dysplasia/cancer.",
        reasoning_framework="""
        1. Identify refractory disease despite maximal medical therapy.
        2. Assess for complications: strictures, fistulas, perforation.
        3. Detect dysplasia or cancer on surveillance.
        4. Reference ECCO and ACG guidelines.
        5. Document rationale for referral.
        """,
        key_factors=["Refractory disease", "Complications", "Dysplasia/cancer", "Guidelines"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Surgery may be avoided with further medical therapy",
        counter_arguments=["Patient risk", "Quality of life", "Surgical complications"],
        resolution_strategy="Multidisciplinary discussion, patient counseling",
        entity_scope="Patients with IBD",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Screening in Cirrhosis",
        keywords=["hepatocellular carcinoma", "screening", "cirrhosis", "ultrasound", "AFP"],
        conclusion_template="HCC screening in cirrhosis is performed with ultrasound every 6 months, with or without AFP.",
        reasoning_framework="""
        1. Identify patients with cirrhosis eligible for screening.
        2. Schedule ultrasound every 6 months.
        3. Consider adding AFP for increased sensitivity.
        4. Reference AASLD guidelines.
        5. Document screening results and follow-up plan.
        """,
        key_factors=["Cirrhosis", "Ultrasound", "AFP", "Screening interval"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Ultrasound may miss small lesions",
        counter_arguments=["AFP sensitivity limitations", "Patient compliance"],
        resolution_strategy="Combine modalities, patient education",
        entity_scope="Patients with cirrhosis",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Diagnosis Criteria",
        keywords=["hepatocellular carcinoma", "diagnosis", "imaging", "biopsy", "LI-RADS"],
        conclusion_template="HCC is diagnosed by characteristic imaging findings (arterial enhancement, washout) or biopsy in indeterminate cases.",
        reasoning_framework="""
        1. Use multiphase CT or MRI to identify arterial enhancement and washout.
        2. Apply LI-RADS criteria for lesion categorization.
        3. Biopsy if imaging is indeterminate.
        4. Reference AASLD guidelines.
        5. Document findings and rationale.
        """,
        key_factors=["Imaging", "LI-RADS", "Biopsy", "Clinical context"],
        primary_authority=["AASLD", "LI-RADS"],
        burden_holder="Radiologist/Hepatologist",
        adversary_position="Imaging may be inconclusive",
        counter_arguments=["Biopsy risks", "Lesion heterogeneity"],
        resolution_strategy="Repeat imaging, multidisciplinary review",
        entity_scope="Patients with liver lesions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Gastroesophageal Reflux Disease: Diagnosis",
        keywords=["GERD", "diagnosis", "symptoms", "pH monitoring", "endoscopy"],
        conclusion_template="GERD is diagnosed by typical symptoms, response to therapy, and/or objective testing (pH monitoring, endoscopy).",
        reasoning_framework="""
        1. Assess symptoms: heartburn, regurgitation.
        2. Trial of PPI therapy for symptom relief.
        3. Use pH monitoring or endoscopy if diagnosis unclear.
        4. Reference ACG guidelines.
        5. Document findings and rationale.
        """,
        key_factors=["Symptoms", "Therapy response", "Objective testing"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Symptoms may be due to functional dyspepsia",
        counter_arguments=["Non-response to PPIs", "Non-specific symptoms"],
        resolution_strategy="Objective testing, alternative diagnosis consideration",
        entity_scope="Patients with suspected GERD",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Gastroesophageal Reflux Disease: Management",
        keywords=["GERD", "management", "PPI", "lifestyle", "surgery"],
        conclusion_template="GERD management includes lifestyle modification, PPI therapy, and surgical options for refractory cases.",
        reasoning_framework="""
        1. Recommend weight loss, dietary changes, head-of-bed elevation.
        2. Initiate PPI therapy for symptom control.
        3. Consider anti-reflux surgery for refractory cases.
        4. Reference ACG guidelines.
        5. Document interventions and outcomes.
        """,
        key_factors=["Lifestyle", "PPI", "Surgery", "Symptom control"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Long-term PPI risks",
        counter_arguments=["Patient preference", "Adverse effects", "Surgical complications"],
        resolution_strategy="Shared decision-making, risk-benefit analysis",
        entity_scope="Patients with GERD",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Celiac Disease: Diagnosis",
        keywords=["celiac disease", "diagnosis", "serology", "biopsy", "gluten"],
        conclusion_template="Celiac disease is diagnosed by positive serology and confirmatory duodenal biopsy showing villous atrophy.",
        reasoning_framework="""
        1. Screen with anti-tTG and EMA serology.
        2. Confirm diagnosis with duodenal biopsy (Marsh criteria).
        3. Ensure patient is consuming gluten prior to testing.
        4. Reference ACG guidelines.
        5. Document findings and rationale.
        """,
        key_factors=["Serology", "Biopsy", "Gluten exposure", "Marsh criteria"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Serology may be negative in IgA deficiency",
        counter_arguments=["Biopsy sampling error", "Non-specific histology"],
        resolution_strategy="Repeat testing, alternative serology, expert pathology review",
        entity_scope="Patients with suspected celiac disease",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Celiac Disease: Management",
        keywords=["celiac disease", "management", "gluten-free diet", "monitoring", "nutritional deficiencies"],
        conclusion_template="Management of celiac disease requires strict gluten-free diet, monitoring for nutritional deficiencies, and periodic serology.",
        reasoning_framework="""
        1. Educate patient on gluten-free diet.
        2. Monitor for adherence and symptom resolution.
        3. Check for nutritional deficiencies (iron, B12, folate, vitamin D).
        4. Repeat serology to assess response.
        5. Reference ACG guidelines.
        6. Document interventions and outcomes.
        """,
        key_factors=["Diet adherence", "Nutritional status", "Serology", "Symptom resolution"],
        primary_authority=["ACG"],
        burden_holder="Patient",
        adversary_position="Diet may be difficult to maintain",
        counter_arguments=["Hidden gluten exposure", "Persistent symptoms"],
        resolution_strategy="Dietitian referral, repeat education, alternative diagnosis consideration",
        entity_scope="Patients with celiac disease",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Acute Pancreatitis: Diagnosis",
        keywords=["acute pancreatitis", "diagnosis", "amylase", "lipase", "imaging"],
        conclusion_template="Acute pancreatitis is diagnosed by two of three criteria: abdominal pain, elevated amylase/lipase, and imaging findings.",
        reasoning_framework="""
        1. Assess for characteristic abdominal pain.
        2. Check amylase and lipase levels (>3x upper limit).
        3. Perform imaging (CT, MRI, ultrasound) for confirmation.
        4. Reference ACG guidelines.
        5. Document findings and rationale.
        """,
        key_factors=["Pain", "Enzyme levels", "Imaging", "Etiology"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Enzyme elevation may be due to other causes",
        counter_arguments=["Imaging may be inconclusive", "Atypical presentation"],
        resolution_strategy="Repeat testing, multidisciplinary review",
        entity_scope="Patients with suspected acute pancreatitis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACG 2019 Guidelines"
    ),
    DoctrineBlock(
        topic="Acute Pancreatitis: Severity Assessment",
        keywords=["acute pancreatitis", "severity", "Ranson", "APACHE II", "organ failure"],
        conclusion_template="Severity is assessed by clinical scoring systems (Ranson, APACHE II) and presence of organ failure or complications.",
        reasoning_framework="""
        1. Apply Ranson or APACHE II score on admission and at 48 hours.
        2. Monitor for organ failure (respiratory, renal, cardiovascular).
        3. Identify local complications (necrosis, pseudocyst).
        4. Reference ACG guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Scoring system", "Organ failure", "Complications", "Clinical course"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Scoring systems may not predict all outcomes",
        counter_arguments=["Rapid clinical deterioration", "Atypical presentation"],
        resolution_strategy="Serial assessment, multidisciplinary review",
        entity_scope="Patients with acute pancreatitis",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="ACG 2019 Guidelines"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Esophageal Varices Grading",
        keywords=["upper endoscopy", "esophageal varices", "grading", "portal hypertension"],
        conclusion_template="Esophageal varices are graded by size and appearance; grading guides management and surveillance intervals.",
        reasoning_framework="""
        1. Identify varices during endoscopy and grade as small, medium, or large.
        2. Assess for red wale signs or stigmata of recent bleeding.
        3. Reference Baveno VI and AASLD guidelines for surveillance and prophylaxis.
        4. Document findings and management plan.
        """,
        key_factors=["Varice size", "Red wale signs", "Portal hypertension", "Surveillance interval"],
        primary_authority=["Baveno VI Consensus", "AASLD"],
        burden_holder="Endoscopist",
        adversary_position="Grading may be subjective",
        counter_arguments=["Inter-observer variability", "Missed small varices"],
        resolution_strategy="Standardized grading, repeat endoscopy",
        entity_scope="Patients with portal hypertension",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Baveno VI Consensus"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Gastric Ulcer Biopsy Protocol",
        keywords=["upper endoscopy", "gastric ulcer", "biopsy", "malignancy"],
        conclusion_template="Gastric ulcers should be biopsied at multiple sites to exclude malignancy; repeat endoscopy if healing is incomplete.",
        reasoning_framework="""
        1. Obtain biopsies from ulcer edge and base.
        2. Send samples for histology to exclude cancer.
        3. Repeat endoscopy in 6-8 weeks if healing is incomplete.
        4. Reference ACG and ASGE guidelines.
        5. Document findings and rationale.
        """,
        key_factors=["Biopsy site", "Histology", "Healing", "Malignancy exclusion"],
        primary_authority=["ACG", "ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Biopsy may miss cancer",
        counter_arguments=["Sampling error", "Non-healing ulcers"],
        resolution_strategy="Repeat biopsies, expert pathology review",
        entity_scope="Patients with gastric ulcer",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Lynch Syndrome Surveillance",
        keywords=["colonoscopy", "Lynch syndrome", "surveillance", "hereditary cancer"],
        conclusion_template="Lynch syndrome patients require colonoscopy every 1-2 years starting at age 20-25.",
        reasoning_framework="""
        1. Identify patients with confirmed Lynch syndrome.
        2. Schedule colonoscopy every 1-2 years.
        3. Reference NCCN and USMSTF guidelines.
        4. Document findings and surveillance plan.
        """,
        key_factors=["Genetic diagnosis", "Surveillance interval", "Family history"],
        primary_authority=["NCCN", "USMSTF"],
        burden_holder="Gastroenterologist",
        adversary_position="Patient compliance may be low",
        counter_arguments=["Cost", "Access", "Psychological impact"],
        resolution_strategy="Patient education, genetic counseling",
        entity_scope="Patients with Lynch syndrome",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NCCN 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Familial Adenomatous Polyposis Management",
        keywords=["colonoscopy", "FAP", "management", "polypectomy", "surgery"],
        conclusion_template="FAP patients require frequent colonoscopy and consideration of prophylactic colectomy.",
        reasoning_framework="""
        1. Identify patients with FAP by genetic testing or clinical criteria.
        2. Schedule colonoscopy every 1-2 years.
        3. Consider prophylactic colectomy for extensive polyposis.
        4. Reference NCCN and USMSTF guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Genetic diagnosis", "Polyp burden", "Surgical indication"],
        primary_authority=["NCCN", "USMSTF"],
        burden_holder="Gastroenterologist",
        adversary_position="Surgery may be delayed",
        counter_arguments=["Patient preference", "Surgical risks"],
        resolution_strategy="Multidisciplinary discussion, patient counseling",
        entity_scope="Patients with FAP",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NCCN 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Hepatitis B Monitoring",
        keywords=["chronic liver disease", "hepatitis B", "monitoring", "HBV DNA", "ALT"],
        conclusion_template="Hepatitis B is monitored by HBV DNA, ALT, and HBeAg status; therapy is guided by viral load and liver injury.",
        reasoning_framework="""
        1. Check HBV DNA, ALT, and HBeAg status regularly.
        2. Reference EASL and AASLD guidelines for therapy initiation.
        3. Monitor for seroconversion and liver injury.
        4. Document findings and management plan.
        """,
        key_factors=["HBV DNA", "ALT", "HBeAg", "Seroconversion"],
        primary_authority=["EASL", "AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Viral load may fluctuate",
        counter_arguments=["ALT may be normal despite injury", "Serologic ambiguity"],
        resolution_strategy="Serial monitoring, combine modalities",
        entity_scope="Patients with chronic hepatitis B",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EASL 2017 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Hepatitis C Monitoring",
        keywords=["chronic liver disease", "hepatitis C", "monitoring", "HCV RNA", "fibrosis"],
        conclusion_template="Hepatitis C is monitored by HCV RNA, liver function, and fibrosis assessment; therapy response is measured by sustained virologic response.",
        reasoning_framework="""
        1. Check HCV RNA and liver function tests.
        2. Assess fibrosis by elastography or biopsy.
        3. Reference AASLD guidelines for therapy and SVR definition.
        4. Document findings and management plan.
        """,
        key_factors=["HCV RNA", "Liver function", "Fibrosis", "SVR"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Fibrosis may progress despite SVR",
        counter_arguments=["False negative RNA", "Biopsy risks"],
        resolution_strategy="Serial monitoring, combine modalities",
        entity_scope="Patients with chronic hepatitis C",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Colon Cancer Surveillance",
        keywords=["IBD", "colon cancer", "surveillance", "dysplasia", "colonoscopy"],
        conclusion_template="IBD patients require colonoscopy surveillance for dysplasia and cancer starting 8 years after diagnosis.",
        reasoning_framework="""
        1. Identify patients with IBD duration >8 years.
        2. Schedule colonoscopy every 1-2 years.
        3. Use chromoendoscopy for enhanced detection.
        4. Reference ECCO and ACG guidelines.
        5. Document findings and surveillance plan.
        """,
        key_factors=["Disease duration", "Surveillance interval", "Chromoendoscopy"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Surveillance may miss flat lesions",
        counter_arguments=["Patient compliance", "Cost", "Access"],
        resolution_strategy="Patient education, advanced imaging",
        entity_scope="Patients with IBD",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Post-Treatment Surveillance",
        keywords=["hepatocellular carcinoma", "post-treatment", "surveillance", "imaging", "recurrence"],
        conclusion_template="Post-treatment HCC surveillance includes imaging every 3-6 months for recurrence detection.",
        reasoning_framework="""
        1. Schedule multiphase CT or MRI every 3-6 months after treatment.
        2. Monitor AFP as adjunct.
        3. Reference AASLD guidelines.
        4. Document findings and follow-up plan.
        """,
        key_factors=["Imaging interval", "AFP", "Recurrence risk"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Recurrence may be missed between intervals",
        counter_arguments=["Imaging limitations", "AFP sensitivity"],
        resolution_strategy="Combine modalities, adjust interval for high-risk",
        entity_scope="Patients post-HCC treatment",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Gastroesophageal Reflux Disease: Complications Surveillance",
        keywords=["GERD", "complications", "Barrett's esophagus", "stricture", "surveillance"],
        conclusion_template="GERD complications (Barrett's, stricture) require endoscopic surveillance per guidelines.",
        reasoning_framework="""
        1. Identify patients with Barrett's esophagus or strictures.
        2. Schedule surveillance endoscopy per AGA/ACG guidelines.
        3. Document findings and management plan.
        """,
        key_factors=["Complication type", "Surveillance interval", "Guidelines"],
        primary_authority=["AGA", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Surveillance may be excessive",
        counter_arguments=["Patient compliance", "Cost"],
        resolution_strategy="Individualized risk assessment, guideline adherence",
        entity_scope="Patients with GERD complications",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGA 2020 Guidelines"
    ),
    DoctrineBlock(
        topic="Celiac Disease: Refractory Disease Evaluation",
        keywords=["celiac disease", "refractory", "evaluation", "biopsy", "malignancy"],
        conclusion_template="Refractory celiac disease requires repeat biopsy, exclusion of lymphoma, and multidisciplinary evaluation.",
        reasoning_framework="""
        1. Assess for persistent symptoms despite gluten-free diet.
        2. Repeat duodenal biopsy to confirm villous atrophy.
        3. Exclude lymphoma with imaging and immunophenotyping.
        4. Reference ACG guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Persistent symptoms", "Biopsy", "Lymphoma exclusion", "Multidisciplinary review"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Symptoms may be due to hidden gluten exposure",
        counter_arguments=["Non-specific histology", "Sampling error"],
        resolution_strategy="Dietitian referral, repeat testing, expert pathology review",
        entity_scope="Patients with refractory celiac disease",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Acute Pancreatitis: Etiology Determination",
        keywords=["acute pancreatitis", "etiology", "gallstones", "alcohol", "hypertriglyceridemia"],
        conclusion_template="Etiology is determined by history, labs, and imaging; gallstones and alcohol are most common causes.",
        reasoning_framework="""
        1. Obtain detailed history (alcohol, medications, trauma).
        2. Check labs: LFTs, triglycerides, calcium.
        3. Perform abdominal ultrasound for gallstones.
        4. Reference ACG guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["History", "Labs", "Imaging", "Common causes"],
        primary_authority=["ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Etiology may be unclear",
        counter_arguments=["Multiple causes", "Idiopathic cases"],
        resolution_strategy="Repeat testing, multidisciplinary review",
        entity_scope="Patients with acute pancreatitis",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ACG 2019 Guidelines"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Duodenal Biopsy Protocol",
        keywords=["upper endoscopy", "duodenal biopsy", "celiac disease", "protocol"],
        conclusion_template="Duodenal biopsy protocol for celiac disease includes at least four samples from the second part and bulb.",
        reasoning_framework="""
        1. Obtain at least four biopsies from second part and bulb.
        2. Reference ACG guidelines for optimal sampling.
        3. Document findings and rationale.
        """,
        key_factors=["Number of samples", "Location", "Guidelines"],
        primary_authority=["ACG"],
        burden_holder="Endoscopist",
        adversary_position="Sampling error",
        counter_arguments=["Non-specific histology", "Biopsy fragmentation"],
        resolution_strategy="Repeat biopsies, expert pathology review",
        entity_scope="Patients with suspected celiac disease",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Bowel Preparation Quality Assessment",
        keywords=["colonoscopy", "bowel preparation", "quality", "Boston scale"],
        conclusion_template="Bowel preparation quality is assessed using Boston Bowel Preparation Scale; inadequate prep requires repeat procedure.",
        reasoning_framework="""
        1. Score each colon segment using Boston scale.
        2. Document total score and adequacy.
        3. Reference ASGE guidelines.
        4. Repeat procedure if prep is inadequate.
        """,
        key_factors=["Boston scale", "Segmental scoring", "Adequacy", "Repeat indication"],
        primary_authority=["ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Prep may be adequate for some segments only",
        counter_arguments=["Patient compliance", "Segmental variability"],
        resolution_strategy="Repeat procedure, patient education",
        entity_scope="Patients undergoing colonoscopy",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASGE 2012 Position Statement"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: NAFLD/NASH Diagnosis",
        keywords=["chronic liver disease", "NAFLD", "NASH", "diagnosis", "biopsy"],
        conclusion_template="NAFLD/NASH is diagnosed by exclusion of other causes, imaging, and biopsy for definitive diagnosis.",
        reasoning_framework="""
        1. Exclude other causes of liver disease (alcohol, viral, drugs).
        2. Use imaging (ultrasound, MRI) for steatosis.
        3. Biopsy for definitive diagnosis and staging.
        4. Reference AASLD guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Exclusion", "Imaging", "Biopsy", "Staging"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Biopsy risks",
        counter_arguments=["Imaging may be inconclusive", "Overlap with other diseases"],
        resolution_strategy="Combine modalities, multidisciplinary review",
        entity_scope="Patients with suspected NAFLD/NASH",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Fecal Calprotectin Interpretation",
        keywords=["IBD", "fecal calprotectin", "interpretation", "monitoring"],
        conclusion_template="Fecal calprotectin is interpreted as a marker of intestinal inflammation; values >250 μg/g suggest active disease.",
        reasoning_framework="""
        1. Collect stool sample for calprotectin measurement.
        2. Interpret values: <50 μg/g normal, 50-250 μg/g borderline, >250 μg/g active inflammation.
        3. Reference ECCO guidelines.
        4. Document findings and adjust therapy as needed.
        """,
        key_factors=["Calprotectin value", "Interpretation", "Guidelines"],
        primary_authority=["ECCO"],
        burden_holder="Gastroenterologist",
        adversary_position="False positives due to infection or NSAIDs",
        counter_arguments=["Non-specific elevation", "Sampling variability"],
        resolution_strategy="Repeat testing, combine with other modalities",
        entity_scope="Patients with IBD",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Liver Transplant Eligibility",
        keywords=["hepatocellular carcinoma", "liver transplant", "eligibility", "Milan criteria"],
        conclusion_template="Eligibility for liver transplant in HCC is determined by Milan criteria: single lesion ≤5 cm or ≤3 lesions ≤3 cm each, no vascular invasion.",
        reasoning_framework="""
        1. Assess tumor size and number by imaging.
        2. Exclude vascular invasion and extrahepatic spread.
        3. Reference Milan criteria and AASLD guidelines.
        4. Document findings and transplant referral.
        """,
        key_factors=["Tumor size", "Number", "Vascular invasion", "Milan criteria"],
        primary_authority=["AASLD", "Milan criteria"],
        burden_holder="Hepatologist",
        adversary_position="Criteria may exclude some candidates",
        counter_arguments=["Patient preference", "Alternative therapies"],
        resolution_strategy="Multidisciplinary review, expanded criteria consideration",
        entity_scope="Patients with HCC",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Peptic Ulcer Bleeding Risk Stratification",
        keywords=["upper endoscopy", "peptic ulcer", "bleeding", "risk stratification", "Forrest classification"],
        conclusion_template="Bleeding risk is stratified by endoscopic findings using Forrest classification; guides management and follow-up.",
        reasoning_framework="""
        1. Classify ulcer by Forrest criteria (Ia-IV).
        2. High-risk stigmata (active bleeding, visible vessel) require endoscopic therapy.
        3. Reference ACG and ASGE guidelines.
        4. Document findings and management plan.
        """,
        key_factors=["Forrest classification", "Stigmata", "Therapy indication"],
        primary_authority=["ACG", "ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Classification may be subjective",
        counter_arguments=["Inter-observer variability", "Missed stigmata"],
        resolution_strategy="Standardized training, repeat endoscopy",
        entity_scope="Patients with peptic ulcer",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Post-CRC Resection Surveillance",
        keywords=["colonoscopy", "CRC", "resection", "surveillance", "interval"],
        conclusion_template="Post-CRC resection surveillance colonoscopy is recommended at 1 year, then every 3-5 years per guidelines.",
        reasoning_framework="""
        1. Schedule colonoscopy at 1 year post-resection.
        2. Adjust interval based on findings and risk.
        3. Reference USMSTF and NCCN guidelines.
        4. Document findings and surveillance plan.
        """,
        key_factors=["Resection status", "Surveillance interval", "Guidelines"],
        primary_authority=["USMSTF", "NCCN"],
        burden_holder="Gastroenterologist",
        adversary_position="Interval may be too long for high-risk patients",
        counter_arguments=["Patient compliance", "Cost"],
        resolution_strategy="Individualized risk assessment, guideline adherence",
        entity_scope="Patients post-CRC resection",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="USMSTF 2020 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Alcoholic Liver Disease Diagnosis",
        keywords=["chronic liver disease", "alcoholic liver disease", "diagnosis", "history", "biopsy"],
        conclusion_template="Alcoholic liver disease is diagnosed by history of excessive alcohol intake, clinical, laboratory, and imaging findings.",
        reasoning_framework="""
        1. Obtain detailed history of alcohol intake.
        2. Assess labs: AST>ALT, elevated GGT, bilirubin.
        3. Imaging for steatosis, cirrhosis.
        4. Biopsy if diagnosis unclear.
        5. Reference AASLD guidelines.
        6. Document findings and management plan.
        """,
        key_factors=["History", "Labs", "Imaging", "Biopsy"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="History may be unreliable",
        counter_arguments=["Overlap with NAFLD", "Biopsy risks"],
        resolution_strategy="Combine modalities, multidisciplinary review",
        entity_scope="Patients with suspected alcoholic liver disease",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Extraintestinal Manifestations Management",
        keywords=["IBD", "extraintestinal manifestations", "management", "arthritis", "skin"],
        conclusion_template="Management of extraintestinal manifestations requires multidisciplinary approach and targeted therapy.",
        reasoning_framework="""
        1. Identify extraintestinal manifestations (arthritis, skin, eye, liver).
        2. Refer to appropriate specialists.
        3. Adjust IBD therapy as needed.
        4. Reference ECCO and ACG guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Manifestation type", "Specialist referral", "Therapy adjustment"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Manifestations may persist despite IBD control",
        counter_arguments=["Therapy side effects", "Patient preference"],
        resolution_strategy="Multidisciplinary review, individualized therapy",
        entity_scope="Patients with IBD",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Imaging Modalities Selection",
        keywords=["hepatocellular carcinoma", "imaging", "modality", "CT", "MRI", "ultrasound"],
        conclusion_template="Multiphasic CT or MRI is preferred for HCC diagnosis and staging; ultrasound is used for screening.",
        reasoning_framework="""
        1. Use multiphasic CT or MRI for diagnosis and staging.
        2. Ultrasound for screening in cirrhosis.
        3. Reference AASLD and LI-RADS guidelines.
        4. Document findings and rationale.
        """,
        key_factors=["Imaging modality", "Diagnosis", "Staging", "Screening"],
        primary_authority=["AASLD", "LI-RADS"],
        burden_holder="Radiologist/Hepatologist",
        adversary_position="Imaging may be inconclusive",
        counter_arguments=["Lesion heterogeneity", "Patient contraindications"],
        resolution_strategy="Repeat imaging, alternative modalities",
        entity_scope="Patients with liver lesions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Gastric Atrophy and Intestinal Metaplasia Surveillance",
        keywords=["upper endoscopy", "gastric atrophy", "intestinal metaplasia", "surveillance"],
        conclusion_template="Patients with gastric atrophy or intestinal metaplasia require endoscopic surveillance per guidelines.",
        reasoning_framework="""
        1. Identify atrophy or metaplasia by histology.
        2. Schedule surveillance endoscopy per ESGE/ACG guidelines.
        3. Document findings and management plan.
        """,
        key_factors=["Histology", "Surveillance interval", "Guidelines"],
        primary_authority=["ESGE", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Surveillance may be excessive",
        counter_arguments=["Patient compliance", "Cost"],
        resolution_strategy="Individualized risk assessment, guideline adherence",
        entity_scope="Patients with gastric atrophy/metaplasia",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ESGE 2019 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Flat Lesion Detection and Management",
        keywords=["colonoscopy", "flat lesion", "detection", "management", "chromoendoscopy"],
        conclusion_template="Flat lesions are detected by enhanced imaging (chromoendoscopy, NBI) and require careful resection.",
        reasoning_framework="""
        1. Use chromoendoscopy or narrow-band imaging for detection.
        2. Carefully resect flat lesions to avoid incomplete removal.
        3. Reference ASGE guidelines.
        4. Document findings and management plan.
        """,
        key_factors=["Imaging technique", "Resection", "Guidelines"],
        primary_authority=["ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Flat lesions may be missed",
        counter_arguments=["Imaging limitations", "Incomplete resection"],
        resolution_strategy="Repeat imaging, expert review",
        entity_scope="Patients undergoing colonoscopy",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASGE 2017 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Autoimmune Hepatitis Diagnosis",
        keywords=["chronic liver disease", "autoimmune hepatitis", "diagnosis", "serology", "biopsy"],
        conclusion_template="Autoimmune hepatitis is diagnosed by serology (ANA, SMA, LKM) and confirmatory biopsy.",
        reasoning_framework="""
        1. Screen for ANA, SMA, LKM antibodies.
        2. Assess liver function tests.
        3. Biopsy for definitive diagnosis and staging.
        4. Reference AASLD guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Serology", "Biopsy", "Liver function", "Staging"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Serology may be negative",
        counter_arguments=["Biopsy risks", "Overlap with other diseases"],
        resolution_strategy="Repeat testing, multidisciplinary review",
        entity_scope="Patients with suspected autoimmune hepatitis",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2019 Guidance"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Small Bowel Imaging",
        keywords=["IBD", "small bowel", "imaging", "MR enterography", "capsule endoscopy"],
        conclusion_template="Small bowel imaging in IBD is performed by MR enterography or capsule endoscopy for disease extent and activity.",
        reasoning_framework="""
        1. Use MR enterography for non-invasive assessment.
        2. Capsule endoscopy for mucosal evaluation.
        3. Reference ECCO and ACG guidelines.
        4. Document findings and management plan.
        """,
        key_factors=["Imaging modality", "Disease extent", "Activity", "Guidelines"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Imaging may miss deep lesions",
        counter_arguments=["Capsule retention", "Cost"],
        resolution_strategy="Combine modalities, individualized assessment",
        entity_scope="Patients with IBD",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Staging Systems",
        keywords=["hepatocellular carcinoma", "staging", "BCLC", "AJCC", "prognosis"],
        conclusion_template="HCC is staged by BCLC and AJCC systems; staging guides prognosis and therapy.",
        reasoning_framework="""
        1. Use BCLC staging for clinical management.
        2. AJCC staging for tumor characteristics.
        3. Reference AASLD guidelines.
        4. Document findings and management plan.
        """,
        key_factors=["Staging system", "Tumor characteristics", "Prognosis", "Therapy"],
        primary_authority=["AASLD", "BCLC", "AJCC"],
        burden_holder="Hepatologist",
        adversary_position="Staging may be ambiguous",
        counter_arguments=["Overlap between stages", "Imaging limitations"],
        resolution_strategy="Multidisciplinary review, repeat imaging",
        entity_scope="Patients with HCC",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Eosinophilic Esophagitis Diagnosis",
        keywords=["upper endoscopy", "eosinophilic esophagitis", "diagnosis", "biopsy"],
        conclusion_template="Eosinophilic esophagitis is diagnosed by endoscopic findings and ≥15 eosinophils per high-power field on biopsy.",
        reasoning_framework="""
        1. Identify rings, furrows, exudates, or strictures during endoscopy.
        2. Obtain biopsies from multiple esophageal sites.
        3. Confirm ≥15 eosinophils per high-power field.
        4. Reference AGA guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Endoscopic findings", "Biopsy", "Eosinophil count", "Guidelines"],
        primary_authority=["AGA"],
        burden_holder="Endoscopist",
        adversary_position="Eosinophilia may be due to GERD",
        counter_arguments=["Overlap with other diseases", "Sampling error"],
        resolution_strategy="Repeat biopsies, expert pathology review",
        entity_scope="Patients with suspected EoE",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGA 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Colonoscopy: Post-Polypectomy Bleeding Management",
        keywords=["colonoscopy", "polypectomy", "bleeding", "management", "endoscopic therapy"],
        conclusion_template="Post-polypectomy bleeding is managed by endoscopic therapy (clip, injection, cautery) and supportive care.",
        reasoning_framework="""
        1. Identify bleeding site during colonoscopy.
        2. Apply endoscopic therapy (clip, injection, cautery).
        3. Monitor for delayed bleeding.
        4. Reference ASGE guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Bleeding site", "Therapy", "Delayed bleeding", "Guidelines"],
        primary_authority=["ASGE"],
        burden_holder="Endoscopist",
        adversary_position="Bleeding may recur",
        counter_arguments=["Therapy failure", "Patient comorbidities"],
        resolution_strategy="Repeat therapy, multidisciplinary review",
        entity_scope="Patients post-polypectomy",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="ASGE 2017 Guidelines"
    ),
    DoctrineBlock(
        topic="Chronic Liver Disease: Wilson Disease Diagnosis",
        keywords=["chronic liver disease", "Wilson disease", "diagnosis", "ceruloplasmin", "biopsy"],
        conclusion_template="Wilson disease is diagnosed by low ceruloplasmin, elevated urinary copper, and confirmatory biopsy.",
        reasoning_framework="""
        1. Screen for low ceruloplasmin and elevated urinary copper.
        2. Assess for Kayser-Fleischer rings.
        3. Biopsy for hepatic copper quantification.
        4. Reference AASLD guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Ceruloplasmin", "Urinary copper", "Biopsy", "Kayser-Fleischer rings"],
        primary_authority=["AASLD"],
        burden_holder="Hepatologist",
        adversary_position="Ceruloplasmin may be normal",
        counter_arguments=["Overlap with other diseases", "Biopsy risks"],
        resolution_strategy="Repeat testing, multidisciplinary review",
        entity_scope="Patients with suspected Wilson disease",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2019 Guidance"
    ),
    DoctrineBlock(
        topic="Inflammatory Bowel Disease: Perianal Disease Management",
        keywords=["IBD", "perianal disease", "management", "fistula", "abscess"],
        conclusion_template="Perianal disease in IBD is managed by MRI, surgical consultation, and targeted medical therapy.",
        reasoning_framework="""
        1. Use MRI for fistula and abscess assessment.
        2. Refer to colorectal surgeon for complex disease.
        3. Initiate medical therapy (biologics).
        4. Reference ECCO and ACG guidelines.
        5. Document findings and management plan.
        """,
        key_factors=["Imaging", "Surgical referral", "Medical therapy", "Guidelines"],
        primary_authority=["ECCO", "ACG"],
        burden_holder="Gastroenterologist",
        adversary_position="Medical therapy may fail",
        counter_arguments=["Surgical risks", "Patient preference"],
        resolution_strategy="Multidisciplinary review, individualized therapy",
        entity_scope="Patients with IBD",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ECCO 2018 Guidelines"
    ),
    DoctrineBlock(
        topic="Hepatocellular Carcinoma: Systemic Therapy Selection",
        keywords=["hepatocellular carcinoma", "systemic therapy", "selection", "sorafenib", "immunotherapy"],
        conclusion_template="Systemic therapy for HCC is selected based on stage, liver function, and patient preference; sorafenib and immunotherapy are options.",
        reasoning_framework="""
        1. Assess HCC stage and liver function (Child-Pugh).
        2. Consider sorafenib, lenvatinib, or immunotherapy per guidelines.
        3. Reference AASLD and NCCN guidelines.
        4. Document findings and therapy plan.
        """,
        key_factors=["Stage", "Liver function", "Therapy options", "Patient preference"],
        primary_authority=["AASLD", "NCCN"],
        burden_holder="Hepatologist",
        adversary_position="Therapy may be limited by liver function",
        counter_arguments=["Adverse effects", "Cost"],
        resolution_strategy="Individualized therapy, multidisciplinary review",
        entity_scope="Patients with HCC",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="AASLD 2018 Guidance"
    ),
    DoctrineBlock(
        topic="Upper Endoscopy: Gastric Polyps Management",
        keywords=["upper endoscopy", "gastric polyps", "management", "biopsy", "surveillance"],
        conclusion_template="Gastric polyps are managed by biopsy, removal if adenomatous, and surveillance per guidelines.",
        reasoning_framework="""
        1. Identify polyps during endoscopy.
        2. Biopsy for histology.
        3. Remove adenomatous or suspicious polyps.
        4. Reference ACG and ESGE guidelines for surveillance.
        5. Document findings and management plan.
        """,
        key_factors=["Polyp type", "Biopsy", "Removal", "Surveillance"],
        primary_authority=["ACG", "ESGE"],
        burden_holder="Endoscopist",
        adversary_position="Polyps may be missed",
        counter_arguments=["Histology ambiguity", "Incomplete removal"],
        resolution_strategy="Repeat endoscopy, expert pathology review",
        entity_scope="Patients with gastric polyps",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ACG 2022 Guidelines"
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