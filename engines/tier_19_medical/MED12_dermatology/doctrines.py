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
        topic="Melanoma ABCDE Criteria Application",
        keywords=["melanoma", "ABCDE", "diagnosis", "skin cancer", "dermatology"],
        conclusion_template="A pigmented lesion meeting two or more ABCDE criteria should be biopsied to rule out melanoma.",
        reasoning_framework="""
The ABCDE criteria (Asymmetry, Border irregularity, Color variation, Diameter >6mm, Evolving) are internationally recognized for early melanoma detection. Lesions are evaluated for each criterion. If two or more are present, the pre-test probability of melanoma increases significantly. Early biopsy is warranted to reduce morbidity and mortality. Exceptions may include classic benign lesions (e.g., seborrheic keratoses) with clear clinical context. The framework prioritizes sensitivity over specificity, acknowledging the high stakes of missed melanoma.
""",
        key_factors=[
            "Presence of asymmetry",
            "Border irregularity",
            "Color variation",
            "Diameter greater than 6mm",
            "Evolution or change in lesion"
        ],
        primary_authority=[
            "American Academy of Dermatology (AAD)",
            "National Comprehensive Cancer Network (NCCN)"
        ],
        burden_holder="Clinician",
        adversary_position="Over-biopsy leads to unnecessary procedures and patient anxiety.",
        counter_arguments=[
            "Missed melanoma has higher morbidity than unnecessary biopsy.",
            "Clinical context and dermoscopy can reduce false positives."
        ],
        resolution_strategy="Prioritize patient safety; biopsy when in doubt.",
        entity_scope="All patients with suspicious pigmented lesions",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2022"
    ),
    DoctrineBlock(
        topic="Basal Cell Carcinoma Diagnosis Standard",
        keywords=["basal cell carcinoma", "BCC", "diagnosis", "skin cancer"],
        conclusion_template="Diagnosis of BCC should be confirmed histopathologically prior to definitive treatment.",
        reasoning_framework="""
Clinical suspicion for BCC arises from characteristic features: pearly papule, telangiectasia, rolled borders, and ulceration. Dermoscopy enhances diagnostic accuracy but is not definitive. Histopathological confirmation via shave, punch, or excisional biopsy is the gold standard. Exceptions include classic superficial BCCs in low-risk areas where non-invasive modalities may be considered. The framework balances diagnostic certainty with procedural risk.
""",
        key_factors=[
            "Clinical morphology",
            "Dermoscopy findings",
            "Biopsy technique",
            "Histopathological confirmation"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Non-invasive diagnosis can suffice in clear cases.",
        counter_arguments=[
            "Histology is necessary for subtype identification and margin assessment.",
            "Misdiagnosis can lead to inappropriate therapy."
        ],
        resolution_strategy="Biopsy all suspected BCCs unless contraindicated.",
        entity_scope="Patients with suspected BCC",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAD BCC Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Squamous Cell Carcinoma Risk Stratification",
        keywords=["squamous cell carcinoma", "SCC", "risk", "stratification", "skin cancer"],
        conclusion_template="SCCs should be stratified into low- and high-risk categories based on clinical and histologic features to guide management.",
        reasoning_framework="""
Risk stratification considers tumor size, location, differentiation, perineural invasion, depth, and patient immunosuppression. High-risk SCCs (e.g., >2cm on trunk, >1cm on face, poorly differentiated, perineural invasion) have higher recurrence and metastasis rates. Management escalates accordingly, often requiring Mohs surgery or adjuvant therapy. Low-risk lesions may be managed with standard excision. The framework ensures resource allocation and improved outcomes.
""",
        key_factors=[
            "Tumor size",
            "Anatomic location",
            "Histologic differentiation",
            "Perineural invasion",
            "Depth of invasion",
            "Immunosuppression status"
        ],
        primary_authority=[
            "National Comprehensive Cancer Network",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Over-stratification may delay treatment.",
        counter_arguments=[
            "Risk stratification optimizes outcomes and reduces recurrence.",
            "Guidelines are evidence-based and improve consistency."
        ],
        resolution_strategy="Apply evidence-based criteria for risk assignment.",
        entity_scope="All diagnosed SCC cases",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NCCN Guidelines 2023"
    ),
    DoctrineBlock(
        topic="Atopic Dermatitis Stepwise Management",
        keywords=["atopic dermatitis", "eczema", "management", "stepwise", "treatment"],
        conclusion_template="Atopic dermatitis should be managed with a stepwise approach, escalating therapy based on disease severity and response.",
        reasoning_framework="""
Initial management includes skin hydration, avoidance of triggers, and topical corticosteroids or calcineurin inhibitors. Moderate-to-severe cases may require phototherapy or systemic agents (e.g., dupilumab, cyclosporine). Regular assessment of disease control and side effects is essential. The framework emphasizes patient education, adherence, and shared decision-making. Step-down therapy is considered upon remission.
""",
        key_factors=[
            "Disease severity",
            "Response to topical therapy",
            "Patient age",
            "Comorbidities",
            "Adherence to therapy"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "European Academy of Dermatology and Venereology"
        ],
        burden_holder="Clinician",
        adversary_position="Early systemic therapy may reduce disease burden.",
        counter_arguments=[
            "Systemic agents have significant side effects.",
            "Stepwise approach minimizes overtreatment."
        ],
        resolution_strategy="Escalate therapy only after failure of prior steps.",
        entity_scope="All patients with atopic dermatitis",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AAD Atopic Dermatitis Guidelines 2014"
    ),
    DoctrineBlock(
        topic="Psoriasis Biologic Selection Algorithm",
        keywords=["psoriasis", "biologics", "treatment", "selection", "algorithm"],
        conclusion_template="Biologic therapy selection for psoriasis should be individualized based on comorbidities, efficacy, safety, and patient preference.",
        reasoning_framework="""
Selection of biologic agents (e.g., TNF-alpha inhibitors, IL-17, IL-23 inhibitors) depends on disease severity, prior treatment response, comorbidities (e.g., IBD, MS), and risk profile. Shared decision-making is critical. Baseline screening for TB, hepatitis, and malignancy risk is required. The framework supports switching agents upon inadequate response or adverse events. Cost and access may influence choice.
""",
        key_factors=[
            "Disease severity",
            "Comorbidities",
            "Prior treatment history",
            "Safety profile",
            "Patient preference",
            "Insurance coverage"
        ],
        primary_authority=[
            "National Psoriasis Foundation",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Cost and insurance restrictions may limit optimal choice.",
        counter_arguments=[
            "Step therapy can delay disease control.",
            "Patient advocacy can improve access."
        ],
        resolution_strategy="Document rationale and pursue appeals as needed.",
        entity_scope="Moderate-to-severe psoriasis patients",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD-NPF Guidelines 2020"
    ),
    DoctrineBlock(
        topic="Wound Healing Phases Recognition",
        keywords=["wound healing", "phases", "inflammation", "proliferation", "remodeling"],
        conclusion_template="Wound healing proceeds through inflammation, proliferation, and remodeling phases, each with distinct clinical and histological features.",
        reasoning_framework="""
The inflammatory phase (days 1–4) involves hemostasis and immune cell infiltration. The proliferative phase (days 4–21) features granulation tissue formation, angiogenesis, and re-epithelialization. Remodeling (up to 1 year) strengthens the wound via collagen maturation. Recognition of phase guides intervention (e.g., debridement, infection control, offloading). Chronic wounds may stall in the inflammatory phase, requiring advanced therapies.
""",
        key_factors=[
            "Duration since injury",
            "Clinical appearance",
            "Histological findings",
            "Presence of infection or necrosis"
        ],
        primary_authority=[
            "Wound Healing Society",
            "European Wound Management Association"
        ],
        burden_holder="Clinician",
        adversary_position="Phases may overlap and are not always distinct.",
        counter_arguments=[
            "Phase recognition aids in targeted therapy.",
            "Adjunctive diagnostics can clarify phase."
        ],
        resolution_strategy="Combine clinical and laboratory assessment.",
        entity_scope="All wound care patients",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="WHS Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Phototherapy Protocols in Dermatology",
        keywords=["phototherapy", "protocols", "psoriasis", "eczema", "UVB", "PUVA"],
        conclusion_template="Phototherapy should follow standardized protocols, adjusting dose based on skin type, disease, and response.",
        reasoning_framework="""
Narrowband UVB is first-line for psoriasis and atopic dermatitis; PUVA is reserved for refractory cases. Protocols specify starting dose by Fitzpatrick skin type, increment schedule, and monitoring for erythema. Eye and genital protection are mandatory. Cumulative dose and skin cancer risk are tracked. Dose adjustments are made for missed sessions or adverse reactions. The framework ensures efficacy and safety.
""",
        key_factors=[
            "Skin type",
            "Disease indication",
            "Prior response",
            "Adverse effects",
            "Cumulative UV exposure"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Photodermatology Group"
        ],
        burden_holder="Clinician",
        adversary_position="Rigid protocols may not suit all patients.",
        counter_arguments=[
            "Protocols are evidence-based for safety.",
            "Individualization is permitted within protocol limits."
        ],
        resolution_strategy="Document deviations with clinical justification.",
        entity_scope="Patients receiving phototherapy",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAD Phototherapy Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Dermatopathology Interpretation Standards",
        keywords=["dermatopathology", "biopsy", "histology", "diagnosis", "skin"],
        conclusion_template="Dermatopathology reports should integrate clinical and histological findings for accurate diagnosis.",
        reasoning_framework="""
Optimal interpretation requires correlation of clinical data (age, lesion site, morphology) with histopathology. Communication between clinician and pathologist is essential. Discordant findings warrant re-examination or additional stains. The framework reduces diagnostic error and improves patient outcomes. Standardized reporting enhances clarity and reproducibility.
""",
        key_factors=[
            "Clinical-pathological correlation",
            "Quality of biopsy specimen",
            "Use of ancillary stains",
            "Communication between teams"
        ],
        primary_authority=[
            "College of American Pathologists",
            "American Society of Dermatopathology"
        ],
        burden_holder="Pathologist",
        adversary_position="Limited clinical information may hinder diagnosis.",
        counter_arguments=[
            "Clinicians must provide adequate data.",
            "Repeat biopsy is justified if necessary."
        ],
        resolution_strategy="Foster multidisciplinary communication.",
        entity_scope="All dermatopathology cases",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CAP Dermatopathology Protocols 2021"
    ),
    DoctrineBlock(
        topic="Cosmetic Botulinum Toxin Use Guidelines",
        keywords=["cosmetic", "botulinum toxin", "botox", "guidelines", "aesthetics"],
        conclusion_template="Cosmetic botulinum toxin use should follow dosing, injection site, and safety protocols to minimize complications.",
        reasoning_framework="""
Indications include dynamic facial rhytides (glabellar, crow's feet, forehead lines). Dosing is individualized by muscle mass and prior response. Injection technique must avoid vascular and nerve injury. Contraindications include neuromuscular disorders and pregnancy. Adverse events (ptosis, asymmetry) are minimized by anatomical knowledge and conservative dosing. Informed consent is mandatory.
""",
        key_factors=[
            "Indication for use",
            "Patient anatomy",
            "Dosing protocol",
            "Contraindications",
            "Informed consent"
        ],
        primary_authority=[
            "American Society for Dermatologic Surgery",
            "International Society of Aesthetic Plastic Surgery"
        ],
        burden_holder="Clinician",
        adversary_position="Off-label use increases risk.",
        counter_arguments=[
            "Off-label use is common but must be justified.",
            "Patient safety is paramount."
        ],
        resolution_strategy="Strict adherence to guidelines and documentation.",
        entity_scope="Cosmetic dermatology patients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASDS Botulinum Toxin Guidelines 2020"
    ),
    DoctrineBlock(
        topic="Acne Treatment Ladder",
        keywords=["acne", "treatment", "ladder", "algorithm", "management"],
        conclusion_template="Acne management should follow a stepwise ladder, escalating from topical to systemic therapy based on severity.",
        reasoning_framework="""
Mild acne: topical retinoids, benzoyl peroxide, or antibiotics. Moderate: add oral antibiotics. Severe or nodulocystic: consider isotretinoin. Hormonal therapy for females with androgenic features. Treatment is tailored to patient preference, side effect profile, and adherence. Maintenance therapy prevents relapse. The ladder reduces antibiotic resistance and optimizes outcomes.
""",
        key_factors=[
            "Acne severity",
            "Prior treatment response",
            "Patient age and sex",
            "Side effect profile",
            "Adherence"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "Global Alliance to Improve Outcomes in Acne"
        ],
        burden_holder="Clinician",
        adversary_position="Early isotretinoin may provide faster control.",
        counter_arguments=[
            "Isotretinoin has significant risks and monitoring requirements.",
            "Stepwise approach is evidence-based."
        ],
        resolution_strategy="Escalate therapy per guidelines; document rationale for deviation.",
        entity_scope="All patients with acne",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAD Acne Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Melanoma Sentinel Lymph Node Biopsy Indication",
        keywords=["melanoma", "sentinel lymph node", "biopsy", "indication"],
        conclusion_template="Sentinel lymph node biopsy is indicated for melanoma with Breslow depth ≥0.8mm or <0.8mm with ulceration.",
        reasoning_framework="""
Sentinel lymph node biopsy (SLNB) provides prognostic information and guides management. Indications are based on Breslow depth and ulceration status. SLNB is not recommended for in situ or thin melanomas (<0.8mm without ulceration). The procedure carries risks (lymphedema, seroma) and should be discussed with patients. The framework aligns with NCCN and AJCC guidelines.
""",
        key_factors=[
            "Breslow depth",
            "Ulceration",
            "Patient comorbidities",
            "Patient preference"
        ],
        primary_authority=[
            "National Comprehensive Cancer Network",
            "American Joint Committee on Cancer"
        ],
        burden_holder="Clinician",
        adversary_position="SLNB may not improve survival.",
        counter_arguments=[
            "SLNB provides staging and prognostic value.",
            "Guidelines support selective use."
        ],
        resolution_strategy="Discuss risks and benefits with patient.",
        entity_scope="Patients with invasive melanoma",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NCCN Melanoma Guidelines 2023"
    ),
    DoctrineBlock(
        topic="Mohs Surgery Indications for Non-Melanoma Skin Cancer",
        keywords=["mohs surgery", "indications", "non-melanoma", "skin cancer", "BCC", "SCC"],
        conclusion_template="Mohs micrographic surgery is indicated for high-risk BCC and SCC in cosmetically or functionally sensitive areas.",
        reasoning_framework="""
Mohs surgery offers tissue-sparing excision with maximal margin control. Indications include recurrent tumors, aggressive histology, ill-defined borders, and tumors on the face, ears, genitalia, hands, or feet. The framework prioritizes functional and cosmetic outcomes while minimizing recurrence. Not indicated for low-risk, superficial lesions in non-critical sites.
""",
        key_factors=[
            "Tumor location",
            "Histologic subtype",
            "Recurrence status",
            "Tumor size",
            "Patient comorbidities"
        ],
        primary_authority=[
            "American College of Mohs Surgery",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Mohs is resource-intensive and may be overused.",
        counter_arguments=[
            "Mohs reduces recurrence and preserves tissue.",
            "Guidelines restrict use to high-risk cases."
        ],
        resolution_strategy="Apply strict criteria for Mohs indication.",
        entity_scope="Patients with high-risk NMSC",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ACMS Mohs Indications 2019"
    ),
    DoctrineBlock(
        topic="Patch Testing for Allergic Contact Dermatitis",
        keywords=["patch test", "allergic contact dermatitis", "diagnosis", "eczema"],
        conclusion_template="Patch testing is the gold standard for diagnosing allergic contact dermatitis.",
        reasoning_framework="""
Patch testing identifies specific allergens responsible for dermatitis. Standardized panels are applied to the back for 48 hours, with readings at 48 and 72–96 hours. Interpretation requires expertise to differentiate irritant from allergic reactions. The framework supports targeted avoidance and improved outcomes. False positives/negatives are possible; clinical correlation is essential.
""",
        key_factors=[
            "History of dermatitis",
            "Exposure history",
            "Test interpretation",
            "Patient adherence to avoidance"
        ],
        primary_authority=[
            "American Contact Dermatitis Society",
            "European Society of Contact Dermatitis"
        ],
        burden_holder="Clinician",
        adversary_position="Patch testing is time-consuming and may not identify all allergens.",
        counter_arguments=[
            "Patch testing guides effective management.",
            "Expanded panels can be used for complex cases."
        ],
        resolution_strategy="Use patch testing in persistent or unexplained dermatitis.",
        entity_scope="Patients with suspected allergic contact dermatitis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACDS Patch Testing Guidelines 2015"
    ),
    DoctrineBlock(
        topic="Systemic Corticosteroids in Psoriasis",
        keywords=["systemic corticosteroids", "psoriasis", "contraindication", "treatment"],
        conclusion_template="Systemic corticosteroids should generally be avoided in psoriasis due to risk of flare and pustular transformation.",
        reasoning_framework="""
Systemic corticosteroids can trigger severe rebound flares, including pustular and erythrodermic psoriasis, upon withdrawal. Alternative systemic agents (methotrexate, cyclosporine, biologics) are preferred. Exceptions may include life-threatening situations (e.g., acute generalized pustular psoriasis). The framework prioritizes long-term disease control and patient safety.
""",
        key_factors=[
            "Disease severity",
            "Prior therapy",
            "Risk of flare",
            "Comorbidities"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "National Psoriasis Foundation"
        ],
        burden_holder="Clinician",
        adversary_position="Short-term corticosteroids may provide rapid relief.",
        counter_arguments=[
            "Risks outweigh benefits in most cases.",
            "Safer alternatives are available."
        ],
        resolution_strategy="Reserve corticosteroids for exceptional cases.",
        entity_scope="Psoriasis patients",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD-NPF Guidelines 2020"
    ),
    DoctrineBlock(
        topic="Topical Calcineurin Inhibitors in Pediatric Atopic Dermatitis",
        keywords=["topical calcineurin inhibitors", "pediatric", "atopic dermatitis", "tacrolimus", "pimecrolimus"],
        conclusion_template="Topical calcineurin inhibitors are safe and effective for pediatric atopic dermatitis refractory to corticosteroids.",
        reasoning_framework="""
Tacrolimus and pimecrolimus are approved for children ≥2 years with atopic dermatitis unresponsive to topical steroids. They are steroid-sparing and avoid skin atrophy. Black box warning for malignancy is based on animal data; human risk is unproven. The framework supports judicious use with informed consent and regular monitoring.
""",
        key_factors=[
            "Age of patient",
            "Disease severity",
            "Response to steroids",
            "Adverse effects"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "FDA"
        ],
        burden_holder="Clinician",
        adversary_position="Long-term safety is uncertain.",
        counter_arguments=[
            "Evidence supports safety in clinical use.",
            "Monitor for adverse events."
        ],
        resolution_strategy="Educate families and monitor regularly.",
        entity_scope="Pediatric atopic dermatitis patients",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD Atopic Dermatitis Guidelines 2014"
    ),
    DoctrineBlock(
        topic="Nail Psoriasis Diagnosis and Management",
        keywords=["nail psoriasis", "diagnosis", "management", "treatment"],
        conclusion_template="Nail psoriasis diagnosis is clinical, supported by dermoscopy and biopsy when uncertain; management is stepwise.",
        reasoning_framework="""
Nail pitting, onycholysis, oil spots, and subungual hyperkeratosis are classic findings. Dermoscopy enhances diagnostic accuracy. Biopsy is reserved for atypical cases or to exclude onychomycosis. Topical steroids, vitamin D analogs, and intralesional steroids are first-line. Systemic agents are considered for severe or refractory cases. The framework is stepwise and minimizes overtreatment.
""",
        key_factors=[
            "Clinical features",
            "Dermoscopy findings",
            "Biopsy results",
            "Severity and impact on function"
        ],
        primary_authority=[
            "National Psoriasis Foundation",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Systemic therapy may be warranted earlier.",
        counter_arguments=[
            "Systemic agents have significant side effects.",
            "Stepwise approach is evidence-based."
        ],
        resolution_strategy="Escalate therapy based on severity and impact.",
        entity_scope="Patients with nail psoriasis",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="NPF Nail Psoriasis Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Chronic Wound Infection Diagnosis",
        keywords=["chronic wound", "infection", "diagnosis", "wound care"],
        conclusion_template="Clinical assessment, supported by tissue biopsy for culture, is the standard for diagnosing chronic wound infection.",
        reasoning_framework="""
Signs of infection (erythema, warmth, pain, exudate, delayed healing) prompt further investigation. Superficial swabs are less reliable than tissue biopsy for microbiological diagnosis. Imaging may be indicated for suspected osteomyelitis. The framework prioritizes accurate diagnosis to guide targeted therapy and prevent resistance.
""",
        key_factors=[
            "Clinical signs of infection",
            "Biopsy for culture",
            "Imaging findings",
            "Patient comorbidities"
        ],
        primary_authority=[
            "Infectious Diseases Society of America",
            "Wound Healing Society"
        ],
        burden_holder="Clinician",
        adversary_position="Swab cultures are less invasive.",
        counter_arguments=[
            "Swabs may yield contaminants.",
            "Biopsy provides definitive results."
        ],
        resolution_strategy="Reserve swabs for superficial wounds only.",
        entity_scope="Patients with chronic wounds",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IDSA Guidelines 2012"
    ),
    DoctrineBlock(
        topic="Photoprotection Counseling in Dermatology",
        keywords=["photoprotection", "counseling", "UV exposure", "skin cancer prevention"],
        conclusion_template="All patients should receive counseling on photoprotection to reduce skin cancer risk.",
        reasoning_framework="""
Photoprotection includes sunscreen (SPF ≥30, broad-spectrum), protective clothing, shade, and avoidance of peak UV hours. Counseling is especially important for high-risk groups (fair skin, immunosuppressed, history of skin cancer). Regular reapplication and education on proper use are emphasized. The framework is preventive and universally applicable.
""",
        key_factors=[
            "Patient risk factors",
            "Sunscreen use",
            "Behavioral modification",
            "Education"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "Skin Cancer Foundation"
        ],
        burden_holder="Clinician",
        adversary_position="Compliance with photoprotection is low.",
        counter_arguments=[
            "Education improves adherence.",
            "Visual aids and reminders are effective."
        ],
        resolution_strategy="Incorporate counseling into every visit.",
        entity_scope="All dermatology patients",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAD Photoprotection Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Rosacea Subtype-Specific Management",
        keywords=["rosacea", "subtype", "management", "treatment"],
        conclusion_template="Rosacea management should be tailored to subtype: erythematotelangiectatic, papulopustular, phymatous, or ocular.",
        reasoning_framework="""
Each subtype responds to different therapies. Erythematotelangiectatic: topical vasoconstrictors, laser. Papulopustular: topical metronidazole, azelaic acid, oral tetracyclines. Phymatous: surgical or laser therapy. Ocular: lid hygiene, oral antibiotics, ophthalmology referral. The framework avoids one-size-fits-all treatment and improves outcomes.
""",
        key_factors=[
            "Subtype identification",
            "Severity",
            "Patient preference",
            "Comorbidities"
        ],
        primary_authority=[
            "National Rosacea Society",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Overlap between subtypes complicates management.",
        counter_arguments=[
            "Combination therapy is often needed.",
            "Subtype identification guides initial therapy."
        ],
        resolution_strategy="Reassess and adjust therapy as needed.",
        entity_scope="Patients with rosacea",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="NRS Rosacea Guidelines 2017"
    ),
    DoctrineBlock(
        topic="Dermatologic Surgery Antimicrobial Prophylaxis",
        keywords=["dermatologic surgery", "antimicrobial prophylaxis", "infection prevention"],
        conclusion_template="Antimicrobial prophylaxis is indicated only for high-risk dermatologic surgeries or patients.",
        reasoning_framework="""
Routine use of antibiotics is not recommended for clean dermatologic procedures. Indications include prosthetic implants, immunosuppression, or surgery on lower extremities with lymphedema. The framework minimizes antibiotic resistance and adverse events. Preoperative assessment identifies candidates for prophylaxis.
""",
        key_factors=[
            "Type of procedure",
            "Patient risk factors",
            "Surgical site",
            "History of infection"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "Infectious Diseases Society of America"
        ],
        burden_holder="Clinician",
        adversary_position="Prophylaxis may prevent rare but serious infections.",
        counter_arguments=[
            "Risks of resistance outweigh benefits in most cases.",
            "Strict criteria ensure appropriate use."
        ],
        resolution_strategy="Follow evidence-based indications for prophylaxis.",
        entity_scope="Dermatologic surgery patients",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Antimicrobial Prophylaxis Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Hidradenitis Suppurativa Stepwise Management",
        keywords=["hidradenitis suppurativa", "management", "treatment", "stepwise"],
        conclusion_template="Hidradenitis suppurativa should be managed with a stepwise approach, escalating from topical to systemic and surgical therapy.",
        reasoning_framework="""
Mild disease: topical clindamycin. Moderate: oral antibiotics, hormonal therapy. Severe/refractory: biologics (adalimumab), surgical intervention. Pain management and wound care are integral. The framework prioritizes quality of life and minimizes scarring. Multidisciplinary care may be needed.
""",
        key_factors=[
            "Disease severity",
            "Response to prior therapy",
            "Comorbidities",
            "Impact on quality of life"
        ],
        primary_authority=[
            "Hidradenitis Suppurativa Foundation",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Early biologic use may improve outcomes.",
        counter_arguments=[
            "Biologics have significant risks and costs.",
            "Stepwise escalation is evidence-based."
        ],
        resolution_strategy="Escalate therapy per guidelines; document rationale for deviation.",
        entity_scope="Patients with hidradenitis suppurativa",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="HSF Management Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Systemic Retinoids in Women of Childbearing Potential",
        keywords=["systemic retinoids", "isotretinoin", "teratogenicity", "women", "pregnancy"],
        conclusion_template="Systemic retinoids are contraindicated in women of childbearing potential unless strict pregnancy prevention programs are followed.",
        reasoning_framework="""
Isotretinoin and acitretin are highly teratogenic. Prescribing requires enrollment in risk management programs (e.g., iPLEDGE), negative pregnancy tests, and dual contraception. Informed consent is mandatory. The framework prioritizes fetal safety and legal compliance. Exceptions are not permitted.
""",
        key_factors=[
            "Pregnancy status",
            "Contraceptive use",
            "Patient education",
            "Compliance with monitoring"
        ],
        primary_authority=[
            "FDA",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Programs are burdensome and may limit access.",
        counter_arguments=[
            "Fetal risk is unacceptable.",
            "Programs are mandated by law."
        ],
        resolution_strategy="Strict adherence to risk management protocols.",
        entity_scope="Women of childbearing potential",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FDA iPLEDGE Program"
    ),
    DoctrineBlock(
        topic="Dermoscopy in Pigmented Lesion Assessment",
        keywords=["dermoscopy", "pigmented lesion", "assessment", "diagnosis"],
        conclusion_template="Dermoscopy should be used to improve diagnostic accuracy of pigmented lesions.",
        reasoning_framework="""
Dermoscopy reveals subsurface structures not visible to the naked eye, increasing sensitivity and specificity for melanoma and other skin cancers. Training is required for accurate interpretation. The framework supports routine use in dermatology practice, with referral for uncertain lesions.
""",
        key_factors=[
            "Lesion morphology",
            "Dermoscopy patterns",
            "Clinician expertise",
            "Patient risk factors"
        ],
        primary_authority=[
            "International Dermoscopy Society",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Dermoscopy may yield false positives/negatives.",
        counter_arguments=[
            "Training mitigates misinterpretation.",
            "Adjunct to, not replacement for, biopsy."
        ],
        resolution_strategy="Combine dermoscopy with clinical judgment.",
        entity_scope="Patients with pigmented lesions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IDS Dermoscopy Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Biopsy Technique Selection in Dermatology",
        keywords=["biopsy", "technique", "punch", "shave", "excisional", "dermatology"],
        conclusion_template="Biopsy technique should be selected based on lesion type, size, and suspected diagnosis.",
        reasoning_framework="""
Shave biopsy is suitable for raised, superficial lesions (e.g., BCC, SCC in situ). Punch biopsy is preferred for inflammatory dermatoses and small, flat lesions. Excisional biopsy is indicated for suspected melanoma or subcutaneous tumors. The framework prioritizes diagnostic yield and minimizes morbidity.
""",
        key_factors=[
            "Lesion morphology",
            "Suspected diagnosis",
            "Anatomic location",
            "Patient comorbidities"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Inappropriate technique may compromise diagnosis.",
        counter_arguments=[
            "Guidelines support technique selection.",
            "Training reduces errors."
        ],
        resolution_strategy="Choose technique per guidelines and clinical context.",
        entity_scope="All dermatology patients requiring biopsy",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Biopsy Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Chronic Urticaria Management Algorithm",
        keywords=["chronic urticaria", "management", "algorithm", "antihistamines"],
        conclusion_template="Chronic urticaria should be managed with second-generation antihistamines, up-dosed as needed, before considering add-on therapy.",
        reasoning_framework="""
Start with standard-dose second-generation antihistamines. If inadequate, increase up to fourfold. Add-on therapy includes omalizumab or cyclosporine. First-generation antihistamines are avoided due to sedation. The framework is stepwise, evidence-based, and prioritizes safety.
""",
        key_factors=[
            "Symptom severity",
            "Response to antihistamines",
            "Comorbidities",
            "Side effect profile"
        ],
        primary_authority=[
            "EAACI/GA2LEN/EDF/WAO",
            "American Academy of Allergy, Asthma & Immunology"
        ],
        burden_holder="Clinician",
        adversary_position="Early use of biologics may improve quality of life.",
        counter_arguments=[
            "Biologics are costly and reserved for refractory cases.",
            "Stepwise escalation is effective for most patients."
        ],
        resolution_strategy="Escalate therapy per guidelines; document rationale for deviation.",
        entity_scope="Patients with chronic urticaria",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EAACI/GA2LEN/EDF/WAO Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Non-Melanoma Skin Cancer Margin Guidelines",
        keywords=["non-melanoma skin cancer", "margin", "excision", "BCC", "SCC"],
        conclusion_template="Standard surgical margins for BCC and SCC should be followed to ensure complete excision.",
        reasoning_framework="""
For low-risk BCC: 4mm margin. For low-risk SCC: 4–6mm margin. High-risk tumors require wider margins or Mohs surgery. The framework is evidence-based to minimize recurrence while preserving tissue. Margins are measured clinically and confirmed histologically.
""",
        key_factors=[
            "Tumor type",
            "Risk stratification",
            "Location",
            "Histologic subtype"
        ],
        primary_authority=[
            "National Comprehensive Cancer Network",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Narrow margins may increase recurrence.",
        counter_arguments=[
            "Guidelines balance recurrence risk and tissue preservation.",
            "Mohs surgery is available for high-risk cases."
        ],
        resolution_strategy="Follow margin guidelines; escalate as needed.",
        entity_scope="Patients with NMSC",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NCCN Guidelines 2023"
    ),
    DoctrineBlock(
        topic="Psoriatic Arthritis Screening in Psoriasis Patients",
        keywords=["psoriatic arthritis", "screening", "psoriasis", "musculoskeletal"],
        conclusion_template="All psoriasis patients should be screened for psoriatic arthritis at regular intervals.",
        reasoning_framework="""
Psoriatic arthritis is underdiagnosed and leads to irreversible joint damage. Screening includes history (joint pain, stiffness), physical exam, and validated questionnaires (PEST, ToPAS). Early rheumatology referral improves outcomes. The framework is preventive and universally applicable.
""",
        key_factors=[
            "History of joint symptoms",
            "Physical exam findings",
            "Screening questionnaire results",
            "Disease duration"
        ],
        primary_authority=[
            "National Psoriasis Foundation",
            "American College of Rheumatology"
        ],
        burden_holder="Clinician",
        adversary_position="Screening may increase unnecessary referrals.",
        counter_arguments=[
            "Early diagnosis prevents disability.",
            "Validated tools improve specificity."
        ],
        resolution_strategy="Screen annually and refer as indicated.",
        entity_scope="All psoriasis patients",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NPF Psoriatic Arthritis Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Cutaneous Lupus Erythematosus Management",
        keywords=["cutaneous lupus", "management", "treatment", "SLE"],
        conclusion_template="Cutaneous lupus erythematosus should be managed with photoprotection, topical therapy, and systemic agents as needed.",
        reasoning_framework="""
Photoprotection is foundational. Topical steroids or calcineurin inhibitors are first-line. Antimalarials (hydroxychloroquine) are added for extensive or refractory disease. Monitor for systemic involvement. The framework is stepwise and multidisciplinary.
""",
        key_factors=[
            "Disease extent",
            "Response to topical therapy",
            "Systemic symptoms",
            "Adherence"
        ],
        primary_authority=[
            "American College of Rheumatology",
            "European League Against Rheumatism"
        ],
        burden_holder="Clinician",
        adversary_position="Systemic therapy may be needed earlier.",
        counter_arguments=[
            "Stepwise escalation reduces unnecessary exposure.",
            "Monitor for systemic progression."
        ],
        resolution_strategy="Escalate therapy per guidelines.",
        entity_scope="Patients with cutaneous lupus",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACR/EULAR Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Vitiligo Treatment Algorithm",
        keywords=["vitiligo", "treatment", "algorithm", "management"],
        conclusion_template="Vitiligo treatment should be individualized, starting with topical agents and escalating to phototherapy or surgery.",
        reasoning_framework="""
Topical corticosteroids or calcineurin inhibitors are first-line for localized disease. Narrowband UVB is effective for generalized vitiligo. Surgical options (grafting) are reserved for stable, refractory cases. The framework incorporates patient preference, disease extent, and psychosocial impact.
""",
        key_factors=[
            "Disease extent",
            "Stability",
            "Response to therapy",
            "Patient preference"
        ],
        primary_authority=[
            "Vitiligo Working Group",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Early phototherapy may improve outcomes.",
        counter_arguments=[
            "Phototherapy is resource-intensive.",
            "Stepwise approach is evidence-based."
        ],
        resolution_strategy="Escalate therapy as indicated; involve patient in decisions.",
        entity_scope="Patients with vitiligo",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="VWG Guidelines 2017"
    ),
    DoctrineBlock(
        topic="Immunosuppressed Patient Skin Cancer Surveillance",
        keywords=["immunosuppressed", "skin cancer", "surveillance", "transplant"],
        conclusion_template="Immunosuppressed patients require regular, lifelong skin cancer surveillance.",
        reasoning_framework="""
Organ transplant recipients and other immunosuppressed patients have increased risk of aggressive skin cancers. Full skin exams are recommended every 6–12 months. Patient education on self-exam and photoprotection is essential. The framework is preventive and multidisciplinary.
""",
        key_factors=[
            "Immunosuppression status",
            "History of skin cancer",
            "Duration since transplant",
            "Photoprotection adherence"
        ],
        primary_authority=[
            "International Transplant Skin Cancer Collaborative",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Frequent exams may burden patients.",
        counter_arguments=[
            "Early detection reduces morbidity.",
            "Education empowers self-surveillance."
        ],
        resolution_strategy="Schedule regular exams and reinforce education.",
        entity_scope="Immunosuppressed patients",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ITSCC Guidelines 2017"
    ),
    DoctrineBlock(
        topic="Eczema Herpeticum Recognition and Management",
        keywords=["eczema herpeticum", "recognition", "management", "atopic dermatitis", "HSV"],
        conclusion_template="Eczema herpeticum should be promptly recognized and treated with systemic antivirals.",
        reasoning_framework="""
Eczema herpeticum presents as painful, umbilicated vesicles in atopic dermatitis patients, often with fever and lymphadenopathy. Delayed treatment can lead to dissemination and mortality. Systemic acyclovir is first-line. Hospitalization may be required for severe cases. The framework emphasizes early recognition and intervention.
""",
        key_factors=[
            "Clinical presentation",
            "History of atopic dermatitis",
            "HSV exposure",
            "Systemic symptoms"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "Infectious Diseases Society of America"
        ],
        burden_holder="Clinician",
        adversary_position="Overdiagnosis may lead to unnecessary antivirals.",
        counter_arguments=[
            "Delayed treatment is life-threatening.",
            "Diagnosis is clinical; confirm with PCR if needed."
        ],
        resolution_strategy="Treat empirically when suspected.",
        entity_scope="Patients with atopic dermatitis and acute vesicular eruption",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2014"
    ),
    DoctrineBlock(
        topic="Scabies Diagnosis and Outbreak Control",
        keywords=["scabies", "diagnosis", "outbreak", "control", "management"],
        conclusion_template="Scabies diagnosis is clinical, supported by microscopy; outbreaks require simultaneous treatment of all contacts.",
        reasoning_framework="""
Classic presentation: pruritic papules, burrows, nocturnal itching. Microscopy of skin scrapings confirms diagnosis. During outbreaks (e.g., institutions), treat all contacts simultaneously to prevent reinfestation. Environmental decontamination (bedding, clothing) is essential. The framework is public health-oriented.
""",
        key_factors=[
            "Clinical features",
            "Microscopy results",
            "Contact tracing",
            "Environmental cleaning"
        ],
        primary_authority=[
            "Centers for Disease Control and Prevention",
            "World Health Organization"
        ],
        burden_holder="Clinician/Public Health Officer",
        adversary_position="Mass treatment may be logistically challenging.",
        counter_arguments=[
            "Partial treatment leads to recurrence.",
            "Education and planning facilitate control."
        ],
        resolution_strategy="Coordinate with public health authorities.",
        entity_scope="Patients and contacts in scabies outbreaks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CDC Scabies Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Alopecia Areata Management",
        keywords=["alopecia areata", "management", "treatment", "hair loss"],
        conclusion_template="Alopecia areata is managed with intralesional steroids for limited disease and systemic agents for extensive involvement.",
        reasoning_framework="""
Limited patches: intralesional triamcinolone. Extensive or rapidly progressive: systemic steroids, JAK inhibitors, or immunotherapy. Spontaneous regrowth is possible. The framework incorporates patient preference, disease extent, and psychosocial impact.
""",
        key_factors=[
            "Extent of hair loss",
            "Disease activity",
            "Patient age",
            "Psychosocial impact"
        ],
        primary_authority=[
            "National Alopecia Areata Foundation",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Systemic therapy may have significant side effects.",
        counter_arguments=[
            "Shared decision-making is essential.",
            "Monitor for adverse events."
        ],
        resolution_strategy="Individualize therapy and monitor closely.",
        entity_scope="Patients with alopecia areata",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD Alopecia Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Cutaneous Drug Reaction Classification",
        keywords=["cutaneous drug reaction", "classification", "exanthem", "SJS", "TEN"],
        conclusion_template="Cutaneous drug reactions should be classified by morphology and severity to guide management.",
        reasoning_framework="""
Exanthematous (morbilliform) eruptions are most common and often benign. Severe reactions (SJS/TEN, DRESS, AGEP) require immediate drug withdrawal and supportive care. Classification is based on morphology, timing, and systemic involvement. The framework ensures prompt recognition and intervention.
""",
        key_factors=[
            "Morphology",
            "Timing relative to drug exposure",
            "Systemic symptoms",
            "Severity"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "European Society of Cutaneous Drug Reactions"
        ],
        burden_holder="Clinician",
        adversary_position="Overlap syndromes may complicate classification.",
        counter_arguments=[
            "Early recognition saves lives.",
            "Multidisciplinary input may be needed."
        ],
        resolution_strategy="Classify and manage per guidelines.",
        entity_scope="Patients with suspected drug reactions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAD Drug Reaction Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Herpes Zoster Antiviral Therapy Timing",
        keywords=["herpes zoster", "antiviral", "therapy", "timing", "shingles"],
        conclusion_template="Antiviral therapy for herpes zoster should be initiated within 72 hours of rash onset.",
        reasoning_framework="""
Early antiviral therapy (acyclovir, valacyclovir, famciclovir) reduces duration, severity, and risk of postherpetic neuralgia. Initiation beyond 72 hours may be considered in immunocompromised or severe cases. The framework prioritizes early recognition and intervention.
""",
        key_factors=[
            "Time since rash onset",
            "Immunosuppression status",
            "Severity",
            "Comorbidities"
        ],
        primary_authority=[
            "Centers for Disease Control and Prevention",
            "Infectious Diseases Society of America"
        ],
        burden_holder="Clinician",
        adversary_position="Late initiation may still provide benefit.",
        counter_arguments=[
            "Greatest benefit is within 72 hours.",
            "Consider therapy in severe or immunosuppressed cases."
        ],
        resolution_strategy="Initiate therapy as early as possible.",
        entity_scope="Patients with herpes zoster",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CDC Herpes Zoster Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Melasma Treatment Principles",
        keywords=["melasma", "treatment", "management", "hyperpigmentation"],
        conclusion_template="Melasma treatment combines photoprotection, topical agents, and procedural interventions as needed.",
        reasoning_framework="""
Photoprotection is foundational. Topical hydroquinone, retinoids, and corticosteroids are first-line. Chemical peels, lasers, and tranexamic acid are considered for refractory cases. The framework is stepwise and individualized, with attention to side effects and recurrence.
""",
        key_factors=[
            "Severity",
            "Response to therapy",
            "Patient skin type",
            "Adherence"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "International Pigment Cell Society"
        ],
        burden_holder="Clinician",
        adversary_position="Procedures may increase risk of post-inflammatory hyperpigmentation.",
        counter_arguments=[
            "Careful patient selection and technique minimize risk.",
            "Photoprotection reduces recurrence."
        ],
        resolution_strategy="Escalate therapy as indicated; educate on photoprotection.",
        entity_scope="Patients with melasma",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD Melasma Guidelines 2017"
    ),
    DoctrineBlock(
        topic="Bullous Pemphigoid Diagnosis and Management",
        keywords=["bullous pemphigoid", "diagnosis", "management", "autoimmune blistering"],
        conclusion_template="Diagnosis of bullous pemphigoid requires clinical, histological, and immunopathological confirmation; management is stepwise.",
        reasoning_framework="""
Clinical features: tense bullae on erythematous base in elderly. Diagnosis confirmed by biopsy for H&E and direct immunofluorescence. Topical or systemic steroids are first-line; steroid-sparing agents (doxycycline, immunosuppressants) for refractory cases. The framework is multidisciplinary and minimizes steroid exposure.
""",
        key_factors=[
            "Clinical presentation",
            "Histology",
            "Direct immunofluorescence",
            "Response to therapy"
        ],
        primary_authority=[
            "European Academy of Dermatology and Venereology",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Steroid-sparing agents may be needed earlier.",
        counter_arguments=[
            "Stepwise escalation reduces side effects.",
            "Monitor for infection and adverse events."
        ],
        resolution_strategy="Individualize therapy and monitor closely.",
        entity_scope="Patients with bullous pemphigoid",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EADV Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Lichen Planus Diagnosis and Management",
        keywords=["lichen planus", "diagnosis", "management", "treatment"],
        conclusion_template="Lichen planus is diagnosed clinically and histologically; management is stepwise, starting with topical steroids.",
        reasoning_framework="""
Classic features: violaceous, flat-topped papules with Wickham striae. Biopsy confirms diagnosis. Topical steroids are first-line; systemic agents (retinoids, immunosuppressants) for extensive or mucosal disease. Monitor for malignant transformation in mucosal LP. The framework is stepwise and multidisciplinary.
""",
        key_factors=[
            "Clinical features",
            "Histology",
            "Disease extent",
            "Response to therapy"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Systemic therapy may be warranted earlier.",
        counter_arguments=[
            "Stepwise escalation reduces unnecessary exposure.",
            "Monitor for complications."
        ],
        resolution_strategy="Escalate therapy as indicated.",
        entity_scope="Patients with lichen planus",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Pyoderma Gangrenosum Diagnosis and Management",
        keywords=["pyoderma gangrenosum", "diagnosis", "management", "ulcer"],
        conclusion_template="Pyoderma gangrenosum is a diagnosis of exclusion; management is immunosuppression and wound care.",
        reasoning_framework="""
Rapidly progressive, painful ulcer with undermined borders. Exclude infection, vasculitis, and malignancy. Biopsy for histology and culture. Systemic steroids or cyclosporine are first-line. Wound care and pain management are essential. The framework is multidisciplinary and individualized.
""",
        key_factors=[
            "Clinical presentation",
            "Exclusion of mimickers",
            "Histology",
            "Response to therapy"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Immunosuppression increases infection risk.",
        counter_arguments=[
            "Infection must be excluded before therapy.",
            "Monitor for adverse events."
        ],
        resolution_strategy="Multidisciplinary management and close monitoring.",
        entity_scope="Patients with suspected pyoderma gangrenosum",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="BAD Guidelines 2019"
    ),
    DoctrineBlock(
        topic="Seborrheic Keratosis Diagnosis and Management",
        keywords=["seborrheic keratosis", "diagnosis", "management", "benign lesion"],
        conclusion_template="Seborrheic keratosis is diagnosed clinically; removal is cosmetic unless symptomatic.",
        reasoning_framework="""
Waxy, stuck-on appearance with variable pigmentation. Dermoscopy aids diagnosis. Biopsy if atypical features or concern for malignancy. Removal options: cryotherapy, curettage, shave excision. The framework is patient-centered and minimizes unnecessary procedures.
""",
        key_factors=[
            "Clinical features",
            "Dermoscopy",
            "Patient symptoms",
            "Atypical features"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Unnecessary removal increases cost and risk.",
        counter_arguments=[
            "Patient preference is important.",
            "Biopsy if malignancy cannot be excluded."
        ],
        resolution_strategy="Educate patients; remove only if indicated.",
        entity_scope="Patients with seborrheic keratoses",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Tinea Diagnosis and Management",
        keywords=["tinea", "dermatophyte", "fungal infection", "diagnosis", "management"],
        conclusion_template="Tinea diagnosis is clinical, confirmed by KOH prep or culture; management is topical or systemic antifungals based on site.",
        reasoning_framework="""
Annular, scaly plaques with central clearing suggest tinea. KOH prep or fungal culture confirms diagnosis. Topical antifungals for skin; systemic for hair, nails, or refractory cases. The framework is evidence-based and minimizes resistance.
""",
        key_factors=[
            "Clinical features",
            "KOH prep",
            "Culture",
            "Site of infection"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Empiric therapy may suffice.",
        counter_arguments=[
            "Confirmation prevents misdiagnosis.",
            "Systemic therapy has risks."
        ],
        resolution_strategy="Confirm diagnosis before systemic therapy.",
        entity_scope="Patients with suspected tinea",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Contact Dermatitis Avoidance Strategy",
        keywords=["contact dermatitis", "avoidance", "allergen", "irritant", "management"],
        conclusion_template="Identification and avoidance of causative agents are central to contact dermatitis management.",
        reasoning_framework="""
Patch testing identifies allergens. Patient education on avoidance is essential. Barrier creams and emollients support skin healing. Topical steroids for flares. The framework is preventive and patient-centered.
""",
        key_factors=[
            "Allergen identification",
            "Patient education",
            "Barrier protection",
            "Adherence"
        ],
        primary_authority=[
            "American Contact Dermatitis Society",
            "European Society of Contact Dermatitis"
        ],
        burden_holder="Clinician",
        adversary_position="Complete avoidance may be impractical.",
        counter_arguments=[
            "Partial reduction improves outcomes.",
            "Education and support are key."
        ],
        resolution_strategy="Provide resources and follow-up.",
        entity_scope="Patients with contact dermatitis",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ACDS Guidelines 2015"
    ),
    DoctrineBlock(
        topic="Chronic Venous Ulcer Management",
        keywords=["chronic venous ulcer", "management", "compression", "wound care"],
        conclusion_template="Compression therapy is the mainstay of chronic venous ulcer management.",
        reasoning_framework="""
Diagnosis confirmed by clinical exam and duplex ultrasound. Compression stockings or wraps improve healing. Wound care includes debridement and infection control. Address underlying venous insufficiency. The framework is multidisciplinary and evidence-based.
""",
        key_factors=[
            "Ulcer etiology",
            "Compression therapy",
            "Wound care",
            "Venous assessment"
        ],
        primary_authority=[
            "Wound Healing Society",
            "Society for Vascular Surgery"
        ],
        burden_holder="Clinician",
        adversary_position="Compression may be contraindicated in arterial disease.",
        counter_arguments=[
            "Assess arterial status before compression.",
            "Alternative therapies available."
        ],
        resolution_strategy="Individualize therapy based on vascular assessment.",
        entity_scope="Patients with venous ulcers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="WHS Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Molluscum Contagiosum Management in Children",
        keywords=["molluscum contagiosum", "management", "children", "treatment"],
        conclusion_template="Molluscum contagiosum is self-limited; treatment is indicated for symptoms, immunosuppression, or cosmetic concerns.",
        reasoning_framework="""
Observation is appropriate for most cases. Curettage, cryotherapy, or topical agents for symptomatic or persistent lesions. Avoid aggressive therapy in atopic dermatitis. The framework is patient-centered and minimizes harm.
""",
        key_factors=[
            "Symptom severity",
            "Immunosuppression",
            "Patient/parent preference",
            "Atopic dermatitis status"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "British Association of Dermatologists"
        ],
        burden_holder="Clinician",
        adversary_position="Treatment may cause pain or scarring.",
        counter_arguments=[
            "Educate on self-limited nature.",
            "Use gentle methods if needed."
        ],
        resolution_strategy="Shared decision-making with family.",
        entity_scope="Children with molluscum contagiosum",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Urticaria Acute vs Chronic Classification",
        keywords=["urticaria", "acute", "chronic", "classification", "hives"],
        conclusion_template="Urticaria is classified as acute (<6 weeks) or chronic (≥6 weeks) to guide evaluation and management.",
        reasoning_framework="""
Acute urticaria is often self-limited and triggered by infection or allergen. Chronic urticaria is idiopathic in most cases and requires stepwise antihistamine therapy. The framework ensures appropriate workup and avoids unnecessary testing.
""",
        key_factors=[
            "Duration of symptoms",
            "Trigger identification",
            "Response to therapy",
            "Systemic symptoms"
        ],
        primary_authority=[
            "EAACI/GA2LEN/EDF/WAO",
            "American Academy of Allergy, Asthma & Immunology"
        ],
        burden_holder="Clinician",
        adversary_position="Classification may not impact therapy.",
        counter_arguments=[
            "Classification guides evaluation and prognosis.",
            "Chronic urticaria requires different approach."
        ],
        resolution_strategy="Classify at initial presentation.",
        entity_scope="Patients with urticaria",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EAACI/GA2LEN/EDF/WAO Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Dermatology Telemedicine Best Practices",
        keywords=["telemedicine", "dermatology", "best practices", "remote care"],
        conclusion_template="Telemedicine in dermatology should follow best practices for image quality, privacy, and documentation.",
        reasoning_framework="""
High-resolution images with proper lighting and scale improve diagnostic accuracy. Secure platforms protect patient privacy. Documentation must meet legal and ethical standards. In-person follow-up is arranged for uncertain or high-risk cases. The framework ensures quality and safety in remote care.
""",
        key_factors=[
            "Image quality",
            "Platform security",
            "Documentation",
            "Appropriateness for remote care"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "American Telemedicine Association"
        ],
        burden_holder="Clinician",
        adversary_position="Telemedicine may miss subtle findings.",
        counter_arguments=[
            "Triaging and follow-up mitigate risk.",
            "Improves access to care."
        ],
        resolution_strategy="Follow best practices and arrange in-person care as needed.",
        entity_scope="Patients receiving teledermatology",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="AAD Teledermatology Guidelines 2020"
    ),
    DoctrineBlock(
        topic="Cutaneous T-Cell Lymphoma Diagnosis and Staging",
        keywords=["cutaneous T-cell lymphoma", "CTCL", "diagnosis", "staging", "mycosis fungoides"],
        conclusion_template="Diagnosis of CTCL requires clinicopathologic correlation; staging guides management.",
        reasoning_framework="""
Multiple biopsies may be needed for diagnosis. Staging includes skin, lymph node, blood, and visceral involvement. Management is multidisciplinary. The framework ensures accurate diagnosis and appropriate therapy.
""",
        key_factors=[
            "Clinical features",
            "Histology",
            "Immunophenotyping",
            "Staging workup"
        ],
        primary_authority=[
            "International Society for Cutaneous Lymphomas",
            "American Academy of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Diagnosis may be delayed due to subtle findings.",
        counter_arguments=[
            "Repeat biopsies and expert review improve accuracy.",
            "Early staging informs prognosis."
        ],
        resolution_strategy="Multidisciplinary approach and expert consultation.",
        entity_scope="Patients with suspected CTCL",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="ISCL Guidelines 2017"
    ),
    DoctrineBlock(
        topic="Sunscreen Use in Infants and Children",
        keywords=["sunscreen", "infants", "children", "photoprotection", "safety"],
        conclusion_template="Sunscreen is recommended for children >6 months; infants <6 months should avoid direct sun exposure.",
        reasoning_framework="""
Physical barriers (clothing, shade) are preferred for infants <6 months. For older children, broad-spectrum SPF ≥30 sunscreen is safe and effective. Reapply every 2 hours and after swimming. The framework is preventive and evidence-based.
""",
        key_factors=[
            "Age",
            "Sun exposure risk",
            "Sunscreen type",
            "Parental education"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "American Academy of Pediatrics"
        ],
        burden_holder="Clinician/Parent",
        adversary_position="Sunscreen may cause irritation in infants.",
        counter_arguments=[
            "Physical barriers are first-line for infants.",
            "Test sunscreen on small area first."
        ],
        resolution_strategy="Educate parents on safe sun practices.",
        entity_scope="Infants and children",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Pruritus Evaluation in Elderly Patients",
        keywords=["pruritus", "elderly", "evaluation", "itch", "geriatric dermatology"],
        conclusion_template="Evaluation of pruritus in elderly patients should include assessment for systemic disease and xerosis.",
        reasoning_framework="""
Common causes: xerosis, medication side effects, systemic disease (renal, hepatic, hematologic). Workup includes history, exam, and targeted labs. Treat underlying cause and provide emollients. The framework is comprehensive and multidisciplinary.
""",
        key_factors=[
            "History and exam",
            "Medication review",
            "Laboratory workup",
            "Skin care"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "International Society of Geriatric Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Extensive workup may not be cost-effective.",
        counter_arguments=[
            "Systemic disease is common in elderly with pruritus.",
            "Targeted workup is justified."
        ],
        resolution_strategy="Individualize evaluation based on risk factors.",
        entity_scope="Elderly patients with pruritus",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Dermatology Quality of Life Assessment",
        keywords=["quality of life", "assessment", "dermatology", "DLQI", "impact"],
        conclusion_template="Quality of life assessment should be incorporated into dermatology practice using validated tools.",
        reasoning_framework="""
Dermatologic diseases impact psychosocial well-being. Tools like DLQI, Skindex, and CDLQI quantify impact and guide therapy. Regular assessment informs shared decision-making and outcome measurement. The framework is patient-centered and evidence-based.
""",
        key_factors=[
            "Disease impact",
            "Validated assessment tool",
            "Patient-reported outcomes",
            "Therapeutic response"
        ],
        primary_authority=[
            "American Academy of Dermatology",
            "International Society of Dermatology"
        ],
        burden_holder="Clinician",
        adversary_position="Quality of life tools may be time-consuming.",
        counter_arguments=[
            "Brief tools are available.",
            "Improves patient-centered care."
        ],
        resolution_strategy="Incorporate into routine visits.",
        entity_scope="All dermatology patients",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAD Guidelines 2016"
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
        if (query_lower in doctrine.topic.lower() or
            any(query_lower in kw.lower() for kw in doctrine.keywords) or
            query_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]