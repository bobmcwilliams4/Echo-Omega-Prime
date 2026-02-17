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
        topic="Stages of General Anesthesia",
        keywords=["anesthesia", "stages", "induction", "maintenance", "emergence", "depth"],
        conclusion_template="General anesthesia progresses through four stages: induction, maintenance, emergence, and recovery.",
        reasoning_framework=(
            "The stages of general anesthesia are defined by clinical signs and physiological responses. "
            "Stage I (Analgesia) begins with administration of anesthetic agents and ends with loss of consciousness. "
            "Stage II (Excitement) is characterized by irregular respiration, involuntary movements, and heightened reflexes; "
            "this stage is minimized by rapid induction. Stage III (Surgical Anesthesia) is subdivided into four planes, "
            "with progressive muscle relaxation, loss of reflexes, and stable vital signs. Stage IV (Overdose) is marked by "
            "respiratory and cardiovascular depression, requiring immediate intervention. Monitoring depth of anesthesia "
            "is essential to avoid awareness or excessive depression. Clinical signs, end-tidal anesthetic concentration, "
            "and EEG-based monitors (e.g., BIS) guide assessment. The anesthesiologist must balance adequate anesthesia "
            "with patient safety, adjusting agents as needed based on surgical stimulus and patient response."
        ),
        key_factors=[
            "Patient response to anesthetic agents",
            "Vital signs",
            "Clinical signs (movement, reflexes)",
            "Depth monitors (BIS, EEG)",
            "Surgical stimulus"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "American Society of Anesthesiologists (ASA) Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Insufficient anesthesia may lead to awareness; excessive anesthesia risks overdose.",
        counter_arguments=[
            "Depth monitors are not always reliable",
            "Clinical signs may be masked by muscle relaxants",
            "Individual variability in anesthetic response"
        ],
        resolution_strategy="Combine clinical assessment with objective monitoring; titrate agents to effect.",
        entity_scope="Operating Room, PACU",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASA Practice Guidelines for Anesthesia Monitoring"
    ),
    DoctrineBlock(
        topic="Minimum Alveolar Concentration (MAC)",
        keywords=["MAC", "minimum alveolar concentration", "volatile anesthetics", "potency", "age", "temperature"],
        conclusion_template="MAC is the concentration of inhaled anesthetic required to prevent movement in 50% of patients exposed to surgical stimulus.",
        reasoning_framework=(
            "MAC provides a standardized measure of anesthetic potency. It is influenced by patient age, body temperature, "
            "concurrent medications, and physiological status. MAC values are additive for different agents. Lower MAC indicates "
            "higher potency. MAC decreases with age, hypothermia, and use of sedatives/opioids. MAC is used to guide dosing of "
            "volatile anesthetics, ensuring adequate depth while minimizing side effects. Awareness risk increases below 0.5 MAC; "
            "most surgeries require 1.2-1.3 MAC. MAC does not account for other endpoints (e.g., amnesia, autonomic response). "
            "Clinical judgment is required to adjust for individual patient factors."
        ),
        key_factors=[
            "Patient age",
            "Body temperature",
            "Concurrent medications",
            "Physiological status",
            "Type of surgery"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "Stoelting's Pharmacology & Physiology in Anesthetic Practice"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="MAC is not a perfect indicator of anesthetic depth; individual variability exists.",
        counter_arguments=[
            "MAC does not reflect amnesia or autonomic suppression",
            "MAC values may not apply to all patient populations",
            "Additive effects may be unpredictable"
        ],
        resolution_strategy="Adjust volatile agent concentration based on MAC and patient-specific factors.",
        entity_scope="Operating Room",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA Guidelines for Use of Volatile Agents"
    ),
    DoctrineBlock(
        topic="Propofol Total Intravenous Anesthesia (TIVA)",
        keywords=["propofol", "TIVA", "total intravenous anesthesia", "infusion", "pharmacokinetics", "awareness"],
        conclusion_template="Propofol TIVA provides anesthesia via continuous intravenous infusion, avoiding inhaled agents.",
        reasoning_framework=(
            "TIVA with propofol is preferred for patients at risk of malignant hyperthermia, those requiring rapid recovery, "
            "or when inhaled anesthetics are contraindicated. Propofol is administered via target-controlled infusion (TCI) or "
            "manual infusion, titrated to clinical effect and depth monitors. Advantages include reduced postoperative nausea, "
            "rapid emergence, and avoidance of environmental pollution. Risks include awareness if infusion is interrupted, "
            "hypotension, and propofol infusion syndrome (rare). TIVA requires reliable IV access, infusion pumps, and vigilant "
            "monitoring. Adjuncts (opioids, dexmedetomidine) may be used to enhance analgesia and reduce propofol requirements."
        ),
        key_factors=[
            "Patient risk factors (MH, PONV)",
            "IV access reliability",
            "Infusion pump accuracy",
            "Depth of anesthesia monitoring",
            "Adjunct medication use"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "European Society of Anaesthesiology TIVA Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="TIVA risks include awareness, hypotension, and technical failures.",
        counter_arguments=[
            "Depth monitors may fail to detect awareness",
            "Infusion pump errors can cause underdosing",
            "Propofol infusion syndrome risk with prolonged high-dose infusions"
        ],
        resolution_strategy="Use depth monitors, ensure reliable IV access, and monitor for signs of awareness.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ESA Guidelines for TIVA"
    ),
    DoctrineBlock(
        topic="Succinylcholine vs Rocuronium for Rapid Sequence Induction",
        keywords=["succinylcholine", "rocuronium", "RSI", "neuromuscular blockade", "intubation", "onset", "duration"],
        conclusion_template="Succinylcholine is preferred for rapid sequence induction due to faster onset, unless contraindicated.",
        reasoning_framework=(
            "Rapid sequence induction (RSI) requires fast-acting neuromuscular blockers to facilitate intubation and minimize "
            "aspiration risk. Succinylcholine has onset <60 seconds and short duration (~5-10 min), making it ideal for RSI. "
            "Contraindications include hyperkalemia, neuromuscular disease, burns, and history of malignant hyperthermia. "
            "Rocuronium (1.2 mg/kg) provides similar onset (~60-90 sec) but longer duration (~30-60 min). Rocuronium is preferred "
            "when succinylcholine is contraindicated. Reversal with sugammadex enables rapid recovery. Choice depends on patient "
            "risk factors, anticipated airway difficulty, and availability of reversal agents."
        ),
        key_factors=[
            "Onset and duration of action",
            "Patient contraindications",
            "Availability of sugammadex",
            "Airway difficulty",
            "Aspiration risk"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "ASA Difficult Airway Algorithm"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Succinylcholine risks include hyperkalemia, malignant hyperthermia; rocuronium has longer duration.",
        counter_arguments=[
            "Rocuronium may delay recovery if sugammadex is unavailable",
            "Succinylcholine may cause bradycardia or fasciculations",
            "Both agents may fail in severe neuromuscular disease"
        ],
        resolution_strategy="Select agent based on patient risk, contraindications, and reversal availability.",
        entity_scope="Operating Room, Emergency Department",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASA RSI Guidelines"
    ),
    DoctrineBlock(
        topic="Sugammadex Reversal of Neuromuscular Blockade",
        keywords=["sugammadex", "neuromuscular blockade", "rocuronium", "reversal", "deep block", "side effects"],
        conclusion_template="Sugammadex provides rapid and effective reversal of rocuronium and vecuronium-induced neuromuscular blockade.",
        reasoning_framework=(
            "Sugammadex is a selective binding agent for aminosteroid neuromuscular blockers (rocuronium, vecuronium). It forms "
            "a complex, rendering the agent inactive and enabling rapid reversal of even deep blockade. Dosing depends on depth "
            "of block: 2 mg/kg for moderate, 4 mg/kg for deep, 16 mg/kg for immediate reversal. Advantages include reduced risk "
            "of residual paralysis, faster recovery, and avoidance of anticholinergic side effects. Risks include hypersensitivity, "
            "anaphylaxis, and interference with hormonal contraceptives. Not effective for benzylisoquinolinium agents (cisatracurium)."
        ),
        key_factors=[
            "Depth of neuromuscular blockade",
            "Agent used (rocuronium, vecuronium)",
            "Patient allergy history",
            "Contraceptive use",
            "Renal function"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "FDA Sugammadex Label"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Sugammadex may cause anaphylaxis, is costly, and not effective for all agents.",
        counter_arguments=[
            "Neostigmine is less effective for deep blockade",
            "Sugammadex may interfere with hormonal contraception",
            "Renal impairment may delay elimination"
        ],
        resolution_strategy="Use sugammadex for deep blockade; assess allergy and renal status before administration.",
        entity_scope="Operating Room, PACU",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FDA Sugammadex Approval"
    ),
    DoctrineBlock(
        topic="Difficult Airway Prediction and Management",
        keywords=["difficult airway", "prediction", "management", "intubation", "airway assessment", "algorithm"],
        conclusion_template="Difficult airway should be predicted using standardized assessment and managed according to ASA algorithm.",
        reasoning_framework=(
            "Prediction of difficult airway relies on history, physical exam, and validated scoring systems (Mallampati, thyromental distance, "
            "mouth opening, neck mobility). Management follows the ASA Difficult Airway Algorithm, emphasizing preparation, backup plans, "
            "and availability of airway adjuncts (video laryngoscope, fiberoptic bronchoscope, supraglottic devices). Failed intubation "
            "requires prompt recognition and transition to alternative techniques. Awake intubation may be indicated for anticipated difficulty. "
            "Documentation and communication are essential for patient safety."
        ),
        key_factors=[
            "Airway assessment findings",
            "History of difficult intubation",
            "Availability of airway devices",
            "Team communication",
            "Patient cooperation"
        ],
        primary_authority=[
            "ASA Difficult Airway Algorithm",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Failure to predict/manage difficult airway increases risk of hypoxia and morbidity.",
        counter_arguments=[
            "Assessment tools may miss unanticipated difficulty",
            "Equipment failure or lack of availability",
            "Patient anatomy may change intraoperatively"
        ],
        resolution_strategy="Follow ASA algorithm, prepare backup plans, and ensure team readiness.",
        entity_scope="Operating Room, Emergency Department",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="ASA Difficult Airway Algorithm"
    ),
    DoctrineBlock(
        topic="Supraglottic Airway Devices (LMA)",
        keywords=["LMA", "supraglottic airway", "airway management", "indications", "contraindications", "complications"],
        conclusion_template="LMAs are effective for airway management in elective and emergency settings, with specific indications and contraindications.",
        reasoning_framework=(
            "Supraglottic airway devices (LMAs) are used for airway management when endotracheal intubation is not required or difficult. "
            "Indications include elective surgery, rescue airway in failed intubation, and short procedures. Contraindications include "
            "risk of aspiration, high airway pressures, and upper airway pathology. Complications include sore throat, laryngospasm, "
            "and rare aspiration. Proper sizing, placement, and cuff inflation are essential. LMAs are integral to difficult airway algorithms."
        ),
        key_factors=[
            "Indication for airway management",
            "Aspiration risk",
            "Airway anatomy",
            "Procedure duration",
            "Patient comorbidities"
        ],
        primary_authority=[
            "ASA Difficult Airway Algorithm",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="LMAs may not protect against aspiration and are unsuitable for high-pressure ventilation.",
        counter_arguments=[
            "LMAs may fail in obese or high-risk patients",
            "Aspiration risk remains",
            "Placement may be difficult in certain anatomies"
        ],
        resolution_strategy="Select LMA based on patient risk and procedure; have backup airway plan.",
        entity_scope="Operating Room, Emergency Department",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASA Difficult Airway Algorithm"
    ),
    DoctrineBlock(
        topic="Invasive Arterial Blood Pressure Monitoring",
        keywords=["arterial line", "invasive blood pressure", "monitoring", "indications", "complications", "waveform analysis"],
        conclusion_template="Arterial lines provide continuous blood pressure monitoring and access for blood sampling in high-risk patients.",
        reasoning_framework=(
            "Invasive arterial monitoring is indicated for patients undergoing major surgery, with hemodynamic instability, or requiring "
            "frequent blood sampling. Placement is typically radial, but femoral, axillary, or brachial sites may be used. Complications "
            "include infection, thrombosis, hematoma, and distal ischemia. Waveform analysis provides information on cardiac output, "
            "stroke volume, and arrhythmias. Proper technique, aseptic placement, and regular assessment are essential for safety."
        ),
        key_factors=[
            "Patient risk profile",
            "Surgical complexity",
            "Hemodynamic instability",
            "Site selection",
            "Aseptic technique"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "ASA Standards for Basic Anesthetic Monitoring"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Arterial lines carry risks of infection, thrombosis, and ischemia.",
        counter_arguments=[
            "Noninvasive monitoring may suffice in low-risk cases",
            "Complications may outweigh benefits",
            "Waveform interpretation requires expertise"
        ],
        resolution_strategy="Use invasive monitoring for high-risk patients; minimize complications with proper technique.",
        entity_scope="Operating Room, ICU",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASA Standards for Basic Anesthetic Monitoring"
    ),
    DoctrineBlock(
        topic="Central Venous Pressure Monitoring",
        keywords=["CVP", "central venous pressure", "monitoring", "fluid status", "indications", "complications"],
        conclusion_template="CVP monitoring is used to assess intravascular volume and guide fluid management in select patients.",
        reasoning_framework=(
            "CVP reflects right atrial pressure and is used to guide fluid management in patients with complex hemodynamics. "
            "Indications include major surgery, sepsis, and cardiac dysfunction. Limitations include poor correlation with left "
            "ventricular preload and susceptibility to confounding factors (mechanical ventilation, intrathoracic pressure). "
            "Complications include infection, thrombosis, and pneumothorax. Interpretation requires integration with clinical context."
        ),
        key_factors=[
            "Patient hemodynamic status",
            "Surgical complexity",
            "Confounding factors",
            "Site selection",
            "Aseptic technique"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "Surviving Sepsis Campaign Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="CVP is a limited predictor of fluid responsiveness and carries procedural risks.",
        counter_arguments=[
            "CVP may be misleading in mechanically ventilated patients",
            "Complications may outweigh benefits",
            "Other indices (PPV, SVV) may be superior"
        ],
        resolution_strategy="Use CVP in select patients; interpret in clinical context and minimize complications.",
        entity_scope="Operating Room, ICU",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Surviving Sepsis Campaign Guidelines"
    ),
    DoctrineBlock(
        topic="ASA Physical Status Classification",
        keywords=["ASA", "physical status", "classification", "risk stratification", "preoperative assessment"],
        conclusion_template="ASA Physical Status Classification provides a standardized method for preoperative risk assessment.",
        reasoning_framework=(
            "The ASA Physical Status Classification ranges from I (healthy) to VI (brain-dead organ donor), with E denoting emergency. "
            "It is used to stratify perioperative risk and guide decision-making. Limitations include interobserver variability and "
            "incomplete capture of all risk factors. ASA status is correlated with perioperative morbidity and mortality. Accurate "
            "classification requires thorough history and physical exam."
        ),
        key_factors=[
            "Patient comorbidities",
            "Severity of disease",
            "Emergency status",
            "Functional status",
            "History and physical exam"
        ],
        primary_authority=[
            "ASA Physical Status Classification",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="ASA classification may not capture all risk factors and is subject to variability.",
        counter_arguments=[
            "Classification is subjective",
            "Does not account for surgical complexity",
            "May underestimate risk in certain populations"
        ],
        resolution_strategy="Use ASA classification as part of comprehensive risk assessment.",
        entity_scope="Preoperative Clinic, Operating Room",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASA Physical Status Classification"
    ),
    DoctrineBlock(
        topic="NPO Guidelines and Aspiration Risk",
        keywords=["NPO", "fasting", "aspiration", "guidelines", "preoperative", "clear liquids", "risk stratification"],
        conclusion_template="NPO guidelines minimize aspiration risk by specifying fasting intervals for solids and liquids.",
        reasoning_framework=(
            "ASA NPO guidelines recommend fasting from clear liquids for 2 hours, breast milk for 4 hours, infant formula for 6 hours, "
            "and solids for 6-8 hours before elective anesthesia. These intervals reduce gastric volume and acidity, minimizing aspiration risk. "
            "Exceptions include emergency surgery, delayed gastric emptying, and high-risk patients. Aspiration risk is increased in obesity, "
            "pregnancy, and gastrointestinal pathology. Preoperative assessment and adherence to guidelines are essential for safety."
        ),
        key_factors=[
            "Type of intake (clear liquids, solids)",
            "Patient risk factors",
            "Surgical urgency",
            "Gastric emptying status",
            "Adherence to guidelines"
        ],
        primary_authority=[
            "ASA NPO Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="NPO guidelines may not eliminate risk in high-risk patients; emergencies require modification.",
        counter_arguments=[
            "Delayed gastric emptying may persist despite fasting",
            "Emergencies require risk-benefit assessment",
            "Guidelines may be difficult to enforce"
        ],
        resolution_strategy="Follow ASA guidelines; modify as needed for emergencies and high-risk patients.",
        entity_scope="Preoperative Clinic, Operating Room",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASA NPO Guidelines"
    ),
    DoctrineBlock(
        topic="Malignant Hyperthermia Crisis Management",
        keywords=["malignant hyperthermia", "MH", "crisis", "dantrolene", "volatile anesthetics", "management"],
        conclusion_template="Malignant hyperthermia crisis requires immediate discontinuation of triggering agents and administration of dantrolene.",
        reasoning_framework=(
            "MH is a life-threatening reaction to volatile anesthetics or succinylcholine, characterized by hypercapnia, tachycardia, "
            "muscle rigidity, and hyperthermia. Immediate management includes discontinuation of triggers, administration of dantrolene "
            "(2.5 mg/kg IV), active cooling, correction of acidosis, hyperkalemia, and arrhythmias. Early recognition and treatment are "
            "critical for survival. All anesthetizing locations must have access to dantrolene and MH cart. Genetic counseling and patient "
            "education are recommended for survivors."
        ),
        key_factors=[
            "Recognition of MH signs",
            "Access to dantrolene",
            "Discontinuation of triggers",
            "Supportive management",
            "Patient education"
        ],
        primary_authority=[
            "Malignant Hyperthermia Association of the United States (MHAUS)",
            "ASA Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Delayed recognition or lack of dantrolene increases mortality.",
        counter_arguments=[
            "MH may mimic other conditions (sepsis, thyroid storm)",
            "Dantrolene may be unavailable in some locations",
            "Genetic testing may be inconclusive"
        ],
        resolution_strategy="Immediate management per MHAUS protocol; ensure dantrolene availability.",
        entity_scope="Operating Room, PACU",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="MHAUS Protocol"
    ),
    DoctrineBlock(
        topic="Postoperative Nausea and Vomiting (PONV) Prophylaxis",
        keywords=["PONV", "postoperative nausea", "vomiting", "prophylaxis", "risk factors", "antiemetics"],
        conclusion_template="PONV prophylaxis should be tailored to patient risk using multimodal antiemetic therapy.",
        reasoning_framework=(
            "PONV risk is determined by patient factors (female, nonsmoker, history of PONV/motion sickness), anesthetic technique, and "
            "surgical factors. Prophylaxis includes 5-HT3 antagonists (ondansetron), dexamethasone, droperidol, and avoidance of volatile "
            "agents and opioids. Multimodal therapy is recommended for high-risk patients. Nonpharmacologic measures (acupuncture, hydration) "
            "may be adjuncts. Rescue therapy is provided for breakthrough symptoms. Risk assessment tools (Apfel score) guide prophylaxis."
        ),
        key_factors=[
            "Patient risk factors",
            "Anesthetic technique",
            "Surgical type",
            "Anti-emetic selection",
            "Multimodal approach"
        ],
        primary_authority=[
            "ASA PONV Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Overuse of antiemetics may cause side effects; underuse increases PONV incidence.",
        counter_arguments=[
            "Individual response to antiemetics varies",
            "Side effects (QT prolongation, sedation)",
            "Nonpharmacologic measures may be insufficient"
        ],
        resolution_strategy="Use risk assessment to guide multimodal prophylaxis; monitor for side effects.",
        entity_scope="Operating Room, PACU",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA PONV Guidelines"
    ),
    DoctrineBlock(
        topic="Spinal Anesthesia Technique and Complications",
        keywords=["spinal anesthesia", "technique", "complications", "local anesthetic", "hypotension", "post-dural puncture headache"],
        conclusion_template="Spinal anesthesia is performed with aseptic technique and careful dosing to minimize complications.",
        reasoning_framework=(
            "Spinal anesthesia involves injection of local anesthetic into the subarachnoid space, typically at L3-L4 or L4-L5. "
            "Aseptic technique and proper patient positioning are essential. Complications include hypotension, bradycardia, "
            "post-dural puncture headache, infection, and rare neurologic injury. Hypotension is managed with fluids and vasopressors. "
            "Post-dural puncture headache is treated with epidural blood patch. Patient selection and informed consent are critical."
        ),
        key_factors=[
            "Patient anatomy",
            "Aseptic technique",
            "Local anesthetic dosing",
            "Complication management",
            "Patient consent"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "ASA Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Spinal anesthesia may cause hypotension, headache, or rare neurologic injury.",
        counter_arguments=[
            "Patient refusal",
            "Anatomic difficulty",
            "Risk of infection or bleeding"
        ],
        resolution_strategy="Careful technique, informed consent, and prompt management of complications.",
        entity_scope="Operating Room, Labor and Delivery",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASA Guidelines for Regional Anesthesia"
    ),
    DoctrineBlock(
        topic="Epidural Anesthesia and Labor Analgesia",
        keywords=["epidural anesthesia", "labor analgesia", "technique", "complications", "local anesthetic", "opioids"],
        conclusion_template="Epidural anesthesia provides effective labor analgesia with careful technique and monitoring for complications.",
        reasoning_framework=(
            "Epidural anesthesia involves injection of local anesthetic and/or opioids into the epidural space. It is the gold standard "
            "for labor analgesia, providing segmental blockade and preserving motor function. Complications include hypotension, "
            "inadequate block, infection, and rare neurologic injury. Proper technique, dosing, and monitoring are essential. Patient "
            "education and consent are required. Epidural analgesia may be contraindicated in coagulopathy or infection."
        ),
        key_factors=[
            "Patient anatomy",
            "Aseptic technique",
            "Local anesthetic/opioid dosing",
            "Complication management",
            "Patient consent"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "ASA Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Epidural may cause hypotension, inadequate block, or rare neurologic injury.",
        counter_arguments=[
            "Patient refusal",
            "Coagulopathy or infection",
            "Risk of bleeding or abscess"
        ],
        resolution_strategy="Careful technique, informed consent, and prompt management of complications.",
        entity_scope="Labor and Delivery, Operating Room",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA Guidelines for Obstetric Anesthesia"
    ),
    DoctrineBlock(
        topic="Ultrasound-Guided Regional Anesthesia and Nerve Blocks",
        keywords=["ultrasound", "regional anesthesia", "nerve block", "technique", "complications", "local anesthetic"],
        conclusion_template="Ultrasound guidance improves safety and efficacy of regional anesthesia and nerve blocks.",
        reasoning_framework=(
            "Ultrasound-guided regional anesthesia enables direct visualization of nerves, vessels, and anatomy, improving block accuracy "
            "and reducing complications. It is used for peripheral nerve blocks (brachial plexus, femoral, sciatic) and central neuraxial blocks. "
            "Complications include local anesthetic toxicity, nerve injury, and infection. Proper technique, dosing, and aseptic precautions "
            "are essential. Training and experience are required for optimal outcomes."
        ),
        key_factors=[
            "Anatomic visualization",
            "Local anesthetic dosing",
            "Aseptic technique",
            "Complication management",
            "Operator experience"
        ],
        primary_authority=[
            "Miller's Anesthesia",
            "ASA Guidelines"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Ultrasound may not eliminate all risks; operator inexperience increases complications.",
        counter_arguments=[
            "Equipment availability",
            "Learning curve",
            "Patient anatomy may limit visualization"
        ],
        resolution_strategy="Use ultrasound guidance when available; ensure operator training and aseptic technique.",
        entity_scope="Operating Room, Pain Clinic",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASA Guidelines for Regional Anesthesia"
    ),
    DoctrineBlock(
        topic="Preoperative Assessment and Optimization",
        keywords=["preoperative assessment", "optimization", "comorbidities", "risk stratification", "history", "physical exam"],
        conclusion_template="Comprehensive preoperative assessment identifies risk factors and enables optimization for anesthesia.",
        reasoning_framework=(
            "Preoperative assessment includes detailed history, physical exam, review of comorbidities, and risk stratification. "
            "Optimization may involve control of hypertension, diabetes, cessation of smoking, and management of cardiac or pulmonary disease. "
            "Laboratory and imaging studies are ordered as indicated. Communication with surgical and medical teams is essential. "
            "Assessment informs anesthesia plan and perioperative management."
        ),
        key_factors=[
            "Patient comorbidities",
            "Functional status",
            "Laboratory/imaging results",
            "Optimization strategies",
            "Team communication"
        ],
        primary_authority=[
            "ASA Preoperative Assessment Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Incomplete assessment increases perioperative risk.",
        counter_arguments=[
            "Time constraints",
            "Limited access to records",
            "Patient noncompliance"
        ],
        resolution_strategy="Thorough assessment and optimization; communicate findings to perioperative team.",
        entity_scope="Preoperative Clinic, Operating Room",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASA Preoperative Assessment Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Antibiotic Prophylaxis",
        keywords=["antibiotic prophylaxis", "perioperative", "infection prevention", "timing", "selection", "surgical site infection"],
        conclusion_template="Perioperative antibiotic prophylaxis reduces surgical site infection when administered appropriately.",
        reasoning_framework=(
            "Antibiotics should be administered within 60 minutes before incision for most procedures, and within 120 minutes for vancomycin or fluoroquinolones. "
            "Selection depends on surgical site, patient allergies, and local resistance patterns. Redosing may be required for prolonged procedures or excessive blood loss. "
            "Prophylaxis is discontinued within 24 hours postoperatively except for specific indications. Overuse increases resistance and side effects."
        ),
        key_factors=[
            "Timing of administration",
            "Antibiotic selection",
            "Patient allergies",
            "Procedure duration",
            "Local resistance patterns"
        ],
        primary_authority=[
            "CDC Surgical Site Infection Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Delayed or inappropriate antibiotic increases infection risk; overuse increases resistance.",
        counter_arguments=[
            "Allergic reactions",
            "Resistance patterns may change",
            "Redosing may be overlooked"
        ],
        resolution_strategy="Follow guidelines for timing and selection; monitor for allergies and resistance.",
        entity_scope="Operating Room",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CDC Surgical Site Infection Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Blood Glucose Management",
        keywords=["blood glucose", "perioperative", "diabetes", "hyperglycemia", "hypoglycemia", "monitoring"],
        conclusion_template="Perioperative blood glucose should be monitored and controlled to minimize complications.",
        reasoning_framework=(
            "Hyperglycemia increases risk of infection, poor wound healing, and adverse outcomes. Target glucose is 80-180 mg/dL. "
            "Insulin infusions may be used for tight control in high-risk patients. Hypoglycemia is avoided by frequent monitoring and "
            "adjustment of insulin or oral agents. Preoperative assessment includes review of diabetes control, medications, and fasting status. "
            "Postoperative monitoring continues until stable."
        ),
        key_factors=[
            "Baseline glucose control",
            "Type of diabetes",
            "Insulin/oral agent use",
            "Monitoring frequency",
            "Surgical stress response"
        ],
        primary_authority=[
            "ADA Perioperative Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor glucose control increases complications; tight control risks hypoglycemia.",
        counter_arguments=[
            "Stress response may cause unpredictable glucose changes",
            "Insulin dosing may be complex",
            "Hypoglycemia may be missed"
        ],
        resolution_strategy="Frequent monitoring and adjustment; target glucose per guidelines.",
        entity_scope="Operating Room, ICU",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ADA Perioperative Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Temperature Management",
        keywords=["temperature management", "hypothermia", "warming", "perioperative", "complications", "monitoring"],
        conclusion_template="Active perioperative warming reduces hypothermia-related complications.",
        reasoning_framework=(
            "Hypothermia increases risk of surgical site infection, coagulopathy, and delayed recovery. Active warming (forced-air, fluid warmers) "
            "is recommended for procedures >30 min. Temperature is monitored continuously. Passive measures (blankets) are insufficient for most cases. "
            "Warming is initiated preoperatively and continued intra/postoperatively. Complications of overheating are rare but monitored."
        ),
        key_factors=[
            "Procedure duration",
            "Patient risk factors",
            "Warming methods",
            "Temperature monitoring",
            "Complication prevention"
        ],
        primary_authority=[
            "ASA Temperature Management Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Failure to warm increases complications; excessive warming may cause hyperthermia.",
        counter_arguments=[
            "Equipment failure",
            "Patient intolerance",
            "Rare overheating"
        ],
        resolution_strategy="Active warming and continuous monitoring; adjust as needed.",
        entity_scope="Operating Room, PACU",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASA Temperature Management Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Fluid Management",
        keywords=["fluid management", "perioperative", "crystalloids", "colloids", "blood loss", "goal-directed therapy"],
        conclusion_template="Perioperative fluid management should be individualized using goal-directed strategies.",
        reasoning_framework=(
            "Fluid management is based on patient status, surgical losses, and hemodynamic monitoring. Crystalloids are preferred for most cases; colloids are reserved for specific indications. "
            "Goal-directed therapy uses dynamic indices (stroke volume variation, pulse pressure variation) to optimize volume status. Over-resuscitation increases risk of edema and complications; "
            "under-resuscitation increases risk of hypoperfusion. Blood products are used for significant losses. Monitoring and adjustment are continuous."
        ),
        key_factors=[
            "Patient comorbidities",
            "Surgical losses",
            "Hemodynamic monitoring",
            "Fluid type selection",
            "Goal-directed indices"
        ],
        primary_authority=[
            "ASA Fluid Management Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Inappropriate fluid management increases risk of complications.",
        counter_arguments=[
            "Dynamic indices may be unreliable",
            "Colloids may cause renal injury",
            "Blood products carry risks"
        ],
        resolution_strategy="Individualize fluid therapy; use goal-directed strategies and monitor continuously.",
        entity_scope="Operating Room, ICU",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA Fluid Management Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Pain Management",
        keywords=["pain management", "perioperative", "multimodal", "opioids", "regional anesthesia", "NSAIDs"],
        conclusion_template="Multimodal perioperative pain management improves outcomes and reduces opioid use.",
        reasoning_framework=(
            "Pain management includes opioids, NSAIDs, acetaminophen, regional anesthesia, and adjuncts (gabapentinoids, ketamine). Multimodal therapy reduces opioid requirements and improves recovery. "
            "Patient-specific factors guide selection. Regional techniques are preferred when feasible. Monitoring for side effects and efficacy is essential. Patient education and informed consent are required."
        ),
        key_factors=[
            "Pain severity",
            "Patient comorbidities",
            "Regional anesthesia feasibility",
            "Adjunct selection",
            "Side effect monitoring"
        ],
        primary_authority=[
            "ASA Pain Management Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Overuse of opioids increases risk of side effects; under-treatment impairs recovery.",
        counter_arguments=[
            "NSAIDs may be contraindicated",
            "Regional techniques may not be feasible",
            "Patient variability in response"
        ],
        resolution_strategy="Use multimodal therapy; monitor and adjust as needed.",
        entity_scope="Operating Room, PACU",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASA Pain Management Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Opioid Stewardship",
        keywords=["opioid stewardship", "perioperative", "opioid-sparing", "multimodal", "addiction", "side effects"],
        conclusion_template="Opioid stewardship reduces risk of addiction and side effects through multimodal and opioid-sparing strategies.",
        reasoning_framework=(
            "Opioid stewardship involves minimizing opioid use, employing multimodal analgesia, and monitoring for side effects. Risk of addiction and opioid-induced respiratory depression is reduced. "
            "Patient education, prescription monitoring, and use of regional techniques are emphasized. Guidelines recommend lowest effective dose and shortest duration. Alternatives (NSAIDs, acetaminophen, regional blocks) are preferred."
        ),
        key_factors=[
            "Patient risk factors",
            "Pain severity",
            "Multimodal options",
            "Prescription monitoring",
            "Education"
        ],
        primary_authority=[
            "CDC Opioid Prescribing Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Inadequate pain control may impair recovery; excessive opioids increase risk.",
        counter_arguments=[
            "Patient variability",
            "Opioid alternatives may be insufficient",
            "Monitoring may be limited"
        ],
        resolution_strategy="Employ opioid-sparing strategies; educate and monitor patients.",
        entity_scope="Operating Room, PACU",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CDC Opioid Prescribing Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Anticoagulation Management",
        keywords=["anticoagulation", "perioperative", "warfarin", "DOAC", "bleeding risk", "bridging"],
        conclusion_template="Perioperative anticoagulation management balances bleeding and thromboembolic risk.",
        reasoning_framework=(
            "Anticoagulation is managed based on bleeding risk, thromboembolic risk, and agent used. Warfarin is stopped 5 days preoperatively; DOACs are stopped 2-3 days prior. Bridging with heparin may be required for high-risk patients. "
            "Resumption is based on surgical bleeding risk. Communication with surgical and medical teams is essential. Monitoring includes INR, anti-Xa, and clinical signs."
        ),
        key_factors=[
            "Agent used",
            "Bleeding risk",
            "Thromboembolic risk",
            "Bridging indication",
            "Monitoring"
        ],
        primary_authority=[
            "ACC Anticoagulation Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Inadequate management increases risk of bleeding or thrombosis.",
        counter_arguments=[
            "Bridging may increase bleeding",
            "Timing may be complex",
            "Patient compliance"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, Preoperative Clinic",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACC Anticoagulation Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Obstructive Sleep Apnea",
        keywords=["obstructive sleep apnea", "OSA", "perioperative", "risk", "monitoring", "CPAP"],
        conclusion_template="Patients with OSA require perioperative risk assessment, monitoring, and use of CPAP when indicated.",
        reasoning_framework=(
            "OSA increases risk of perioperative complications, including respiratory depression and airway obstruction. Preoperative screening and risk stratification are essential. Use of CPAP is continued perioperatively. "
            "Monitoring in PACU and consideration for extended observation are recommended. Sedatives and opioids are minimized. Communication with surgical and medical teams is essential."
        ),
        key_factors=[
            "OSA severity",
            "CPAP compliance",
            "Opioid/sedative use",
            "Monitoring",
            "Risk stratification"
        ],
        primary_authority=[
            "ASA OSA Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Failure to manage OSA increases risk of respiratory complications.",
        counter_arguments=[
            "Patient may not disclose OSA",
            "CPAP may be unavailable",
            "Monitoring may be limited"
        ],
        resolution_strategy="Screen and stratify risk; continue CPAP and monitor closely.",
        entity_scope="Operating Room, PACU",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA OSA Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Allergies and Anaphylaxis",
        keywords=["allergy", "anaphylaxis", "perioperative", "risk", "management", "epinephrine"],
        conclusion_template="Perioperative allergy and anaphylaxis require prompt recognition and management with epinephrine.",
        reasoning_framework=(
            "Allergy and anaphylaxis may occur perioperatively due to drugs, latex, or blood products. Prompt recognition (hypotension, bronchospasm, rash) and management with epinephrine, antihistamines, and steroids are essential. "
            "Preoperative assessment includes history and avoidance of triggers. Documentation and communication are critical. Emergency protocols are followed."
        ),
        key_factors=[
            "History of allergy",
            "Trigger identification",
            "Recognition of anaphylaxis",
            "Emergency management",
            "Documentation"
        ],
        primary_authority=[
            "ASA Anaphylaxis Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Delayed recognition increases morbidity and mortality.",
        counter_arguments=[
            "Anaphylaxis may mimic other conditions",
            "Triggers may be unknown",
            "Documentation may be incomplete"
        ],
        resolution_strategy="Prompt recognition and management; document and communicate.",
        entity_scope="Operating Room, PACU",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASA Anaphylaxis Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Hypertension",
        keywords=["hypertension", "perioperative", "blood pressure", "management", "medications", "complications"],
        conclusion_template="Perioperative hypertension is managed with continuation of antihypertensives and intraoperative control.",
        reasoning_framework=(
            "Hypertension increases risk of perioperative complications. Antihypertensives are continued except ACE inhibitors/ARBs, which may be held. Intraoperative management includes titration of anesthetic depth, fluids, and vasoactive agents. "
            "Severe hypertension is treated with short-acting agents (labetalol, hydralazine). Monitoring and adjustment are continuous."
        ),
        key_factors=[
            "Baseline blood pressure",
            "Medication use",
            "Intraoperative control",
            "Complication prevention",
            "Monitoring"
        ],
        primary_authority=[
            "ASA Hypertension Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor control increases risk of stroke, MI, and bleeding.",
        counter_arguments=[
            "ACE inhibitors/ARBs may cause hypotension",
            "Patient compliance",
            "Monitoring may be limited"
        ],
        resolution_strategy="Continue antihypertensives; monitor and adjust intraoperatively.",
        entity_scope="Operating Room, Preoperative Clinic",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASA Hypertension Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Diabetes",
        keywords=["diabetes", "perioperative", "insulin", "hyperglycemia", "hypoglycemia", "monitoring"],
        conclusion_template="Diabetes is managed perioperatively with frequent glucose monitoring and adjustment of medications.",
        reasoning_framework=(
            "Diabetes increases risk of perioperative complications. Insulin and oral agents are adjusted based on fasting status and procedure. Glucose is monitored frequently. Target glucose is 80-180 mg/dL. Hypoglycemia is avoided by adjustment and monitoring. "
            "Communication with surgical and medical teams is essential."
        ),
        key_factors=[
            "Type of diabetes",
            "Medication adjustment",
            "Monitoring frequency",
            "Target glucose",
            "Team communication"
        ],
        primary_authority=[
            "ADA Perioperative Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor control increases risk of infection and complications.",
        counter_arguments=[
            "Stress response may cause unpredictable changes",
            "Insulin dosing may be complex",
            "Monitoring may be limited"
        ],
        resolution_strategy="Frequent monitoring and adjustment; communicate with team.",
        entity_scope="Operating Room, ICU",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ADA Perioperative Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Renal Disease",
        keywords=["renal disease", "perioperative", "dialysis", "fluid management", "electrolytes", "medications"],
        conclusion_template="Renal disease is managed perioperatively with careful fluid, electrolyte, and medication adjustment.",
        reasoning_framework=(
            "Renal disease increases risk of perioperative complications. Fluid and electrolyte management are individualized. Dialysis is scheduled pre/postoperatively as needed. Medications are adjusted for renal clearance. Monitoring includes creatinine, electrolytes, and volume status. "
            "Communication with nephrology and surgical teams is essential."
        ),
        key_factors=[
            "Renal function",
            "Dialysis schedule",
            "Fluid/electrolyte management",
            "Medication adjustment",
            "Team communication"
        ],
        primary_authority=[
            "ASA Renal Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Dialysis schedule may be complex",
            "Medication adjustment may be overlooked",
            "Monitoring may be limited"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASA Renal Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Liver Disease",
        keywords=["liver disease", "perioperative", "coagulopathy", "fluid management", "medications", "monitoring"],
        conclusion_template="Liver disease is managed perioperatively with attention to coagulopathy, fluid, and medication adjustment.",
        reasoning_framework=(
            "Liver disease increases risk of bleeding, fluid imbalance, and drug toxicity. Coagulopathy is corrected with blood products as needed. Fluid management avoids overload. Medications are adjusted for hepatic metabolism. Monitoring includes liver function tests, coagulation, and volume status. "
            "Communication with hepatology and surgical teams is essential."
        ),
        key_factors=[
            "Liver function",
            "Coagulopathy",
            "Fluid management",
            "Medication adjustment",
            "Team communication"
        ],
        primary_authority=[
            "ASA Liver Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of bleeding and complications.",
        counter_arguments=[
            "Coagulopathy may be severe",
            "Medication adjustment may be overlooked",
            "Monitoring may be limited"
        ],
        resolution_strategy="Individualize management; correct coagulopathy and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASA Liver Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Cardiac Disease",
        keywords=["cardiac disease", "perioperative", "ischemia", "arrhythmia", "monitoring", "medications"],
        conclusion_template="Cardiac disease is managed perioperatively with risk stratification, monitoring, and medication adjustment.",
        reasoning_framework=(
            "Cardiac disease increases risk of perioperative complications. Risk stratification includes assessment of ischemia, arrhythmia, and functional status. Medications are continued except for specific contraindications. Monitoring includes ECG, troponin, and hemodynamics. Communication with cardiology and surgical teams is essential."
        ),
        key_factors=[
            "Cardiac function",
            "Risk stratification",
            "Medication adjustment",
            "Monitoring",
            "Team communication"
        ],
        primary_authority=[
            "ACC/AHA Cardiac Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of ischemia and arrhythmia.",
        counter_arguments=[
            "Medication adjustment may be complex",
            "Monitoring may be limited",
            "Patient compliance"
        ],
        resolution_strategy="Individualize management; monitor and communicate closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Cardiac Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Pulmonary Disease",
        keywords=["pulmonary disease", "perioperative", "COPD", "asthma", "risk", "monitoring"],
        conclusion_template="Pulmonary disease is managed perioperatively with optimization, monitoring, and medication adjustment.",
        reasoning_framework=(
            "Pulmonary disease increases risk of perioperative complications. Optimization includes bronchodilator therapy, smoking cessation, and pulmonary rehabilitation. Monitoring includes pulse oximetry, capnography, and ABG as needed. Medications are continued except for specific contraindications. Communication with pulmonology and surgical teams is essential."
        ),
        key_factors=[
            "Pulmonary function",
            "Optimization strategies",
            "Medication adjustment",
            "Monitoring",
            "Team communication"
        ],
        primary_authority=[
            "ASA Pulmonary Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of respiratory complications.",
        counter_arguments=[
            "Optimization may be limited",
            "Medication adjustment may be overlooked",
            "Monitoring may be limited"
        ],
        resolution_strategy="Individualize management; optimize and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASA Pulmonary Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Pediatric Patients",
        keywords=["pediatric", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Pediatric patients require age-specific perioperative management and monitoring.",
        reasoning_framework=(
            "Pediatric patients have unique physiological and pharmacological considerations. Age-specific dosing, monitoring, and risk assessment are essential. Communication with pediatric specialists and family is critical. Informed consent and patient comfort are prioritized. Guidelines recommend age-appropriate fasting, monitoring, and medication adjustment."
        ),
        key_factors=[
            "Age and weight",
            "Medication dosing",
            "Monitoring",
            "Risk assessment",
            "Communication"
        ],
        primary_authority=[
            "ASA Pediatric Anesthesia Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Age-specific dosing may be complex",
            "Monitoring may be limited",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, PACU",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA Pediatric Anesthesia Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Geriatric Patients",
        keywords=["geriatric", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Geriatric patients require tailored perioperative management to minimize complications.",
        reasoning_framework=(
            "Geriatric patients have increased risk of perioperative complications due to comorbidities and physiological changes. Medication dosing is adjusted for age and renal/hepatic function. Monitoring is intensified. Risk assessment includes frailty and cognitive status. Communication with patient and family is essential. Guidelines recommend tailored fasting, monitoring, and medication adjustment."
        ),
        key_factors=[
            "Age and comorbidities",
            "Medication adjustment",
            "Monitoring",
            "Risk assessment",
            "Communication"
        ],
        primary_authority=[
            "ASA Geriatric Anesthesia Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Medication adjustment may be complex",
            "Monitoring may be limited",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, PACU",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASA Geriatric Anesthesia Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Pregnancy",
        keywords=["pregnancy", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Pregnant patients require specialized perioperative management to minimize maternal and fetal risk.",
        reasoning_framework=(
            "Pregnancy increases risk of perioperative complications. Anesthesia is tailored to minimize fetal exposure and maternal risk. Monitoring includes fetal heart rate and maternal hemodynamics. Medications are selected for safety. Communication with obstetrics and surgical teams is essential. Guidelines recommend tailored fasting, monitoring, and medication adjustment."
        ),
        key_factors=[
            "Gestational age",
            "Medication selection",
            "Monitoring",
            "Risk assessment",
            "Communication"
        ],
        primary_authority=[
            "ASA Obstetric Anesthesia Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of maternal and fetal complications.",
        counter_arguments=[
            "Medication selection may be limited",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, Labor and Delivery",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASA Obstetric Anesthesia Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Trauma Patients",
        keywords=["trauma", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Trauma patients require rapid assessment, resuscitation, and tailored anesthesia management.",
        reasoning_framework=(
            "Trauma patients have increased risk of perioperative complications. Rapid assessment and resuscitation are essential. Anesthesia is tailored to injuries and hemodynamic status. Monitoring includes ECG, pulse oximetry, and invasive lines as needed. Communication with trauma and surgical teams is critical. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Injury severity",
            "Resuscitation",
            "Monitoring",
            "Medication selection",
            "Communication"
        ],
        primary_authority=[
            "ASA Trauma Anesthesia Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Rapid assessment may be limited",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, Emergency Department",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASA Trauma Anesthesia Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Oncology Patients",
        keywords=["oncology", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Oncology patients require tailored perioperative management to minimize complications and support recovery.",
        reasoning_framework=(
            "Oncology patients have increased risk of perioperative complications due to comorbidities and treatment effects. Anesthesia is tailored to disease and therapy. Monitoring includes ECG, pulse oximetry, and laboratory studies. Medications are selected for safety. Communication with oncology and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Cancer type",
            "Treatment effects",
            "Monitoring",
            "Medication selection",
            "Communication"
        ],
        primary_authority=[
            "ASA Oncology Anesthesia Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Treatment effects may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASA Oncology Anesthesia Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Infectious Disease",
        keywords=["infectious disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Patients with infectious disease require perioperative management to minimize transmission and complications.",
        reasoning_framework=(
            "Infectious disease increases risk of perioperative complications and transmission. Anesthesia is tailored to disease and therapy. Monitoring includes ECG, pulse oximetry, and laboratory studies. Infection control measures are implemented. Communication with infectious disease and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Infection type",
            "Transmission risk",
            "Monitoring",
            "Medication selection",
            "Infection control"
        ],
        primary_authority=[
            "CDC Infection Control Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of transmission and complications.",
        counter_arguments=[
            "Transmission risk may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; implement infection control and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CDC Infection Control Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Neurologic Disease",
        keywords=["neurologic disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Neurologic disease is managed perioperatively with tailored anesthesia and monitoring.",
        reasoning_framework=(
            "Neurologic disease increases risk of perioperative complications. Anesthesia is tailored to disease and therapy. Monitoring includes EEG, ECG, and neurologic assessment. Medications are selected for safety. Communication with neurology and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Neurologic function",
            "Disease type",
            "Monitoring",
            "Medication selection",
            "Communication"
        ],
        primary_authority=[
            "ASA Neurologic Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Disease effects may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASA Neurologic Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Psychiatric Disease",
        keywords=["psychiatric disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Psychiatric disease is managed perioperatively with tailored anesthesia, medication adjustment, and communication.",
        reasoning_framework=(
            "Psychiatric disease increases risk of perioperative complications and medication interactions. Anesthesia is tailored to disease and therapy. Monitoring includes mental status and medication effects. Communication with psychiatry and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Psychiatric diagnosis",
            "Medication adjustment",
            "Monitoring",
            "Communication",
            "Risk assessment"
        ],
        primary_authority=[
            "ASA Psychiatric Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications and interactions.",
        counter_arguments=[
            "Medication interactions may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, Preoperative Clinic",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASA Psychiatric Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Immunosuppressed Patients",
        keywords=["immunosuppression", "perioperative", "anesthesia", "risk", "monitoring", "infection"],
        conclusion_template="Immunosuppressed patients require perioperative management to minimize infection and complications.",
        reasoning_framework=(
            "Immunosuppressed patients have increased risk of perioperative infection and complications. Anesthesia is tailored to disease and therapy. Monitoring includes infection signs and laboratory studies. Infection control measures are implemented. Communication with immunology and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Immunosuppression type",
            "Infection risk",
            "Monitoring",
            "Medication selection",
            "Infection control"
        ],
        primary_authority=[
            "CDC Infection Control Guidelines",
            "ASA Recommendations"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of infection and complications.",
        counter_arguments=[
            "Infection risk may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; implement infection control and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="CDC Infection Control Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Endocrine Disease",
        keywords=["endocrine disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Endocrine disease is managed perioperatively with tailored anesthesia, medication adjustment, and monitoring.",
        reasoning_framework=(
            "Endocrine disease increases risk of perioperative complications. Anesthesia is tailored to disease and therapy. Monitoring includes hormone levels and clinical signs. Medications are adjusted for perioperative needs. Communication with endocrinology and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Endocrine diagnosis",
            "Medication adjustment",
            "Monitoring",
            "Communication",
            "Risk assessment"
        ],
        primary_authority=[
            "ASA Endocrine Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Hormone levels may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASA Endocrine Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Autoimmune Disease",
        keywords=["autoimmune disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Autoimmune disease is managed perioperatively with tailored anesthesia, medication adjustment, and monitoring.",
        reasoning_framework=(
            "Autoimmune disease increases risk of perioperative complications. Anesthesia is tailored to disease and therapy. Monitoring includes disease activity and laboratory studies. Medications are adjusted for perioperative needs. Communication with rheumatology and surgical teams is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Autoimmune diagnosis",
            "Medication adjustment",
            "Monitoring",
            "Communication",
            "Risk assessment"
        ],
        primary_authority=[
            "ASA Autoimmune Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Disease activity may be unpredictable",
            "Monitoring may be complex",
            "Communication may be challenging"
        ],
        resolution_strategy="Individualize management; communicate and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASA Autoimmune Disease Guidelines"
    ),
    DoctrineBlock(
        topic="Perioperative Management of Rare Diseases",
        keywords=["rare disease", "perioperative", "anesthesia", "risk", "monitoring", "medications"],
        conclusion_template="Rare diseases require individualized perioperative management and consultation with specialists.",
        reasoning_framework=(
            "Rare diseases may have unique perioperative risks and management needs. Anesthesia is tailored to disease and therapy. Monitoring includes disease-specific signs and laboratory studies. Consultation with specialists is essential. Guidelines recommend individualized management and monitoring."
        ),
        key_factors=[
            "Rare disease diagnosis",
            "Specialist consultation",
            "Monitoring",
            "Medication adjustment",
            "Risk assessment"
        ],
        primary_authority=[
            "ASA Rare Disease Guidelines",
            "Miller's Anesthesia"
        ],
        burden_holder="Anesthesiologist",
        adversary_position="Poor management increases risk of complications.",
        counter_arguments=[
            "Disease effects may be unpredictable",
            "Monitoring may be complex",
            "Specialist consultation may be limited"
        ],
        resolution_strategy="Individualize management; consult specialists and monitor closely.",
        entity_scope="Operating Room, ICU",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASA Rare Disease Guidelines"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]