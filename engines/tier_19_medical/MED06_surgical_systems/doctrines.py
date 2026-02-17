from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="ASA Physical Status Classification",
        keywords=["ASA", "anesthesia", "risk stratification", "preoperative", "physical status"],
        conclusion_template="Patient is classified as ASA {status} based on preoperative assessment.",
        reasoning_framework="""
        The ASA Physical Status Classification System is used to assess and communicate a patient's preoperative medical comorbidities. 
        The classification ranges from ASA I (healthy patient) to ASA VI (brain-dead patient for organ donation). 
        The assessment is based on medical history, current conditions, and functional status. 
        Key factors include age, comorbidities, functional limitations, and acute illness. 
        The classification guides anesthetic risk and perioperative management. 
        Primary authorities are the American Society of Anesthesiologists and institutional guidelines. 
        The burden holder is the anesthesiologist performing the preoperative evaluation. 
        Adversary positions may include surgical teams seeking to minimize perceived risk. 
        Counter arguments focus on subjective interpretation and interobserver variability. 
        Resolution strategy involves multidisciplinary review and consensus. 
        Entity scope includes all surgical patients undergoing anesthesia.
        """,
        key_factors=[
            "Medical comorbidities",
            "Functional status",
            "Age",
            "Acute illness",
            "History of anesthesia complications"
        ],
        primary_authority=["American Society of Anesthesiologists", "Institutional Anesthesia Guidelines"],
        burden_holder="Anesthesiologist",
        adversary_position="Surgeon seeking lower risk classification",
        counter_arguments=[
            "Subjectivity in classification",
            "Inconsistent application across providers",
            "Potential for risk minimization"
        ],
        resolution_strategy="Multidisciplinary review and consensus",
        entity_scope="All surgical patients",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Physical Status Classification System, 2014 Revision"
    ),
    DoctrineBlock(
        topic="Mallampati Airway Assessment",
        keywords=["Mallampati", "airway", "anesthesia", "intubation", "risk"],
        conclusion_template="Patient's airway is classified as Mallampati Class {class} based on oral examination.",
        reasoning_framework="""
        The Mallampati classification assesses the visibility of oropharyngeal structures to predict the ease of endotracheal intubation. 
        The patient is asked to open their mouth and protrude their tongue; the examiner observes the visibility of the soft palate, uvula, and tonsillar pillars. 
        Classes range from I (full visibility) to IV (hard palate only). 
        Key factors include anatomical variation, patient cooperation, and examiner experience. 
        The assessment informs anesthesia planning and airway management strategies. 
        Primary authorities are anesthesia societies and institutional protocols. 
        The burden holder is the anesthesiologist or airway manager. 
        Adversary positions may include surgical urgency overriding airway concerns. 
        Counter arguments focus on limited predictive value and interobserver variability. 
        Resolution strategy involves combining Mallampati with other airway assessments. 
        Entity scope includes all patients undergoing anesthesia.
        """,
        key_factors=[
            "Visibility of oropharyngeal structures",
            "Patient cooperation",
            "Anatomical variation",
            "Examiner experience"
        ],
        primary_authority=["American Society of Anesthesiologists", "Institutional Airway Guidelines"],
        burden_holder="Anesthesiologist",
        adversary_position="Surgeon prioritizing rapid induction",
        counter_arguments=[
            "Limited predictive value",
            "Interobserver variability",
            "Other airway assessment tools may be superior"
        ],
        resolution_strategy="Combine Mallampati with other airway assessments",
        entity_scope="Patients undergoing anesthesia",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Difficult Airway Algorithm, 2013"
    ),
    DoctrineBlock(
        topic="WHO Surgical Safety Checklist",
        keywords=["WHO", "safety", "checklist", "surgery", "patient safety"],
        conclusion_template="WHO Surgical Safety Checklist completed and documented for procedure.",
        reasoning_framework="""
        The WHO Surgical Safety Checklist is a standardized tool to enhance patient safety during surgery. 
        It consists of three phases: Sign In (before induction), Time Out (before incision), and Sign Out (before leaving the operating room). 
        Each phase addresses critical safety elements such as patient identification, surgical site, anesthesia safety, and equipment readiness. 
        Key factors include team communication, checklist adherence, and documentation. 
        Primary authorities are the World Health Organization and institutional safety committees. 
        The burden holder is the circulating nurse or designated checklist leader. 
        Adversary positions may include resistance to checklist use due to perceived workflow disruption. 
        Counter arguments focus on evidence of reduced complications and improved outcomes. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Checklist adherence",
            "Team communication",
            "Patient identification",
            "Surgical site verification",
            "Anesthesia safety"
        ],
        primary_authority=["World Health Organization", "Institutional Safety Committee"],
        burden_holder="Circulating Nurse",
        adversary_position="Surgeon resisting checklist use",
        counter_arguments=[
            "Workflow disruption",
            "Checklist fatigue",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, and feedback",
        entity_scope="All surgical procedures",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Surgical Safety Checklist, 2008"
    ),
    DoctrineBlock(
        topic="Laparoscopic vs Open Surgery Decision Criteria",
        keywords=["laparoscopy", "open surgery", "minimally invasive", "criteria", "decision"],
        conclusion_template="Laparoscopic approach is indicated based on patient and procedure criteria.",
        reasoning_framework="""
        The choice between laparoscopic and open surgery is guided by patient factors, procedural complexity, and surgeon expertise. 
        Laparoscopy offers benefits such as reduced postoperative pain, shorter hospital stay, and faster recovery, but may be contraindicated in cases of severe adhesions, hemodynamic instability, or lack of expertise. 
        Key factors include patient comorbidities, previous abdominal surgeries, procedural indications, and available technology. 
        Primary authorities are surgical societies and institutional protocols. 
        The burden holder is the operating surgeon. 
        Adversary positions may include patient preference or institutional limitations. 
        Counter arguments focus on conversion rates, cost, and learning curve. 
        Resolution strategy involves shared decision-making and risk-benefit analysis. 
        Entity scope includes abdominal and pelvic surgeries.
        """,
        key_factors=[
            "Patient comorbidities",
            "Previous abdominal surgeries",
            "Procedural complexity",
            "Surgeon expertise",
            "Available technology"
        ],
        primary_authority=["Society of American Gastrointestinal and Endoscopic Surgeons", "Institutional Surgical Guidelines"],
        burden_holder="Operating Surgeon",
        adversary_position="Patient preferring open approach",
        counter_arguments=[
            "Conversion to open surgery",
            "Higher cost",
            "Learning curve for laparoscopy"
        ],
        resolution_strategy="Shared decision-making and risk-benefit analysis",
        entity_scope="Abdominal and pelvic surgeries",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAGES Guidelines for Laparoscopic Surgery, 2017"
    ),
    DoctrineBlock(
        topic="Robotic-Assisted Surgery (da Vinci Platform)",
        keywords=["robotic surgery", "da Vinci", "minimally invasive", "technology", "indications"],
        conclusion_template="Robotic-assisted surgery is indicated based on procedure and surgeon expertise.",
        reasoning_framework="""
        Robotic-assisted surgery, particularly using the da Vinci platform, is indicated for select procedures where enhanced dexterity, visualization, and precision are beneficial. 
        Indications include prostatectomy, hysterectomy, and colorectal surgery. 
        Key factors include surgeon training, procedure complexity, patient anatomy, and institutional resources. 
        Primary authorities are surgical societies, FDA, and institutional credentialing bodies. 
        The burden holder is the operating surgeon and credentialing committee. 
        Adversary positions may include concerns about cost, operative time, and technology dependence. 
        Counter arguments focus on improved outcomes, reduced complications, and patient satisfaction. 
        Resolution strategy involves credentialing, outcome tracking, and cost-benefit analysis. 
        Entity scope includes procedures amenable to robotic assistance.
        """,
        key_factors=[
            "Surgeon training",
            "Procedure complexity",
            "Patient anatomy",
            "Institutional resources",
            "FDA approval"
        ],
        primary_authority=["FDA", "American College of Surgeons", "Institutional Credentialing Committee"],
        burden_holder="Operating Surgeon",
        adversary_position="Hospital administration concerned about cost",
        counter_arguments=[
            "Increased operative time",
            "High equipment cost",
            "Technology dependence"
        ],
        resolution_strategy="Credentialing, outcome tracking, cost-benefit analysis",
        entity_scope="Robotic-assisted surgical procedures",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Approval for da Vinci Surgical System, 2000"
    ),
    DoctrineBlock(
        topic="Surgical Site Infection Prevention Bundle",
        keywords=["SSI", "infection prevention", "bundle", "antibiotics", "sterility"],
        conclusion_template="Surgical site infection prevention bundle implemented and documented.",
        reasoning_framework="""
        The SSI prevention bundle consists of evidence-based interventions including preoperative antibiotic administration, skin antisepsis, normothermia, glycemic control, and sterile technique. 
        Key factors include timing and selection of antibiotics, patient risk factors, and adherence to sterile protocols. 
        Primary authorities are CDC, WHO, and institutional infection control committees. 
        The burden holder is the surgical team and infection control nurse. 
        Adversary positions may include resource limitations or patient allergies. 
        Counter arguments focus on antibiotic resistance and compliance challenges. 
        Resolution strategy involves protocol standardization, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Antibiotic timing and selection",
            "Skin antisepsis",
            "Normothermia",
            "Glycemic control",
            "Sterile technique"
        ],
        primary_authority=["CDC", "WHO", "Institutional Infection Control Committee"],
        burden_holder="Surgical Team",
        adversary_position="Patient with antibiotic allergy",
        counter_arguments=[
            "Antibiotic resistance",
            "Compliance challenges",
            "Resource limitations"
        ],
        resolution_strategy="Protocol standardization, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Guideline for SSI Prevention, 2017"
    ),
    DoctrineBlock(
        topic="Enhanced Recovery After Surgery (ERAS) Protocols",
        keywords=["ERAS", "recovery", "protocol", "perioperative", "outcomes"],
        conclusion_template="ERAS protocol implemented for patient, with multidisciplinary documentation.",
        reasoning_framework="""
        ERAS protocols are multimodal perioperative care pathways designed to reduce surgical stress, optimize recovery, and improve outcomes. 
        Components include preoperative counseling, carbohydrate loading, opioid-sparing analgesia, early mobilization, and nutrition. 
        Key factors include protocol adherence, patient engagement, and multidisciplinary coordination. 
        Primary authorities are ERAS Society, surgical societies, and institutional committees. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include resistance to protocol change or patient noncompliance. 
        Counter arguments focus on variability in outcomes and resource demands. 
        Resolution strategy involves education, audit, and continuous improvement. 
        Entity scope includes elective surgical patients.
        """,
        key_factors=[
            "Protocol adherence",
            "Patient engagement",
            "Multidisciplinary coordination",
            "Opioid-sparing analgesia",
            "Early mobilization"
        ],
        primary_authority=["ERAS Society", "American College of Surgeons", "Institutional ERAS Committee"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Traditionalist surgeon resisting protocol",
        counter_arguments=[
            "Variability in outcomes",
            "Resource demands",
            "Patient noncompliance"
        ],
        resolution_strategy="Education, audit, continuous improvement",
        entity_scope="Elective surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ERAS Society Guidelines, 2018"
    ),
    DoctrineBlock(
        topic="Electrosurgery Safety (Monopolar vs Bipolar)",
        keywords=["electrosurgery", "monopolar", "bipolar", "safety", "energy devices"],
        conclusion_template="Electrosurgery device selection and safety protocols documented for procedure.",
        reasoning_framework="""
        Electrosurgery devices are used for cutting and coagulation during surgery. 
        Monopolar devices require a return electrode and pose higher risk for stray current injuries, while bipolar devices confine current between two electrodes and reduce risk. 
        Key factors include procedure type, patient risk factors (pacemakers, implants), device settings, and staff training. 
        Primary authorities are surgical societies, device manufacturers, and institutional safety committees. 
        The burden holder is the operating surgeon and perioperative staff. 
        Adversary positions may include preference for device familiarity over safety. 
        Counter arguments focus on device limitations and cost. 
        Resolution strategy involves protocol adherence, staff education, and device maintenance. 
        Entity scope includes all surgical procedures using electrosurgery.
        """,
        key_factors=[
            "Device selection",
            "Procedure type",
            "Patient risk factors",
            "Device settings",
            "Staff training"
        ],
        primary_authority=["American College of Surgeons", "Device Manufacturers", "Institutional Safety Committee"],
        burden_holder="Operating Surgeon",
        adversary_position="Surgeon preferring familiar device",
        counter_arguments=[
            "Device limitations",
            "Cost concerns",
            "Training requirements"
        ],
        resolution_strategy="Protocol adherence, staff education, device maintenance",
        entity_scope="Electrosurgery procedures",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AORN Electrosurgery Safety Guidelines, 2016"
    ),
    DoctrineBlock(
        topic="Blood Loss Estimation and Transfusion Thresholds",
        keywords=["blood loss", "transfusion", "threshold", "hemoglobin", "estimation"],
        conclusion_template="Blood loss estimated and transfusion threshold determined based on patient factors.",
        reasoning_framework="""
        Blood loss estimation during surgery is critical for timely transfusion decisions. 
        Methods include visual estimation, gravimetric measurement, and laboratory assessment. 
        Transfusion thresholds are guided by hemoglobin levels, patient comorbidities, and hemodynamic stability. 
        Key factors include accuracy of estimation, patient risk factors, and institutional protocols. 
        Primary authorities are transfusion societies, surgical societies, and institutional guidelines. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include surgeon preference for restrictive or liberal transfusion. 
        Counter arguments focus on risks of transfusion and underestimation of blood loss. 
        Resolution strategy involves protocol-driven decision-making and multidisciplinary review. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Estimation accuracy",
            "Hemoglobin levels",
            "Patient comorbidities",
            "Hemodynamic stability",
            "Institutional protocols"
        ],
        primary_authority=["AABB", "American College of Surgeons", "Institutional Transfusion Committee"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Surgeon favoring restrictive transfusion",
        counter_arguments=[
            "Risks of transfusion",
            "Underestimation of blood loss",
            "Variability in thresholds"
        ],
        resolution_strategy="Protocol-driven decision-making, multidisciplinary review",
        entity_scope="All surgical patients",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AABB Transfusion Guidelines, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Instrument Sterilization Methods",
        keywords=["sterilization", "instruments", "autoclave", "disinfection", "infection control"],
        conclusion_template="Sterilization method selected and validated for surgical instruments.",
        reasoning_framework="""
        Surgical instrument sterilization is achieved through methods such as steam autoclaving, ethylene oxide gas, hydrogen peroxide plasma, and chemical disinfection. 
        Selection depends on instrument material, complexity, and manufacturer recommendations. 
        Validation includes biological and chemical indicators. 
        Key factors include instrument compatibility, sterilization efficacy, and process validation. 
        Primary authorities are CDC, FDA, and institutional infection control committees. 
        The burden holder is the sterile processing department. 
        Adversary positions may include resource limitations or instrument damage concerns. 
        Counter arguments focus on cost and turnaround time. 
        Resolution strategy involves adherence to validated protocols and routine monitoring. 
        Entity scope includes all reusable surgical instruments.
        """,
        key_factors=[
            "Instrument compatibility",
            "Sterilization efficacy",
            "Process validation",
            "Manufacturer recommendations",
            "Turnaround time"
        ],
        primary_authority=["CDC", "FDA", "Institutional Infection Control Committee"],
        burden_holder="Sterile Processing Department",
        adversary_position="Surgeon concerned about instrument damage",
        counter_arguments=[
            "Cost",
            "Turnaround time",
            "Instrument longevity"
        ],
        resolution_strategy="Adherence to validated protocols, routine monitoring",
        entity_scope="Reusable surgical instruments",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Guidelines for Disinfection and Sterilization, 2008"
    ),
    DoctrineBlock(
        topic="Surgical Patient Positioning and Pressure Injury Prevention",
        keywords=["positioning", "pressure injury", "ulcers", "surgery", "prevention"],
        conclusion_template="Patient positioning and pressure injury prevention measures documented for procedure.",
        reasoning_framework="""
        Proper patient positioning during surgery is essential to prevent pressure injuries, nerve damage, and musculoskeletal complications. 
        Measures include padding, repositioning, and use of pressure-relieving devices. 
        Key factors include procedure duration, patient risk factors (obesity, diabetes), and team vigilance. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the surgical and perioperative nursing teams. 
        Adversary positions may include time constraints or resource limitations. 
        Counter arguments focus on workflow disruption and cost. 
        Resolution strategy involves protocol adherence, education, and monitoring. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Procedure duration",
            "Patient risk factors",
            "Padding and positioning devices",
            "Team vigilance",
            "Documentation"
        ],
        primary_authority=["AORN", "American College of Surgeons", "Institutional Nursing Committee"],
        burden_holder="Surgical and Perioperative Nursing Teams",
        adversary_position="Surgeon prioritizing speed over safety",
        counter_arguments=[
            "Workflow disruption",
            "Cost",
            "Resource limitations"
        ],
        resolution_strategy="Protocol adherence, education, monitoring",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AORN Guidelines for Positioning, 2019"
    ),
    DoctrineBlock(
        topic="Preoperative Fasting Guidelines",
        keywords=["preoperative", "fasting", "NPO", "anesthesia", "guidelines"],
        conclusion_template="Preoperative fasting guidelines followed and documented for patient.",
        reasoning_framework="""
        Preoperative fasting reduces risk of aspiration during anesthesia. 
        Guidelines recommend minimum fasting periods for clear liquids (2 hours), breast milk (4 hours), and solids (6-8 hours). 
        Key factors include patient age, comorbidities, procedure urgency, and compliance. 
        Primary authorities are anesthesia societies and institutional protocols. 
        The burden holder is the anesthesia team. 
        Adversary positions may include urgent surgery or patient noncompliance. 
        Counter arguments focus on risk of dehydration and hypoglycemia. 
        Resolution strategy involves individualized assessment and documentation. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Fasting duration",
            "Patient age",
            "Comorbidities",
            "Procedure urgency",
            "Compliance"
        ],
        primary_authority=["ASA", "Institutional Anesthesia Guidelines"],
        burden_holder="Anesthesia Team",
        adversary_position="Surgeon requesting urgent procedure",
        counter_arguments=[
            "Dehydration risk",
            "Hypoglycemia",
            "Patient discomfort"
        ],
        resolution_strategy="Individualized assessment, documentation",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Preoperative Fasting Guidelines, 2017"
    ),
    DoctrineBlock(
        topic="Antibiotic Prophylaxis in Surgery",
        keywords=["antibiotic", "prophylaxis", "surgery", "infection prevention", "timing"],
        conclusion_template="Antibiotic prophylaxis administered within recommended timeframe for procedure.",
        reasoning_framework="""
        Antibiotic prophylaxis reduces risk of surgical site infection. 
        Guidelines recommend administration within 60 minutes before incision, with selection based on procedure and patient allergies. 
        Key factors include timing, selection, patient risk factors, and documentation. 
        Primary authorities are CDC, surgical societies, and institutional protocols. 
        The burden holder is the anesthesia and surgical teams. 
        Adversary positions may include patient allergies or resistance concerns. 
        Counter arguments focus on antibiotic stewardship and resistance. 
        Resolution strategy involves adherence to guidelines and audit. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Timing of administration",
            "Antibiotic selection",
            "Patient allergies",
            "Documentation",
            "Procedure type"
        ],
        primary_authority=["CDC", "American College of Surgeons", "Institutional Infection Control Committee"],
        burden_holder="Anesthesia and Surgical Teams",
        adversary_position="Patient with allergy",
        counter_arguments=[
            "Antibiotic resistance",
            "Stewardship concerns",
            "Documentation errors"
        ],
        resolution_strategy="Adherence to guidelines, audit",
        entity_scope="All surgical procedures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Guidelines for SSI Prevention, 2017"
    ),
    DoctrineBlock(
        topic="Venous Thromboembolism (VTE) Prophylaxis",
        keywords=["VTE", "thrombosis", "prophylaxis", "surgery", "risk assessment"],
        conclusion_template="VTE risk assessed and prophylaxis measures implemented for patient.",
        reasoning_framework="""
        VTE prophylaxis is essential to reduce risk of deep vein thrombosis and pulmonary embolism in surgical patients. 
        Measures include pharmacologic (heparin, LMWH) and mechanical (compression devices) interventions. 
        Key factors include patient risk assessment, contraindications, and protocol adherence. 
        Primary authorities are surgical societies, hematology societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include bleeding risk or patient refusal. 
        Counter arguments focus on risk-benefit analysis and alternative measures. 
        Resolution strategy involves individualized assessment and documentation. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Risk assessment",
            "Contraindications",
            "Protocol adherence",
            "Patient compliance",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "American Society of Hematology", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Patient refusing prophylaxis",
        counter_arguments=[
            "Bleeding risk",
            "Patient refusal",
            "Contraindications"
        ],
        resolution_strategy="Individualized assessment, documentation",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACCP Guidelines for VTE Prophylaxis, 2012"
    ),
    DoctrineBlock(
        topic="Intraoperative Temperature Management",
        keywords=["temperature", "hypothermia", "intraoperative", "warming", "patient safety"],
        conclusion_template="Intraoperative temperature management measures implemented and documented.",
        reasoning_framework="""
        Maintaining normothermia during surgery reduces risk of complications such as SSI, coagulopathy, and delayed recovery. 
        Measures include forced-air warming, warmed IV fluids, and temperature monitoring. 
        Key factors include procedure duration, patient risk factors, and device availability. 
        Primary authorities are anesthesia societies, surgical societies, and institutional protocols. 
        The burden holder is the anesthesia team. 
        Adversary positions may include resource limitations or device malfunction. 
        Counter arguments focus on workflow disruption and cost. 
        Resolution strategy involves protocol adherence and device maintenance. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Procedure duration",
            "Patient risk factors",
            "Device availability",
            "Temperature monitoring",
            "Documentation"
        ],
        primary_authority=["ASA", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Anesthesia Team",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Workflow disruption",
            "Cost",
            "Device malfunction"
        ],
        resolution_strategy="Protocol adherence, device maintenance",
        entity_scope="All surgical patients",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Guidelines for Temperature Management, 2015"
    ),
    DoctrineBlock(
        topic="Surgical Counts and Prevention of Retained Foreign Objects",
        keywords=["surgical counts", "retained objects", "safety", "sponges", "instruments"],
        conclusion_template="Surgical counts completed and documented to prevent retained foreign objects.",
        reasoning_framework="""
        Surgical counts of sponges, instruments, and needles are performed to prevent retained foreign objects. 
        Counts are conducted at key procedural stages and discrepancies are resolved before closure. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the circulating nurse and surgical team. 
        Adversary positions may include time constraints or workflow disruption. 
        Counter arguments focus on technology solutions and human error. 
        Resolution strategy involves protocol adherence, audit, and use of adjunct technologies. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Team communication",
            "Protocol adherence",
            "Documentation",
            "Technology adjuncts",
            "Discrepancy resolution"
        ],
        primary_authority=["AORN", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Circulating Nurse",
        adversary_position="Surgeon prioritizing speed",
        counter_arguments=[
            "Workflow disruption",
            "Human error",
            "Technology limitations"
        ],
        resolution_strategy="Protocol adherence, audit, adjunct technologies",
        entity_scope="All surgical procedures",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AORN Guidelines for Surgical Counts, 2016"
    ),
    DoctrineBlock(
        topic="Universal Protocol for Preventing Wrong Site Surgery",
        keywords=["universal protocol", "wrong site", "surgery", "patient safety", "verification"],
        conclusion_template="Universal protocol completed to verify patient, procedure, and site.",
        reasoning_framework="""
        The Universal Protocol requires preoperative verification, site marking, and a time out to prevent wrong site, wrong procedure, or wrong patient surgery. 
        Key factors include team communication, checklist adherence, and documentation. 
        Primary authorities are The Joint Commission, surgical societies, and institutional protocols. 
        The burden holder is the surgical team and circulating nurse. 
        Adversary positions may include workflow disruption or resistance to protocol. 
        Counter arguments focus on evidence of improved safety and reduced errors. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Preoperative verification",
            "Site marking",
            "Time out",
            "Team communication",
            "Documentation"
        ],
        primary_authority=["The Joint Commission", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical Team",
        adversary_position="Surgeon resisting protocol",
        counter_arguments=[
            "Workflow disruption",
            "Checklist fatigue",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="The Joint Commission Universal Protocol, 2003"
    ),
    DoctrineBlock(
        topic="Informed Consent for Surgery",
        keywords=["informed consent", "surgery", "patient rights", "documentation", "legal"],
        conclusion_template="Informed consent obtained and documented for surgical procedure.",
        reasoning_framework="""
        Informed consent requires disclosure of risks, benefits, alternatives, and obtaining voluntary agreement from the patient. 
        Key factors include patient comprehension, documentation, and legal requirements. 
        Primary authorities are legal statutes, surgical societies, and institutional protocols. 
        The burden holder is the operating surgeon. 
        Adversary positions may include patient refusal or lack of comprehension. 
        Counter arguments focus on language barriers and urgency. 
        Resolution strategy involves use of interpreters, written materials, and documentation. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Disclosure of risks and benefits",
            "Patient comprehension",
            "Documentation",
            "Legal requirements",
            "Alternatives"
        ],
        primary_authority=["Legal Statutes", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Operating Surgeon",
        adversary_position="Patient refusing consent",
        counter_arguments=[
            "Language barriers",
            "Urgency",
            "Patient comprehension"
        ],
        resolution_strategy="Use of interpreters, written materials, documentation",
        entity_scope="All surgical procedures",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Legal Statutes on Informed Consent"
    ),
    DoctrineBlock(
        topic="Postoperative Pain Management",
        keywords=["pain management", "postoperative", "analgesia", "opioids", "multimodal"],
        conclusion_template="Postoperative pain management plan implemented and documented.",
        reasoning_framework="""
        Effective postoperative pain management improves recovery and patient satisfaction. 
        Multimodal analgesia combines opioids, NSAIDs, local anesthetics, and non-pharmacologic measures. 
        Key factors include pain assessment, patient risk factors, and protocol adherence. 
        Primary authorities are pain societies, surgical societies, and institutional protocols. 
        The burden holder is the anesthesia and surgical teams. 
        Adversary positions may include opioid stewardship concerns or patient refusal. 
        Counter arguments focus on risk of addiction and adverse effects. 
        Resolution strategy involves individualized assessment and documentation. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Pain assessment",
            "Protocol adherence",
            "Patient risk factors",
            "Opioid stewardship",
            "Documentation"
        ],
        primary_authority=["American Pain Society", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Anesthesia and Surgical Teams",
        adversary_position="Patient refusing opioids",
        counter_arguments=[
            "Risk of addiction",
            "Adverse effects",
            "Opioid stewardship"
        ],
        resolution_strategy="Individualized assessment, documentation",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="APS Guidelines for Postoperative Pain Management, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Hand Hygiene Protocols",
        keywords=["hand hygiene", "surgery", "infection prevention", "protocol", "scrubbing"],
        conclusion_template="Surgical hand hygiene protocol followed and documented before procedure.",
        reasoning_framework="""
        Surgical hand hygiene reduces risk of SSI. 
        Protocols include traditional scrubbing with antiseptic soap or alcohol-based hand rubs. 
        Key factors include technique, duration, and compliance. 
        Primary authorities are CDC, WHO, and institutional infection control committees. 
        The burden holder is the surgical team. 
        Adversary positions may include workflow disruption or skin irritation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Technique",
            "Duration",
            "Compliance",
            "Antiseptic selection",
            "Documentation"
        ],
        primary_authority=["CDC", "WHO", "Institutional Infection Control Committee"],
        burden_holder="Surgical Team",
        adversary_position="Surgeon resisting protocol",
        counter_arguments=[
            "Workflow disruption",
            "Skin irritation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Guidelines for Hand Hygiene, 2002"
    ),
    DoctrineBlock(
        topic="Surgical Smoke Evacuation",
        keywords=["surgical smoke", "evacuation", "safety", "electrosurgery", "health"],
        conclusion_template="Surgical smoke evacuation measures implemented and documented for procedure.",
        reasoning_framework="""
        Surgical smoke contains hazardous chemicals and biological material. 
        Evacuation systems reduce exposure for staff and patients. 
        Key factors include device availability, procedure type, and compliance. 
        Primary authorities are OSHA, surgical societies, and institutional safety committees. 
        The burden holder is the surgical team. 
        Adversary positions may include device cost or workflow disruption. 
        Counter arguments focus on evidence of health risks and compliance challenges. 
        Resolution strategy involves protocol adherence, education, and device maintenance. 
        Entity scope includes procedures generating surgical smoke.
        """,
        key_factors=[
            "Device availability",
            "Procedure type",
            "Compliance",
            "Health risks",
            "Documentation"
        ],
        primary_authority=["OSHA", "American College of Surgeons", "Institutional Safety Committee"],
        burden_holder="Surgical Team",
        adversary_position="Surgeon resisting device use",
        counter_arguments=[
            "Device cost",
            "Workflow disruption",
            "Compliance challenges"
        ],
        resolution_strategy="Protocol adherence, education, device maintenance",
        entity_scope="Procedures generating surgical smoke",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Guidelines for Surgical Smoke, 2015"
    ),
    DoctrineBlock(
        topic="Surgical Fire Prevention",
        keywords=["surgical fire", "prevention", "safety", "electrosurgery", "oxygen"],
        conclusion_template="Surgical fire prevention measures implemented and documented for procedure.",
        reasoning_framework="""
        Surgical fires are rare but catastrophic events. 
        Prevention includes minimizing oxygen concentration, proper draping, and device maintenance. 
        Key factors include procedure type, device settings, and team vigilance. 
        Primary authorities are surgical societies, fire safety organizations, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or device limitations. 
        Counter arguments focus on evidence of risk and compliance challenges. 
        Resolution strategy involves protocol adherence, education, and audit. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Oxygen concentration",
            "Device settings",
            "Team vigilance",
            "Procedure type",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "NFPA", "Institutional Safety Committee"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Surgeon resisting protocol",
        counter_arguments=[
            "Workflow disruption",
            "Device limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Protocol adherence, education, audit",
        entity_scope="All surgical procedures",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA Guidelines for Surgical Fire Prevention, 2014"
    ),
    DoctrineBlock(
        topic="Surgical Site Marking",
        keywords=["site marking", "surgery", "patient safety", "verification", "protocol"],
        conclusion_template="Surgical site marked and verified according to protocol.",
        reasoning_framework="""
        Surgical site marking prevents wrong site surgery. 
        Protocols require marking by the operating surgeon and verification by the team. 
        Key factors include patient involvement, team communication, and documentation. 
        Primary authorities are The Joint Commission, surgical societies, and institutional protocols. 
        The burden holder is the operating surgeon. 
        Adversary positions may include workflow disruption or patient refusal. 
        Counter arguments focus on evidence of improved safety and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Patient involvement",
            "Team communication",
            "Documentation",
            "Protocol adherence",
            "Verification"
        ],
        primary_authority=["The Joint Commission", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Operating Surgeon",
        adversary_position="Patient refusing marking",
        counter_arguments=[
            "Workflow disruption",
            "Patient refusal",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="The Joint Commission Universal Protocol, 2003"
    ),
    DoctrineBlock(
        topic="Surgical Team Briefing and Debriefing",
        keywords=["team briefing", "debriefing", "surgery", "communication", "safety"],
        conclusion_template="Surgical team briefing and debriefing completed and documented for procedure.",
        reasoning_framework="""
        Team briefing before surgery and debriefing after improves communication, safety, and outcomes. 
        Key factors include team participation, protocol adherence, and documentation. 
        Primary authorities are surgical societies, safety committees, and institutional protocols. 
        The burden holder is the surgical team leader. 
        Adversary positions may include workflow disruption or resistance to protocol. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Team participation",
            "Protocol adherence",
            "Documentation",
            "Communication",
            "Feedback"
        ],
        primary_authority=["American College of Surgeons", "Institutional Safety Committee"],
        burden_holder="Surgical Team Leader",
        adversary_position="Surgeon resisting protocol",
        counter_arguments=[
            "Workflow disruption",
            "Compliance challenges",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Team Briefing, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Specimen Handling and Identification",
        keywords=["specimen handling", "identification", "surgery", "pathology", "safety"],
        conclusion_template="Surgical specimen handling and identification protocols followed and documented.",
        reasoning_framework="""
        Proper handling and identification of surgical specimens prevents errors and ensures accurate diagnosis. 
        Protocols require labeling, documentation, and communication with pathology. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are surgical societies, pathology associations, and institutional protocols. 
        The burden holder is the surgical team and circulating nurse. 
        Adversary positions may include workflow disruption or labeling errors. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Labeling",
            "Documentation",
            "Team communication",
            "Protocol adherence",
            "Pathology coordination"
        ],
        primary_authority=["American College of Surgeons", "College of American Pathologists", "Institutional Protocols"],
        burden_holder="Surgical Team and Circulating Nurse",
        adversary_position="Workflow disruption",
        counter_arguments=[
            "Labeling errors",
            "Compliance challenges",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CAP Guidelines for Specimen Handling, 2015"
    ),
    DoctrineBlock(
        topic="Surgical Wound Classification",
        keywords=["wound classification", "surgery", "infection risk", "protocol", "documentation"],
        conclusion_template="Surgical wound classified and documented according to protocol.",
        reasoning_framework="""
        Surgical wound classification informs infection risk and postoperative management. 
        Categories include clean, clean-contaminated, contaminated, and dirty-infected. 
        Key factors include procedure type, contamination risk, and documentation. 
        Primary authorities are surgical societies and institutional protocols. 
        The burden holder is the surgical team. 
        Adversary positions may include workflow disruption or classification errors. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Procedure type",
            "Contamination risk",
            "Documentation",
            "Protocol adherence",
            "Classification accuracy"
        ],
        primary_authority=["American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical Team",
        adversary_position="Workflow disruption",
        counter_arguments=[
            "Classification errors",
            "Compliance challenges",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Wound Classification, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Drain Management",
        keywords=["drain management", "surgery", "postoperative", "infection prevention", "protocol"],
        conclusion_template="Surgical drain management plan implemented and documented.",
        reasoning_framework="""
        Proper management of surgical drains reduces risk of infection and improves outcomes. 
        Protocols include selection, placement, monitoring, and removal. 
        Key factors include drain type, indication, patient risk factors, and documentation. 
        Primary authorities are surgical societies and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or patient refusal. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients with drains.
        """,
        key_factors=[
            "Drain type",
            "Indication",
            "Patient risk factors",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Patient refusing drain",
        counter_arguments=[
            "Workflow disruption",
            "Patient refusal",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="Surgical patients with drains",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Drain Management, 2018"
    ),
    DoctrineBlock(
        topic="Surgical Antibiotic Stewardship",
        keywords=["antibiotic stewardship", "surgery", "infection prevention", "protocol", "resistance"],
        conclusion_template="Antibiotic stewardship measures implemented and documented for surgical procedure.",
        reasoning_framework="""
        Antibiotic stewardship reduces resistance and improves outcomes. 
        Protocols include appropriate selection, dosing, and duration. 
        Key factors include patient risk factors, procedure type, and documentation. 
        Primary authorities are CDC, surgical societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include resistance to protocol or patient allergies. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Selection",
            "Dosing",
            "Duration",
            "Patient risk factors",
            "Documentation"
        ],
        primary_authority=["CDC", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Patient with allergy",
        counter_arguments=[
            "Resistance to protocol",
            "Patient allergies",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Guidelines for Antibiotic Stewardship, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Fluid Management",
        keywords=["fluid management", "surgery", "perioperative", "protocol", "outcomes"],
        conclusion_template="Surgical fluid management plan implemented and documented for patient.",
        reasoning_framework="""
        Proper fluid management reduces risk of complications such as hypovolemia and fluid overload. 
        Protocols include assessment, monitoring, and individualized therapy. 
        Key factors include patient risk factors, procedure type, and documentation. 
        Primary authorities are anesthesia societies, surgical societies, and institutional protocols. 
        The burden holder is the anesthesia and surgical teams. 
        Adversary positions may include resistance to protocol or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Assessment",
            "Monitoring",
            "Individualized therapy",
            "Patient risk factors",
            "Documentation"
        ],
        primary_authority=["ASA", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Anesthesia and Surgical Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Resistance to protocol",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Guidelines for Fluid Management, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Identification Protocol",
        keywords=["patient identification", "surgery", "safety", "protocol", "verification"],
        conclusion_template="Patient identification protocol followed and documented before procedure.",
        reasoning_framework="""
        Proper patient identification prevents errors and improves safety. 
        Protocols require verification using multiple identifiers and documentation. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are The Joint Commission, surgical societies, and institutional protocols. 
        The burden holder is the surgical team and circulating nurse. 
        Adversary positions may include workflow disruption or resistance to protocol. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical procedures.
        """,
        key_factors=[
            "Multiple identifiers",
            "Team communication",
            "Protocol adherence",
            "Documentation",
            "Verification"
        ],
        primary_authority=["The Joint Commission", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical Team and Circulating Nurse",
        adversary_position="Workflow disruption",
        counter_arguments=[
            "Resistance to protocol",
            "Workflow disruption",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical procedures",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="The Joint Commission Patient Identification Protocol, 2003"
    ),
    DoctrineBlock(
        topic="Surgical Patient Allergies Documentation",
        keywords=["allergies", "documentation", "surgery", "patient safety", "protocol"],
        conclusion_template="Patient allergies documented and verified before procedure.",
        reasoning_framework="""
        Proper documentation and verification of patient allergies prevents adverse reactions. 
        Protocols require review, documentation, and communication with the team. 
        Key factors include patient history, team communication, and protocol adherence. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Patient history",
            "Team communication",
            "Protocol adherence",
            "Documentation",
            "Verification"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Allergy Documentation, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Medication Reconciliation",
        keywords=["medication reconciliation", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Medication reconciliation completed and documented for patient before procedure.",
        reasoning_framework="""
        Medication reconciliation prevents errors and adverse drug events. 
        Protocols require review, documentation, and communication with the team. 
        Key factors include patient history, team communication, and protocol adherence. 
        Primary authorities are surgical societies, pharmacy associations, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Patient history",
            "Team communication",
            "Protocol adherence",
            "Documentation",
            "Verification"
        ],
        primary_authority=["American College of Surgeons", "ASHP", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASHP Guidelines for Medication Reconciliation, 2015"
    ),
    DoctrineBlock(
        topic="Surgical Patient Preoperative Assessment",
        keywords=["preoperative assessment", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Preoperative assessment completed and documented for patient before procedure.",
        reasoning_framework="""
        Preoperative assessment identifies risk factors and optimizes patient safety. 
        Protocols require review of history, physical examination, and laboratory tests. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Patient risk factors",
            "Team communication",
            "Protocol adherence",
            "Documentation",
            "Verification"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASA Guidelines for Preoperative Assessment, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Postoperative Monitoring",
        keywords=["postoperative monitoring", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Postoperative monitoring plan implemented and documented for patient.",
        reasoning_framework="""
        Postoperative monitoring detects complications early and improves outcomes. 
        Protocols require assessment of vital signs, pain, and wound status. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Vital signs",
            "Pain assessment",
            "Wound status",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Postoperative Monitoring, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Discharge Planning",
        keywords=["discharge planning", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Discharge planning completed and documented for patient after procedure.",
        reasoning_framework="""
        Discharge planning ensures safe transition from hospital to home or other care settings. 
        Protocols require assessment of patient needs, education, and follow-up arrangements. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Patient needs",
            "Education",
            "Follow-up arrangements",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "AORN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Discharge Planning, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Family Communication",
        keywords=["family communication", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Family communication plan implemented and documented for patient before and after procedure.",
        reasoning_framework="""
        Effective communication with patient families improves satisfaction and outcomes. 
        Protocols require timely updates, education, and documentation. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Timely updates",
            "Education",
            "Protocol adherence",
            "Documentation",
            "Family engagement"
        ],
        primary_authority=["American College of Surgeons", "AORN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Family Communication, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Privacy and Confidentiality",
        keywords=["privacy", "confidentiality", "surgery", "patient rights", "protocol"],
        conclusion_template="Patient privacy and confidentiality maintained and documented during surgical care.",
        reasoning_framework="""
        Maintaining patient privacy and confidentiality is a legal and ethical requirement. 
        Protocols require secure handling of patient information and communication. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are legal statutes, surgical societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or inadvertent disclosure. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Secure handling of information",
            "Protocol adherence",
            "Documentation",
            "Team communication",
            "Legal requirements"
        ],
        primary_authority=["Legal Statutes", "American College of Surgeons", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Inadvertent disclosure",
        counter_arguments=[
            "Workflow disruption",
            "Compliance challenges",
            "Legal consequences"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HIPAA Privacy Rule"
    ),
    DoctrineBlock(
        topic="Surgical Patient Cultural Competency",
        keywords=["cultural competency", "surgery", "patient safety", "protocol", "communication"],
        conclusion_template="Cultural competency measures implemented and documented for patient during surgical care.",
        reasoning_framework="""
        Cultural competency improves patient satisfaction and outcomes. 
        Protocols require assessment of cultural needs, use of interpreters, and education. 
        Key factors include team communication, protocol adherence, and documentation. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or resistance to protocol. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Assessment of cultural needs",
            "Use of interpreters",
            "Education",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "AORN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Resistance to protocol",
        counter_arguments=[
            "Workflow disruption",
            "Compliance challenges",
            "Perceived redundancy"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Cultural Competency, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Emergency Response Protocol",
        keywords=["emergency response", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Emergency response protocol implemented and documented for patient during surgical care.",
        reasoning_framework="""
        Emergency response protocols ensure timely intervention during surgical emergencies. 
        Protocols require team communication, equipment readiness, and documentation. 
        Key factors include team training, protocol adherence, and documentation. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Team training",
            "Equipment readiness",
            "Protocol adherence",
            "Documentation",
            "Communication"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Workflow disruption",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Emergency Response, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Blood Conservation Strategies",
        keywords=["blood conservation", "surgery", "patient safety", "protocol", "transfusion"],
        conclusion_template="Blood conservation strategies implemented and documented for patient during surgical care.",
        reasoning_framework="""
        Blood conservation reduces transfusion risks and improves outcomes. 
        Strategies include preoperative optimization, intraoperative techniques, and restrictive transfusion thresholds. 
        Key factors include patient risk factors, procedure type, and documentation. 
        Primary authorities are surgical societies, transfusion societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include resistance to protocol or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Preoperative optimization",
            "Intraoperative techniques",
            "Restrictive transfusion thresholds",
            "Patient risk factors",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "AABB", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Resistance to protocol",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AABB Guidelines for Blood Conservation, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Preoperative Optimization",
        keywords=["preoperative optimization", "surgery", "patient safety", "protocol", "risk reduction"],
        conclusion_template="Preoperative optimization measures implemented and documented for patient before procedure.",
        reasoning_framework="""
        Preoperative optimization reduces surgical risk and improves outcomes. 
        Measures include management of comorbidities, nutritional support, and smoking cessation. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and anesthesia teams. 
        Adversary positions may include workflow disruption or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Management of comorbidities",
            "Nutritional support",
            "Smoking cessation",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Anesthesia Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Workflow disruption",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Preoperative Optimization, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Postoperative Complication Management",
        keywords=["complication management", "postoperative", "surgery", "patient safety", "protocol"],
        conclusion_template="Postoperative complication management plan implemented and documented for patient.",
        reasoning_framework="""
        Effective management of postoperative complications improves outcomes. 
        Protocols require early detection, intervention, and documentation. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, anesthesia societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Early detection",
            "Intervention",
            "Patient risk factors",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "ASA", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Workflow disruption",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Complication Management, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Postoperative Nutrition",
        keywords=["postoperative nutrition", "surgery", "patient safety", "protocol", "recovery"],
        conclusion_template="Postoperative nutrition plan implemented and documented for patient.",
        reasoning_framework="""
        Proper postoperative nutrition improves recovery and outcomes. 
        Protocols require assessment, individualized therapy, and documentation. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, nutrition societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or resource limitations. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Assessment",
            "Individualized therapy",
            "Patient risk factors",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "ASPEN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Resource limitations",
        counter_arguments=[
            "Workflow disruption",
            "Resource limitations",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASPEN Guidelines for Postoperative Nutrition, 2016"
    ),
    DoctrineBlock(
        topic="Surgical Patient Postoperative Mobilization",
        keywords=["postoperative mobilization", "surgery", "patient safety", "protocol", "recovery"],
        conclusion_template="Postoperative mobilization plan implemented and documented for patient.",
        reasoning_framework="""
        Early mobilization after surgery reduces complications and improves outcomes. 
        Protocols require assessment, individualized therapy, and documentation. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, rehabilitation societies, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or patient refusal. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Assessment",
            "Individualized therapy",
            "Patient risk factors",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "AORN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Patient refusing mobilization",
        counter_arguments=[
            "Workflow disruption",
            "Patient refusal",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Postoperative Mobilization, 2017"
    ),
    DoctrineBlock(
        topic="Surgical Patient Postoperative Follow-Up",
        keywords=["postoperative follow-up", "surgery", "patient safety", "protocol", "documentation"],
        conclusion_template="Postoperative follow-up plan implemented and documented for patient.",
        reasoning_framework="""
        Proper follow-up after surgery detects complications and improves outcomes. 
        Protocols require assessment, scheduling, and documentation. 
        Key factors include patient risk factors, team communication, and protocol adherence. 
        Primary authorities are surgical societies, nursing associations, and institutional protocols. 
        The burden holder is the surgical and nursing teams. 
        Adversary positions may include workflow disruption or incomplete documentation. 
        Counter arguments focus on evidence of improved outcomes and compliance challenges. 
        Resolution strategy involves education, audit, and feedback. 
        Entity scope includes all surgical patients.
        """,
        key_factors=[
            "Assessment",
            "Scheduling",
            "Patient risk factors",
            "Protocol adherence",
            "Documentation"
        ],
        primary_authority=["American College of Surgeons", "AORN", "Institutional Protocols"],
        burden_holder="Surgical and Nursing Teams",
        adversary_position="Incomplete documentation",
        counter_arguments=[
            "Workflow disruption",
            "Incomplete documentation",
            "Compliance challenges"
        ],
        resolution_strategy="Education, audit, feedback",
        entity_scope="All surgical patients",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACS Guidelines for Postoperative Follow-Up, 2016"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]