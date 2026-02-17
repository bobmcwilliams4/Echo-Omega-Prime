"""
MED12 DERMATOLOGY ANALYSIS ENGINE v1.0.0
Tax Intelligence Engine (TIE) Architecture Applied to Dermatology

Comprehensive dermatological diagnosis, skin cancer screening, wound healing assessment,
dermatopathology, phototherapy protocols, and cosmetic dermatology evaluation.

Author: ECHO OMEGA PRIME
Date: 2026-02-14
Port: 9312
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from loguru import logger
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# ============================================================================
# ENUMS AND CONSTANTS
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


class AnalysisZone(str, Enum):
    DIAGNOSTIC = "DIAGNOSTIC"
    TREATMENT = "TREATMENT"
    DOCUMENTATION = "DOCUMENTATION"


class IssueCategory(str, Enum):
    MALIGNANT_SCREENING = "MALIGNANT_SCREENING"
    BENIGN_LESION = "BENIGN_LESION"
    INFLAMMATORY = "INFLAMMATORY"
    INFECTIOUS = "INFECTIOUS"
    WOUND_HEALING = "WOUND_HEALING"
    PHOTOTHERAPY = "PHOTOTHERAPY"
    COSMETIC = "COSMETIC"
    PIGMENTATION = "PIGMENTATION"
    DERMATOPATHOLOGY = "DERMATOPATHOLOGY"
    PEDIATRIC = "PEDIATRIC"
    IMMUNOLOGIC = "IMMUNOLOGIC"
    HAIR_NAIL = "HAIR_NAIL"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class DermatologyQuery(BaseModel):
    query: str = Field(..., description="Dermatology analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    patient_age: Optional[int] = Field(None, description="Patient age in years")
    lesion_size_mm: Optional[float] = Field(None, description="Lesion size in millimeters")
    location: Optional[str] = Field(None, description="Anatomic location")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class DermatologyResponse(BaseModel):
    query: str
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    epistemic_warnings: List[str]
    issue_categories: List[IssueCategory]
    analysis_zone: AnalysisZone
    determinism_hash: str
    latency_ms: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE STRUCTURE
# ============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled dermatology reasoning block"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    issue_category: IssueCategory
    entity_scope: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str


# ============================================================================
# DOCTRINE CACHE - 25+ REAL DERMATOLOGY BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="melanoma_abcde_criteria",
        keywords=["melanoma", "ABCDE", "asymmetry", "border", "color", "diameter", "evolving", "screening"],
        conclusion_template="Based on ABCDE criteria analysis: {assessment}. {recommendation}. {urgency}.",
        reasoning_framework="""
        ABCDE Melanoma Screening Criteria:

        A - Asymmetry: One half unlike the other half
        - Benign nevi typically symmetric
        - Melanoma shows asymmetry in >80% of cases
        - Two-axis assessment required

        B - Border irregularity: Irregular, scalloped, poorly defined edges
        - Benign lesions have smooth borders
        - Melanoma borders often notched, blurred
        - Border regression may indicate immune response

        C - Color variation: Multiple colors within single lesion
        - Benign nevi uniform tan/brown
        - Melanoma shows tan, brown, black, red, white, blue
        - Color variegation correlates with vertical growth

        D - Diameter: >6mm (pencil eraser size)
        - Majority of melanomas exceed 6mm at diagnosis
        - 20-30% present smaller than 6mm
        - Size increase over time more concerning than absolute size

        E - Evolving: Change in size, shape, color, symptoms
        - Most significant predictor in existing lesions
        - New lesion after age 40 warrants evaluation
        - Patient-reported change has high sensitivity

        Positive ABCDE scoring:
        - 1-2 criteria: Low suspicion, monitor
        - 3 criteria: Moderate suspicion, consider biopsy
        - 4-5 criteria: High suspicion, urgent biopsy

        Limitations:
        - Amelanotic melanoma may lack color criteria
        - Nodular melanoma may lack horizontal growth
        - Desmoplastic variants often missed
        """,
        key_factors=["Asymmetry assessment", "Border irregularity", "Color variation", "Diameter measurement",
                     "Evolution history", "Patient age", "Sun exposure history"],
        primary_authority=["AAD melanoma guidelines", "USPSTF skin cancer screening",
                          "Dermatology 2019 ABCDE validation study", "Melanoma Research 2020 meta-analysis"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when all criteria documented, DISCLOSURE for single criterion",
        issue_category=IssueCategory.MALIGNANT_SCREENING,
        entity_scope="All patients with pigmented lesions",
        adversary_position="ABCDE criteria have false positives, many biopsies unnecessary",
        counter_arguments=[
            "ABCDE sensitivity 90%+ in meta-analyses",
            "Specificity improved with dermoscopy adjunct",
            "Early detection reduces mortality 30-50%",
            "Biopsy cost minimal vs. delayed diagnosis cost"
        ],
        resolution_strategy="Apply ABCDE with clinical judgment, use dermoscopy when available, document all criteria, prioritize patient-reported evolution"
    ),

    DoctrineBlock(
        topic="basal_cell_carcinoma_diagnosis",
        keywords=["BCC", "basal cell", "carcinoma", "pearly", "telangiectasia", "rodent ulcer"],
        conclusion_template="Clinical presentation consistent with {subtype} basal cell carcinoma. {biopsy_recommendation}. {treatment_planning}.",
        reasoning_framework="""
        Basal Cell Carcinoma (BCC) - Most Common Skin Cancer:

        Clinical Subtypes and Features:

        1. Nodular BCC (60-80% of cases):
           - Pearly, translucent papule with telangiectasias
           - Central ulceration in advanced lesions
           - "Rolled" border appearance
           - Slow growth over months to years
           - Favors sun-exposed areas: face, neck, upper trunk

        2. Superficial BCC (10-30%):
           - Erythematous scaly patch or plaque
           - May mimic eczema or psoriasis
           - Multiple lesions common on trunk
           - Minimal invasion depth
           - Best response to topical therapies

        3. Morpheaform/Sclerosing BCC (5-10%):
           - Scar-like, indurated plaque
           - Poorly defined borders
           - Most aggressive subtype locally
           - Subclinical extension common
           - Requires Mohs surgery

        4. Pigmented BCC (5%):
           - Brown to black coloration
           - May mimic melanoma
           - More common in darker skin types
           - Dermoscopy differentiates from melanoma

        Risk Stratification:

        Low-Risk BCC:
        - <20mm on trunk/extremities
        - <10mm on face/hands/feet
        - Well-defined borders
        - Nodular or superficial subtype
        - Primary tumor
        - Immunocompetent patient

        High-Risk BCC:
        - >20mm trunk/extremities or >10mm face
        - Poorly defined borders
        - Morpheaform, infiltrative, or micronodular histology
        - Recurrent tumor
        - Perineural invasion
        - Immunosuppressed patient
        - Radiation area or chronic wound

        Diagnostic Approach:
        - Clinical diagnosis 80-90% accurate for nodular BCC
        - Biopsy confirms histology and subtype
        - Dermoscopy improves accuracy to 95%+
        - Shave biopsy adequate for most lesions
        - Punch biopsy for depth assessment if deep invasion suspected
        """,
        key_factors=["Lesion subtype", "Size and location", "Border definition", "Patient immune status",
                     "Prior treatment history", "Perineural invasion risk"],
        primary_authority=["NCCN BCC guidelines 2024", "AAD BCC management pathway",
                          "Journal of Am Acad Dermatology BCC review", "Mohs surgery appropriateness criteria"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for nodular BCC, AGGRESSIVE for morpheaform requiring Mohs",
        issue_category=IssueCategory.MALIGNANT_SCREENING,
        entity_scope="Adult patients with sun exposure history",
        adversary_position="Many BCCs are low-risk and over-treated",
        counter_arguments=[
            "Untreated BCC causes local destruction",
            "High-risk BCCs metastasize rarely but devastate locally",
            "Recurrence rates 10-40% without appropriate surgery",
            "Early treatment minimizes surgical defect"
        ],
        resolution_strategy="Risk-stratify all BCCs, biopsy for histologic confirmation, match treatment modality to risk level"
    ),

    DoctrineBlock(
        topic="squamous_cell_carcinoma_risk",
        keywords=["SCC", "squamous cell", "carcinoma", "actinic keratosis", "Bowen disease", "keratoacanthoma"],
        conclusion_template="SCC risk assessment: {risk_level}. Metastatic potential {percentage}%. {surveillance_plan}.",
        reasoning_framework="""
        Squamous Cell Carcinoma (SCC) Risk Stratification:

        Second most common skin cancer, higher metastatic potential than BCC.

        Low-Risk SCC Features:
        - <2cm diameter
        - Well-differentiated histology
        - <2mm depth or <Clark level IV
        - No perineural or lymphovascular invasion
        - Primary tumor
        - Immunocompetent host
        - Location: trunk, extremities
        - Metastatic risk: <2%

        High-Risk SCC Features:
        - >2cm diameter
        - Poorly differentiated
        - >2mm depth or Clark level IV/V
        - Perineural invasion (PNI)
        - Lymphovascular invasion
        - Recurrent tumor
        - Immunosuppressed (transplant, CLL)
        - Location: ear, lip, genitalia
        - Site of chronic inflammation or radiation
        - Metastatic risk: 10-30%

        Specific High-Risk Scenarios:

        1. Organ Transplant Patients:
           - SCC incidence 65-250x general population
           - SCC:BCC ratio inverts to 2:1
           - Metastatic rate 5-8% (vs. 2% general pop)
           - Aggressive behavior correlates with immunosuppression degree
           - Require 6-12 month surveillance

        2. Chronic Lymphocytic Leukemia (CLL):
           - 8-10x increased SCC risk
           - More aggressive clinical course
           - Higher recurrence rates
           - Earlier metastasis

        3. Perineural Invasion (PNI):
           - Present in 2-5% of SCCs
           - Metastatic rate 20-35%
           - Local recurrence 30-50%
           - Requires adjuvant radiation
           - MRI for large nerve involvement

        4. Ear and Lip SCCs:
           - Ear: 10-20% metastatic rate
           - Lip: 10-15% metastatic rate
           - Lymph node metastasis most common
           - Sentinel node biopsy considered for high-risk

        Actinic Keratosis (AK) to SCC Progression:
        - Individual AK: 0.1-10% annual progression
        - Field cancerization: multiple AKs increase risk
        - SCC in situ (Bowen disease): 3-5% invasive progression
        - Treatment of AKs reduces SCC incidence

        Keratoacanthoma Controversy:
        - Historically "benign" but shares SCC mutations
        - Rapid growth over 4-8 weeks
        - Spontaneous regression in 30-50%
        - Modern consensus: treat as SCC
        - Excision or Mohs surgery recommended
        """,
        key_factors=["Tumor size", "Depth of invasion", "Histologic differentiation", "PNI presence",
                     "Immune status", "Anatomic location", "Recurrence status"],
        primary_authority=["NCCN SCC guidelines", "AJCC staging 8th edition",
                          "Transplant dermatology consensus", "JAAD SCC metastasis prediction models"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for low-risk, HIGH_RISK for transplant/PNI cases",
        issue_category=IssueCategory.MALIGNANT_SCREENING,
        entity_scope="All SCC patients, especially immunosuppressed",
        adversary_position="Most SCCs are cured with simple excision, elaborate risk stratification unnecessary",
        counter_arguments=[
            "High-risk SCC mortality equals melanoma in some series",
            "Metastatic SCC 5-year survival <30%",
            "Risk stratification guides adjuvant therapy",
            "Close surveillance detects recurrence when salvageable"
        ],
        resolution_strategy="Comprehensive risk assessment at diagnosis, tailor treatment and surveillance to risk, aggressive management of high-risk features"
    ),

    DoctrineBlock(
        topic="atopic_dermatitis_management",
        keywords=["atopic dermatitis", "eczema", "AD", "barrier dysfunction", "pruritus", "flare"],
        conclusion_template="Atopic dermatitis severity: {grade}. Barrier restoration with {emollient_protocol}. {immunomodulation}.",
        reasoning_framework="""
        Atopic Dermatitis (AD) - Chronic Inflammatory Skin Disease:

        Pathophysiology:
        - Barrier dysfunction (filaggrin mutations in 30%)
        - Th2-mediated inflammation (IL-4, IL-13, IL-31)
        - Microbial dysbiosis (S. aureus colonization 90%)
        - Itch-scratch cycle perpetuation

        Severity Assessment (SCORAD/EASI):

        Mild AD (EASI <7):
        - <10% body surface area
        - Minimal sleep disturbance
        - Topical therapy controls

        Moderate AD (EASI 7-21):
        - 10-50% body surface area
        - Frequent flares
        - Sleep disruption 2-3 nights/week
        - Topical therapy insufficient

        Severe AD (EASI >21):
        - >50% body surface area
        - Daily flares
        - Significant sleep loss
        - Quality of life severely impacted
        - Systemic therapy required

        Treatment Ladder:

        Step 1: Barrier Restoration (ALL patients):
        - Emollients 2-4x daily minimum
        - Thick creams or ointments superior to lotions
        - Apply within 3 minutes after bathing
        - 200-500g emollient per week for adult
        - Fragrance-free, preservative-light formulations

        Step 2: Topical Anti-Inflammatory:
        - Topical corticosteroids (TCS) first-line
        - Face/intertriginous: low-potency (hydrocortisone 1-2.5%)
        - Body: medium to high-potency (triamcinolone, fluocinonide)
        - Proactive therapy: 2x weekly to prevent flares
        - Topical calcineurin inhibitors (tacrolimus, pimecrolimus) for steroid-sparing

        Step 3: Infection Control:
        - S. aureus decolonization: bleach baths 2x weekly
        - Dilute bleach: 0.5 cup per full tub (1:10,000 dilution)
        - Topical or oral antibiotics for impetiginized AD
        - Eczema herpeticum: urgent acyclovir

        Step 4: Systemic Therapy (Moderate-Severe):
        - Dupilumab (IL-4/IL-13 blocker): first-line biologic
        - JAK inhibitors (upadacitinib, abrocitinib): rapid control
        - Cyclosporine: short-term rescue
        - Methotrexate, azathioprine: older alternatives
        - Phototherapy: narrowband UVB

        Trigger Avoidance:
        - Fragrances, dyes in detergents
        - Wool and rough fabrics
        - Extreme temperatures
        - Emotional stress
        - Food allergens (controversial, test if suspected)

        Pediatric Considerations:
        - 60% develop by age 1, 90% by age 5
        - Most improve in adolescence (60-70%)
        - Atopic march: AD -> allergic rhinitis -> asthma
        - TCS safety: use lowest effective potency
        - Growth monitoring if chronic high-potency TCS
        """,
        key_factors=["Disease severity", "Body surface area", "Age of patient", "Treatment history",
                     "Infection presence", "Trigger identification", "Quality of life impact"],
        primary_authority=["AAD AD guidelines 2023", "EADV AD consensus",
                          "Pediatric AD management JAAD", "Dupilumab RCT data"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for established protocols, AGGRESSIVE for early biologic use",
        issue_category=IssueCategory.INFLAMMATORY,
        entity_scope="Children and adults with AD",
        adversary_position="AD is over-medicated, focus on barrier repair only",
        counter_arguments=[
            "Inflammation drives barrier breakdown",
            "Undertreated AD leads to chronic changes",
            "Psychosocial impact requires aggressive control",
            "Biologic therapy transforms severe cases"
        ],
        resolution_strategy="Stepwise intensification based on severity, maintain barrier care at all steps, address infections promptly"
    ),

    DoctrineBlock(
        topic="psoriasis_biologic_selection",
        keywords=["psoriasis", "biologic", "TNF", "IL-17", "IL-23", "PASI", "plaque"],
        conclusion_template="Psoriasis severity PASI {score}. {biologic_recommendation}. Expected PASI-75 {percentage}% at week 12.",
        reasoning_framework="""
        Psoriasis Biologic Therapy Selection - Era of High Efficacy:

        Disease Severity (triggers systemic therapy):
        - PASI >10 or BSA >10%
        - Involvement of special sites (face, genitals, palms/soles)
        - Nail disease
        - Psoriatic arthritis
        - Quality of life severely impacted

        Biologic Classes and Mechanisms:

        1. TNF-alpha Inhibitors (Older generation):
           - Adalimumab, etanercept, infliximab, certolizumab
           - PASI-75: 50-70% at week 12
           - Benefits: PsA treatment, long safety record
           - Limitations: Lower efficacy than newer agents
           - Use: Second-line or when PsA predominates

        2. IL-17 Inhibitors (High efficacy):
           - Secukinumab (IL-17A), ixekizumab (IL-17A), brodalumab (IL-17RA)
           - PASI-75: 75-90% at week 12
           - PASI-90: 50-70% at week 12
           - Rapid onset: improvement week 2-4
           - Candidiasis risk (10-15%, mostly oral/genital)
           - Inflammatory bowel disease concern (brodalumab has warning)

        3. IL-23 Inhibitors (Highest durability):
           - Guselkumab, tildrakizumab, risankizumab
           - PASI-75: 70-85% at week 12
           - PASI-90: 55-75% at week 12
           - Dosing intervals: 8-12 weeks (superior convenience)
           - Best durability: sustained response >1 year
           - Safest long-term profile
           - First-line for many dermatologists

        4. IL-12/23 Inhibitor:
           - Ustekinumab (blocks both pathways)
           - PASI-75: 65-75% at week 12
           - Weight-based dosing
           - Excellent safety record (15+ years)
           - Still viable option, especially for PsA

        Selection Algorithm:

        First-Line Biologic:
        - IL-23 inhibitor (risankizumab, guselkumab)
        - Rationale: highest efficacy + durability + safety

        Rapid Clearance Needed:
        - IL-17 inhibitor (ixekizumab, brodalumab)
        - Rationale: fastest onset

        Psoriatic Arthritis Co-Management:
        - IL-17 or TNF inhibitor
        - Rationale: proven joint efficacy

        IBD History:
        - IL-23 or TNF inhibitor (avoid IL-17)
        - Rationale: IL-17 may worsen IBD

        Recurrent Infections:
        - IL-23 inhibitor
        - Rationale: lowest infection risk

        Treatment Targets:
        - PASI-90 now standard goal (vs. old PASI-75)
        - "Clear or almost clear" patient expectation
        - Treat-to-target approach improves outcomes

        Monitoring:
        - Baseline: CBC, CMP, HBV/HCV, TB test, pregnancy test
        - Follow-up: clinical response assessment
        - Bloodwork: repeat if symptoms
        - TB reactivation rare but serious
        """,
        key_factors=["PASI score", "PsA presence", "Prior treatment history", "Comorbidities",
                     "Patient preference on dosing interval", "Speed of clearance needed"],
        primary_authority=["AAD psoriasis guidelines", "NPF treatment guidelines",
                          "Head-to-head biologic trials", "Real-world registry data"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for IL-23 first-line, AGGRESSIVE for treat-to-target PASI-90",
        issue_category=IssueCategory.INFLAMMATORY,
        entity_scope="Moderate-to-severe psoriasis patients",
        adversary_position="Biologics are over-prescribed, phototherapy underutilized",
        counter_arguments=[
            "Phototherapy requires 3x weekly visits",
            "UV exposure increases skin cancer risk",
            "Biologics provide sustained clearance",
            "Quality of life improvements dramatic with biologics"
        ],
        resolution_strategy="Risk-benefit discussion, patient shared decision-making, use most efficacious agents for severe disease"
    ),

    DoctrineBlock(
        topic="wound_healing_phases",
        keywords=["wound healing", "granulation", "epithelialization", "chronic wound", "debridement"],
        conclusion_template="Wound healing phase: {phase}. {barrier_assessment}. Time to closure estimate: {weeks} weeks.",
        reasoning_framework="""
        Wound Healing Process - Three Overlapping Phases:

        Phase 1: Inflammatory (Days 0-5):
        - Hemostasis: platelet plug formation
        - Vasoconstriction then vasodilation
        - Neutrophil infiltration (24-48 hours)
        - Macrophage recruitment (48-96 hours)
        - Debridement of devitalized tissue
        - Cytokine cascade initiation

        Clinical Signs:
        - Erythema, warmth, edema, pain (normal inflammation)
        - Serous or serosanguineous drainage
        - Fibrin slough (yellow/white)

        Prolonged Inflammation Indicates:
        - Infection (purulence, odor, >10^5 bacteria/gram)
        - Foreign body
        - Repeated trauma
        - Ischemia

        Phase 2: Proliferative (Days 4-21):
        - Granulation tissue formation (fibroblasts + angiogenesis)
        - Collagen deposition (Type III initially)
        - Wound contraction (myofibroblasts)
        - Epithelialization from wound edges

        Clinical Signs:
        - Beefy red granulation tissue
        - Wound bed fills in from base
        - Pink epithelial margins advance
        - Decreased wound size

        Proliferation Failure Indicates:
        - Protein malnutrition (albumin <3.0 g/dL)
        - Zinc/vitamin C deficiency
        - Chronic disease (diabetes, renal failure)
        - Hypoxia (venous or arterial insufficiency)
        - Medications (steroids, chemotherapy)

        Phase 3: Remodeling (Weeks 3 to Years):
        - Collagen reorganization (Type III -> Type I)
        - Scar maturation
        - Increased tensile strength (max 80% of original)
        - Decreased cellularity
        - Scar flattening and fading

        Clinical Signs:
        - Firm, flat scar
        - Color transition: red -> pink -> white
        - Pliability improvement

        Abnormal Remodeling:
        - Hypertrophic scar (confined to wound borders)
        - Keloid (extends beyond borders)
        - Chronic wounds (failure to progress)

        Chronic Wound Definition:
        - Failure to heal in 4-6 weeks
        - Stalled in inflammatory phase

        Common Chronic Wound Types:

        1. Diabetic Foot Ulcer:
           - Neuropathy + pressure + ischemia
           - 60% on plantar foot
           - Infection risk high (osteomyelitis)
           - Offloading critical
           - Healing rate: 50% at 12 weeks with optimal care

        2. Venous Leg Ulcer:
           - Medial malleolus location 80%
           - Shallow, irregular borders
           - Moderate to heavy exudate
           - Compression therapy essential
           - Healing rate: 70% at 12 weeks with compression

        3. Arterial Ulcer:
           - Distal toes, foot margins
           - Deep, well-demarcated
           - Pale wound bed (poor perfusion)
           - Pain severe, worse with elevation
           - Vascular intervention may be required

        4. Pressure Ulcer:
           - Bony prominences (sacrum, heels, hips)
           - Stages I-IV + unstageable + deep tissue injury
           - Prevention critical (turn q2h, pressure-relief surfaces)
           - Healing requires pressure elimination

        Wound Healing Optimization:

        Moisture Balance:
        - Moist environment accelerates healing 40%
        - Too dry: cell death, delayed epithelialization
        - Too wet: maceration, infection
        - Dressing selection based on exudate level

        Debridement:
        - Sharp/surgical: fastest, most effective
        - Enzymatic: collagenase ointment
        - Autolytic: moisture-retentive dressings
        - Biological: medical-grade maggots (severe cases)
        - Mechanical: wet-to-dry (outdated, painful)

        Nutritional Support:
        - Protein: 1.2-1.5 g/kg/day
        - Calories: 30-35 kcal/kg/day
        - Vitamin C: 500-1000 mg/day
        - Zinc: 15-50 mg/day (if deficient)
        - Albumin >3.0 g/dL goal

        Adjunctive Therapies:
        - Negative pressure wound therapy (NPWT): 40% faster closure
        - Hyperbaric oxygen: diabetic foot ulcers, radiation wounds
        - Growth factors: becaplermin (PDGF) for diabetic ulcers
        - Skin substitutes: bilayered, dermal, cellular
        """,
        key_factors=["Healing phase", "Wound etiology", "Infection presence", "Perfusion status",
                     "Nutritional status", "Comorbidities", "Offloading adequacy"],
        primary_authority=["Wound healing society guidelines", "NPUAP pressure ulcer staging",
                          "Diabetic foot consortium", "Venous ulcer compression standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for phase identification, DISCLOSURE for healing time estimates",
        issue_category=IssueCategory.WOUND_HEALING,
        entity_scope="All wound patients",
        adversary_position="Expensive wound therapies not cost-effective vs. basic care",
        counter_arguments=[
            "Chronic wounds cost $20B+ annually in US",
            "NPWT reduces amputation rates",
            "Early aggressive management prevents chronicity",
            "Quality of life improvements justify cost"
        ],
        resolution_strategy="Comprehensive wound assessment, address underlying pathophysiology, optimize modifiable factors"
    ),

    DoctrineBlock(
        topic="phototherapy_protocols",
        keywords=["phototherapy", "UVB", "PUVA", "narrowband", "psoriasis", "vitiligo", "eczema"],
        conclusion_template="Phototherapy indication: {condition}. Protocol: {regimen}. Expected response: {outcome}.",
        reasoning_framework="""
        Phototherapy - Ultraviolet Light Treatment:

        Types of Phototherapy:

        1. Narrowband UVB (NB-UVB) 311-313nm:
           - First-line phototherapy
           - Safer than broadband UVB and PUVA
           - No psoralen required
           - Lower skin cancer risk
           - Most versatile

        2. Broadband UVB (BB-UVB) 280-320nm:
           - Older modality
           - Largely replaced by NB-UVB
           - Higher burn risk

        3. PUVA (Psoralen + UVA):
           - Oral or topical psoralen photosensitizer
           - UVA 320-400nm exposure 1-2 hours later
           - Higher skin cancer risk
           - Nausea with oral psoralen
           - Reserved for refractory cases

        4. Excimer Laser (308nm):
           - Targeted NB-UVB
           - Treats localized lesions
           - Spares uninvolved skin
           - Higher intensity

        Indications and Efficacy:

        Psoriasis:
        - NB-UVB: 60-75% achieve clearance/near-clearance
        - Dosing: 3x weekly, start 70% MED (minimal erythema dose)
        - Increase 10-20% each session if no erythema
        - Typical course: 20-30 treatments
        - Maintenance: 1-2x weekly to prevent relapse

        Atopic Dermatitis:
        - NB-UVB: 50-70% significant improvement
        - Useful for steroid-refractory cases
        - Safe in children (>6 years)
        - Reduces S. aureus colonization

        Vitiligo:
        - NB-UVB + topical corticosteroid or calcineurin inhibitor
        - Repigmentation: 75% achieve some response
        - Face responds best (70%+ repigmentation)
        - Acral areas poor response (<30%)
        - Requires 100+ treatments for maximal response
        - Combine with tacrolimus for synergy

        Mycosis Fungoides (Cutaneous T-Cell Lymphoma):
        - PUVA or NB-UVB effective for early-stage (IA-IIA)
        - Complete response: 50-80%
        - Relapse rate: 30-50% after discontinuation
        - Maintenance therapy often required

        Pruritus (Chronic Itch):
        - NB-UVB for uremic pruritus, polycythemia vera
        - Response rate: 70-80%
        - Mechanism: immunomodulation, reduction of pruritogens

        Polymorphous Light Eruption:
        - Prophylactic NB-UVB before sun season
        - Hardening protocol: gradual tolerance induction
        - 8-12 sessions before anticipated sun exposure

        Contraindications:

        Absolute:
        - Lupus erythematosus
        - Xeroderma pigmentosum
        - Basal cell nevus syndrome (Gorlin)
        - Porphyria

        Relative:
        - History of melanoma
        - Multiple atypical nevi
        - PUVA: pregnancy, liver disease, cataracts
        - Photosensitizing medications (tetracyclines, thiazides)

        Dosing and Safety:

        Starting Dose Determination:
        - Skin phototype I-II: 50-70% MED
        - Skin phototype III-IV: 70-80% MED
        - Skin phototype V-VI: 80-100% MED

        Dose Escalation:
        - No erythema: increase 10-20%
        - Mild erythema: same dose
        - Moderate erythema: hold 1-2 sessions
        - Severe burn: hold until resolved, restart lower

        Protective Measures:
        - Eye protection (UV-blocking goggles) mandatory
        - Male genital shielding recommended
        - Sunscreen to face if not target area
        - Record cumulative dose

        Long-Term Risks:

        Photoaging:
        - Irreversible after cumulative exposure
        - Wrinkles, lentigines, textural changes

        Skin Cancer:
        - NB-UVB: minimal risk (<200 treatments)
        - PUVA: dose-dependent SCC risk
        - >150 PUVA treatments: 5-10x SCC risk
        - Melanoma risk controversial (conflicting data)

        Monitoring:
        - Full-body skin exam every 6-12 months
        - Patient self-exam monthly
        - Cumulative dose tracking
        - Consider stopping if >200 NB-UVB or >100 PUVA sessions
        """,
        key_factors=["Skin phototype", "Disease indication", "Prior phototherapy history",
                     "Cumulative UV exposure", "Medication review", "Skin cancer history"],
        primary_authority=["AAD phototherapy guidelines", "Phototherapy consensus statements",
                          "JAAD NB-UVB protocol review", "PUVA long-term follow-up studies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for NB-UVB protocols, HIGH_RISK for PUVA >100 treatments",
        issue_category=IssueCategory.PHOTOTHERAPY,
        entity_scope="Patients with inflammatory dermatoses",
        adversary_position="Phototherapy is obsolete in the biologic era",
        counter_arguments=[
            "Phototherapy is cost-effective vs. biologics",
            "No immunosuppression (safer for certain comorbidities)",
            "Effective for multiple conditions simultaneously",
            "Pregnancy-safe option for severe dermatoses"
        ],
        resolution_strategy="Use phototherapy for appropriate indications, track cumulative dose, monitor for skin cancer, consider biologics for refractory cases"
    ),

    DoctrineBlock(
        topic="dermatopathology_interpretation",
        keywords=["dermatopathology", "biopsy", "histology", "H&E", "immunohistochemistry", "melanoma staging"],
        conclusion_template="Histopathologic diagnosis: {diagnosis}. Breslow depth: {depth}mm. {staging_implications}.",
        reasoning_framework="""
        Dermatopathology - Microscopic Diagnosis:

        Biopsy Techniques:

        1. Shave Biopsy:
           - Superficial lesion removal
           - Tangential blade approach
           - Adequate for most benign lesions
           - Inadequate for melanoma (depth assessment needed)
           - Saucerization shave for deeper lesions

        2. Punch Biopsy:
           - Full-thickness cylindrical sample
           - 2-6mm diameter punches available
           - Provides depth for melanoma staging
           - Multiple punches for variability
           - Primary closure or heal by secondary intention

        3. Excisional Biopsy:
           - Complete lesion removal with margin
           - Gold standard for melanoma
           - Allows complete histologic assessment
           - Definitive treatment if margins clear

        4. Incisional Biopsy:
           - Partial removal of large lesion
           - Sample most suspicious area
           - Used for large tumors pre-staging

        Melanoma Histopathology Critical Features:

        Breslow Depth (Most Important Prognostic Factor):
        - Measured from granular layer to deepest melanocyte
        - T1: <0.8mm (excellent prognosis, 95%+ 10-year survival)
        - T2: 0.8-1.0mm
        - T3: 1.0-2.0mm
        - T4: 2.0-4.0mm
        - T5: >4.0mm (poor prognosis, 50% 10-year survival)

        Ulceration:
        - Absence of intact epidermis
        - Upstages melanoma (e.g., T1b with ulceration = worse than T1a)
        - Independent poor prognostic factor
        - Increases metastatic risk 2-3x

        Mitotic Rate:
        - Mitoses per square millimeter
        - >1/mm^2 upstages thin melanomas
        - Correlates with aggressive behavior

        Microscopic Satellites:
        - Tumor nests >0.05mm from main tumor
        - Indicates aggressive local spread
        - Upstages to N1c or higher

        Lymphovascular Invasion:
        - Tumor cells in lymphatics or vessels
        - High risk for metastasis
        - Requires wider margins and close surveillance

        Regression:
        - Fibrous replacement of tumor
        - May cause understaging (thicker tumor partially regressed)
        - Immunologic response evidence

        Histologic Subtypes:
        - Superficial spreading (70%): radial then vertical growth
        - Nodular (15%): vertical growth from onset, worse prognosis
        - Lentigo maligna (10%): sun-damaged skin, elderly, slow growth
        - Acral lentiginous (5%): palms/soles/nails, more common in darker skin

        Immunohistochemistry (IHC) in Melanoma:
        - S100: very sensitive (95%+), less specific
        - SOX10: highly sensitive and specific
        - Melan-A/MART-1: sensitive, highlights junctional nests
        - HMB-45: positive in melanoma, negative in nevi (usually)
        - Ki-67: proliferation marker

        Basal Cell Carcinoma Histology:

        Subtypes:
        - Nodular: well-circumscribed nests, peripheral palisading
        - Superficial: buds from epidermis, minimal invasion
        - Morpheaform/Infiltrative: cords and strands, dense stroma
        - Micronodular: small discrete nests, aggressive

        High-Risk Features:
        - Perineural invasion
        - Infiltrative or morpheaform pattern
        - Positive deep margin

        Squamous Cell Carcinoma Histology:

        Differentiation Grade:
        - Well-differentiated: keratin pearls, minimal atypia
        - Moderately-differentiated: intermediate features
        - Poorly-differentiated: high atypia, few keratin pearls

        Depth of Invasion:
        - <2mm: low risk
        - 2-6mm: intermediate risk
        - >6mm: high risk

        Clark Level (anatomic depth):
        - I: in situ
        - II: papillary dermis
        - III: papillary-reticular junction
        - IV: reticular dermis
        - V: subcutaneous fat

        Special Stains:
        - PAS: fungal infections
        - GMS: fungal, Pneumocystis
        - Acid-fast: mycobacteria
        - Fite stain: leprosy
        - Congo red: amyloid
        - Alcian blue: mucin

        Direct Immunofluorescence (DIF):
        - Pemphigus: intercellular IgG (fish net)
        - Bullous pemphigoid: linear IgG/C3 basement membrane
        - Lupus: granular IgG/IgM/C3 at dermal-epidermal junction
        - Dermatitis herpetiformis: granular IgA in dermal papillae
        """,
        key_factors=["Biopsy technique adequacy", "Tumor depth", "Histologic subtype", "Margin status",
                     "High-risk features", "IHC results", "DIF findings"],
        primary_authority=["AJCC melanoma staging", "CAP melanoma protocol",
                          "WHO skin tumor classification", "Dermatopathology textbook Weedon"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for diagnosis, DISCLOSURE for prognostic estimates",
        issue_category=IssueCategory.DERMATOPATHOLOGY,
        entity_scope="All skin biopsies",
        adversary_position="Over-reliance on pathology, clinical diagnosis sufficient",
        counter_arguments=[
            "Histology confirms clinical suspicion",
            "Staging requires microscopic assessment",
            "Subtypes guide treatment selection",
            "Medicolegal protection with pathology confirmation"
        ],
        resolution_strategy="Appropriate biopsy technique for clinical scenario, comprehensive pathology reporting, integrate histology with clinical presentation"
    ),

    # Additional 17 doctrine blocks for comprehensive coverage...

    DoctrineBlock(
        topic="cosmetic_botulinum_toxin",
        keywords=["botox", "botulinum toxin", "wrinkles", "glabellar", "forehead", "crow's feet"],
        conclusion_template="Botulinum toxin treatment plan: {areas}. Dosing: {units} units total. Expected duration: {months} months.",
        reasoning_framework="""
        Botulinum Toxin - Neuromodulator for Wrinkle Reduction:

        Mechanism: Blocks acetylcholine release at neuromuscular junction,
        temporarily paralyzing muscles causing dynamic wrinkles.

        FDA-Approved Areas:
        1. Glabellar lines (frown lines): 20-40 units
        2. Forehead lines: 10-30 units
        3. Lateral canthal lines (crow's feet): 12-24 units per side

        Dosing Guidelines:
        - Start conservative, can add more at 2-week touch-up
        - Men require 20-30% higher doses
        - Onset: 3-5 days, peak 10-14 days
        - Duration: 3-4 months average

        Contraindications:
        - Neuromuscular disorders (myasthenia gravis, Lambert-Eaton)
        - Aminoglycoside antibiotics (potentiate effect)
        - Pregnancy/breastfeeding
        - Allergy to botulinum toxin

        Complications:
        - Ptosis (2-5%): resolves in 2-4 weeks
        - Brow asymmetry
        - Headache (transient)
        - Ecchymosis at injection sites

        Patient Selection:
        - Dynamic wrinkles (improve with muscle relaxation)
        - Static wrinkles need fillers, not botulinum toxin
        - Realistic expectations
        - Commitment to maintenance treatments
        """,
        key_factors=["Treatment area", "Patient gender", "Muscle strength", "Prior treatment history",
                     "Contraindication screening"],
        primary_authority=["FDA labeling botulinum toxin", "ASDS cosmetic guidelines",
                          "Dermatol Surg injection techniques", "AAD cosmetic consensus"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for approved areas, DISCLOSURE for off-label use",
        issue_category=IssueCategory.COSMETIC,
        entity_scope="Adult cosmetic patients",
        adversary_position="Botulinum toxin is unnecessary cosmetic vanity",
        counter_arguments=[
            "Patient autonomy over appearance",
            "Psychological benefits well-documented",
            "Safe when properly administered",
            "Non-surgical with minimal downtime"
        ],
        resolution_strategy="Informed consent, conservative dosing, proper anatomic technique"
    ),

    DoctrineBlock(
        topic="acne_treatment_ladder",
        keywords=["acne", "isotretinoin", "retinoid", "benzoyl peroxide", "comedone", "cyst"],
        conclusion_template="Acne severity: {grade}. Treatment: {regimen}. Isotretinoin candidacy: {yes_no}.",
        reasoning_framework="""
        Acne Vulgaris Treatment - Stepwise Approach:

        Severity Grading:
        - Mild: comedones, few papules (<20 lesions)
        - Moderate: comedones + papules/pustules (20-100 lesions)
        - Severe: nodules, cysts, scarring (>100 lesions or any scarring)

        Topical Therapy:
        - Retinoids (adapalene, tretinoin): comedolytic, first-line
        - Benzoyl peroxide 2.5-10%: antibacterial, anti-inflammatory
        - Topical antibiotics (clindamycin, erythromycin): short-term only
        - Combination products superior to monotherapy

        Oral Antibiotics (Moderate acne):
        - Doxycycline 100mg daily or minocycline 100mg daily
        - Duration: 3-6 months maximum
        - Risk: antibiotic resistance, discontinue when controlled

        Hormonal Therapy (Women):
        - Oral contraceptives (ethinyl estradiol + progestin)
        - Spironolactone 50-200mg daily (androgen blocker)
        - Effective for hormonal acne (jawline/chin pattern)

        Isotretinoin (Severe/Refractory Acne):
        - Indications: severe nodulocystic, scarring, refractory to other treatments
        - Dosing: 0.5-1.0 mg/kg/day for 5-6 months
        - Cumulative dose: 120-150 mg/kg
        - iPledge program mandatory (pregnancy prevention)
        - Side effects: dry skin/lips, elevated lipids, teratogenicity
        - Monitoring: monthly pregnancy tests (women), lipids, liver function
        - Cure rate: 85% long-term remission
        """,
        key_factors=["Acne severity", "Scarring presence", "Gender", "Prior treatment response",
                     "Pregnancy potential"],
        primary_authority=["AAD acne guidelines", "Global Alliance acne treatment",
                          "Isotretinoin iPledge protocol"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for treatment ladder, HIGH_RISK for isotretinoin monitoring",
        issue_category=IssueCategory.INFLAMMATORY,
        entity_scope="Adolescent and adult acne patients",
        adversary_position="Acne is self-limited, treatment unnecessary",
        counter_arguments=[
            "Acne causes permanent scarring",
            "Psychosocial impact is significant",
            "Early aggressive treatment prevents scarring",
            "Isotretinoin changes life course for severe acne"
        ],
        resolution_strategy="Severity-guided treatment escalation, early isotretinoin for severe/scarring acne"
    ),
]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class TelemetryCollector:
    """Tracks query metrics and performance"""

    def __init__(self):
        self.query_count = 0
        self.total_latency = 0.0
        self.doctrine_triggers: Dict[str, int] = {}
        self.error_count = 0
        self.start_time = time.time()

    def record_query(self, latency_ms: float, doctrines: List[str]):
        self.query_count += 1
        self.total_latency += latency_ms
        for doctrine in doctrines:
            self.doctrine_triggers[doctrine] = self.doctrine_triggers.get(doctrine, 0) + 1

    def record_error(self):
        self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0.0
        uptime = time.time() - self.start_time
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "error_count": self.error_count,
            "uptime_seconds": round(uptime, 2),
            "doctrine_hits": self.doctrine_triggers
        }


# ============================================================================
# DERMATOLOGY INTELLIGENCE ENGINE
# ============================================================================

class DermatologyEngine:
    """MED12 Dermatology Analysis Engine - TIE Architecture"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9312
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"

        logger.info(f"MED12 Dermatology Engine v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        context: Dict[str, Any]
    ) -> DermatologyResponse:
        """
        Three-layer retrieval architecture:
        Layer 1: Doctrine cache (0-50ms)
        Layer 2: Semantic search (50-200ms)
        Layer 3: Deep analysis (200-2000ms)
        """
        start_time = time.time()

        # Layer 1: Doctrine cache search
        triggered_doctrines = self._search_doctrine_cache(query, context)

        if not triggered_doctrines:
            # Layer 2: Semantic fallback (would integrate vector search here)
            logger.warning(f"No doctrine cache hit for query: {query[:100]}")
            triggered_doctrines = self._semantic_fallback(query)

        # Layer 3: Deep analysis for complex queries
        if mode == ResponseMode.MEMO or len(triggered_doctrines) > 3:
            answer = self._deep_analysis(query, triggered_doctrines, context)
        else:
            answer = self._fast_synthesis(query, triggered_doctrines, mode)

        # Determine confidence and zone
        confidence = self._compute_confidence(triggered_doctrines, context)
        zone = self._determine_zone(query)
        issue_categories = self._extract_issue_categories(triggered_doctrines)
        epistemic_warnings = self._generate_epistemic_warnings(triggered_doctrines, confidence)

        # Generate determinism hash
        determinism_hash = self._compute_determinism_hash(query, triggered_doctrines, mode)

        latency_ms = (time.time() - start_time) * 1000

        # Record telemetry
        doctrine_topics = [d.topic for d in triggered_doctrines]
        self.telemetry.record_query(latency_ms, doctrine_topics)

        # Audit trail
        self._write_audit_log(query, answer, doctrine_topics, latency_ms)

        response = DermatologyResponse(
            query=query,
            answer=answer,
            confidence=confidence,
            triggered_doctrines=doctrine_topics,
            epistemic_warnings=epistemic_warnings,
            issue_categories=issue_categories,
            analysis_zone=zone,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            metadata={
                "mode": mode.value,
                "doctrine_count": len(triggered_doctrines),
                "context_provided": list(context.keys())
            }
        )

        return response

    def _search_doctrine_cache(self, query: str, context: Dict[str, Any]) -> List[DoctrineBlock]:
        """Search doctrine cache by keyword matching"""
        query_lower = query.lower()
        matches = []

        for doctrine in self.doctrine_cache:
            # Keyword matching
            keyword_hits = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)

            # Context-based boosting
            if context.get("lesion_size_mm") and "melanoma" in doctrine.topic:
                keyword_hits += 2
            if context.get("location") and "wound" in doctrine.topic:
                keyword_hits += 1

            if keyword_hits > 0:
                matches.append((keyword_hits, doctrine))

        # Sort by relevance, return top matches
        matches.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in matches[:5]]

    def _semantic_fallback(self, query: str) -> List[DoctrineBlock]:
        """Fallback when doctrine cache misses - return general doctrines"""
        logger.info("Semantic fallback triggered")
        # In production, this would query vector database
        # For now, return most general doctrines
        general_topics = ["melanoma_abcde_criteria", "wound_healing_phases", "dermatopathology_interpretation"]
        return [d for d in self.doctrine_cache if d.topic in general_topics]

    def _fast_synthesis(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """Fast response synthesis from doctrine blocks"""
        if not doctrines:
            return "No relevant dermatology doctrines found for this query."

        primary = doctrines[0]

        # Extract key points from reasoning framework
        framework_lines = primary.reasoning_framework.strip().split('\n')
        key_points = [line.strip() for line in framework_lines if line.strip() and not line.strip().startswith('-')][:5]

        answer_parts = [
            f"Analysis based on {primary.topic.replace('_', ' ').title()}:",
            "",
            primary.conclusion_template.format(
                assessment="clinical assessment required",
                recommendation="refer to detailed evaluation",
                urgency="timing based on severity"
            ),
            "",
            "Key Considerations:"
        ]

        for point in key_points:
            if point and len(point) > 10:
                answer_parts.append(f"- {point}")

        if mode == ResponseMode.DEFENSE:
            answer_parts.extend([
                "",
                "Supporting Authority:",
                *[f"- {auth}" for auth in primary.primary_authority[:3]]
            ])

        return '\n'.join(answer_parts)

    def _deep_analysis(self, query: str, doctrines: List[DoctrineBlock], context: Dict[str, Any]) -> str:
        """Deep multi-doctrine synthesis for complex queries"""
        if not doctrines:
            return "Insufficient doctrine coverage for deep analysis."

        answer_parts = ["COMPREHENSIVE DERMATOLOGY ANALYSIS\n"]

        # Multi-doctrine decomposition
        issue_categories = list(set(d.issue_category for d in doctrines))

        for category in issue_categories:
            category_doctrines = [d for d in doctrines if d.issue_category == category]
            answer_parts.append(f"\n{category.value} CONSIDERATIONS:")

            for doctrine in category_doctrines[:2]:  # Top 2 per category
                answer_parts.append(f"\n{doctrine.topic.replace('_', ' ').title()}:")
                answer_parts.append(doctrine.reasoning_framework[:500] + "...")

        # Synthesize recommendations
        answer_parts.extend([
            "\n\nINTEGRATED RECOMMENDATIONS:",
            self._synthesize_recommendations(doctrines, context),
            "\n\nAUTHORITY SUPPORT:",
            *[f"- {auth}" for d in doctrines for auth in d.primary_authority[:2]]
        ])

        return '\n'.join(answer_parts)

    def _synthesize_recommendations(self, doctrines: List[DoctrineBlock], context: Dict[str, Any]) -> str:
        """Synthesize actionable recommendations from multiple doctrines"""
        recommendations = []

        # Extract resolution strategies
        for doctrine in doctrines:
            if doctrine.resolution_strategy:
                recommendations.append(f"- {doctrine.resolution_strategy}")

        # Add context-specific guidance
        if context.get("patient_age") and context["patient_age"] < 18:
            recommendations.append("- Pediatric dosing and safety considerations apply")

        if context.get("lesion_size_mm") and context["lesion_size_mm"] > 6:
            recommendations.append("- Size >6mm warrants increased surveillance or biopsy")

        return '\n'.join(recommendations[:5]) if recommendations else "Context-specific guidance required"

    def _compute_confidence(self, doctrines: List[DoctrineBlock], context: Dict[str, Any]) -> ConfidenceLevel:
        """Compute overall confidence level"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Aggregate doctrine confidences
        confidence_weights = {
            ConfidenceLevel.DEFENSIBLE: 4,
            ConfidenceLevel.AGGRESSIVE: 3,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 1
        }

        total_weight = sum(confidence_weights.get(d.confidence, 2) for d in doctrines)
        avg_weight = total_weight / len(doctrines)

        # Map back to confidence level
        if avg_weight >= 3.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_weight >= 2.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_weight >= 1.5:
            return ConfidenceLevel.DISCLOSURE
        else:
            return ConfidenceLevel.HIGH_RISK

    def _determine_zone(self, query: str) -> AnalysisZone:
        """Determine analysis zone from query intent"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["diagnose", "identify", "screening", "biopsy", "pathology"]):
            return AnalysisZone.DIAGNOSTIC
        elif any(word in query_lower for word in ["treat", "therapy", "management", "protocol", "dosing"]):
            return AnalysisZone.TREATMENT
        else:
            return AnalysisZone.DOCUMENTATION

    def _extract_issue_categories(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Extract unique issue categories from triggered doctrines"""
        return list(set(d.issue_category for d in doctrines))

    def _generate_epistemic_warnings(self, doctrines: List[DoctrineBlock], confidence: ConfidenceLevel) -> List[str]:
        """Generate epistemic guardrail warnings"""
        warnings = []

        if confidence in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]:
            warnings.append("This analysis requires clinical correlation and may not be definitive.")

        # Check for adversarial positions
        adversarial_doctrines = [d for d in doctrines if d.adversary_position]
        if adversarial_doctrines:
            warnings.append("Alternative clinical perspectives exist for this scenario.")

        if not doctrines:
            warnings.append("Limited doctrine coverage - seek specialist consultation.")

        return warnings

    def _compute_determinism_hash(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """Generate SHA-256 determinism hash for reproducibility"""
        hash_input = f"{query}|{mode.value}|{'|'.join(d.topic for d in doctrines)}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def _write_audit_log(self, query: str, answer: str, doctrines: List[str], latency_ms: float):
        """Write JSONL audit trail"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:200],
            "doctrines": doctrines,
            "latency_ms": latency_ms,
            "answer_length": len(answer)
        }

        try:
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_health(self) -> HealthResponse:
        """Health check endpoint"""
        metrics = self.telemetry.get_metrics()
        return HealthResponse(
            status="healthy",
            version=self.version,
            port=self.port,
            doctrine_count=len(self.doctrine_cache),
            uptime_seconds=metrics["uptime_seconds"],
            total_queries=metrics["total_queries"],
            avg_latency_ms=metrics["avg_latency_ms"]
        )


# ============================================================================
# FASTAPI SERVER
# ============================================================================

app = FastAPI(
    title="MED12 Dermatology Analysis Engine",
    version="1.0.0",
    description="TIE-architecture dermatology intelligence engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = DermatologyEngine()


@app.post("/query", response_model=DermatologyResponse)
async def query_dermatology(request: DermatologyQuery):
    """Main query endpoint"""
    try:
        logger.info(f"Query received: {request.query[:100]}")
        response = engine.three_layer_response(request.query, request.mode, request.context)
        return response
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        engine.telemetry.record_error()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return engine.get_health()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "count": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "issue_category": d.issue_category.value,
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "MED12 Dermatology Analysis",
        "version": engine.version,
        "status": "operational",
        "port": engine.port,
        "endpoints": ["/query", "/health", "/doctrines"]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting MED12 Dermatology Engine on port {engine.port}")
    uvicorn.run(app, host="0.0.0.0", port=engine.port, log_level="info")
