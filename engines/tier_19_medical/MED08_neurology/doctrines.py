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
        topic="Acute Ischemic Stroke tPA Eligibility",
        keywords=[
            "ischemic stroke", "tPA", "alteplase", "thrombolysis", "NIHSS", "onset time", "contraindications", "CT head"
        ],
        conclusion_template="Patient is {eligibility_status} for IV tPA administration based on current guidelines.",
        reasoning_framework="""
        1. Confirm diagnosis of acute ischemic stroke with sudden onset of focal neurological deficit.
        2. Establish precise time of symptom onset or last known well.
        3. Exclude intracranial hemorrhage or major early infarct signs via non-contrast CT.
        4. Assess for absolute contraindications: recent surgery, active bleeding, severe hypertension, low platelets, INR >1.7, recent anticoagulant use, recent stroke/head trauma.
        5. Evaluate relative contraindications: minor or rapidly improving symptoms, seizure at onset, pregnancy, recent MI.
        6. Confirm age ≥18 years.
        7. Confirm NIHSS score and clinical severity.
        8. If within 4.5 hours from onset and no contraindications, patient is eligible for tPA.
        9. If between 3-4.5 hours, apply additional exclusion criteria (age >80, severe stroke, diabetes with prior stroke, oral anticoagulant use).
        10. Document informed consent and proceed with weight-based dosing if eligible.
        """,
        key_factors=[
            "Time from symptom onset", "Imaging exclusion of hemorrhage", "Absolute and relative contraindications", "Age", "NIHSS score"
        ],
        primary_authority=[
            "AHA/ASA 2018 Guidelines", "NINDS tPA Study", "ECASS III Trial"
        ],
        burden_holder="Treating Neurologist",
        adversary_position="Patient is not eligible for tPA due to contraindications or time window exceeded.",
        counter_arguments=[
            "Minor or rapidly improving symptoms may still benefit in select cases.",
            "Uncertainty in time of onset may allow for treatment if last known well is within window.",
            "Relative contraindications are not absolute."
        ],
        resolution_strategy="Multidisciplinary consensus, strict adherence to published guidelines, and risk-benefit documentation.",
        entity_scope="Acute stroke centers, emergency departments",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AHA/ASA 2018 Acute Ischemic Stroke Guidelines"
    ),
    DoctrineBlock(
        topic="Mechanical Thrombectomy for Large Vessel Occlusion",
        keywords=[
            "mechanical thrombectomy", "LVO", "endovascular therapy", "stroke", "CT angiography", "ASPECTS", "DAWN", "DEFUSE 3"
        ],
        conclusion_template="Patient is {eligibility_status} for mechanical thrombectomy based on vessel imaging and clinical criteria.",
        reasoning_framework="""
        1. Confirm diagnosis of acute ischemic stroke with disabling neurological deficit.
        2. Obtain vascular imaging (CTA/MRA) to identify large vessel occlusion (ICA, M1, proximal M2, basilar).
        3. Assess time from last known well—standard window is 0-6 hours, extended window up to 24 hours in select cases.
        4. Evaluate ASPECTS score (≥6 preferred) to estimate infarct core.
        5. Apply DAWN/DEFUSE 3 criteria for 6-24 hour window: small infarct core, severe clinical deficit, mismatch between clinical deficit and infarct size.
        6. Exclude significant pre-stroke disability (mRS >1).
        7. Exclude contraindications such as extensive infarct, uncorrectable coagulopathy.
        8. If eligible, proceed to endovascular therapy as soon as possible.
        """,
        key_factors=[
            "Vessel imaging", "Time from onset", "ASPECTS score", "Clinical severity", "Pre-stroke disability"
        ],
        primary_authority=[
            "AHA/ASA 2019 Guidelines", "DAWN Trial", "DEFUSE 3 Trial"
        ],
        burden_holder="Stroke Neurologist/Interventionalist",
        adversary_position="Patient is not eligible due to infarct size, time window, or comorbidities.",
        counter_arguments=[
            "Some patients outside standard criteria may benefit.",
            "Advanced imaging may identify salvageable tissue beyond 6 hours.",
            "Pre-stroke disability may not preclude benefit in select cases."
        ],
        resolution_strategy="Strict adherence to guideline-based criteria, multidisciplinary review, documentation of rationale.",
        entity_scope="Comprehensive stroke centers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AHA/ASA 2019 Endovascular Guidelines"
    ),
    DoctrineBlock(
        topic="ILAE 2017 Seizure Classification",
        keywords=[
            "seizure", "epilepsy", "ILAE", "focal onset", "generalized onset", "unknown onset", "awareness", "motor", "non-motor"
        ],
        conclusion_template="Seizure classified as {seizure_type} according to ILAE 2017 criteria.",
        reasoning_framework="""
        1. Determine onset: focal, generalized, or unknown.
        2. For focal seizures, assess awareness (aware vs. impaired).
        3. Classify by prominent features: motor (tonic-clonic, automatisms, atonic, etc.) or non-motor (sensory, cognitive, emotional).
        4. For generalized seizures, determine motor (tonic-clonic, myoclonic, atonic) or non-motor (absence).
        5. Use clinical history, EEG, and imaging to support classification.
        6. Recognize that some seizures may remain unclassified due to incomplete data.
        """,
        key_factors=[
            "Seizure onset", "Awareness", "Motor vs. non-motor features", "EEG findings"
        ],
        primary_authority=[
            "ILAE 2017 Classification", "Epilepsy Foundation"
        ],
        burden_holder="Epileptologist/Neurologist",
        adversary_position="Seizure cannot be classified due to insufficient data or atypical presentation.",
        counter_arguments=[
            "Classification may evolve with new data.",
            "Overlap between types can occur.",
            "EEG may be non-diagnostic."
        ],
        resolution_strategy="Iterative reassessment, use of ancillary testing, and expert consensus.",
        entity_scope="Epilepsy clinics, neurology practices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ILAE 2017 Seizure Classification"
    ),
    DoctrineBlock(
        topic="First-Line AED Selection Algorithm",
        keywords=[
            "antiepileptic drugs", "AED", "first-line", "seizure type", "side effects", "comorbidities", "drug interactions"
        ],
        conclusion_template="Recommended first-line AED is {drug_choice} based on seizure type and patient profile.",
        reasoning_framework="""
        1. Identify seizure type (focal, generalized, absence, myoclonic).
        2. Review patient age, sex, comorbidities (psychiatric, hepatic, renal, pregnancy).
        3. Consider drug efficacy for seizure type.
        4. Evaluate side effect profiles and tolerability.
        5. Assess for potential drug-drug interactions.
        6. For focal seizures: carbamazepine, lamotrigine, levetiracetam, oxcarbazepine.
        7. For generalized tonic-clonic: valproate, lamotrigine, levetiracetam.
        8. For absence: ethosuximide, valproate.
        9. For myoclonic: valproate, levetiracetam.
        10. Adjust for special populations (pregnancy: avoid valproate; elderly: avoid sedating drugs).
        """,
        key_factors=[
            "Seizure type", "Comorbidities", "Drug interactions", "Side effect profile", "Patient age/sex"
        ],
        primary_authority=[
            "AAN Epilepsy Guidelines", "ILAE Treatment Guidelines"
        ],
        burden_holder="Prescribing Neurologist",
        adversary_position="Alternative AEDs may be equally effective or better tolerated.",
        counter_arguments=[
            "Patient preference may influence choice.",
            "Cost and access may limit options.",
            "Polytherapy may be required in refractory cases."
        ],
        resolution_strategy="Shared decision-making, guideline adherence, and periodic reassessment.",
        entity_scope="Epilepsy clinics, primary care",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN/ILAE AED Guidelines"
    ),
    DoctrineBlock(
        topic="Parkinson Disease Diagnosis and Staging",
        keywords=[
            "parkinsonism", "bradykinesia", "rigidity", "tremor", "UPDRS", "Hoehn and Yahr", "dopaminergic response"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for Parkinson disease, staged as {stage} per Hoehn and Yahr.",
        reasoning_framework="""
        1. Identify cardinal motor features: bradykinesia plus at least one of rigidity, rest tremor, or postural instability.
        2. Exclude secondary causes (drug-induced, vascular, atypical parkinsonism).
        3. Assess response to dopaminergic therapy.
        4. Use UPDRS for symptom quantification.
        5. Stage disease using Hoehn and Yahr scale (1-5).
        6. Evaluate for non-motor symptoms (autonomic, cognitive, mood).
        7. Consider neuroimaging (DaTscan) if diagnosis is uncertain.
        """,
        key_factors=[
            "Motor features", "Response to dopaminergic therapy", "Exclusion of secondary causes", "Disease staging"
        ],
        primary_authority=[
            "MDS Clinical Diagnostic Criteria", "Hoehn and Yahr Staging"
        ],
        burden_holder="Movement Disorders Specialist",
        adversary_position="Symptoms may be due to atypical parkinsonism or secondary causes.",
        counter_arguments=[
            "Overlap with other parkinsonian syndromes.",
            "Early disease may lack classic features.",
            "Imaging may be inconclusive."
        ],
        resolution_strategy="Longitudinal follow-up, response to therapy, and multidisciplinary input.",
        entity_scope="Movement disorders clinics",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="MDS 2015 Diagnostic Criteria"
    ),
    DoctrineBlock(
        topic="Alzheimer Disease Diagnosis and Cognitive Assessment",
        keywords=[
            "Alzheimer", "dementia", "cognitive decline", "MMSE", "MoCA", "CSF biomarkers", "amyloid PET", "neuropsychology"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for Alzheimer disease based on clinical and biomarker criteria.",
        reasoning_framework="""
        1. Document progressive cognitive decline interfering with daily function.
        2. Exclude delirium, depression, and other reversible causes.
        3. Perform cognitive testing (MMSE, MoCA).
        4. Assess for functional impairment in activities of daily living.
        5. Obtain neuroimaging (MRI) to exclude structural lesions.
        6. Consider CSF biomarkers (Aβ42, tau) and amyloid PET for confirmation.
        7. Neuropsychological testing for detailed domain assessment.
        8. Apply NIA-AA or DSM-5 criteria for probable Alzheimer disease.
        """,
        key_factors=[
            "Cognitive decline", "Functional impairment", "Neuroimaging", "Biomarkers", "Neuropsychological profile"
        ],
        primary_authority=[
            "NIA-AA 2018 Criteria", "DSM-5", "AAN Dementia Guidelines"
        ],
        burden_holder="Cognitive Neurologist",
        adversary_position="Cognitive impairment may be due to other causes (vascular, Lewy body, depression).",
        counter_arguments=[
            "Mixed pathologies are common.",
            "Biomarkers may be unavailable or inconclusive.",
            "Early disease may not meet full criteria."
        ],
        resolution_strategy="Serial assessment, multidisciplinary input, and use of ancillary testing.",
        entity_scope="Memory clinics, geriatrics",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="NIA-AA 2018 Alzheimer Criteria"
    ),
    DoctrineBlock(
        topic="Multiple Sclerosis McDonald Criteria and DMT Selection",
        keywords=[
            "multiple sclerosis", "McDonald criteria", "dissemination in space", "dissemination in time", "DMT", "MRI", "oligoclonal bands"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for MS per McDonald criteria; recommended DMT is {dmt_choice}.",
        reasoning_framework="""
        1. Identify clinical attacks and objective lesions.
        2. Demonstrate dissemination in space (≥2 CNS regions on MRI or clinical exam).
        3. Demonstrate dissemination in time (simultaneous enhancing/non-enhancing lesions or new lesions over time).
        4. CSF oligoclonal bands can substitute for dissemination in time.
        5. Exclude alternative diagnoses (infections, vascular, metabolic, other demyelinating diseases).
        6. Once diagnosis is established, stratify disease activity and prognostic factors.
        7. Select DMT based on disease activity, safety profile, comorbidities, and patient preference.
        8. Monitor for adverse effects and efficacy.
        """,
        key_factors=[
            "Clinical attacks", "MRI lesions", "CSF oligoclonal bands", "Exclusion of mimics", "Disease activity"
        ],
        primary_authority=[
            "2017 McDonald Criteria", "AAN MS Guidelines"
        ],
        burden_holder="MS Specialist",
        adversary_position="Criteria not met or alternative diagnosis more likely.",
        counter_arguments=[
            "Radiologically isolated syndrome may not require treatment.",
            "DMT selection may be limited by insurance or comorbidities.",
            "Atypical presentations may complicate diagnosis."
        ],
        resolution_strategy="Serial imaging, multidisciplinary review, and shared decision-making.",
        entity_scope="MS centers, neurology clinics",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="2017 McDonald Criteria"
    ),
    DoctrineBlock(
        topic="Glasgow Coma Scale and TBI Severity Classification",
        keywords=[
            "GCS", "traumatic brain injury", "consciousness", "eye opening", "verbal response", "motor response", "severity"
        ],
        conclusion_template="GCS score is {gcs_score}, classified as {severity} TBI.",
        reasoning_framework="""
        1. Assess eye opening (1-4), verbal response (1-5), and motor response (1-6).
        2. Sum components for total GCS score (3-15).
        3. Classify TBI severity: severe (3-8), moderate (9-12), mild (13-15).
        4. Reassess periodically for changes.
        5. Consider confounders (intubation, intoxication, sedation).
        6. Use GCS in conjunction with imaging and clinical context.
        """,
        key_factors=[
            "GCS score", "Component scores", "Confounders", "Imaging findings"
        ],
        primary_authority=[
            "Teasdale and Jennett 1974", "Brain Trauma Foundation Guidelines"
        ],
        burden_holder="Emergency Physician/Neurosurgeon",
        adversary_position="GCS may not reflect true neurological status due to confounders.",
        counter_arguments=[
            "Sedation or intubation may lower score.",
            "Serial exams may provide more accurate assessment.",
            "Pediatric GCS differs from adult."
        ],
        resolution_strategy="Document confounders, repeat assessments, use adjunctive tools.",
        entity_scope="Emergency departments, trauma centers",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Brain Trauma Foundation TBI Guidelines"
    ),
    DoctrineBlock(
        topic="CT and MRI Stroke Protocol Interpretation",
        keywords=[
            "CT head", "MRI brain", "stroke protocol", "ischemia", "hemorrhage", "ASPECTS", "DWI", "FLAIR"
        ],
        conclusion_template="Imaging findings are {imaging_interpretation} consistent with {stroke_type}.",
        reasoning_framework="""
        1. For CT: assess for hemorrhage, early ischemic changes, mass effect, and ASPECTS score.
        2. For MRI: evaluate DWI for acute infarct, FLAIR for timing, GRE/SWI for hemorrhage.
        3. Identify vessel occlusion on CTA/MRA.
        4. Compare imaging findings with clinical presentation and time course.
        5. Exclude stroke mimics (tumor, seizure, infection).
        6. Document findings relevant to acute management (tPA/thrombectomy eligibility).
        """,
        key_factors=[
            "Imaging modality", "Timing of imaging", "Hemorrhage vs. ischemia", "ASPECTS score", "Vessel status"
        ],
        primary_authority=[
            "AHA/ASA Imaging Guidelines", "ASPECTS Criteria"
        ],
        burden_holder="Neuroradiologist/Stroke Neurologist",
        adversary_position="Imaging is inconclusive or inconsistent with clinical findings.",
        counter_arguments=[
            "Early ischemic changes may be subtle.",
            "Artifact may obscure findings.",
            "Clinical correlation is essential."
        ],
        resolution_strategy="Repeat imaging, multidisciplinary review, and clinical correlation.",
        entity_scope="Stroke centers, radiology departments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AHA/ASA Imaging Recommendations"
    ),
    DoctrineBlock(
        topic="Lumbar Puncture and CSF Interpretation",
        keywords=[
            "lumbar puncture", "CSF analysis", "opening pressure", "meningitis", "encephalitis", "subarachnoid hemorrhage", "oligoclonal bands"
        ],
        conclusion_template="CSF findings are {csf_interpretation}, supporting diagnosis of {diagnosis}.",
        reasoning_framework="""
        1. Measure opening pressure and collect CSF in sequential tubes.
        2. Analyze cell count, protein, glucose, and differential.
        3. Assess for xanthochromia (subarachnoid hemorrhage).
        4. Send for Gram stain, culture, PCR as indicated.
        5. Evaluate for oligoclonal bands and IgG index (MS).
        6. Interpret findings in clinical context (infectious, inflammatory, hemorrhagic, neoplastic).
        7. Consider traumatic tap and correct for RBCs if needed.
        """,
        key_factors=[
            "Opening pressure", "Cell count and differential", "Protein/glucose", "Oligoclonal bands", "Xanthochromia"
        ],
        primary_authority=[
            "IDSA Meningitis Guidelines", "AAN CSF Interpretation Guidelines"
        ],
        burden_holder="Consulting Neurologist",
        adversary_position="CSF findings are non-specific or confounded by traumatic tap.",
        counter_arguments=[
            "Traumatic tap may mimic hemorrhage.",
            "Partial treatment may alter findings.",
            "Overlap between infectious and inflammatory patterns."
        ],
        resolution_strategy="Repeat LP if needed, use adjunctive testing, and clinical correlation.",
        entity_scope="Hospitals, neurology clinics",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IDSA/AAN CSF Guidelines"
    ),
    DoctrineBlock(
        topic="Migraine Diagnosis and Prophylactic Treatment",
        keywords=[
            "migraine", "headache", "ICHD-3", "aura", "prophylaxis", "triptans", "beta-blockers", "topiramate"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for migraine; recommended prophylactic treatment is {prophylactic_choice}.",
        reasoning_framework="""
        1. Apply ICHD-3 criteria: recurrent headache attacks lasting 4-72 hours, with ≥2 of unilateral, pulsating, moderate/severe, aggravated by activity.
        2. Assess for associated symptoms: nausea, photophobia, phonophobia, aura.
        3. Exclude secondary causes (imaging if red flags).
        4. Indicate prophylaxis if ≥4 attacks/month, disabling symptoms, or contraindications to abortive therapy.
        5. First-line prophylactics: beta-blockers, topiramate, valproate, amitriptyline.
        6. Consider comorbidities and side effect profiles.
        7. Monitor efficacy and adjust as needed.
        """,
        key_factors=[
            "Headache frequency", "Associated symptoms", "Exclusion of secondary causes", "Prophylactic indication", "Comorbidities"
        ],
        primary_authority=[
            "ICHD-3", "AAN Migraine Guidelines"
        ],
        burden_holder="Headache Specialist/Neurologist",
        adversary_position="Headache does not meet criteria or is secondary.",
        counter_arguments=[
            "Overlap with tension-type or cluster headache.",
            "Medication overuse may complicate diagnosis.",
            "Patient preference may affect prophylactic choice."
        ],
        resolution_strategy="Serial assessment, headache diary, and individualized treatment plan.",
        entity_scope="Headache clinics, primary care",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="ICHD-3/AAN Migraine Guidelines"
    ),
    # 30+ additional DoctrineBlocks with real content for comprehensive coverage:
    DoctrineBlock(
        topic="Status Epilepticus Initial Management",
        keywords=[
            "status epilepticus", "benzodiazepines", "lorazepam", "midazolam", "seizure", "emergency"
        ],
        conclusion_template="Initial management of status epilepticus initiated with {first_line_agent}.",
        reasoning_framework="""
        1. Recognize continuous or recurrent seizures lasting >5 minutes.
        2. Ensure airway, breathing, and circulation.
        3. Obtain IV access, check glucose, and correct metabolic derangements.
        4. Administer first-line benzodiazepine (IV lorazepam, IM midazolam, or rectal diazepam).
        5. Monitor for respiratory depression.
        6. Prepare for second-line therapy if seizures persist.
        """,
        key_factors=[
            "Duration of seizure", "Airway protection", "First-line agent", "Response to therapy"
        ],
        primary_authority=[
            "Neurocritical Care Society Guidelines", "AAN Status Epilepticus Guidelines"
        ],
        burden_holder="Emergency Physician/Neurologist",
        adversary_position="Delayed or inappropriate therapy increases morbidity.",
        counter_arguments=[
            "Non-convulsive status may be missed.",
            "IV access may be difficult.",
            "Benzodiazepine resistance may occur."
        ],
        resolution_strategy="Rapid protocolized response, escalation to second-line agents, and EEG monitoring.",
        entity_scope="Emergency departments, ICUs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NCS/AAN Status Epilepticus Guidelines"
    ),
    DoctrineBlock(
        topic="TIA Risk Stratification and Management",
        keywords=[
            "TIA", "transient ischemic attack", "ABCD2", "stroke risk", "antiplatelet", "carotid imaging"
        ],
        conclusion_template="Patient stratified as {risk_level} risk for stroke post-TIA; recommended management is {management_plan}.",
        reasoning_framework="""
        1. Confirm transient focal neurological deficit resolving within 24 hours.
        2. Use ABCD2 score (Age, BP, Clinical features, Duration, Diabetes) to estimate risk.
        3. Perform urgent brain imaging (MRI preferred) and vascular imaging (carotid, intracranial).
        4. Initiate antiplatelet therapy unless contraindicated.
        5. Address modifiable risk factors (hypertension, diabetes, atrial fibrillation).
        6. Refer for carotid endarterectomy if significant stenosis.
        7. Educate patient on warning signs and follow-up.
        """,
        key_factors=[
            "ABCD2 score", "Imaging findings", "Vascular risk factors", "Antiplatelet therapy"
        ],
        primary_authority=[
            "AHA/ASA TIA Guidelines", "NICE Stroke Guidelines"
        ],
        burden_holder="Stroke Neurologist/Primary Care",
        adversary_position="TIA diagnosis is uncertain or risk is underestimated.",
        counter_arguments=[
            "TIA mimics may confound diagnosis.",
            "Imaging may reveal infarct, changing management.",
            "Bleeding risk may preclude antiplatelet use."
        ],
        resolution_strategy="Comprehensive workup, multidisciplinary input, and individualized risk assessment.",
        entity_scope="Stroke clinics, primary care",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AHA/ASA TIA Guidelines"
    ),
    DoctrineBlock(
        topic="Carotid Stenosis Intervention Criteria",
        keywords=[
            "carotid stenosis", "endarterectomy", "stenting", "NASCET", "symptomatic", "asymptomatic"
        ],
        conclusion_template="Patient is {intervention_eligibility} for carotid intervention based on degree of stenosis and symptoms.",
        reasoning_framework="""
        1. Quantify degree of stenosis using NASCET criteria.
        2. For symptomatic patients (recent TIA/stroke), recommend endarterectomy if stenosis is 70-99%, consider for 50-69%.
        3. For asymptomatic patients, consider intervention if stenosis >80% and life expectancy >5 years.
        4. Assess surgical risk and comorbidities.
        5. Consider carotid stenting for high surgical risk.
        6. Optimize medical therapy for all patients.
        """,
        key_factors=[
            "Degree of stenosis", "Symptom status", "Surgical risk", "Life expectancy"
        ],
        primary_authority=[
            "NASCET", "CREST Trial", "AHA/ASA Guidelines"
        ],
        burden_holder="Vascular Neurologist/Surgeon",
        adversary_position="Medical management alone may suffice, especially in asymptomatic cases.",
        counter_arguments=[
            "Perioperative risk may outweigh benefit.",
            "Advances in medical therapy reduce intervention need.",
            "Patient preference and comorbidities are critical."
        ],
        resolution_strategy="Shared decision-making, guideline-based selection, and risk stratification.",
        entity_scope="Stroke centers, vascular surgery",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NASCET/CREST/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="Anticoagulation in Atrial Fibrillation for Stroke Prevention",
        keywords=[
            "atrial fibrillation", "anticoagulation", "CHA2DS2-VASc", "stroke prevention", "DOAC", "warfarin"
        ],
        conclusion_template="Anticoagulation is {anticoagulation_recommendation} for stroke prevention in atrial fibrillation.",
        reasoning_framework="""
        1. Calculate CHA2DS2-VASc score to estimate stroke risk.
        2. Recommend anticoagulation for score ≥2 in men or ≥3 in women.
        3. Assess bleeding risk using HAS-BLED score.
        4. Choose DOAC over warfarin unless contraindicated (mechanical valve, severe mitral stenosis).
        5. Monitor renal function and drug interactions.
        6. Educate patient on adherence and bleeding precautions.
        """,
        key_factors=[
            "CHA2DS2-VASc score", "Bleeding risk", "Contraindications", "Drug selection"
        ],
        primary_authority=[
            "AHA/ACC/HRS AFib Guidelines", "ESC Guidelines"
        ],
        burden_holder="Cardiologist/Primary Care",
        adversary_position="Bleeding risk or contraindications may preclude anticoagulation.",
        counter_arguments=[
            "Left atrial appendage occlusion may be an alternative.",
            "Patient refusal or non-adherence.",
            "Renal or hepatic dysfunction may limit options."
        ],
        resolution_strategy="Individualized risk-benefit assessment, patient education, and periodic review.",
        entity_scope="Cardiology, primary care",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AHA/ACC/HRS AFib Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Myasthenia Gravis",
        keywords=[
            "myasthenia gravis", "acetylcholine receptor antibody", "MuSK", "edrophonium", "ice pack test", "pyridostigmine", "thymectomy"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for myasthenia gravis; recommended management is {management_plan}.",
        reasoning_framework="""
        1. Identify fluctuating muscle weakness, especially ocular, bulbar, and proximal limb muscles.
        2. Confirm diagnosis with serology (AChR, MuSK antibodies) or electrophysiology (repetitive nerve stimulation, SFEMG).
        3. Use bedside tests (ice pack, edrophonium) if needed.
        4. Assess for thymoma with chest imaging.
        5. Initiate symptomatic therapy (pyridostigmine).
        6. Consider immunosuppression (steroids, azathioprine) for generalized disease.
        7. Thymectomy for all patients with thymoma and select non-thymoma cases.
        """,
        key_factors=[
            "Clinical features", "Antibody status", "Electrophysiology", "Thymic imaging"
        ],
        primary_authority=[
            "AAN Myasthenia Gravis Guidelines", "MGFA Recommendations"
        ],
        burden_holder="Neuromuscular Specialist",
        adversary_position="Symptoms may be due to other neuromuscular disorders.",
        counter_arguments=[
            "Seronegative MG may require advanced testing.",
            "Overlap with Lambert-Eaton or motor neuron disease.",
            "Immunosuppression risks."
        ],
        resolution_strategy="Multimodal diagnostic approach, multidisciplinary management, and patient-centered care.",
        entity_scope="Neuromuscular clinics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AAN/MGFA Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Acute Management of Guillain-Barré Syndrome",
        keywords=[
            "guillain-barré", "GBS", "areflexia", "ascending weakness", "CSF albuminocytologic dissociation", "IVIG", "plasmapheresis"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for GBS; acute management initiated with {treatment_choice}.",
        reasoning_framework="""
        1. Recognize acute, progressive, symmetrical weakness with areflexia.
        2. Assess for sensory symptoms and cranial nerve involvement.
        3. Perform CSF analysis (elevated protein, normal WBC).
        4. Nerve conduction studies support demyelination.
        5. Initiate IVIG or plasmapheresis as soon as diagnosis is suspected.
        6. Monitor respiratory function and autonomic instability.
        7. Exclude alternative diagnoses (myelopathy, botulism, tick paralysis).
        """,
        key_factors=[
            "Clinical course", "Areflexia", "CSF findings", "Electrophysiology", "Respiratory status"
        ],
        primary_authority=[
            "AAN GBS Guidelines", "CIDP Foundation"
        ],
        burden_holder="Neurologist",
        adversary_position="GBS mimics or atypical presentations may delay diagnosis.",
        counter_arguments=[
            "CSF may be normal early.",
            "Axonal variants may lack demyelination.",
            "Treatment complications (thrombosis, infection)."
        ],
        resolution_strategy="Early recognition, supportive care, and multidisciplinary management.",
        entity_scope="Hospitals, neurology wards",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAN GBS Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Chronic Inflammatory Demyelinating Polyneuropathy (CIDP)",
        keywords=[
            "CIDP", "chronic demyelinating neuropathy", "nerve conduction", "CSF protein", "IVIG", "steroids"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for CIDP; recommended management is {management_plan}.",
        reasoning_framework="""
        1. Identify progressive or relapsing symmetrical weakness and sensory loss >8 weeks.
        2. Confirm demyelination on nerve conduction studies.
        3. CSF analysis shows elevated protein with normal cell count.
        4. Exclude mimics (diabetes, hereditary neuropathy, toxins).
        5. Initiate first-line therapy (IVIG, steroids, plasmapheresis).
        6. Monitor for response and adjust therapy as needed.
        """,
        key_factors=[
            "Clinical course", "Electrophysiology", "CSF findings", "Exclusion of mimics"
        ],
        primary_authority=[
            "EFNS/PNS CIDP Guidelines", "AAN Guidelines"
        ],
        burden_holder="Neuromuscular Specialist",
        adversary_position="Chronic neuropathy due to other causes.",
        counter_arguments=[
            "Overlap with diabetic or hereditary neuropathy.",
            "Steroid side effects.",
            "Incomplete response to therapy."
        ],
        resolution_strategy="Serial assessment, multidisciplinary review, and individualized therapy.",
        entity_scope="Neuromuscular clinics",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="EFNS/PNS CIDP Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Amyotrophic Lateral Sclerosis (ALS)",
        keywords=[
            "ALS", "motor neuron disease", "UMN", "LMN", "EMG", "riluzole", "edaravone"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for ALS; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify progressive upper and lower motor neuron signs in multiple regions.
        2. Exclude mimics (cervical myelopathy, multifocal motor neuropathy, myasthenia gravis).
        3. Confirm with EMG showing widespread denervation.
        4. Assess respiratory function and bulbar involvement.
        5. Initiate disease-modifying therapy (riluzole, edaravone).
        6. Provide multidisciplinary supportive care (nutrition, respiratory, palliative).
        """,
        key_factors=[
            "UMN and LMN signs", "EMG findings", "Exclusion of mimics", "Respiratory function"
        ],
        primary_authority=[
            "El Escorial Criteria", "AAN ALS Guidelines"
        ],
        burden_holder="Neuromuscular Specialist",
        adversary_position="Symptoms due to alternative diagnosis or atypical presentation.",
        counter_arguments=[
            "Overlap with other motor neuron disorders.",
            "Diagnostic delay is common.",
            "Limited disease-modifying options."
        ],
        resolution_strategy="Early referral to ALS center, multidisciplinary care, and patient/family support.",
        entity_scope="ALS clinics, neurology centers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="El Escorial Criteria"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Lambert-Eaton Myasthenic Syndrome (LEMS)",
        keywords=[
            "LEMS", "lambert-eaton", "proximal weakness", "autonomic symptoms", "VGCC antibody", "small cell lung cancer"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for LEMS; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify proximal muscle weakness with autonomic symptoms (dry mouth, impotence).
        2. Confirm with electrophysiology (incremental response on repetitive stimulation).
        3. Test for VGCC antibodies.
        4. Screen for underlying malignancy (small cell lung cancer).
        5. Initiate symptomatic therapy (3,4-diaminopyridine, pyridostigmine).
        6. Treat underlying malignancy if present.
        """,
        key_factors=[
            "Clinical features", "Electrophysiology", "Antibody status", "Malignancy screening"
        ],
        primary_authority=[
            "AAN LEMS Guidelines", "EFNS Recommendations"
        ],
        burden_holder="Neuromuscular Specialist",
        adversary_position="Symptoms due to other neuromuscular junction disorders.",
        counter_arguments=[
            "Overlap with myasthenia gravis.",
            "Antibody-negative cases.",
            "Malignancy may be occult."
        ],
        resolution_strategy="Comprehensive diagnostic approach, oncology collaboration, and tailored therapy.",
        entity_scope="Neuromuscular and oncology clinics",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN/EFNS LEMS Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Bell's Palsy",
        keywords=[
            "bell's palsy", "facial palsy", "corticosteroids", "antivirals", "house-brackmann", "lyme disease"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for Bell's palsy; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify acute, unilateral, lower motor neuron facial weakness.
        2. Exclude alternative causes (stroke, Lyme disease, tumor, otitis).
        3. Assess severity using House-Brackmann scale.
        4. Initiate corticosteroids within 72 hours of onset.
        5. Consider antivirals for severe cases.
        6. Provide eye protection and supportive care.
        """,
        key_factors=[
            "Clinical presentation", "Exclusion of mimics", "Severity grading", "Timing of therapy"
        ],
        primary_authority=[
            "AAN Bell's Palsy Guidelines", "IDSA Lyme Guidelines"
        ],
        burden_holder="Neurologist/Primary Care",
        adversary_position="Facial weakness due to alternative etiology.",
        counter_arguments=[
            "Lyme disease may require antibiotics.",
            "Delayed therapy reduces efficacy.",
            "Incomplete recovery in severe cases."
        ],
        resolution_strategy="Prompt diagnosis, exclusion of mimics, and early initiation of therapy.",
        entity_scope="Primary care, neurology",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAN Bell's Palsy Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Trigeminal Neuralgia",
        keywords=[
            "trigeminal neuralgia", "facial pain", "carbamazepine", "MRI", "vascular compression", "surgical options"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for trigeminal neuralgia; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify recurrent, unilateral, brief, electric shock-like facial pain in trigeminal distribution.
        2. Exclude secondary causes with MRI (tumor, MS, vascular malformation).
        3. Initiate first-line therapy with carbamazepine or oxcarbazepine.
        4. Consider surgical options (microvascular decompression, radiofrequency ablation) for refractory cases.
        5. Monitor for medication side effects.
        """,
        key_factors=[
            "Pain characteristics", "Imaging exclusion", "Response to therapy", "Surgical candidacy"
        ],
        primary_authority=[
            "AAN Trigeminal Neuralgia Guidelines", "EFNS Recommendations"
        ],
        burden_holder="Neurologist/Pain Specialist",
        adversary_position="Atypical facial pain or secondary neuralgia.",
        counter_arguments=[
            "Medication intolerance.",
            "Secondary causes may require different management.",
            "Surgical risks."
        ],
        resolution_strategy="Comprehensive evaluation, imaging, and stepwise therapy escalation.",
        entity_scope="Pain clinics, neurology",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Trigeminal Neuralgia Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Cluster Headache",
        keywords=[
            "cluster headache", "trigeminal autonomic cephalalgia", "oxygen therapy", "sumatriptan", "verapamil", "ICHD-3"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for cluster headache; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify severe, unilateral, orbital/temporal pain with autonomic features (lacrimation, rhinorrhea, ptosis).
        2. Attacks occur in clusters (weeks-months) with remission periods.
        3. Exclude secondary causes with MRI if atypical features.
        4. Acute treatment: high-flow oxygen, subcutaneous sumatriptan.
        5. Preventive therapy: verapamil, lithium, corticosteroids.
        6. Monitor for side effects and adjust therapy as needed.
        """,
        key_factors=[
            "Attack characteristics", "Autonomic features", "Response to acute therapy", "Preventive options"
        ],
        primary_authority=[
            "ICHD-3", "AAN Cluster Headache Guidelines"
        ],
        burden_holder="Headache Specialist/Neurologist",
        adversary_position="Atypical features or secondary headache.",
        counter_arguments=[
            "Medication contraindications.",
            "Oxygen access issues.",
            "Overlap with migraine or other TACs."
        ],
        resolution_strategy="Accurate diagnosis, individualized therapy, and patient education.",
        entity_scope="Headache clinics, neurology",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="ICHD-3/AAN Cluster Headache Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Tension-Type Headache",
        keywords=[
            "tension-type headache", "headache", "analgesics", "amitriptyline", "ICHD-3", "prophylaxis"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for tension-type headache; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify bilateral, pressing/tightening, mild-moderate headache without nausea or photophobia.
        2. Exclude secondary causes if red flags present.
        3. Acute treatment: simple analgesics (acetaminophen, NSAIDs).
        4. Preventive therapy: amitriptyline for frequent/chronic cases.
        5. Educate on lifestyle modification and stress management.
        """,
        key_factors=[
            "Headache characteristics", "Exclusion of secondary causes", "Response to therapy", "Prophylactic indication"
        ],
        primary_authority=[
            "ICHD-3", "AAN Tension-Type Headache Guidelines"
        ],
        burden_holder="Primary Care/Neurologist",
        adversary_position="Chronic headache may have mixed or secondary etiology.",
        counter_arguments=[
            "Medication overuse headache.",
            "Psychiatric comorbidities.",
            "Incomplete response to therapy."
        ],
        resolution_strategy="Comprehensive assessment, patient education, and stepwise therapy.",
        entity_scope="Primary care, neurology",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="ICHD-3/AAN Tension-Type Headache Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Idiopathic Intracranial Hypertension (IIH)",
        keywords=[
            "IIH", "pseudotumor cerebri", "papilledema", "CSF opening pressure", "acetazolamide", "weight loss"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for IIH; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify symptoms: headache, transient visual obscurations, pulsatile tinnitus.
        2. Confirm papilledema on fundoscopic exam.
        3. Exclude secondary causes with MRI/MRV.
        4. Perform lumbar puncture: elevated opening pressure, normal CSF composition.
        5. Initiate acetazolamide and recommend weight loss.
        6. Monitor visual function and consider surgical intervention if progressive loss.
        """,
        key_factors=[
            "Symptoms", "Papilledema", "Imaging exclusion", "CSF opening pressure"
        ],
        primary_authority=[
            "Friedman Criteria", "AAN IIH Guidelines"
        ],
        burden_holder="Neuro-ophthalmologist/Neurologist",
        adversary_position="Symptoms due to secondary intracranial hypertension.",
        counter_arguments=[
            "Venous sinus thrombosis may mimic IIH.",
            "Medication intolerance.",
            "Vision loss despite therapy."
        ],
        resolution_strategy="Comprehensive evaluation, serial visual monitoring, and multidisciplinary management.",
        entity_scope="Neuro-ophthalmology, neurology",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="Friedman Criteria/AAN IIH Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Normal Pressure Hydrocephalus (NPH)",
        keywords=[
            "NPH", "gait disturbance", "urinary incontinence", "cognitive decline", "ventriculomegaly", "CSF tap test"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for NPH; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify classic triad: gait disturbance, cognitive decline, urinary incontinence.
        2. Confirm ventriculomegaly on imaging (Evans index >0.3).
        3. Exclude alternative causes (Alzheimer, Parkinson, subcortical ischemia).
        4. Perform large-volume CSF tap test to assess response.
        5. Consider ventriculoperitoneal shunt if improvement noted.
        6. Monitor for shunt complications.
        """,
        key_factors=[
            "Clinical triad", "Imaging findings", "Tap test response", "Exclusion of mimics"
        ],
        primary_authority=[
            "AAN NPH Guidelines", "Japanese NPH Guidelines"
        ],
        burden_holder="Neurologist/Neurosurgeon",
        adversary_position="Symptoms due to other neurodegenerative or vascular causes.",
        counter_arguments=[
            "Tap test may be falsely negative.",
            "Shunt complications.",
            "Mixed pathologies."
        ],
        resolution_strategy="Multidisciplinary evaluation, careful patient selection, and post-shunt monitoring.",
        entity_scope="Neurology, neurosurgery",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN NPH Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Restless Legs Syndrome (RLS)",
        keywords=[
            "restless legs", "RLS", "dopamine agonists", "iron deficiency", "sleep disorder", "gabapentin"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for RLS; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify urge to move legs, worse at rest and night, relieved by movement.
        2. Exclude mimics (neuropathy, akathisia, cramps).
        3. Check ferritin and correct iron deficiency.
        4. Initiate dopamine agonists or gabapentin for moderate-severe symptoms.
        5. Monitor for augmentation and side effects.
        """,
        key_factors=[
            "Clinical criteria", "Exclusion of mimics", "Iron status", "Response to therapy"
        ],
        primary_authority=[
            "IRLSSG Criteria", "AAN RLS Guidelines"
        ],
        burden_holder="Sleep Specialist/Neurologist",
        adversary_position="Symptoms due to other sleep or movement disorders.",
        counter_arguments=[
            "Medication side effects.",
            "Augmentation with dopamine agonists.",
            "Incomplete response."
        ],
        resolution_strategy="Comprehensive evaluation, iron repletion, and individualized therapy.",
        entity_scope="Sleep clinics, neurology",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="IRLSSG/AAN RLS Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Essential Tremor",
        keywords=[
            "essential tremor", "postural tremor", "propranolol", "primidone", "deep brain stimulation"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for essential tremor; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify bilateral, symmetric, postural or action tremor of hands/forearms.
        2. Exclude other causes (Parkinson, hyperthyroidism, medication-induced).
        3. Assess impact on daily function.
        4. Initiate first-line therapy (propranolol, primidone).
        5. Consider deep brain stimulation for refractory cases.
        """,
        key_factors=[
            "Tremor characteristics", "Exclusion of mimics", "Functional impact", "Response to therapy"
        ],
        primary_authority=[
            "AAN Essential Tremor Guidelines", "MDS Recommendations"
        ],
        burden_holder="Neurologist",
        adversary_position="Tremor due to alternative etiology.",
        counter_arguments=[
            "Medication intolerance.",
            "Overlap with Parkinson disease.",
            "Surgical risks."
        ],
        resolution_strategy="Comprehensive assessment, trial of therapy, and consideration of advanced interventions.",
        entity_scope="Movement disorders clinics",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Essential Tremor Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Huntington Disease",
        keywords=[
            "huntington disease", "chorea", "genetic testing", "CAG repeat", "psychiatric symptoms", "tetrabenazine"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for Huntington disease; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify progressive chorea, psychiatric symptoms, and cognitive decline.
        2. Confirm diagnosis with genetic testing (CAG repeat expansion in HTT gene).
        3. Assess family history and age of onset.
        4. Provide symptomatic therapy (tetrabenazine, antipsychotics).
        5. Offer genetic counseling and multidisciplinary support.
        """,
        key_factors=[
            "Clinical features", "Genetic confirmation", "Family history", "Symptomatic therapy"
        ],
        primary_authority=[
            "AAN Huntington Disease Guidelines", "HDSA Recommendations"
        ],
        burden_holder="Neurologist/Genetic Counselor",
        adversary_position="Symptoms due to other movement or psychiatric disorders.",
        counter_arguments=[
            "Genetic testing may have ethical implications.",
            "Symptomatic therapy may be limited.",
            "Family impact."
        ],
        resolution_strategy="Genetic counseling, multidisciplinary care, and patient/family support.",
        entity_scope="Movement disorders, genetics",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Huntington Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Wilson Disease",
        keywords=[
            "wilson disease", "copper metabolism", "ceruloplasmin", "kayser-fleischer rings", "liver disease", "penicillamine"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for Wilson disease; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify hepatic, neurological, and psychiatric symptoms in young patients.
        2. Confirm low ceruloplasmin, elevated urinary copper, and presence of Kayser-Fleischer rings.
        3. Genetic testing for ATP7B mutations as needed.
        4. Initiate chelation therapy (penicillamine, trientine) and zinc.
        5. Monitor for hepatic and neurological complications.
        """,
        key_factors=[
            "Clinical features", "Copper studies", "Ophthalmologic findings", "Genetic testing"
        ],
        primary_authority=[
            "AASLD Wilson Disease Guidelines", "AAN Recommendations"
        ],
        burden_holder="Neurologist/Hepatologist",
        adversary_position="Symptoms due to other liver or movement disorders.",
        counter_arguments=[
            "Overlap with other hepatic or neuropsychiatric diseases.",
            "Chelation therapy side effects.",
            "Delayed diagnosis."
        ],
        resolution_strategy="Comprehensive metabolic and genetic evaluation, multidisciplinary care.",
        entity_scope="Neurology, hepatology",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AASLD/AAN Wilson Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Peripheral Neuropathy",
        keywords=[
            "peripheral neuropathy", "nerve conduction", "EMG", "diabetes", "B12 deficiency", "gabapentin"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for peripheral neuropathy; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify sensory, motor, or autonomic symptoms and distribution.
        2. Confirm with nerve conduction studies and EMG.
        3. Screen for common causes (diabetes, B12 deficiency, alcohol, toxins).
        4. Treat underlying cause and initiate symptomatic therapy (gabapentin, pregabalin).
        5. Monitor for progression and adjust therapy.
        """,
        key_factors=[
            "Clinical features", "Electrophysiology", "Etiology", "Response to therapy"
        ],
        primary_authority=[
            "AAN Peripheral Neuropathy Guidelines", "EFNS Recommendations"
        ],
        burden_holder="Neurologist/Primary Care",
        adversary_position="Symptoms due to central or non-neurological causes.",
        counter_arguments=[
            "Overlap with radiculopathy or myopathy.",
            "Incomplete workup.",
            "Medication side effects."
        ],
        resolution_strategy="Comprehensive evaluation, targeted therapy, and periodic reassessment.",
        entity_scope="Primary care, neurology",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Peripheral Neuropathy Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Carpal Tunnel Syndrome",
        keywords=[
            "carpal tunnel", "median nerve", "nerve conduction", "splinting", "corticosteroid injection", "surgery"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for carpal tunnel syndrome; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify numbness, tingling, and weakness in median nerve distribution.
        2. Confirm with nerve conduction studies.
        3. Assess severity and functional impact.
        4. Initiate conservative therapy (splinting, activity modification).
        5. Consider corticosteroid injection or surgical decompression for refractory cases.
        """,
        key_factors=[
            "Clinical features", "Electrophysiology", "Severity", "Response to therapy"
        ],
        primary_authority=[
            "AAN Carpal Tunnel Guidelines", "AAOS Recommendations"
        ],
        burden_holder="Neurologist/Orthopedist",
        adversary_position="Symptoms due to other neuropathy or musculoskeletal disorder.",
        counter_arguments=[
            "Overlap with cervical radiculopathy.",
            "Surgical risks.",
            "Recurrence after therapy."
        ],
        resolution_strategy="Comprehensive assessment, stepwise therapy, and patient education.",
        entity_scope="Primary care, neurology, orthopedics",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Carpal Tunnel Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Myopathy",
        keywords=[
            "myopathy", "CK", "EMG", "muscle biopsy", "steroids", "inflammatory myopathy"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for myopathy; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify proximal muscle weakness and atrophy.
        2. Check serum CK and other muscle enzymes.
        3. Confirm with EMG and muscle biopsy if indicated.
        4. Screen for inflammatory, metabolic, and hereditary causes.
        5. Initiate immunosuppressive therapy for inflammatory myopathies.
        6. Monitor for side effects and disease progression.
        """,
        key_factors=[
            "Clinical features", "CK level", "EMG findings", "Biopsy", "Etiology"
        ],
        primary_authority=[
            "AAN Myopathy Guidelines", "ENMC Recommendations"
        ],
        burden_holder="Neuromuscular Specialist",
        adversary_position="Weakness due to neuropathy or central cause.",
        counter_arguments=[
            "Overlap with motor neuron disease.",
            "Biopsy may be non-diagnostic.",
            "Steroid side effects."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and individualized therapy.",
        entity_scope="Neuromuscular clinics",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Myopathy Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Cerebral Palsy",
        keywords=[
            "cerebral palsy", "spasticity", "motor delay", "MRI", "multidisciplinary care", "botulinum toxin"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for cerebral palsy; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify non-progressive motor impairment with onset in early childhood.
        2. Assess for spasticity, dystonia, ataxia, and associated deficits.
        3. Confirm with neuroimaging (MRI) to identify perinatal brain injury.
        4. Exclude progressive or genetic disorders.
        5. Initiate multidisciplinary care (PT, OT, speech, orthopedics).
        6. Consider botulinum toxin or baclofen for spasticity.
        """,
        key_factors=[
            "Clinical features", "Imaging findings", "Exclusion of progressive disease", "Functional impact"
        ],
        primary_authority=[
            "AACPDM Guidelines", "AAN Recommendations"
        ],
        burden_holder="Pediatric Neurologist",
        adversary_position="Progressive or genetic disorder mimicking CP.",
        counter_arguments=[
            "Genetic testing may be needed.",
            "Overlap with metabolic disorders.",
            "Variable response to therapy."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and ongoing reassessment.",
        entity_scope="Pediatrics, neurology, rehabilitation",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AACPDM/AAN Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Spinal Cord Compression",
        keywords=[
            "spinal cord compression", "myelopathy", "MRI", "emergency", "steroids", "surgery"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for spinal cord compression; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify acute or subacute myelopathy (weakness, sensory loss, sphincter dysfunction).
        2. Obtain emergent MRI to confirm compression and identify etiology (tumor, abscess, herniation).
        3. Initiate high-dose steroids if malignancy suspected.
        4. Consult neurosurgery or orthopedics for decompression.
        5. Monitor for neurological deterioration.
        """,
        key_factors=[
            "Clinical features", "Imaging confirmation", "Etiology", "Timing of intervention"
        ],
        primary_authority=[
            "AAN Spinal Cord Compression Guidelines", "NCCN Recommendations"
        ],
        burden_holder="Neurologist/Neurosurgeon",
        adversary_position="Symptoms due to non-compressive myelopathy.",
        counter_arguments=[
            "Steroid risks.",
            "Delay in imaging or intervention.",
            "Non-compressive etiologies."
        ],
        resolution_strategy="Rapid diagnostic workup, multidisciplinary coordination, and timely intervention.",
        entity_scope="Hospitals, neurology, neurosurgery",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAN Spinal Cord Compression Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Subarachnoid Hemorrhage (SAH)",
        keywords=[
            "subarachnoid hemorrhage", "SAH", "thunderclap headache", "CT head", "LP", "aneurysm", "coiling"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for SAH; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify sudden, severe "thunderclap" headache, often with neck stiffness or loss of consciousness.
        2. Obtain emergent non-contrast CT head.
        3. If CT negative and suspicion remains, perform LP for xanthochromia.
        4. Confirm aneurysm with CTA/MRA.
        5. Initiate blood pressure control, nimodipine, and neurosurgical consultation for coiling/clipping.
        6. Monitor for vasospasm and hydrocephalus.
        """,
        key_factors=[
            "Clinical presentation", "Imaging findings", "LP results", "Aneurysm identification"
        ],
        primary_authority=[
            "AHA/ASA SAH Guidelines", "WFNS Recommendations"
        ],
        burden_holder="Emergency Physician/Neurologist",
        adversary_position="Headache due to other etiology or negative workup.",
        counter_arguments=[
            "CT sensitivity decreases over time.",
            "LP may be traumatic.",
            "Aneurysm may be incidental."
        ],
        resolution_strategy="Comprehensive workup, multidisciplinary management, and serial monitoring.",
        entity_scope="Emergency, neurology, neurosurgery",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AHA/ASA SAH Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Intracerebral Hemorrhage (ICH)",
        keywords=[
            "intracerebral hemorrhage", "ICH", "CT head", "blood pressure control", "neurosurgery", "anticoagulation reversal"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for ICH; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify acute focal neurological deficit with headache, vomiting, or altered consciousness.
        2. Confirm with emergent non-contrast CT head.
        3. Initiate blood pressure control (SBP <140 mmHg).
        4. Reverse anticoagulation if present.
        5. Consult neurosurgery for large or accessible hematomas.
        6. Monitor for increased intracranial pressure and complications.
        """,
        key_factors=[
            "Clinical presentation", "Imaging confirmation", "Blood pressure", "Anticoagulation status"
        ],
        primary_authority=[
            "AHA/ASA ICH Guidelines", "Neurocritical Care Society"
        ],
        burden_holder="Emergency Physician/Neurologist",
        adversary_position="Hemorrhage due to trauma or underlying lesion.",
        counter_arguments=[
            "Underlying vascular malformation or tumor.",
            "Surgical risks.",
            "Rebleeding risk."
        ],
        resolution_strategy="Comprehensive evaluation, guideline-based management, and multidisciplinary care.",
        entity_scope="Emergency, neurology, neurosurgery",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AHA/ASA ICH Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Brain Abscess",
        keywords=[
            "brain abscess", "ring-enhancing lesion", "MRI", "antibiotics", "neurosurgery", "source control"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for brain abscess; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify focal neurological deficit, headache, fever, or seizure.
        2. Confirm with MRI showing ring-enhancing lesion.
        3. Avoid LP if mass effect present.
        4. Initiate empiric antibiotics and consult neurosurgery for drainage.
        5. Identify and treat primary source (sinus, dental, cardiac).
        6. Monitor for complications and adjust antibiotics based on culture.
        """,
        key_factors=[
            "Imaging findings", "Clinical features", "Source identification", "Response to therapy"
        ],
        primary_authority=[
            "IDSA Brain Abscess Guidelines", "AAN Recommendations"
        ],
        burden_holder="Neurologist/Infectious Disease",
        adversary_position="Lesion due to tumor or other infection.",
        counter_arguments=[
            "Imaging overlap with neoplasm.",
            "Antibiotic resistance.",
            "Surgical risks."
        ],
        resolution_strategy="Comprehensive workup, multidisciplinary management, and serial imaging.",
        entity_scope="Hospitals, neurology, neurosurgery",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IDSA Brain Abscess Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Meningitis",
        keywords=[
            "meningitis", "CSF analysis", "bacterial", "viral", "empiric antibiotics", "steroids"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for meningitis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify fever, headache, neck stiffness, and altered mental status.
        2. Perform LP for CSF analysis (cell count, glucose, protein, Gram stain, PCR).
        3. Initiate empiric antibiotics and dexamethasone for suspected bacterial meningitis.
        4. Adjust therapy based on culture/PCR results.
        5. Monitor for complications (hydrocephalus, seizures).
        """,
        key_factors=[
            "Clinical features", "CSF findings", "Empiric therapy", "Response to treatment"
        ],
        primary_authority=[
            "IDSA Meningitis Guidelines", "AAN Recommendations"
        ],
        burden_holder="Neurologist/Infectious Disease",
        adversary_position="Symptoms due to encephalitis or non-infectious cause.",
        counter_arguments=[
            "Partial treatment may alter CSF findings.",
            "Overlap with encephalitis.",
            "Steroid risks."
        ],
        resolution_strategy="Comprehensive evaluation, guideline-based therapy, and serial monitoring.",
        entity_scope="Hospitals, neurology, infectious disease",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDSA Meningitis Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Encephalitis",
        keywords=[
            "encephalitis", "HSV", "CSF PCR", "MRI", "acyclovir", "seizures"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for encephalitis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify altered mental status, fever, seizures, or focal deficits.
        2. Perform LP for CSF analysis and PCR for HSV and other viruses.
        3. Obtain MRI to identify temporal lobe involvement.
        4. Initiate empiric acyclovir for suspected HSV encephalitis.
        5. Monitor for complications and adjust therapy based on PCR results.
        """,
        key_factors=[
            "Clinical features", "CSF PCR", "MRI findings", "Empiric therapy"
        ],
        primary_authority=[
            "IDSA Encephalitis Guidelines", "AAN Recommendations"
        ],
        burden_holder="Neurologist/Infectious Disease",
        adversary_position="Symptoms due to non-infectious or metabolic encephalopathy.",
        counter_arguments=[
            "PCR may be negative early.",
            "Overlap with autoimmune encephalitis.",
            "Acyclovir toxicity."
        ],
        resolution_strategy="Comprehensive evaluation, serial testing, and multidisciplinary management.",
        entity_scope="Hospitals, neurology, infectious disease",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IDSA Encephalitis Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Autoimmune Encephalitis",
        keywords=[
            "autoimmune encephalitis", "NMDA receptor", "CSF antibodies", "MRI", "immunotherapy", "tumor screening"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for autoimmune encephalitis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify subacute onset of memory deficits, psychiatric symptoms, seizures, or movement disorder.
        2. Perform CSF and serum antibody testing (NMDA, LGI1, CASPR2, etc.).
        3. Obtain MRI and EEG for supportive findings.
        4. Screen for underlying malignancy (ovarian teratoma, lung, thymus).
        5. Initiate immunotherapy (steroids, IVIG, plasmapheresis).
        6. Escalate to rituximab or cyclophosphamide if refractory.
        """,
        key_factors=[
            "Clinical features", "Antibody testing", "Imaging findings", "Tumor screening"
        ],
        primary_authority=[
            "Lancet Neurology 2016 Consensus", "AAN Recommendations"
        ],
        burden_holder="Neurologist",
        adversary_position="Symptoms due to infectious or metabolic encephalopathy.",
        counter_arguments=[
            "Antibody-negative cases.",
            "Overlap with psychiatric disorders.",
            "Immunotherapy risks."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and serial monitoring.",
        entity_scope="Hospitals, neurology",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="Lancet Neurology 2016 Consensus"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Neurocysticercosis",
        keywords=[
            "neurocysticercosis", "seizures", "MRI", "cystic lesions", "albendazole", "steroids"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for neurocysticercosis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify seizures, headache, or focal deficits in endemic areas.
        2. Confirm with MRI showing cystic lesions with scolex.
        3. Serological testing for Taenia solium antibodies.
        4. Initiate antiparasitic therapy (albendazole) and steroids to reduce inflammation.
        5. Manage seizures and monitor for complications (hydrocephalus).
        """,
        key_factors=[
            "Imaging findings", "Serology", "Clinical features", "Response to therapy"
        ],
        primary_authority=[
            "IDSA Neurocysticercosis Guidelines", "CDC Recommendations"
        ],
        burden_holder="Neurologist/Infectious Disease",
        adversary_position="Lesions due to tumor or other infection.",
        counter_arguments=[
            "Antiparasitic therapy may worsen edema.",
            "Overlap with other ring-enhancing lesions.",
            "Steroid side effects."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and individualized therapy.",
        entity_scope="Hospitals, neurology, infectious disease",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="IDSA Neurocysticercosis Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Neurosarcoidosis",
        keywords=[
            "neurosarcoidosis", "granulomatous disease", "MRI", "CSF", "biopsy", "steroids"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for neurosarcoidosis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify neurological symptoms in patient with known or suspected sarcoidosis.
        2. MRI shows meningeal enhancement, parenchymal lesions, or cranial nerve involvement.
        3. CSF analysis may show lymphocytic pleocytosis, elevated protein, low glucose.
        4. Confirm with biopsy of accessible lesion.
        5. Initiate corticosteroids; escalate to immunosuppressants if refractory.
        """,
        key_factors=[
            "Clinical features", "Imaging findings", "CSF analysis", "Biopsy confirmation"
        ],
        primary_authority=[
            "AAN Neurosarcoidosis Guidelines", "ATS Sarcoidosis Guidelines"
        ],
        burden_holder="Neurologist",
        adversary_position="Symptoms due to other inflammatory or neoplastic disease.",
        counter_arguments=[
            "Biopsy may not be feasible.",
            "Steroid side effects.",
            "Overlap with infectious etiologies."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and individualized therapy.",
        entity_scope="Hospitals, neurology",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN Neurosarcoidosis Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of CNS Vasculitis",
        keywords=[
            "CNS vasculitis", "angiography", "MRI", "CSF", "biopsy", "immunosuppression"
        ],
        conclusion_template="Diagnosis is {diagnosis_status} for CNS vasculitis; management plan includes {management_plan}.",
        reasoning_framework="""
        1. Identify subacute multifocal neurological deficits, headache, or cognitive decline.
        2. MRI shows multifocal infarcts or hemorrhages.
        3. Angiography reveals beading or narrowing of vessels.
        4. Exclude mimics (infection, embolic disease, RCVS).
        5. CSF may show lymphocytic pleocytosis and elevated protein.
        6. Confirm with brain or meningeal biopsy if possible.
        7. Initiate immunosuppressive therapy (steroids, cyclophosphamide).
        """,
        key_factors=[
            "Clinical features", "Imaging/angiography", "CSF analysis", "Biopsy confirmation"
        ],
        primary_authority=[
            "AAN CNS Vasculitis Guidelines", "ACR Recommendations"
        ],
        burden_holder="Neurologist/Rheumatologist",
        adversary_position="Symptoms due to other vascular or inflammatory disease.",
        counter_arguments=[
            "Biopsy may be non-diagnostic.",
            "Immunosuppression risks.",
            "Overlap with RCVS or infection."
        ],
        resolution_strategy="Comprehensive evaluation, multidisciplinary care, and individualized therapy.",
        entity_scope="Hospitals, neurology, rheumatology",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAN CNS Vasculitis Guidelines"
    ),
    DoctrineBlock(
        topic="Diagnosis and Management of Rapidly Progressive