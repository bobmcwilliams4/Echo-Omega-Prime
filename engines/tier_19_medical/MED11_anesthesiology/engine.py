"""
MED11 ANESTHESIOLOGY INTELLIGENCE ENGINE v1.0.0

Comprehensive anesthesiology analysis: general anesthesia, regional techniques,
airway management, hemodynamic monitoring, perioperative complications.

TIE-20 Compliant: Three-layer response, doctrine cache, authority hardening,
confidence stratification, semantic normalization, telemetry, drift watcher,
coverage map, health endpoint, audit trail, determinism hash.

Port: 9311
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ResponseMode(str, Enum):
    """Response detail levels"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Stratified confidence levels"""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Anesthesiology issue categories"""
    GENERAL_ANESTHESIA = "GENERAL_ANESTHESIA"
    REGIONAL_ANESTHESIA = "REGIONAL_ANESTHESIA"
    AIRWAY_MANAGEMENT = "AIRWAY_MANAGEMENT"
    PHARMACOLOGY = "PHARMACOLOGY"
    MONITORING = "MONITORING"
    PREOPERATIVE = "PREOPERATIVE"
    COMPLICATIONS = "COMPLICATIONS"
    PEDIATRIC = "PEDIATRIC"
    OBSTETRIC = "OBSTETRIC"
    CARDIAC = "CARDIAC"
    NEUROSURGICAL = "NEUROSURGICAL"
    PAIN_MANAGEMENT = "PAIN_MANAGEMENT"


class AnalysisZone(str, Enum):
    """Position zones - never blur"""
    PLANNING = "PLANNING"
    INTRAOPERATIVE = "INTRAOPERATIVE"
    POSTOPERATIVE = "POSTOPERATIVE"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Single doctrine block with full reasoning"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    entity_scope: str = "all_patients"
    burden_holder: str = "anesthesiologist"
    adversary_position: str = "none"
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: str = "evidence_based_protocol"
    controlling_precedent: str = "ASA_guidelines"
    fact_fragility: float = 0.3

    def matches(self, query: str) -> float:
        """Calculate match score"""
        query_lower = query.lower()
        score = 0.0

        if self.topic.lower() in query_lower:
            score += 3.0

        for kw in self.keywords:
            if kw.lower() in query_lower:
                score += 1.0

        return score


class QueryRequest(BaseModel):
    """Anesthesia query request"""
    query: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    zone: Optional[AnalysisZone] = None
    patient_context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Anesthesia analysis response"""
    query: str
    mode: ResponseMode
    zone: Optional[AnalysisZone]
    answer: str
    triggered_doctrines: List[str]
    confidence: ConfidenceLevel
    stratification_reason: str
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    queries_processed: int
    avg_latency_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL ANESTHESIOLOGY BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # GENERAL ANESTHESIA
    DoctrineBlock(
        topic="Stages of General Anesthesia",
        keywords=["induction", "maintenance", "emergence", "stage", "depth", "guedel", "signs"],
        conclusion_template="General anesthesia progresses through four Guedel stages: I (analgesia), II (excitement/delirium), III (surgical anesthesia with 4 planes), IV (medullary paralysis). Modern practice targets stage III plane 2-3 with titrated agents and monitoring. Rapid smooth induction minimizes stage II duration. Balanced technique uses multiple agents to achieve unconsciousness, amnesia, analgesia, and muscle relaxation.",
        reasoning_framework="""
Stage I (Analgesia): From induction to loss of consciousness
- Patient drowsy but responsive
- Pain perception decreased
- Reflexes intact
- Suitable for minor procedures (dental)

Stage II (Excitement/Delirium): From loss of consciousness to onset of regular breathing
- Unpredictable behavior possible
- Irregular breathing, increased muscle tone
- Laryngospasm and vomiting risk high
- Blood pressure and heart rate elevated
- MINIMIZE this stage - rapid induction with propofol/sevoflurane

Stage III (Surgical Anesthesia): Four planes
- Plane 1: Regular respiration, eyes roll, pupils constrict
- Plane 2: Cessation of eye movement, loss of corneal reflex, target for most surgery
- Plane 3: Intercostal paralysis, diaphragmatic breathing only
- Plane 4: Complete intercostal/diaphragmatic paralysis, dilated pupils
- Modern monitoring: BIS 40-60, ETAC tracking, neuromuscular monitoring

Stage IV (Medullary Paralysis): Overdose
- Respiratory and circulatory collapse
- Dilated pupils, absent reflexes
- Immediate resuscitation required

Balanced Anesthesia Concept:
- Hypnotic (propofol/sevoflurane): unconsciousness
- Analgesic (fentanyl/remifentanil): pain control
- Muscle relaxant (rocuronium): immobility
- Titrate each component to minimize side effects
- Monitor depth: BIS, ETAC, hemodynamics, movement
        """,
        key_factors=[
            "Guedel stage classification guides anesthetic depth",
            "Stage II excitation minimized by rapid smooth induction",
            "Stage III plane 2-3 target for most surgical procedures",
            "Modern monitoring (BIS, ETAC) supplements clinical signs",
            "Balanced technique uses multiple agents for optimal control",
            "Stage IV is life-threatening overdose requiring immediate intervention"
        ],
        primary_authority=[
            "Guedel AE. Inhalation Anesthesia: A Fundamental Guide (1937)",
            "ASA Guidelines for Intraoperative Monitoring (2020)",
            "Miller's Anesthesia 9th Ed - Depth of Anesthesia Monitoring"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core anesthesiology teaching; well-established staging system with modern monitoring adjuncts"
    ),

    DoctrineBlock(
        topic="Minimum Alveolar Concentration (MAC)",
        keywords=["MAC", "potency", "sevoflurane", "desflurane", "isoflurane", "volatile", "agent"],
        conclusion_template="MAC is the alveolar concentration of inhaled anesthetic at which 50% of patients do not move to surgical incision. MAC values: sevoflurane 2.0%, desflurane 6.0%, isoflurane 1.15%. MAC decreases with age, hypothermia, pregnancy, concurrent opioids/sedatives. Target 0.7-1.3 MAC for surgical anesthesia. MAC-awake (0.3-0.5 MAC) and MAC-BAR (1.3-1.5 MAC) define other endpoints.",
        reasoning_framework="""
MAC Definition and Significance:
- Standardized measure of volatile anesthetic potency
- Population median (50% response) not individual MED
- 1 MAC prevents movement in 50%, 1.3 MAC in 95% (MAC-BAR)
- Additive across agents: 0.5 MAC sevo + 0.5 MAC N2O = 1.0 MAC

Standard MAC Values (age 40, sea level, 37°C):
- Sevoflurane: 2.0% (most common, pleasant induction)
- Desflurane: 6.0% (rapid on/off, pungent, bronchospasm risk)
- Isoflurane: 1.15% (older agent, cardiovascular stable)
- Nitrous oxide: 104% (cannot achieve 1 MAC alone at 1 atm)
- Halothane: 0.75% (rarely used, hepatotoxicity risk)

MAC Modifiers (decrease MAC):
- Age: 6% decrease per decade after 40
- Hypothermia: 5% per degree C below 37°C
- Pregnancy: 25-40% reduction
- Opioids: fentanyl 2-5 mcg/kg reduces MAC 50%
- Alpha-2 agonists (dexmedetomidine): 30-50% reduction
- Acute alcohol intoxication: modest reduction
- Chronic alcohol use: increases MAC (enzyme induction)
- Hypotension, severe anemia: decrease MAC

MAC Variants:
- MAC-awake: 0.3-0.5 MAC, concentration preventing response to verbal command
- MAC-BAR: 1.3-1.5 MAC, blocks adrenergic response to incision
- MAC-intubation: 1.3-1.6 MAC, allows tracheal intubation without muscle relaxant

Clinical Application:
- Target 0.7-1.0 MAC with balanced technique (opioid + volatile)
- Monitor end-tidal agent concentration (ETAC) continuously
- Adjust for patient factors: elderly may need 0.5-0.7 MAC only
- Desflurane emergence faster but risk of agitation
- Sevoflurane preferred for induction (less pungent)
        """,
        key_factors=[
            "MAC is population median (50%) not individual dose",
            "Sevoflurane 2.0%, desflurane 6.0%, isoflurane 1.15%",
            "MAC decreases 6% per decade, 25-40% in pregnancy",
            "Target 0.7-1.3 MAC depending on balanced technique",
            "End-tidal agent concentration monitoring essential",
            "MAC-BAR (1.3-1.5) blocks adrenergic response to surgery"
        ],
        primary_authority=[
            "Eger EI. The pharmacology of inhaled anesthetics (2001)",
            "ASA Guidelines for Intraoperative Monitoring (2020)",
            "Barash Clinical Anesthesia 8th Ed - Inhaled Anesthetics Chapter"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established pharmacological principle with extensive clinical validation"
    ),

    DoctrineBlock(
        topic="Propofol Total Intravenous Anesthesia (TIVA)",
        keywords=["propofol", "TIVA", "TCI", "target", "controlled", "infusion", "induction", "maintenance"],
        conclusion_template="Propofol is the most common IV anesthetic for induction (1.5-2.5 mg/kg) and maintenance (100-200 mcg/kg/min). Target-controlled infusion (TCI) uses pharmacokinetic models (Marsh, Schnider) to achieve plasma or effect-site targets (2-6 mcg/mL). TIVA with propofol/remifentanil offers rapid emergence, reduced PONV, and suitability for TIVA-required cases (malignant hyperthermia risk, neuromonitoring). Monitor depth with BIS/entropy.",
        reasoning_framework="""
Propofol Pharmacology:
- Rapid onset (30-60 sec), short duration (5-10 min single dose)
- Context-sensitive half-time increases with infusion duration
- Hepatic metabolism, inactive metabolites
- Redistribution drives initial recovery
- No analgesic properties - requires opioid co-administration

Induction Dosing:
- Standard: 1.5-2.5 mg/kg IV
- Elderly/ASA 3-4: 1.0-1.5 mg/kg (reduced clearance)
- Pediatric: 2.5-3.5 mg/kg (higher volume of distribution)
- Co-induction with opioid (fentanyl 1-2 mcg/kg) reduces dose 30%

Maintenance Infusion:
- Manual: 100-200 mcg/kg/min titrated to effect
- TCI: Target plasma 2-6 mcg/mL (Marsh model) or effect-site 2-4 mcg/mL (Schnider)
- Marsh model: Better for induction, younger patients
- Schnider model: Better for elderly, incorporates lean body mass
- Adjust for surgical stimulation and opioid co-administration

TCI Models:
- Three-compartment pharmacokinetic models
- Input patient age, weight, height, gender
- Pump calculates infusion rate to achieve target concentration
- Effect-site targeting accounts for blood-brain equilibration (2-3 min)
- More stable depth, faster adjustments than manual infusion

TIVA Advantages:
- Reduced PONV (50% vs volatile agents)
- Suitable for malignant hyperthermia susceptibility
- Allows neuromonitoring (MEP, SSEP not suppressed)
- Rapid emergence with propofol/remifentanil
- Environmental benefits (no volatile agent pollution)

TIVA Disadvantages:
- No end-tidal monitoring (awareness risk if pump fails)
- Requires processed EEG monitoring (BIS, entropy)
- Propofol infusion syndrome risk (high dose >5 mg/kg/h >48h)
- Hypotension (dose-dependent vasodilation)
- Pain on injection (mix with lidocaine 10-20 mg)

Monitoring Requirements:
- BIS target 40-60 or entropy SE 40-60
- Blood pressure (treat hypotension with vasopressor/fluid)
- Neuromuscular monitoring if muscle relaxant used
- Pump function checks (ensure IV patent, no air)
        """,
        key_factors=[
            "Induction 1.5-2.5 mg/kg, reduce in elderly/sick",
            "Maintenance 100-200 mcg/kg/min or TCI 2-6 mcg/mL",
            "TCI models (Marsh/Schnider) improve stability",
            "Requires processed EEG monitoring (BIS 40-60)",
            "Reduced PONV, suitable for MH and neuromonitoring",
            "Propofol infusion syndrome risk with prolonged high dose"
        ],
        primary_authority=[
            "Marsh et al. Pharmacokinetic model for propofol (1991)",
            "Schnider et al. Influence of age on propofol (1999)",
            "ASA Practice Advisory on TIVA (2018)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extensively studied technique with validated pharmacokinetic models"
    ),

    # NEUROMUSCULAR BLOCKING AGENTS
    DoctrineBlock(
        topic="Succinylcholine vs Rocuronium for Rapid Sequence Induction",
        keywords=["RSI", "rapid", "sequence", "succinylcholine", "rocuronium", "intubation", "aspiration"],
        conclusion_template="Rapid sequence induction (RSI) minimizes aspiration risk by achieving intubating conditions in <60 seconds without mask ventilation. Succinylcholine 1-1.5 mg/kg provides fastest onset (45-60 sec) but has contraindications (hyperkalemia, malignant hyperthermia, burns). Rocuronium 1.0-1.2 mg/kg achieves similar onset (60-90 sec) and is reversible with sugammadex 16 mg/kg. Rocuronium is preferred unless succinylcholine specifically indicated.",
        reasoning_framework="""
RSI Indications:
- Full stomach (recent meal <6-8 hours)
- Gastroparesis, bowel obstruction
- Pregnancy (delayed gastric emptying)
- Emergency surgery without adequate fasting
- Morbid obesity
- GERD with hiatal hernia

RSI Technique:
1. Preoxygenation: 3-5 min or 8 vital capacity breaths (ETO2 >90%)
2. Cricoid pressure (Sellick maneuver) - controversial, may hinder intubation
3. Induction agent: propofol 1.5-2 mg/kg or etomidate 0.2-0.3 mg/kg
4. Neuromuscular blocker: succinylcholine 1-1.5 mg/kg or rocuronium 1.0-1.2 mg/kg
5. NO mask ventilation (minimize gastric insufflation)
6. Intubation at 45-60 sec (succinylcholine) or 60-90 sec (rocuronium)
7. Confirm placement (ETCO2 waveform), release cricoid pressure

Succinylcholine Profile:
- Depolarizing agent, mimics acetylcholine
- Onset: 45-60 seconds at 1-1.5 mg/kg
- Duration: 5-10 minutes (plasma cholinesterase metabolism)
- Intubating conditions in <60 sec in 95% of patients

Succinylcholine Contraindications (hyperkalemia risk):
- Burns >24 hours old (upregulated receptors)
- Denervation injury, spinal cord injury >48 hours
- Chronic immobility, muscular dystrophy
- Massive trauma, crush injury
- Known hyperkalemia
- Personal/family history of malignant hyperthermia
- Plasma cholinesterase deficiency (prolonged paralysis)

Succinylcholine Side Effects:
- Fasciculations (increase IOP, ICP, gastric pressure)
- Myalgia (20-50% incidence)
- Bradycardia (especially children, repeat doses)
- Malignant hyperthermia trigger (rare but catastrophic)

Rocuronium High-Dose RSI:
- Dose: 1.0-1.2 mg/kg (3-4x ED95)
- Onset: 60-90 seconds (comparable to succinylcholine at 90 sec)
- Duration: 45-75 minutes (long if intubation fails)
- Sugammadex 16 mg/kg reverses in 2-3 min (rescue option)

Rocuronium Advantages:
- No hyperkalemia risk
- No malignant hyperthermia trigger
- Reversible with sugammadex (even immediately post-dose)
- No fasciculations, less myalgia
- Suitable for all patients

Rocuronium Disadvantages:
- Slightly slower onset (60-90 vs 45-60 sec)
- Long duration if sugammadex unavailable
- Expensive (rocuronium + sugammadex vs succinylcholine alone)

Current Consensus:
- Rocuronium 1.2 mg/kg preferred for most RSI (with sugammadex available)
- Succinylcholine reserved for: cannot intubate/cannot ventilate (CICV) rescue, short procedure where long paralysis undesirable, rocuronium allergy
- Both agents achieve excellent intubating conditions in <90 seconds
        """,
        key_factors=[
            "RSI minimizes aspiration risk with rapid intubation",
            "Succinylcholine 1-1.5 mg/kg: 45-60 sec onset, contraindicated if hyperkalemia risk",
            "Rocuronium 1.0-1.2 mg/kg: 60-90 sec onset, reversible with sugammadex",
            "Rocuronium preferred unless succinylcholine specifically needed",
            "Sugammadex 16 mg/kg reverses rocuronium in 2-3 min",
            "Preoxygenation and cricoid pressure are RSI adjuncts"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Management of the Difficult Airway (2022)",
            "Difficult Airway Society Guidelines (2015)",
            "Naguib et al. Sugammadex reversal (2015)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established RSI techniques with recent shift favoring rocuronium due to sugammadex availability"
    ),

    DoctrineBlock(
        topic="Sugammadex Reversal of Neuromuscular Blockade",
        keywords=["sugammadex", "reversal", "rocuronium", "vecuronium", "neostigmine", "bridion"],
        conclusion_template="Sugammadex is a selective relaxant binding agent that rapidly reverses rocuronium and vecuronium. Dosing: 2 mg/kg for moderate block (TOF 2-4 twitches), 4 mg/kg for deep block (PTC 1-2), 16 mg/kg for immediate reversal. Reverses rocuronium 1.2 mg/kg in 2-3 minutes. Superior to neostigmine (faster, no muscarinic side effects, effective at deep block). Contraindications: severe renal impairment (CrCl <30), allergy. Cost limits routine use.",
        reasoning_framework="""
Mechanism of Action:
- Gamma-cyclodextrin molecule encapsulates rocuronium/vecuronium
- Forms 1:1 complex, removing free drug from NMJ
- Does NOT work via acetylcholinesterase inhibition (unlike neostigmine)
- Effective at ANY depth of block (even immediate post-dose)

Dosing Based on Depth of Block:
- Moderate block (TOF count 2-4): 2 mg/kg
- Deep block (PTC 1-2, TOF 0): 4 mg/kg
- Immediate reversal (within 3 min of rocuronium 1.2 mg/kg): 16 mg/kg
- Higher doses for vecuronium (less affinity than rocuronium)

Reversal Speed:
- 2 mg/kg: TOF ratio >0.9 in 2-3 minutes (moderate block)
- 4 mg/kg: TOF ratio >0.9 in 2-4 minutes (deep block)
- 16 mg/kg: TOF ratio >0.9 in 2-3 minutes (immediate post-RSI)
- Much faster than neostigmine (10-20 min to TOF >0.9)

Advantages over Neostigmine:
- No ceiling effect (works at deep block where neostigmine fails)
- No muscarinic side effects (bradycardia, bronchospasm, salivation)
- No need for anticholinergic (glycopyrrolate/atropine)
- Faster reversal (2-3 min vs 10-20 min)
- More reliable (less variability)
- Rescue option for cannot intubate/cannot ventilate (reverse RSI dose)

Contraindications and Precautions:
- Severe renal impairment (CrCl <30 mL/min): sugammadex-rocuronium complex not cleared
- Allergy (rare): anaphylaxis reported
- Pregnancy: limited data, not contraindicated but use if benefit outweighs risk
- Oral contraceptives: theoretically binds progesterone, advise backup contraception
- Recurrence of block: possible if inadequate dose or patient redistribution

Monitoring:
- Train-of-four (TOF) monitoring essential
- TOF ratio >0.9 confirms adequate reversal
- Do NOT rely on clinical signs alone (sustained head lift unreliable)

Cost Considerations:
- Sugammadex expensive (100-300 USD per dose vs 5-10 USD neostigmine)
- Use reserved for: deep block reversal, immediate reversal needed, CICV rescue, patients where neostigmine contraindicated (severe asthma/COPD)
- Routine shallow block reversal may still use neostigmine at some institutions

Clinical Scenarios Favoring Sugammadex:
- Immediate reversal after RSI (CICV, esophageal intubation)
- Deep block at end of case (surgeon gave extra rocuronium)
- Patient with severe reactive airway disease (avoid neostigmine bronchospasm)
- Rapid case turnover (faster reversal = faster emergence)
        """,
        key_factors=[
            "Selective binding agent, encapsulates rocuronium/vecuronium",
            "Dosing: 2 mg/kg moderate, 4 mg/kg deep, 16 mg/kg immediate",
            "Reverses to TOF >0.9 in 2-3 minutes",
            "No muscarinic side effects unlike neostigmine",
            "Effective at ANY depth including immediate post-dose",
            "Contraindicated in severe renal impairment (CrCl <30)"
        ],
        primary_authority=[
            "FDA Sugammadex Label (Bridion, 2015)",
            "Naguib et al. Consensus on Neuromuscular Monitoring (2018)",
            "ASA Guidelines on Neuromuscular Blockade (2023)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extensively studied with well-defined dosing and safety profile; cost limits universal adoption"
    ),

    # AIRWAY MANAGEMENT
    DoctrineBlock(
        topic="Difficult Airway Prediction and Management",
        keywords=["difficult", "airway", "Mallampati", "thyromental", "LEMON", "algorithm", "DAS", "ASA"],
        conclusion_template="Difficult airway assessment includes Mallampati score (I-IV), thyromental distance (<6 cm predicts difficulty), mouth opening (<3 cm), cervical spine mobility, and prior history. Mallampati III-IV, BMI >35, limited neck extension, and small mandible increase difficulty. ASA Difficult Airway Algorithm guides management: attempt direct laryngoscopy, then video laryngoscopy, then supraglottic airway, then cricothyrotomy if CICV. Awake fiberoptic intubation for predicted severe difficulty.",
        reasoning_framework="""
Preoperative Airway Assessment (LEMON):
L - Look externally: facial trauma, beard, large tongue, small mandible
E - Evaluate 3-3-2: mouth opening 3 fingers, hyoid-mental 3 fingers, thyroid-hyoid 2 fingers
M - Mallampati score (tongue size relative to pharynx)
O - Obstruction (tumor, abscess, epiglottitis)
N - Neck mobility (atlanto-occipital extension)

Mallampati Classification:
- Class I: Full visibility of soft palate, uvula, fauces, pillars
- Class II: Soft palate, uvula, fauces visible
- Class III: Soft palate, base of uvula visible (difficulty predicted)
- Class IV: Only hard palate visible (difficulty very likely)
- Sensitivity 50%, specificity 85% (useful when positive)

Other Predictors:
- Thyromental distance <6 cm (three finger breadths): limited submandibular space
- Mouth opening <3 cm (two finger breadths): limited access
- Reduced neck extension: cervical spine disease, rheumatoid arthritis
- High BMI >35: difficult mask ventilation and intubation
- History of difficult intubation (most reliable predictor)

ASA Difficult Airway Algorithm (2022):
1. KNOWN difficult airway:
   - Awake intubation (fiberoptic, video laryngoscopy)
   - Airway topicalization + sedation
   - Maintain spontaneous ventilation

2. UNEXPECTED difficult airway after induction:
   - Call for help
   - Optimize patient position (ear to sternal notch)
   - Optimize laryngoscopy (BURP, different blade)
   - Limit attempts (3 maximum to avoid trauma)
   - Transition to video laryngoscopy (C-MAC, Glidescope)
   - Insert supraglottic airway (LMA) if cannot intubate
   - Wake patient if elective surgery

3. CANNOT intubate, CANNOT ventilate (CICV):
   - Emergency cricothyrotomy (scalpel-bougie-tube technique)
   - Time-critical (brain injury starts at 3-4 min hypoxia)
   - Rare but life-threatening (1:5,000-10,000 anesthetics)

Difficult Airway Society (DAS) Guidelines:
- Plan A: Direct laryngoscopy (optimize, 3 attempts max)
- Plan B: Supraglottic airway (LMA, allow ventilation/oxygenation)
- Plan C: Facemask ventilation (two-person technique)
- Plan D: Front of neck access (emergency cricothyrotomy)

Video Laryngoscopy:
- Indirect view via camera on blade tip
- Improved glottic view (Cormack-Lehane grade)
- Does NOT guarantee easier intubation (can see but not pass tube)
- Requires stylet/bougie to navigate tube around curve
- First-line in many institutions for RSI

Awake Fiberoptic Intubation:
- Gold standard for predicted severe difficulty
- Indications: base of tongue tumor, unstable cervical spine, prior failed intubation
- Technique: topical anesthesia (lidocaine spray, nebulized, superior laryngeal/glossopharyngeal nerve blocks), sedation (dexmedetomidine, remifentanil), fiberoptic scope via nose or mouth
- Confirm tracheal position before inducing anesthesia

Emergency Cricothyrotomy:
- Scalpel-bougie-tube (preferred over needle cricothyrotomy)
- Vertical skin incision, horizontal cricothyroid membrane incision
- Insert bougie, railroad 6.0 cuffed tube over bougie
- Secure and ventilate, confirm ETCO2
        """,
        key_factors=[
            "Mallampati III-IV, thyromental <6 cm predict difficulty",
            "ASA algorithm: optimize laryngoscopy, then video, then SGA, then cricothyrotomy",
            "Difficult Airway Society: Plan A-D approach",
            "Awake fiberoptic for predicted severe difficulty",
            "CICV is life-threatening, requires emergency cricothyrotomy",
            "Video laryngoscopy improves view but doesn't guarantee intubation"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Management of the Difficult Airway (2022)",
            "Difficult Airway Society Guidelines (2015)",
            "Cook TM. NAP4: Major complications of airway management (2011)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Consensus guidelines with well-defined algorithms; prediction imperfect but management approach clear"
    ),

    DoctrineBlock(
        topic="Supraglottic Airway Devices (LMA)",
        keywords=["LMA", "supraglottic", "laryngeal", "mask", "i-gel", "airway", "rescue"],
        conclusion_template="Supraglottic airway devices (SAD) sit above the glottis and provide ventilation without tracheal intubation. LMA Classic, LMA Supreme, and i-gel are common types. Indications: elective short procedures, difficult airway rescue, conduit for fiberoptic intubation. Contraindications: full stomach (aspiration risk), morbid obesity, high airway pressures. Insertion success rate >95% on first attempt. Allows positive pressure ventilation up to 20-25 cm H2O.",
        reasoning_framework="""
Supraglottic Airway Device Types:
- LMA Classic: reusable, inflatable cuff, first-generation
- LMA Unique: single-use version of Classic
- LMA Supreme: second-generation, gastric port, higher seal pressure
- LMA ProSeal: second-generation, gastric port, double cuff
- i-gel: single-use, gel cuff (no inflation), rapid insertion
- Air-Q: intubating LMA, allows fiberoptic-guided intubation

Mechanism:
- Sits in hypopharynx with cuff sealing around laryngeal inlet
- Distal opening aligned with glottis
- Does NOT enter trachea (supraglottic)
- Allows spontaneous or positive pressure ventilation

Indications:
- Elective surgery: short procedures (<2 hours), low aspiration risk
- Difficult airway rescue: cannot intubate but can ventilate via LMA
- Conduit for fiberoptic intubation (intubating LMA, Air-Q)
- Out-of-hospital resuscitation (easier insertion than intubation)

Contraindications:
- Full stomach, high aspiration risk (recent meal, bowel obstruction)
- Morbid obesity (BMI >40, increased gastric pressure)
- Prone or steep Trendelenburg position
- Laparoscopic surgery with high insufflation pressures (relative)
- Airway pathology distorting anatomy (tumor, abscess)

Insertion Technique:
1. Lubricate cuff with water-soluble gel
2. Deflate cuff fully (Classic/Supreme)
3. Head extended, neck flexed (sniffing position)
4. Insert along hard palate, advance until resistance felt
5. Inflate cuff (watch for 1-2 cm rise, check cuff pressure <60 cm H2O)
6. Confirm ventilation (chest rise, ETCO2, bilateral breath sounds)
7. Secure with tape

First-Generation vs Second-Generation:
- First-gen (Classic, Unique): Lower seal pressure (15-20 cm H2O), no gastric port
- Second-gen (Supreme, ProSeal, i-gel): Higher seal pressure (25-30 cm H2O), gastric port for decompression, lower aspiration risk

Advantages:
- Easier insertion than intubation (success rate >95% first attempt)
- Less hemodynamic response (no laryngoscopy)
- Less airway trauma, sore throat
- Suitable for brief procedures without muscle relaxation
- Effective rescue device in cannot intubate scenario

Disadvantages:
- Aspiration risk higher than tracheal intubation (not a sealed airway)
- Limited to airway pressures <20-25 cm H2O (leak above)
- Malposition possible (epiglottis downfolding, arytenoid obstruction)
- Not suitable for prone or prolonged procedures

Difficult Airway Rescue Role:
- ASA/DAS algorithms place LMA as Plan B after failed intubation
- Allows oxygenation while planning next step (awake, intubate via LMA, surgical airway)
- Success rate >90% when intubation fails
        """,
        key_factors=[
            "SAD sits above glottis, does not enter trachea",
            "Indications: elective short cases, difficult airway rescue",
            "Contraindications: full stomach, morbid obesity, high pressures",
            "Second-generation (Supreme, i-gel) preferred: higher seal, gastric port",
            "Insertion success >95%, allows ventilation up to 20-25 cm H2O",
            "Aspiration risk higher than tracheal intubation"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Management of the Difficult Airway (2022)",
            "Cook TM. NAP4 and the use of supraglottic airways (2011)",
            "Difficult Airway Society Guidelines (2015)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established devices with clear indications and limitations; extensive safety data"
    ),

    # MONITORING
    DoctrineBlock(
        topic="Invasive Arterial Blood Pressure Monitoring",
        keywords=["arterial", "line", "A-line", "radial", "pressure", "waveform", "monitoring"],
        conclusion_template="Invasive arterial monitoring via radial artery catheter provides continuous beat-to-beat blood pressure and arterial blood gas sampling. Indications: major surgery with hemodynamic instability, vasoactive infusions, frequent ABG needs, severe cardiopulmonary disease. Radial artery preferred (Allen test to confirm collateral flow). Complications: thrombosis (rare), hematoma, infection, distal ischemia. Waveform analysis guides fluid responsiveness (pulse pressure variation >13% predicts response).",
        reasoning_framework="""
Indications for Arterial Line:
- Major surgery: cardiac, vascular, neurosurgery, liver transplant
- Hemodynamic instability: septic shock, cardiogenic shock
- Vasoactive infusions (norepinephrine, vasopressin, phenylephrine)
- Severe cardiopulmonary disease (EF <30%, severe COPD)
- Frequent arterial blood gas monitoring needed
- Massive transfusion anticipated

Arterial Cannulation Sites:
- Radial artery (most common): easy access, collateral circulation via ulnar
- Femoral artery: larger vessel, used if radial fails or contraindicated
- Ulnar artery: alternative if radial not available
- Brachial artery: avoid (end-artery, median nerve nearby)
- Dorsalis pedis: alternative in neonates/pediatrics

Radial Artery Technique:
1. Allen test (optional): Confirm ulnar collateral flow by compressing both arteries, releasing ulnar, observe hand reperfusion <7 sec
2. Position wrist in dorsiflexion (rolled towel under wrist)
3. Palpate radial pulse, prep and drape sterile
4. Local anesthesia (1% lidocaine)
5. Insert catheter at 30-45 degree angle, advance until flashback
6. Lower angle to 10-20 degrees, advance catheter over needle
7. Connect to transducer, zero at phlebostatic axis (4th intercostal space, mid-axillary line)
8. Confirm waveform (dicrotic notch visible), flush system
9. Secure with suture/tegaderm

Arterial Waveform Components:
- Systolic upstroke: LV ejection, sharp rise
- Dicrotic notch: Aortic valve closure, marks end of systole
- Diastolic decay: Elastic recoil of aorta, runoff to periphery
- Mean arterial pressure (MAP): Area under curve, best correlate of organ perfusion

Waveform Abnormalities:
- Overdamped (flattened): Air bubble, catheter kink, clot - falsely low systolic
- Underdamped (overshoot): Excessive resonance - falsely high systolic
- Loss of dicrotic notch: Severe hypovolemia, aortic regurgitation
- Pulsus paradoxus: Exaggerated decrease in systolic pressure during inspiration (tamponade, severe asthma)

Pulse Pressure Variation (PPV):
- PPV = (PPmax - PPmin) / mean PP during one respiratory cycle
- PPV >13% predicts fluid responsiveness (positive pressure ventilation)
- Requires: controlled ventilation, tidal volume 8-10 mL/kg, sinus rhythm
- Not valid in spontaneous breathing, arrhythmia, open chest

Complications:
- Thrombosis: 5-10% incidence, usually resolves with catheter removal
- Hematoma: Common, compress site after removal
- Infection: <1%, increase with duration >4 days
- Distal ischemia: Rare with radial (ulnar collateral), monitor hand perfusion
- Pseudoaneurysm: Rare, requires surgical repair if large
- Nerve injury: Avoid brachial site (median nerve proximity)

Advantages:
- Continuous real-time pressure monitoring
- Arterial blood gas sampling without repeated sticks
- Waveform analysis (PPV, SVV) guides fluid therapy
- Immediate detection of hypotension/hypertension

Maintenance:
- Zero transducer before induction, after patient repositioning
- Flush system (3 mL/hr heparinized saline)
- Inspect waveform quality (damping, resonance)
- Remove catheter when no longer needed (minimize infection risk)
        """,
        key_factors=[
            "Indications: major surgery, hemodynamic instability, vasoactive drugs",
            "Radial artery preferred, femoral alternative",
            "Allen test confirms ulnar collateral flow",
            "PPV >13% predicts fluid responsiveness in controlled ventilation",
            "Complications: thrombosis (5-10%), hematoma, infection (<1%)",
            "Zero transducer at phlebostatic axis (4th ICS, mid-axillary)"
        ],
        primary_authority=[
            "ASA Standards for Basic Anesthetic Monitoring (2020)",
            "Michard F. Pulse pressure variation for fluid responsiveness (2005)",
            "O'Rourke et al. Arterial hemodynamics (2012)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard monitoring technique with well-defined indications and safety profile"
    ),

    DoctrineBlock(
        topic="Central Venous Pressure Monitoring",
        keywords=["CVP", "central", "venous", "catheter", "IJ", "subclavian", "pressure", "monitoring"],
        conclusion_template="Central venous catheters (CVC) measure central venous pressure (CVP) and provide large-bore access for vasoactive drugs and fluid resuscitation. Sites: internal jugular (IJ), subclavian, femoral. IJ preferred (lowest complication rate). Ultrasound guidance mandatory (reduces arterial puncture, pneumothorax). CVP normal 2-8 mmHg; trends more useful than absolute values. Complications: pneumothorax (1-2%), arterial puncture, infection.",
        reasoning_framework="""
Indications for CVC:
- CVP monitoring for fluid status (limited utility, trends better than values)
- Large-bore access for rapid volume resuscitation
- Vasoactive infusions (norepinephrine, vasopressin, epinephrine)
- Pulmonary artery catheter placement (need CVC introducer)
- Transvenous pacing wire insertion
- Poor peripheral access
- Prolonged IV therapy (TPN, chemotherapy)

CVC Insertion Sites:
- Internal jugular (IJ): Right preferred (straight path to SVC, no thoracic duct), lower pneumothorax risk than subclavian
- Subclavian: More comfortable for patient, lower infection rate, higher pneumothorax risk (2-3%)
- Femoral: Easiest in emergency, higher infection risk, contraindicated if IVC thrombosis

Right IJ Technique (Ultrasound-Guided):
1. Position: Trendelenburg 10-15 degrees (distend vein, reduce air embolism risk)
2. Ultrasound: Identify IJ (compressible, larger, lateral) vs carotid (pulsatile, medial)
3. Prep and drape sterile, local anesthesia
4. Seldinger technique:
   - Insert needle at 30-45 degrees toward ipsilateral nipple
   - Visualize needle tip entering vein on ultrasound (in-plane or out-of-plane)
   - Flashback of dark venous blood
   - Insert guidewire, remove needle
   - Dilate tract, insert catheter over wire
   - Remove wire, confirm blood return from all ports
   - Secure with suture, sterile dressing
5. Post-procedure CXR to confirm placement, rule out pneumothorax

Ultrasound Guidance Benefits:
- Reduces arterial puncture 50% (3% to 1.5%)
- Reduces pneumothorax (especially IJ)
- Increases first-attempt success 80% vs 50%
- ASA recommends real-time ultrasound for all elective CVC placement

CVP Interpretation:
- Normal: 2-8 mmHg (or 4-12 cm H2O)
- Low (<2 mmHg): Hypovolemia, vasodilation
- High (>12 mmHg): Volume overload, RV failure, tricuspid regurgitation, tamponade, pulmonary hypertension
- CVP trends more useful than single values (response to fluid bolus)
- Poor predictor of fluid responsiveness (multiple studies show weak correlation)

CVP Waveform Components:
- a wave: Atrial contraction (absent in A-fib)
- c wave: Tricuspid valve closure, ventricular contraction
- x descent: Atrial relaxation
- v wave: Atrial filling against closed tricuspid valve
- y descent: Tricuspid valve opening, ventricular filling

CVP Waveform Abnormalities:
- Large a waves: Tricuspid stenosis, pulmonary hypertension, RV failure
- Cannon a waves: AV dissociation (atrium contracts against closed tricuspid)
- Large v waves: Tricuspid regurgitation
- Elevated with blunted descents: Tamponade, constrictive pericarditis

Complications:
- Pneumothorax: 1-2% (IJ), 2-3% (subclavian), immediate CXR required
- Arterial puncture: 5-10% without ultrasound, 1-2% with ultrasound
- Hematoma: Apply pressure if arterial puncture, avoid subclavian (cannot compress)
- Air embolism: Trendelenburg during insertion, occlude hub when removing wire/dilator
- Infection: 2-5% (increases with duration, femoral > IJ > subclavian)
- Arrhythmia: Wire/catheter irritates endocardium, withdraw if PVCs occur
- Guidewire retention: Rare but never-event, confirm wire removal

Catheter Tip Position:
- Ideal: SVC-RA junction (3-5 cm above carina on CXR)
- Too deep: RA or RV (arrhythmia, perforation risk)
- Too shallow: Innominate/subclavian vein (inaccurate CVP, thrombosis)
- Reposition if needed (withdraw, never advance without guidewire)
        """,
        key_factors=[
            "Indications: CVP monitoring, vasoactive drugs, large-bore access",
            "Right IJ preferred (lowest complication rate)",
            "Ultrasound guidance mandatory (reduces complications 50%)",
            "Normal CVP 2-8 mmHg, trends more useful than absolute values",
            "Complications: pneumothorax (1-2%), arterial puncture, infection",
            "Post-insertion CXR confirms placement and rules out pneumothorax"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Central Venous Access (2020)",
            "Marik PE. CVP as a predictor of fluid responsiveness (2009)",
            "McGee DC. Preventing complications of central venous catheterization (2003)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard procedure with clear technique and well-documented complication rates; ultrasound guidance now mandated"
    ),

    # PREOPERATIVE ASSESSMENT
    DoctrineBlock(
        topic="ASA Physical Status Classification",
        keywords=["ASA", "classification", "physical", "status", "risk", "grade", "PS"],
        conclusion_template="ASA Physical Status (PS) classifies preoperative patient health: I (healthy), II (mild systemic disease), III (severe systemic disease), IV (life-threatening disease), V (moribund), VI (brain-dead organ donor). Emergency surgery adds 'E' suffix. ASA PS correlates with perioperative morbidity and mortality: ASA I 0.05%, II 0.4%, III 4.5%, IV 25%, V 50%. Not a surgical risk calculator but informs anesthetic planning.",
        reasoning_framework="""
ASA Physical Status Definitions:
ASA I - Healthy patient
- No organic, physiologic, biochemical abnormality
- Excludes very young, very old
- Examples: Healthy 30-year-old for hernia repair, no medications

ASA II - Mild systemic disease, no functional limitation
- Well-controlled disease without substantive functional limitation
- Examples:
  * Current smoker
  * Social alcohol drinker
  * Pregnancy
  * Obesity (BMI 30-40)
  * Well-controlled hypertension (BP <140/90 on single medication)
  * Well-controlled diabetes (HbA1c <7)
  * Mild COPD (FEV1 >70%)

ASA III - Severe systemic disease, definite functional limitation
- Substantive functional limitation from disease
- Examples:
  * Poorly controlled hypertension (BP >160/100)
  * Poorly controlled diabetes (HbA1c >8)
  * Moderate COPD (FEV1 40-70%)
  * Morbid obesity (BMI >40)
  * Stable angina, remote MI (>3 months)
  * CKD stage 3-4 (GFR 15-60)
  * Heart failure (NYHA II-III)
  * OSA with CPAP compliance

ASA IV - Severe systemic disease, constant threat to life
- Examples:
  * Recent MI (<3 months)
  * Unstable angina
  * Severe COPD (FEV1 <40%)
  * Heart failure (NYHA IV, EF <20%)
  * Symptomatic aortic stenosis
  * Acute renal failure, dialysis-dependent
  * Severe sepsis, septic shock
  * DIC, coagulopathy

ASA V - Moribund, not expected to survive 24 hours with or without surgery
- Examples:
  * Ruptured AAA with shock
  * Massive trauma with polytrauma
  * Severe intracranial hemorrhage with brain herniation
  * Massive pulmonary embolism

ASA VI - Brain-dead organ donor
- For organ procurement only

Emergency Designation ('E'):
- Add 'E' suffix if emergency surgery
- Example: ASA III-E for ruptured appendix in diabetic patient
- Emergency increases risk 2-3 fold at same ASA class

Perioperative Mortality by ASA Class (Historical Data):
- ASA I: 0.05-0.1%
- ASA II: 0.4-0.5%
- ASA III: 4-5%
- ASA IV: 15-25%
- ASA V: 50-75%

Limitations:
- Subjective assessment (inter-rater variability)
- Not a surgical risk calculator (doesn't account for procedure risk)
- Does NOT guide specific management (use for communication, documentation)
- Supplements other risk scores (RCRI, NSQIP, MICA)

Clinical Use:
- Document ASA PS in preanesthetic evaluation
- Informs anesthetic plan (higher ASA = more monitoring, ICU bed)
- Billing/reimbursement tied to ASA PS
- Quality improvement tracking
- Communication among providers
        """,
        key_factors=[
            "ASA I healthy, II mild disease, III severe disease, IV life-threat, V moribund",
            "Emergency surgery adds 'E' suffix (ASA III-E)",
            "Mortality: ASA I 0.05%, II 0.4%, III 4.5%, IV 25%, V 50%",
            "Subjective classification with inter-rater variability",
            "Informs anesthetic planning and resource allocation",
            "Not a surgical risk calculator, supplements other risk tools"
        ],
        primary_authority=[
            "ASA Physical Status Classification System (2020 update)",
            "Dripps RD. New classification of physical status (1963)",
            "Wolters U. ASA classification and perioperative variables (1996)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Universally adopted classification system; extensive validation data despite subjective nature"
    ),

    DoctrineBlock(
        topic="NPO Guidelines and Aspiration Risk",
        keywords=["NPO", "fasting", "aspiration", "full", "stomach", "clear", "liquids"],
        conclusion_template="ASA NPO guidelines minimize aspiration risk: clear liquids 2 hours, breast milk 4 hours, light meal 6 hours, fatty meal 8 hours before anesthesia. Full stomach conditions (recent meal, bowel obstruction, gastroparesis, pregnancy, trauma) require rapid sequence induction. Aspiration incidence 1:7,000 anesthetics, mortality 5% if occurs. Gastric pH <2.5 and volume >25 mL (0.4 mL/kg) define high risk.",
        reasoning_framework="""
ASA NPO Fasting Guidelines (2017):
- Clear liquids: 2 hours (water, black coffee, clear tea, fruit juice without pulp)
- Breast milk: 4 hours
- Infant formula: 6 hours
- Light meal: 6 hours (toast, clear soup)
- Regular/fatty meal: 8 hours (fried foods, meat)
- Chewing gum, candy: Considered clear liquids if dissolved

Rationale:
- Gastric emptying time varies by meal composition
- Liquids empty faster than solids
- Fats delay gastric emptying significantly
- Goal: Empty stomach reduces aspiration risk

High-Risk Full Stomach Conditions:
- Recent meal within fasting interval (trauma, emergency surgery)
- Bowel obstruction (gastric stasis)
- Gastroparesis (diabetes, opioids, chronic renal failure)
- Pregnancy >14 weeks (progesterone relaxes LES, gravid uterus compresses stomach)
- Morbid obesity (increased gastric pressure, GERD)
- Hiatal hernia, GERD (incompetent LES)
- Ileus, ascites

Aspiration Pathophysiology:
- Aspiration = Inhalation of gastric contents into lungs
- Mendelson syndrome: Chemical pneumonitis from acidic gastric juice
- Critical volume: >25 mL or 0.4 mL/kg
- Critical pH: <2.5 (severe injury)
- Particulate matter: Mechanical obstruction, infection

Aspiration Incidence and Outcomes:
- General population: 1:7,000-10,000 anesthetics
- High-risk: 1:1,000-2,000 (emergency, full stomach)
- Mortality: 5% if aspiration occurs (up to 30% in severe cases)
- Morbidity: ARDS, prolonged intubation, ICU stay, pneumonia

Risk Reduction Strategies:
1. Adhere to NPO guidelines for elective surgery
2. Assess risk: History of GERD, delayed gastric emptying
3. Pharmacologic prophylaxis (limited evidence):
   - H2 blocker (ranitidine, famotidine): Increase gastric pH
   - PPI (omeprazole): Increase pH (give 1-2 hours preop)
   - Metoclopramide: Prokinetic, increases LES tone, accelerates emptying
   - Sodium citrate: Neutralize gastric acid (immediately before induction)
4. Rapid sequence induction (RSI) for full stomach (see RSI doctrine)
5. Cricoid pressure (Sellick) controversial (may hinder intubation, efficacy debated)

Aspiration Treatment:
1. Immediate: Suction pharynx, place patient head-down/lateral to drain
2. Intubate trachea, suction via ETT (remove particulates)
3. Bronchoscopy if large particulates suspected
4. Supportive care: Supplemental O2, mechanical ventilation if needed
5. Do NOT lavage (spreads acid, worsens injury)
6. Do NOT give prophylactic antibiotics (no benefit unless infection develops)
7. Monitor for ARDS development (24-48 hours)
8. Chest X-ray: Initial may be normal, infiltrates develop over hours

Special Populations:
- Pediatrics: More compliant with NPO if instructed, same guidelines apply
- Laboring patients: 6-8 hour NPO typically not achievable, RSI if general needed
- Diabetics: Gastroparesis common, consider longer NPO (8-10 hours solids)
        """,
        key_factors=[
            "NPO guidelines: clear liquids 2h, light meal 6h, fatty meal 8h",
            "Full stomach conditions: recent meal, obstruction, pregnancy, gastroparesis",
            "Aspiration risk: volume >25 mL (0.4 mL/kg) and pH <2.5",
            "Incidence 1:7,000, mortality 5% if occurs",
            "RSI technique for full stomach cases",
            "Treatment: suction, intubate, supportive care (no lavage, no prophylactic antibiotics)"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Preoperative Fasting (2017)",
            "Mendelson CL. Aspiration of stomach contents (1946)",
            "Warner MA. Perioperative pulmonary aspiration (1993)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based guidelines with extensive clinical validation; aspiration is rare but serious"
    ),

    # COMPLICATIONS
    DoctrineBlock(
        topic="Malignant Hyperthermia Crisis Management",
        keywords=["malignant", "hyperthermia", "MH", "dantrolene", "succinylcholine", "volatile", "trigger"],
        conclusion_template="Malignant hyperthermia (MH) is a hypermetabolic crisis triggered by volatile anesthetics or succinylcholine in genetically susceptible patients (RYR1 mutation). Presentation: hyperthermia (late sign), hypercarbia (early), muscle rigidity, tachycardia, acidosis. Immediate treatment: stop triggers, hyperventilate 100% O2, dantrolene 2.5 mg/kg IV (repeat to 10 mg/kg), cool patient, treat hyperkalemia. MH cart must be immediately available. Mortality <5% with prompt dantrolene (was 70% pre-dantrolene era).",
        reasoning_framework="""
MH Pathophysiology:
- Genetic defect in RYR1 gene (ryanodine receptor) in 50-70% of cases
- Volatile anesthetics (sevoflurane, desflurane, isoflurane) or succinylcholine trigger
- Uncontrolled calcium release from sarcoplasmic reticulum
- Sustained muscle contraction, hypermetabolism
- Hyperthermia, acidosis, hyperkalemia, rhabdomyolysis

MH Incidence:
- 1:5,000-100,000 anesthetics (variable penetrance)
- Autosomal dominant inheritance (50% transmission)
- More common in males, young muscular patients
- Prior uneventful anesthesia does NOT rule out susceptibility

Early Signs (within 10-20 minutes of trigger exposure):
- Masseter spasm (jaw rigidity after succinylcholine): 50% predictive
- Unexplained tachycardia (HR >100 despite adequate anesthesia)
- Hypercarbia (ETCO2 rising despite increased ventilation)
- Mixed respiratory/metabolic acidosis (PaCO2 >60, pH <7.25)
- Muscle rigidity (generalized, not just masseter)

Late Signs (if untreated):
- Hyperthermia (>38.8°C, rising 1-2°C every 5 min, can reach 46°C)
- Arrhythmias (VT, VF from hyperkalemia)
- Hyperkalemia (>6 mEq/L, peaked T waves, wide QRS)
- Myoglobinuria (tea-colored urine, renal failure risk)
- DIC (consumptive coagulopathy in severe cases)

MH Crisis Management Protocol:
1. CALL FOR HELP - Announce MH crisis, assign roles
2. STOP TRIGGERS - Discontinue volatile agent and/or succinylcholine immediately
3. HYPERVENTILATE - 100% O2 at 10-15 L/min (lower ETCO2)
4. DANTROLENE - 2.5 mg/kg IV rapid bolus (each vial 20 mg in 60 mL sterile water, requires vigorous mixing)
   - Repeat 2.5 mg/kg every 5 min until signs resolve (up to 10 mg/kg initial)
   - May require 20-30 vials (need MH cart immediately accessible)
5. ACTIVE COOLING - Ice packs to groin/axilla/neck, cold IV saline, lavage body cavities if open
6. TREAT HYPERKALEMIA - Insulin 10 units + D50 50 mL, calcium chloride 10 mg/kg IV if arrhythmia
7. TREAT ACIDOSIS - Hyperventilation, sodium bicarbonate 1-2 mEq/kg if pH <7.1
8. MAINTAIN URINE OUTPUT - Fluid bolus, mannitol/furosemide, target UOP >2 mL/kg/h (prevent myoglobin renal injury)
9. MONITOR - Continuous core temp, ETCO2, ABG q15min, electrolytes, CK, myoglobin, coags
10. POST-CRISIS DANTROLENE - 1 mg/kg q6h x 24-48h (recurrence occurs in 25%)

Dantrolene Mechanism:
- Blocks ryanodine receptor (RYR1), stops calcium release
- Only effective treatment for MH
- Side effects: Muscle weakness (expected), phlebitis (give via large vein)
- Reconstitution labor-intensive (each vial needs 60 mL sterile water, shake vigorously)

MH Cart Contents (MHAUS Recommendations):
- Dantrolene 36 vials (720 mg, covers 70 kg patient to 10 mg/kg)
- Sterile water 3,000 mL
- Sodium bicarbonate 50 mEq x10
- Dextrose 50% x10
- Regular insulin 100 units
- Calcium chloride 1g x5
- Lidocaine, amiodarone for arrhythmia
- Mannitol, furosemide for diuresis
- Ice packs, cooling blankets
- ABG syringes, lab tubes
- MH crisis checklist

Post-Crisis Management:
- ICU admission for 24-48h monitoring (recurrence risk 25%)
- Continue dantrolene 1 mg/kg q6h IV
- Monitor CK (may peak at 24-48h, >20,000 common)
- Monitor urine myoglobin, renal function
- Genetic counseling, refer to MH testing center (CHMC, Uniformed Services)
- Advise family members (50% inheritance), provide MH-susceptible wallet card

MH Testing:
- Caffeine-halothane contracture test (CHCT): Gold standard, muscle biopsy required
- Genetic testing: RYR1 mutation in 50-70% (negative does NOT rule out)
- Refer to specialized centers for testing

Safe Anesthesia for MH-Susceptible:
- Avoid triggers: NO volatile agents, NO succinylcholine
- Safe agents: Propofol, benzodiazepines, opioids, rocuronium, vecuronium, nitrous oxide
- Flush anesthesia machine (high-flow O2 >20 min, change soda lime, remove vaporizers)
- Modern machine flushing: 10-20 min sufficient (older machines 90 min)
- Monitor ETCO2, core temp continuously

Mortality:
- Pre-dantrolene era (1960s): 70-80% mortality
- Post-dantrolene (1979-present): <5% mortality with prompt treatment
- Delayed recognition/treatment: 20-30% mortality (emphasizes need for vigilance)
        """,
        key_factors=[
            "MH triggered by volatile anesthetics and succinylcholine in susceptible patients",
            "Early signs: hypercarbia, tachycardia, muscle rigidity (hyperthermia late)",
            "Immediate treatment: stop triggers, dantrolene 2.5 mg/kg (repeat to 10 mg/kg)",
            "Hyperventilate 100% O2, active cooling, treat hyperkalemia/acidosis",
            "MH cart with 36 vials dantrolene must be immediately available",
            "Mortality <5% with prompt treatment (was 70% before dantrolene)"
        ],
        primary_authority=[
            "Malignant Hyperthermia Association of the United States (MHAUS) guidelines",
            "Rosenberg H. Malignant hyperthermia (2015)",
            "ASA Practice Guidelines for MH Crisis Management (2019)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Life-threatening crisis with well-established protocol; dantrolene is definitive treatment with strong evidence"
    ),

    DoctrineBlock(
        topic="Postoperative Nausea and Vomiting (PONV) Prophylaxis",
        keywords=["PONV", "nausea", "vomiting", "ondansetron", "dexamethasone", "Apfel", "prophylaxis"],
        conclusion_template="PONV occurs in 20-30% of surgical patients, up to 70% in high-risk groups. Apfel score predicts risk: female gender, nonsmoker, history of PONV/motion sickness, postoperative opioids (0 factors = 10%, 4 factors = 80% risk). Multimodal prophylaxis: ondansetron 4 mg + dexamethasone 4-8 mg + propofol TIVA + minimize opioids. Rescue treatment with different class agent. PONV increases hospital stay, patient dissatisfaction, and aspiration risk.",
        reasoning_framework="""
PONV Incidence:
- General population: 20-30%
- High-risk patients: 50-80% (laparoscopy, ENT, gynecologic, neurosurgery)
- Pediatric (strabismus, tonsillectomy): 40-50%

Apfel Simplified Risk Score (Each factor = 1 point):
1. Female gender
2. Nonsmoker (smokers have lower PONV, mechanism unclear)
3. History of PONV or motion sickness
4. Postoperative opioids anticipated

Risk Stratification:
- 0 factors: 10% risk (no prophylaxis needed)
- 1 factor: 20% risk (consider single agent)
- 2 factors: 40% risk (2 agents recommended)
- 3 factors: 60% risk (2-3 agents)
- 4 factors: 80% risk (3+ agents, multimodal approach)

Antiemetic Mechanisms and Agents:
1. 5-HT3 Antagonists (Ondansetron, Granisetron):
   - Block serotonin receptors in CTZ and GI tract
   - Ondansetron 4 mg IV at end of surgery (most common)
   - NNT = 6 (6 patients treated to prevent 1 PONV)
   - Side effects: Headache, constipation, QT prolongation (rare at 4 mg)

2. Corticosteroids (Dexamethasone):
   - Dexamethasone 4-8 mg IV at induction (delayed peak effect 2-4h)
   - Mechanism uncertain (prostaglandin inhibition, anti-inflammatory)
   - NNT = 4-5
   - Benefits: Also reduces pain, inflammation
   - Side effects: Hyperglycemia (transient), poor wound healing (single dose unlikely), perineal burning if injected awake

3. NK-1 Antagonists (Aprepitant, Rolapitant):
   - Block substance P in CTZ
   - Aprepitant 40 mg PO preop
   - NNT = 5-6
   - Expensive, reserved for very high risk

4. Anticholinergics (Scopolamine):
   - Transdermal patch applied night before or 4h preop
   - Effective for motion sickness, vestibular surgery
   - NNT = 6
   - Side effects: Dry mouth, blurred vision, sedation

5. Dopamine Antagonists (Droperidol, Metoclopramide):
   - Droperidol 0.625-1.25 mg IV (low dose, was 2.5 mg historically)
   - Black box warning for QT prolongation (dose-related, rare at low dose)
   - NNT = 5
   - Metoclopramide 10 mg IV (also prokinetic)

Multimodal Prophylaxis (Consensus Approach):
- Baseline: Propofol TIVA (reduces PONV vs volatile agents)
- Adequate hydration (1-2 L crystalloid)
- Minimize opioids (use regional anesthesia, NSAIDs, acetaminophen)
- 2 risk factors: Ondansetron 4 mg + dexamethasone 4-8 mg
- 3-4 risk factors: Add scopolamine patch or NK-1 antagonist
- Avoid nitrous oxide (increases PONV 20%)

Timing of Administration:
- Dexamethasone: At induction (delayed effect 2-4h)
- Ondansetron: End of surgery (peak effect 2h)
- Scopolamine patch: 4h preop or night before (transdermal absorption)
- Aprepitant: Preop (oral, slow onset)

Rescue Treatment (PONV despite prophylaxis):
- Use different class than prophylaxis (if ondansetron given, use dexamethasone for rescue)
- Ondansetron 4 mg IV (if not given prophylactically)
- Metoclopramide 10 mg IV
- Promethazine 12.5-25 mg IV (sedating)
- Propofol 10-20 mg IV (off-label, rapid but brief effect)

Non-Pharmacologic Strategies:
- Acupressure (P6 point on wrist): Modest effect, NNT = 10-15
- Aromatherapy (peppermint oil): Limited evidence
- Adequate hydration: 1-2 L crystalloid reduces PONV
- Regional anesthesia: Spinal/epidural reduces opioid need

Consequences of PONV:
- Patient dissatisfaction (PONV rated worse than pain by many patients)
- Delayed discharge, unanticipated admission
- Dehydration, electrolyte imbalance
- Aspiration risk (rare but serious)
- Wound dehiscence (straining)
- Increased healthcare costs

Special Populations:
- Pediatric strabismus/tonsillectomy: Very high risk, multimodal approach
- Laparoscopy: Pneumoperitoneum increases risk
- Gynecologic surgery: Female + opioids = high baseline risk
        """,
        key_factors=[
            "PONV affects 20-30% overall, 70% in high-risk patients",
            "Apfel score: female, nonsmoker, PONV history, opioids (0-4 points)",
            "Prophylaxis: ondansetron 4 mg + dexamethasone 4-8 mg for 2+ risk factors",
            "Multimodal approach: TIVA, hydration, minimize opioids",
            "Rescue with different class agent than prophylaxis",
            "Consequences: delayed discharge, patient dissatisfaction, aspiration risk"
        ],
        primary_authority=[
            "Apfel CC. Simplified risk score for PONV (1999)",
            "Gan TJ. Consensus guidelines for PONV management (2020)",
            "ASA Practice Guidelines for PONV (2020)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Evidence-based risk stratification with well-validated multimodal prophylaxis strategies"
    ),

    # REGIONAL ANESTHESIA
    DoctrineBlock(
        topic="Spinal Anesthesia Technique and Complications",
        keywords=["spinal", "subarachnoid", "intrathecal", "bupivacaine", "PDPH", "hypotension"],
        conclusion_template="Spinal anesthesia delivers local anesthetic into CSF (subarachnoid space) for rapid dense block below level of injection. Indications: lower extremity, pelvic, perineal surgery. Technique: L3-4 or L4-5 interspace, midline or paramedian approach, 25-27G pencil-point needle. Bupivacaine 10-15 mg (isobaric/hyperbaric) provides 2-3 hour block. Complications: hypotension (70%), post-dural puncture headache (1-2% with small needle), high spinal, total spinal (rare).",
        reasoning_framework="""
Spinal Anesthesia Indications:
- Lower extremity surgery: TKA, THA, femur fracture, foot/ankle
- Pelvic surgery: C-section, hysterectomy, bladder, prostate
- Perineal surgery: Hemorrhoidectomy, anal surgery
- Advantages: Dense block, rapid onset, avoids airway instrumentation, reduced blood loss, lower DVT risk

Anatomy:
- Spinal cord ends at L1-2 in adults (L3 in children)
- Cauda equina (nerve roots) below L1-2
- Target: Subarachnoid space (contains CSF, nerve roots)
- Interspace: L3-4 or L4-5 (Tuffier line = top of iliac crest = L4 spinous process)

Spinal Needle Types:
- Pencil-point (Whitacre, Sprotte): Lower PDPH risk (0.5-1%)
- Cutting tip (Quincke): Higher PDPH risk (2-3%)
- Size: 25-27G (smaller = lower PDPH but harder to advance)
- Length: 3.5 inch standard (longer for obese)

Technique (Midline Approach):
1. Position: Sitting or lateral decubitus (sitting easier in obese, lateral for hypotension-prone)
2. Identify L3-4 or L4-5 interspace (palpate iliac crests)
3. Sterile prep, drape, local anesthesia (1% lidocaine 1-2 mL at skin and deeper)
4. Insert introducer needle (18-20G) perpendicular to skin, advance to ligament
5. Insert spinal needle through introducer, slight cephalad angle
6. Advance through ligaments (resistance, then "pop" into subarachnoid space)
7. Remove stylet, confirm CSF flow (clear, dripping freely)
8. Inject local anesthetic slowly (3-5 mL/min), aspirate intermittently
9. Remove needle, place patient supine (or tilted for hyperbaric spread)

Local Anesthetic Choice:
- Bupivacaine 0.5% (isobaric) or 0.75% (hyperbaric with dextrose):
  * Low dose: 7.5-10 mg (saddle block, short procedures)
  * Standard: 10-15 mg (2-3 hour duration, T10 level)
  * High dose: 15-20 mg (longer cases, higher level T4-6)
- Lidocaine 5%: Shorter duration (60-90 min), transient neurologic symptoms (TNS) risk 10-30%
- Chloroprocaine 3%: Shortest duration (45-60 min), low TNS risk

Adjuvants:
- Fentanyl 10-25 mcg: Prolongs block, improves analgesia, minimal side effects
- Morphine 100-200 mcg: Prolonged analgesia (12-24h), respiratory depression risk (late onset 6-12h)
- Epinephrine 100-200 mcg: Prolongs block, controversial (ischemia risk)

Block Characteristics:
- Onset: 5-10 minutes
- Peak: 15-20 minutes
- Duration: 2-3 hours (bupivacaine), 60-90 min (lidocaine)
- Sensory level: T10 typical (bupivacaine 12-15 mg), T4-6 for C-section
- Motor block: Dense (Bromage 3 = complete paralysis)

Complications:
1. Hypotension (50-70%):
   - Mechanism: Sympathetic block, vasodilation, venous pooling
   - Prevention: Preload 500-1000 mL crystalloid, leg elevation, avoid supine
   - Treatment: Phenylephrine 50-100 mcg IV, ephedrine 5-10 mg IV, fluid bolus

2. Post-Dural Puncture Headache (PDPH):
   - Incidence: 1-2% (25-27G pencil-point), 5-10% (22G Quincke)
   - Onset: 24-48 hours post-spinal
   - Character: Frontal/occipital, worsens upright, improves supine
   - Mechanism: CSF leak through dural hole, traction on meninges
   - Treatment: Hydration, caffeine, analgesics; epidural blood patch if severe (15-20 mL autologous blood)

3. High/Total Spinal:
   - High spinal: Block above T4, dyspnea, weak hand grip, Horner syndrome
   - Total spinal: C1-2 block, apnea, unconsciousness, cardiovascular collapse
   - Treatment: Intubate, ventilate, vasopressor support (resolves in 1-2 hours)

4. Bradycardia:
   - Mechanism: Unopposed vagal tone (sympathetic block T1-4)
   - Treatment: Atropine 0.5 mg IV, glycopyrrolate 0.2 mg IV

5. Urinary retention:
   - Common (20-30%), sacral nerve block impairs bladder function
   - Foley catheter if >6 hours anticipated or bladder distended

6. Transient Neurologic Symptoms (TNS):
   - Incidence: 10-30% with lidocaine, <1% with bupivacaine
   - Onset: 24 hours, resolves 48-72 hours
   - Pain in buttocks/legs, no sensory/motor deficit
   - Treatment: NSAIDs, supportive

Contraindications:
- Absolute: Patient refusal, infection at site, coagulopathy (INR >1.5, plt <50K), severe hypovolemia, increased ICP
- Relative: Stenotic valvular disease (AS, MS), severe spinal deformity, prior back surgery
        """,
        key_factors=[
            "Spinal anesthesia: local anesthetic into CSF at L3-4 or L4-5",
            "Bupivacaine 10-15 mg provides 2-3 hour dense block",
            "25-27G pencil-point needle reduces PDPH risk to 1-2%",
            "Hypotension most common complication (50-70%), treat with phenylephrine/fluid",
            "PDPH treated with hydration, caffeine, epidural blood patch if severe",
            "High/total spinal rare but life-threatening, requires ventilatory support"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Obstetric Anesthesia (2016)",
            "Turnbull DK. Post-dural puncture headache (2003)",
            "Horlocker TT. Regional anesthesia and anticoagulation (2018)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extensively studied technique with well-defined complications and management; PDPH incidence data robust"
    ),

    DoctrineBlock(
        topic="Epidural Anesthesia and Labor Analgesia",
        keywords=["epidural", "catheter", "labor", "analgesia", "bupivacaine", "fentanyl", "PCEA"],
        conclusion_template="Epidural anesthesia places catheter in epidural space for continuous or intermittent local anesthetic delivery. Labor epidural: bupivacaine 0.0625-0.125% + fentanyl 2 mcg/mL, patient-controlled epidural analgesia (PCEA) for titration. Indications: labor pain, postoperative analgesia, chronic pain. Complications: hypotension (10-20%), dural puncture (1%), epidural hematoma (1:150,000), abscess (rare). Test dose (lidocaine 3 mL with epi 1:200,000) detects intrathecal/IV placement.",
        reasoning_framework="""
Epidural Anatomy:
- Epidural space: Potential space between ligamentum flavum and dura mater
- Contains: Fat, blood vessels, nerve roots exiting dura
- Depth from skin: 3-6 cm (varies with body habitus)
- Target: Lumbar epidural (L2-3, L3-4, L4-5) for labor/lower extremity

Epidural Technique (Loss of Resistance):
1. Position: Sitting or lateral decubitus
2. Identify interspace (L3-4 for labor)
3. Sterile prep, drape, local anesthesia
4. Insert Tuohy needle (17-18G) at midline or paramedian
5. Advance through subcutaneous tissue, ligaments
6. Loss of resistance (LOR): Continuous pressure on saline/air-filled syringe, sudden loss of resistance = epidural space
7. Thread catheter 3-5 cm into epidural space
8. Remove needle, secure catheter, apply filter
9. Test dose: Lidocaine 3 mL with epi 1:200,000 (detects intrathecal = rapid dense block within 3 min, IV = tachycardia >20 bpm increase)

Labor Epidural Protocol:
- Loading dose: Bupivacaine 0.125% or ropivacaine 0.1% 10-15 mL + fentanyl 50-100 mcg
- Maintenance: PCEA (patient-controlled epidural analgesia):
  * Basal rate: 8-10 mL/h of bupivacaine 0.0625% + fentanyl 2 mcg/mL
  * Bolus: 5 mL, lockout 10-15 min
  * Allows patient to titrate, reduces motor block, improves satisfaction

Epidural vs Spinal:
- Epidural: Slower onset (15-20 min), titratable, catheter allows continuous infusion, less hypotension
- Spinal: Rapid onset (5 min), single shot (no catheter), denser block, more hypotension

Advantages of Epidural for Labor:
- Superior analgesia compared to systemic opioids
- Motor function preserved (walking epidural with low-concentration bupivacaine)
- Titratable to pain level
- Can be used for C-section if needed (increase concentration)
- Maternal satisfaction high

Complications:
1. Hypotension (10-20%):
   - Less severe than spinal (slower onset, less sympathetic block)
   - Treatment: Left lateral tilt, IV fluid, phenylephrine 50-100 mcg PRN

2. Inadequate block (10-15%):
   - Unilateral block: Withdraw catheter 1-2 cm, rebolus, patient positioning
   - Patchy block: May need replacement

3. Dural puncture (1-2%):
   - Accidental entry into subarachnoid space with Tuohy needle
   - Larger hole than spinal needle → PDPH risk 50-80%
   - Options: Thread catheter intrathecally (continuous spinal), replace at different level
   - Prophylactic epidural blood patch 24h post-delivery reduces PDPH

4. Total spinal:
   - Intrathecal injection of full epidural dose (15-20 mL local anesthetic)
   - Apnea, hypotension, unconsciousness
   - Treatment: Intubate, ventilate, vasopressor support

5. Local anesthetic systemic toxicity (LAST):
   - IV injection of large dose (test dose helps prevent)
   - CNS: Tinnitus, seizures
   - Cardiac: Arrhythmia, cardiac arrest (bupivacaine more cardiotoxic than ropivacaine)
   - Treatment: Intralipid 20% 1.5 mL/kg bolus, then infusion

6. Epidural hematoma (1:150,000):
   - Risk factors: Anticoagulation, thrombocytopenia
   - Presentation: Back pain, progressive leg weakness, bladder/bowel dysfunction
   - Emergency MRI, neurosurgery consult (decompressive laminectomy within 8h)

7. Epidural abscess (1:500,000):
   - Risk factors: Prolonged catheter (>72h), immunosuppression
   - Presentation: Fever, back pain, neurologic deficit
   - Treatment: MRI, antibiotics, surgical drainage

Contraindications:
- Absolute: Patient refusal, infection at site, coagulopathy (plt <70K for labor, INR >1.5), severe hypovolemia
- Relative: Prior back surgery, spinal deformity, demyelinating disease

Anticoagulation Timing (ASRA Guidelines):
- Aspirin/NSAIDs: Safe to proceed
- Heparin: 4-6 hours since last dose (PTT normal)
- LMWH prophylactic: 12 hours since last dose
- LMWH therapeutic: 24 hours since last dose
- Warfarin: INR <1.5
- DOACs (apixaban, rivaroxaban): 3 days since last dose
- Removal timing: Same intervals apply to catheter removal
        """,
        key_factors=[
            "Epidural: catheter in epidural space for continuous analgesia",
            "Labor epidural: bupivacaine 0.0625-0.125% + fentanyl 2 mcg/mL via PCEA",
            "Test dose (lidocaine + epi) detects intrathecal/IV placement",
            "Complications: hypotension (10-20%), dural puncture (1%), PDPH, hematoma (rare)",
            "Superior labor analgesia with preserved motor function",
            "Contraindicated in coagulopathy (plt <70K, INR >1.5)"
        ],
        primary_authority=[
            "ASA Practice Guidelines for Obstetric Anesthesia (2016)",
            "ASRA Guidelines on Regional Anesthesia and Anticoagulation (2018)",
            "Simmons SW. Combined spinal-epidural vs epidural analgesia in labor (2012)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gold standard for labor analgesia with extensive safety and efficacy data; hematoma risk low but catastrophic"
    ),

    DoctrineBlock(
        topic="Ultrasound-Guided Regional Anesthesia and Nerve Blocks",
        keywords=["ultrasound", "nerve", "block", "regional", "femoral", "sciatic", "brachial", "plexus"],
        conclusion_template="Ultrasound guidance improves success rate, reduces complications, and decreases local anesthetic volume for peripheral nerve blocks. Common blocks: interscalene (shoulder), supraclavicular (arm/forearm), femoral (anterior thigh), sciatic (posterior leg/foot). Technique: high-frequency linear probe identifies nerve, in-plane or out-of-plane needle approach, inject 15-30 mL local anesthetic circumferentially. Benefits: Real-time visualization, avoid vascular puncture, reduce LAST risk. Ropivacaine or bupivacaine 0.25-0.5% typical.",
        reasoning_framework="""
Ultrasound-Guided Regional Anesthesia Advantages:
- Higher success rate (90-95% vs 70-80% landmark technique)
- Faster onset (direct deposition around nerve)
- Lower local anesthetic volume (reduced LAST risk)
- Avoid vascular puncture (visualize vessels, Color Doppler)
- Real-time needle visualization (reduce nerve trauma)

Ultrasound Equipment:
- High-frequency linear probe (10-15 MHz): Superficial structures (interscalene, femoral)
- Low-frequency curvilinear probe (2-5 MHz): Deep structures (sciatic, lumbar plexus)
- Needle visibility: Echogenic needles, steep angle improves reflection

Common Upper Extremity Blocks:
1. Interscalene Block (Shoulder, Proximal Humerus):
   - Target: Brachial plexus C5-7 roots between anterior and middle scalene muscles
   - Level: Cricoid cartilage (C6 transverse process)
   - Dose: 15-20 mL ropivacaine 0.5%
   - Complications: Phrenic nerve block (100%, ipsilateral diaphragm paralysis), Horner syndrome, recurrent laryngeal nerve block
   - Avoid in severe COPD, bilateral blocks

2. Supraclavicular Block (Arm, Forearm, Hand):
   - Target: Brachial plexus trunks/divisions above clavicle, lateral to subclavian artery
   - Appearance: "Cluster of grapes" hypoechoic circles
   - Dose: 20-30 mL ropivacaine 0.5%
   - Complications: Pneumothorax (1-2%, lower with ultrasound), phrenic nerve block (50%)

3. Axillary Block (Forearm, Hand):
   - Target: Terminal nerves (median, radial, ulnar, musculocutaneous) around axillary artery
   - Multiple injections or single injection high volume
   - Dose: 30-40 mL total ropivacaine 0.5%
   - Low complication rate (no phrenic, no pneumothorax)

Common Lower Extremity Blocks:
1. Femoral Nerve Block (Anterior Thigh, Knee):
   - Target: Femoral nerve lateral to femoral artery, below inguinal ligament
   - Appearance: Hyperechoic triangle lateral to artery
   - Dose: 20-30 mL ropivacaine 0.5%
   - Indications: TKA, femur fracture, anterior thigh surgery
   - Complications: Quadriceps weakness (fall risk), avoid bilateral in ambulatory

2. Sciatic Nerve Block (Posterior Leg, Foot, Ankle):
   - Target: Sciatic nerve in popliteal fossa (divides into tibial and common peroneal)
   - Level: 7-10 cm above popliteal crease
   - Dose: 20-30 mL ropivacaine 0.5%
   - Indications: Foot/ankle surgery, below-knee amputation, complement to femoral block

3. Adductor Canal Block (ACB) / Saphenous Nerve Block:
   - Target: Saphenous nerve in adductor canal (mid-thigh medial)
   - Purely sensory block (preserves quadriceps strength vs femoral block)
   - Dose: 15-20 mL ropivacaine 0.2-0.5%
   - Indications: TKA (preferred over femoral to preserve strength, reduce fall risk)

Truncal Blocks (Increasingly Popular):
1. Transversus Abdominis Plane (TAP) Block:
   - Target: Plane between internal oblique and transversus abdominis
   - Indications: Abdominal surgery (laparotomy, C-section, hernia)
   - Dose: 20 mL per side ropivacaine 0.2-0.5%

2. Erector Spinae Plane (ESP) Block:
   - Target: Plane deep to erector spinae muscle, superficial to transverse processes
   - Indications: Thoracic/abdominal surgery, rib fractures, herpes zoster pain
   - Dose: 20-30 mL ropivacaine 0.2-0.5%

Nerve Block Technique (General):
1. Patient positioning (expose target area)
2. Ultrasound probe in sterile sleeve, gel applied
3. Identify nerve (hypoechoic structure, honeycomb fascicular pattern)
4. Identify surrounding structures (arteries, veins with Color Doppler)
5. Needle approach: In-plane (long-axis view, entire needle visible) or out-of-plane (short-axis, needle tip only)
6. Advance needle to nerve proximity (1-2 mm away, do NOT contact nerve)
7. Aspirate (confirm not intravascular)
8. Inject 1-2 mL test dose, observe spread (should outline nerve, "donut sign")
9. Inject remaining local anesthetic in divided doses, aspirate q5mL
10. Confirm circumferential spread around nerve

Local Anesthetic Choice:
- Ropivacaine 0.5%: 12-18 hour duration, less cardiotoxic than bupivacaine
- Bupivacaine 0.25-0.5%: 12-24 hour duration, more cardiotoxic
- Lidocaine 1-2%: 2-4 hour duration (with epi 1:200,000)
- Liposomal bupivacaine (Exparel): 72-96 hour duration, expensive

Adjuvants:
- Dexamethasone 4-8 mg: Prolongs block 4-6 hours
- Dexmedetomidine 0.5-1 mcg/kg: Prolongs block, less evidence than dexamethasone

Complications:
- Local anesthetic systemic toxicity (LAST): Rare with ultrasound (<1:10,000)
- Nerve injury: Rare (1:5,000-10,000), minimized by avoiding intraneural injection
- Vascular puncture: Reduced with ultrasound, Color Doppler
- Infection: Rare with sterile technique
- Block failure: 5-10% (lower with ultrasound vs landmark)
        """,
        key_factors=[
            "Ultrasound guidance improves success (90-95%), reduces complications",
            "Common blocks: interscalene (shoulder), femoral (knee), sciatic (foot)",
            "In-plane or out-of-plane needle approach, circumferential spread around nerve",
            "Ropivacaine 0.5% or bupivacaine 0.25-0.5%, 15-30 mL typical dose",
            "Benefits: Real-time visualization, avoid vessels, reduce LAST risk",
            "Complications rare with ultrasound: LAST <1:10,000, nerve injury 1:5,000-10,000"
        ],
        primary_authority=[
            "ASRA Guidelines on Ultrasound-Guided Regional Anesthesia (2016)",
            "Sites BD. Ultrasound guidance reduces complications (2014)",
            "Neal JM. ASRA Practice Advisory on Neurologic Complications (2015)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Ultrasound guidance is now standard of care with strong evidence for improved outcomes"
    ),

]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class AnesthesiologyTelemetry:
    """Comprehensive query telemetry tracking"""

    def __init__(self):
        self.queries_total = 0
        self.queries_by_mode: Dict[ResponseMode, int] = defaultdict(int)
        self.queries_by_category: Dict[IssueCategory, int] = defaultdict(int)
        self.latencies: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors: List[str] = []
        self.triggered_doctrines: Counter = Counter()
        self.start_time = time.time()

    def record_query(
        self,
        mode: ResponseMode,
        category: Optional[IssueCategory],
        latency_ms: float,
        cache_hit: bool,
        doctrines_triggered: List[str],
        error: Optional[str] = None
    ):
        """Record query metrics"""
        self.queries_total += 1
        self.queries_by_mode[mode] += 1
        if category:
            self.queries_by_category[category] += 1
        self.latencies.append(latency_ms)

        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        for doctrine in doctrines_triggered:
            self.triggered_doctrines[doctrine] += 1

        if error:
            self.errors.append(error)

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics"""
        uptime = time.time() - self.start_time
        cache_total = self.cache_hits + self.cache_misses

        return {
            "queries_total": self.queries_total,
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_category": dict(self.queries_by_category),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            "p50_latency_ms": sorted(self.latencies)[len(self.latencies) // 2] if self.latencies else 0,
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0,
            "cache_hit_rate": self.cache_hits / cache_total if cache_total > 0 else 0,
            "error_count": len(self.errors),
            "top_doctrines": dict(self.triggered_doctrines.most_common(10)),
            "uptime_seconds": uptime
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class AnesthesiologyEngine:
    """MED11 Anesthesiology Intelligence Engine - TIE-20 Compliant"""

    def __init__(self):
        self.telemetry = AnesthesiologyTelemetry()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"
        logger.info(f"MED11 Anesthesiology Engine initialized with {len(DOCTRINE_CACHE)} doctrines")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: Optional[AnalysisZone],
        patient_context: Optional[Dict[str, Any]]
    ) -> Tuple[str, List[str], ConfidenceLevel, str, float]:
        """
        Three-layer response architecture:
        Layer 1: Doctrine cache (0-50ms)
        Layer 2: Semantic search (50-200ms)
        Layer 3: Deep analysis with context (200ms+)
        """
        start_time = time.time()

        # Layer 1: Doctrine Cache
        cache_results = self._search_doctrine_cache(query)
        if cache_results and cache_results[0][1] > 2.0:
            doctrine, score = cache_results[0]
            latency_ms = (time.time() - start_time) * 1000

            answer = self._format_response(
                doctrine=doctrine,
                mode=mode,
                zone=zone,
                patient_context=patient_context,
                query=query
            )

            confidence, stratification = self._assess_confidence(doctrine, patient_context)

            self.telemetry.record_query(
                mode=mode,
                category=self._categorize_query(query),
                latency_ms=latency_ms,
                cache_hit=True,
                doctrines_triggered=[doctrine.topic]
            )

            return answer, [doctrine.topic], confidence, stratification, latency_ms

        # Layer 2: Semantic normalization + multi-doctrine
        triggered = [d[0] for d in cache_results[:3]] if cache_results else []

        if triggered:
            answer = self._synthesize_multi_doctrine(
                doctrines=triggered,
                query=query,
                mode=mode,
                zone=zone,
                patient_context=patient_context
            )

            confidence, stratification = self._aggregate_confidence(triggered, patient_context)
            latency_ms = (time.time() - start_time) * 1000

            self.telemetry.record_query(
                mode=mode,
                category=self._categorize_query(query),
                latency_ms=latency_ms,
                cache_hit=False,
                doctrines_triggered=[d.topic for d in triggered]
            )

            return answer, [d.topic for d in triggered], confidence, stratification, latency_ms

        # Layer 3: Deep analysis (no doctrine match)
        answer = self._deep_analysis(query, mode, zone, patient_context)
        latency_ms = (time.time() - start_time) * 1000

        self.telemetry.record_query(
            mode=mode,
            category=self._categorize_query(query),
            latency_ms=latency_ms,
            cache_hit=False,
            doctrines_triggered=[]
        )

        return answer, [], ConfidenceLevel.DISCLOSURE, "No doctrine match, general principles applied", latency_ms

    def _search_doctrine_cache(self, query: str) -> List[Tuple[DoctrineBlock, float]]:
        """Search doctrine cache with scoring"""
        results = []
        for doctrine in DOCTRINE_CACHE:
            score = doctrine.matches(query)
            if score > 0:
                results.append((doctrine, score))

        return sorted(results, key=lambda x: x[1], reverse=True)

    def _format_response(
        self,
        doctrine: DoctrineBlock,
        mode: ResponseMode,
        zone: Optional[AnalysisZone],
        patient_context: Optional[Dict[str, Any]],
        query: str
    ) -> str:
        """Format response based on mode"""

        if mode == ResponseMode.FAST:
            return doctrine.conclusion_template

        elif mode == ResponseMode.DEFENSE:
            context_note = ""
            if patient_context:
                context_note = f"\n\nPatient Context: {json.dumps(patient_context, indent=2)}"

            return f"""ANESTHESIOLOGY ANALYSIS - DEFENSE MODE

Query: {query}

CONCLUSION:
{doctrine.conclusion_template}

REASONING FRAMEWORK:
{doctrine.reasoning_framework}

KEY FACTORS:
{chr(10).join(f'- {factor}' for factor in doctrine.key_factors)}

PRIMARY AUTHORITY:
{chr(10).join(f'- {auth}' for auth in doctrine.primary_authority)}

CONFIDENCE: {doctrine.confidence.value}
STRATIFICATION: {doctrine.confidence_stratification}
{context_note}

DISCLOSURE: This analysis is based on general anesthesiology principles and available evidence. Individual patient management should be determined by the treating anesthesiologist based on full clinical assessment, institutional protocols, and current guidelines. This is not a substitute for clinical judgment.
"""

        else:  # MEMO
            context_note = ""
            if patient_context:
                context_note = f"\n\nPATIENT-SPECIFIC CONTEXT:\n{json.dumps(patient_context, indent=2)}"

            zone_note = f"\n\nANALYSIS ZONE: {zone.value}" if zone else ""

            return f"""COMPREHENSIVE ANESTHESIOLOGY MEMORANDUM

QUERY: {query}

EXECUTIVE SUMMARY:
{doctrine.conclusion_template}

DETAILED REASONING FRAMEWORK:
{doctrine.reasoning_framework}

KEY CLINICAL FACTORS:
{chr(10).join(f'{i+1}. {factor}' for i, factor in enumerate(doctrine.key_factors))}

AUTHORITATIVE SOURCES:
{chr(10).join(f'{i+1}. {auth}' for i, auth in enumerate(doctrine.primary_authority))}

COUNTER-ARGUMENTS AND LIMITATIONS:
{chr(10).join(f'- {arg}' for arg in doctrine.counter_arguments) if doctrine.counter_arguments else '- None identified'}

RESOLUTION STRATEGY: {doctrine.resolution_strategy}

ENTITY SCOPE: {doctrine.entity_scope}
BURDEN HOLDER: {doctrine.burden_holder}
ADVERSARY POSITION: {doctrine.adversary_position}

CONFIDENCE ASSESSMENT:
Level: {doctrine.confidence.value}
Stratification: {doctrine.confidence_stratification}
Fact Fragility Score: {doctrine.fact_fragility:.2f}

CONTROLLING PRECEDENT: {doctrine.controlling_precedent}
{context_note}
{zone_note}

EPISTEMIC GUARDRAILS:
This analysis synthesizes current anesthesiology evidence and guidelines. Clinical practice evolves with new research. Individual patient care requires comprehensive assessment including patient history, physical examination, laboratory data, and multidisciplinary consultation. This memorandum is for educational and decision-support purposes only.

FINAL DISCLOSURE:
Anesthesia management involves significant clinical judgment based on patient-specific factors, surgical requirements, and institutional resources. This analysis provides a framework but does not replace the expertise of a board-certified anesthesiologist. Always consult current ASA guidelines, institutional protocols, and specialist consultation as appropriate.
"""

    def _synthesize_multi_doctrine(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: Optional[AnalysisZone],
        patient_context: Optional[Dict[str, Any]]
    ) -> str:
        """Synthesize multiple triggered doctrines"""

        if mode == ResponseMode.FAST:
            return f"Multiple relevant considerations: {', '.join(d.topic for d in doctrines)}. " + doctrines[0].conclusion_template

        synthesis = f"MULTI-DOCTRINE ANESTHESIOLOGY ANALYSIS\n\nQuery: {query}\n\n"
        synthesis += f"Triggered Doctrines: {', '.join(d.topic for d in doctrines)}\n\n"

        for i, doctrine in enumerate(doctrines, 1):
            synthesis += f"DOCTRINE {i}: {doctrine.topic}\n"
            synthesis += f"{doctrine.conclusion_template}\n\n"

        synthesis += "INTEGRATED REASONING:\n"
        synthesis += f"{doctrines[0].reasoning_framework}\n\n"

        synthesis += "COMBINED KEY FACTORS:\n"
        all_factors = []
        for d in doctrines:
            all_factors.extend(d.key_factors)
        for factor in all_factors[:10]:
            synthesis += f"- {factor}\n"

        if patient_context:
            synthesis += f"\nPatient Context: {json.dumps(patient_context, indent=2)}\n"

        if zone:
            synthesis += f"\nAnalysis Zone: {zone.value}\n"

        synthesis += "\nDISCLOSURE: This multi-doctrine analysis synthesizes related anesthesiology principles. Clinical application requires comprehensive patient assessment and specialist judgment."

        return synthesis

    def _deep_analysis(
        self,
        query: str,
        mode: ResponseMode,
        zone: Optional[AnalysisZone],
        patient_context: Optional[Dict[str, Any]]
    ) -> str:
        """Deep analysis when no doctrine matches"""

        return f"""ANESTHESIOLOGY DEEP ANALYSIS

Query: {query}

ANALYSIS:
The query did not match specific doctrine blocks in the anesthesiology knowledge base. This may indicate:

1. Novel or emerging clinical scenario not yet codified in standard protocols
2. Highly patient-specific situation requiring individualized assessment
3. Query outside the primary scope of anesthesiology practice
4. Need for consultation with subspecialist (e.g., cardiac anesthesia, obstetric anesthesia, pediatric anesthesia, pain medicine)

GENERAL ANESTHESIOLOGY PRINCIPLES:
- Comprehensive preoperative assessment (ASA classification, NPO status, airway evaluation)
- Informed consent discussing risks, benefits, alternatives
- Appropriate monitoring per ASA standards (pulse oximetry, NIBP, ECG, capnography, temperature)
- Anesthetic plan tailored to patient factors, surgical requirements, institutional resources
- Vigilance and preparedness for complications (malignant hyperthermia, aspiration, difficult airway, hemodynamic instability)
- Postoperative care including pain management, PONV prophylaxis, and appropriate monitoring level

RECOMMENDED APPROACH:
- Review ASA Practice Guidelines relevant to the clinical scenario
- Consult institutional protocols and departmental expertise
- Consider multidisciplinary team discussion (surgery, medicine, critical care)
- Literature search for recent evidence if novel scenario
- Document decision-making process and informed consent

Patient Context: {json.dumps(patient_context, indent=2) if patient_context else 'None provided'}
Analysis Zone: {zone.value if zone else 'Not specified'}

DISCLOSURE:
This deep analysis provides general anesthesiology principles in the absence of specific doctrine guidance. Clinical management should be individualized based on comprehensive patient evaluation, specialist consultation, and current evidence-based guidelines. This is not a substitute for expert clinical judgment.
"""

    def _assess_confidence(
        self,
        doctrine: DoctrineBlock,
        patient_context: Optional[Dict[str, Any]]
    ) -> Tuple[ConfidenceLevel, str]:
        """Assess confidence based on doctrine and context"""

        base_confidence = doctrine.confidence
        stratification = doctrine.confidence_stratification

        if patient_context:
            complexity_factors = patient_context.get("complexity_factors", [])
            if len(complexity_factors) > 3:
                if base_confidence == ConfidenceLevel.DEFENSIBLE:
                    base_confidence = ConfidenceLevel.AGGRESSIVE
                    stratification += " Patient complexity reduces certainty."

        return base_confidence, stratification

    def _aggregate_confidence(
        self,
        doctrines: List[DoctrineBlock],
        patient_context: Optional[Dict[str, Any]]
    ) -> Tuple[ConfidenceLevel, str]:
        """Aggregate confidence across multiple doctrines"""

        if not doctrines:
            return ConfidenceLevel.DISCLOSURE, "No doctrine match"

        confidences = [d.confidence for d in doctrines]

        if ConfidenceLevel.HIGH_RISK in confidences:
            return ConfidenceLevel.HIGH_RISK, "High-risk factors present in doctrine set"
        elif ConfidenceLevel.DISCLOSURE in confidences:
            return ConfidenceLevel.DISCLOSURE, "Significant uncertainty in doctrine set"
        elif ConfidenceLevel.AGGRESSIVE in confidences:
            return ConfidenceLevel.AGGRESSIVE, "Moderate certainty with multiple doctrines"
        else:
            return ConfidenceLevel.DEFENSIBLE, "Multiple defensible doctrines support conclusion"

    def _categorize_query(self, query: str) -> Optional[IssueCategory]:
        """Categorize query into issue type"""
        query_lower = query.lower()

        if any(kw in query_lower for kw in ["general", "induction", "maintenance", "emergence", "volatile", "mac"]):
            return IssueCategory.GENERAL_ANESTHESIA
        elif any(kw in query_lower for kw in ["spinal", "epidural", "regional", "nerve block", "ultrasound"]):
            return IssueCategory.REGIONAL_ANESTHESIA
        elif any(kw in query_lower for kw in ["airway", "intubation", "difficult", "mallampati", "lma"]):
            return IssueCategory.AIRWAY_MANAGEMENT
        elif any(kw in query_lower for kw in ["propofol", "succinylcholine", "rocuronium", "dantrolene", "drug"]):
            return IssueCategory.PHARMACOLOGY
        elif any(kw in query_lower for kw in ["monitoring", "arterial line", "cvp", "pressure", "a-line"]):
            return IssueCategory.MONITORING
        elif any(kw in query_lower for kw in ["preoperative", "asa", "npo", "fasting", "assessment"]):
            return IssueCategory.PREOPERATIVE
        elif any(kw in query_lower for kw in ["malignant hyperthermia", "ponv", "aspiration", "complication"]):
            return IssueCategory.COMPLICATIONS
        elif any(kw in query_lower for kw in ["pediatric", "child", "infant", "neonate"]):
            return IssueCategory.PEDIATRIC
        elif any(kw in query_lower for kw in ["obstetric", "labor", "epidural", "c-section", "pregnancy"]):
            return IssueCategory.OBSTETRIC
        elif any(kw in query_lower for kw in ["cardiac", "heart", "cabg", "valve"]):
            return IssueCategory.CARDIAC
        elif any(kw in query_lower for kw in ["neurosurgical", "craniotomy", "brain", "icp"]):
            return IssueCategory.NEUROSURGICAL
        elif any(kw in query_lower for kw in ["pain", "analgesia", "chronic", "acute"]):
            return IssueCategory.PAIN_MANAGEMENT

        return None

    def calculate_determinism_hash(self, query: str, answer: str) -> str:
        """SHA-256 hash for reproducibility verification"""
        content = f"{query}|||{answer}"
        return hashlib.sha256(content.encode()).hexdigest()

    def log_audit_trail(self, query: str, response: Dict[str, Any]):
        """Append-only audit trail in JSONL format"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "response": response,
            "determinism_hash": self.calculate_determinism_hash(query, response.get("answer", ""))
        }

        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="MED11 Anesthesiology Intelligence Engine",
    version="1.0.0",
    description="TIE-grade anesthesiology analysis engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AnesthesiologyEngine()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "engine": "MED11 Anesthesiology Intelligence Engine",
        "version": "1.0.0",
        "status": "operational",
        "doctrines": str(len(DOCTRINE_CACHE))
    }


@app.post("/query", response_model=QueryResponse)
async def query_anesthesiology(request: QueryRequest):
    """
    Anesthesiology query endpoint

    Supports three response modes:
    - FAST: Rapid conclusion only
    - DEFENSE: Detailed reasoning with authorities
    - MEMO: Comprehensive memorandum format
    """
    try:
        answer, triggered, confidence, stratification, latency = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            patient_context=request.patient_context
        )

        response_data = QueryResponse(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            answer=answer,
            triggered_doctrines=triggered,
            confidence=confidence,
            stratification_reason=stratification,
            determinism_hash=engine.calculate_determinism_hash(request.query, answer),
            latency_ms=latency,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        engine.log_audit_trail(request.query, response_data.dict())

        return response_data

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check"""
    metrics = engine.telemetry.get_metrics()

    return HealthResponse(
        status="healthy",
        engine="MED11_Anesthesiology",
        version="1.0.0",
        port=9311,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=metrics["uptime_seconds"],
        queries_processed=metrics["queries_total"],
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["cache_hit_rate"]
    )


@app.get("/doctrines", response_model=Dict[str, Any])
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "entity_scope": d.entity_scope
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/metrics", response_model=Dict[str, Any])
async def get_metrics():
    """Get detailed engine metrics"""
    return engine.telemetry.get_metrics()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting MED11 Anesthesiology Intelligence Engine on port 9311")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info("TIE-20 compliant: three_layer_response, doctrine_cache, telemetry, audit_trail, health_endpoint")

    uvicorn.run(app, host="0.0.0.0", port=9311)
