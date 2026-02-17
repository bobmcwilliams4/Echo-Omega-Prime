from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MODERATE = "Moderate"
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
        topic="AO/OTA Fracture Classification System",
        keywords=["fracture", "classification", "AO", "OTA", "orthopedics", "trauma"],
        conclusion_template="Fracture is classified as {fracture_type} according to AO/OTA system.",
        reasoning_framework="""
The AO/OTA Fracture Classification System is a comprehensive scheme for categorizing fractures based on anatomical location, morphology, and severity. The system employs a hierarchical numeric code to describe bone, segment, and fracture type. Classification assists in communication, research, and treatment planning. The process involves radiographic assessment, identification of bone and segment, and determination of fracture pattern (simple, wedge, complex). The system is updated periodically to reflect advances in understanding. Accurate classification requires familiarity with system rules and radiographic interpretation. The AO/OTA system is widely adopted in trauma centers globally and forms the basis for multicenter studies and registries.
""",
        key_factors=[
            "Anatomical location",
            "Fracture morphology",
            "Severity",
            "Radiographic interpretation",
            "AO/OTA coding rules"
        ],
        primary_authority=[
            "AO Foundation",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Alternative classification systems (e.g., Gustilo-Anderson for open fractures)",
        counter_arguments=[
            "Complexity of the system",
            "Interobserver variability",
            "Potential for misclassification"
        ],
        resolution_strategy="Standardized training and use of reference materials; multidisciplinary review.",
        entity_scope="Orthopedic trauma cases",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AO/OTA Fracture and Dislocation Classification Compendium (2018)"
    ),
    DoctrineBlock(
        topic="Gustilo-Anderson Open Fracture Classification",
        keywords=["open fracture", "classification", "Gustilo", "Anderson", "infection risk"],
        conclusion_template="Open fracture is classified as Gustilo-Anderson Type {type}.",
        reasoning_framework="""
The Gustilo-Anderson Classification is the standard for categorizing open fractures based on wound size, contamination, and soft tissue injury. The system divides open fractures into Types I, II, IIIA, IIIB, and IIIC, with increasing severity and risk of complications. Type III fractures are further subdivided based on the need for vascular repair and extent of soft tissue damage. Classification guides antibiotic selection, surgical timing, and prognosis. Accurate classification requires initial and intraoperative assessment. The system is validated by decades of clinical use and correlates with infection and nonunion rates.
""",
        key_factors=[
            "Wound size",
            "Degree of contamination",
            "Soft tissue injury",
            "Vascular involvement"
        ],
        primary_authority=[
            "Gustilo RB",
            "Anderson JT",
            "Journal of Bone and Joint Surgery"
        ],
        burden_holder="Orthopedic trauma surgeon",
        adversary_position="Alternative open fracture classification systems",
        counter_arguments=[
            "Subjectivity in classification",
            "Changes after initial debridement",
            "Interobserver variability"
        ],
        resolution_strategy="Reassessment after initial debridement; consensus classification.",
        entity_scope="Open fracture management",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gustilo RB, Anderson JT. JBJS 1976;58(4):453-8"
    ),
    DoctrineBlock(
        topic="Total Hip Arthroplasty: Cemented vs Uncemented",
        keywords=["hip arthroplasty", "THA", "cemented", "uncemented", "prosthesis"],
        conclusion_template="Total hip arthroplasty is recommended as {fixation_type} fixation based on patient factors.",
        reasoning_framework="""
The choice between cemented and uncemented fixation in total hip arthroplasty (THA) depends on patient age, bone quality, and surgeon preference. Cemented fixation is preferred in elderly patients with poor bone stock, providing immediate stability. Uncemented fixation relies on biological ingrowth and is favored in younger patients with good bone quality. Randomized trials and registry data support both methods, with similar long-term outcomes. Complications differ: cemented fixation may increase cardiopulmonary risk, while uncemented fixation risks early loosening. Decision-making incorporates radiographic assessment, patient comorbidities, and implant design.
""",
        key_factors=[
            "Patient age",
            "Bone quality",
            "Comorbidities",
            "Implant design",
            "Surgeon experience"
        ],
        primary_authority=[
            "National Joint Registry",
            "AAOS Clinical Practice Guidelines"
        ],
        burden_holder="Operating orthopedic surgeon",
        adversary_position="Universal preference for one fixation method",
        counter_arguments=[
            "Registry data favoring uncemented fixation in younger patients",
            "Cemented fixation in elderly reduces periprosthetic fracture risk"
        ],
        resolution_strategy="Individualized approach based on patient and implant factors.",
        entity_scope="Elective hip arthroplasty",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAOS Clinical Practice Guideline: Hip Arthroplasty"
    ),
    DoctrineBlock(
        topic="Total Knee Arthroplasty: Mechanical vs Kinematic Alignment",
        keywords=["knee arthroplasty", "TKA", "mechanical alignment", "kinematic alignment"],
        conclusion_template="Total knee arthroplasty is performed using {alignment_strategy} alignment.",
        reasoning_framework="""
Mechanical alignment aims for neutral limb alignment, reducing implant wear and improving longevity. Kinematic alignment restores native joint anatomy, potentially improving function and patient satisfaction. Randomized studies show comparable outcomes, but mechanical alignment remains standard due to long-term data. Kinematic alignment may benefit select patients with preoperative deformity. Decision-making involves preoperative imaging, patient anatomy, and intraoperative assessment. Both approaches require precise surgical technique and implant positioning.
""",
        key_factors=[
            "Preoperative limb alignment",
            "Patient anatomy",
            "Implant design",
            "Surgeon experience"
        ],
        primary_authority=[
            "AAOS",
            "Australian Orthopaedic Association National Joint Replacement Registry"
        ],
        burden_holder="Operating surgeon",
        adversary_position="Exclusive use of mechanical alignment",
        counter_arguments=[
            "Lack of long-term data for kinematic alignment",
            "Potential for increased implant wear"
        ],
        resolution_strategy="Shared decision-making; patient-specific alignment strategy.",
        entity_scope="Elective knee arthroplasty",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AOA NJRR Annual Report"
    ),
    DoctrineBlock(
        topic="Lumbar Spine: Fusion vs Disc Arthroplasty",
        keywords=["lumbar spine", "fusion", "disc arthroplasty", "degenerative disc disease"],
        conclusion_template="Treatment for lumbar degenerative disc disease is {procedure_type}.",
        reasoning_framework="""
Lumbar fusion is the traditional treatment for degenerative disc disease, providing pain relief and stability. Disc arthroplasty preserves motion and may reduce adjacent segment disease. Randomized controlled trials show similar outcomes, but arthroplasty is limited to select patients without facet arthropathy or instability. Fusion is indicated for multi-level disease, deformity, or instability. Decision-making includes MRI assessment, patient age, activity level, and comorbidities. Long-term data favor fusion for complex cases; arthroplasty is appropriate for younger, active patients with single-level disease.
""",
        key_factors=[
            "Facet joint integrity",
            "Number of affected levels",
            "Patient age",
            "Activity level",
            "Comorbidities"
        ],
        primary_authority=[
            "North American Spine Society",
            "FDA-approved device studies"
        ],
        burden_holder="Spine surgeon",
        adversary_position="Universal preference for fusion",
        counter_arguments=[
            "Limited indications for arthroplasty",
            "Potential for device failure"
        ],
        resolution_strategy="Patient selection based on imaging and clinical criteria.",
        entity_scope="Lumbar degenerative disc disease",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NASS Evidence-Based Guidelines"
    ),
    DoctrineBlock(
        topic="Adolescent Idiopathic Scoliosis: Lenke Classification",
        keywords=["scoliosis", "Lenke classification", "AIS", "spine deformity"],
        conclusion_template="Adolescent idiopathic scoliosis is classified as Lenke Type {type}.",
        reasoning_framework="""
The Lenke Classification system categorizes adolescent idiopathic scoliosis based on curve type, lumbar modifier, and sagittal thoracic modifier. Accurate classification guides surgical planning, including fusion levels and instrumentation. The system uses radiographic analysis to determine structural and nonstructural curves. Lenke Types 1-6 encompass the spectrum of deformity. The classification is validated by multicenter studies and forms the basis for international consensus on AIS management. Decision-making incorporates radiographic measurements, curve flexibility, and patient symptoms.
""",
        key_factors=[
            "Curve type",
            "Lumbar modifier",
            "Sagittal thoracic modifier",
            "Radiographic flexibility"
        ],
        primary_authority=[
            "Lenke LG",
            "Scoliosis Research Society"
        ],
        burden_holder="Pediatric spine surgeon",
        adversary_position="Alternative classification systems (King-Moe, etc.)",
        counter_arguments=[
            "Complexity of the system",
            "Potential for misclassification"
        ],
        resolution_strategy="Standardized radiographic protocols; multidisciplinary review.",
        entity_scope="Adolescent idiopathic scoliosis",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Lenke LG et al. Spine 2001;26(16):1859-66"
    ),
    DoctrineBlock(
        topic="ACL Reconstruction: Graft Selection BTB vs Hamstring vs Quad Tendon",
        keywords=["ACL reconstruction", "graft selection", "BTB", "hamstring", "quad tendon"],
        conclusion_template="ACL reconstruction is performed using {graft_type} graft.",
        reasoning_framework="""
Graft selection for ACL reconstruction is based on patient age, activity level, and comorbidities. Bone-patellar tendon-bone (BTB) grafts offer high fixation strength and are preferred in athletes, but carry risk of anterior knee pain. Hamstring grafts have lower donor site morbidity and are favored in recreational athletes. Quadriceps tendon grafts are emerging as an alternative with favorable biomechanical properties. Randomized studies show similar outcomes, but graft choice impacts recovery and complication profile. Decision-making incorporates patient preference, surgeon experience, and anatomical considerations.
""",
        key_factors=[
            "Patient age",
            "Activity level",
            "Donor site morbidity",
            "Graft biomechanical properties"
        ],
        primary_authority=[
            "American Orthopaedic Society for Sports Medicine",
            "Meta-analyses of randomized trials"
        ],
        burden_holder="Operating surgeon",
        adversary_position="Universal preference for one graft type",
        counter_arguments=[
            "BTB grafts increase anterior knee pain",
            "Hamstring grafts risk hamstring weakness",
            "Quad tendon grafts lack long-term data"
        ],
        resolution_strategy="Shared decision-making; individualized graft selection.",
        entity_scope="ACL reconstruction",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AOSSM Consensus Statement"
    ),
    DoctrineBlock(
        topic="Rotator Cuff Repair: Indications and Technique Selection",
        keywords=["rotator cuff", "repair", "indications", "technique", "arthroscopic", "open"],
        conclusion_template="Rotator cuff repair is indicated for {tear_type} and performed using {technique}.",
        reasoning_framework="""
Indications for rotator cuff repair include symptomatic full-thickness tears, acute traumatic tears, and failure of conservative management. Technique selection (arthroscopic vs open) depends on tear size, tissue quality, and surgeon expertise. Arthroscopic repair offers faster recovery and less morbidity, while open repair may be necessary for massive tears. Randomized studies show comparable outcomes. Decision-making involves MRI assessment, patient age, comorbidities, and functional demands. Repair is contraindicated in irreparable tears with poor tissue quality.
""",
        key_factors=[
            "Tear size",
            "Tissue quality",
            "Patient age",
            "Comorbidities",
            "Surgeon expertise"
        ],
        primary_authority=[
            "American Shoulder and Elbow Surgeons",
            "AAOS"
        ],
        burden_holder="Shoulder surgeon",
        adversary_position="Universal arthroscopic repair",
        counter_arguments=[
            "Open repair may be superior for massive tears",
            "Arthroscopic repair risks incomplete fixation"
        ],
        resolution_strategy="Technique selection based on tear characteristics and surgeon skill.",
        entity_scope="Rotator cuff pathology",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAOS Clinical Practice Guideline: Rotator Cuff Repair"
    ),
    DoctrineBlock(
        topic="Compartment Syndrome: Diagnosis and Management",
        keywords=["compartment syndrome", "diagnosis", "management", "fasciotomy"],
        conclusion_template="Compartment syndrome is diagnosed and managed by emergent fasciotomy.",
        reasoning_framework="""
Compartment syndrome is a surgical emergency characterized by elevated intracompartmental pressure leading to ischemia. Diagnosis is clinical, based on pain out of proportion, pain with passive stretch, and neurologic deficits. Measurement of compartment pressure (>30 mmHg or within 30 mmHg of diastolic BP) supports diagnosis. Management is emergent fasciotomy to prevent irreversible muscle and nerve damage. Delay increases risk of morbidity. Decision-making requires high clinical suspicion, especially in trauma, crush injury, or reperfusion scenarios.
""",
        key_factors=[
            "Clinical signs",
            "Compartment pressure measurement",
            "Time to intervention",
            "Patient comorbidities"
        ],
        primary_authority=[
            "AAOS",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating physician",
        adversary_position="Reliance on pressure measurement alone",
        counter_arguments=[
            "Pressure measurement may be falsely low",
            "Clinical diagnosis is paramount"
        ],
        resolution_strategy="Immediate surgical intervention based on clinical suspicion.",
        entity_scope="Acute compartment syndrome",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAOS Emergency Management Guidelines"
    ),
    DoctrineBlock(
        topic="Bone Healing: Diamond Concept",
        keywords=["bone healing", "diamond concept", "biology", "mechanical stability"],
        conclusion_template="Bone healing is optimized by addressing all four pillars of the diamond concept.",
        reasoning_framework="""
The Diamond Concept posits that bone healing requires four essential elements: osteogenic cells, osteoconductive scaffold, osteoinductive signals, and mechanical stability. Successful healing involves addressing each pillar through surgical technique, biologics, and fixation. The concept guides management of nonunion and complex fractures. Decision-making includes assessment of biological environment, mechanical stability, and patient factors. Adjuncts such as bone grafts, growth factors, and stable fixation are employed based on deficiency in any pillar.
""",
        key_factors=[
            "Osteogenic cells",
            "Osteoconductive scaffold",
            "Osteoinductive signals",
            "Mechanical stability"
        ],
        primary_authority=[
            "Giannoudis PV",
            "Journal of Bone and Joint Surgery"
        ],
        burden_holder="Operating surgeon",
        adversary_position="Reliance on mechanical stability alone",
        counter_arguments=[
            "Biological environment may be insufficient",
            "Mechanical stability without biology may fail"
        ],
        resolution_strategy="Comprehensive approach addressing all pillars.",
        entity_scope="Fracture healing and nonunion",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Giannoudis PV et al. JBJS Br 2007;89(3):301-9"
    ),
    DoctrineBlock(
        topic="Musculoskeletal MRI: Meniscal Tear Classification",
        keywords=["MRI", "meniscal tear", "classification", "knee", "imaging"],
        conclusion_template="Meniscal tear is classified as {tear_type} based on MRI findings.",
        reasoning_framework="""
MRI is the gold standard for noninvasive diagnosis and classification of meniscal tears. Tear types include longitudinal, horizontal, radial, complex, and root tears. Classification guides treatment: repair is favored for peripheral, longitudinal tears; partial meniscectomy for complex or degenerative tears. Decision-making incorporates MRI findings, patient age, activity level, and symptoms. The accuracy of MRI is validated by arthroscopic correlation studies. Radiologists and orthopedic surgeons collaborate for precise classification.
""",
        key_factors=[
            "Tear morphology",
            "Location",
            "Patient age",
            "Activity level"
        ],
        primary_authority=[
            "Radiological Society of North America",
            "AAOS"
        ],
        burden_holder="Radiologist/orthopedic surgeon",
        adversary_position="Reliance on clinical exam alone",
        counter_arguments=[
            "MRI may miss subtle tears",
            "Clinical exam may be sufficient in select cases"
        ],
        resolution_strategy="Combined clinical and imaging assessment.",
        entity_scope="Knee meniscal pathology",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RSNA MRI Knee Guidelines"
    ),
    DoctrineBlock(
        topic="Femoral Neck Fracture: Garden Classification",
        keywords=["femoral neck fracture", "Garden classification", "hip fracture"],
        conclusion_template="Femoral neck fracture is classified as Garden Type {type}.",
        reasoning_framework="""
The Garden Classification divides femoral neck fractures into four types based on displacement and angulation. Type I and II are incomplete or nondisplaced; Type III and IV are displaced. Classification guides management: internal fixation for nondisplaced, arthroplasty for displaced in elderly. Accurate classification requires AP and lateral radiographs. The system is validated by correlation with outcomes and risk of avascular necrosis. Decision-making incorporates patient age, comorbidities, and fracture morphology.
""",
        key_factors=[
            "Fracture displacement",
            "Angulation",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Garden RS",
            "British Orthopaedic Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Alternative classification systems (Pauwels, etc.)",
        counter_arguments=[
            "Interobserver variability",
            "Complexity in borderline cases"
        ],
        resolution_strategy="Standardized radiographic protocols; multidisciplinary review.",
        entity_scope="Femoral neck fractures",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Garden RS. JBJS Br 1961;43-B: 753-8"
    ),
    DoctrineBlock(
        topic="Intertrochanteric Fracture: Evans Classification",
        keywords=["intertrochanteric fracture", "Evans classification", "hip fracture"],
        conclusion_template="Intertrochanteric fracture is classified as Evans Type {type}.",
        reasoning_framework="""
The Evans Classification categorizes intertrochanteric fractures based on stability. Stable fractures have intact posteromedial cortex; unstable fractures are comminuted. Classification guides choice of fixation device: sliding hip screw for stable, intramedullary nail for unstable. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and fixation failure rates. Decision-making incorporates patient age, comorbidities, and fracture morphology.
""",
        key_factors=[
            "Fracture stability",
            "Comminution",
            "Posteromedial cortex integrity",
            "Patient age"
        ],
        primary_authority=[
            "Evans EM",
            "British Orthopaedic Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal use of intramedullary nail",
        counter_arguments=[
            "Sliding hip screw may fail in unstable fractures",
            "Intramedullary nail may be unnecessary in stable fractures"
        ],
        resolution_strategy="Device selection based on fracture stability.",
        entity_scope="Intertrochanteric fractures",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Evans EM. JBJS Br 1949;31-B: 190-203"
    ),
    DoctrineBlock(
        topic="Pediatric Supracondylar Humerus Fracture: Gartland Classification",
        keywords=["supracondylar fracture", "Gartland classification", "pediatric", "elbow"],
        conclusion_template="Supracondylar humerus fracture is classified as Gartland Type {type}.",
        reasoning_framework="""
The Gartland Classification divides pediatric supracondylar humerus fractures into three types based on displacement. Type I is nondisplaced; Type II is displaced with intact posterior cortex; Type III is completely displaced. Classification guides management: Type I treated with immobilization, Type II and III require reduction and pinning. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and risk of neurovascular injury.
""",
        key_factors=[
            "Fracture displacement",
            "Posterior cortex integrity",
            "Neurovascular status",
            "Patient age"
        ],
        primary_authority=[
            "Gartland JJ",
            "Pediatric Orthopaedic Society of North America"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Type II fractures may be managed nonoperatively",
            "Risk of neurovascular injury in Type III"
        ],
        resolution_strategy="Management based on fracture type and neurovascular status.",
        entity_scope="Pediatric supracondylar fractures",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gartland JJ. JBJS Am 1959;41-A: 899-906"
    ),
    DoctrineBlock(
        topic="Distal Radius Fracture: AO/OTA Classification",
        keywords=["distal radius fracture", "AO/OTA classification", "wrist fracture"],
        conclusion_template="Distal radius fracture is classified as AO/OTA Type {type}.",
        reasoning_framework="""
The AO/OTA Classification for distal radius fractures categorizes injuries based on fracture morphology, articular involvement, and displacement. Types A, B, and C represent extra-articular, partial articular, and complete articular fractures. Classification guides management: stable, extra-articular fractures may be managed conservatively; articular and displaced fractures require fixation. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and risk of posttraumatic arthritis.
""",
        key_factors=[
            "Fracture morphology",
            "Articular involvement",
            "Displacement",
            "Patient age"
        ],
        primary_authority=[
            "AO Foundation",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Risk of arthritis in articular fractures"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Distal radius fractures",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AO/OTA Fracture Compendium"
    ),
    DoctrineBlock(
        topic="Ankle Fracture: Lauge-Hansen Classification",
        keywords=["ankle fracture", "Lauge-Hansen classification", "mechanism", "injury"],
        conclusion_template="Ankle fracture is classified as Lauge-Hansen Type {type}.",
        reasoning_framework="""
The Lauge-Hansen Classification categorizes ankle fractures based on mechanism of injury: supination-adduction, supination-external rotation, pronation-abduction, and pronation-external rotation. Classification guides management and predicts associated ligament injuries. Accurate classification requires radiographic assessment and understanding of injury mechanism. The system is validated by correlation with outcomes and risk of instability. Decision-making incorporates patient age, comorbidities, and fracture morphology.
""",
        key_factors=[
            "Mechanism of injury",
            "Fracture morphology",
            "Ligament involvement",
            "Patient age"
        ],
        primary_authority=[
            "Lauge-Hansen N",
            "AO Foundation"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Reliance on radiographs alone",
        counter_arguments=[
            "Mechanism may be unclear",
            "Radiographs may not reveal ligament injury"
        ],
        resolution_strategy="Combined clinical and radiographic assessment.",
        entity_scope="Ankle fractures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Lauge-Hansen N. Acta Orthop Scand 1950;19(1-4):97-111"
    ),
    DoctrineBlock(
        topic="Shoulder Instability: Classification and Management",
        keywords=["shoulder instability", "classification", "management", "Bankart", "Hill-Sachs"],
        conclusion_template="Shoulder instability is classified as {instability_type} and managed accordingly.",
        reasoning_framework="""
Shoulder instability is classified as traumatic, atraumatic, or multidirectional. Traumatic instability often involves Bankart and Hill-Sachs lesions. Management depends on patient age, activity level, and lesion size. Arthroscopic repair is favored for isolated Bankart; open repair for large Hill-Sachs or bone loss. Decision-making incorporates MRI, CT, and clinical exam. The system is validated by correlation with recurrence rates and functional outcomes.
""",
        key_factors=[
            "Instability type",
            "Lesion size",
            "Patient age",
            "Activity level"
        ],
        primary_authority=[
            "American Shoulder and Elbow Surgeons",
            "AAOS"
        ],
        burden_holder="Shoulder surgeon",
        adversary_position="Universal arthroscopic repair",
        counter_arguments=[
            "Open repair may be superior for bone loss",
            "Arthroscopic repair risks recurrence"
        ],
        resolution_strategy="Technique selection based on lesion characteristics and patient factors.",
        entity_scope="Shoulder instability",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAOS Clinical Practice Guideline: Shoulder Instability"
    ),
    DoctrineBlock(
        topic="Osteoporosis: FRAX Risk Assessment",
        keywords=["osteoporosis", "FRAX", "risk assessment", "fracture risk"],
        conclusion_template="Fracture risk is assessed using FRAX and is {risk_level}.",
        reasoning_framework="""
The FRAX tool estimates 10-year probability of major osteoporotic fracture based on clinical risk factors and bone mineral density. Risk factors include age, sex, BMI, prior fracture, glucocorticoid use, smoking, and alcohol. FRAX guides decision-making for pharmacologic therapy. The tool is validated by large cohort studies and is recommended by international guidelines. Decision-making incorporates DXA results, clinical risk factors, and patient preference.
""",
        key_factors=[
            "Age",
            "Sex",
            "Bone mineral density",
            "Clinical risk factors"
        ],
        primary_authority=[
            "World Health Organization",
            "National Osteoporosis Foundation"
        ],
        burden_holder="Treating physician",
        adversary_position="Reliance on DXA alone",
        counter_arguments=[
            "FRAX may underestimate risk in high-risk populations",
            "DXA may be sufficient in select cases"
        ],
        resolution_strategy="Combined clinical and imaging assessment.",
        entity_scope="Osteoporosis management",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO FRAX Guidelines"
    ),
    DoctrineBlock(
        topic="Periprosthetic Joint Infection: Diagnosis and Management",
        keywords=["periprosthetic joint infection", "PJI", "diagnosis", "management", "arthroplasty"],
        conclusion_template="Periprosthetic joint infection is diagnosed and managed according to international consensus criteria.",
        reasoning_framework="""
Diagnosis of PJI relies on clinical, laboratory, and microbiological criteria. Major criteria include sinus tract or two positive cultures; minor criteria include elevated ESR/CRP, synovial WBC, and neutrophil percentage. Management includes debridement, antibiotics, and implant retention (DAIR) for early infections; staged revision for chronic infections. Decision-making incorporates timing, organism virulence, and patient factors. International consensus guidelines provide standardized diagnostic and management algorithms.
""",
        key_factors=[
            "Clinical signs",
            "Laboratory criteria",
            "Microbiological culture",
            "Timing of infection"
        ],
        primary_authority=[
            "International Consensus Meeting on PJI",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Reliance on clinical signs alone",
        counter_arguments=[
            "Laboratory tests may be falsely negative",
            "Clinical signs may be absent in chronic infection"
        ],
        resolution_strategy="Multimodal diagnostic approach; guideline-based management.",
        entity_scope="Periprosthetic joint infection",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ICM PJI Criteria"
    ),
    DoctrineBlock(
        topic="Osteosarcoma: Enneking Staging System",
        keywords=["osteosarcoma", "Enneking staging", "bone tumor", "malignancy"],
        conclusion_template="Osteosarcoma is staged as Enneking Stage {stage}.",
        reasoning_framework="""
The Enneking Staging System categorizes bone tumors based on grade, site, and metastasis. Stage IA and IB are low-grade; IIA and IIB are high-grade; III indicates metastasis. Staging guides surgical planning and adjuvant therapy. Accurate staging requires imaging, biopsy, and clinical assessment. The system is validated by correlation with prognosis and survival. Decision-making incorporates tumor grade, size, and patient factors.
""",
        key_factors=[
            "Tumor grade",
            "Site",
            "Metastasis",
            "Patient age"
        ],
        primary_authority=[
            "Enneking WF",
            "Musculoskeletal Tumor Society"
        ],
        burden_holder="Orthopedic oncologist",
        adversary_position="Alternative staging systems",
        counter_arguments=[
            "Complexity in borderline cases",
            "Potential for misclassification"
        ],
        resolution_strategy="Multidisciplinary review; standardized imaging protocols.",
        entity_scope="Bone tumor management",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Enneking WF. Clin Orthop Relat Res 1986;204:9-24"
    ),
    DoctrineBlock(
        topic="Osteomyelitis: Cierny-Mader Classification",
        keywords=["osteomyelitis", "Cierny-Mader classification", "infection", "bone"],
        conclusion_template="Osteomyelitis is classified as Cierny-Mader Type {type}.",
        reasoning_framework="""
The Cierny-Mader Classification divides osteomyelitis into anatomical and physiological types. Anatomical types (I-IV) describe bone involvement; physiological types (A, B, C) describe host status. Classification guides surgical and medical management. Accurate classification requires imaging, microbiology, and clinical assessment. The system is validated by correlation with outcomes and recurrence rates. Decision-making incorporates anatomical site, host factors, and infection chronicity.
""",
        key_factors=[
            "Anatomical involvement",
            "Host status",
            "Microbiological culture",
            "Imaging findings"
        ],
        primary_authority=[
            "Cierny G",
            "Mader JT"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Medical management may be sufficient in select cases",
            "Host status may change over time"
        ],
        resolution_strategy="Management based on classification and patient factors.",
        entity_scope="Osteomyelitis management",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Cierny G, Mader JT. Clin Orthop Relat Res 1985; 198:7-24"
    ),
    DoctrineBlock(
        topic="Patella Fracture: Classification and Management",
        keywords=["patella fracture", "classification", "management", "knee"],
        conclusion_template="Patella fracture is classified as {fracture_type} and managed accordingly.",
        reasoning_framework="""
Patella fractures are classified as transverse, vertical, comminuted, or osteochondral. Management depends on fracture type, displacement, and extensor mechanism integrity. Nondisplaced fractures are managed conservatively; displaced or disrupted extensor mechanism requires surgical fixation. Decision-making incorporates radiographic assessment, patient age, and activity level. The system is validated by correlation with outcomes and risk of nonunion.
""",
        key_factors=[
            "Fracture type",
            "Displacement",
            "Extensor mechanism integrity",
            "Patient age"
        ],
        primary_authority=[
            "AAOS",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in nondisplaced fractures",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Patella fractures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAOS Fracture Management Guidelines"
    ),
    DoctrineBlock(
        topic="Tibial Plateau Fracture: Schatzker Classification",
        keywords=["tibial plateau fracture", "Schatzker classification", "knee", "trauma"],
        conclusion_template="Tibial plateau fracture is classified as Schatzker Type {type}.",
        reasoning_framework="""
The Schatzker Classification divides tibial plateau fractures into six types based on fracture morphology and displacement. Types I-III are lateral; IV is medial; V and VI are bicondylar. Classification guides surgical planning and fixation strategy. Accurate classification requires CT and radiographic assessment. The system is validated by correlation with outcomes and risk of posttraumatic arthritis. Decision-making incorporates fracture type, displacement, and patient factors.
""",
        key_factors=[
            "Fracture morphology",
            "Displacement",
            "Articular involvement",
            "Patient age"
        ],
        primary_authority=[
            "Schatzker J",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Tibial plateau fractures",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Schatzker J et al. Clin Orthop Relat Res 1979;138:94-104"
    ),
    DoctrineBlock(
        topic="Pediatric Femoral Shaft Fracture: Management Principles",
        keywords=["pediatric femoral shaft fracture", "management", "orthopedics"],
        conclusion_template="Management of pediatric femoral shaft fracture is based on age and fracture characteristics.",
        reasoning_framework="""
Management of pediatric femoral shaft fractures depends on patient age, fracture type, and displacement. Infants and toddlers are managed with Pavlik harness or spica casting; older children may require flexible nailing or external fixation. Decision-making incorporates radiographic assessment, patient age, and comorbidities. The principles are validated by correlation with outcomes and risk of malunion. Surgical fixation is reserved for unstable or displaced fractures in older children.
""",
        key_factors=[
            "Patient age",
            "Fracture type",
            "Displacement",
            "Comorbidities"
        ],
        primary_authority=[
            "Pediatric Orthopaedic Society of North America",
            "AAOS"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in young children",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on age and fracture characteristics.",
        entity_scope="Pediatric femoral shaft fractures",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="POSNA Management Guidelines"
    ),
    DoctrineBlock(
        topic="Pelvic Fracture: Tile Classification",
        keywords=["pelvic fracture", "Tile classification", "trauma", "stability"],
        conclusion_template="Pelvic fracture is classified as Tile Type {type}.",
        reasoning_framework="""
The Tile Classification divides pelvic fractures into three types based on stability: Type A (stable), Type B (rotationally unstable), and Type C (rotationally and vertically unstable). Classification guides management: stable fractures are managed conservatively; unstable fractures require surgical fixation. Accurate classification requires CT and radiographic assessment. The system is validated by correlation with outcomes and risk of hemorrhage. Decision-making incorporates fracture type, hemodynamic status, and patient factors.
""",
        key_factors=[
            "Fracture stability",
            "Displacement",
            "Hemodynamic status",
            "Patient age"
        ],
        primary_authority=[
            "Tile M",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Surgical fixation risks hemorrhage"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Pelvic fractures",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tile M. Fractures of the Pelvis and Acetabulum"
    ),
    DoctrineBlock(
        topic="Acetabular Fracture: Letournel Classification",
        keywords=["acetabular fracture", "Letournel classification", "hip", "trauma"],
        conclusion_template="Acetabular fracture is classified as Letournel Type {type}.",
        reasoning_framework="""
The Letournel Classification divides acetabular fractures into elementary and associated types based on fracture morphology. Classification guides surgical approach and fixation strategy. Accurate classification requires CT and radiographic assessment. The system is validated by correlation with outcomes and risk of posttraumatic arthritis. Decision-making incorporates fracture type, displacement, and patient factors.
""",
        key_factors=[
            "Fracture morphology",
            "Displacement",
            "Articular involvement",
            "Patient age"
        ],
        primary_authority=[
            "Letournel E",
            "Orthopaedic Trauma Association"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Acetabular fractures",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Letournel E. Fractures of the Acetabulum"
    ),
    DoctrineBlock(
        topic="Clavicle Fracture: Allman Classification",
        keywords=["clavicle fracture", "Allman classification", "shoulder", "trauma"],
        conclusion_template="Clavicle fracture is classified as Allman Group {group}.",
        reasoning_framework="""
The Allman Classification divides clavicle fractures into three groups based on anatomical location: Group I (middle third), Group II (distal third), Group III (medial third). Classification guides management: middle third fractures are most common and may be managed conservatively; displaced or distal fractures may require surgical fixation. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and risk of nonunion.
""",
        key_factors=[
            "Anatomical location",
            "Displacement",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Allman FL",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in nondisplaced fractures",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture location and displacement.",
        entity_scope="Clavicle fractures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Allman FL. JBJS Am 1967;49-A: 774-84"
    ),
    DoctrineBlock(
        topic="Scaphoid Fracture: Herbert Classification",
        keywords=["scaphoid fracture", "Herbert classification", "wrist", "trauma"],
        conclusion_template="Scaphoid fracture is classified as Herbert Type {type}.",
        reasoning_framework="""
The Herbert Classification divides scaphoid fractures into stable and unstable types based on fracture morphology and displacement. Stable fractures are managed conservatively; unstable fractures require surgical fixation. Accurate classification requires radiographic and CT assessment. The system is validated by correlation with outcomes and risk of nonunion. Decision-making incorporates fracture type, displacement, and patient factors.
""",
        key_factors=[
            "Fracture morphology",
            "Displacement",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Herbert TJ",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Scaphoid fractures",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Herbert TJ. JBJS Br 1984;66-B: 114-23"
    ),
    DoctrineBlock(
        topic="Proximal Humerus Fracture: Neer Classification",
        keywords=["proximal humerus fracture", "Neer classification", "shoulder", "trauma"],
        conclusion_template="Proximal humerus fracture is classified as Neer Type {type}.",
        reasoning_framework="""
The Neer Classification divides proximal humerus fractures into four parts based on displacement and involvement of anatomical segments. Classification guides management: nondisplaced fractures are managed conservatively; displaced or multi-part fractures may require surgical fixation. Accurate classification requires radiographic and CT assessment. The system is validated by correlation with outcomes and risk of avascular necrosis.
""",
        key_factors=[
            "Fracture displacement",
            "Number of parts",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Neer CS",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in nondisplaced fractures",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Proximal humerus fractures",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Neer CS. JBJS Am 1970;52-A: 1077-89"
    ),
    DoctrineBlock(
        topic="Pediatric Forearm Fracture: Management Principles",
        keywords=["pediatric forearm fracture", "management", "orthopedics"],
        conclusion_template="Management of pediatric forearm fracture is based on age and fracture characteristics.",
        reasoning_framework="""
Management of pediatric forearm fractures depends on patient age, fracture type, and displacement. Nondisplaced fractures are managed with immobilization; displaced fractures may require closed reduction and casting or surgical fixation. Decision-making incorporates radiographic assessment, patient age, and comorbidities. The principles are validated by correlation with outcomes and risk of malunion. Surgical fixation is reserved for unstable or displaced fractures in older children.
""",
        key_factors=[
            "Patient age",
            "Fracture type",
            "Displacement",
            "Comorbidities"
        ],
        primary_authority=[
            "Pediatric Orthopaedic Society of North America",
            "AAOS"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in young children",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on age and fracture characteristics.",
        entity_scope="Pediatric forearm fractures",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="POSNA Management Guidelines"
    ),
    DoctrineBlock(
        topic="Carpal Tunnel Syndrome: Diagnosis and Management",
        keywords=["carpal tunnel syndrome", "diagnosis", "management", "nerve compression"],
        conclusion_template="Carpal tunnel syndrome is diagnosed and managed according to clinical and electrodiagnostic criteria.",
        reasoning_framework="""
Diagnosis of carpal tunnel syndrome is based on clinical signs (numbness, tingling, nocturnal symptoms), physical exam (Phalen, Tinel), and electrodiagnostic studies. Management includes splinting, steroid injection, and surgical release. Decision-making incorporates symptom severity, duration, and patient factors. The principles are validated by correlation with outcomes and recurrence rates. Surgical release is indicated for refractory or severe cases.
""",
        key_factors=[
            "Clinical signs",
            "Electrodiagnostic studies",
            "Symptom severity",
            "Patient age"
        ],
        primary_authority=[
            "American Society for Surgery of the Hand",
            "AAOS"
        ],
        burden_holder="Treating physician",
        adversary_position="Reliance on clinical signs alone",
        counter_arguments=[
            "Electrodiagnostic studies may be falsely negative",
            "Clinical signs may be sufficient in select cases"
        ],
        resolution_strategy="Combined clinical and electrodiagnostic assessment.",
        entity_scope="Carpal tunnel syndrome",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASSH Management Guidelines"
    ),
    DoctrineBlock(
        topic="Spinal Cord Injury: ASIA Impairment Scale",
        keywords=["spinal cord injury", "ASIA impairment scale", "neurology"],
        conclusion_template="Spinal cord injury is classified as ASIA Grade {grade}.",
        reasoning_framework="""
The ASIA Impairment Scale grades spinal cord injury from A (complete) to E (normal). Classification guides prognosis and management. Accurate grading requires neurological exam of motor and sensory function. The system is validated by correlation with outcomes and recovery rates. Decision-making incorporates exam findings, imaging, and patient factors.
""",
        key_factors=[
            "Motor function",
            "Sensory function",
            "Imaging findings",
            "Patient age"
        ],
        primary_authority=[
            "American Spinal Injury Association",
            "AAOS"
        ],
        burden_holder="Treating physician",
        adversary_position="Alternative grading systems",
        counter_arguments=[
            "Complexity in borderline cases",
            "Potential for misclassification"
        ],
        resolution_strategy="Standardized exam protocols; multidisciplinary review.",
        entity_scope="Spinal cord injury",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASIA Impairment Scale Guidelines"
    ),
    DoctrineBlock(
        topic="Radial Head Fracture: Mason Classification",
        keywords=["radial head fracture", "Mason classification", "elbow", "trauma"],
        conclusion_template="Radial head fracture is classified as Mason Type {type}.",
        reasoning_framework="""
The Mason Classification divides radial head fractures into three types: Type I (nondisplaced), Type II (displaced), Type III (comminuted). Classification guides management: Type I treated with immobilization; Type II and III may require surgical fixation or excision. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and risk of stiffness.
""",
        key_factors=[
            "Fracture displacement",
            "Comminution",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Mason ML",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in nondisplaced fractures",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Radial head fractures",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mason ML. JBJS Br 1954;36-B: 98-102"
    ),
    DoctrineBlock(
        topic="Calcaneal Fracture: Sanders Classification",
        keywords=["calcaneal fracture", "Sanders classification", "foot", "trauma"],
        conclusion_template="Calcaneal fracture is classified as Sanders Type {type}.",
        reasoning_framework="""
The Sanders Classification divides calcaneal fractures based on CT assessment of articular involvement. Types I-IV represent increasing severity and comminution. Classification guides surgical planning and fixation strategy. Accurate classification requires CT imaging. The system is validated by correlation with outcomes and risk of posttraumatic arthritis. Decision-making incorporates fracture type, displacement, and patient factors.
""",
        key_factors=[
            "Articular involvement",
            "Comminution",
            "Displacement",
            "Patient age"
        ],
        primary_authority=[
            "Sanders R",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Stable fractures may be managed nonoperatively",
            "Surgical fixation risks infection"
        ],
        resolution_strategy="Management based on fracture type and patient factors.",
        entity_scope="Calcaneal fractures",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Sanders R. Foot Ankle Int 1993;14(3):183-92"
    ),
    DoctrineBlock(
        topic="Hallux Valgus: Severity Classification",
        keywords=["hallux valgus", "severity classification", "foot", "deformity"],
        conclusion_template="Hallux valgus is classified as {severity} based on radiographic angles.",
        reasoning_framework="""
Severity of hallux valgus is classified as mild, moderate, or severe based on hallux valgus angle and intermetatarsal angle. Classification guides surgical planning and choice of procedure. Accurate classification requires radiographic measurement. The system is validated by correlation with outcomes and recurrence rates. Decision-making incorporates angle measurement, patient symptoms, and activity level.
""",
        key_factors=[
            "Hallux valgus angle",
            "Intermetatarsal angle",
            "Patient symptoms",
            "Activity level"
        ],
        primary_authority=[
            "American Orthopaedic Foot & Ankle Society",
            "AAOS"
        ],
        burden_holder="Foot and ankle surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in mild cases",
            "Surgical fixation risks recurrence"
        ],
        resolution_strategy="Management based on severity and patient factors.",
        entity_scope="Hallux valgus",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AOFAS Hallux Valgus Guidelines"
    ),
    DoctrineBlock(
        topic="Achilles Tendon Rupture: Management Principles",
        keywords=["Achilles tendon rupture", "management", "foot", "trauma"],
        conclusion_template="Achilles tendon rupture is managed by {treatment_strategy}.",
        reasoning_framework="""
Management of Achilles tendon rupture includes conservative (functional bracing) and surgical repair. Decision-making incorporates patient age, activity level, and comorbidities. Randomized studies show similar outcomes, but surgical repair reduces risk of re-rupture in active patients. Conservative management is favored in older or low-demand patients. The principles are validated by correlation with outcomes and complication rates.
""",
        key_factors=[
            "Patient age",
            "Activity level",
            "Comorbidities",
            "Rupture severity"
        ],
        primary_authority=[
            "American Orthopaedic Foot & Ankle Society",
            "AAOS"
        ],
        burden_holder="Foot and ankle surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in select cases",
            "Surgical repair risks infection"
        ],
        resolution_strategy="Management based on patient factors and rupture severity.",
        entity_scope="Achilles tendon rupture",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AOFAS Achilles Tendon Guidelines"
    ),
    DoctrineBlock(
        topic="Hip Dysplasia: Tönnis Classification",
        keywords=["hip dysplasia", "Tönnis classification", "pediatric", "hip"],
        conclusion_template="Hip dysplasia is classified as Tönnis Grade {grade}.",
        reasoning_framework="""
The Tönnis Classification grades hip dysplasia based on radiographic findings: Grade I (mild), Grade II (moderate), Grade III (severe). Classification guides management: mild cases may be managed conservatively; moderate and severe cases may require surgical intervention. Accurate classification requires radiographic assessment. The system is validated by correlation with outcomes and risk of osteoarthritis.
""",
        key_factors=[
            "Radiographic findings",
            "Patient age",
            "Severity",
            "Comorbidities"
        ],
        primary_authority=[
            "Tönnis D",
            "Pediatric Orthopaedic Society of North America"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in mild cases",
            "Surgical intervention risks complications"
        ],
        resolution_strategy="Management based on grade and patient factors.",
        entity_scope="Hip dysplasia",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tönnis D. Congenital Dysplasia and Dislocation of the Hip"
    ),
    DoctrineBlock(
        topic="Developmental Dysplasia of the Hip: Graf Classification",
        keywords=["developmental dysplasia of the hip", "Graf classification", "ultrasound", "pediatric"],
        conclusion_template="Developmental dysplasia of the hip is classified as Graf Type {type}.",
        reasoning_framework="""
The Graf Classification uses ultrasound to categorize developmental dysplasia of the hip into Types I-IV based on morphology and stability. Classification guides management: Type I is normal; Type II may require observation; Types III and IV require intervention. Accurate classification requires standardized ultrasound technique. The system is validated by correlation with outcomes and risk of dislocation.
""",
        key_factors=[
            "Ultrasound findings",
            "Morphology",
            "Stability",
            "Patient age"
        ],
        primary_authority=[
            "Graf R",
            "Pediatric Orthopaedic Society of North America"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Reliance on clinical exam alone",
        counter_arguments=[
            "Ultrasound may be operator-dependent",
            "Clinical exam may be sufficient in select cases"
        ],
        resolution_strategy="Combined clinical and ultrasound assessment.",
        entity_scope="Developmental dysplasia of the hip",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Graf R. Hip Sonography"
    ),
    DoctrineBlock(
        topic="Slipped Capital Femoral Epiphysis: Classification and Management",
        keywords=["slipped capital femoral epiphysis", "SCFE", "classification", "management"],
        conclusion_template="SCFE is classified as {severity} and managed accordingly.",
        reasoning_framework="""
SCFE is classified as stable or unstable based on ability to ambulate, and as mild, moderate, or severe based on degree of slip. Management includes in situ pinning for stable slips; unstable slips require urgent intervention. Accurate classification requires radiographic assessment and clinical exam. The system is validated by correlation with outcomes and risk of avascular necrosis.
""",
        key_factors=[
            "Ability to ambulate",
            "Degree of slip",
            "Patient age",
            "Comorbidities"
        ],
        primary_authority=[
            "Pediatric Orthopaedic Society of North America",
            "AAOS"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in mild cases",
            "Urgent intervention risks complications"
        ],
        resolution_strategy="Management based on classification and patient factors.",
        entity_scope="SCFE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="POSNA SCFE Guidelines"
    ),
    DoctrineBlock(
        topic="Osteogenesis Imperfecta: Sillence Classification",
        keywords=["osteogenesis imperfecta", "Sillence classification", "bone disease"],
        conclusion_template="Osteogenesis imperfecta is classified as Sillence Type {type}.",
        reasoning_framework="""
The Sillence Classification divides osteogenesis imperfecta into four types based on clinical and genetic features. Type I is mild; Type II is perinatal lethal; Type III is severe; Type IV is moderate. Classification guides management and prognosis. Accurate classification requires clinical exam, genetic testing, and radiographic assessment. The system is validated by correlation with outcomes and fracture risk.
""",
        key_factors=[
            "Clinical features",
            "Genetic testing",
            "Radiographic findings",
            "Patient age"
        ],
        primary_authority=[
            "Sillence DO",
            "Pediatric Orthopaedic Society of North America"
        ],
        burden_holder="Pediatric orthopedic surgeon",
        adversary_position="Alternative classification systems",
        counter_arguments=[
            "Genetic testing may be unavailable",
            "Clinical features may overlap"
        ],
        resolution_strategy="Combined clinical and genetic assessment.",
        entity_scope="Osteogenesis imperfecta",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Sillence DO. JBJS Br 1979;61-B: 331-43"
    ),
    DoctrineBlock(
        topic="Musculoskeletal Tumor: AJCC Staging",
        keywords=["musculoskeletal tumor", "AJCC staging", "bone", "soft tissue"],
        conclusion_template="Musculoskeletal tumor is staged as AJCC Stage {stage}.",
        reasoning_framework="""
The AJCC Staging System categorizes musculoskeletal tumors based on size, grade, lymph node involvement, and metastasis. Staging guides surgical planning, adjuvant therapy, and prognosis. Accurate staging requires imaging, biopsy, and clinical assessment. The system is validated by correlation with outcomes and survival rates. Decision-making incorporates tumor size, grade, and patient factors.
""",
        key_factors=[
            "Tumor size",
            "Grade",
            "Lymph node involvement",
            "Metastasis"
        ],
        primary_authority=[
            "American Joint Committee on Cancer",
            "Musculoskeletal Tumor Society"
        ],
        burden_holder="Orthopedic oncologist",
        adversary_position="Alternative staging systems",
        counter_arguments=[
            "Complexity in borderline cases",
            "Potential for misclassification"
        ],
        resolution_strategy="Multidisciplinary review; standardized imaging protocols.",
        entity_scope="Musculoskeletal tumor management",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AJCC Cancer Staging Manual"
    ),
    DoctrineBlock(
        topic="Osteonecrosis of the Femoral Head: Ficat-Arlet Classification",
        keywords=["osteonecrosis", "femoral head", "Ficat-Arlet classification", "hip"],
        conclusion_template="Osteonecrosis of the femoral head is classified as Ficat-Arlet Stage {stage}.",
        reasoning_framework="""
The Ficat-Arlet Classification divides osteonecrosis of the femoral head into four stages based on radiographic and MRI findings. Stage I is pre-radiographic; Stage II shows sclerosis; Stage III has subchondral collapse; Stage IV has joint space narrowing. Classification guides management: early stages may be managed conservatively; advanced stages require surgical intervention. Accurate classification requires radiographic and MRI assessment. The system is validated by correlation with outcomes and risk of collapse.
""",
        key_factors=[
            "Radiographic findings",
            "MRI findings",
            "Patient age",
            "Severity"
        ],
        primary_authority=[
            "Ficat P",
            "Arlet J"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Universal surgical management",
        counter_arguments=[
            "Conservative management may be sufficient in early stages",
            "Surgical intervention risks complications"
        ],
        resolution_strategy="Management based on stage and patient factors.",
        entity_scope="Osteonecrosis of the femoral head",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ficat P, Arlet J. Osteonecrosis Guidelines"
    ),
    DoctrineBlock(
        topic="Spinal Deformity: Scoliosis Cobb Angle Measurement",
        keywords=["scoliosis", "Cobb angle", "spinal deformity", "measurement"],
        conclusion_template="Scoliosis is measured as Cobb angle {angle} degrees.",
        reasoning_framework="""
The Cobb Angle is the standard measurement for quantifying spinal deformity in scoliosis. Angle is measured on radiographs between the most tilted vertebrae above and below the curve. Measurement guides management: observation for mild curves, bracing for moderate, surgery for severe. Accurate measurement requires standardized radiographic technique. The system is validated by correlation with outcomes and progression risk.
""",
        key_factors=[
            "Radiographic technique",
            "Vertebral selection",
            "Patient age",
            "Curve progression"
        ],
        primary_authority=[
            "Scoliosis Research Society",
            "AAOS"
        ],
        burden_holder="Treating physician",
        adversary_position="Alternative measurement techniques",
        counter_arguments=[
            "Interobserver variability",
            "Potential for mismeasurement"
        ],
        resolution_strategy="Standardized protocols; multidisciplinary review.",
        entity_scope="Spinal deformity",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SRS Cobb Angle Guidelines"
    ),
    DoctrineBlock(
        topic="Musculoskeletal Infection: MSIS Criteria",
        keywords=["musculoskeletal infection", "MSIS criteria", "diagnosis", "management"],
        conclusion_template="Musculoskeletal infection is diagnosed according to MSIS criteria.",
        reasoning_framework="""
The Musculoskeletal Infection Society (MSIS) criteria provide standardized diagnostic algorithms for musculoskeletal infection, including periprosthetic joint infection. Major criteria include sinus tract or two positive cultures; minor criteria include elevated ESR/CRP, synovial WBC, and neutrophil percentage. Management includes antibiotics, surgical debridement, and implant revision. Decision-making incorporates timing, organism virulence, and patient factors. The criteria are validated by correlation with outcomes and recurrence rates.
""",
        key_factors=[
            "Clinical signs",
            "Laboratory criteria",
            "Microbiological culture",
            "Timing of infection"
        ],
        primary_authority=[
            "Musculoskeletal Infection Society",
            "AAOS"
        ],
        burden_holder="Treating orthopedic surgeon",
        adversary_position="Reliance on clinical signs alone",
        counter_arguments=[
            "Laboratory tests may be falsely negative",
            "Clinical signs may be absent in chronic infection"
        ],
        resolution_strategy="Multimodal diagnostic approach; guideline-based management.",
        entity_scope="Musculoskeletal infection",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="MSIS Diagnostic Criteria"
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