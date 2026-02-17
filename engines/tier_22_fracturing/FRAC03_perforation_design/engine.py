"""
FRAC03 - Perforation Design Engine
Tax Intelligence Engine (TIE) Gold Standard Pattern
Port: 9023 | Domain: Completions - Perforating

Real perforating engineering expertise encoded as doctrine blocks.
Covers shaped charge design, gun systems, shot density/phasing, perforation
friction calculations, limited entry design, cluster efficiency, dynamic
underbalance, API testing standards, gun debris, HPHT operations, oriented
perforating, propellant systems, abrasive jetting, erosion, TCP operations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "FRAC03"
ENGINE_NAME = "Perforation Design Engine"
VERSION = "1.0.0"
PORT = 9023

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    backtrace=True,
    diagnose=True
)


# ============================================================================
# ENUMS
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
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    CHARGE_DESIGN = "CHARGE_DESIGN"
    GUN_SYSTEM = "GUN_SYSTEM"
    SHOT_DENSITY = "SHOT_DENSITY"
    PHASING = "PHASING"
    PERFORATION_FRICTION = "PERFORATION_FRICTION"
    LIMITED_ENTRY = "LIMITED_ENTRY"
    CLUSTER_EFFICIENCY = "CLUSTER_EFFICIENCY"
    UNDERBALANCED_PERF = "UNDERBALANCED_PERF"
    OVERBALANCED_PERF = "OVERBALANCED_PERF"
    API_TESTING = "API_TESTING"
    GUN_DEBRIS = "GUN_DEBRIS"
    HPHT_OPERATIONS = "HPHT_OPERATIONS"
    ORIENTED_PERF = "ORIENTED_PERF"
    PROPELLANT_SYSTEMS = "PROPELLANT_SYSTEMS"
    ABRASIVE_JETTING = "ABRASIVE_JETTING"
    PERFORATION_EROSION = "PERFORATION_EROSION"
    FRAC_OPTIMIZATION = "FRAC_OPTIMIZATION"
    TCP_OPERATIONS = "TCP_OPERATIONS"
    WIRELINE_OPERATIONS = "WIRELINE_OPERATIONS"
    SAFETY = "SAFETY"


class AuthorityLevel(str, Enum):
    API_STANDARD = "API_STANDARD"
    INDUSTRY_PRACTICE = "INDUSTRY_PRACTICE"
    FIELD_DATA = "FIELD_DATA"
    SIMULATION = "SIMULATION"
    VENDOR_SPEC = "VENDOR_SPEC"
    EXPERT_OPINION = "EXPERT_OPINION"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    authority_level: AuthorityLevel
    fragility_score: float = 0.0


class QueryRequest(BaseModel):
    question: str = Field(..., description="Perforation design question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    response_time_ms: float
    determinism_hash: str
    telemetry: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL PERFORATING EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Deep Penetrating vs Big Hole Charge Design",
        keywords=["shaped charge", "penetration depth", "entry hole", "charge design", "deep penetrating", "big hole"],
        conclusion_template=[
            "Deep penetrating charges (small diameter, high velocity jet) are preferred for maximizing reservoir contact in low permeability formations.",
            "Big hole charges (larger diameter, lower penetration) improve productivity in high permeability or unconsolidated formations by reducing near-wellbore damage.",
            "Charge selection must balance penetration depth (typically 12-36 inches) against entry hole diameter (0.3-0.7 inches) based on reservoir properties."
        ],
        reasoning_framework="""
Shaped charge design fundamentally trades penetration depth for entry hole diameter:
1. Deep Penetrating Charges: Small liner diameter (19-25mm cone angle 40-42°), high detonation velocity (7000-8000 m/s), jet velocity >8 km/s. Penetration 24-36 inches in concrete, entry hole 0.3-0.4 inches. Preferred for tight formations (k<1 mD) where deep reservoir contact is critical.
2. Big Hole Charges: Larger liner diameter (25-34mm cone angle 50-60°), moderate detonation velocity, wider jet. Penetration 12-20 inches, entry hole 0.5-0.7 inches. Preferred for high perm (k>50 mD) or unconsolidated sands where skin damage dominates.
3. Physics: Jet penetration ∝ (ρ_liner/ρ_target)^0.5 * L_liner * (v_jet/v_target)^0.5. Entry hole ∝ liner diameter.
4. Productivity: In tight rock, flow is radial—deeper penetration bypasses damaged zone. In high perm, convergence near wellbore dominates—larger entry reduces friction.
5. Casing/cement: Deep penetrating charges create cleaner tunnels through steel/cement interfaces, reducing debris.
        """,
        key_factors=[
            "Formation permeability (tight vs permeable)",
            "Reservoir damage extent (skin factor)",
            "Casing/cement bond quality",
            "Gun size constraints (3-1/8\" vs 7\" OD)",
            "Shot density requirements (holes per foot)",
            "Cost considerations (deep penet charges more expensive)",
            "Target penetration through damaged zone"
        ],
        primary_authority=[
            "API RP 19B Section 1: Surface Performance Testing",
            "SPE 25891: Optimum Perforating Strategy",
            "SPE 73337: Impact of Perforation Entry Hole Diameter on Flow Performance"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Use cheapest charges that meet minimum penetration spec",
        counter_arguments=[
            "Deep penetrating charges cost 40-60% more than big hole charges",
            "In very high perm reservoirs (k>500 mD), entry hole diameter becomes dominant factor",
            "Perforation cleanup (underbalance surge) can enlarge entry holes post-perf",
            "Gun debris from deep penetrating charges can be harder to clean out"
        ],
        resolution_strategy="Perform nodal analysis with different charge types—model perforation skin effect (Karakas-Tariq correlation) and total productivity. In unconventionals (k<0.001 mD), deep penetrating almost always wins. In conventional high perm, run sensitivity on entry hole diameter impact.",
        entity_scope="All perforating operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Deep penetrating preference in tight formations is industry consensus with strong field data support. Big hole advantage in high perm has theoretical basis but fewer field confirmations.",
        controlling_precedent="API RP 19B performance testing standards",
        issue_category=IssueCategory.CHARGE_DESIGN,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Shot Density and Phasing for Horizontal Wells",
        keywords=["shot density", "phasing", "spf", "holes per foot", "0 degree", "60 degree", "90 degree", "120 degree", "180 degree"],
        conclusion_template=[
            "In horizontal wells, 60-degree phasing with 6-10 SPF (shots per foot) is the industry standard for balancing perforation friction and rock coverage.",
            "0-degree phasing (all shots in single plane) creates extreme limited entry but risks uneven fracture initiation across clusters.",
            "Higher shot density (>12 SPF) reduces perforation friction but increases gun cost and debris volume without proportional productivity gain."
        ],
        reasoning_framework="""
Shot density and phasing control both perforation friction (critical for limited entry) and fracture initiation:
1. Shot Density (SPF): 4 SPF = underperforated (high friction), 6-8 SPF = standard, 10-12 SPF = high density, 16+ SPF = extreme (often unnecessary). Perforation friction ∝ 1/N_perfs. Doubling SPF cuts friction by ~40% (not 50% due to interference).
2. Phasing: 0° = all shots on one side (spiral). 60° = 6 shots/360° spiral. 90° = 4 shots orthogonal. 120° = 3 shots. 180° = 2 shots opposite sides.
3. Limited Entry Physics: Want HIGH perforation friction to divert flow to other clusters. 0° or 60° with low SPF (4-6) maximizes friction. But 0° risks skipping clusters if initiation is asymmetric.
4. Rock Coverage: 60° phasing ensures more uniform radial coverage around wellbore. 0° leaves 3/4 of wellbore perimeter unperforated—fracture may not initiate if charges face away from max horizontal stress.
5. Horizontal Well Practice: 60° phasing, 6 SPF, 6-8 shots/cluster (1-1.5 ft clusters). This gives moderate perforation friction (500-1500 psi at 60 bpm) while ensuring at least one shot is somewhat aligned with fracture plane.
6. Perforation Friction Calculation: ΔP = (ρ*Q²)/(2*C²*A²*N) where C=discharge coeff ~0.6-0.8, A=hole area, N=number of holes. Phasing affects effective N due to interference.
        """,
        key_factors=[
            "Limited entry design goals (perforation friction target)",
            "Cluster spacing (closer spacing needs fewer SPF/cluster)",
            "Gun outer diameter constraints (small guns can't fit high SPF)",
            "Fracture initiation risk (0° phasing can cause skips)",
            "Gun debris volume (higher SPF = more debris)",
            "Cost (charges, gun assembly time)",
            "Erosion during frac (higher SPF reduces per-perf erosion)"
        ],
        primary_authority=[
            "SPE 184834: Limited Entry Design in Unconventional Reservoirs",
            "SPE 194357: Perforation Friction Pressure Loss",
            "SPE 179117: Impact of Perforation Phasing on Fracture Initiation"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Use highest SPF possible to minimize perforation friction and ensure all clusters frac",
        counter_arguments=[
            "High SPF (12-16) reduces limited entry effectiveness—all clusters get flow, can't divert to unopened intervals",
            "0-degree phasing creates maximum limited entry but field data shows uneven cluster efficiency",
            "In very low permeability (k<0.0001 mD), perforation friction becomes insignificant relative to formation entry friction",
            "Gun debris from 16 SPF can bridge off and cause screenouts"
        ],
        resolution_strategy="Model perforation friction for different SPF/phasing combinations. Target 500-2000 psi friction at design rate (60-80 bpm). Use 60° phasing as default for fracture initiation reliability. Consider oriented perforating if stress field is well-known—align shots with SHmax for easier initiation.",
        entity_scope="Horizontal well completions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="60° phasing at 6-8 SPF is industry consensus. Optimal friction target varies by operator and basin—some prefer 1000 psi, others 3000 psi.",
        controlling_precedent="Industry practice in Permian, Eagle Ford, Bakken",
        issue_category=IssueCategory.SHOT_DENSITY,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE,
        fragility_score=0.30
    ),

    DoctrineBlock(
        topic="Limited Entry Perforation Friction Diversion",
        keywords=["limited entry", "perforation friction", "diversion", "cluster efficiency", "friction pressure"],
        conclusion_template=[
            "Limited entry design uses perforation friction to equalize flow distribution across clusters in plug-and-perf completions.",
            "Target perforation friction of 500-2000 psi at design injection rate forces heel clusters (lower friction path to wellbore) to take similar fluid volume as toe clusters.",
            "Effectiveness depends on achieving 2-4x ratio of perforation friction to near-wellbore formation entry friction."
        ],
        reasoning_framework="""
Limited entry creates artificial flow restriction to overcome natural bias toward heel:
1. Problem: In plug-and-perf, heel clusters are nearest the wellbore entry point. Without perforation restriction, 70-90% of fluid goes to first 2-3 clusters (heel bias). Toe clusters starve.
2. Solution: Reduce perforation count (4-6 SPF instead of 12-16) to create high friction. If ΔP_perf >> ΔP_formation_entry, flow equalizes because all clusters see similar total backpressure.
3. Design Target: ΔP_perf = 500-2000 psi at 60-80 bpm injection rate. Higher friction = better diversion but risks exceeding surface pressure limits.
4. Physics: Perforation friction ΔP = (ρQ²)/(2C²A²N). To increase friction: reduce N (lower SPF), reduce hole area A (smaller entry holes), or increase rate Q.
5. Perforation Erosion Issue: During pumping, perforation holes erode (especially with proppant). Entry holes can grow from 0.4" to 0.7-1.0". Friction drops 50-75% over the stage. Limited entry effectiveness degrades.
6. Cluster Efficiency: Good limited entry achieves 60-80% cluster efficiency (% of clusters that initiate fractures). Poor design (low friction) sees 30-50% efficiency—toe clusters never break down.
7. Ratio Rule: Want ΔP_perf / ΔP_formation ≈ 2-4. If formation entry friction is 100 psi (high perm), need 200-400 psi perforation friction. If formation entry is 1000 psi (tight rock), need 2000-4000 psi perforation friction.
8. Trade-offs: High perforation friction increases screenout risk (can't inject enough fluid to place proppant). Must model with frac simulator.
        """,
        key_factors=[
            "Injection rate (bpm) and fluid viscosity",
            "Formation permeability (affects entry friction)",
            "Cluster spacing (closer spacing needs less diversion)",
            "Number of clusters per stage",
            "Perforation erosion rate during treatment",
            "Surface pressure limitations",
            "Fracture toughness (affects breakdown pressure variation)",
            "Stress shadow effects between clusters"
        ],
        primary_authority=[
            "SPE 184834: Limited Entry Design Optimization",
            "SPE 189895: Cluster Efficiency and Perforation Erosion",
            "SPE 174829: Perforation Friction Pressure Loss Mechanisms"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Perforate all clusters with high SPF to ensure breakdown—don't rely on friction diversion",
        counter_arguments=[
            "In very tight formations (k<0.0001 mD), formation entry friction dominates—perforation friction becomes secondary",
            "Perforation erosion during treatment means limited entry only works for first 10-20% of proppant—rest of stage has no diversion",
            "Diverter systems (degradable particles) can achieve better late-stage diversion than perforation friction",
            "Field tracer studies show limited entry often fails—heel bias still observed even with 'proper' friction design"
        ],
        resolution_strategy="Model with hydraulic fracture simulator coupling perforation friction + formation entry + stress shadows. Run sensitivity on SPF (4, 6, 8, 10, 12). Target ΔP_perf ≈ 1000-1500 psi initially, knowing it will drop 50%+ due to erosion. Consider hybrid approach: limited entry for initiation + chemical diverter for late-stage proppant placement.",
        entity_scope="Plug-and-perf completions in horizontal wells",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Limited entry theory is sound, but field effectiveness is highly variable. Some operators report excellent results, others see minimal improvement over high SPF. Depends on formation properties, stress regime, fluid design.",
        controlling_precedent="Industry practice—not codified in standards",
        issue_category=IssueCategory.LIMITED_ENTRY,
        authority_level=AuthorityLevel.FIELD_DATA,
        fragility_score=0.45
    ),

    DoctrineBlock(
        topic="Underbalanced vs Overbalanced Perforating",
        keywords=["underbalanced", "overbalanced", "dynamic underbalance", "surge", "cleanup", "perforation damage"],
        conclusion_template=[
            "Underbalanced perforating (wellbore pressure < reservoir pressure during shot detonation) creates surge flow that cleans perforation tunnels of debris and crushed rock.",
            "Overbalanced perforating (wellbore pressure > reservoir pressure) forces drilling mud and debris into perforation tunnels, creating near-wellbore damage that can reduce productivity by 50-80%.",
            "Dynamic underbalance >200-300 psi is recommended for maximizing perforating efficiency in most applications."
        ],
        reasoning_framework="""
Perforating creates debris and damage that must be removed to achieve full productivity:
1. Damage Mechanisms: Shaped charge detonation creates crushed zone around tunnel (compacted rock, low perm). Debris from charge liner, gun steel, and pulverized rock fills tunnel. Overbalanced pressure forces this debris + drilling mud solids into formation, plugging pore throats.
2. Underbalanced Perforating: Set wellbore pressure below reservoir pressure before shooting. When charges detonate, reservoir fluid surges into wellbore, flushing debris out of tunnels. Surge flow can be 10-100x higher velocity than normal production—effective cleanup.
3. Dynamic Underbalance: Instantaneous pressure differential when shot fires. Can be much higher than static underbalance due to rapid gas expansion or wellbore unloading. Target >200 psi, ideally 500-1000 psi.
4. Methods: Tubing-conveyed perforating (TCP) with wellbore pre-evacuated. Cushion fluids (N2, light hydrocarbons) to reduce hydrostatic. Propellant charges to rapidly drop pressure post-perf.
5. Overbalanced Necessity: Sometimes required for well control (high pressure reservoirs, live oil), or when running wireline in deviated wells (need heavy fluid for tool weight). Creates 50-80% productivity loss vs underbalanced.
6. Extreme Overbalanced Perforating (EOP): INTENTIONALLY high overbalance (1000+ psi) to create deep micro-fractures radiating from perforation tunnel. Cracks bypass damage zone. Only works in brittle, low-stress formations. Rare application.
7. Flow Performance: Underbalanced perforations can have skin factor -2 to 0 (stimulation effect). Overbalanced perforations have skin +5 to +20 (severe damage). In low perm formations, this is the difference between commercial and non-commercial well.
        """,
        key_factors=[
            "Reservoir pressure and fluid type (gas vs oil)",
            "Wellbore fluid density (mud weight)",
            "Well control requirements (H2S, high pressure)",
            "Perforating method (TCP allows easier underbalance than wireline)",
            "Formation damage sensitivity (clay content, fines migration)",
            "Formation strength (EOP requires brittle rock)",
            "Cleanup flow rate potential (low perm may not surge effectively)",
            "Economic value of productivity improvement"
        ],
        primary_authority=[
            "API RP 19B Section 4: Underbalanced Perforating",
            "SPE 54673: Dynamic Underbalance—Measuring and Controlling the Pressure Transient",
            "SPE 25905: Perforation Cleanup and Formation Damage"
        ],
        burden_holder="Completion Engineer and Well Control Authority",
        adversary_position="Overbalanced perforating is safer and cheaper—damage can be mitigated with stimulation",
        counter_arguments=[
            "In very low permeability formations (k<0.01 mD), underbalance surge may be too weak to clean tunnels effectively",
            "Underbalanced TCP operations are more expensive (coiled tubing, N2 pumping, rig time) than wireline overbalanced",
            "Hydraulic fracturing will bypass near-wellbore damage anyway—underbalance is unnecessary cost in frac wells",
            "Well control risks in high-pressure reservoirs outweigh productivity benefits of underbalance"
        ],
        resolution_strategy="Evaluate well economics: In high-value, naturally producing wells (vertical conventional), underbalanced perforating ROI is excellent—can pay back in weeks. In unconventional frac wells, the fracture dominates flow—overbalanced is acceptable. In moderate perm formations (1-100 mD) without planned frac, underbalanced is strongly preferred. Always run nodal analysis with skin factors for overbalanced (+10) vs underbalanced (-1) to quantify production impact.",
        entity_scope="All perforating operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Underbalanced superiority is well-established by lab testing and field data for conventional completions. Debate exists for unconventional frac wells where some operators report no measurable difference.",
        controlling_precedent="API RP 19B Section 4 testing protocols",
        issue_category=IssueCategory.UNDERBALANCED_PERF,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.20
    ),

    DoctrineBlock(
        topic="API RP 19B Perforating Performance Testing",
        keywords=["API 19B", "concrete target", "API Section 1", "API Section 2", "penetration testing", "flow performance"],
        conclusion_template=[
            "API RP 19B Section 1 (surface performance in concrete) measures penetration depth and entry hole diameter under controlled conditions.",
            "API RP 19B Section 2 (flow performance testing) measures perforating system productivity using formation core samples at downhole stress and pressure.",
            "Section 1 results are used for charge selection; Section 2 results predict actual well productivity but are more expensive and less commonly performed."
        ],
        reasoning_framework="""
API RP 19B defines standardized testing to compare perforating systems:
1. Section 1 - Surface Performance: Shoot charges into concrete targets (4500 psi compressive strength, Berea sandstone strength analog). Measure penetration depth (inches), entry hole diameter (inches), and hole volume (cubic inches). Test at 2000 psi hydrostatic pressure, 250°F temperature. Results published by service companies—industry standard for charge comparisons.
2. Section 2 - Flow Performance: Shoot charges into actual formation core samples (Berea sandstone most common, or reservoir-specific core). Apply confining stress (3000-10000 psi) and pore pressure (1000-5000 psi) to simulate downhole conditions. Flow gas or fluid through perforations and measure productivity (flow rate vs drawdown). Calculate perforating skin factor. Much more representative of downhole performance but expensive ($50k-200k per test series).
3. Section 3 - Debris, Section 4 - Underbalance: Additional testing protocols less commonly performed.
4. Penetration Depth: In concrete, deep penetrating charges achieve 24-36 inches. Downhole penetration is typically 50-70% of API concrete penetration due to steel casing/cement/formation interfaces and crushed zone effects.
5. Flow Performance Metric: "Productivity ratio" = (perforated core flow) / (open hole core flow). Good perforating systems achieve 0.6-0.9. Poor systems (damaged, overbalanced) can be 0.1-0.3.
6. Limitations: API testing uses Berea sandstone (120 mD permeability, 6000 psi strength). Actual reservoirs range from 0.0001 mD shale to 5000 mD carbonate, 1000 psi to 40000 psi strength. Results are directional, not absolute predictions.
7. Industry Use: Section 1 data is universally available and used for charge selection. Section 2 data exists for major charge types but not all configurations. For critical applications (HPHT, expensive wells), operators may fund custom Section 2 testing with reservoir core.
        """,
        key_factors=[
            "Charge type and gun size selection",
            "Wellbore pressure during perforating (overbalanced vs underbalanced)",
            "Formation rock properties vs Berea sandstone analog",
            "Downhole temperature and pressure",
            "Cost-benefit of Section 2 testing ($50k-200k)",
            "Availability of reservoir core samples for testing",
            "Service company charge performance claims validation"
        ],
        primary_authority=[
            "API RP 19B: Recommended Practice for Evaluation of Well Perforators",
            "API RP 19B Section 1: Surface Performance Testing",
            "API RP 19B Section 2: Flow Performance Testing in Core"
        ],
        burden_holder="Perforating service company (provide test data)",
        adversary_position="API Section 1 concrete testing is sufficient—Section 2 is too expensive and not necessary",
        counter_arguments=[
            "Section 1 concrete tests don't account for formation damage, pore pressure effects, or realistic stress conditions",
            "Many operators successfully select charges based on Section 1 data alone without productivity issues",
            "Section 2 testing with Berea sandstone still doesn't match actual reservoir properties (especially shale or carbonate)",
            "Cost of Section 2 testing ($200k) exceeds value in most applications—only justified for mega-projects"
        ],
        resolution_strategy="Use API Section 1 data for routine charge selection—it provides good relative comparison between charge types. For high-value wells (>$10M completion cost, critical HPHT applications, novel charge systems), consider Section 2 testing with reservoir core if available. If reservoir core is unavailable, use Berea Section 2 data as directional guidance but apply 30-50% safety factor on predicted productivity.",
        entity_scope="All perforating charge selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 19B is the industry-standard testing protocol. Section 1 data reliability is high for penetration/entry hole. Section 2 productivity predictions are directional but not absolute due to formation variability.",
        controlling_precedent="API RP 19B testing standard",
        issue_category=IssueCategory.API_TESTING,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.15
    ),

    DoctrineBlock(
        topic="Tubing-Conveyed Perforating (TCP) vs Wireline Operations",
        keywords=["TCP", "tubing conveyed perforating", "wireline", "E-line", "conveyance", "operational risk"],
        conclusion_template=[
            "Tubing-conveyed perforating (TCP) runs guns on production tubing or coiled tubing, allowing controlled placement, underbalanced operations, and immediate flow testing.",
            "Wireline perforating uses electric line to convey guns—faster and cheaper but limited to near-vertical wellbores and typically requires overbalanced conditions.",
            "In horizontal wells and underbalanced applications, TCP is strongly preferred despite higher cost."
        ],
        reasoning_framework="""
Conveyance method affects operational execution, cost, and well performance:
1. Wireline Perforating: Electric line (E-line) with bridle weight runs guns downhole. Advantages: Fast rig-up (2-4 hours), low cost ($20k-50k), can log and perf in same run, proven technology. Limitations: Requires heavy fluid for tool weight (overbalanced), difficult in deviated wells (>60°), limited gun string length (200-400 ft), can't flow well immediately after perf (must pull tools first).
2. Tubing-Conveyed Perforating (TCP): Guns attached to production tubing or coiled tubing. Lower guns downhole with rig or CT unit, shoot, drop guns or blow guns off subs, immediately flow well. Advantages: Works in horizontal wells, enables underbalanced perforating, can test well immediately, unlimited gun string length. Disadvantages: Slower (8-24 hours operation), more expensive ($100k-300k), requires specialized equipment (blast joints, ported subs).
3. Horizontal Well Reality: Wireline cannot reliably reach TD in horizontal laterals >3000 ft. Friction and wellbore tortuosity cause tool to stop. TCP on coiled tubing is the only option for laterals >5000 ft.
4. Underbalanced Requirement: Wireline requires heavy fluid (12-16 ppg mud) to get tools to depth—inherently overbalanced. TCP allows wellbore to be evacuated or filled with light cushion fluid (N2, diesel) before shooting—achieves underbalance.
5. Immediate Flow Testing: TCP guns can be designed to drop off or blow apart after detonation. Well can flow immediately to test productivity and clean up perforations. Wireline requires pulling tools out (2-4 hours) before well can flow—perforations sit in stagnant mud during this time, increasing damage.
6. Gun Debris: TCP guns often have more debris (heavy tubing connection, larger OD guns). Wireline guns are smaller, less debris. However, TCP underbalance surge cleans debris; wireline overbalance pushes debris into formation.
7. Cost Trade-off: Wireline costs $30k-50k. TCP costs $150k-300k. But if TCP enables 20% higher productivity via underbalance, ROI is excellent in high-value wells.
        """,
        key_factors=[
            "Well trajectory (vertical vs horizontal)",
            "Lateral length (wireline limit ~3000 ft)",
            "Underbalance requirement for productivity",
            "Immediate flow testing needs",
            "Operational rig time availability",
            "Well control complexity (high pressure, H2S)",
            "Budget constraints",
            "Formation damage sensitivity"
        ],
        primary_authority=[
            "SPE 56634: Tubing-Conveyed Perforating—Technology and Applications",
            "SPE 28555: Comparison of Wireline and TCP Perforating",
            "Industry practice in unconventional completions"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Use wireline for all wells to minimize cost—productivity difference vs TCP is not worth the extra expense",
        counter_arguments=[
            "In vertical wells <10,000 ft with moderate productivity, wireline is the economic choice—TCP premium can't be justified",
            "Modern wireline tractor technology can reach 5000+ ft in horizontal wells (but at TCP-comparable cost)",
            "If well will be hydraulically fractured, the overbalanced perforation damage is irrelevant—fracture bypasses near-wellbore",
            "TCP operations have higher NPT risk (stuck pipe, gun misfire, tubing/coil damage)"
        ],
        resolution_strategy="Decision matrix: Vertical wells <60° deviation with no underbalance requirement → wireline. Horizontal wells >3000 ft lateral or requiring underbalance → TCP. Moderate deviation (60-75°) and short laterals (1000-3000 ft) → evaluate wireline tractor vs TCP cost-benefit. High-value wells where 10-20% productivity gain pays for TCP in <6 months → use TCP.",
        entity_scope="All perforating operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TCP vs wireline trade-offs are well-understood industry consensus. Wireline dominance in vertical wells, TCP dominance in horizontals is clear. Gray zone is moderate deviation wells where both are technically feasible.",
        controlling_precedent="Industry practice based on well trajectory and economics",
        issue_category=IssueCategory.TCP_OPERATIONS,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Perforation Friction Pressure Calculation",
        keywords=["perforation friction", "pressure drop", "friction calculation", "discharge coefficient", "hole area"],
        conclusion_template=[
            "Perforation friction pressure drop is calculated as ΔP = (ρQ²)/(2C²A²N) where ρ=fluid density, Q=flow rate, C=discharge coefficient, A=hole area, N=number of holes.",
            "Discharge coefficient C ranges from 0.6-0.95 depending on hole geometry, with 0.8 being typical for shaped charge perforations.",
            "Perforation erosion during fracturing can reduce friction by 50-75% as entry holes enlarge from 0.4\" to 1.0\" diameter."
        ],
        reasoning_framework="""
Perforation friction calculation is critical for limited entry design and frac modeling:
1. Basic Equation: ΔP = (ρQ²)/(2C²A²N) derived from Bernoulli with contraction/expansion losses. ρ = fluid density (lbm/ft³ or kg/m³), Q = volumetric flow rate (bpm or m³/s), C = discharge coefficient (dimensionless), A = hole area (in² or m²), N = number of holes.
2. Discharge Coefficient C: Represents flow efficiency through sharp-edged orifice. Perfect nozzle C=1.0. Sharp orifice C=0.61. Shaped charge perforations create rough, tapered holes with C=0.6-0.8. Higher C = lower friction (more efficient flow). Formation plugging or debris reduces C. API default is C=0.8 for clean perforations.
3. Hole Area A: For circular entry hole of diameter d (inches), A = π(d/2)². Deep penetrating charges: d=0.3-0.4 in, A=0.07-0.13 in². Big hole charges: d=0.5-0.7 in, A=0.20-0.38 in². Doubling hole diameter reduces friction by 4x (A² in denominator).
4. Number of Holes N: For cluster with L feet of perforations at S shots/ft, N=L*S. Example: 1 ft cluster, 6 SPF, N=6 holes. N appears linearly in denominator, but effective N is reduced by interference between closely-spaced holes.
5. Erosion During Frac: Proppant-laden fluid (1-2 ppg sand) erodes perforation tunnels. Entry holes grow from initial 0.4" to 0.7-1.0" over 30-60 minutes of pumping. Area increases 3-6x, friction drops to 15-30% of initial value. Limited entry effectiveness degrades over stage.
6. Rate Sensitivity: Friction ∝ Q². Doubling injection rate quadruples friction. At 40 bpm: ΔP=500 psi. At 80 bpm: ΔP=2000 psi. Non-linear response.
7. Typical Values: 6 holes/cluster, 0.4" diameter, 60 bpm slickwater (density 8.5 ppg, viscosity 1 cp), C=0.8 → ΔP ≈ 1200 psi. After erosion to 0.7" → ΔP ≈ 250 psi.
8. Software Tools: Most frac simulators (FracCADE, MFrac, GOHFER) have built-in perforation friction models with erosion. Can iterate on SPF and phasing to hit target friction.
        """,
        key_factors=[
            "Injection rate (bpm) and fluid density/viscosity",
            "Entry hole diameter (charge type selection)",
            "Shot density (SPF) and cluster length",
            "Discharge coefficient (hole quality, debris)",
            "Perforation erosion rate (proppant concentration, pumping duration)",
            "Multi-cluster interference effects",
            "Non-Darcy turbulent flow at very high rates",
            "Perforation tunnel length and tortuosity"
        ],
        primary_authority=[
            "SPE 174829: Perforation Friction Pressure Loss—State of the Art",
            "SPE 194357: Advanced Perforation Friction Modeling",
            "Petroleum Engineering Handbook Section on Perforating"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Perforation friction models are inaccurate due to erosion—don't rely on them for limited entry design",
        counter_arguments=[
            "Discharge coefficient C varies widely (0.6-0.95) based on hole quality—small changes dramatically affect calculated friction",
            "Erosion rate is highly variable depending on proppant type, concentration, fluid velocity—cannot be accurately predicted",
            "Multi-perforation interference effects in clusters mean effective N is less than actual hole count—equation is simplified",
            "Field pressure measurements often show 2-3x higher friction than calculated—suggests C values are too optimistic"
        ],
        resolution_strategy="Use perforation friction equation with conservative C=0.6-0.7 for initial design. Model erosion by reducing C or increasing hole diameter by 50-100% over stage duration. Validate with field pressure data from initial stages—adjust C to match observed friction. For critical limited entry designs, plan for 50% friction degradation and use chemical diverters as backup for late-stage diversion.",
        entity_scope="All fracturing operations with perforation clusters",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Basic friction equation is theoretically sound, but field application has high uncertainty due to discharge coefficient variability and erosion. Many operators report that calculated friction is 30-50% lower than measured field values.",
        controlling_precedent="SPE technical papers and frac simulator models",
        issue_category=IssueCategory.PERFORATION_FRICTION,
        authority_level=AuthorityLevel.SIMULATION,
        fragility_score=0.50
    ),

    DoctrineBlock(
        topic="Gun Debris Management and Wellbore Cleanout",
        keywords=["gun debris", "gun recovery", "wellbore cleanup", "charge debris", "gun steel", "brass liner"],
        conclusion_template=[
            "Gun debris from perforating includes charge liner material (brass/copper), gun body steel, bulkheads, and detonating cord—total 50-500 lbs depending on gun size and shot count.",
            "In horizontal wells, debris settles in low side of wellbore and can cause stuck pipe, screen plugging, or proppant bridging if not managed.",
            "Debris mitigation strategies include retrievable guns, dissolvable gun systems, underbalanced cleanup surge, and coiled tubing washout."
        ],
        reasoning_framework="""
Perforating creates substantial metallic debris that must be managed:
1. Debris Sources: Each shaped charge has brass or copper liner (20-100 grams). Gun carrier body is steel (10-200 lbs depending on size). Bulkheads, subs, detonating cord contribute additional mass. For a 60-ft gun string with 360 charges (6 SPF), total debris can be 200-400 lbs of metal fragments.
2. Debris Behavior: In vertical wells, debris falls to bottom—can be circulated out or left in sump. In horizontal wells, debris settles on low side of lateral. Forms ridges and piles that can bridge off wellbore (8-10" debris pile in 4.5" openhole). Subsequent trips with completion tools (plugs, frac sleeves) risk stuck pipe.
3. Retrievable Guns: TCP guns on tubing can be pulled back out of wellbore after shooting, removing bulk of gun body. Charge debris (liner material) remains. Common in casing gun operations.
4. Dissolvable Gun Systems: Gun carrier made of magnesium alloy or composite that dissolves in wellbore fluids over 2-48 hours. Eliminates gun body debris. Expensive ($500k-1M per well for full lateral). Used in critical applications where wellbore access is mandatory (multi-lateral wells, intelligent completions).
5. Underbalanced Cleanup: Dynamic underbalance surge can flush small debris fragments (charge liner, small gun pieces) out of perforation tunnels and up wellbore. Most effective in vertical wells with gas kick. Less effective for large gun body chunks in horizontal wells.
6. Coiled Tubing Washout: After perforating, run coiled tubing to TD and circulate debris out. Requires CT unit on location (adds $100k-300k cost). Standard practice in horizontal wells with debris concerns.
7. Through-Tubing Guns: Small OD guns (1.69"-2.125") that fit through production tubing. Gun body is much lighter (20-50 lbs total) than casing guns (200-500 lbs). Less debris but also lower performance (fewer shots, smaller charges).
8. Proppant Transport Risk: Large debris piles can cause proppant to bridge and screen out during fracturing. Coiled tubing cleanout before frac is often performed to mitigate this risk.
        """,
        key_factors=[
            "Well trajectory (vertical vs horizontal)",
            "Openhole vs cased hole perforating",
            "Gun size and shot count (debris volume)",
            "Subsequent wellbore access requirements (completion tools, workover)",
            "Budget for debris mitigation (CT cleanout, dissolvable guns)",
            "Underbalanced capability (debris flush)",
            "Proppant bridging risk during frac",
            "Screen/ICD plugging risk in sand control completions"
        ],
        primary_authority=[
            "SPE 184823: Gun Debris Management in Horizontal Wells",
            "SPE 174961: Dissolvable Perforating Gun Systems",
            "Industry practice in unconventional completions"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Gun debris is a non-issue—it settles harmlessly in wellbore and doesn't affect production",
        counter_arguments=[
            "Many horizontal wells are perforated and fractured without debris cleanup, with no reported issues",
            "Coiled tubing cleanout adds $200k-500k to well cost—economic benefit is unclear",
            "Dissolvable gun systems are very expensive and have reliability concerns (premature dissolution, incomplete dissolution)",
            "Underbalanced surge in horizontal wells is often ineffective at moving debris due to low flow velocity"
        ],
        resolution_strategy="Assess debris risk based on wellbore geometry and subsequent operations. In simple plug-and-perf horizontal wells with no further trips, debris can often be left in place—frac will compact it into low side. In wells requiring multiple trips (bridge plugs, completion tools, logging), consider CT cleanout or through-tubing guns to minimize debris. In multi-lateral or intelligent completions where wellbore access is critical, dissolvable guns may be justified despite cost.",
        entity_scope="All perforating operations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Debris concerns are real but economic impact is debated. Some operators routinely perform cleanout; others never do. Field data on stuck pipe frequency or productivity impact is limited and anecdotal.",
        controlling_precedent="Industry practice varies widely by operator and basin",
        issue_category=IssueCategory.GUN_DEBRIS,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE,
        fragility_score=0.55
    ),

    DoctrineBlock(
        topic="Oriented Perforating for Fracture Initiation",
        keywords=["oriented perforating", "phased perforating", "stress orientation", "SHmax", "fracture plane", "gyroscope"],
        conclusion_template=[
            "Oriented perforating uses gyroscope guidance to align perforation shots with maximum horizontal stress (SHmax) direction to promote easier fracture initiation.",
            "Shots fired perpendicular to SHmax (aligned with fracture plane) require 500-2000 psi lower breakdown pressure than randomly oriented perforations.",
            "Primary application is in formations with high stress anisotropy (SHmax - Shmin > 1000 psi) where fracture initiation is difficult."
        ],
        reasoning_framework="""
Oriented perforating optimizes shot placement relative to in-situ stress field:
1. Stress Field Basics: Earth has three principal stresses—vertical (Sv), max horizontal (SHmax), min horizontal (Shmin). In most sedimentary basins, Sv > SHmax > Shmin (normal faulting regime) or SHmax > Sv > Shmin (strike-slip regime). Hydraulic fractures initiate perpendicular to minimum stress and propagate in plane parallel to SHmax.
2. Random Perforating Problem: Standard spiral guns (60° or 120° phasing) shoot in all radial directions. Some shots align with SHmax (easy fracture initiation), some perpendicular to SHmax (hard initiation). Perforation clusters break down sequentially as pressure rises to overcome worst-oriented shots. Results in uneven breakdown, high treating pressure, potential screenout.
3. Oriented Solution: Use gyroscope (or magnetometer in vertical wells) to determine SHmax azimuth. Rotate gun string to align shots with SHmax direction. All perforations fire into optimal orientation. Fracture initiates at lower pressure with less tortuosity.
4. Pressure Reduction: In high-stress anisotropy formations (SHmax-Shmin = 1500 psi), oriented perforating can reduce breakdown pressure by 1000-2000 psi vs random. Lower treating pressure reduces surface equipment requirements and screenout risk.
5. Limited Entry Compatibility: Oriented perforating + limited entry is powerful combination. Align all clusters optimally, then use perforation friction to equalize flow. Achieves high cluster efficiency (70-90%) with minimal treating pressure.
6. Implementation: Wireline or TCP guns with orienting sub (gyro/magnetometer). Real-time surface readout shows gun orientation. Rotate string and verify alignment before firing. Adds 1-2 hours per stage. Common in Canada, less common in US unconventionals (operators accept higher breakdown pressure to save time).
7. Stress Determination: Requires knowing SHmax azimuth. Methods: Dipole sonic anisotropy, image log breakouts/drilling-induced fractures, microseismic from offset wells, regional stress maps. Uncertainty ±10-30°. In some basins, stress rotates 90° between formations—need accurate depth control.
8. Limitations: Only beneficial if stress anisotropy is high (>500 psi difference). In low-stress environments (Gulf Coast, some shales), random perforating performs nearly as well. Added time and cost may not be justified.
        """,
        key_factors=[
            "Stress anisotropy magnitude (SHmax - Shmin)",
            "SHmax azimuth determination accuracy",
            "Formation brittleness (fracture initiation difficulty)",
            "Treating pressure limitations (surface equipment, wellbore integrity)",
            "Operational time constraints (oriented perf adds time)",
            "Well trajectory relative to stress field",
            "Economic value of lower breakdown pressure",
            "Limited entry design integration"
        ],
        primary_authority=[
            "SPE 179117: Oriented Perforating—Impact on Fracture Initiation and Propagation",
            "SPE 168603: Perforation Orientation Effects in Horizontal Wells",
            "Canadian industry practice in Montney, Duvernay"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Random perforating works fine—oriented perf adds time and cost without measurable production benefit",
        counter_arguments=[
            "US unconventional operators rarely use oriented perforating—suggests marginal value in low-stress shales",
            "SHmax azimuth uncertainty (±20°) means oriented shots may not actually be optimally aligned",
            "Perforation erosion during frac means initial orientation becomes irrelevant after 10-20 minutes of pumping",
            "Field studies comparing oriented vs random show mixed results—some basins see benefit, others see none"
        ],
        resolution_strategy="Perform stress analysis: If SHmax-Shmin > 1000 psi and SHmax azimuth is well-constrained (±10°), oriented perforating is likely beneficial—model with frac simulator to quantify pressure reduction. If stress anisotropy is low (<500 psi) or SHmax is poorly known (±30°), skip oriented perforating—added cost exceeds benefit. Consider hybrid: Orient first stage as test, measure breakdown pressure improvement vs random perforations, then decide whether to orient remaining stages.",
        entity_scope="Horizontal well completions in moderate-to-high stress anisotropy formations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Oriented perforating theory is sound and supported by modeling. Field results are variable—strong evidence of benefit in some basins (Canada), weak evidence in others (Permian). Operator-specific practices vary widely.",
        controlling_precedent="Not standardized—operator and basin dependent",
        issue_category=IssueCategory.ORIENTED_PERF,
        authority_level=AuthorityLevel.FIELD_DATA,
        fragility_score=0.50
    ),

    DoctrineBlock(
        topic="Extreme Overbalanced Perforating (EOP)",
        keywords=["extreme overbalanced", "EOP", "microfractures", "deep penetrating fractures", "brittle rock"],
        conclusion_template=[
            "Extreme overbalanced perforating intentionally uses very high overbalance (1000-3000 psi) to create radial microfractures extending from perforation tunnels.",
            "Microfractures bypass near-wellbore damage zone and can increase productivity by 2-5x in brittle, low-stress formations.",
            "EOP is only effective in specific geological conditions—hard, brittle rock with low confining stress—and is rarely used in modern completions."
        ],
        reasoning_framework="""
EOP is counterintuitive approach that weaponizes overbalanced pressure:
1. Conventional Wisdom: Overbalanced perforating is bad—forces debris into formation, creates damage. Underbalanced is good—cleans tunnels. This is true for ductile formations (shales, soft sandstones).
2. EOP Concept: In very hard, brittle rock (high strength carbonate, cemented sandstone), extreme overbalance creates tensile hoop stress around perforation tunnel that exceeds rock tensile strength. Rock fractures radially, creating network of microfractures extending 6-12 inches from tunnel. These cracks bypass crushed zone damage and connect perforation to undamaged formation.
3. Pressure Requirement: Need overbalance >1000 psi, often 2000-3000 psi. At detonation, shaped charge creates cavity. Wellbore pressure hammers into cavity, generating stress pulse. If rock is brittle and confining stress is low, tensile failure occurs.
4. Formation Requirements: High compressive strength (>10,000 psi), low tensile strength (<1000 psi), brittle failure mode (not ductile), low confining stress (<5000 psi). Typical candidates: Austin Chalk, hard carbonates, cemented Paleozoic sandstones. Does NOT work in shale (too ductile) or high-stress formations (compressive stress prevents tensile failure).
5. Field Results: Limited published data. Some operators in Austin Chalk reported 3-5x productivity improvement vs underbalanced perforating in 1990s. Other operators saw no benefit. Difficult to isolate EOP effect from other completion variables.
6. Mechanism Uncertainty: Debate exists whether EOP actually creates deep fractures or just enlarges crushed zone. Core flow testing shows productivity improvement, but fracture extent is hard to verify. Some studies suggest "microfractures" are actually just enhanced permeability in crushed zone due to dilation.
7. Modern Application: Rare. Most operators use hydraulic fracturing for stimulation—EOP microfractures are tiny compared to frac. Only relevant in naturally fractured reservoirs where operators want to connect to natural fracture network without full hydraulic frac. Niche application.
        """,
        key_factors=[
            "Rock mechanical properties (compressive strength, brittleness)",
            "Confining stress magnitude (overburden, tectonic stress)",
            "Natural fracture network presence",
            "Wellbore pressure control capability (achieve high overbalance safely)",
            "Formation damage severity (EOP bypasses damage)",
            "Alternative stimulation options (hydraulic fracturing)",
            "Well control risk (high pressure)",
            "Economic value of productivity improvement"
        ],
        primary_authority=[
            "SPE 25905: Extreme Overbalance Perforating",
            "SPE 58793: EOP Field Study in Austin Chalk",
            "Limited field data from 1990s-2000s"
        ],
        burden_holder="Completion Engineer",
        adversary_position="EOP is unproven and risky—stick with underbalanced perforating or hydraulic fracturing",
        counter_arguments=[
            "EOP productivity improvements are poorly documented—most evidence is anecdotal or from single operators",
            "High overbalance creates well control risk and violates casing/cement integrity in some cases",
            "Hydraulic fracturing creates much larger fractures (100-1000 ft) vs EOP microfractures (0.5-1 ft)—EOP is obsolete",
            "EOP may work in specific formations (Austin Chalk) but is not transferable to other basins"
        ],
        resolution_strategy="EOP is a specialty technique for niche applications. Do NOT use in routine completions. Only consider if: (1) Formation is demonstrably brittle with high strength, (2) Natural fractures are present and stimulation goal is to connect to them, (3) Hydraulic fracturing is not planned or has failed in offset wells, (4) Operator has prior EOP experience in same formation. Otherwise, use underbalanced perforating or conventional fracturing.",
        entity_scope="Niche application in specific brittle, naturally fractured formations",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="EOP is poorly documented in peer-reviewed literature. Most knowledge is proprietary or anecdotal. Mechanism is theoretically plausible but not rigorously validated. High uncertainty.",
        controlling_precedent="No industry standard—operator-specific and formation-specific",
        issue_category=IssueCategory.OVERBALANCED_PERF,
        authority_level=AuthorityLevel.EXPERT_OPINION,
        fragility_score=0.75
    ),

    DoctrineBlock(
        topic="Cluster Efficiency in Plug-and-Perf Completions",
        keywords=["cluster efficiency", "perforation clusters", "fracture initiation", "uneven breakdown", "toe bias", "heel bias"],
        conclusion_template=[
            "Cluster efficiency is the percentage of perforation clusters that successfully initiate fractures and accept fluid during a frac stage.",
            "Poor cluster efficiency (30-50%) results in uneven stimulation—some clusters take all the fluid while others remain unstimulated, leaving significant reserves untapped.",
            "Achieving high cluster efficiency (70-90%) requires optimized perforation design (limited entry), proper cluster spacing, stress shadow management, and diversion systems."
        ],
        reasoning_framework="""
Cluster efficiency is critical metric for horizontal well completion quality:
1. Definition: In a stage with N clusters, if only M clusters initiate fractures, cluster efficiency = M/N * 100%. Perfect efficiency = 100% (all clusters frac). Typical field reality = 40-60% without optimization.
2. Measurement: Fiber optic DAS/DTS monitoring, tracer flowback analysis, production logging, microseismic mapping. Direct observation shows many clusters never break down or take minimal fluid.
3. Causes of Low Efficiency:
   a) Stress Shadows: First cluster to frac increases local stress in adjacent rock, making neighboring clusters harder to break down. Creates positive feedback—strong clusters get stronger, weak clusters stay shut.
   b) Perforation Friction Variation: Clusters with higher friction (fewer holes, debris, poor cleanup) divert flow to lower-friction clusters. Without proper limited entry design, low-friction clusters dominate.
   c) Formation Heterogeneity: Layers with different Young's modulus, stress, or permeability preferentially accept fluid. Clusters in "sweet spots" take all fluid.
   d) Heel Bias: In plug-and-perf, heel clusters are nearest to wellbore entry. Without sufficient perforation friction diversion, they take 70-80% of fluid.
4. Impact on Production: Low cluster efficiency means large portions of reservoir are unstimulated. A well with 30% cluster efficiency has 70% of its perforation clusters contributing little/no production. Ultimate recovery can be 30-50% lower than properly stimulated well.
5. Improvement Strategies:
   a) Limited Entry Design: 500-2000 psi perforation friction to equalize flow distribution.
   b) Cluster Spacing: Increase spacing from 15-20 ft to 30-50 ft to reduce stress shadow interference.
   c) Diverters: Degradable particles or fibers that temporarily plug high-flow clusters, forcing fluid to weak clusters.
   d) Oriented Perforating: Align all clusters optimally to reduce breakdown pressure variation.
   e) Reduced Cluster Count: Fewer clusters per stage (3-4 instead of 6-8) with more proppant per cluster. Less interference, higher efficiency.
6. Economics: Improving cluster efficiency from 50% to 80% can increase well EUR by 20-40%. Justifies significant completion design investment.
7. Trade-offs: High efficiency requires more complex (expensive) completion design. Some operators accept lower efficiency to minimize cost and operational time.
        """,
        key_factors=[
            "Perforation design (SPF, phasing, limited entry friction)",
            "Cluster spacing (stress shadow management)",
            "Formation mechanical properties (Young's modulus, stress contrast)",
            "Fluid design (viscosity, diverter selection)",
            "Injection rate and pressure (breakdown pressure uniformity)",
            "Wellbore trajectory relative to stress field",
            "Number of clusters per stage (fewer = higher efficiency)",
            "Completion cost tolerance (more complex design = higher cost)"
        ],
        primary_authority=[
            "SPE 189895: Cluster Efficiency in Unconventional Completions",
            "SPE 184873: Fiber Optic Diagnostics of Cluster Efficiency",
            "SPE 191407: Impact of Cluster Spacing on Fracture Geometry"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Cluster efficiency is overhyped—low efficiency is acceptable as long as total well productivity is economic",
        counter_arguments=[
            "Some operators achieve excellent well performance with 40-50% cluster efficiency—suggests efficiency is not the limiting factor",
            "Improving cluster efficiency from 50% to 80% may not translate to proportional production increase due to fracture overlap and reservoir depletion effects",
            "Diagnostic tools (fiber optic, tracers) are expensive ($200k-500k per well) and results are often ambiguous",
            "Simplified completions (high cluster count, no diverters) have lower NPT and faster drilling/completion times—economic advantage may outweigh efficiency gain"
        ],
        resolution_strategy="Establish baseline cluster efficiency using diagnostics (fiber optic DAS on 2-3 wells, or tracer analysis). If efficiency is <50%, investigate improvement: Model perforation friction and stress shadows to identify limiting factors. Test modifications (increased spacing, limited entry, diverters) on pilot wells with diagnostic monitoring. If efficiency improves to 70%+ and production increases, roll out to full development. If efficiency gains don't translate to production, accept simpler completion design.",
        entity_scope="Plug-and-perf horizontal well completions",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Cluster efficiency concept is well-established and supported by fiber optic data. However, direct correlation between efficiency and production is variable—some wells with low efficiency still perform well, others with high efficiency underperform. Formation quality may be more important than completion efficiency in many cases.",
        controlling_precedent="Active research area—no industry consensus on optimal efficiency target",
        issue_category=IssueCategory.CLUSTER_EFFICIENCY,
        authority_level=AuthorityLevel.FIELD_DATA,
        fragility_score=0.45
    ),

    DoctrineBlock(
        topic="Perforation Design for Hydraulic Fracturing",
        keywords=["frac perforation", "cluster spacing", "shots per cluster", "limited entry frac", "plug and perf"],
        conclusion_template=[
            "Optimal perforation design for plug-and-perf fracturing balances cluster count (reservoir contact) against cluster efficiency (uniform stimulation).",
            "Industry standard is 4-8 clusters per stage, 20-50 ft spacing, 6-10 shots per cluster in 60-degree phasing, targeting 1000-2000 psi perforation friction.",
            "Tighter cluster spacing (<20 ft) increases stress shadow interference; wider spacing (>50 ft) may leave unstimulated gaps."
        ],
        reasoning_framework="""
Perforation design directly controls fracture initiation and fluid distribution:
1. Cluster Count Trade-off: More clusters = more fractures = more reservoir contact (good). But more clusters = lower perforation friction = worse flow distribution = lower cluster efficiency (bad). Optimization balancing act.
2. Cluster Spacing: Determines stress shadow interference. Hydraulic fracture increases stress in surrounding rock (stress shadow). Adjacent fractures within ~50 ft interfere—closer fractures are harder to initiate and may not propagate independently. Spacing <20 ft: severe interference, low efficiency. Spacing 20-50 ft: moderate interference, acceptable. Spacing >50 ft: minimal interference, but may leave unstimulated zones between fractures.
3. Shots Per Cluster: Controls perforation friction (key to limited entry). 4-6 SPF = high friction (2000-4000 psi), strong diversion, but risks not breaking down if pressure limited. 8-10 SPF = moderate friction (800-1500 psi), balanced design. 12-16 SPF = low friction (200-500 psi), ensures breakdown but poor diversion, heel bias.
4. Phasing: 60-degree phasing is standard—balances perforation friction with fracture initiation reliability. 0-degree (all shots same plane) creates maximum friction but risks asymmetric breakdown. 120-degree reduces friction but often unnecessary.
5. Cluster Length: 0.5-2.0 ft typical. Shorter clusters (6 shots in 1 ft = 6 SPF) create point source for fracture. Longer clusters (12 shots in 2 ft = 6 SPF) distribute initiation over larger interval. Point source preferred for discrete fracture initiation.
6. Stage Length: 100-300 ft typical in unconventionals. Shorter stages (100-150 ft) with fewer clusters (3-4) achieve higher efficiency but require more plugs (higher cost, longer completion time). Longer stages (200-300 ft) with more clusters (6-8) are faster but lower efficiency.
7. Perforation Friction Target: 500 psi minimum (or diversion is negligible), 1000-2000 psi optimal (good diversion without excessive pressure), >3000 psi aggressive (may limit ability to place proppant). Design for 1500 psi at 70 bpm injection rate.
8. Erosion Planning: Perforation friction will drop 50-70% during stage due to erosion. Plan for degradation—use chemical/fiber diverters mid-stage to re-establish diversion after initial limited entry effect fades.
9. Field Validation: Measure treating pressure, step-down tests, fiber optic DAS to confirm clusters are breaking down uniformly. Adjust design for subsequent stages based on real-time data.
        """,
        key_factors=[
            "Formation properties (permeability, Young's modulus, stress)",
            "Reservoir depletion state (new well vs infill)",
            "Stage length and lateral length",
            "Fluid design (slickwater vs hybrid vs gel)",
            "Proppant loading per stage",
            "Surface pressure limitations",
            "Completion time and cost constraints",
            "Diagnostic monitoring availability (fiber optic, tracers)"
        ],
        primary_authority=[
            "SPE 184834: Limited Entry Design Optimization in Unconventional Reservoirs",
            "SPE 191407: Cluster Spacing Optimization",
            "SPE 189895: Perforation Strategy for Cluster Efficiency"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Use high SPF (12-16) and tight spacing (15-20 ft) to maximize reservoir contact—limited entry is overrated",
        counter_arguments=[
            "Some operators use 8 clusters/stage at 15 ft spacing with 12 SPF and achieve excellent production—suggests limited entry is not critical",
            "Tight spacing (<20 ft) is common in Permian Basin and many wells are economic—stress shadow concerns may be overstated",
            "Simplified designs (no limited entry, no diverters) reduce NPT and completion time—economic benefit exceeds efficiency loss",
            "Formation properties (rock quality, natural fractures) may be more important than completion design—good rock produces with any reasonable completion"
        ],
        resolution_strategy="Establish baseline design: 5-6 clusters per stage, 30-40 ft spacing, 6-8 SPF, 60° phasing. Model perforation friction—target 1200-1800 psi. Run initial stages and monitor with pressure diagnostics (step-down tests, treating pressure profile). If all clusters break down evenly, design is validated. If heel bias observed (pressure drops after first few clusters break down), increase friction (reduce SPF to 4-6) or add diverters. If multiple clusters fail to break down, reduce friction (increase SPF to 10-12) or reduce cluster count.",
        entity_scope="Plug-and-perf completions in unconventional horizontal wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Perforation design principles are well-established. Optimal parameters (cluster spacing, SPF, friction target) are basin-specific and operator-specific. Industry consensus exists on general ranges but not precise values.",
        controlling_precedent="Industry practice based on field trials and simulation",
        issue_category=IssueCategory.FRAC_OPTIMIZATION,
        authority_level=AuthorityLevel.INDUSTRY_PRACTICE,
        fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Casing Gun vs Through-Tubing Gun Selection",
        keywords=["casing gun", "through tubing gun", "gun size", "3-1/8 inch", "7 inch", "gun OD"],
        conclusion_template=[
            "Casing guns (3-1/8\" to 7\" OD) deliver maximum perforation performance but require wellbore intervention for deployment.",
            "Through-tubing guns (1.69\" to 2-1/8\" OD) fit through production tubing for workover operations but have reduced shot density and penetration.",
            "Gun size selection balances productivity requirements against operational constraints (wellbore access, tubing size, completion configuration)."
        ],
        reasoning_framework="""
Gun outer diameter determines charge size, shot count, and deployment method:
1. Casing Guns: Large OD (3-1/8\", 4\", 5\", 7\" common sizes). Run in openhole or through casing before tubing installation. Maximum performance—can fit larger charges (deeper penetration, bigger holes), higher shot density (up to 16-20 SPF). Heavy gun weight (200-500 lbs per 60 ft). Require wireline, coil tubing, or tubing-conveyed deployment. Cannot be run through installed tubing—wellbore must be empty or gun run on tubing string itself.
2. Through-Tubing Guns: Small OD (1.69\", 1.81\", 2-1/8\"). Fit through production tubing (2-7/8\", 3-1/2\", 4-1/2\" typical). Allow perforating without killing well or pulling tubing. Lower performance—smaller charges (12-20 inch penetration vs 24-36 inch), lower shot density (4-6 SPF max vs 12-16 SPF), smaller entry holes. Light weight (20-50 lbs). Primarily for workovers, reperforating, or tubing-deployed TCP in horizontal wells.
3. Performance Comparison: 7\" casing gun with 7\" big hole charges: 36\" penetration, 0.6\" entry holes, 12 SPF = 90 holes per 60 ft gun. 1.69\" through-tubing gun with 1.69\" deep penetrating charges: 14\" penetration, 0.28\" entry holes, 4 SPF = 24 holes per 60 ft. Productivity ratio: casing gun can be 3-5x better due to deeper penetration, more holes, and larger entry holes.
4. Application Decision Tree:
   - Initial completion, wellbore empty, maximum productivity required → Large casing gun (4-7\" OD)
   - Horizontal well TCP, need underbalanced, wellbore access after perf → Medium casing gun (3-1/8\" to 4\" OD) on coil tubing or tubing string
   - Workover, well producing, tubing in place, cannot kill well → Through-tubing gun (sized to tubing ID)
   - Vertical well, deviated <60°, cost-sensitive → Small casing gun (3-1/8\") on wireline
5. Horizontal Well Considerations: In long laterals (>5000 ft), even 3-1/8\" casing guns on wireline may not reach TD due to friction. Coiled tubing conveyance required. Some operators use 2-1/8\" through-tubing guns on CT to balance performance and deployment reliability.
6. Gun Loading: Larger guns hold more charges but require longer gun strings for same shot count. 7\" gun: 24 shots per 10 ft. 3-1/8\" gun: 6-12 shots per 10 ft. 1.69\" gun: 4 shots per 10 ft. Long gun strings (200-400 ft) are heavy, expensive, and have deployment risks (stuck guns, misfire).
        """,
        key_factors=[
            "Initial completion vs workover",
            "Tubing size and configuration",
            "Well trajectory (vertical vs horizontal)",
            "Productivity requirements (high-value vs marginal well)",
            "Wellbore access (can wellbore be emptied for large guns?)",
            "Deployment method (wireline, CT, tubing-conveyed)",
            "Gun string length required (shot count needed)",
            "Budget (large guns are more expensive)"
        ],
        primary_authority=[
            "API RP 19B: Gun size performance testing",
            "SPE 28555: Perforating Gun Selection Criteria",
            "Service company gun catalogs and specifications"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Use smallest gun that fits—large guns are unnecessary expense",
        counter_arguments=[
            "In formations with k>100 mD, perforation performance is less critical—even through-tubing guns deliver adequate productivity",
            "Horizontal well TCP with 3-1/8\" guns is significantly more expensive ($200k+) than wireline with 1.69\" guns ($50k)—economic benefit must justify cost",
            "Gun size selection has minimal impact in wells that will be hydraulically fractured—fracture performance dominates",
            "Smaller guns have lower debris volume and easier gun recovery/cleanup"
        ],
        resolution_strategy="Start with productivity requirement: Tight formations (k<1 mD) or high-value wells → maximize perforation performance with largest feasible gun (4-7\" casing guns). Moderate formations (1-100 mD) → 3-1/8\" to 4\" casing guns balance performance and cost. High-perm formations (k>100 mD) or workover applications → through-tubing guns acceptable. Validate with nodal analysis: Model production with different gun sizes (perforation skin effect). If 7\" gun increases NPV by >$500k vs 3-1/8\" gun (due to higher productivity), justify the larger gun. If production difference is <5%, use smaller gun to reduce cost.",
        entity_scope="All perforating operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gun size vs performance relationship is well-established by API testing. Economic optimization is operator-specific and depends on reservoir quality and well value.",
        controlling_precedent="API RP 19B specifications and service company design guides",
        issue_category=IssueCategory.GUN_SYSTEM,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.20
    ),

    DoctrineBlock(
        topic="Perforation Erosion During Hydraulic Fracturing",
        keywords=["perforation erosion", "hole enlargement", "proppant erosion", "washout", "friction degradation"],
        conclusion_template=[
            "Perforation holes erode during hydraulic fracturing due to high-velocity proppant-laden fluid flow, enlarging from initial 0.3-0.5\" diameter to 0.7-1.2\" over 30-90 minutes of pumping.",
            "Erosion reduces perforation friction by 50-80%, degrading limited entry effectiveness and causing heel bias to re-emerge late in treatment.",
            "Erosion rate depends on proppant concentration (ppg), proppant hardness (ceramic vs sand), fluid velocity, and rock strength around perforation tunnel."
        ],
        reasoning_framework="""
Perforation erosion is critical factor limiting limited entry effectiveness:
1. Erosion Mechanism: Hydraulic fracturing fluid carries proppant (sand or ceramic) at 0.5-2.5 ppg concentration. Fluid velocity through perforations is 50-200 ft/sec (very high). Proppant particles impact perforation tunnel walls at high kinetic energy, abrading rock and creating larger hole. Similar to sandblasting effect.
2. Hole Enlargement: Initial shaped charge perforation: 0.3-0.5\" diameter. After 10 minutes of pumping at 1.5 ppg sand: 0.5-0.7\". After 30-60 minutes: 0.7-1.0\". After full stage (90-120 min): 1.0-1.5\". Entry hole area increases 4-9x, perforation friction drops to 15-30% of initial value.
3. Limited Entry Degradation: Limited entry design relies on perforation friction to equalize flow. Initial friction might be 1500 psi (good diversion). After 30 minutes of erosion, friction drops to 400 psi (poor diversion). Heel clusters start taking more fluid again, toe clusters starve. Cluster efficiency degrades over the stage.
4. Erosion Rate Factors:
   a) Proppant Type: White sand (MOH hardness 7) erodes slower than ceramic proppant (MOH 8-9). Resin-coated sand is slightly less erosive.
   b) Proppant Concentration: Erosion rate ∝ concentration. 0.5 ppg = slow erosion. 2.0 ppg = fast erosion. Slickwater stages (low sand loading) erode less than hybrid/gel stages (high loading).
   c) Rock Strength: Soft formations (shale, poorly cemented sandstone) erode faster. Hard formations (carbonate, cemented sandstone) resist erosion but still erode significantly.
   d) Fluid Velocity: Higher injection rate = higher velocity = faster erosion. 60 bpm might cause 50% enlargement, 100 bpm might cause 80% enlargement in same time.
   e) Hole Geometry: Shaped charges create tapered tunnel—narrow at entry, wider inside. Erosion preferentially enlarges entry hole (highest velocity point).
5. Mitigation Strategies:
   a) Diverters: Add degradable fiber or particulate diverters mid-stage to re-establish flow balance after erosion degrades perforation friction.
   b) Stage Sequencing: Pump clean fluid (no proppant) for first 10-15 minutes to initiate all fractures with maximum perforation friction. Then add proppant—erosion occurs but fractures already initiated.
   c) Lower Proppant Concentration: Use 1.0 ppg average instead of 1.5-2.0 ppg. Slower erosion but less proppant placed (trade-off).
   d) Accept Erosion: Design for end-of-stage erosion state. Plan for low friction and rely on diverters for late-stage flow control.
6. Measurement: Difficult to measure in real-time. Post-stage caliper logs can show enlarged perforations. Perforation friction calculation from treating pressure (back-calculated) can show degradation trend. Fiber optic flow rate per cluster shows when diversion fails.
        """,
        key_factors=[
            "Proppant type and concentration (ppg)",
            "Injection rate and fluid velocity",
            "Pumping duration (stage time)",
            "Formation rock strength and erosion resistance",
            "Initial perforation size (small holes erode faster proportionally)",
            "Limited entry design sensitivity to friction variation",
            "Diverter system availability and timing",
            "Stage design (proppant ramp vs immediate loading)"
        ],
        primary_authority=[
            "SPE 189895: Perforation Erosion Effects on Cluster Efficiency",
            "SPE 184870: Real-Time Perforation Friction Analysis",
            "SPE 174838: Proppant Transport and Perforation Erosion"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Perforation erosion is inevitable and cannot be prevented—design completions that don't rely on perforation friction",
        counter_arguments=[
            "Erosion happens in all wells regardless of design—limited entry is fundamentally flawed due to erosion",
            "Diverter systems are more effective than trying to maintain perforation friction throughout stage",
            "High SPF designs (12-16 shots/cluster) start with low friction, so erosion has minimal impact on relative performance",
            "Field data on erosion rates is sparse—most claims are based on modeling, not measurement"
        ],
        resolution_strategy="Accept erosion as reality of hydraulic fracturing. Design limited entry for initial fracture initiation (first 10-20% of stage volume). Plan diverter system for mid/late-stage flow control after erosion degrades perforation friction. Monitor treating pressure and step-down tests throughout stage to detect when friction has degraded. Adjust diverter timing based on observed erosion rate. For critical wells, consider fiber optic DAS monitoring to measure real-time erosion impact on cluster flow distribution.",
        entity_scope="All hydraulic fracturing operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Perforation erosion is well-documented phenomenon. Magnitude and rate are variable and difficult to predict precisely. Impact on completion effectiveness is significant but can be mitigated with proper design.",
        controlling_precedent="Industry experience and modeling studies",
        issue_category=IssueCategory.PERFORATION_EROSION,
        authority_level=AuthorityLevel.FIELD_DATA,
        fragility_score=0.40
    ),

    DoctrineBlock(
        topic="Perforating in HPHT (High Pressure High Temperature) Environments",
        keywords=["HPHT", "high pressure", "high temperature", "deep well", "extreme conditions", "charge performance"],
        conclusion_template=[
            "HPHT perforating (pressure >15,000 psi, temperature >300°F) requires specialized charges, gun systems, and procedures to maintain performance and safety.",
            "Charge penetration decreases 10-30% at extreme temperatures (350-400°F) due to explosive degradation and liner material property changes.",
            "Gun system pressure ratings, detonation reliability, and conveyance methods must be validated for HPHT conditions to prevent failures."
        ],
        reasoning_framework="""
HPHT environments create unique challenges for perforating systems:
1. Temperature Effects on Charges:
   a) Explosive Degradation: Most shaped charge explosives (HMX, RDX-based) are rated to 350°F. Above 350°F, explosive can decompose, reducing detonation velocity and pressure. Penetration can drop 20-30%.
   b) Liner Material: Copper/brass liners change mechanical properties at high temperature (reduced yield strength, increased ductility). Jet formation is less coherent—shorter penetration, larger entry hole. At 400°F, penetration may be 70-80% of surface test values.
   c) Charge Case: Zinc or steel cases can fail structurally at >400°F. Require Inconel or stainless cases for extreme HPHT.
2. Pressure Effects:
   a) Gun Body: Standard gun carriers rated to 15,000-20,000 psi. HPHT wells (25,000-30,000 psi) require heavy-wall carriers (higher tensile steel, thicker walls). Weight increases 30-50%.
   b) Seals and Connections: O-rings, packoffs, electrical feedthroughs must be rated for pressure. Standard elastomers fail >20,000 psi or >300°F. HPHT guns use metal seals or specialized elastomers (AFLAS, Kalrez).
   c) Detonating Cord: Standard det cord can fail under extreme pressure differential. HPHT systems use armored det cord or dual-redundant initiators.
3. Detonation Reliability:
   a) Initiator Function: Electric detonators must fire reliably at high temperature. Standard EFI detonators rated to 350°F. HPHT wells may need thermal-barrier-protected initiators or shock tube systems.
   b) Sympathetic Detonation: High pressure can enhance shock wave transmission between charges—unintended sympathetic detonation risk. Gun design must account for this.
4. Conveyance Challenges:
   a) Wireline: Requires very heavy cable (for tool weight) and bridle in HPHT. Cable insulation degrades at >350°F. Temperature-rated cable (Teflon-jacketed) required but expensive and less reliable.
   b) Tubing-Conveyed: Preferred in HPHT. Allows precise depth control and eliminates cable temperature issues. But requires rig and more time.
5. Well Control: HPHT wells have extreme kick potential. Perforating creates communication with reservoir—if underbalanced, massive influx possible. Overbalanced perforating often mandatory for safety, despite productivity penalty.
6. Post-Perf Cleanup: HPHT reservoirs often have high flow potential. Underbalanced surge (if achieved) can be extremely violent—wellhead equipment must handle rates >50,000 bpm and potential debris surge.
7. Charge Selection: Use charges specifically tested at HPHT conditions (API Section 1 at 400°F, 25,000 psi). Standard room-temperature test data is not valid. Service companies offer "HPHT-rated" charges with modified explosive formulations and liner materials.
8. Field Procedures: Extended pre-job heating cycles to stabilize gun temperature. Minimize time at extreme temperature (run guns, shoot within 2 hours before heat soak degrades charges). Real-time monitoring of gun pressure/temperature during run-in.
        """,
        key_factors=[
            "Wellbore pressure and temperature magnitude",
            "Explosive temperature rating (degradation threshold)",
            "Gun carrier pressure rating and material",
            "Detonator reliability at temperature",
            "Conveyance method capability (wireline vs TCP)",
            "Well control requirements and risks",
            "Charge performance testing at HPHT conditions",
            "Regulatory requirements for HPHT operations",
            "Cost of HPHT-rated equipment (2-3x standard)"
        ],
        primary_authority=[
            "API RP 19B Section 1: Testing at elevated pressure and temperature",
            "SPE 166506: HPHT Perforating Challenges and Solutions",
            "Service company HPHT charge specifications and field procedures"
        ],
        burden_holder="Completion Engineer and Service Company",
        adversary_position="Use standard charges and guns—HPHT degradation is overstated by service companies to sell expensive systems",
        counter_arguments=[
            "Many HPHT wells have been perforated with standard equipment without failures—suggests HPHT-rated systems are over-engineered",
            "Cost premium for HPHT charges and guns (200-300% vs standard) often cannot be justified economically",
            "Penetration reduction at high temperature (10-20%) is within normal variability and may not affect productivity",
            "Overbalanced perforating (required for well control) creates so much damage that charge performance becomes secondary"
        ],
        resolution_strategy="Classify well severity: Moderate HPHT (15,000-20,000 psi, 300-350°F) → use standard charges with thermal protection and heavy-wall guns. Extreme HPHT (>20,000 psi or >350°F) → HPHT-rated charges, guns, and procedures mandatory. Validate all equipment ratings against actual downhole conditions (don't assume service company specs are conservative). For critical/expensive wells (>$50M), fund pre-job HPHT performance testing (shoot charges in pressure vessel at actual P/T) to confirm penetration. Use TCP for depth control and well control management—wireline in HPHT is high-risk.",
        entity_scope="Deep, high-pressure, high-temperature wells (typically >15,000 ft, >300°F)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="HPHT effects on perforating are well-documented. Equipment ratings and procedures are established. Economic trade-offs (HPHT system cost vs risk mitigation) are debated—some operators use HPHT systems routinely, others push standard equipment to limits.",
        controlling_precedent="API RP 19B testing standards and regulatory requirements (state/federal well control rules)",
        issue_category=IssueCategory.HPHT_OPERATIONS,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.30
    ),

    DoctrineBlock(
        topic="Propellant-Assisted Perforating Systems",
        keywords=["propellant", "perforating propellant", "pressure surge", "dynamic underbalance", "energized perforating"],
        conclusion_template=[
            "Propellant perforating uses solid propellant charges that burn after perforation to rapidly reduce wellbore pressure, creating dynamic underbalance for perforation cleanup.",
            "Propellant systems can achieve 2000-5000 psi underbalance in 1-5 seconds, providing superior cleanup compared to conventional underbalanced perforating.",
            "Applications include tight formations where conventional underbalance cannot generate sufficient surge, and wells where tubing evacuation is not feasible."
        ],
        reasoning_framework="""
Propellant systems create extreme dynamic underbalance through controlled gas generation:
1. Operating Principle: After shaped charges detonate and create perforation tunnels, solid propellant charges ignite and burn. Propellant combustion generates large volume of gas (CO2, N2, H2O vapor) in sealed wellbore. Gas rapidly expands, displacing wellbore fluid upward and dropping bottomhole pressure. Creates sudden, large underbalance (2000-5000 psi in 1-5 seconds). Reservoir fluid surges into wellbore, flushing perforation debris.
2. Propellant Types:
   a) Fast-Burn: Ignite immediately after perforation, reach peak pressure in 1-3 seconds. High-intensity surge, short duration (5-10 seconds). Used for aggressive cleanup in moderate permeability.
   b) Slow-Burn: Ignite 5-10 seconds after perforation, burn over 15-30 seconds. Lower peak pressure but sustained surge. Used in low-permeability formations where reservoir needs time to respond.
3. Pressure Dynamics: Propellant generates 10,000-20,000 psi surface pressure initially (sealed wellbore, gas expansion). Then rapid vent (burst disk or controlled bleed-off) drops pressure below reservoir pressure. Swing from high overbalance to high underbalance in <10 seconds. Creates massive flow transient.
4. Cleanup Effectiveness: Propellant surge velocity can be 10-50x higher than conventional underbalanced perforating. Can remove debris, mud cake, and even partial formation damage. Field studies show 2-5x productivity improvement vs conventional underbalanced in tight formations.
5. Applications:
   a) Tight Gas/Oil: k<1 mD formations where conventional underbalance cannot generate strong surge flow. Propellant creates artificial surge even in low-perm rock.
   b) Deepwater: Cannot evacuate wellbore (extreme hydrostatic). Propellant achieves underbalance without fluid removal.
   c) Wells with Tubing: Tubing-conveyed propellant guns allow underbalance in completed wells without killing well or pulling tubing.
6. Risks and Limitations:
   a) Wellhead Pressure: Propellant generates surface pressure spike (can be 10,000-15,000 psi). Wellhead equipment must be rated and pressure control system (burst disk, choke) must be properly sized.
   b) Debris Surge: Violent cleanup can bring large debris volumes (gun parts, formation sand) to surface rapidly. Flowback equipment must handle solids.
   c) Formation Damage: High overbalance during propellant burn can fracture weak formations or push fluids into formation (opposite of desired effect). Requires careful modeling.
   d) H2S/CO2: Propellant combustion can generate H2S or CO2 depending on formulation. Sour gas hazard in confined spaces.
7. System Components: Shaped charge guns + propellant chambers + pressure relief system (burst disk or bleed valve) + firing electronics (timed delay between charge detonation and propellant ignition). Entire system is expendable—dropped or blown apart after use.
8. Cost: Propellant systems cost 50-150% more than conventional TCP due to specialized propellant charges and pressure control equipment. Justified in high-value wells where productivity improvement pays for itself.
        """,
        key_factors=[
            "Formation permeability (tight formations benefit most)",
            "Wellhead pressure rating and pressure control equipment",
            "Well completion configuration (open hole, cased hole, tubing)",
            "Ability to evacuate wellbore (deepwater wells cannot)",
            "Formation strength (weak formations may fracture during propellant burn)",
            "Economic value of productivity improvement",
            "Regulatory approvals (propellant systems require permits in some jurisdictions)",
            "Surface safety equipment (debris handling, H2S monitoring)"
        ],
        primary_authority=[
            "SPE 73337: Propellant Perforating Systems Performance",
            "SPE 94280: Dynamic Underbalance with Propellant Fracturing",
            "Service company propellant system specifications (Owen/Baker Hughes/Schlumberger)"
        ],
        burden_holder="Completion Engineer and Service Company",
        adversary_position="Propellant systems are dangerous and expensive—conventional underbalanced perforating is sufficient",
        counter_arguments=[
            "Propellant surface pressure spikes (10,000+ psi) create well control and equipment risks that may not be justified",
            "Field data on productivity improvement is limited—many claims are from service company case studies, not independent peer review",
            "In very tight formations (k<0.01 mD), even propellant surge may be ineffective because reservoir cannot respond fast enough",
            "Hydraulic fracturing will bypass near-wellbore damage anyway—propellant cleanup is unnecessary in frac wells"
        ],
        resolution_strategy="Evaluate formation properties and completion type: Tight formations (k<1 mD) without planned hydraulic frac → propellant perforating strong candidate. Model expected productivity improvement (skin effect -5 to -2 vs +10 overbalanced). If NPV increase >$1M, propellant system ROI is excellent. Ensure wellhead equipment is rated for propellant pressure and surface safety systems are in place (debris separation, H2S detection). In unconventional frac wells, propellant systems are likely not justified—fracture dominates performance.",
        entity_scope="Tight formations, deepwater wells, high-value wells where productivity is critical",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Propellant perforating has strong theoretical basis and some field validation. However, field data is sparse and often from service company sources. Long-term productivity comparisons (propellant vs conventional) are limited. Technology is proven but not universally adopted, suggesting economic benefit is marginal in many applications.",
        controlling_precedent="Not standardized—service company proprietary systems",
        issue_category=IssueCategory.PROPELLANT_SYSTEMS,
        authority_level=AuthorityLevel.VENDOR_SPEC,
        fragility_score=0.60
    ),

    DoctrineBlock(
        topic="Abrasive Jetting as Perforating Alternative",
        keywords=["abrasive jetting", "hydrajetting", "jet perforating", "coiled tubing jetting", "sand jetting"],
        conclusion_template=[
            "Abrasive jetting uses high-pressure fluid mixed with abrasive particles (sand/ceramic) ejected through nozzles to erode holes in casing and formation.",
            "Jetting creates 0.25-0.75 inch diameter holes with 6-24 inch penetration depending on formation hardness, pump pressure (5000-10,000 psi), and jetting time.",
            "Advantages over shaped charges: no explosives (safer in high-H2S or spark-risk environments), can jet and frac in single trip, unlimited hole count. Disadvantages: slower, less penetration, requires CT unit."
        ],
        reasoning_framework="""
Abrasive jetting is non-explosive alternative to shaped charge perforating:
1. Operating Principle: Coiled tubing with jetting tool (nozzle assembly) is positioned at target depth. High-pressure pump (5,000-10,000 psi) circulates fluid through CT. Abrasive particles (sand 20/40 mesh or ceramic) are injected into fluid stream. Fluid+abrasive mixture exits nozzles at 200-400 ft/sec velocity. Abrasive impacts casing/cement/rock and erodes material, creating hole. Continue jetting until desired penetration achieved (typically 5-30 minutes per hole).
2. Hole Characteristics: Diameter 0.25-0.75 inches (smaller than shaped charges). Penetration 6-24 inches in sandstone/shale (less than shaped charges which achieve 24-36 inches). Hole shape is tapered/conical (not cylindrical like shaped charges). Surface finish is rough/eroded.
3. Performance Factors:
   a) Formation Hardness: Soft formations (unconsolidated sand, soft shale) jet quickly (10-20 inches in 5 minutes). Hard formations (carbonate, cemented sandstone) jet slowly (6-12 inches in 30 minutes). Extremely hard rock (granite, chert) may not jet effectively.
   b) Pump Pressure: Higher pressure = higher abrasive velocity = faster erosion. 5,000 psi typical, 8,000-10,000 psi for hard formations. Limited by CT and surface equipment ratings.
   c) Abrasive Type: Sand (quartz, MOH hardness 7) is cheap and effective in most formations. Ceramic abrasive (MOH 9) is faster in hard rock but expensive. Size: 20/40 or 40/70 mesh typical.
   d) Nozzle Configuration: Single nozzle = one hole. Oriented multi-nozzle tools can jet 2-6 holes simultaneously in radial pattern (phasing). Rotating nozzle can create spiral pattern (like shaped charge spiral guns).
4. Advantages:
   a) No Explosives: Safe in H2S environments (no spark/detonation risk), restricted areas, near platforms/infrastructure.
   b) Unlimited Holes: Can jet as many holes as needed (100+ per stage). Not limited by gun length or charge count.
   c) Jet-and-Frac: After jetting holes, can immediately pump frac without tripping out. Single-trip operation saves rig time (8-24 hours) vs perf-and-frac with gun retrieval.
   d) Selective Placement: Can jet specific intervals based on real-time logs (gamma, temperature, production logs). Can avoid thief zones or water zones.
5. Disadvantages:
   a) Slower: Jetting 60 holes takes 2-6 hours vs 1-second detonation for shaped charges.
   b) Less Penetration: 6-24 inches vs 24-36 inches for shaped charges. May not bypass damage zone effectively in tight formations.
   c) Requires CT Unit: Cannot jet with wireline. CT spread costs $50k-200k, adds operational complexity.
   d) Flow Performance: Rough, tapered holes have lower flow efficiency (higher perforation friction) than clean shaped charge holes. Discharge coefficient C~0.5 vs 0.8 for shaped charges.
6. Applications: Most common in horizontal unconventional completions as alternative to plug-and-perf. Jet holes, drop frac plug, frac stage—then move to next interval. Saves one trip. Also used in live H2S wells (Permian Basin, Scoop/Stack), near-platform operations (offshore), and wells where explosives permits are difficult.
7. Industry Adoption: Growing in US unconventionals (Eagle Ford, Permian) as operators seek to reduce completion time. Still minority of wells (<10%) compared to shaped charge plug-and-perf. Not widely adopted in vertical wells or conventional completions where wireline shaped charges are faster and cheaper.
        """,
        key_factors=[
            "Formation hardness (soft formations jet easily)",
            "Completion time constraints (jetting is slower)",
            "H2S or explosive restrictions",
            "Availability of CT unit and high-pressure pumps",
            "Economics (CT jetting can save one trip vs plug-and-perf)",
            "Penetration requirements (bypass damage zone)",
            "Hole count needed (jetting has no limit)",
            "Frac design compatibility (jet-and-frac single trip)"
        ],
        primary_authority=[
            "SPE 179117: Abrasive Jetting for Horizontal Well Completions",
            "SPE 184850: Comparison of Jetting vs Perforating Productivity",
            "Service company jetting system specifications (NCS, Archer, Packers Plus)"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Shaped charge perforating is faster and proven—abrasive jetting is unproven technology with limited field data",
        counter_arguments=[
            "Shaped charge perforating is 10-50x faster than jetting—time savings justify sticking with proven technology",
            "Jetting penetration (6-24 inches) may not adequately bypass near-wellbore damage in tight formations",
            "Jetting productivity is questionable—rough holes with high friction may offset any benefit of unlimited hole count",
            "CT jetting requires specialized equipment and trained crews—operational risks and logistics are higher than wireline perforating"
        ],
        resolution_strategy="Evaluate jetting vs shaped charges on case-by-case basis: In H2S environments or explosive-restricted areas, jetting is the only option—productivity trade-off is necessary for safety. In horizontal unconventional completions with planned plug-and-perf, model economics of jet-and-frac single-trip vs perf-then-frac two-trip. If jetting saves 12+ hours rig time per well (12 hours @ $30k/hr = $360k), jet-and-frac may be economic even if productivity is 10-20% lower. In vertical wells or conventional completions, shaped charges are faster and cheaper—jetting is not justified.",
        entity_scope="Horizontal unconventional completions, H2S wells, explosive-restricted areas",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Abrasive jetting is proven technology with growing adoption. However, long-term productivity comparisons vs shaped charges are limited. Most field data is from service companies or single-operator studies. Industry has not broadly adopted jetting as replacement for shaped charges, suggesting economic/performance benefits are marginal in most applications.",
        controlling_precedent="Not standardized—operator and service company specific",
        issue_category=IssueCategory.ABRASIVE_JETTING,
        authority_level=AuthorityLevel.FIELD_DATA,
        fragility_score=0.55
    ),

    DoctrineBlock(
        topic="Gun Loading and Safety Procedures",
        keywords=["gun loading", "perforating safety", "charge handling", "detonation risk", "gun assembly", "explosive storage"],
        conclusion_template=[
            "Perforating gun loading and handling requires strict adherence to explosive safety protocols to prevent premature detonation, personnel injury, or equipment damage.",
            "Primary hazards include: stray electrical current (initiator firing), static discharge, mechanical shock (dropping guns), and fire/heat exposure.",
            "Industry standards (API RP 67, OSHA explosives regulations, state explosive permits) mandate training, equipment grounding, restricted areas, and emergency procedures."
        ],
        reasoning_framework="""
Perforating operations involve Class A explosives—safety is paramount:
1. Explosive Classification: Shaped charges and detonating cord are Class 1.1D explosives (mass detonation hazard). Subject to federal regulations (ATF, DOT, OSHA) and state explosive permits. Transportation, storage, and handling require licensed personnel and permitted facilities.
2. Gun Loading Hazards:
   a) Electrical Initiation: Electric detonators (EFI) fire with <1 amp current at 50-250 volts. Stray current from radio transmitters, welding equipment, lightning, or static discharge can cause premature firing. During loading, all electrical sources must be isolated and guns grounded.
   b) Shock Sensitivity: Shaped charges can detonate if dropped >10 feet onto hard surface. Detonating cord is less shock-sensitive but still hazardous. Handling procedures require soft surfaces, no dropping, padded transport.
   c) Heat Sensitivity: Charges rated to 350-400°F storage. Prolonged exposure to >400°F or open flame can cause cook-off (uncontrolled detonation). Storage magazines must be climate-controlled in hot climates.
   d) Sympathetic Detonation: One charge detonating can trigger adjacent charges even without detonating cord connection. Minimum 6-12 inch spacing required during assembly. Charges stored in separate containers until final assembly.
3. Loading Procedures (Industry Standard):
   a) Restricted Area: Establish 200-500 ft explosive exclusion zone. No smoking, welding, radio transmitters, cell phones, vehicles (except explosive truck). Posted signage and barriers.
   b) Grounding: Gun carrier, loading bench, personnel (wrist straps) all bonded to ground grid. Prevents static buildup. Test ground resistance <10 ohms before starting.
   c) Charge Inspection: Visually inspect every charge for damage (cracks, deformed liner, loose components). Damaged charges are rejected—never use.
   d) Sequential Loading: Load charges one at a time onto gun carrier. Attach retainers/bulkheads. Connect detonating cord. Do NOT connect initiator until all charges loaded and gun ready for deployment.
   e) Initiator Connection: Last step before running gun downhole. Use shorting plugs on initiator leads until final connection to surface panel. Test firing circuit continuity with blasting ohm-meter (max 50 mA current—too low to fire detonator).
   f) Transport: Loaded guns transported in explosive truck (DOT Class 1.1 placard) with grounded gun rack. No guns on personnel vehicles.
4. Storage Requirements: Explosives stored in Type 1 or Type 2 magazine (steel/concrete, bullet-resistant, locked, climate-controlled). Quantity limits per magazine based on ATF regulations. Inventory tracking with chain-of-custody logs. Magazines located >300 ft from occupied buildings, >100 ft from roads/property lines.
5. Personnel Qualifications: Gun loaders must have explosive handler certification (state-issued, requires training and background check). Perforating supervisors must have blaster license. Minimum two trained personnel present during loading operations.
6. Emergency Procedures: If misfire (gun fails to detonate downhole), wait 30 minutes minimum before attempting retrieval (residual current may cause delayed firing). If gun fire while on surface (dropped gun, electrical fault), evacuate 500 ft radius, contact fire/police, follow explosive incident protocol.
7. Regulatory Compliance: OSHA 29 CFR 1910.109 (explosives storage/handling), ATF 27 CFR 555 (commerce in explosives), DOT 49 CFR 177 (explosive transportation), State explosive permits (Texas, Louisiana, etc. require permits for perforating operations).
8. Insurance and Liability: Perforating service company must carry explosive operations insurance ($5M-50M limits). Operator typically requires proof of insurance before allowing guns on location. Service company assumes liability for explosive incidents during loading/transport/deployment.
        """,
        key_factors=[
            "Personnel training and certification (explosive handlers)",
            "Grounding system adequacy (electrical safety)",
            "Restricted area enforcement (distance, barriers)",
            "Charge inspection quality control",
            "Detonator handling procedures (shorting plugs, ohm-meter testing)",
            "Magazine storage compliance (ATF/OSHA regulations)",
            "Emergency response plan (misfire, surface detonation)",
            "Regulatory permits (state explosive permits, county approvals)",
            "Insurance coverage (explosive operations liability)"
        ],
        primary_authority=[
            "API RP 67: Recommended Practice for Oilfield Explosives Safety",
            "OSHA 29 CFR 1910.109: Explosives and Blasting Agents",
            "ATF 27 CFR 555: Commerce in Explosives",
            "DOT 49 CFR 177: Carriage by Public Highway (Explosives)"
        ],
        burden_holder="Perforating Service Company and On-Site Supervisor",
        adversary_position="Perforating safety procedures are overly conservative—experienced crews can safely cut corners to save time",
        counter_arguments=[
            "Industry has excellent safety record—incidents are extremely rare, suggesting current procedures may be excessive",
            "Grounding and electrical isolation procedures add 1-2 hours to gun loading—time cost is significant",
            "Many regulations are decades old and don't reflect modern safer initiator designs (electronically-safe detonators)",
            "Restricted area requirements (200-500 ft) are impractical on crowded well pads—often ignored in practice"
        ],
        resolution_strategy="Zero tolerance for safety shortcuts. Perforating safety record is excellent BECAUSE procedures are strictly followed. One incident (surface detonation injuring personnel) can cost $10M-100M in liability, shutdown entire operation, and destroy company reputation. Economic benefit of saving 1-2 hours is insignificant compared to risk. Enforce API RP 67 and OSHA requirements fully. Conduct pre-job safety briefing with all personnel. Verify grounding system with ohm-meter before every loading operation. Maintain detailed explosive inventory and chain-of-custody logs. Ensure all personnel have current explosive handler certifications. Conduct annual safety audits with third-party explosive safety experts.",
        entity_scope="All perforating operations involving explosives",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Perforating safety standards (API RP 67, OSHA) are well-established and based on decades of industry experience and regulatory development. Compliance is mandatory and universally accepted. No reasonable debate exists on safety requirement adequacy—only on enforcement rigor.",
        controlling_precedent="API RP 67, OSHA 29 CFR 1910.109, ATF/DOT regulations, state explosive laws",
        issue_category=IssueCategory.SAFETY,
        authority_level=AuthorityLevel.API_STANDARD,
        fragility_score=0.10
    ),
]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class EngineMetrics:
    def __init__(self):
        self.queries_total = 0
        self.queries_by_mode = defaultdict(int)
        self.queries_by_category = defaultdict(int)
        self.doctrines_triggered = defaultdict(int)
        self.avg_response_time_ms = 0.0
        self.cache_hit_rate = 0.0
        self.start_time = time.time()

    def record_query(self, mode: ResponseMode, categories: List[IssueCategory],
                     doctrines: List[str], response_time_ms: float):
        self.queries_total += 1
        self.queries_by_mode[mode.value] += 1
        for cat in categories:
            self.queries_by_category[cat.value] += 1
        for doctrine in doctrines:
            self.doctrines_triggered[doctrine] += 1

        # Update rolling average response time
        self.avg_response_time_ms = (
            (self.avg_response_time_ms * (self.queries_total - 1) + response_time_ms)
            / self.queries_total
        )

    def get_summary(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "queries_total": self.queries_total,
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_category": dict(self.queries_by_category),
            "top_doctrines": dict(sorted(
                self.doctrines_triggered.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]),
            "avg_response_time_ms": round(self.avg_response_time_ms, 2),
            "uptime_seconds": round(uptime, 2)
        }


METRICS = EngineMetrics()


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class PerforationEngine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.drift_detected = []
        self.coverage_gaps = []
        logger.info(f"Initialized {ENGINE_ID} with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, question: str, mode: ResponseMode,
                            zone: AnalysisZone) -> Tuple[str, List[str], ConfidenceLevel]:
        """
        TIE-20 Component 1: Three-layer response architecture
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (if needed)
        Layer 3: Deep analysis (MEMO mode)
        """
        start_time = time.time()

        # Layer 1: Doctrine Cache Lookup
        triggered_doctrines = self._search_doctrine_cache(question)

        if triggered_doctrines:
            answer = self._synthesize_from_doctrines(
                triggered_doctrines, question, mode, zone
            )
            confidence = self._assess_confidence(triggered_doctrines)
            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines, {elapsed_ms:.1f}ms")
            return answer, [d.topic for d in triggered_doctrines], confidence

        # Layer 2: Semantic fallback (not implemented - would call vector DB)
        logger.warning("No doctrine cache hits - returning disclosure response")
        return self._disclosure_response(question), [], ConfidenceLevel.DISCLOSURE

    def _search_doctrine_cache(self, question: str) -> List[DoctrineBlock]:
        """Search doctrine cache using keyword matching"""
        question_lower = question.lower()
        question_terms = set(question_lower.split())

        matches = []
        for doctrine in self.doctrines:
            # Check keyword overlap
            keyword_hits = sum(1 for kw in doctrine.keywords if kw.lower() in question_lower)
            if keyword_hits >= 2:  # Require at least 2 keyword matches
                matches.append((doctrine, keyword_hits))

        # Sort by keyword hits and return top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in matches[:5]]  # Return top 5 matches

    def _synthesize_from_doctrines(self, doctrines: List[DoctrineBlock],
                                   question: str, mode: ResponseMode,
                                   zone: AnalysisZone) -> str:
        """Synthesize answer from triggered doctrines based on response mode"""

        if mode == ResponseMode.FAST:
            # Concise response - just conclusions
            parts = []
            for doc in doctrines[:2]:  # Limit to 2 doctrines for brevity
                parts.append(f"**{doc.topic}**: {doc.conclusion_template[0]}")
            return "\n\n".join(parts)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authority citations
            parts = [f"## Perforation Design Analysis: {question}\n"]
            for doc in doctrines:
                parts.append(f"### {doc.topic}")
                parts.append(f"**Conclusion**: {' '.join(doc.conclusion_template)}")
                parts.append(f"\n**Key Factors**: {', '.join(doc.key_factors[:5])}")
                parts.append(f"\n**Authority**: {'; '.join(doc.primary_authority)}")
                parts.append(f"\n**Confidence**: {doc.confidence.value}")
                if doc.counter_arguments:
                    parts.append(f"\n**Counter-Arguments**: {'; '.join(doc.counter_arguments[:3])}")
                parts.append("")
            return "\n".join(parts)

        else:  # MEMO mode
            # Full documentation with reasoning
            parts = [f"# Perforation Design Memorandum: {question}\n"]
            parts.append(f"**Analysis Zone**: {zone.value}")
            parts.append(f"**Doctrines Applied**: {len(doctrines)}\n")

            for idx, doc in enumerate(doctrines, 1):
                parts.append(f"## {idx}. {doc.topic}")
                parts.append(f"**Issue Category**: {doc.issue_category.value}")
                parts.append(f"**Authority Level**: {doc.authority_level.value}")
                parts.append(f"\n### Conclusion")
                parts.append('\n'.join(f"- {c}" for c in doc.conclusion_template))
                parts.append(f"\n### Reasoning Framework")
                parts.append(doc.reasoning_framework)
                parts.append(f"\n### Key Factors")
                parts.append('\n'.join(f"- {f}" for f in doc.key_factors))
                parts.append(f"\n### Primary Authority")
                parts.append('\n'.join(f"- {a}" for a in doc.primary_authority))
                parts.append(f"\n### Resolution Strategy")
                parts.append(doc.resolution_strategy)
                parts.append(f"\n### Confidence Assessment")
                parts.append(f"**Level**: {doc.confidence.value}")
                parts.append(f"**Stratification**: {doc.confidence_stratification}")
                parts.append(f"**Fragility Score**: {doc.fragility_score}")
                parts.append("")

            return "\n".join(parts)

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence level
        confidence_hierarchy = {
            ConfidenceLevel.DEFENSIBLE: 0,
            ConfidenceLevel.AGGRESSIVE: 1,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 3
        }

        min_confidence = min(doctrines, key=lambda d: confidence_hierarchy[d.confidence])
        return min_confidence.confidence

    def _disclosure_response(self, question: str) -> str:
        """Generate disclosure response when no doctrines match"""
        return f"""**Perforation Design Query**: {question}

**Response**: No specific doctrine blocks were triggered for this query. This may indicate:
1. The question is outside the engine's current expertise domains
2. More specific terminology is needed to match doctrine keywords
3. The question requires custom analysis beyond standardized doctrines

**Recommended Action**: Consult with a perforating specialist or service company engineer for questions outside standard doctrine coverage.

**Covered Domains**: Shaped charge design, gun systems (casing/through-tubing/TCP), shot density and phasing, perforation friction, limited entry design, cluster efficiency, underbalanced/overbalanced perforating, API testing, gun debris, HPHT operations, oriented perforating, propellant systems, abrasive jetting, safety procedures.

**Confidence**: DISCLOSURE (requires expert review)"""

    def calculate_determinism_hash(self, question: str, answer: str,
                                   doctrines: List[str]) -> str:
        """TIE-20 Component 16: SHA-256 determinism hash"""
        content = f"{question}|{answer}|{'|'.join(sorted(doctrines))}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    description="Perforation design intelligence engine with TIE-20 gold standard",
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = PerforationEngine()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component 12: Health endpoint"""
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=time.time() - METRICS.start_time
    )


@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint with three-layer response"""
    start_time = time.time()

    try:
        answer, doctrines, confidence = engine.three_layer_response(
            request.question, request.mode, request.zone
        )

        response_time_ms = (time.time() - start_time) * 1000
        determinism_hash = engine.calculate_determinism_hash(
            request.question, answer, doctrines
        )

        # Extract categories from triggered doctrines
        categories = [
            d.issue_category for d in engine.doctrines
            if d.topic in doctrines
        ]

        # Record metrics
        METRICS.record_query(request.mode, categories, doctrines, response_time_ms)

        # Build telemetry
        telemetry = {
            "doctrines_searched": len(DOCTRINE_CACHE),
            "doctrines_triggered": len(doctrines),
            "response_time_ms": round(response_time_ms, 2),
            "mode": request.mode.value,
            "zone": request.zone.value,
            "categories": [c.value for c in categories]
        }

        logger.info(
            f"Query processed: {len(doctrines)} doctrines, "
            f"{response_time_ms:.1f}ms, confidence={confidence.value}"
        )

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            zone=request.zone,
            triggered_doctrines=doctrines,
            response_time_ms=response_time_ms,
            determinism_hash=determinism_hash,
            telemetry=telemetry
        )

    except Exception as e:
        logger.error(f"Query failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Engine performance metrics"""
    return METRICS.get_summary()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "categories": list(set(d.issue_category.value for d in DOCTRINE_CACHE)),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "authority": d.authority_level.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/")
async def root():
    """Root endpoint with engine information"""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "status": "operational",
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "endpoints": {
            "query": "/query (POST)",
            "health": "/health (GET)",
            "metrics": "/metrics (GET)",
            "doctrines": "/doctrines (GET)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
