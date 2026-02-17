"""
MED08 Neurology Analysis Engine v1.0.0
Tax Intelligence Engine (TIE) Architecture - Neurology Domain

Analyzes neurological conditions with real clinical protocols:
- Stroke assessment (NIHSS, tPA eligibility, thrombectomy criteria)
- Seizure classification (ILAE 2017) and epilepsy management
- Neurodegenerative diseases (Parkinson, Alzheimer, MS)
- Traumatic brain injury (GCS, mild/moderate/severe)
- Neuroimaging interpretation (CT/MRI stroke protocols)
- Neurological examination and diagnostic testing

Port: 9233
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMERATIONS AND DATA MODELS
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
    STROKE_ACUTE = "STROKE_ACUTE"
    STROKE_CHRONIC = "STROKE_CHRONIC"
    SEIZURE_CLASSIFICATION = "SEIZURE_CLASSIFICATION"
    EPILEPSY_MANAGEMENT = "EPILEPSY_MANAGEMENT"
    PARKINSONS_DISEASE = "PARKINSONS_DISEASE"
    ALZHEIMERS_DEMENTIA = "ALZHEIMERS_DEMENTIA"
    MULTIPLE_SCLEROSIS = "MULTIPLE_SCLEROSIS"
    TRAUMATIC_BRAIN_INJURY = "TRAUMATIC_BRAIN_INJURY"
    NEUROIMAGING_INTERPRETATION = "NEUROIMAGING_INTERPRETATION"
    CSF_ANALYSIS = "CSF_ANALYSIS"
    NEURO_EXAMINATION = "NEURO_EXAMINATION"
    HEADACHE_DISORDERS = "HEADACHE_DISORDERS"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass
class DoctrineBlock:
    """Core knowledge unit with real neurological expertise"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = "ALL_PATIENTS"
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    confidence_stratification: Optional[str] = None
    controlling_precedent: Optional[str] = None


@dataclass
class TelemetryData:
    """Query execution telemetry"""
    query_id: str
    timestamp: str
    latency_ms: float
    cache_hit: bool
    doctrine_topics_triggered: List[str]
    confidence_level: str
    response_mode: str
    zone: str
    error_domain: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE - REAL NEUROLOGY EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # === STROKE - ACUTE MANAGEMENT ===
    DoctrineBlock(
        topic="Acute Ischemic Stroke tPA Eligibility",
        keywords=["tpa", "alteplase", "thrombolysis", "stroke", "window", "contraindication", "NIHSS"],
        conclusion_template="tPA eligibility determination requires strict adherence to time windows and exclusion criteria. Standard window is 3 hours from last known well time, extended to 4.5 hours in select patients. NIHSS score guides severity assessment. Absolute contraindications include recent hemorrhage, active bleeding, prior ICH. Relative contraindications require risk-benefit analysis.",
        reasoning_framework="""
1. TIME WINDOW ASSESSMENT (Critical Gate):
   - Last known well (LKW) time = time patient last seen at baseline
   - Standard window: 0-3 hours from LKW (Class I, Level A evidence)
   - Extended window: 3-4.5 hours (Class I, Level B evidence) if patient meets criteria:
     * Age < 80 years
     * No history of diabetes AND prior stroke
     * NIHSS ≤ 25
     * Not on oral anticoagulants
   - Wake-up strokes: Consider imaging-based selection (MRI DWI-FLAIR mismatch)

2. ABSOLUTE CONTRAINDICATIONS (Hard Stops):
   - Intracranial hemorrhage (current or prior)
   - Acute bleeding or bleeding diathesis (platelets < 100,000, INR > 1.7, aPTT > 40s)
   - Recent intracranial/intraspinal surgery (within 3 months)
   - Severe uncontrolled hypertension (BP > 185/110 despite treatment)
   - Active internal bleeding
   - Ischemic stroke or head trauma within 3 months
   - Subarachnoid hemorrhage
   - Arterial puncture at non-compressible site within 7 days
   - History of intracranial hemorrhage
   - Intracranial neoplasm, AVM, or aneurysm

3. RELATIVE CONTRAINDICATIONS (Risk-Benefit Analysis):
   - Rapidly improving or minor symptoms (NIHSS < 4): Consider natural history vs. risk
   - Severe stroke (NIHSS > 22): Higher hemorrhage risk but potential benefit
   - Recent surgery or trauma (14-30 days): Case-by-case
   - Recent GI or urinary hemorrhage (within 21 days)
   - Recent myocardial infarction (within 3 months)
   - Pregnancy: Relative contraindication, consider if disabling stroke

4. NIHSS SCORE INTERPRETATION (Severity Stratification):
   - 0: No stroke symptoms
   - 1-4: Minor stroke (consider tPA vs. natural history)
   - 5-15: Moderate stroke (clear tPA benefit)
   - 16-20: Moderate to severe stroke
   - 21-42: Severe stroke (higher hemorrhage risk, but potential benefit)
   - NIHSS components: LOC, gaze, visual fields, facial palsy, motor arm/leg, ataxia, sensory, language, dysarthria, extinction

5. PRE-TREATMENT CHECKLIST:
   - CT head to rule out hemorrhage and large territory infarct (> 1/3 MCA)
   - Blood pressure control to < 185/110 (labetalol, nicardipine)
   - Labs: CBC, PT/INR, aPTT, glucose
   - Review medication list (anticoagulants, recent heparin)
   - Consent discussion: 6% symptomatic ICH risk vs. 30% improved outcome

6. DOSING AND ADMINISTRATION:
   - Dose: 0.9 mg/kg (maximum 90 mg)
   - 10% as bolus over 1 minute
   - Remaining 90% as infusion over 60 minutes
   - Monitor BP every 15 minutes during and after infusion
   - No anticoagulants or antiplatelets for 24 hours post-tPA
   - Repeat CT if neurological deterioration
        """,
        key_factors=[
            "Last known well time < 3 hours (or < 4.5 hours with extended criteria)",
            "CT excludes intracranial hemorrhage and large infarct",
            "No absolute contraindications present",
            "BP controlled to < 185/110 mmHg",
            "NIHSS score documents severity and eligibility",
            "Patient or family consent obtained after risk discussion",
            "Platelet count > 100,000, INR ≤ 1.7, aPTT ≤ 40s"
        ],
        primary_authority=[
            "AHA/ASA 2019 Guidelines for Management of Acute Ischemic Stroke",
            "NINDS rt-PA Stroke Study (NEJM 1995)",
            "ECASS III Trial (extended window to 4.5 hours, Lancet 2008)",
            "Powers et al. 2019 Stroke Guidelines Update"
        ],
        burden_holder="Treating physician",
        adversary_position="tPA carries 6% symptomatic ICH risk; alternative is expectant management with antiplatelet therapy",
        counter_arguments=[
            "Natural history: 30% of untreated strokes improve spontaneously",
            "Hemorrhage risk increases with larger infarcts and severe strokes",
            "Minor strokes (NIHSS < 4) may not justify tPA risk",
            "Extended window (> 3 hours) has higher hemorrhage risk",
            "Patient age > 80 or diabetes + prior stroke increases risk"
        ],
        resolution_strategy="Apply strict time window and contraindication criteria; document NIHSS score; obtain informed consent; ensure BP control; treat if benefits outweigh risks",
        entity_scope="Acute ischemic stroke patients within treatment window",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AHA/ASA Class I recommendation for tPA within 3 hours (Level A evidence)"
    ),

    DoctrineBlock(
        topic="Mechanical Thrombectomy for Large Vessel Occlusion",
        keywords=["thrombectomy", "lvo", "stent retriever", "aspiration", "nihss", "imaging"],
        conclusion_template="Mechanical thrombectomy is indicated for large vessel occlusion (LVO) in anterior circulation within 6 hours, and up to 24 hours in select patients with favorable imaging. CTA/MRA confirms LVO. NIHSS ≥ 6 suggests LVO. Thrombectomy provides 20-30% absolute benefit in good outcomes. Combine with tPA if eligible.",
        reasoning_framework="""
1. LVO IDENTIFICATION (Imaging-Based Diagnosis):
   - Target vessels: ICA terminus, M1 MCA, proximal M2 MCA
   - CTA first-line: Visualizes clot, collaterals, vessel anatomy
   - MRA alternative: No contrast, but slower and less detailed
   - Clinical clues: NIHSS ≥ 6, cortical signs (aphasia, neglect, gaze deviation)
   - CT perfusion: Identifies penumbra (salvageable tissue) vs. core infarct

2. TIME WINDOWS (Evidence-Based):
   - 0-6 hours: Class I recommendation (MR CLEAN, ESCAPE, EXTEND-IA, SWIFT PRIME, REVASCAT trials)
     * No advanced imaging needed if LVO on CTA
     * Treat all LVO patients regardless of penumbral imaging
   - 6-16 hours: DEFUSE 3 and DAWN trials (2018)
     * Requires favorable perfusion imaging (small core, large penumbra)
     * DAWN criteria: Clinical-core mismatch (high NIHSS, small infarct)
     * DEFUSE 3 criteria: Perfusion mismatch ≥ 1.8, core < 70 mL
   - 16-24 hours: DAWN extended window
     * Age ≥ 80: NIHSS ≥ 10, core < 21 mL
     * Age < 80: NIHSS ≥ 10, core < 31 mL (or NIHSS ≥ 20, core 31-51 mL)

3. ELIGIBILITY CRITERIA:
   - Confirmed LVO on CTA/MRA (ICA, M1, proximal M2)
   - NIHSS ≥ 6 (lower scores rarely have LVO)
   - Pre-stroke mRS ≤ 1 (functional independence)
   - ASPECTS ≥ 6 (< 1/3 MCA territory infarcted on CT)
   - No contraindication to anesthesia or contrast
   - Groin access feasible

4. TECHNIQUE SELECTION:
   - Stent retrievers (Solitaire, Trevo): First-line, Class I evidence
   - Direct aspiration (ADAPT): Alternative, may reduce procedure time
   - Combined approach: Use both if initial failure
   - Target: TICI 2b-3 reperfusion (≥ 50% territory reperfused)
   - Procedure time: Door-to-groin < 90 minutes, groin-to-reperfusion < 60 minutes

5. OUTCOMES AND BENEFITS:
   - Absolute benefit: 20-30% increase in good outcome (mRS 0-2 at 90 days)
   - Number needed to treat: 3-4 patients for one good outcome
   - Mortality reduction: Not significant in most trials, but functional benefit clear
   - Hemorrhage risk: Similar to tPA alone (6-7% sICH)

6. COMBINATION WITH tPA:
   - If patient eligible for both: Give tPA first, do not delay thrombectomy
   - tPA during transfer to thrombectomy center: Drip-and-ship protocol
   - Thrombectomy alone if tPA contraindicated: Still effective

7. POST-PROCEDURE MANAGEMENT:
   - BP control: Target < 140/90 to reduce reperfusion hemorrhage
   - Avoid anticoagulation for 24 hours
   - Repeat imaging at 24 hours (CT to assess hemorrhage)
   - Early mobilization if no hemorrhage
        """,
        key_factors=[
            "CTA/MRA confirms large vessel occlusion (ICA, M1, proximal M2)",
            "NIHSS ≥ 6 or cortical syndrome present",
            "Time from LKW < 6 hours (or < 24 hours with favorable imaging)",
            "ASPECTS ≥ 6 on non-contrast CT",
            "Pre-stroke functional independence (mRS ≤ 1)",
            "Thrombectomy-capable center available",
            "No contraindication to anesthesia or contrast"
        ],
        primary_authority=[
            "AHA/ASA 2019 Stroke Guidelines (Class I recommendation)",
            "MR CLEAN trial (NEJM 2015): First positive trial",
            "DAWN trial (NEJM 2018): Extended window 6-24 hours",
            "DEFUSE 3 trial (NEJM 2018): Extended window with perfusion imaging",
            "Nogueira et al. 2018: Thrombectomy meta-analysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AHA/ASA Class I recommendation for thrombectomy within 6 hours for LVO"
    ),

    # === SEIZURES AND EPILEPSY ===
    DoctrineBlock(
        topic="ILAE 2017 Seizure Classification",
        keywords=["seizure", "ilae", "focal", "generalized", "classification", "semiology"],
        conclusion_template="ILAE 2017 classifies seizures by onset (focal, generalized, unknown), awareness (aware, impaired awareness), and motor vs. non-motor features. Focal seizures originate in one hemisphere; generalized seizures involve bilateral networks from onset. Classification guides treatment selection and prognosis.",
        reasoning_framework="""
1. SEIZURE ONSET CLASSIFICATION (Primary Division):
   - FOCAL ONSET: Seizure originates in one hemisphere
     * May remain focal or evolve to bilateral tonic-clonic
     * EEG: Focal epileptiform discharges
     * Imaging: May show structural lesion in one hemisphere
   - GENERALIZED ONSET: Seizure involves bilateral networks from onset
     * EEG: Generalized spike-wave or polyspike-wave
     * No focal features in history or imaging
   - UNKNOWN ONSET: Insufficient information to classify
     * Treat empirically based on semiology
     * Reclassify when more data available (EEG, witness account)

2. FOCAL SEIZURE SUBTYPES (Based on Features):
   A. AWARENESS STATUS:
      - Focal aware (formerly simple partial): Consciousness preserved
      - Focal impaired awareness (formerly complex partial): Consciousness altered

   B. MOTOR vs. NON-MOTOR:
      - Motor focal seizures:
        * Automatisms (lip smacking, hand fumbling)
        * Atonic (focal limb drop)
        * Clonic (rhythmic jerking)
        * Epileptic spasms (focal)
        * Hyperkinetic (thrashing, pedaling)
        * Myoclonic (brief jerks)
        * Tonic (sustained posturing)

      - Non-motor focal seizures:
        * Autonomic (tachycardia, piloerection, sweating)
        * Behavior arrest (freezing, staring)
        * Cognitive (déjà vu, forced thinking)
        * Emotional (fear, pleasure, laughter)
        * Sensory (visual, auditory, olfactory, gustatory, somatosensory)

   C. FOCAL TO BILATERAL TONIC-CLONIC:
      - Seizure starts focally, then generalizes
      - Formerly called "secondary generalization"
      - Prognosis and treatment differ from primary generalized

3. GENERALIZED SEIZURE SUBTYPES:
   - MOTOR:
     * Tonic-clonic (grand mal): Tonic stiffening followed by clonic jerking
     * Absence (petit mal): Brief staring spell, 3 Hz spike-wave on EEG
     * Myoclonic: Brief shock-like jerks
     * Atonic: Drop attacks, loss of muscle tone
     * Tonic: Sustained stiffening
     * Clonic: Rhythmic jerking without tonic phase
     * Epileptic spasms (generalized)

   - NON-MOTOR (ABSENCE):
     * Typical absence: 3 Hz spike-wave, abrupt onset/offset
     * Atypical absence: < 3 Hz spike-wave, gradual onset/offset
     * Myoclonic absence: Absence with rhythmic myoclonic jerks
     * Eyelid myoclonia: Brief eyelid jerks with absence

4. UNKNOWN ONSET SEIZURES:
   - Reclassify when EEG or witness description available
   - Treat based on most likely category:
     * Tonic-clonic of unknown onset → Broad-spectrum AED
     * Behavior arrest → Likely focal impaired awareness

5. CLINICAL APPLICATION:
   - History: Detailed seizure description from witness
   - EEG: Interictal epileptiform discharges guide classification
   - MRI: Structural lesion suggests focal onset
   - Treatment selection: Focal vs. generalized determines AED choice
   - Prognosis: Focal structural epilepsy has different trajectory than genetic generalized epilepsy
        """,
        key_factors=[
            "Onset: focal (one hemisphere) vs. generalized (bilateral) vs. unknown",
            "Awareness: preserved (aware) vs. impaired during focal seizures",
            "Motor features: automatisms, tonic, clonic, myoclonic, atonic, epileptic spasms",
            "Non-motor features: cognitive, emotional, sensory, autonomic, behavior arrest",
            "EEG findings: focal spikes vs. generalized spike-wave",
            "Imaging: structural lesion suggests focal onset",
            "Focal to bilateral tonic-clonic: starts focal, then generalizes"
        ],
        primary_authority=[
            "Fisher et al. 2017 ILAE Seizure Classification (Epilepsia)",
            "Scheffer et al. 2017 ILAE Epilepsy Classification (Epilepsia)",
            "ILAE 2017 Operational Classification of Seizure Types"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ILAE 2017 replaces 1981 classification as international standard"
    ),

    DoctrineBlock(
        topic="First-Line AED Selection Algorithm",
        keywords=["aed", "antiepileptic", "anticonvulsant", "focal", "generalized", "monotherapy"],
        conclusion_template="AED selection depends on seizure type, epilepsy syndrome, patient factors, and side effect profile. Focal epilepsy: levetiracetam, lamotrigine, or carbamazepine. Generalized epilepsy: valproate (avoid in women of childbearing potential), levetiracetam, or lamotrigine. Start low, titrate slow. Monotherapy preferred.",
        reasoning_framework="""
1. FOCAL EPILEPSY (First-Line Options):
   A. LEVETIRACETAM (Keppra):
      - Dosing: Start 500 mg BID, target 1000-1500 mg BID
      - Pros: No drug interactions, no lab monitoring, rapid titration, renal clearance
      - Cons: Psychiatric side effects (irritability, depression, aggression) in 10-15%
      - Use when: Quick seizure control needed, polypharmacy concerns, no psych history

   B. LAMOTRIGINE (Lamictal):
      - Dosing: Start 25 mg daily, escalate slowly over 6-8 weeks to 200-400 mg daily
      - Pros: Well-tolerated, mood stabilization, low side effect burden
      - Cons: Slow titration, Stevens-Johnson syndrome risk (0.3%, higher if rapid titration or with valproate)
      - Use when: Mood disorder comorbidity, long-term tolerability priority

   C. CARBAMAZEPINE (Tegretol):
      - Dosing: Start 200 mg BID, target 600-1200 mg/day divided
      - Pros: Long track record, generic available
      - Cons: Drug interactions (CYP3A4 inducer), hyponatremia, aplastic anemia (rare), requires lab monitoring
      - Use when: Cost priority, no drug interaction concerns, HLA-B*1502 negative (Asians at SJS risk)

   D. OXCARBAZEPINE (Trileptal):
      - Similar to carbamazepine but fewer drug interactions
      - Hyponatremia more common (25% vs. 10%)

2. GENERALIZED EPILEPSY (First-Line Options):
   A. VALPROATE (Depakote) - MOST EFFECTIVE:
      - Dosing: Start 250 mg BID, target 750-2000 mg/day divided, level 50-100 mcg/mL
      - Pros: Broad spectrum (all generalized seizure types), mood stabilization
      - Cons: Teratogenicity (neural tube defects, cognitive impairment in 30-40% exposed fetuses), weight gain, hair loss, tremor, thrombocytopenia, hepatotoxicity, PCOS in women
      - AVOID in women of childbearing potential unless no alternatives
      - Requires labs: CBC, LFTs, ammonia, valproate level

   B. LEVETIRACETAM:
      - Effective for myoclonic and tonic-clonic seizures
      - Less effective for absence seizures than valproate
      - First choice in women of childbearing potential

   C. LAMOTRIGINE:
      - Effective for absence and tonic-clonic
      - Less effective for myoclonic seizures (may worsen juvenile myoclonic epilepsy)
      - Good choice for women, mood comorbidity

   D. ETHOSUXIMIDE:
      - Absence seizures only (not for tonic-clonic)
      - Dosing: Start 250 mg daily, target 750-1500 mg/day

3. BROAD-SPECTRUM AEDs (Focal AND Generalized):
   - Levetiracetam
   - Lamotrigine
   - Valproate
   - Topiramate (side effects limit use: cognitive slowing, weight loss, kidney stones)
   - Zonisamide (similar to topiramate)

4. AEDs TO AVOID IN SPECIFIC SCENARIOS:
   - Carbamazepine, oxcarbazepine, phenytoin in generalized epilepsy: May worsen absence and myoclonic seizures
   - Lamotrigine in juvenile myoclonic epilepsy: May worsen myoclonic jerks
   - Valproate in women of childbearing potential: Teratogenicity
   - Gabapentin, vigabatrin in absence seizures: Ineffective or worsen

5. PATIENT-SPECIFIC FACTORS:
   - Women of childbearing potential: Avoid valproate, prefer levetiracetam or lamotrigine
   - Elderly: Start low doses, avoid polypharmacy, consider levetiracetam (renal dosing)
   - Renal impairment: Dose-adjust levetiracetam, gabapentin, topiramate
   - Hepatic impairment: Avoid valproate, reduce carbamazepine
   - Drug interactions: Avoid enzyme inducers (carbamazepine, phenytoin) if on OCPs, warfarin, etc.
   - Psychiatric comorbidity: Lamotrigine for mood, avoid levetiracetam if aggression history
   - Cost: Generics (carbamazepine, phenytoin, valproate) vs. newer agents

6. MONOTHERAPY PRINCIPLE:
   - Start with one AED, titrate to maximum tolerated dose before adding second
   - Monotherapy controls 60-70% of epilepsy patients
   - Polypharmacy increases side effects and drug interactions
   - Add second AED only if monotherapy fails at therapeutic doses

7. TITRATION STRATEGY:
   - Start low, go slow to minimize side effects
   - Lamotrigine: 6-8 weeks to target (slow to avoid SJS)
   - Levetiracetam: 1-2 weeks (rapid titration tolerated)
   - Carbamazepine: 2-4 weeks
   - Valproate: 1-2 weeks
   - Adjust based on seizure control and side effects
        """,
        key_factors=[
            "Seizure type: focal vs. generalized determines AED efficacy",
            "Women of childbearing potential: avoid valproate (teratogenic)",
            "Psychiatric comorbidity: lamotrigine stabilizes mood, levetiracetam may worsen aggression",
            "Drug interactions: enzyme inducers (carbamazepine, phenytoin) reduce OCP efficacy",
            "Tolerability: levetiracetam and lamotrigine better tolerated than older AEDs",
            "Monotherapy preferred: 60-70% controlled on single AED",
            "Cost: generics (carbamazepine, valproate) vs. branded newer agents"
        ],
        primary_authority=[
            "AAN/AES 2018 Guidelines for Treatment of Epilepsy",
            "Glauser et al. 2013 ILAE Treatment Guidelines",
            "Marson et al. SANAD trials (Lancet 2007): Valproate best for generalized, carbamazepine/lamotrigine for focal",
            "FDA prescribing information for each AED"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Monotherapy with AED matched to seizure type is standard of care"
    ),

    # === NEURODEGENERATIVE DISEASES ===
    DoctrineBlock(
        topic="Parkinson Disease Diagnosis and Staging",
        keywords=["parkinson", "bradykinesia", "tremor", "rigidity", "hoehn yahr", "updrs"],
        conclusion_template="Parkinson disease is a clinical diagnosis based on bradykinesia plus rest tremor or rigidity. Exclude secondary parkinsonism and atypical parkinsonian syndromes. Hoehn-Yahr stages disease severity (1-5). UPDRS scores motor impairment. Levodopa is gold standard treatment. Consider DaTscan if diagnosis uncertain.",
        reasoning_framework="""
1. DIAGNOSTIC CRITERIA (UK Brain Bank Criteria):
   A. BRADYKINESIA (Required - Must be present):
      - Slowness of voluntary movement
      - Decrement in amplitude or speed with repetitive actions
      - Test: Finger tapping, hand opening/closing, foot tapping

   B. PLUS at least ONE of:
      - Rest tremor (4-6 Hz, pill-rolling, diminishes with action)
      - Rigidity (cogwheel or lead-pipe, test passive movement)
      - Postural instability (pull test: > 2 steps backward or falls)

   C. SUPPORTIVE FEATURES (Increase confidence):
      - Asymmetric onset (90% of PD starts unilateral)
      - Progressive course
      - Excellent response to levodopa (> 70% improvement)
      - Levodopa-induced dyskinesias after years of treatment
      - Clinical course > 10 years

2. EXCLUSION CRITERIA (Rule out secondary parkinsonism):
   - Drug-induced: Metoclopramide, prochlorperazine, haloperidol, risperidone (D2 blockers)
   - Vascular parkinsonism: Stepwise progression, lower body predominant, gait apraxia, white matter disease on MRI
   - Normal pressure hydrocephalus: Triad of gait, dementia, incontinence; ventriculomegaly on CT/MRI
   - Multiple system atrophy (MSA): Autonomic failure (orthostatic hypotension, urinary dysfunction), cerebellar signs, poor levodopa response
   - Progressive supranuclear palsy (PSP): Vertical gaze palsy, axial rigidity, early falls, poor levodopa response
   - Corticobasal degeneration: Asymmetric apraxia, alien limb, cortical sensory loss
   - Dementia with Lewy bodies: Dementia before or within 1 year of motor symptoms, visual hallucinations, fluctuations
   - Wilson disease (age < 40): Kayser-Fleischer rings, low ceruloplasmin, elevated urinary copper

3. HOEHN-YAHR STAGING (Disease Severity):
   - Stage 1: Unilateral involvement, minimal functional impairment
   - Stage 2: Bilateral involvement, no postural instability, independent
   - Stage 3: Bilateral involvement, mild postural instability, independent in ADLs
   - Stage 4: Severe disability, still able to walk or stand unassisted
   - Stage 5: Wheelchair-bound or bedridden unless aided

4. UPDRS (Unified Parkinson Disease Rating Scale):
   - Part I: Mentation, behavior, mood (16 points)
   - Part II: Activities of daily living (52 points)
   - Part III: Motor examination (108 points) - most commonly used
   - Part IV: Complications of therapy (23 points)
   - Total: 199 points (higher = more severe)
   - Used to track progression and treatment response

5. IMAGING (When to Order):
   - Brain MRI: Rule out vascular parkinsonism, NPH, tumor, MSA (hot cross bun sign)
   - DaTscan (Ioflupane I-123 SPECT): Differentiates PD from essential tremor, drug-induced, psychogenic
     * Abnormal in PD: Reduced striatal dopamine transporter uptake
     * Normal in essential tremor, drug-induced, psychogenic
     * Also abnormal in MSA, PSP, CBD (cannot differentiate from PD)
   - NOT needed for typical PD: Classic presentation + levodopa response = clinical diagnosis

6. TREATMENT INITIATION:
   - Levodopa/carbidopa (Sinemet): Gold standard, most effective
     * Start 25/100 mg TID, titrate to effect
     * Motor complications (dyskinesias, wearing off) after 5-10 years in 50%
     * Delayed start in young patients (< 60) to postpone dyskinesias

   - Dopamine agonists (pramipexole, ropinirole): Alternative first-line in young patients
     * Less effective than levodopa but lower dyskinesia risk
     * Higher impulse control disorder risk (gambling, hypersexuality)

   - MAO-B inhibitors (rasagiline, selegiline): Mild benefit, may delay levodopa need

   - COMT inhibitors (entacapone): Add to levodopa to reduce wearing off

   - Amantadine: Mild anti-parkinsonian effect, reduces dyskinesias

   - Deep brain stimulation (DBS): For advanced PD with motor fluctuations despite optimal medical therapy

7. PROGNOSIS:
   - Average progression: Hoehn-Yahr increases by 0.5 stage per year
   - Life expectancy: Near-normal if diagnosed young, reduced if older or dementia present
   - Dementia develops in 30-40% after 10-20 years
   - Falls and aspiration are leading causes of morbidity
        """,
        key_factors=[
            "Bradykinesia is required for diagnosis",
            "Plus rest tremor, rigidity, or postural instability",
            "Asymmetric onset and progressive course support diagnosis",
            "Excellent levodopa response (> 70%) confirms diagnosis",
            "Exclude drug-induced, vascular, and atypical parkinsonism",
            "DaTscan if uncertain (abnormal in PD, normal in essential tremor)",
            "Hoehn-Yahr stages severity (1 = unilateral, 5 = bedridden)"
        ],
        primary_authority=[
            "UK Parkinson Disease Society Brain Bank Criteria",
            "Movement Disorder Society (MDS) Clinical Diagnostic Criteria 2015",
            "AAN Practice Parameter: Diagnosis and Prognosis of PD (Neurology 2006)",
            "Hoehn and Yahr 1967 original staging"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Clinical diagnosis based on bradykinesia plus tremor/rigidity; levodopa response confirms"
    ),

    DoctrineBlock(
        topic="Alzheimer Disease Diagnosis and Cognitive Assessment",
        keywords=["alzheimer", "dementia", "mmse", "moca", "amyloid", "biomarker", "cognitive"],
        conclusion_template="Alzheimer disease is diagnosed clinically by progressive cognitive decline (memory plus other domain) impairing function, excluding other causes. MMSE and MoCA screen for cognitive impairment. MRI rules out structural causes. Biomarkers (amyloid PET, CSF) support diagnosis but not required for clinical diagnosis. Cholinesterase inhibitors provide modest benefit.",
        reasoning_framework="""
1. CLINICAL DIAGNOSTIC CRITERIA (NIA-AA 2011):
   A. PROBABLE ALZHEIMER DEMENTIA:
      - Insidious onset (months to years)
      - Progressive worsening of cognition
      - Initial and prominent memory impairment (episodic memory)
      - Plus impairment in at least one other cognitive domain:
        * Executive function (planning, judgment, problem-solving)
        * Language (word-finding, naming)
        * Visuospatial (getting lost, difficulty with complex visual tasks)
        * Personality/behavior changes
      - Impairment in activities of daily living (ADLs)
      - No evidence of other neurological or psychiatric cause

   B. EXCLUSION CRITERIA (Rule out other dementias):
      - Vascular dementia: Stepwise decline, focal neuro signs, strokes on MRI
      - Lewy body dementia: Visual hallucinations, parkinsonism, fluctuations within days
      - Frontotemporal dementia: Early personality/behavior changes, language variant
      - Normal pressure hydrocephalus: Gait, urinary incontinence, ventriculomegaly
      - Reversible causes: B12 deficiency, hypothyroidism, depression, medications

2. COGNITIVE SCREENING TOOLS:
   A. MINI-MENTAL STATE EXAMINATION (MMSE):
      - 30-point scale: Orientation (10), registration (3), attention (5), recall (3), language (8), visuospatial (1)
      - Normal: 24-30
      - Mild dementia: 18-23
      - Moderate: 10-17
      - Severe: < 10
      - Adjust for education: Add 1 point if < 9 years education
      - Limitations: Ceiling effect in mild cognitive impairment, insensitive to executive dysfunction

   B. MONTREAL COGNITIVE ASSESSMENT (MoCA):
      - 30-point scale: More sensitive than MMSE for mild cognitive impairment
      - Domains: Visuospatial/executive (5), naming (3), memory (5), attention (6), language (3), abstraction (2), orientation (6)
      - Normal: ≥ 26
      - MCI: 18-25
      - Dementia: < 18
      - Add 1 point if ≤ 12 years education
      - Preferred over MMSE in clinical practice due to higher sensitivity

   C. CLOCK DRAWING TEST:
      - Ask patient to draw clock face, set time to 10 past 11
      - Screens for visuospatial and executive dysfunction
      - Abnormal if numbers missing, crowded, or time wrong

3. MILD COGNITIVE IMPAIRMENT (MCI) - Pre-Dementia Stage:
   - Cognitive decline beyond normal aging but not dementia
   - Preserved ADLs (key difference from dementia)
   - Amnestic MCI: Memory impairment, higher risk of progression to AD (10-15% per year)
   - Non-amnestic MCI: Other domains affected, may progress to FTD or Lewy body
   - Follow longitudinally, repeat cognitive testing every 6-12 months

4. LABORATORY AND IMAGING WORKUP:
   A. LABS (Rule out reversible causes):
      - TSH: Hypothyroidism
      - B12: Deficiency causes cognitive impairment
      - CBC: Anemia, infection
      - CMP: Electrolytes, renal, hepatic function
      - RPR: Neurosyphilis (rare but reversible)
      - Consider: HIV, Lyme, heavy metals if risk factors

   B. BRAIN MRI (Preferred) or CT:
      - Medial temporal lobe atrophy (hippocampus) supports AD
      - Rule out: Stroke, tumor, subdural hematoma, NPH (ventriculomegaly)
      - White matter hyperintensities: Vascular contribution
      - PET is NOT standard workup (expensive, not covered by Medicare except research)

5. BIOMARKERS (Support diagnosis, not required):
   - Amyloid PET (Florbetapir, Flutemetamol): Detects amyloid plaques
     * Positive: Supports AD but can be positive in normal elderly
     * Negative: Rules out AD, consider alternative diagnosis
     * Not routinely covered by insurance

   - CSF Analysis:
     * Low Aβ42 (amyloid): Deposition in plaques
     * High tau and phospho-tau: Neuronal injury
     * Used in research, atypical cases, or young-onset dementia

   - Apolipoprotein E (APOE) genotype:
     * APOE ε4 allele: Increases AD risk (dose-dependent)
     * NOT diagnostic, NOT recommended for clinical use (ethical issues)

6. TREATMENT (Modest symptomatic benefit):
   A. CHOLINESTERASE INHIBITORS (Mild to moderate AD):
      - Donepezil (Aricept): Start 5 mg daily, increase to 10 mg after 4-6 weeks
      - Rivastigmine (Exelon): Patch or oral
      - Galantamine (Razadyne): BID dosing
      - Benefit: 2-3 point MMSE improvement, delay nursing home by 6-12 months
      - Side effects: Nausea, diarrhea, bradycardia, weight loss

   B. NMDA ANTAGONIST (Moderate to severe AD):
      - Memantine (Namenda): Start 5 mg daily, titrate to 10 mg BID
      - Can combine with cholinesterase inhibitor
      - Modest benefit, well-tolerated

   C. NEW AGENTS (2023-2024):
      - Lecanemab (Leqembi): Monoclonal antibody, removes amyloid plaques
        * Slows decline by 27% over 18 months
        * Infusion reactions, ARIA (brain swelling/microhemorrhages) risk
        * Requires amyloid PET confirmation
        * Medicare coverage limited to clinical trial participation
      - Aducanumab (Aduhelm): Controversial approval, limited use due to cost and ARIA risk

7. NON-PHARMACOLOGIC MANAGEMENT:
   - Caregiver education and support groups
   - Cognitive stimulation therapy
   - Exercise (30 min daily, aerobic and resistance)
   - Social engagement
   - Address sleep, depression, anxiety (common comorbidities)
   - Safety: Driving assessment, home safety evaluation, advance directives
        """,
        key_factors=[
            "Progressive memory impairment plus other cognitive domain",
            "Impairment in ADLs distinguishes dementia from MCI",
            "MoCA more sensitive than MMSE for mild cognitive impairment",
            "MRI rules out vascular, structural, and reversible causes",
            "Labs: TSH, B12, CBC, CMP to exclude reversible causes",
            "Cholinesterase inhibitors (donepezil) provide modest benefit",
            "Biomarkers (amyloid PET, CSF) support diagnosis but not required"
        ],
        primary_authority=[
            "NIA-AA 2011 Diagnostic Guidelines for Alzheimer Disease",
            "AAN Practice Parameter: Dementia Evaluation (Neurology 2001)",
            "Folstein et al. 1975 MMSE original publication",
            "Nasreddine et al. 2005 MoCA development and validation",
            "FDA approvals for lecanemab (2023) and memantine/cholinesterase inhibitors"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Clinical diagnosis based on progressive cognitive decline; biomarkers support but not required"
    ),

    DoctrineBlock(
        topic="Multiple Sclerosis McDonald Criteria and DMT Selection",
        keywords=["multiple sclerosis", "mcdonald", "mri", "oligoclonal bands", "dmt", "relapse"],
        conclusion_template="Multiple sclerosis is diagnosed by McDonald 2017 criteria: dissemination in space (2+ CNS areas) and time (2+ episodes or MRI progression), excluding alternative diagnoses. MRI shows T2 lesions in periventricular, juxtacortical, infratentorial, spinal cord. CSF oligoclonal bands support diagnosis. Disease-modifying therapies (DMTs) reduce relapse rate and MRI activity.",
        reasoning_framework="""
1. MCDONALD 2017 DIAGNOSTIC CRITERIA:
   A. DISSEMINATION IN SPACE (DIS) - Need 2+ of 4 CNS areas:
      - Periventricular: ≥ 1 T2 lesion adjacent to lateral ventricles
      - Juxtacortical: ≥ 1 T2 lesion touching cortex (U-fibers)
      - Infratentorial: ≥ 1 T2 lesion in brainstem or cerebellum
      - Spinal cord: ≥ 1 T2 lesion (non-enhancing, > 3 mm)

   B. DISSEMINATION IN TIME (DIT) - Evidence of lesions at different times:
      - Simultaneous enhancing (Gd+) and non-enhancing lesions on one MRI, OR
      - New T2 or Gd+ lesion on follow-up MRI (any time), OR
      - CSF-specific oligoclonal bands (can substitute for DIT if DIS met)

   C. EXCLUSION OF ALTERNATIVE DIAGNOSES:
      - Neuromyelitis optica (NMO): Aquaporin-4 antibody, longitudinally extensive cord lesions (> 3 vertebral segments)
      - ADEM: Monophasic, post-infectious, multifocal lesions with encephalopathy
      - Sarcoidosis: Systemic symptoms, chest imaging, ACE level, biopsy
      - Vasculitis: Systemic symptoms, labs, angiography
      - Lyme disease: Endemic area, erythema migrans, Lyme antibodies
      - Migraine: White matter lesions but no cord or infratentorial lesions

2. MRI LESION CHARACTERISTICS (Suggestive of MS):
   - Shape: Ovoid, perpendicular to ventricles (Dawson fingers)
   - Location: Periventricular > juxtacortical > infratentorial > spinal cord
   - Size: 3 mm or larger (smaller lesions less specific)
   - Enhancement: Gd+ indicates active inflammation (open blood-brain barrier)
   - Black holes: T1 hypointense lesions (axonal loss, chronic damage)
   - Spinal cord: Short segment (< 3 vertebral levels), peripheral, asymmetric

3. CSF ANALYSIS (Supportive but not required):
   - Oligoclonal bands (OCBs): Present in CSF but not serum in 85-95% of MS
     * Supports diagnosis, can substitute for DIT
     * Not specific (also in other inflammatory conditions)
   - Elevated IgG index: Increased intrathecal IgG synthesis
   - Mild lymphocytic pleocytosis: < 50 WBCs (higher suggests infection)
   - Protein: Normal or mildly elevated (< 100 mg/dL)

4. CLINICAL PRESENTATION PATTERNS:
   - Relapsing-remitting MS (RRMS): 85% at onset
     * Discrete attacks (relapses) followed by recovery
     * No progression between attacks
     * Most common presenting symptoms: Optic neuritis, transverse myelitis, brainstem syndrome

   - Secondary progressive MS (SPMS): 50% of RRMS converts after 10-15 years
     * Progressive disability accumulation independent of relapses
     * May have superimposed relapses

   - Primary progressive MS (PPMS): 15% at onset
     * Progressive from onset without discrete relapses
     * Older age at onset (40s), more spinal cord involvement

   - Clinically isolated syndrome (CIS): Single episode, may or may not progress to MS
     * MRI lesions predict conversion to MS (60% if ≥ 9 T2 lesions)

5. DISEASE-MODIFYING THERAPY (DMT) SELECTION:
   A. FIRST-LINE AGENTS (Moderate efficacy, better safety):
      - Interferons (IFN-β1a, IFN-β1b): Injectable, 30% relapse reduction
        * Side effects: Flu-like symptoms, injection site reactions, depression

      - Glatiramer acetate (Copaxone): Injectable, 30% relapse reduction
        * Side effects: Injection site reactions, lipoatrophy, chest tightness

      - Teriflunomide (Aubagio): Oral, 30% relapse reduction
        * Side effects: Diarrhea, hair thinning, hepatotoxicity, teratogenic

      - Dimethyl fumarate (Tecfidera): Oral, 40-50% relapse reduction
        * Side effects: Flushing, GI upset, lymphopenia (PML risk if severe)

   B. SECOND-LINE AGENTS (High efficacy, higher risk):
      - Fingolimod (Gilenya): Oral, 50-60% relapse reduction
        * Side effects: Bradycardia (first dose), macular edema, PML, infections
        * First-dose monitoring required (6 hours cardiac telemetry)

      - Natalizumab (Tysabri): IV monthly, 68% relapse reduction
        * Side effects: PML (progressive multifocal leukoencephalopathy) risk if JC virus positive
        * Requires JC virus antibody testing every 3-6 months
        * Most effective single agent

      - Ocrelizumab (Ocrevus): IV every 6 months, 47% relapse reduction
        * Only FDA-approved for PPMS (slows progression)
        * Also approved for RRMS
        * Side effects: Infusion reactions, infections, possible cancer risk

      - Alemtuzumab (Lemtrada): IV yearly for 2 years, 50-70% relapse reduction
        * Side effects: Autoimmune thyroid disease (30%), ITP, nephropathy
        * Requires monthly monitoring for 4 years post-treatment

   C. HIGHLY ACTIVE MS (Aggressive from onset or breakthrough on DMT):
      - Start with high-efficacy agents: Natalizumab, ocrelizumab, alemtuzumab
      - Criteria: ≥ 2 relapses in 1 year with disability, or ≥ 9 T2 lesions, or ≥ 1 Gd+ lesion

6. RELAPSE MANAGEMENT:
   - Methylprednisolone: 1 gram IV daily for 3-5 days
     * Speeds recovery, does not affect long-term outcome
     * Side effects: Insomnia, mood changes, hyperglycemia, GI upset
   - Plasma exchange (PLEX): For severe relapses not responding to steroids

7. PROGNOSIS:
   - RRMS: Variable, 50% require walking aid after 15 years if untreated
   - DMTs reduce relapse rate by 30-70% and slow MRI progression
   - Good prognosis: Female, young age, sensory symptoms, complete recovery from relapses
   - Poor prognosis: Male, older age, motor symptoms, incomplete recovery, high MRI lesion burden
        """,
        key_factors=[
            "McDonald 2017: Dissemination in space (2+ CNS areas) and time (2+ events or MRI progression)",
            "MRI T2 lesions: periventricular, juxtacortical, infratentorial, spinal cord",
            "CSF oligoclonal bands support diagnosis (85-95% sensitive)",
            "Exclude NMO, ADEM, sarcoidosis, vasculitis, Lyme",
            "DMTs reduce relapse rate: first-line (30-50%), second-line (50-70%)",
            "Natalizumab most effective but PML risk if JC virus positive",
            "Ocrelizumab only DMT approved for primary progressive MS"
        ],
        primary_authority=[
            "Thompson et al. 2018 McDonald 2017 Criteria Revision",
            "AAN Practice Guideline: DMTs for MS (Neurology 2018)",
            "FDA approvals for ocrelizumab (2017), alemtuzumab, natalizumab",
            "DEFINE, CONFIRM trials (dimethyl fumarate efficacy)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="McDonald 2017 criteria are international standard for MS diagnosis"
    ),

    # === TRAUMATIC BRAIN INJURY ===
    DoctrineBlock(
        topic="Glasgow Coma Scale and TBI Severity Classification",
        keywords=["glasgow", "gcs", "traumatic brain injury", "tbi", "mild", "moderate", "severe"],
        conclusion_template="Glasgow Coma Scale (GCS) scores consciousness level (3-15) based on eye opening, verbal response, and motor response. TBI severity: mild (GCS 13-15), moderate (GCS 9-12), severe (GCS 3-8). GCS guides imaging, ICU admission, and prognosis. CT head indicated for GCS < 15 or high-risk features.",
        reasoning_framework="""
1. GLASGOW COMA SCALE (GCS) SCORING:
   A. EYE OPENING (1-4 points):
      - 4: Spontaneous - eyes open without stimulation
      - 3: To voice - opens eyes to verbal command
      - 2: To pain - opens eyes only to painful stimulus
      - 1: None - no eye opening even to pain

   B. VERBAL RESPONSE (1-5 points):
      - 5: Oriented - knows name, place, date
      - 4: Confused - disoriented but converses
      - 3: Inappropriate words - intelligible but non-conversational
      - 2: Incomprehensible sounds - moans, groans, no words
      - 1: None - no verbal output
      - T: Intubated - mark as 1T and use motor + eye only for total

   C. MOTOR RESPONSE (1-6 points):
      - 6: Obeys commands - follows simple instructions
      - 5: Localizes to pain - purposeful movement toward painful stimulus
      - 4: Withdraws from pain - flexion, but not localizing
      - 3: Abnormal flexion (decorticate) - arms flex, legs extend
      - 2: Abnormal extension (decerebrate) - arms and legs extend
      - 1: None - no motor response to pain

   TOTAL GCS: Eye + Verbal + Motor = 3 to 15 points

2. TBI SEVERITY CLASSIFICATION (Based on GCS):
   - MILD TBI (Concussion): GCS 13-15
     * Most common (80% of TBI)
     * May have brief loss of consciousness (< 30 minutes) or none
     * Post-concussive symptoms: Headache, dizziness, confusion, amnesia
     * CT head often normal, but obtain if high-risk features present

   - MODERATE TBI: GCS 9-12
     * Loss of consciousness 30 minutes to 24 hours
     * Post-traumatic amnesia > 24 hours
     * CT head almost always abnormal (contusion, hemorrhage, edema)
     * Admit to ICU for monitoring

   - SEVERE TBI: GCS 3-8
     * Coma, unresponsive
     * CT head shows significant injury (diffuse axonal injury, mass lesion)
     * Intubate for airway protection if GCS ≤ 8
     * ICU admission, ICP monitoring if GCS < 9

3. CT HEAD INDICATIONS IN MILD TBI (Canadian CT Head Rule):
   HIGH-RISK (CT mandatory):
   - GCS < 15 at 2 hours post-injury
   - Suspected skull fracture (palpable, basal skull fracture signs)
   - Vomiting ≥ 2 episodes
   - Age ≥ 65 years
   - Amnesia > 30 minutes before impact (retrograde)
   - Dangerous mechanism: Fall > 3 feet or 5 stairs, MVA with ejection, pedestrian struck

   MEDIUM-RISK (CT recommended):
   - Amnesia > 30 minutes (any)
   - Dangerous mechanism

   LOW-RISK (Observation acceptable):
   - GCS 15, no LOC, no amnesia, minor mechanism
   - Discharge with head injury instructions, return if deterioration

4. CT FINDINGS AND MANAGEMENT:
   - Epidural hematoma: Lens-shaped, arterial (middle meningeal), "lucid interval" then deterioration
     * Surgical evacuation if > 30 mL, midline shift, or GCS decline

   - Subdural hematoma: Crescent-shaped, venous, crosses suture lines
     * Acute: Bright on CT, evacuate if > 10 mm, midline shift > 5 mm, or GCS decline
     * Chronic: Dark on CT, common in elderly, anticoagulated

   - Subarachnoid hemorrhage (traumatic): Blood in sulci, cisterns
     * Monitor for vasospasm (days 3-14), hydrocephalus

   - Intraparenchymal contusion: Frontal and temporal poles common (coup-contrecoup)
     * Monitor for expansion, edema, mass effect

   - Diffuse axonal injury: Normal CT or small hemorrhages at gray-white junction, corpus callosum
     * MRI more sensitive (GRE sequence shows microhemorrhages)
     * Poor prognosis if severe

5. INTRACRANIAL PRESSURE (ICP) MONITORING:
   - Indications: Severe TBI (GCS 3-8) with abnormal CT
   - Goal: ICP < 20 mmHg, CPP (cerebral perfusion pressure) 60-70 mmHg
   - Interventions:
     * Head of bed 30 degrees
     * Sedation, analgesia
     * Osmotic therapy: Mannitol 0.25-1 g/kg or hypertonic saline 3-23.4%
     * Hyperventilation to PaCO2 30-35 mmHg (temporary, avoid prolonged)
     * Decompressive craniectomy if refractory elevated ICP

6. PROGNOSIS (Glasgow Outcome Scale - GOS):
   - 1: Death
   - 2: Persistent vegetative state
   - 3: Severe disability (conscious, dependent)
   - 4: Moderate disability (independent, disabled)
   - 5: Good recovery (minor deficits)

   Predictors of poor outcome:
   - Low GCS (3-5)
   - Older age (> 60)
   - Hypotension, hypoxia
   - Pupillary abnormalities (dilated, unreactive)
   - CT findings: Midline shift, compressed cisterns, diffuse injury

7. MILD TBI / CONCUSSION MANAGEMENT:
   - Rest (physical and cognitive) for 24-48 hours
   - Gradual return to activity (stepwise protocol)
   - No contact sports until asymptomatic
   - Second impact syndrome risk if return too soon (rare but catastrophic)
   - Post-concussive syndrome: Symptoms > 3 months in 10-15%
        """,
        key_factors=[
            "GCS = Eye (1-4) + Verbal (1-5) + Motor (1-6) = 3 to 15 total",
            "TBI severity: mild (13-15), moderate (9-12), severe (3-8)",
            "Intubate if GCS ≤ 8 to protect airway",
            "CT head indicated for GCS < 15, age > 65, vomiting, amnesia, dangerous mechanism",
            "Epidural hematoma: lens-shaped, lucid interval, arterial, surgical evacuation",
            "Subdural hematoma: crescent-shaped, venous, crosses sutures",
            "ICP monitoring if severe TBI (GCS 3-8) with abnormal CT"
        ],
        primary_authority=[
            "Teasdale and Jennett 1974: Original GCS publication",
            "Brain Trauma Foundation 2016 Guidelines for Severe TBI",
            "Canadian CT Head Rule (Stiell et al. JAMA 2001)",
            "AAN Practice Parameter: Concussion Management (Neurology 2013)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GCS is universal standard for consciousness assessment; GCS ≤ 8 requires intubation"
    ),

    # === NEUROIMAGING INTERPRETATION ===
    DoctrineBlock(
        topic="CT and MRI Stroke Protocol Interpretation",
        keywords=["stroke", "imaging", "dwi", "flair", "aspects", "mismatch", "perfusion"],
        conclusion_template="Non-contrast CT is first-line for acute stroke: Excludes hemorrhage, assesses early ischemic changes (ASPECTS score). CTA identifies LVO for thrombectomy. MRI DWI detects acute infarct (bright), FLAIR shows subacute infarct. DWI-FLAIR mismatch suggests stroke within 4.5 hours (wake-up stroke). CT/MRI perfusion identifies penumbra for extended window treatment.",
        reasoning_framework="""
1. NON-CONTRAST CT HEAD (First-Line Imaging):
   A. PRIMARY PURPOSE: Exclude intracranial hemorrhage (ICH)
      - ICH appears bright (hyperdense) on CT
      - Rules out tPA if hemorrhage present
      - Obtained in all suspected strokes within minutes of arrival

   B. EARLY ISCHEMIC CHANGES (Subtle findings in first 3-6 hours):
      - Loss of gray-white differentiation (insular ribbon sign)
      - Hyperdense MCA sign: Clot in vessel appears bright (direct sign of LVO)
      - Sulcal effacement: Loss of normal sulcal spaces
      - Basal ganglia obscuration
      - These changes predict larger infarct and worse outcome

   C. ASPECTS SCORE (Alberta Stroke Program Early CT Score):
      - 10-point scale to quantify early ischemic changes in MCA territory
      - Subtract 1 point for each affected region (10 regions total):
        * M1-M6: MCA cortex (6 regions)
        * Insula, caudate, lentiform, internal capsule (4 regions)
      - ASPECTS 10: Normal CT
      - ASPECTS 7-9: Mild early changes
      - ASPECTS < 6: Large infarct, thrombectomy may be futile (controversial)
      - Used to select thrombectomy candidates (ASPECTS ≥ 6 preferred)

2. CT ANGIOGRAPHY (CTA):
   - DETECTS LARGE VESSEL OCCLUSION (LVO):
     * ICA terminus, M1 MCA, M2 MCA, basilar artery
     * Absence of contrast in vessel = occlusion
   - COLLATERAL ASSESSMENT:
     * Good collaterals: Reconstitution of MCA branches distal to occlusion
     * Poor collaterals: No distal filling, predicts larger infarct
   - USED TO SELECT THROMBECTOMY CANDIDATES:
     * LVO present + ASPECTS ≥ 6 → thrombectomy eligible

3. MRI STROKE PROTOCOL:
   A. DIFFUSION-WEIGHTED IMAGING (DWI):
      - DETECTS ACUTE INFARCT within minutes
      - Bright signal (restricted diffusion) = cytotoxic edema from ischemia
      - Most sensitive sequence for acute stroke (abnormal in 90% within 3 hours)
      - Remains abnormal for 1-2 weeks

   B. APPARENT DIFFUSION COEFFICIENT (ADC):
      - Companion sequence to DWI
      - Dark signal (low ADC) confirms restricted diffusion (acute infarct)
      - Differentiates acute infarct (low ADC) from T2 shine-through (high ADC)

   C. FLAIR (Fluid-Attenuated Inversion Recovery):
      - Detects subacute and chronic infarcts
      - Bright signal develops 6-24 hours after stroke onset
      - Used to date stroke timing (DWI-FLAIR mismatch)

   D. DWI-FLAIR MISMATCH (Wake-Up Stroke Protocol):
      - DWI positive (acute infarct) + FLAIR negative (< 4.5 hours old)
      - Suggests stroke within tPA window
      - WAKE-UP trial: MRI-guided tPA for wake-up strokes if DWI-FLAIR mismatch
      - Allows treatment in patients with unknown symptom onset time

   E. GRADIENT ECHO (GRE) or SWI (Susceptibility-Weighted Imaging):
      - Detects hemorrhage, microbleeds, chronic blood products
      - Excludes hemorrhagic transformation before tPA
      - Cerebral amyloid angiopathy: Multiple cortical microbleeds

4. CT PERFUSION (CTP) or MRI PERFUSION:
   - IDENTIFIES PENUMBRA (Salvageable tissue):
     * Core infarct: Severely reduced CBF, already dead tissue
     * Penumbra: Reduced CBF but viable, can be saved if reperfused

   - PERFUSION PARAMETERS:
     * CBF (cerebral blood flow): Low in core and penumbra
     * CBV (cerebral blood volume): Low in core, normal/high in penumbra (autoregulation)
     * MTT (mean transit time): Prolonged in core and penumbra
     * Tmax (time to maximum): Delayed in penumbra (> 6 seconds)

   - MISMATCH PARADIGM (Extended window thrombectomy selection):
     * Ischemic core (CBF < 30%): Volume in mL
     * Penumbra (Tmax > 6 seconds): Volume in mL
     * Mismatch ratio: Penumbra / Core
     * DEFUSE 3 criteria: Core < 70 mL, mismatch ratio ≥ 1.8
     * DAWN criteria: Clinical-core mismatch (high NIHSS, small core)

   - USED IN 6-24 HOUR WINDOW:
     * Selects patients with large penumbra for thrombectomy
     * Only perfusion imaging candidates benefit from late thrombectomy

5. IMAGING PROTOCOL BY TIME WINDOW:
   - 0-3 HOURS (tPA window):
     * Non-contrast CT to exclude hemorrhage → Give tPA if eligible
     * CTA optional (if LVO suspected and thrombectomy available)

   - 3-6 HOURS (Thrombectomy window):
     * Non-contrast CT + CTA (detect LVO, assess ASPECTS)
     * Thrombectomy if LVO, no advanced imaging needed

   - 6-24 HOURS (Extended window):
     * Non-contrast CT + CTA + CT perfusion (or MRI with DWI/perfusion)
     * Thrombectomy if favorable mismatch (DEFUSE 3 or DAWN criteria)

   - WAKE-UP STROKE (Unknown onset):
     * MRI with DWI-FLAIR mismatch → tPA eligible if mismatch present

6. POSTERIOR CIRCULATION STROKE (Basilar Artery):
   - CT often normal in first 24 hours (small brainstem infarcts)
   - MRI DWI more sensitive for posterior fossa
   - CTA or MRA to detect basilar occlusion
   - Basilar thrombectomy: Extended window (up to 24 hours or longer)

7. HEMORRHAGIC STROKE IMAGING:
   - Intracerebral hemorrhage (ICH): Bright on CT, location guides etiology
     * Hypertensive: Basal ganglia, thalamus, pons, cerebellum
     * Amyloid angiopathy: Lobar, elderly, microbleeds on MRI
     * AVM, aneurysm, tumor, coagulopathy: Atypical locations
   - CTA "spot sign": Active contrast extravasation, predicts hematoma expansion
   - MRI gradient echo: Detects chronic microbleeds (CAA vs. hypertensive)
        """,
        key_factors=[
            "Non-contrast CT first: Excludes hemorrhage, assesses ASPECTS score",
            "CTA identifies large vessel occlusion for thrombectomy",
            "MRI DWI detects acute infarct within minutes (bright signal)",
            "DWI-FLAIR mismatch: DWI+ / FLAIR- suggests stroke < 4.5 hours (wake-up stroke)",
            "CT/MRI perfusion: Identifies penumbra (salvageable tissue) for 6-24 hour window",
            "ASPECTS ≥ 6 predicts good thrombectomy outcome",
            "Perfusion mismatch (DEFUSE 3/DAWN): Core < 70 mL, mismatch ratio ≥ 1.8"
        ],
        primary_authority=[
            "Barber et al. 2000: ASPECTS score development",
            "WAKE-UP trial (NEJM 2018): DWI-FLAIR mismatch for tPA",
            "DEFUSE 3 and DAWN trials: Perfusion imaging for extended window",
            "AHA/ASA 2019 Stroke Guidelines: Imaging recommendations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Non-contrast CT is mandatory first imaging for acute stroke; CTA + perfusion guide extended window treatment"
    ),

    # === CSF ANALYSIS ===
    DoctrineBlock(
        topic="Lumbar Puncture and CSF Interpretation",
        keywords=["lumbar puncture", "csf", "meningitis", "subarachnoid hemorrhage", "xanthochromia"],
        conclusion_template="Lumbar puncture obtains CSF for analysis when meningitis, encephalitis, or SAH suspected. Normal CSF: Clear, 0-5 WBC, protein 15-45 mg/dL, glucose > 2/3 serum. Bacterial meningitis: Elevated WBC (PMN predominant), high protein, low glucose. Viral: Lymphocytic pleocytosis, normal glucose. SAH: RBC in all tubes, xanthochromia if > 12 hours.",
        reasoning_framework="""
1. INDICATIONS FOR LUMBAR PUNCTURE:
   - Suspected meningitis or encephalitis (fever, headache, neck stiffness, altered mental status)
   - Subarachnoid hemorrhage (thunderclap headache, CT negative, obtain LP if high suspicion)
   - Guillain-Barré syndrome (elevated protein, normal WBC)
   - Multiple sclerosis (oligoclonal bands)
   - Idiopathic intracranial hypertension (elevated opening pressure)
   - Carcinomatous meningitis (malignant cells in CSF)
   - Normal pressure hydrocephalus (large volume tap as therapeutic trial)

2. CONTRAINDICATIONS:
   - Increased intracranial pressure with mass lesion (risk of herniation)
     * Obtain CT head before LP if papilledema, focal neuro signs, or immunocompromised
   - Coagulopathy (platelets < 50,000, INR > 1.5)
     * Correct before LP to reduce epidural hematoma risk
   - Infection at LP site (cellulitis, abscess)
   - Spinal epidural abscess (relative contraindication, may seed CSF)

3. NORMAL CSF VALUES:
   - Appearance: Clear, colorless (water-like)
   - Opening pressure: 10-20 cm H2O (measured in lateral decubitus position)
   - WBC: 0-5 cells/μL (all mononuclear)
   - RBC: 0 cells/μL (traumatic tap may have RBCs)
   - Protein: 15-45 mg/dL
   - Glucose: 50-80 mg/dL (or > 2/3 of serum glucose)
   - Gram stain: No organisms
   - Culture: Sterile

4. BACTERIAL MENINGITIS (Strep pneumoniae, Neisseria meningitidis, Listeria):
   - WBC: > 1,000 cells/μL (often > 10,000)
   - Differential: Neutrophil (PMN) predominant (> 80%)
   - Protein: Elevated (> 100 mg/dL, often > 200)
   - Glucose: Low (< 40 mg/dL or < 40% of serum)
   - Gram stain: Positive in 60-80% (gram-positive diplococci for Strep pneumo)
   - Culture: Positive in 70-85% if not on antibiotics
   - Treatment: Empiric antibiotics ASAP (ceftriaxone + vancomycin + ampicillin if > 50 or immunocompromised)

5. VIRAL MENINGITIS (Enterovirus, HSV-2):
   - WBC: 10-500 cells/μL (typically < 1,000)
   - Differential: Lymphocyte predominant (> 50%)
     * Early viral may be PMN-predominant, repeat LP in 6-12 hours shows lymphocytic shift
   - Protein: Normal to mildly elevated (50-100 mg/dL)
   - Glucose: Normal (> 2/3 serum)
   - Gram stain and culture: Negative
   - PCR: Enterovirus PCR, HSV PCR if encephalitis suspected
   - Treatment: Supportive (except HSV encephalitis → acyclovir)

6. TUBERCULOUS MENINGITIS (Mycobacterium tuberculosis):
   - WBC: 100-500 cells/μL
   - Differential: Lymphocyte predominant (> 50%)
   - Protein: Markedly elevated (100-500 mg/dL)
   - Glucose: Low (< 40 mg/dL)
   - AFB smear: Low sensitivity (10-20%), repeat LPs increase yield
   - Culture: Positive in 50-80% but takes 4-8 weeks
   - PCR: TB PCR faster but less sensitive than culture
   - Treatment: RIPE therapy (rifampin, isoniazid, pyrazinamide, ethambutol) for 9-12 months

7. FUNGAL MENINGITIS (Cryptococcus in HIV, Coccidioides):
   - WBC: 20-500 cells/μL
   - Differential: Lymphocyte predominant
   - Protein: Elevated (50-200 mg/dL)
   - Glucose: Low to normal
   - India ink: Positive in 50% of Cryptococcus (budding yeast with capsule)
   - Cryptococcal antigen: Highly sensitive and specific (> 95%)
   - Fungal culture: Positive in 90%
   - Treatment: Amphotericin B + flucytosine for Cryptococcus

8. SUBARACHNOID HEMORRHAGE (SAH):
   - RBC: Elevated in all tubes (tube 1, 2, 3, 4)
     * Traumatic tap: RBC decreases from tube 1 to 4
     * SAH: RBC same in all tubes (non-clearing)
   - Xanthochromia: Yellow discoloration of supernatant after centrifugation
     * Develops 2-12 hours after SAH (RBC lysis releases bilirubin)
     * Persists for 1-4 weeks
     * Highly specific for SAH if present
   - Obtain LP if thunderclap headache and CT negative (5% of SAH CT-negative)

9. GUILLAIN-BARRÉ SYNDROME (GBS):
   - WBC: Normal (< 10 cells/μL) - "albuminocytologic dissociation"
   - Protein: Markedly elevated (> 55 mg/dL, often > 100)
     * Elevated protein appears 1-2 weeks after symptom onset
   - Glucose: Normal
   - Used to support clinical diagnosis of GBS

10. CSF OPENING PRESSURE INTERPRETATION:
    - Normal: 10-20 cm H2O
    - Elevated (> 20 cm H2O):
      * Bacterial meningitis
      * Fungal meningitis
      * Carcinomatous meningitis
      * Idiopathic intracranial hypertension (> 25 cm, often > 30)
      * Venous sinus thrombosis
    - Low (< 6 cm H2O):
      * CSF leak (post-LP headache, spontaneous intracranial hypotension)
      * Dehydration

11. TRAUMATIC TAP (Blood from LP procedure):
    - RBC count decreases from tube 1 to 4
    - Calculate corrected WBC: Subtract 1 WBC per 700 RBC
    - No xanthochromia (unless SAH present and > 12 hours)
        """,
        key_factors=[
            "Normal CSF: 0-5 WBC, protein 15-45 mg/dL, glucose > 2/3 serum, clear",
            "Bacterial meningitis: PMN-predominant (> 1,000 WBC), high protein, low glucose",
            "Viral meningitis: Lymphocytic (10-500 WBC), normal glucose",
            "SAH: RBC same in all tubes (non-clearing), xanthochromia if > 12 hours",
            "TB meningitis: Lymphocytic, very high protein (> 100), low glucose",
            "GBS: Normal WBC, elevated protein (albuminocytologic dissociation)",
            "CT head before LP if papilledema, focal signs, or immunocompromised"
        ],
        primary_authority=[
            "IDSA Guidelines for Bacterial Meningitis (CID 2004)",
            "AAN Practice Parameter: LP Evaluation (Neurology 2005)",
            "Tunkel et al. 2017 Meningitis Guidelines Update",
            "CSF Reference Ranges (various textbooks and lab standards)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="LP is diagnostic gold standard for meningitis; CT before LP if increased ICP suspected"
    ),

    # === HEADACHE DISORDERS ===
    DoctrineBlock(
        topic="Migraine Diagnosis and Prophylactic Treatment",
        keywords=["migraine", "headache", "aura", "prophylaxis", "triptan", "ichd"],
        conclusion_template="Migraine is diagnosed clinically by ICHD-3 criteria: ≥ 5 attacks lasting 4-72 hours with unilateral, pulsating, moderate-severe pain, plus nausea/vomiting or photophobia/phonophobia. Aura in 25% (visual most common). Acute treatment: Triptans or NSAIDs. Prophylaxis if ≥ 4 attacks/month: Topiramate, propranolol, or CGRP inhibitors.",
        reasoning_framework="""
1. ICHD-3 DIAGNOSTIC CRITERIA (Migraine Without Aura):
   A. ≥ 5 ATTACKS fulfilling criteria B-D

   B. DURATION: 4-72 hours (untreated or unsuccessfully treated)

   C. AT LEAST TWO of the following headache characteristics:
      - Unilateral location (one side of head)
      - Pulsating quality (throbbing)
      - Moderate to severe pain intensity (interferes with daily activities)
      - Aggravation by routine physical activity (walking, climbing stairs)

   D. AT LEAST ONE of the following during headache:
      - Nausea and/or vomiting
      - Photophobia (light sensitivity) AND phonophobia (sound sensitivity)

   E. NOT better accounted for by another ICHD-3 diagnosis

2. MIGRAINE WITH AURA (25% of migraineurs):
   - AURA CHARACTERISTICS:
     * Visual aura (90%): Scintillating scotoma, zigzag lines, fortification spectra
     * Sensory aura: Unilateral paresthesias (pins and needles) spreading over minutes
     * Speech/language disturbance: Transient aphasia
     * Motor weakness (rare): Hemiplegic migraine (familial or sporadic)

   - TIMING: Aura develops over 5-20 minutes, lasts < 60 minutes, then headache follows

   - DIFFERENTIAL: Exclude stroke, TIA, seizure
     * Positive phenomena (zigzag lines) favor migraine over stroke
     * Gradual spread over minutes favors migraine (stroke is sudden)
     * Full recovery after aura (stroke has persistent deficit)

3. ACUTE TREATMENT (Abortive Therapy):
   A. TRIPTANS (First-line for moderate-severe migraine):
      - Mechanism: 5-HT1B/1D agonists, vasoconstriction, block trigeminal pain
      - Options: Sumatriptan (Imitrex), rizatriptan (Maxalt), eletriptan (Relpax)
      - Dosing: Take at onset of headache (not during aura)
        * Sumatriptan: 50-100 mg PO, or 6 mg SC, or 20 mg nasal spray
        * Rizatriptan: 10 mg PO (dissolving tablet)
      - Effectiveness: 60-70% pain-free at 2 hours
      - Side effects: Chest tightness, flushing, paresthesias (not cardiac)
      - Contraindications: Coronary artery disease, uncontrolled hypertension, stroke
      - Medication overuse headache if > 10 days/month

   B. NSAIDs (Mild to moderate migraine):
      - Ibuprofen 400-800 mg, naproxen 500 mg, aspirin 1000 mg
      - Effective if taken early
      - Combine with metoclopramide (anti-nausea + prokinetic)

   C. ANTIEMETICS:
      - Metoclopramide 10 mg IV/PO: Anti-nausea + enhances NSAID absorption
      - Prochlorperazine 10 mg IV/IM: Anti-dopaminergic, reduces nausea
      - Ondansetron 4-8 mg: Less effective than metoclopramide for migraine

   D. GEPANTS (CGRP antagonists, newer agents):
      - Ubrogepant (Ubrelvy), rimegepant (Nurtec)
      - Effective for acute migraine, alternative to triptans
      - No cardiovascular contraindications
      - Expensive, not first-line

4. PROPHYLACTIC TREATMENT (Preventive Therapy):
   INDICATIONS:
   - ≥ 4 migraine attacks per month
   - ≥ 8 headache days per month
   - Failure of acute treatment
   - Medication overuse headache
   - Patient preference

   A. FIRST-LINE OPTIONS:
      - PROPRANOLOL: 40-240 mg/day divided
        * Beta-blocker, most evidence for efficacy
        * Side effects: Fatigue, bradycardia, hypotension, depression
        * Avoid in asthma, heart block

      - TOPIRAMATE: 25-100 mg/day (start low, titrate slow)
        * Most effective (50% reduction in 50% of patients)
        * Side effects: Cognitive slowing, paresthesias, weight loss, kidney stones
        * Teratogenic (cleft palate), avoid in pregnancy

      - AMITRIPTYLINE: 25-100 mg at bedtime
        * Tricyclic antidepressant, good for chronic migraine
        * Side effects: Sedation, dry mouth, weight gain, constipation
        * Useful if comorbid depression or insomnia

      - VALPROATE: 500-1500 mg/day divided
        * Effective but teratogenic (avoid in women of childbearing potential)
        * Side effects: Weight gain, tremor, hair loss, hepatotoxicity

   B. CGRP MONOCLONAL ANTIBODIES (Newest, highly effective):
      - Erenumab (Aimovig), fremanezumab (Ajovy), galcanezumab (Emgality), eptinezumab (Vyepti)
      - Monthly or quarterly injections (or IV for eptinezumab)
      - 50% reduction in migraine days in 50-60% of patients
      - Minimal side effects (injection site reactions, constipation)
      - Expensive ($700/month), insurance often requires failure of 2+ oral prophylactics
      - Considered second-line or for chronic migraine

   C. BOTULINUM TOXIN (Chronic migraine only):
      - Indication: ≥ 15 headache days/month for ≥ 3 months
      - Injection protocol: 155-195 units across 31-39 sites (forehead, temples, neck, trapezius)
      - Repeat every 12 weeks
      - 50% reduction in headache days in 50% of patients
      - FDA-approved for chronic migraine, not episodic

   D. OTHER OPTIONS:
      - Candesartan (ARB): 16 mg/day, alternative to beta-blockers
      - Magnesium: 400 mg/day, mild benefit
      - Riboflavin (vitamin B2): 400 mg/day, mild benefit
      - Coenzyme Q10: 300 mg/day, mild benefit

5. CHRONIC MIGRAINE (≥ 15 headache days/month for ≥ 3 months):
   - Often medication overuse headache (MOH) from triptans/analgesics
   - Withdraw overused medication (may worsen for 2 weeks before improvement)
   - Start prophylaxis (topiramate, botulinum toxin, CGRP antibody)
   - Address comorbidities: Sleep, stress, depression, anxiety

6. MENSTRUAL MIGRAINE (Perimenstrual attacks):
   - TREATMENT:
     * Frovatriptan 2.5 mg BID for 6 days starting 2 days before menses
     * Naproxen 500 mg BID for same window
     * Continuous oral contraceptives (skip placebo week to avoid estrogen withdrawal)

7. MIGRAINE TRIGGERS (Identify and avoid):
   - Foods: Aged cheese, chocolate, alcohol (red wine), MSG, nitrates
   - Sleep: Too little or too much, irregular sleep schedule
   - Stress: Let-down after stress (weekend migraines)
   - Hormones: Menstruation, oral contraceptives
   - Sensory: Bright lights, strong smells, loud noises
   - Weather: Barometric pressure changes

8. RED FLAGS (Not migraine, consider alternative diagnosis):
   - First or worst headache of life (SAH)
   - Sudden onset (thunderclap)
   - Headache after age 50 (giant cell arteritis, mass lesion)
   - Progressive headache with personality change (mass, subdural)
   - Fever, neck stiffness (meningitis)
   - Focal neurological deficit that persists (stroke, tumor)
   - Papilledema (increased ICP)
   - Pregnancy or postpartum (venous sinus thrombosis, preeclampsia)
        """,
        key_factors=[
            "ICHD-3: ≥ 5 attacks, 4-72 hours, unilateral/pulsating/moderate-severe, plus nausea or photo/phonophobia",
            "Aura in 25%: Visual zigzag lines, gradual spread over 5-20 minutes, then headache",
            "Acute treatment: Triptans first-line for moderate-severe (sumatriptan 50-100 mg)",
            "Prophylaxis if ≥ 4 attacks/month: Topiramate, propranolol, or CGRP antibodies",
            "CGRP antibodies (erenumab): 50% reduction in 50-60%, expensive, second-line",
            "Chronic migraine (≥ 15 days/month): Botulinum toxin, topiramate, CGRP antibodies",
            "Red flags: First/worst headache, sudden onset, fever, focal deficit, papilledema"
        ],
        primary_authority=[
            "ICHD-3 2018 Headache Classification (International Headache Society)",
            "AAN/AHS 2012 Migraine Prevention Guidelines",
            "FDA approvals for CGRP antibodies (2018-2020) and gepants",
            "PREEMPT trials: Botulinum toxin for chronic migraine (2010)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ICHD-3 criteria are international standard; triptans first-line acute, CGRP antibodies emerging prophylaxis"
    ),
]


# ============================================================================
# ENGINE CORE LOGIC
# ============================================================================

class MED08NeurologyEngine:
    """Neurology Analysis Engine - TIE Architecture"""

    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry_log: List[TelemetryData] = []
        self.query_count = 0
        self.cache_hit_count = 0

        # Build keyword index for fast lookup
        self.keyword_index: Dict[str, List[DoctrineBlock]] = {}
        for block in self.doctrine_cache:
            for keyword in block.keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(block)

        logger.info(f"MED08 Neurology Engine initialized with {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode = ResponseMode.FAST,
        zone: AnalysisZone = AnalysisZone.PLANNING
    ) -> Dict[str, Any]:
        """
        TIE-20 Component: Three-layer response architecture
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (if cache miss)
        Layer 3: Deep analysis (full reasoning)
        """
        start_time = datetime.now()
        query_id = hashlib.sha256(f"{query}{datetime.now().isoformat()}".encode()).hexdigest()[:16]

        # Layer 1: Doctrine cache lookup
        triggered_blocks = self._doctrine_cache_lookup(query)
        cache_hit = len(triggered_blocks) > 0

        if cache_hit:
            self.cache_hit_count += 1
            response = self._generate_response_from_cache(query, triggered_blocks, mode, zone)
        else:
            # Layer 2/3: Semantic retrieval + deep analysis
            response = self._deep_analysis(query, mode, zone)

        # Record telemetry
        latency = (datetime.now() - start_time).total_seconds() * 1000
        telemetry = TelemetryData(
            query_id=query_id,
            timestamp=datetime.now().isoformat(),
            latency_ms=latency,
            cache_hit=cache_hit,
            doctrine_topics_triggered=[b.topic for b in triggered_blocks],
            confidence_level=response.get("confidence", "DEFENSIBLE"),
            response_mode=mode.value,
            zone=zone.value
        )
        self.telemetry_log.append(telemetry)
        self.query_count += 1

        logger.info(f"Query {query_id}: {len(triggered_blocks)} doctrines triggered, {latency:.1f}ms, cache_hit={cache_hit}")

        return response

    def _doctrine_cache_lookup(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache by keyword matching"""
        query_lower = query.lower()
        matched_blocks = []

        # Keyword-based matching
        for keyword, blocks in self.keyword_index.items():
            if keyword in query_lower:
                matched_blocks.extend(blocks)

        # Deduplicate and rank by keyword match count
        block_scores = {}
        for block in matched_blocks:
            if block.topic not in block_scores:
                block_scores[block.topic] = {"block": block, "score": 0}
            block_scores[block.topic]["score"] += 1

        # Return top 5 blocks
        sorted_blocks = sorted(block_scores.values(), key=lambda x: x["score"], reverse=True)
        return [item["block"] for item in sorted_blocks[:5]]

    def _generate_response_from_cache(
        self,
        query: str,
        blocks: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """Generate response from cached doctrine blocks"""

        # Select primary block (highest relevance)
        primary_block = blocks[0]

        if mode == ResponseMode.FAST:
            # Concise response: conclusion + key factors
            return {
                "query": query,
                "mode": mode.value,
                "zone": zone.value,
                "conclusion": primary_block.conclusion_template,
                "key_factors": primary_block.key_factors[:5],
                "confidence": primary_block.confidence.value,
                "authority": primary_block.primary_authority[0] if primary_block.primary_authority else None,
                "doctrine_topics": [b.topic for b in blocks],
                "determinism_hash": self._compute_determinism_hash(query, primary_block)
            }

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready: full reasoning framework
            return {
                "query": query,
                "mode": mode.value,
                "zone": zone.value,
                "conclusion": primary_block.conclusion_template,
                "reasoning_framework": primary_block.reasoning_framework,
                "key_factors": primary_block.key_factors,
                "primary_authority": primary_block.primary_authority,
                "confidence": primary_block.confidence.value,
                "confidence_stratification": primary_block.confidence_stratification,
                "burden_holder": primary_block.burden_holder,
                "adversary_position": primary_block.adversary_position,
                "counter_arguments": primary_block.counter_arguments,
                "resolution_strategy": primary_block.resolution_strategy,
                "controlling_precedent": primary_block.controlling_precedent,
                "doctrine_topics": [b.topic for b in blocks],
                "related_doctrines": [{"topic": b.topic, "keywords": b.keywords} for b in blocks[1:3]],
                "determinism_hash": self._compute_determinism_hash(query, primary_block)
            }

        else:  # MEMO mode
            # Full documentation: multi-doctrine synthesis
            return {
                "query": query,
                "mode": mode.value,
                "zone": zone.value,
                "executive_summary": primary_block.conclusion_template,
                "primary_doctrine": {
                    "topic": primary_block.topic,
                    "reasoning_framework": primary_block.reasoning_framework,
                    "key_factors": primary_block.key_factors,
                    "authority": primary_block.primary_authority,
                    "confidence": primary_block.confidence.value
                },
                "related_doctrines": [
                    {
                        "topic": b.topic,
                        "conclusion": b.conclusion_template,
                        "keywords": b.keywords,
                        "authority": b.primary_authority
                    }
                    for b in blocks[1:]
                ],
                "comprehensive_analysis": self._synthesize_multi_doctrine(blocks),
                "risk_assessment": self._fact_fragility_scoring(primary_block),
                "recommendations": self._generate_recommendations(primary_block, zone),
                "determinism_hash": self._compute_determinism_hash(query, primary_block)
            }

    def _deep_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> Dict[str, Any]:
        """
        Deep analysis when cache misses
        In production, this would call vector search + LLM synthesis
        For now, return general guidance
        """
        return {
            "query": query,
            "mode": mode.value,
            "zone": zone.value,
            "conclusion": f"Deep analysis required for query: {query}. No direct doctrine match found. Consider consulting primary neurological references or subspecialty guidelines.",
            "guidance": "This query requires clinical judgment beyond cached doctrine. Recommend reviewing patient-specific factors, obtaining relevant imaging/labs, and consulting subspecialty if needed.",
            "suggested_doctrines": [b.topic for b in self.doctrine_cache[:5]],
            "confidence": ConfidenceLevel.DISCLOSURE.value,
            "determinism_hash": hashlib.sha256(query.encode()).hexdigest()
        }

    def _synthesize_multi_doctrine(self, blocks: List[DoctrineBlock]) -> str:
        """Synthesize multiple doctrine blocks into coherent analysis"""
        synthesis_parts = []
        for i, block in enumerate(blocks[:3], 1):
            synthesis_parts.append(f"{i}. {block.topic}: {block.conclusion_template}")

        return " | ".join(synthesis_parts)

    def _fact_fragility_scoring(self, block: DoctrineBlock) -> Dict[str, Any]:
        """
        TIE-20 Component: Fact fragility scoring
        Assesses verifiability and recharacterization risk
        """
        # Higher authority sources = lower fragility
        authority_count = len(block.primary_authority)
        fragility_score = max(1, 10 - authority_count * 2)

        return {
            "fragility_score": fragility_score,
            "verifiability": "HIGH" if authority_count >= 3 else "MEDIUM" if authority_count >= 2 else "LOW",
            "recharacterization_risk": "LOW" if block.confidence == ConfidenceLevel.DEFENSIBLE else "MEDIUM",
            "testimony_dependence": "LOW"  # Medical facts generally well-documented
        }

    def _generate_recommendations(self, block: DoctrineBlock, zone: AnalysisZone) -> List[str]:
        """Generate actionable recommendations based on zone"""
        recommendations = []

        if zone == AnalysisZone.PLANNING:
            recommendations.append(f"Review {block.topic} guidelines before proceeding")
            recommendations.append("Obtain relevant diagnostic studies per protocol")
            if block.primary_authority:
                recommendations.append(f"Reference: {block.primary_authority[0]}")

        elif zone == AnalysisZone.REPORTING:
            recommendations.append("Document clinical reasoning in medical record")
            recommendations.append("Include relevant physical exam and diagnostic findings")
            recommendations.append("Cite evidence-based guidelines used in decision-making")

        elif zone == AnalysisZone.AUDIT:
            recommendations.append("Ensure documentation supports medical necessity")
            recommendations.append("Verify compliance with clinical practice guidelines")
            if block.primary_authority:
                recommendations.append(f"Guideline support: {block.primary_authority[0]}")

        return recommendations

    def _compute_determinism_hash(self, query: str, block: DoctrineBlock) -> str:
        """
        TIE-20 Component: Determinism hash for reproducibility
        SHA-256 hash of query + doctrine topic
        """
        content = f"{query}|{block.topic}|{block.conclusion_template}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def health_check(self) -> Dict[str, Any]:
        """
        TIE-20 Component: Health endpoint
        Returns comprehensive engine status
        """
        cache_hit_rate = (self.cache_hit_count / self.query_count * 100) if self.query_count > 0 else 0

        avg_latency = 0
        if self.telemetry_log:
            avg_latency = sum(t.latency_ms for t in self.telemetry_log) / len(self.telemetry_log)

        return {
            "status": "operational",
            "engine": "MED08_neurology",
            "version": "1.0.0",
            "port": 9233,
            "doctrine_blocks": len(self.doctrine_cache),
            "query_count": self.query_count,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "avg_latency_ms": f"{avg_latency:.1f}",
            "telemetry_records": len(self.telemetry_log),
            "last_query": self.telemetry_log[-1].timestamp if self.telemetry_log else None
        }

    def get_metrics(self) -> Dict[str, Any]:
        """
        TIE-20 Component: Metrics collector
        Returns detailed performance metrics
        """
        if not self.telemetry_log:
            return {"message": "No queries processed yet"}

        latencies = [t.latency_ms for t in self.telemetry_log]

        return {
            "total_queries": self.query_count,
            "cache_hits": self.cache_hit_count,
            "cache_hit_rate": f"{(self.cache_hit_count / self.query_count * 100):.1f}%",
            "avg_latency_ms": sum(latencies) / len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 20 else max(latencies),
            "doctrine_coverage": {
                "total_blocks": len(self.doctrine_cache),
                "triggered_blocks": len(set(t.doctrine_topics_triggered[0] if t.doctrine_topics_triggered else None for t in self.telemetry_log if t.doctrine_topics_triggered))
            }
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="MED08 Neurology Analysis Engine",
    description="TIE-grade neurology intelligence engine with 25+ doctrine blocks covering stroke, seizures, neurodegenerative diseases, TBI, and neuroimaging",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = MED08NeurologyEngine()


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Neurology question or clinical scenario")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context zone")


class QueryResponse(BaseModel):
    query: str
    mode: str
    zone: str
    conclusion: str
    key_factors: Optional[List[str]] = None
    reasoning_framework: Optional[str] = None
    confidence: str
    doctrine_topics: List[str]
    determinism_hash: str
    primary_authority: Optional[List[str]] = None


# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.get("/")
async def root():
    """Root endpoint with engine info"""
    return {
        "engine": "MED08_neurology",
        "version": "1.0.0",
        "status": "operational",
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "endpoints": ["/query", "/health", "/metrics", "/doctrines"]
    }


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """
    Main query endpoint
    Processes neurology questions using three-layer TIE architecture
    """
    try:
        result = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone
        )
        return result
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health")
async def health():
    """
    TIE-20 Component: Health endpoint
    Returns comprehensive engine status
    """
    return engine.health_check()


@APP.get("/metrics")
async def metrics():
    """
    TIE-20 Component: Metrics endpoint
    Returns performance telemetry
    """
    return engine.get_metrics()


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "total_blocks": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "keywords": block.keywords,
                "confidence": block.confidence.value,
                "authority_count": len(block.primary_authority)
            }
            for block in DOCTRINE_CACHE
        ]
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting MED08 Neurology Engine on port 9233")
    uvicorn.run(APP, host="0.0.0.0", port=9233)
