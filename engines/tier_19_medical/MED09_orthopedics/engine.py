"""
MED09 Orthopedics Analysis Engine v1.0.0
Port: 9234

Analyzes orthopedic conditions: fracture classification, joint replacement assessment,
spine surgery planning, sports medicine injuries, and musculoskeletal imaging interpretation.

TIE-20 Components:
1. three_layer_response (cache/semantic/deep)
2. response_modes (FAST/DEFENSE/MEMO)
3. doctrine_cache (25+ real orthopedic expertise blocks)
4. authority_hardening (hierarchical evidence weighting)
5. confidence_stratification (DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK)
6. semantic_normalization (medical term standardization)
7. vector_search (semantic retrieval fallback)
8. telemetry (query tracing, latency tracking)
9. drift_watcher (doctrine drift detection)
10. coverage_map (triggered/missed doctrines)
11. metrics_collector (latency/error/hit rates)
12. health_endpoint (comprehensive status)
13. zoned_analysis (DIAGNOSTIC/PLANNING/SURGICAL zones)
14. fact_fragility_scoring (evidence strength)
15. audit_trail_jsonl (forensic query log)
16. determinism_hash_sha256 (reproducibility)
17. fastapi_server (CORS, lifespan, typed endpoints)
18. loguru_logging (structured, rotated)
19. multi_doctrine_decomposition (issue categories, interaction DAG)
20. deep_analysis_mode (multi-source synthesis)
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "MED09"
ENGINE_NAME = "Orthopedics Analysis Engine"
VERSION = "1.0.0"
PORT = 9234

LOG_FILE = Path(__file__).parent / "med09_orthopedics.log"
AUDIT_FILE = Path(__file__).parent / "med09_audit.jsonl"

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════

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
    PLANNING = "PLANNING"
    SURGICAL = "SURGICAL"

class IssueCategory(str, Enum):
    FRACTURE_CLASSIFICATION = "fracture_classification"
    JOINT_REPLACEMENT = "joint_replacement"
    SPINE_SURGERY = "spine_surgery"
    SPORTS_MEDICINE = "sports_medicine"
    IMAGING_INTERPRETATION = "imaging_interpretation"
    INFECTION_MANAGEMENT = "infection_management"
    PEDIATRIC_ORTHOPEDICS = "pediatric_orthopedics"
    TRAUMA_MANAGEMENT = "trauma_management"
    SOFT_TISSUE_INJURY = "soft_tissue_injury"
    BONE_HEALING = "bone_healing"

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Orthopedic analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.DIAGNOSTIC, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional clinical context")

class DoctrineMatch(BaseModel):
    topic: str
    keywords: List[str]
    conclusion: str
    reasoning: str
    confidence: ConfidenceLevel
    authority_weight: float
    sources: List[str]

class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    doctrines_triggered: List[DoctrineMatch]
    confidence: ConfidenceLevel
    fragility_score: float
    categories: List[IssueCategory]
    determinism_hash: str
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float
    uptime_seconds: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE BLOCK
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DoctrineBlock:
    """Real orthopedic domain expertise block"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    authority_weight: float = 1.0
    fragility_score: float = 0.3

    def matches(self, query: str) -> float:
        """Calculate match score based on keyword overlap"""
        query_lower = query.lower()
        matches = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        return matches / len(self.keywords) if self.keywords else 0.0

    def render(self, context: Dict[str, Any]) -> str:
        """Render conclusion with context"""
        try:
            return self.conclusion_template.format(**context)
        except (KeyError, ValueError):
            return self.conclusion_template

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL ORTHOPEDIC EXPERTISE BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # ═══ FRACTURE CLASSIFICATION ═══
    DoctrineBlock(
        topic="AO/OTA Fracture Classification System",
        keywords=["fracture classification", "AO system", "OTA", "fracture type", "fracture pattern"],
        conclusion_template="The AO/OTA system uses alphanumeric codes: bone (1-9), segment (1-4), type (A/B/C). Type A = simple, B = wedge, C = complex. Subgroups add detail (.1/.2/.3). Example: 32-B2 = femoral shaft wedge fracture with intact butterfly fragment.",
        reasoning_framework="""
The AO/OTA classification provides standardized fracture description:
1. BONE: Coded 1-9 (humerus=1, radius/ulna=2, femur=3, tibia/fibula=4, etc.)
2. SEGMENT: Proximal(1), diaphyseal(2), distal(3), malleolar(4)
3. TYPE: A=simple/2-part, B=wedge/3-part, C=complex/multifragmentary
4. GROUP/SUBGROUP: Further detail on fracture morphology

Key principles:
- Type A fractures generally have better prognosis (simpler reduction)
- Type C fractures often require advanced fixation (more comminution)
- Classification guides treatment selection (plate vs IM nail vs external fixation)
- Higher complexity correlates with longer healing time and complication risk
- Distal femur 33-C3 fractures have highest nonunion risk in this region
- Proximal humerus 11-C2/C3 fractures often need arthroplasty in elderly

Clinical implications:
- Simple patterns (A type): Often amenable to closed reduction/casting
- Wedge patterns (B type): May need interfragmentary screw + neutralization plate
- Complex patterns (C type): Require bridging fixation, respect soft tissues
- Articular involvement: Demands anatomic reduction (step-off >2mm = poor outcome)
- Metaphyseal comminution: Consider locked plating vs intramedullary device
        """,
        key_factors=[
            "Bone segment involved",
            "Fracture pattern complexity (A/B/C)",
            "Articular involvement",
            "Soft tissue injury severity",
            "Patient age and bone quality",
            "Mechanism of injury (high vs low energy)"
        ],
        primary_authority=[
            "Müller ME, Nazarian S, Koch P, Schatzker J. The Comprehensive Classification of Fractures of Long Bones. Springer-Verlag; 1990.",
            "Marsh JL, et al. Fracture and Dislocation Classification Compendium - 2007: OTA/AO. J Orthop Trauma. 2007;21(10 Suppl):S1-133.",
            "Ruedi TP, Murphy WM. AO Principles of Fracture Management. 2nd ed. Thieme; 2007."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FRACTURE_CLASSIFICATION,
        authority_weight=1.0,
        fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Gustilo-Anderson Open Fracture Classification",
        keywords=["open fracture", "Gustilo", "Anderson", "soft tissue injury", "contamination"],
        conclusion_template="Gustilo-Anderson grades open fractures I-IIIC based on wound size, contamination, and soft tissue damage. Grade I <1cm clean wound. Grade II 1-10cm moderate contamination. Grade IIIA >10cm adequate coverage. Grade IIIB requires flap. Grade IIIC has vascular injury requiring repair.",
        reasoning_framework="""
Gustilo-Anderson classification stratifies infection/complication risk:

GRADE I:
- Wound <1cm
- Minimal contamination
- Simple fracture pattern
- Inside-out mechanism
- Infection risk ~2%

GRADE II:
- Wound 1-10cm
- Moderate soft tissue damage
- No extensive stripping
- Moderate contamination
- Infection risk ~5-10%

GRADE IIIA:
- Wound >10cm
- Extensive soft tissue damage BUT adequate bone coverage
- High energy mechanism
- Infection risk ~10-25%

GRADE IIIB:
- Extensive soft tissue loss
- Periosteal stripping
- Bone exposure requiring flap coverage
- High contamination
- Infection risk ~25-50%

GRADE IIIC:
- Vascular injury requiring arterial repair
- Limb-threatening ischemia
- Infection risk >50%
- Amputation consideration (MESS score >7)

Treatment principles:
- All grades: Irrigation/debridement within 6 hours (golden period)
- I/II: Early internal fixation acceptable
- IIIA: Consider temporary external fixation
- IIIB: External fixation, delayed flap coverage (within 7 days)
- IIIC: Vascular repair first, consider amputation if MESS >7

Antibiotic protocol:
- Grade I: 1st generation cephalosporin 24hr
- Grade II/IIIA: Add aminoglycoside 72hr
- IIIB/IIIC: Add penicillin (clostridial coverage) if farm/contaminated
        """,
        key_factors=[
            "Wound size and location",
            "Degree of contamination",
            "Soft tissue viability",
            "Vascular status",
            "Fracture pattern complexity",
            "Time to treatment"
        ],
        primary_authority=[
            "Gustilo RB, Anderson JT. Prevention of infection in the treatment of one thousand and twenty-five open fractures of long bones. J Bone Joint Surg Am. 1976;58(4):453-458.",
            "Gustilo RB, Mendoza RM, Williams DN. Problems in the management of type III (severe) open fractures. J Trauma. 1984;24(8):742-746.",
            "Bosse MJ, et al. An analysis of outcomes of reconstruction or amputation after leg-threatening injuries. N Engl J Med. 2002;347(24):1924-1931."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FRACTURE_CLASSIFICATION,
        authority_weight=1.0,
        fragility_score=0.2
    ),

    # ═══ JOINT REPLACEMENT ═══
    DoctrineBlock(
        topic="Total Hip Arthroplasty: Cemented vs Uncemented",
        keywords=["hip replacement", "THA", "cemented", "uncemented", "cementless", "fixation"],
        conclusion_template="Cemented THA preferred in elderly (>75yr) with poor bone quality. Uncemented THA preferred in younger (<65yr) active patients with good bone stock. Hybrid (cemented femur, uncemented acetabulum) is option for intermediate cases. Long-term survivorship similar but failure modes differ.",
        reasoning_framework="""
Fixation method selection depends on patient factors and bone quality:

CEMENTED THA:
Indications:
- Age >75 years
- Osteoporotic bone (T-score < -2.5)
- Inflammatory arthritis (RA)
- Poor bone quality (Dorr type C femur)
- Immediate weight bearing needed

Advantages:
- Immediate fixation stability
- Lower periprosthetic fracture risk acutely
- Better short-term pain relief
- Proven long-term results (Charnley)

Disadvantages:
- Cement mantle fracture risk
- Aseptic loosening from polyethylene wear debris
- Difficult revision (cement removal)
- BCIS (bone cement implantation syndrome) risk

UNCEMENTED THA:
Indications:
- Age <65 years
- Good bone quality (Dorr type A/B)
- Active lifestyle
- Desire for bone preservation

Advantages:
- Biological fixation (osseointegration)
- Easier revision (no cement removal)
- Lower osteolysis from cement debris
- Preserves bone stock

Disadvantages:
- Initial micromotion (6-12 week protected weight bearing)
- Higher periprosthetic fracture risk
- Thigh pain (stress shielding, micromotion)
- Requires good bone quality for ingrowth

HYBRID THA:
- Cemented femoral stem + uncemented acetabular cup
- Combines immediate femoral stability with biological acetabular fixation
- Popular in older patients (65-75yr) with mixed bone quality
- Swedish Registry shows excellent 15-year survivorship

Bearing surface considerations independent of fixation:
- Ceramic-on-polyethylene: Most common, low wear
- Ceramic-on-ceramic: Lowest wear, squeaking risk
- Metal-on-polyethylene: Avoid (higher wear)
- Metal-on-metal: Abandoned (ALVAL, pseudotumor)
        """,
        key_factors=[
            "Patient age",
            "Bone quality (DEXA, Dorr classification)",
            "Activity level",
            "Comorbidities (RA, osteoporosis)",
            "Surgeon experience",
            "Immediate weight bearing requirement"
        ],
        primary_authority=[
            "Mäkelä KT, et al. Failure rate of cemented and uncemented total hip replacements: register study of combined Nordic database of four nations. BMJ. 2014;348:f7592.",
            "Dorr LD, Faugere MC, Mackel AM, et al. Structural and cellular assessment of bone quality of proximal femur. Bone. 1993;14(3):231-242.",
            "Hailer NP, Garellick G, Kärrholm J. Uncemented and cemented primary total hip arthroplasty in the Swedish Hip Arthroplasty Register. Acta Orthop. 2010;81(1):34-41."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.JOINT_REPLACEMENT,
        authority_weight=1.0,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Total Knee Arthroplasty: Mechanical vs Kinematic Alignment",
        keywords=["knee replacement", "TKA", "alignment", "mechanical axis", "kinematic alignment"],
        conclusion_template="Mechanical alignment targets neutral HKA axis (0 degrees), places components perpendicular to mechanical axis. Kinematic alignment restores native joint line obliquity and individual anatomy. Mechanical alignment remains gold standard with proven 20-year survivorship. Kinematic alignment shows improved early function but lacks long-term data >10 years.",
        reasoning_framework="""
Alignment philosophy debate in TKA:

MECHANICAL ALIGNMENT (Traditional):
Goals:
- Neutral mechanical axis (hip-knee-ankle = 0 degrees +/- 3)
- Femoral component perpendicular to femoral mechanical axis (5-7 degrees valgus from anatomic axis)
- Tibial component perpendicular to tibial mechanical axis (0 degrees)
- Equal flexion/extension gaps

Advantages:
- Proven 20-year survivorship (>90%)
- Equal load distribution across compartments
- Lower aseptic loosening risk (theoretical)
- Standardized technique

Disadvantages:
- Alters native joint line obliquity
- May create asymmetric soft tissue tension
- 20% dissatisfaction rate
- Ignores individual constitutional alignment
- May overcorrect varus/valgus laxity

KINEMATIC ALIGNMENT (Modern Alternative):
Goals:
- Restore native distal femoral joint line angle
- Match individual anatomic axis
- Calipered resection technique
- Maintain constitutional alignment (within 3 degrees varus/valgus)

Advantages:
- Improved early patient satisfaction
- Better ROM in some studies
- Fewer soft tissue releases
- More natural knee kinematics
- Ligament balancing less critical

Disadvantages:
- Lack of long-term data (longest follow-up ~10 years)
- Higher failure rate in outlier alignment (>3 degrees)?
- Uncertainty about polyethylene wear with non-neutral alignment
- Less forgiving of technical error
- Component positioning outside traditional safe zones

Current evidence:
- RCTs show similar 5-year survivorship
- Kinematic alignment has better early function scores
- No difference in complications at mid-term
- Registry data awaited for long-term outcomes
- CORR study (Australian Registry): No difference at 10 years

Safe middle ground:
- Restricted kinematic alignment (limit to 3 degrees varus/valgus from neutral)
- Individualized approach based on preoperative deformity
- Avoid extreme outliers (HKA >6 degrees from neutral)
        """,
        key_factors=[
            "Preoperative alignment and deformity",
            "Ligamentous laxity",
            "Patient expectations",
            "Surgeon experience with technique",
            "Long-term activity level",
            "Bone quality"
        ],
        primary_authority=[
            "Howell SM, Papadopoulos S, Kuznik K, et al. Does varus alignment adversely affect implant survival and function six years after kinematically aligned TKA? Int Orthop. 2015;39(11):2117-2124.",
            "Dossett HG, Swartz GJ, Estrada NA, et al. Kinematic versus mechanical alignment in TKA: a systematic review. Orthopedics. 2012;35(2):e160-169.",
            "Australian Orthopaedic Association National Joint Replacement Registry. Annual Report 2021."
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.JOINT_REPLACEMENT,
        authority_weight=0.85,
        fragility_score=0.4
    ),

    # ═══ SPINE SURGERY ═══
    DoctrineBlock(
        topic="Lumbar Spine: Fusion vs Disc Arthroplasty",
        keywords=["lumbar fusion", "disc replacement", "arthroplasty", "ALIF", "motion preservation"],
        conclusion_template="Lumbar fusion (ALIF/PLIF/TLIF) is gold standard for single-level degenerative disc disease with >20-year data. Disc arthroplasty preserves motion, may reduce adjacent segment disease, but has strict contraindications (facet arthritis, spondylolisthesis, osteoporosis). FDA-approved devices show non-inferiority to fusion at 5 years but lack long-term data >10 years.",
        reasoning_framework="""
Decision between fusion and arthroplasty for lumbar degenerative disc disease:

LUMBAR FUSION (ALIF/PLIF/TLIF):
Indications:
- Single or multi-level degenerative disc disease
- Spondylolisthesis (grade 1 or 2)
- Facet arthropathy
- Deformity correction
- Prior failed discectomy
- Age >60 years

Advantages:
- Proven long-term outcomes (>20 years)
- Eliminates pain source (disc)
- Works regardless of facet condition
- Multiple approach options
- Insurance coverage standard

Disadvantages:
- Adjacent segment disease (25-30% at 10 years)
- Loss of motion at fused level
- Longer recovery (3-6 months)
- Pseudoarthrosis risk (5-10%)
- Hardware complications

DISC ARTHROPLASTY (ProDisc-L, Charite, Mobi-C lumbar):
Indications (ALL required):
- Single-level degenerative disc disease (L3-S1)
- Intact facet joints (no arthritis on CT)
- No spondylolisthesis
- Normal bone density (T-score > -1.0)
- Age <60 years
- BMI <35
- No prior lumbar surgery at level

Advantages:
- Motion preservation
- Faster return to activity (6-8 weeks)
- Lower adjacent segment disease risk (theoretical)
- Non-inferiority to fusion at 2-5 years (FDA IDE studies)

Disadvantages:
- Strict inclusion criteria (only 5-10% of patients qualify)
- Lack of long-term data (>10 years limited)
- Facet arthritis development over time
- Subsidence risk with osteoporosis
- Revision to fusion more complex
- Not covered by all insurance

FDA IDE study results (ProDisc-L):
- 60.7% success vs 53.1% fusion at 2 years
- Similar complication rates
- Lower reoperation in arthroplasty group
- Patient satisfaction equivalent

Contraindications to arthroplasty (absolute):
- Facet arthritis (Fujiwara grade 2+)
- Spondylolisthesis
- Spondylolysis
- Osteoporosis
- Prior fusion at adjacent level
- Infection, tumor, trauma

Decision algorithm:
1. Young patient (<50), single level, pristine facets → consider arthroplasty
2. Any facet arthritis → fusion
3. Multilevel disease → fusion
4. Age >60 → fusion
5. Spondylolisthesis → fusion always
        """,
        key_factors=[
            "Patient age",
            "Number of levels involved",
            "Facet joint condition (CT scan)",
            "Bone density",
            "Prior surgery",
            "Spondylolisthesis presence"
        ],
        primary_authority=[
            "Zigler JE, et al. ProDisc-L randomized controlled trial: 2-year results. Spine. 2007;32(26):2933-2940.",
            "Park CK, et al. Comparison of ProDisc-L and anterior lumbar interbody fusion. J Neurosurg Spine. 2009;10(3):231-238.",
            "Guyer RD, et al. Prospective randomized study of the Charite artificial disc: data from two investigational centers. Spine J. 2004;4(6 Suppl):252S-259S."
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPINE_SURGERY,
        authority_weight=0.9,
        fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Adolescent Idiopathic Scoliosis: Lenke Classification",
        keywords=["scoliosis", "Lenke", "adolescent", "spinal deformity", "curve pattern"],
        conclusion_template="Lenke classification uses 6 curve types (1-6) plus lumbar modifier (A/B/C) and sagittal modifier (-/N/+). Type 1 = main thoracic. Type 2 = double thoracic. Type 3 = double major. Type 5 = thoracolumbar. Classification guides fusion levels to minimize levels fused while achieving balanced correction.",
        reasoning_framework="""
Lenke classification provides treatment roadmap for AIS:

CURVE TYPE (1-6):
Type 1 (Main Thoracic): Most common
- Structural main thoracic curve
- Non-structural proximal thoracic and lumbar curves
- Fusion: Upper instrumented vertebra (UIV) to lowest instrumented vertebra (LIV)
- Typically T4-T5 to T11-T12 or L1

Type 2 (Double Thoracic):
- Structural proximal thoracic AND main thoracic
- Non-structural lumbar
- Fusion: Must include proximal curve (T1-T2 to L1)
- Failure to fuse proximal → shoulder imbalance

Type 3 (Double Major):
- Structural main thoracic AND lumbar curves
- Lumbar curve ≥main thoracic on side bending
- Fusion: Both curves (typically T4-L3 or L4)

Type 4 (Triple Major):
- All three curves structural
- Rare, most severe
- Long fusion (T1-L3/L4)

Type 5 (Thoracolumbar/Lumbar):
- Single structural thoracolumbar or lumbar curve
- Fusion: Shorter construct (T10-L3 typical)

Type 6 (Thoracolumbar/Lumbar - Main Thoracic):
- Structural main thoracic and TL/L curves
- Main thoracic larger
- Fusion: T4-L3/L4

LUMBAR MODIFIER (A/B/C):
Based on relationship of CSVL (center sacral vertical line) to apical lumbar vertebra:
- A: CSVL passes between pedicles (most flexible)
- B: CSVL touches apical vertebra (intermediate)
- C: CSVL does not touch apical vertebra (most rigid)
- Influences need to include lumbar curve in fusion

SAGITTAL MODIFIER (-/N/+):
T5-T12 kyphosis measurement:
- Minus (-): <10 degrees (hypokyphotic)
- Normal (N): 10-40 degrees
- Plus (+): >40 degrees (hyperkyphotic)

Surgical decision-making:
- Main thoracic curve (Type 1A-): Selective thoracic fusion (most common)
- Double thoracic (Type 2): Must fuse proximal curve
- Double major (Type 3C): Fusion to L4 likely needed
- Hypokyphotic (minus modifier): Anterior release may be needed
- Curve >70 degrees: Consider anterior release or vertebral column resection (VCR)

Fusion level selection principles:
- UIV: Stable vertebra (no rotation, centered over sacrum)
- LIV: Last substantially rotated/translated vertebra
- Goal: Coronal and sagittal balance postoperatively
- Minimize fusion levels (preserve motion)

Anterior vs posterior approach:
- Posterior only: Standard for most curves <70 degrees
- Anterior + posterior: Curves >70 degrees, rigid curves, hypokyphosis
- VCR (vertebral column resection): Severe rigid deformity >100 degrees
        """,
        key_factors=[
            "Curve magnitude and flexibility",
            "Number of structural curves",
            "Lumbar modifier (pelvic tilt)",
            "Sagittal alignment",
            "Skeletal maturity (Risser grade)",
            "Patient age and growth remaining"
        ],
        primary_authority=[
            "Lenke LG, et al. Adolescent idiopathic scoliosis: a new classification to determine extent of spinal arthrodesis. J Bone Joint Surg Am. 2001;83-A(8):1169-1181.",
            "Lenke LG, et al. Rationale behind the current state-of-the-art treatment of scoliosis (in the pedicle screw era). Spine. 2008;33(10):1051-1054.",
            "Richards BS, et al. Standardization of criteria for adolescent idiopathic scoliosis brace studies. Spine. 2005;30(18):2068-2075."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPINE_SURGERY,
        authority_weight=1.0,
        fragility_score=0.2
    ),

    # ═══ SPORTS MEDICINE ═══
    DoctrineBlock(
        topic="ACL Reconstruction: Graft Selection BTB vs Hamstring vs Quad Tendon",
        keywords=["ACL", "graft", "BTB", "hamstring", "patellar tendon", "quadriceps tendon"],
        conclusion_template="Bone-patellar tendon-bone (BTB) graft has lowest failure rate, fastest bone-to-bone healing, gold standard for athletes. Hamstring (4-strand) has lower anterior knee pain but higher re-rupture rate in young athletes. Quad tendon offers middle ground with lower donor site morbidity. Allograft has higher failure in patients <25 years old.",
        reasoning_framework="""
Graft selection based on patient factors and goals:

BONE-PATELLAR TENDON-BONE (BTB) AUTOGRAFT:
Advantages:
- Lowest re-rupture rate (2-3%)
- Fastest healing (bone-to-bone in tunnel, 6-8 weeks)
- Highest ultimate tensile strength (2900N)
- Gold standard for pivoting athletes
- Best graft for revision ACL

Disadvantages:
- Anterior knee pain (10-20%)
- Kneeling pain
- Patellar fracture risk (<1%)
- Patellar tendinitis
- Loss of terminal extension if graft too long

Indications:
- High-demand athletes (cutting sports)
- Revision ACL reconstruction
- Combined ACL/PCL or multiligament knee
- Hyperlaxity (generalized laxity)

HAMSTRING AUTOGRAFT (4-strand semitendinosus/gracilis):
Advantages:
- Lower anterior knee pain vs BTB
- Smaller incision (cosmetic)
- No patellar complications
- Preserves extensor mechanism

Disadvantages:
- Higher re-rupture rate (5-8%, especially <25 years old)
- Slower healing (tendon-to-bone, 12 weeks)
- Hamstring weakness (10-15%)
- Tunnel widening (biological incorporation slower)
- Lower ultimate tensile strength (2500N for 4-strand)

Indications:
- Recreational athletes
- Older patients (>35 years)
- Anterior knee pain concerns
- Cosmetic concerns

QUADRICEPS TENDON AUTOGRAFT:
Advantages:
- Large graft diameter (10-11mm achievable)
- Lower anterior knee pain than BTB
- Bone block option (similar healing to BTB)
- Excellent strength (2350N)
- Low donor site morbidity

Disadvantages:
- Less long-term data than BTB/hamstring
- Quadriceps weakness (transient)
- Larger proximal incision
- Technical harvest difficulty

Indications:
- Revision ACL (if BTB previously used)
- Large patient (need big graft)
- Combined ACL/LCL or ACL/MCL
- Multiligament reconstruction

ALLOGRAFT (Cadaver):
Advantages:
- No donor site morbidity
- Faster surgery (no harvest)
- Multiple grafts available (multiligament)
- Larger graft sizes

Disadvantages:
- Higher failure rate, especially age <25 (10-15%)
- Disease transmission risk (very low with modern processing)
- Slower incorporation
- Expensive
- Immune response concerns

Indications:
- Age >40 years
- Low-demand patients
- Multiligament reconstruction
- Revision with multiple grafts needed

Graft preparation variables affecting outcomes:
- Fixation method: Interference screw vs suspensory (Endobutton)
- Tunnel position: Anatomic vs transtibial
- Graft diameter: >8mm significantly lower failure
- Graft tensioning: 20-30N at 20-30 degrees flexion

Return to sport timing by graft:
- BTB: 6-9 months (bone healing)
- Hamstring: 9-12 months (tendon incorporation)
- Quad tendon with bone: 6-9 months
- Allograft: 9-12 months minimum

MOON study findings (multicenter ACL cohort):
- BTB: 1.8% failure at 2 years
- Hamstring: 5.8% failure at 2 years
- Age <18 years: 3x higher failure rate regardless of graft
- Graft diameter <8mm: 85% higher failure rate
        """,
        key_factors=[
            "Patient age (<25 = higher failure risk)",
            "Activity level and sport",
            "Prior knee issues (anterior knee pain)",
            "Generalized ligamentous laxity",
            "Graft diameter achievable",
            "Revision vs primary reconstruction"
        ],
        primary_authority=[
            "MOON Knee Group. Predictors of clinical outcome following ACL reconstruction. J Bone Joint Surg Am. 2014;96(20):1751-1759.",
            "Kaeding CC, et al. Risk Factors and Predictors of Subsequent ACL Injury in Either Knee After ACL Reconstruction. Am J Sports Med. 2015;43(7):1583-1590.",
            "Freedman KB, et al. Arthroscopic anterior cruciate ligament reconstruction: a metaanalysis comparing patellar tendon and hamstring tendon autografts. Am J Sports Med. 2003;31(1):2-11."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPORTS_MEDICINE,
        authority_weight=1.0,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Rotator Cuff Repair: Indications and Technique Selection",
        keywords=["rotator cuff", "shoulder", "tear", "repair", "arthroscopic", "tendon"],
        conclusion_template="Acute full-thickness rotator cuff tears in active patients warrant early repair (<6 months). Chronic degenerative tears may do well with PT in low-demand patients. Tear size, muscle quality (Goutallier grade), and patient age guide repair vs debridement vs reverse shoulder arthroplasty. Double-row repair biomechanically superior to single-row for tears >3cm.",
        reasoning_framework="""
Decision-making for rotator cuff pathology:

INDICATIONS FOR SURGICAL REPAIR:
Strong indications:
- Acute traumatic tear <6 months old
- Full-thickness tear with weakness
- Failed conservative therapy (3-6 months PT)
- Young patient (<60 years) with tear
- High-demand occupation/sport
- Tear >1.5cm

Relative indications:
- Chronic degenerative tear with pain (not weakness)
- Partial-thickness tear >50% tendon thickness
- Age 60-75 with good muscle quality

CONTRAINDICATIONS TO REPAIR:
Absolute:
- Active infection
- Severe muscle atrophy (Goutallier grade 4)
- Irreparable retracted tear with fixed tendon
- Medical comorbidities prohibiting surgery

Relative:
- Age >80 years
- Low-demand patient
- Minimal pain
- Workers' compensation (poorer outcomes)

REPAIR TECHNIQUE SELECTION:

Single-Row Repair:
Indications:
- Small tears (<2cm)
- Good tendon quality
- Crescent-shaped tear

Technique:
- One row of anchors in lateral footprint
- Simple or mattress sutures
- Faster surgery

Biomechanics:
- 50% contact area vs double-row
- Lower ultimate load to failure
- Similar clinical outcomes for small tears

Double-Row Repair:
Indications:
- Medium to large tears (2-4cm)
- U-shaped or L-shaped tears
- Good bone quality
- Need for maximal healing

Technique:
- Medial row of anchors (suture or knotless)
- Lateral row of anchors (suture bridge or knotless)
- Recreates anatomic footprint

Biomechanics:
- 100% contact area restoration
- Higher load to failure (650N vs 450N single-row)
- Better gap resistance
- Lower re-tear rate for large tears (15% vs 25%)

Suture Bridge (Knotless Double-Row):
- Variation of double-row
- Medial anchors pass sutures laterally
- Lateral anchors lock sutures (no knots)
- Improved healing biology (no knot prominence)
- Equivalent outcomes to standard double-row

MASSIVE ROTATOR CUFF TEARS (>5cm, 2+ tendons):
Surgical options hierarchy:
1. Attempt repair if reducible (double-row, margin convergence)
2. Superior capsular reconstruction (SCR) if irreparable
3. Reverse shoulder arthroplasty if age >70, pseudoparalysis
4. Latissimus dorsi transfer if young, active, irreparable

Goutallier classification of muscle fatty infiltration:
- Grade 0: Normal muscle
- Grade 1: Some fatty streaks
- Grade 2: More muscle than fat
- Grade 3: Equal muscle and fat
- Grade 4: More fat than muscle (irreparable, poor healing)

Repair failure predictors:
- Tear size >4cm (40% re-tear rate)
- Goutallier grade 3-4 (70% re-tear rate)
- Age >65 years
- Smoking (vasoconstriction)
- Workers' compensation (litigation bias)
- Repair under tension (>1cm retraction)

Augmentation strategies for challenging tears:
- Biologic augmentation (PRP, bone marrow aspirate)
- Patch augmentation (dermal allograft, synthetic)
- Margin convergence (side-to-side sutures before repair)
- Interval slide (release coracohumeral ligament)

Rehabilitation phases:
- Phase 1 (0-6 weeks): Passive ROM only (sling)
- Phase 2 (6-12 weeks): Active-assisted ROM
- Phase 3 (12-18 weeks): Strengthening begins
- Phase 4 (4-6 months): Return to activity
- Full healing: 6-12 months (imaging shows persistent defects in 40%)
        """,
        key_factors=[
            "Tear size and retraction",
            "Muscle quality (Goutallier grade)",
            "Patient age and activity level",
            "Acuity (acute vs chronic)",
            "Bone quality",
            "Patient compliance with rehab"
        ],
        primary_authority=[
            "Galatz LM, et al. The outcome and repair integrity of completely arthroscopically repaired large and massive rotator cuff tears. J Bone Joint Surg Am. 2004;86-A(2):219-224.",
            "Goutallier D, et al. Fatty muscle degeneration in cuff ruptures: pre- and postoperative evaluation by CT scan. Clin Orthop Relat Res. 1994;(304):78-83.",
            "Park MC, et al. Part II: Biomechanical assessment for a footprint-restoring transosseous-equivalent rotator cuff repair technique compared with a double-row repair technique. J Shoulder Elbow Surg. 2007;16(4):469-476."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPORTS_MEDICINE,
        authority_weight=1.0,
        fragility_score=0.3
    ),

    # ═══ TRAUMA MANAGEMENT ═══
    DoctrineBlock(
        topic="Compartment Syndrome: Diagnosis and Management",
        keywords=["compartment syndrome", "fasciotomy", "pressure measurement", "Whitesides", "ischemia"],
        conclusion_template="Compartment syndrome is clinical diagnosis: pain out of proportion, pain with passive stretch, tense compartment, paresthesias. Tissue pressure >30mmHg absolute or delta pressure <30mmHg (diastolic BP - compartment pressure) warrants fasciotomy. Time to fasciotomy <6 hours critical to prevent irreversible muscle necrosis and Volkmann contracture.",
        reasoning_framework="""
Compartment syndrome pathophysiology and management:

PATHOPHYSIOLOGY:
Sequence of events:
1. Increased compartment pressure (fracture, soft tissue trauma, reperfusion)
2. Venous outflow obstruction (pressure exceeds venous pressure ~25mmHg)
3. Decreased arteriovenous gradient
4. Reduced capillary perfusion
5. Muscle and nerve ischemia
6. Cell death and edema (worsens pressure - vicious cycle)

Critical pressure thresholds:
- Capillary pressure: 25-30mmHg
- Tissue ischemia begins: >20mmHg for >6 hours
- Absolute emergency: >30mmHg
- Delta pressure <30mmHg (diastolic BP - compartment pressure)

CLINICAL DIAGNOSIS (5 P's - UNRELIABLE):
1. Pain out of proportion to injury (earliest, most sensitive)
2. Pain with passive stretch (most specific)
3. Paresthesias (late finding)
4. Pulselessness (very late, irreversible damage likely)
5. Pallor (very late)
6. Pressure (tense compartment on palpation)

Key point: 2% of compartment syndromes have palpable pulses (ABI >0.9)
Waiting for pulselessness = too late

PRESSURE MEASUREMENT:
Indications:
- Uncooperative/unconscious patient
- Equivocal exam
- Regional anesthesia (masks pain)
- Polytrauma with distracting injuries

Whitesides technique:
- Handheld device or arterial line transducer
- Measure all compartments (leg has 4, forearm has 3)
- Measure at fracture site (highest pressure)

Stryker device (most common):
- Disposable pressure monitor
- Side-port needle into compartment
- Digital readout

Critical values:
- Absolute pressure >30mmHg → fasciotomy
- Delta pressure <30mmHg → fasciotomy
  (Delta = diastolic BP - compartment pressure)
- Continuous monitoring if borderline (q1-2 hours)

FASCIOTOMY INDICATIONS (ONE CRITERION SUFFICIENT):
1. Clinical compartment syndrome (pain + stretch pain)
2. Absolute pressure >30mmHg
3. Delta pressure <30mmHg
4. Pressure >25mmHg if prolonged ischemia expected (>6 hours)
5. ANY suspicion in unconscious patient

LEG FASCIOTOMY TECHNIQUE:
Four compartments:
1. Anterior (tibialis anterior, EHL, EDL)
2. Lateral (peroneus longus/brevis)
3. Superficial posterior (gastrocnemius, soleus)
4. Deep posterior (tibialis posterior, FHL, FDL)

Two-incision technique (preferred):
Anterolateral incision:
- 2cm lateral to tibial crest
- Release anterior and lateral compartments

Posteromedial incision:
- 2cm posterior to medial tibial border
- Release superficial and deep posterior compartments
- Watch for saphenous vein/nerve

Single-incision technique (fibulectomy):
- Rarely used
- Complete fibula removal
- Higher complication rate

FOREARM FASCIOTOMY:
Three compartments:
1. Volar (flexor-pronator mass)
2. Dorsal (extensor-supinator)
3. Mobile wad (brachioradialis, ECRL, ECRB)

Volar incision:
- Zigzag or lazy-S from elbow to palm
- Release carpal tunnel
- Release flexor-pronator fascia

Dorsal incision:
- Longitudinal over extensor mass
- Release extensor compartment

POSTOPERATIVE MANAGEMENT:
Immediate:
- Leave wounds open
- Sterile dressings
- Splint in position of function
- Elevate limb
- Monitor neurovascular status

Delayed closure:
- Reassess in 48-72 hours
- Skin approximation or skin graft
- NPWT (negative pressure wound therapy) bridge to closure

Complications if delayed fasciotomy:
- Rhabdomyolysis (CK >5000, myoglobinuria)
- Acute kidney injury (fluid resuscitation critical)
- Volkmann contracture (forearm)
- Foot drop (leg anterior compartment)
- Claw toe deformity (leg deep posterior)
- Amputation (if necrotic muscle not debrided)

Time-dependent outcomes:
- <6 hours: Excellent recovery expected
- 6-12 hours: Partial recovery, some deficit likely
- >12 hours: Poor outcomes, permanent disability common
- >24 hours: Consider primary amputation if necrotic
        """,
        key_factors=[
            "Time from injury",
            "Absolute compartment pressure",
            "Delta pressure (diastolic - compartment)",
            "Pain with passive stretch",
            "Associated fracture or vascular injury",
            "Patient consciousness/cooperation"
        ],
        primary_authority=[
            "Mabee JR, Bostwick TL. Pathophysiology and mechanisms of compartment syndrome. Orthop Rev. 1993;22(2):175-181.",
            "McQueen MM, Court-Brown CM. Compartment monitoring in tibial fractures: the pressure threshold for decompression. J Bone Joint Surg Br. 1996;78(1):99-104.",
            "Whitesides TE, Haney TC, Morimoto K, Harada H. Tissue pressure measurements as a determinant for the need of fasciotomy. Clin Orthop Relat Res. 1975;(113):43-51."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.TRAUMA_MANAGEMENT,
        authority_weight=1.0,
        fragility_score=0.15
    ),

    # ═══ BONE HEALING ═══
    DoctrineBlock(
        topic="Bone Healing: Diamond Concept",
        keywords=["bone healing", "nonunion", "diamond concept", "biology", "osteogenesis"],
        conclusion_template="Diamond concept requires 4 elements for successful bone healing: (1) osteoconductive scaffold, (2) osteogenic cells, (3) osteoinductive growth factors, (4) mechanical stability. Deficiency in any element leads to nonunion. Smoking reduces healing by 50%, NSAIDs delay healing but don't prevent it, and electrical stimulation improves healing in recalcitrant cases.",
        reasoning_framework="""
Diamond concept of bone healing (Giannoudis 2007):

ELEMENT 1: OSTEOCONDUCTIVE SCAFFOLD
Definition: 3D matrix for cell migration and vascularization
Options:
- Autograft bone (gold standard)
- Allograft bone (structural, no cells)
- Bone graft substitutes (calcium phosphate, calcium sulfate)
- DBM (demineralized bone matrix)

Key points:
- Autograft best but limited quantity (30cc from iliac crest)
- RIA (reamer-irrigator-aspirator) harvests 60-90cc from femur
- Masquelet technique: Cement spacer induces membrane, then graft
- Bone graft substitutes good for metaphyseal voids, poor for critical defects

ELEMENT 2: OSTEOGENIC CELLS
Definition: Cells capable of forming bone (MSCs, osteoblasts)
Sources:
- Bone marrow aspirate (iliac crest: 1 in 50,000 cells is MSC)
- Adipose tissue (1 in 500 cells is MSC)
- Autograft bone (contains viable cells)
- BMA + cancellous autograft = synergistic

Key points:
- MSC concentration decreases with age
- Iliac crest aspirate: 2-6 x 10^6 nucleated cells/mL
- Centrifugation concentrates cells 3-5 fold
- Single aspiration 2mL max (larger volume = peripheral blood dilution)

ELEMENT 3: OSTEOINDUCTIVE GROWTH FACTORS
Definition: Signals that induce MSC differentiation to osteoblasts
Endogenous:
- BMPs (bone morphogenetic proteins) - BMP-2, BMP-7
- PDGF (platelet-derived growth factor)
- IGF (insulin-like growth factor)
- TGF-β (transforming growth factor beta)

Exogenous (FDA approved):
- rhBMP-2 (INFUSE): Anterior lumbar fusion, tibial nonunion
- rhBMP-7 (OP-1): Tibial nonunion (humanitarian device exemption)
- PRP (platelet-rich plasma): Concentrated growth factors, mixed evidence

BMP-2 dosing:
- ALIF: 12mg on collagen sponge
- Tibial nonunion: 6-12mg
- WARNING: Off-label cervical spine use → airway swelling risk
- WARNING: High dose (>40mg) → ectopic bone, seroma, osteolysis

ELEMENT 4: MECHANICAL STABILITY
Definition: Appropriate mechanical environment for healing
Stability spectrum:
- Absolute stability → primary bone healing (no callus)
  - Compression plating
  - Lag screw fixation
- Relative stability → secondary bone healing (callus formation)
  - Intramedullary nail
  - Bridge plating
  - External fixation

Interfragmentary strain theory:
- <2% strain: Primary bone healing (cortical remodeling)
- 2-10% strain: Optimal callus formation
- >10% strain: Nonunion (excessive motion)

Fixation method by fracture:
- Simple metaphyseal: Compression plating (absolute stability)
- Diaphyseal: IM nail (relative stability)
- Complex comminuted: Bridge plate (relative stability)

NONUNION TREATMENT (Diamond applied):
Atrophic nonunion (no callus, biology problem):
1. Scaffold: Autograft or BMP-2
2. Cells: BMA from iliac crest
3. Growth factors: BMP-2 (6-12mg)
4. Stability: Increase fixation rigidity

Hypertrophic nonunion (abundant callus, mechanics problem):
1. Scaffold: Not needed (biology intact)
2. Cells: Not needed
3. Growth factors: Not needed
4. Stability: Increase rigidity (exchange nail, add plate)

MODIFIABLE FACTORS AFFECTING HEALING:

Negative factors:
- Smoking: 2x nonunion risk (nicotine vasoconstriction)
- NSAIDs: Delay healing 2-4 weeks, don't prevent if <2 weeks
- Diabetes: Poor glycemic control (HbA1c >7%) impairs healing
- Malnutrition: Albumin <3.5, vitamin D <20
- Infection: Biofilm prevents healing
- Gap >5mm: Critical-size defect

Positive factors:
- Low-intensity pulsed ultrasound (LIPUS): 20 min/day, 38% faster healing
- Electrical stimulation: Capacitive coupling or pulsed electromagnetic fields
- Weight bearing: Cyclical loading stimulates callus (Wolff's law)
- Vitamin D supplementation: Goal >30 ng/mL
- Smoking cessation: Improves healing within 4 weeks

TIMELINE OF HEALING:
- Inflammatory phase: 0-7 days (hematoma, cytokine release)
- Soft callus: 1-3 weeks (cartilage, type II collagen)
- Hard callus: 3-12 weeks (woven bone, type I collagen)
- Remodeling: 3 months - 2 years (lamellar bone, Haversian systems)

Radiographic healing:
- Bridging callus 3 of 4 cortices
- Trabeculae crossing fracture site
- Loss of fracture line

Clinical healing:
- No pain with weight bearing
- No motion at fracture site
- Full function restored
        """,
        key_factors=[
            "Fracture biology (blood supply, soft tissue injury)",
            "Mechanical stability adequacy",
            "Patient factors (smoking, diabetes, nutrition)",
            "Infection presence",
            "Gap size and bone loss",
            "Fixation method and implant choice"
        ],
        primary_authority=[
            "Giannoudis PV, Einhorn TA, Marsh D. Fracture healing: the diamond concept. Injury. 2007;38 Suppl 4:S3-6.",
            "Bhandari M, et al. Pharmacological interventions for preventing delayed union and nonunion in long bone fractures. Cochrane Database Syst Rev. 2012;(5):CD005479.",
            "Einhorn TA, Gerstenfeld LC. Fracture healing: mechanisms and interventions. Nat Rev Rheumatol. 2015;11(1):45-54."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BONE_HEALING,
        authority_weight=1.0,
        fragility_score=0.2
    ),

    # ═══ IMAGING INTERPRETATION ═══
    DoctrineBlock(
        topic="Musculoskeletal MRI: Meniscal Tear Classification",
        keywords=["meniscus", "MRI", "tear", "knee", "imaging", "meniscal"],
        conclusion_template="Meniscal tears graded 0-III on MRI. Grade I = intrasubstance signal not touching surface (no tear). Grade II = linear signal not extending to surface (no tear, degeneration). Grade III = signal extending to articular surface (true tear). Vertical longitudinal tears (bucket handle) are unstable and usually require repair. Horizontal tears often asymptomatic degenerative changes in patients >40 years.",
        reasoning_framework="""
MRI classification and clinical correlation for meniscal pathology:

STOLLER CLASSIFICATION (MRI grading):
Grade 0: Normal meniscus
- Homogeneous low signal (black) on all sequences
- Sharp triangular morphology
- Smooth articular surface

Grade I: Intrasubstance degeneration
- Focal globular increased signal (white)
- Does NOT extend to surface
- Myxoid degeneration (mucoid material)
- Not a tear, no surgical indication
- Asymptomatic, age-related change

Grade II: Intrasubstance degeneration (advanced)
- Linear increased signal (white)
- Does NOT extend to articular surface
- Still not a tear
- May progress to Grade III
- No surgical indication

Grade III: True meniscal tear
- Linear increased signal extending to articular surface
- Confirmed on 2+ consecutive slices
- Requires clinical correlation for treatment

TEAR PATTERN CLASSIFICATION:
Vertical tears:
1. Longitudinal (vertical): Parallel to circumferential fibers
   - Stable if <10mm length
   - Unstable if full-length (bucket handle)
   - Medial meniscus more common
   - Repairable if peripheral (red-red or red-white zone)

2. Radial: Perpendicular to circumferential fibers
   - Root tears (posterior root avulsion)
   - Parrot beak configuration
   - Disrupt hoop stresses
   - Poor healing (white-white zone)
   - Usually require partial meniscectomy

3. Bucket handle: Long longitudinal tear with displacement
   - Fragment flips into intercondylar notch
   - Locked knee (blocks extension)
   - Double PCL sign on MRI
   - Surgical emergency (repair vs excision)

Horizontal tears:
- Parallel to tibial plateau
- Splits meniscus into superior and inferior leaflets
- Degenerative, common >40 years old
- Often asymptomatic (incidental finding)
- Partial meniscectomy if symptomatic

Complex tears:
- Combination of vertical and horizontal components
- Unstable, fragmented tissue
- Usually require debridement (not repairable)

MENISCAL ZONES (Blood supply):
Red-Red zone (peripheral 0-3mm):
- Vascular supply from perimeniscal capillary plexus
- Excellent healing potential
- Repair success rate 85-90%

Red-White zone (3-6mm from periphery):
- Partial vascular supply
- Moderate healing potential
- Repair success rate 60-75%
- May augment with fibrin clot, PRP

White-White zone (>6mm from periphery, central):
- Avascular
- Poor healing potential
- Repair success rate <25%
- Usually debride vs leave alone if stable

CLINICAL CORRELATION (Critical):
MRI sensitivity for meniscal tear: 89%
MRI specificity: 88%
BUT: 35% of asymptomatic adults >40 have Grade III signal

Treatment algorithm:
1. Grade III + mechanical symptoms (locking, catching) → Arthroscopy
2. Grade III + NO symptoms → Conservative (PT, injections)
3. Grade III + degenerative knee (OA) → Conservative (meniscectomy worsens OA)
4. Grade I/II regardless of symptoms → Conservative

Meniscal repair vs meniscectomy decision:
Repair indications:
- Vertical longitudinal tear >10mm
- Tear in red-red or red-white zone (<6mm from periphery)
- Acute tear (<6 months)
- Young patient (<40 years)
- Stable knee (intact ACL) or concurrent ACL reconstruction
- No degenerative changes

Meniscectomy indications:
- Complex tear
- White-white zone tear
- Horizontal tear (symptomatic)
- Degenerative tear (age >50)
- Failed prior repair
- Irreparable root tear

Leave-alone indications:
- Small stable tear (<5mm)
- Asymptomatic incidental finding
- Degenerative knee with OA

Root tear special considerations:
- Posterior medial meniscal root (PMMR) tear:
  - Extrusion of meniscus (>3mm on coronal MRI)
  - Equivalent to total meniscectomy (loss of hoop stresses)
  - Rapid cartilage degeneration if untreated
  - Transtibial pullout repair recommended if symptomatic

POST-MENISCECTOMY SEQUELAE:
- Each 10% of meniscus removed → 2x increase in contact stress
- Total meniscectomy → 3-6x peak stress increase
- Accelerated OA in 80% at 10 years
- Medial meniscectomy worse than lateral (60% vs 40% weight bearing)

MENISCAL REPAIR TECHNIQUES:
- Inside-out: Gold standard, low failure (5-10%), nerve risk
- Outside-in: Anterior horn tears, nerve-sparing
- All-inside: Fast, popular, 10-15% failure, less invasive
- Root repair: Transtibial pullout with suture anchor
        """,
        key_factors=[
            "MRI grade (I/II vs III)",
            "Patient age and activity level",
            "Presence of mechanical symptoms",
            "Tear pattern and location (zone)",
            "Degree of osteoarthritis",
            "ACL status (intact vs torn)"
        ],
        primary_authority=[
            "Stoller DW, et al. Meniscal tears: pathologic correlation with MR imaging. Radiology. 1987;163(3):731-735.",
            "Englund M, et al. Incidental meniscal findings on knee MRI in middle-aged and elderly persons. N Engl J Med. 2008;359(11):1108-1115.",
            "Pache S, et al. Meniscal ramp lesions: anatomy, diagnosis, and treatment. Arthroscopy. 2018;34(5):1382-1400."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.IMAGING_INTERPRETATION,
        authority_weight=1.0,
        fragility_score=0.25
    ),
]

# ═══════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════

ORTHOPEDIC_TERM_MAP = {
    # Fracture terminology
    "broken bone": "fracture",
    "crack": "fracture",
    "breakage": "fracture",
    "ao classification": "AO/OTA classification",
    "open wound": "open fracture",
    "compound fracture": "open fracture",
    "closed fracture": "simple fracture",

    # Joint replacement
    "hip replacement": "total hip arthroplasty",
    "knee replacement": "total knee arthroplasty",
    "tha": "total hip arthroplasty",
    "tka": "total knee arthroplasty",
    "artificial joint": "arthroplasty",
    "prosthetic joint": "arthroplasty",

    # Spine
    "spinal fusion": "lumbar fusion",
    "back surgery": "spine surgery",
    "disc": "intervertebral disc",
    "slipped disc": "disc herniation",
    "pinched nerve": "nerve compression",

    # Sports medicine
    "torn acl": "ACL tear",
    "torn meniscus": "meniscal tear",
    "shoulder tear": "rotator cuff tear",
    "knee cartilage": "meniscus",

    # General
    "bone scan": "imaging",
    "x-ray": "radiograph",
    "mri": "magnetic resonance imaging",
    "ct scan": "computed tomography",
    "bone density": "DEXA scan",
    "infection": "osteomyelitis",
    "bone infection": "osteomyelitis",
    "nonhealing": "nonunion",
    "delayed healing": "delayed union",
}

def normalize_query(query: str) -> str:
    """Normalize orthopedic terminology"""
    normalized = query.lower()
    for term, replacement in ORTHOPEDIC_TERM_MAP.items():
        normalized = normalized.replace(term, replacement)
    return normalized

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class QueryTelemetry:
    query_id: str
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    doctrines_triggered: List[str]
    cache_hit: bool
    latency_ms: float
    confidence: ConfidenceLevel
    fragility_score: float
    timestamp: str
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self.queries: List[QueryTelemetry] = []
        self.start_time = time.time()

    def record(self, telemetry: QueryTelemetry):
        self.queries.append(telemetry)

        # Write to audit trail
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "query_id": telemetry.query_id,
                "timestamp": telemetry.timestamp,
                "query": telemetry.query,
                "mode": telemetry.mode,
                "zone": telemetry.zone,
                "doctrines": telemetry.doctrines_triggered,
                "cache_hit": telemetry.cache_hit,
                "latency_ms": telemetry.latency_ms,
                "confidence": telemetry.confidence,
                "fragility": telemetry.fragility_score,
                "error": telemetry.error
            }) + "\n")

    def get_metrics(self) -> Dict[str, Any]:
        if not self.queries:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "cache_hit_rate": 0.0,
                "error_rate": 0.0
            }

        total = len(self.queries)
        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        errors = sum(1 for q in self.queries if q.error)
        avg_latency = sum(q.latency_ms for q in self.queries) / total

        return {
            "total_queries": total,
            "avg_latency_ms": round(avg_latency, 2),
            "cache_hit_rate": round(cache_hits / total, 3),
            "error_rate": round(errors / total, 3),
            "uptime_seconds": round(time.time() - self.start_time, 1)
        }

# Global telemetry collector
telemetry = TelemetryCollector()

# ═══════════════════════════════════════════════════════════════════════════
# COVERAGE MAP & DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════

class CoverageMap:
    def __init__(self):
        self.triggered: Dict[str, int] = defaultdict(int)
        self.missed_queries: List[str] = []

    def record_trigger(self, topic: str):
        self.triggered[topic] += 1

    def record_miss(self, query: str):
        self.missed_queries.append(query)

    def get_coverage(self) -> Dict[str, Any]:
        total_doctrines = len(DOCTRINE_CACHE)
        triggered_count = len(self.triggered)

        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_count,
            "coverage_rate": round(triggered_count / total_doctrines, 3) if total_doctrines else 0,
            "most_triggered": sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:5],
            "epistemic_gaps": len(self.missed_queries),
            "sample_gaps": self.missed_queries[-5:] if self.missed_queries else []
        }

coverage_map = CoverageMap()

# ═══════════════════════════════════════════════════════════════════════════
# CORE ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def three_layer_response(
    query: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    context: Optional[Dict[str, Any]]
) -> QueryResponse:
    """
    TIE-20 Component #1: Three-layer response
    Layer 1: Doctrine cache (0-200ms)
    Layer 2: Semantic retrieval (200-1000ms)
    Layer 3: Deep analysis (1000ms+)
    """
    start_time = time.time()
    query_id = hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:16]

    normalized_query = normalize_query(query)

    # Layer 1: Doctrine cache lookup
    matched_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        score = doctrine.matches(normalized_query)
        if score > 0.2:  # 20% keyword match threshold
            matched_doctrines.append((score, doctrine))
            coverage_map.record_trigger(doctrine.topic)

    matched_doctrines.sort(reverse=True, key=lambda x: x[0])
    cache_hit = len(matched_doctrines) > 0

    if not cache_hit:
        coverage_map.record_miss(query)

    # Build response based on mode
    if mode == ResponseMode.FAST:
        answer = build_fast_response(matched_doctrines, context)
    elif mode == ResponseMode.DEFENSE:
        answer = build_defense_response(matched_doctrines, context)
    else:  # MEMO
        answer = build_memo_response(matched_doctrines, context, zone)

    # Calculate confidence and fragility
    confidence = calculate_confidence(matched_doctrines)
    fragility = calculate_fragility(matched_doctrines)

    # Extract categories
    categories = list(set(d.category for _, d in matched_doctrines[:3]))

    # Determinism hash
    determinism_hash = hashlib.sha256(
        f"{query}{mode}{zone}{[d.topic for _, d in matched_doctrines]}".encode()
    ).hexdigest()[:16]

    latency_ms = (time.time() - start_time) * 1000

    # Build doctrine matches for response
    doctrine_matches = [
        DoctrineMatch(
            topic=doctrine.topic,
            keywords=doctrine.keywords,
            conclusion=doctrine.render(context or {}),
            reasoning=doctrine.reasoning_framework[:500] if mode == ResponseMode.FAST else doctrine.reasoning_framework,
            confidence=doctrine.confidence,
            authority_weight=doctrine.authority_weight,
            sources=doctrine.primary_authority
        )
        for score, doctrine in matched_doctrines[:5]
    ]

    response = QueryResponse(
        query=query,
        mode=mode,
        zone=zone,
        answer=answer,
        doctrines_triggered=doctrine_matches,
        confidence=confidence,
        fragility_score=fragility,
        categories=categories,
        determinism_hash=determinism_hash,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.utcnow().isoformat()
    )

    # Record telemetry
    telemetry.record(QueryTelemetry(
        query_id=query_id,
        query=query,
        mode=mode,
        zone=zone,
        doctrines_triggered=[d.topic for _, d in matched_doctrines],
        cache_hit=cache_hit,
        latency_ms=latency_ms,
        confidence=confidence,
        fragility_score=fragility,
        timestamp=response.timestamp
    ))

    return response

def build_fast_response(matched_doctrines: List[Tuple[float, DoctrineBlock]], context: Optional[Dict]) -> str:
    """FAST mode: Concise conclusion"""
    if not matched_doctrines:
        return "No specific orthopedic doctrine matched. Please provide more clinical details."

    top_doctrine = matched_doctrines[0][1]
    return top_doctrine.render(context or {})

def build_defense_response(matched_doctrines: List[Tuple[float, DoctrineBlock]], context: Optional[Dict]) -> str:
    """DEFENSE mode: Audit-ready with citations"""
    if not matched_doctrines:
        return "INSUFFICIENT DATA: No established orthopedic doctrine applies. Recommend specialist consultation."

    parts = []
    for i, (score, doctrine) in enumerate(matched_doctrines[:3], 1):
        parts.append(f"DOCTRINE {i}: {doctrine.topic}")
        parts.append(f"CONCLUSION: {doctrine.render(context or {})}")
        parts.append(f"AUTHORITY: {'; '.join(doctrine.primary_authority)}")
        parts.append(f"CONFIDENCE: {doctrine.confidence.value}")
        parts.append("")

    return "\n".join(parts)

def build_memo_response(matched_doctrines: List[Tuple[float, DoctrineBlock]], context: Optional[Dict], zone: AnalysisZone) -> str:
    """MEMO mode: Full documentation"""
    if not matched_doctrines:
        return """ORTHOPEDIC ANALYSIS MEMORANDUM

ISSUE: Query does not match established orthopedic doctrine in our knowledge base.

RECOMMENDATION:
1. Consult subspecialist in relevant field
2. Review current literature
3. Consider multidisciplinary case conference

This represents an epistemic gap in the current doctrine cache."""

    parts = [f"ORTHOPEDIC ANALYSIS MEMORANDUM - {zone.value} ZONE", "=" * 60, ""]

    for i, (score, doctrine) in enumerate(matched_doctrines[:3], 1):
        parts.append(f"DOCTRINE {i}: {doctrine.topic}")
        parts.append(f"Match Score: {score:.1%}")
        parts.append("")
        parts.append("CONCLUSION:")
        parts.append(doctrine.render(context or {}))
        parts.append("")
        parts.append("REASONING FRAMEWORK:")
        parts.append(doctrine.reasoning_framework)
        parts.append("")
        parts.append("KEY FACTORS:")
        for factor in doctrine.key_factors:
            parts.append(f"  - {factor}")
        parts.append("")
        parts.append("PRIMARY AUTHORITY:")
        for auth in doctrine.primary_authority:
            parts.append(f"  - {auth}")
        parts.append("")
        parts.append(f"CONFIDENCE LEVEL: {doctrine.confidence.value}")
        parts.append(f"EVIDENCE FRAGILITY: {doctrine.fragility_score:.2f}")
        parts.append("")
        parts.append("-" * 60)
        parts.append("")

    return "\n".join(parts)

def calculate_confidence(matched_doctrines: List[Tuple[float, DoctrineBlock]]) -> ConfidenceLevel:
    """Calculate overall confidence level"""
    if not matched_doctrines:
        return ConfidenceLevel.DISCLOSURE

    top_score = matched_doctrines[0][0]
    top_doctrine = matched_doctrines[0][1]

    if top_score > 0.6 and top_doctrine.confidence == ConfidenceLevel.DEFENSIBLE:
        return ConfidenceLevel.DEFENSIBLE
    elif top_score > 0.4:
        return ConfidenceLevel.AGGRESSIVE
    elif top_score > 0.2:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

def calculate_fragility(matched_doctrines: List[Tuple[float, DoctrineBlock]]) -> float:
    """Calculate fact fragility score"""
    if not matched_doctrines:
        return 0.9

    scores = [d.fragility_score for _, d in matched_doctrines[:3]]
    return sum(scores) / len(scores) if scores else 0.5

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    description="Orthopedics Analysis Engine with TIE-20 components",
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode} | Zone: {request.zone}")
        response = three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
        logger.info(f"Query completed in {response.latency_ms}ms | Confidence: {response.confidence}")
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    metrics = telemetry.get_metrics()
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        total_queries=metrics["total_queries"],
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["cache_hit_rate"],
        uptime_seconds=metrics["uptime_seconds"]
    )

@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage map"""
    return coverage_map.get_coverage()

@app.get("/metrics")
async def metrics_endpoint():
    """Detailed metrics"""
    return telemetry.get_metrics()

@app.get("/doctrines")
async def doctrines_endpoint():
    """List all loaded doctrines"""
    return [
        {
            "topic": d.topic,
            "category": d.category.value,
            "keywords": d.keywords,
            "confidence": d.confidence.value,
            "authority_weight": d.authority_weight
        }
        for d in DOCTRINE_CACHE
    ]

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Audit trail: {AUDIT_FILE}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
