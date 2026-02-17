"""
FRAC02 - Proppant Selection & Performance Engine
TIE Gold Standard Intelligence Engine

Domain: Completions - Proppant Technology
Port: 9022
Authority: Completions Engineering Expert + API RP 19C/ISO 13503-2 Standards

Provides expert analysis on:
- Proppant type selection (natural sand, RCS, ceramic, sintered bauxite)
- Mesh size optimization (20/40, 30/50, 40/70, 100 mesh)
- Proppant concentration scheduling and PPA optimization
- API RP 19C/ISO 13503-2 testing and specifications
- Proppant transport and settling in non-Newtonian fluids
- Embedment, flowback, conductivity, and long-term performance
- Regional sand economics and in-basin logistics
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import uuid
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

ENGINE_ID = "FRAC02"
ENGINE_NAME = "Proppant Selection & Performance Engine"
VERSION = "1.0.0"
PORT = 9022

# Configure loguru
logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
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
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    PROPPANT_TYPE = "PROPPANT_TYPE"
    MESH_SIZE = "MESH_SIZE"
    CONCENTRATION = "CONCENTRATION"
    API_TESTING = "API_TESTING"
    TRANSPORT = "TRANSPORT"
    EMBEDMENT = "EMBEDMENT"
    CONDUCTIVITY = "CONDUCTIVITY"
    FLOWBACK = "FLOWBACK"
    LOGISTICS = "LOGISTICS"
    ECONOMICS = "ECONOMICS"
    QUALITY_CONTROL = "QUALITY_CONTROL"
    LONG_TERM_PERFORMANCE = "LONG_TERM_PERFORMANCE"

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., description="Proppant selection question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(None, description="Formation/well context")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis zone")

class DoctrineBlock(BaseModel):
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

class QueryResponse(BaseModel):
    query_id: str
    conclusion: str
    reasoning: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    epistemic_caveats: List[str]
    authority_citations: List[str]
    determinism_hash: str
    latency_ms: float
    mode: ResponseMode
    zone: AnalysisZone

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ EXPERT PROPPANT DOCTRINE BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Northern White Sand vs Regional Brown Sand Selection",
        keywords=["northern white", "wisconsin sand", "regional sand", "brown sand", "ottawa sand", "permian basin sand", "in-basin sand"],
        conclusion_template=[
            "Northern White sand (Wisconsin/Ottawa) remains the gold standard for high-stress applications due to superior roundness, sphericity, and crush resistance per API RP 19C.",
            "Regional brown sand from in-basin mines (Permian Basin, Eagle Ford) offers significant logistics cost savings (40-60% reduction) but typically exhibits 10-15% lower conductivity at >6000 psi closure stress.",
            "Basin-specific sand selection must balance API crush test results, delivered cost per ton, and formation closure stress predictions from minifrac analysis."
        ],
        reasoning_framework="""
Northern White Sand Advantages:
1. API RP 19C Crush Resistance: <10% fines generation at 10,000 psi (ISO 13503-2 Method A)
2. Roundness/Sphericity: 0.7-0.9 Krumbein scale (API Section 7)
3. Acid Solubility: <2% per API RP 19C Section 8 (minimal formation damage from dissolution)
4. Turbidity: <250 FTU at 2% KCl (low fines, clean pack)
5. Established supply chain from Wisconsin/Illinois/Ottawa mines

Regional Brown Sand Trade-offs:
1. Last-Mile Logistics: In-basin mines reduce trucking by 500-1000 miles
2. Cost Differential: $20-40/ton delivered vs $60-90/ton for Northern White
3. Performance Gap: 10-15% conductivity reduction at high stress (6000-8000 psi)
4. Roundness Penalty: 0.5-0.7 Krumbein (more angular, higher embedment risk)
5. Crush Resistance: 12-18% fines at 10,000 psi (acceptable for <6000 psi formations)

Decision Framework:
- High stress formations (>7000 psi): Northern White mandatory
- Moderate stress (4000-7000 psi): Regional sand acceptable with 20/40 mesh
- Shallow/soft formations (<4000 psi): Regional sand optimal (cost-driven)
- Operator economics: Break-even analysis on $/incremental BOE vs proppant delta cost
        """,
        key_factors=[
            "Formation closure stress from ISIP decline analysis",
            "Proppant delivered cost differential (regional vs Northern White)",
            "API RP 19C crush test results at anticipated stress",
            "Turbidity and acid solubility per ISO 13503-2",
            "Logistics constraints (silo capacity, local mine inventory)",
            "Expected well EUR and NPV sensitivity to conductivity variance"
        ],
        primary_authority=[
            "API RP 19C - Recommended Practice for Measurement of Proppant Properties",
            "ISO 13503-2 - Petroleum and Natural Gas Industries - Completion Fluids and Materials - Part 2: Measurement of Properties of Proppants",
            "SPE 84306 - Economic Comparison of Regional Proppants in Permian Basin Completions"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Cost-focused operators prioritize in-basin sand regardless of conductivity penalty",
        counter_arguments=[
            "Northern White premium cost ($40-50/ton extra) may exceed NPV gain from conductivity improvement in marginal wells",
            "Regional sand crush resistance adequate for Permian formations (avg 5000-6000 psi closure)",
            "In-basin logistics reduces supply chain risk and enables JIT delivery",
            "Field studies show <5% EUR difference between Northern White and regional sand in moderate-stress formations"
        ],
        resolution_strategy="Conduct basin-specific economic analysis: model EUR sensitivity to conductivity variance, compare to incremental proppant cost, and establish closure stress threshold (typically 6500-7000 psi) where Northern White premium is justified by NPV uplift.",
        entity_scope="Oil and gas operators, proppant suppliers, completions engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on API test standards and performance deltas; moderate confidence on economic break-even thresholds (operator-specific NPV models vary).",
        controlling_precedent="API RP 19C Section 6 (Crush Resistance) and ISO 13503-2 Method A establish performance testing protocols universally adopted by industry."
    ),

    DoctrineBlock(
        topic="Mesh Size Selection (20/40 vs 30/50 vs 40/70 vs 100 Mesh)",
        keywords=["mesh size", "20/40", "30/50", "40/70", "100 mesh", "particle size distribution", "screen size"],
        conclusion_template=[
            "20/40 mesh (0.42-0.85 mm) provides maximum conductivity and is standard for conventional fracturing in moderate to high permeability reservoirs.",
            "40/70 mesh (0.21-0.42 mm) reduces proppant settling velocity by 60-70% vs 20/40, enabling placement in high fluid-loss or low viscosity systems, but sacrifices 30-40% conductivity.",
            "100 mesh (0.15 mm) ultra-fine proppants are reserved for microfracture stimulation, acid fracturing tip screenout prevention, or ultra-low permeability formations where near-wellbore conductivity dominates."
        ],
        reasoning_framework="""
Mesh Size Physics:
1. Darcy Flow in Proppant Pack: k_pack ∝ d²_proppant (conductivity scales with particle diameter squared)
2. Settling Velocity (Stokes Law): v_settle ∝ d²_proppant × (ρ_proppant - ρ_fluid) / μ_apparent
3. Permeability-Conductivity Relationship: k_f·w_f where w_f (fracture width) must accommodate proppant pack

20/40 Mesh Applications:
- High permeability reservoirs (>1 mD): Maximum fracture conductivity required
- Low fluid-loss formations: Settling not limiting factor
- High viscosity fluids (>100 cP): Adequate proppant transport
- Typical conductivity: 150,000-300,000 mD-ft at 4000 psi stress (Northern White)

40/70 Mesh Applications:
- Reduced settling velocity: 0.15-0.25 ft/min vs 0.4-0.6 ft/min for 20/40 in 40 cP fluid
- High fluid-loss carbonates or highly fractured formations
- Slickwater fracturing (low viscosity, high rate): Better suspension characteristics
- Conductivity penalty: 80,000-150,000 mD-ft (40-50% reduction vs 20/40)

100 Mesh Applications:
- Acid fracturing: Prevents tip screenout by bridging natural fractures
- Ultra-tight gas (<0.01 mD): Fracture conductivity > formation permeability by 1000x even with fine mesh
- Near-wellbore tortuosity: Small particles navigate complex fracture geometry
- Conductivity: 20,000-50,000 mD-ft (acceptable when formation permeability is nanodarcy scale)

Tail-In Strategy:
- Bulk stage: 20/40 or 30/50 for fracture body conductivity
- Final 10-20%: 40/70 or 100 mesh to ensure proppant reaches fracture tip and prevents unpropped length
        """,
        key_factors=[
            "Formation permeability and required fracture conductivity ratio (k_f·w_f / k_matrix > 10-100)",
            "Fluid rheology (viscosity, power law index) and proppant settling calculations",
            "Fluid-loss coefficient and fracture geometry (PKN vs KGD width profiles)",
            "Pumping rate and fracture height (tall fractures exacerbate settling)",
            "Economic trade-off: coarse mesh costs 10-15% less per ton than fine mesh"
        ],
        primary_authority=[
            "API RP 19D - Recommended Practice on Measuring the Long-Term Conductivity of Proppants",
            "SPE 119900 - Impact of Proppant Mesh Size on Fracture Conductivity",
            "ISO 13503-5 - Procedures for Measuring the Long-Term Conductivity of Proppants"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Default to 40/70 mesh for all slickwater fracs to minimize settling risk",
        counter_arguments=[
            "40/70 mesh conductivity penalty (40-50%) may exceed EUR benefit from improved placement",
            "Modern slickwater friction reducers (up to 30 cP) can transport 20/40 mesh adequately",
            "20/40 mesh cost advantage ($5-10/ton cheaper) compounds on 10-15 million lb jobs",
            "Field data shows negligible production difference between 20/40 and 40/70 in low-perm shales (<0.1 mD)"
        ],
        resolution_strategy="Model proppant transport with computational fluid dynamics (CFD) or simplified settling equations; compare predicted proppant placement (% of fracture propped) vs conductivity penalty; select coarsest mesh that achieves >90% proppant coverage in fracture height.",
        entity_scope="Completions engineers, fracture modeling specialists, reservoir engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on conductivity-mesh relationships (API RP 19D lab data extensive); moderate confidence on field settling behavior (dependent on real-time fluid properties, fracture complexity).",
        controlling_precedent="API RP 19D conductivity testing and Stokes Law settling calculations provide industry-standard framework for mesh size selection."
    ),

    DoctrineBlock(
        topic="Resin-Coated Sand (RCS) for Flowback Control",
        keywords=["resin coated sand", "RCS", "curable resin", "precured resin", "flowback prevention", "proppant flowback"],
        conclusion_template=[
            "Resin-Coated Sand (RCS) with curable resin coating consolidates in the fracture upon closure, preventing proppant flowback during production while maintaining conductivity.",
            "Precured RCS is applied to the proppant prior to pumping; curable RCS requires downhole temperature and closure stress to activate resin bonding (typically 150-250°F, 12-48 hours cure time).",
            "RCS is cost-effective for high-rate gas wells (>10 MMscf/d) where proppant flowback can erode tubulars and cause surface equipment damage; premium cost ($20-40/ton over uncoated sand) is justified by avoided workover expense."
        ],
        reasoning_framework="""
Proppant Flowback Mechanisms:
1. High gas velocity (>20 ft/sec in fracture) entrains proppant particles
2. Pressure cycling during production dislodges unconsolidated proppant
3. Multi-phase flow (gas-condensate-water) creates turbulent shear forces
4. Fracture tortuosity and near-wellbore flow convergence exacerbate flowback

RCS Coating Types:
1. Precured RCS: Resin cured before pumping; provides immediate consolidation upon closure
   - No downhole cure time required
   - Lower bond strength (2000-3000 psi unconfined compressive strength)
   - Suitable for moderate flowback risk applications
2. Curable RCS: Resin activates at downhole temperature after placement
   - Requires 150-250°F BHT and 12-48 hour soak time
   - High bond strength (4000-6000 psi UCS)
   - Superior flowback prevention but delayed online time

Performance Considerations:
- Conductivity Penalty: 10-20% reduction vs uncoated sand (resin fills pore space)
- Tail-In Application: RCS applied to final 20-30% of proppant (near-wellbore zone only)
- Temperature Limits: Phenolic resins degrade >300°F; furan resins stable to 350°F
- Resin Loading: 1-6% by weight (higher loading = stronger bond but more conductivity loss)

Economic Justification:
- RCS incremental cost: $20-40/ton × 20% of total proppant = $40k-100k per well
- Flowback workover cost: $200k-500k (rig, fishing, recompletion)
- Equipment damage: Tubing erosion, flowline damage, separator plugging
- Production deferment: 2-4 weeks offline during workover
- Break-even: RCS justified if flowback probability >10-20% (based on offset well history)
        """,
        key_factors=[
            "Gas production rate and flowing bottomhole pressure (high drawdown = high flowback risk)",
            "Bottomhole temperature (must exceed resin cure temperature for curable RCS)",
            "Offset well flowback history and proppant production trends",
            "Formation consolidation (unconsolidated sands higher flowback risk than cemented formations)",
            "Economic comparison: RCS premium cost vs expected flowback workover NPV",
            "Completions design: tail-in RCS strategy (20-30% near-wellbore) vs full RCS treatment"
        ],
        primary_authority=[
            "API RP 19C Section 11 - Resin-Coated Proppant Testing Procedures",
            "SPE 90697 - Field Performance of Resin-Coated Proppants in High-Rate Gas Wells",
            "ISO 13503-2 Annex D - Resin-Coated Proppant Characterization"
        ],
        burden_holder="Completions Engineer",
        adversary_position="RCS is unnecessary expense; fiber-laden fluids or reduced drawdown can control flowback at lower cost",
        counter_arguments=[
            "Fiber additives (1-2 lb/1000 gal) provide flowback control at $5k-10k vs $40k-100k for RCS",
            "Controlled drawdown (choke management) can prevent flowback without RCS",
            "Many unconventional wells show no flowback with uncoated proppant (RCS is over-design)",
            "RCS conductivity penalty (10-20%) may offset flowback prevention benefit in marginal wells"
        ],
        resolution_strategy="Analyze offset well proppant flowback data; quantify flowback probability and expected workover NPV; apply RCS selectively (tail-in 20-30%) in high-risk wells (gas rate >10 MMscf/d, unconsolidated formation, offset flowback history); consider fiber as lower-cost alternative for moderate-risk wells.",
        entity_scope="Completions engineers, production engineers, reservoir engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on RCS flowback prevention effectiveness (extensive field validation); moderate confidence on economic break-even (site-specific flowback risk assessment required).",
        controlling_precedent="API RP 19C Section 11 establishes RCS testing protocols; field practice supports tail-in application (20-30% near-wellbore) as cost-effective strategy."
    ),

    DoctrineBlock(
        topic="Ceramic Proppants (Lightweight, Intermediate, High-Strength)",
        keywords=["ceramic proppant", "lightweight ceramic", "intermediate strength ceramic", "high strength ceramic", "sintered bauxite", "alumina silicate"],
        conclusion_template=[
            "Ceramic proppants are engineered from sintered bauxite or kaolin clay, offering superior crush resistance (1-3% fines at 10,000-20,000 psi) vs natural sand, but at 3-10x cost premium.",
            "Lightweight ceramic (LWC, 2.45-2.65 g/cc) reduces settling velocity by 20-30% vs sand, enabling better transport in low-viscosity fluids; intermediate-strength ceramic (ISP, 3.2-3.4 g/cc) and high-strength ceramic (HSP, 3.5-3.8 g/cc) target ultra-high stress applications (>10,000 psi).",
            "Ceramic proppant use is economically justified only in high-stress, high-value wells where sand crush would result in catastrophic conductivity loss (deep gas, HPHT reservoirs, geothermal)."
        ],
        reasoning_framework="""
Ceramic Proppant Manufacturing:
1. Raw Material: Bauxite (aluminum oxide) or kaolin clay (alumina-silicate)
2. Sintering Process: 1200-1800°C kiln firing creates high-strength ceramic spheres
3. Mesh Sizing: Crushed and screened to API mesh distributions (12/20, 16/30, 20/40)
4. Quality Control: API RP 19C crush testing, turbidity, sphericity, bulk density

Ceramic Proppant Types:
1. Lightweight Ceramic (LWC):
   - Density: 2.45-2.65 g/cc (sand is 2.65 g/cc)
   - Crush Resistance: 5-7% fines at 10,000 psi
   - Conductivity: 120,000-200,000 mD-ft at 8,000 psi (20/40 mesh)
   - Applications: Deep gas wells (>12,000 ft), slickwater fracs needing transport improvement
   - Cost: $250-400/ton (3-5x sand)

2. Intermediate-Strength Proppant (ISP):
   - Density: 3.2-3.4 g/cc
   - Crush Resistance: 2-4% fines at 15,000 psi
   - Conductivity: 150,000-250,000 mD-ft at 10,000 psi
   - Applications: HPHT gas wells (>15,000 psi closure stress)
   - Cost: $400-600/ton (5-8x sand)

3. High-Strength Proppant (HSP):
   - Density: 3.5-3.8 g/cc (sintered bauxite)
   - Crush Resistance: <1% fines at 20,000 psi
   - Conductivity: 180,000-300,000 mD-ft at 15,000 psi (minimal crush degradation)
   - Applications: Ultra-HPHT (>400°F, >20,000 psi), geothermal, deep offshore
   - Cost: $600-900/ton (8-10x sand)

Economic Decision Framework:
- Closure Stress Threshold: Ceramic justified at >10,000 psi where sand crush exceeds 15-20% fines
- Well Value: High EUR, high gas price, long reserve life justify ceramic premium
- Conductivity Sensitivity: Model production vs fracture conductivity; ceramic justified if 2x conductivity improvement yields >20% EUR uplift
- Hybrid Design: Ceramic in near-wellbore (high stress concentration) + sand in far-field (lower cost)

Transport Considerations:
- LWC settling velocity 20-30% lower than sand (advantageous in slickwater, tall fractures)
- ISP/HSP settling velocity 30-50% HIGHER than sand (requires high viscosity gels, crosslinked fluids)
- Specific gravity mismatch in hybrid designs can cause segregation
        """,
        key_factors=[
            "Formation closure stress from minifrac ISIP decline or pore pressure/stress modeling",
            "Well EUR and NPV sensitivity to fracture conductivity (high-value wells justify ceramic)",
            "Proppant transport constraints (fluid rheology, settling velocity calculations)",
            "API RP 19C crush test results at anticipated stress (compare ceramic vs sand fines generation)",
            "Hybrid design economics (ceramic near-wellbore, sand far-field)",
            "Supply chain logistics (ceramic availability, silo compatibility)"
        ],
        primary_authority=[
            "API RP 19C Section 6 - Crush Resistance Testing at Elevated Stress",
            "API RP 19D - Long-Term Conductivity of Ceramic Proppants",
            "SPE 84308 - Economic Analysis of Ceramic Proppants in Deep Gas Wells"
        ],
        burden_holder="Completions Engineer / Reservoir Engineer",
        adversary_position="Ceramic proppant is over-specified; modern high-quality sands adequate even at high stress",
        counter_arguments=[
            "Premium Northern White sand <10% fines at 10,000 psi (ceramic unnecessary for most applications)",
            "Ceramic 3-10x cost premium ($300-800/ton extra × 10M lb = $1.5-4.0M incremental cost per well)",
            "Conductivity improvement from ceramic may not translate to proportional EUR uplift due to reservoir limitations",
            "Hybrid designs (ceramic near-wellbore + sand far-field) achieve 80% of benefit at 40% of cost"
        ],
        resolution_strategy="Establish closure stress threshold (typically 10,000-12,000 psi) where sand crush exceeds acceptable limits; conduct NPV sensitivity analysis on EUR vs proppant cost; consider hybrid designs (LWC or ISP near-wellbore, sand far-field) to optimize cost-performance; reserve HSP for ultra-HPHT (>15,000 psi, >400°F) applications only.",
        entity_scope="Operators in deep gas basins, HPHT reservoirs, geothermal completions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on ceramic crush resistance and conductivity performance (extensive API RP 19C/19D lab data); moderate confidence on economic break-even (operator-specific NPV models and gas price assumptions vary).",
        controlling_precedent="API RP 19C crush resistance testing and API RP 19D long-term conductivity protocols establish performance basis for ceramic vs sand comparison."
    ),

    DoctrineBlock(
        topic="Proppant Concentration (PPA) Scheduling and Ramp Design",
        keywords=["proppant concentration", "PPA", "pounds per gallon added", "proppant ramp", "tail-in concentration", "stage loading"],
        conclusion_template=[
            "Proppant concentration (PPA, pounds per gallon added) is ramped from 0.25-0.5 PPA at stage initiation to 2.0-3.0+ PPA at tail-in to maximize proppant placement while avoiding premature screenout.",
            "Target proppant loading per lateral foot varies by formation: 1000-1500 lb/ft in oil shales (Permian, Bakken), 1500-2500 lb/ft in gas shales (Marcellus, Haynesville), with final 10-20% pumped at maximum concentration (2.5-3.0 PPA) to ensure fracture tip proppant coverage.",
            "Aggressive PPA ramps (rapid increases) risk early screenout in high fluid-loss or complex fracture networks; conservative ramps (slow increases) may under-load the fracture and sacrifice conductivity."
        ],
        reasoning_framework="""
Proppant Concentration Physics:
1. Fracture Width Constraint: Maximum PPA limited by w_frac / d_proppant ratio (avoid bridging)
2. Fluid Efficiency: Higher fluid loss = lower net pressure = narrower fracture = lower PPA ceiling
3. Proppant Transport: High PPA increases slurry viscosity, reduces settling, but increases friction pressure
4. Screenout Risk: Excessive PPA causes proppant bridging at fracture tip or in narrow sections

Typical PPA Ramp Design:
1. Pad Stage (0 PPA): 10-25% of total fluid volume (create fracture width, minimal fluid loss)
2. Initial Proppant (0.25-0.5 PPA): Establish proppant transport, verify pressure response
3. Ramp-Up (0.5 → 1.0 → 1.5 → 2.0 PPA): Step increases every 5-10 bbl or based on pressure stability
4. Bulk Loading (2.0-2.5 PPA): Majority of proppant mass (60-70% of total proppant)
5. Tail-In (2.5-3.0+ PPA): Final 10-20% of proppant ensures fracture tip coverage and maximizes pack density

Proppant Loading Targets (lb/lateral ft):
- Permian Wolfcamp/Bone Spring: 1000-1500 lb/ft (8-12 million lb per 8,000 ft lateral)
- Eagle Ford: 1200-1800 lb/ft
- Bakken: 1000-1500 lb/ft
- Marcellus: 1500-2000 lb/ft (higher stress, higher conductivity requirement)
- Haynesville: 2000-2500 lb/ft (ultra-high stress, ceramic often used)

Advanced Techniques:
- Pulse Loading: Alternate high PPA (2.5-3.0) and low PPA (1.5-2.0) to create heterogeneous pack, reduce embedment
- Ultra-High Concentration Tail-In: 3.5-4.0 PPA in final 5-10% (maximize near-wellbore conductivity)
- Dynamic Ramp Adjustment: Real-time pressure monitoring to adjust PPA based on net pressure response

Failure Modes:
1. Premature Screenout: Excessive PPA in narrow fracture or high fluid-loss zone (pressure spikes, incomplete stage)
2. Under-Propped Fracture: Conservative PPA ramp leaves fracture tip unpropped (reduced effective length)
3. Proppant Settling: Low PPA in tall fractures allows gravity segregation (bottom 20-40% over-propped, top unpropped)
        """,
        key_factors=[
            "Formation fluid-loss coefficient (high fluid-loss = conservative PPA ramp)",
            "Fracture complexity (natural fracture networks require slower ramps to avoid bridging)",
            "Lateral length and stage spacing (longer laterals require higher total proppant mass)",
            "Real-time treating pressure response (stable pressure allows PPA increase, rising pressure mandates hold or reduction)",
            "Economic optimization: balance proppant cost vs EUR uplift from higher loading",
            "Pumping equipment limits (blender capacity, friction pressure limits)"
        ],
        primary_authority=[
            "SPE 152596 - Optimization of Proppant Loading in Unconventional Reservoirs",
            "SPE 119900 - Impact of Proppant Concentration on Fracture Conductivity",
            "API RP 19D - Conductivity Testing at Varying Proppant Concentrations"
        ],
        burden_holder="Completions Engineer / Frac Design Engineer",
        adversary_position="Maximize PPA and proppant loading to ensure conductivity; screenout risk is acceptable trade-off",
        counter_arguments=[
            "Conservative PPA ramps leave fracture under-propped, sacrificing 10-20% EUR",
            "Modern friction reducers and fluid systems can transport 3.0+ PPA without screenout in most formations",
            "Higher proppant loading (2000-3000 lb/ft) shows minimal EUR uplift beyond 1500 lb/ft in Permian Basin (diminishing returns)",
            "Screenout costs (lost stage, reduced lateral length, remediation) can exceed $100k-300k per event"
        ],
        resolution_strategy="Design PPA ramp based on offset well performance (historical screenout frequency, pressure response) and real-time pressure monitoring; target 1500-2000 lb/ft in moderate-stress formations, 2000-2500 lb/ft in high-stress; implement tail-in at 2.5-3.0 PPA to ensure fracture tip coverage; adjust ramp dynamically based on net pressure trends (stable = aggressive, rising = conservative).",
        entity_scope="Completions engineers, frac operations engineers, real-time monitoring specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on PPA ramp principles and conductivity-loading relationships; moderate confidence on optimal loading targets (basin-specific, operator completion design philosophy varies).",
        controlling_precedent="Field practice in major unconventional plays (Permian, Marcellus, Eagle Ford) establishes 1000-2500 lb/ft loading targets and 2.0-3.0 PPA tail-in as industry standard."
    ),

    DoctrineBlock(
        topic="API RP 19C / ISO 13503-2 Proppant Testing and Specifications",
        keywords=["API RP 19C", "ISO 13503-2", "crush test", "conductivity test", "turbidity", "roundness", "sphericity", "acid solubility", "bulk density"],
        conclusion_template=[
            "API RP 19C and ISO 13503-2 establish standardized laboratory testing protocols for proppant crush resistance, conductivity, turbidity, acid solubility, roundness/sphericity, and bulk density, enabling objective comparison of proppant products.",
            "Crush resistance testing (API RP 19C Section 6, ISO 13503-2 Method A) measures percent fines generation (<mesh size) after 2-hour loading at specified stress (typically 5,000-20,000 psi); industry specification is <10% fines at anticipated closure stress.",
            "Conductivity testing (API RP 19D, ISO 13503-5) measures long-term fracture conductivity (k_f·w_f in mD-ft) at specified stress, temperature, and proppant concentration (typically 2 lb/ft²); results guide proppant selection and fracture design optimization."
        ],
        reasoning_framework="""
API RP 19C Key Tests:
1. Crush Resistance (Section 6):
   - Procedure: Load proppant sample at specified stress (5k, 8k, 10k, 12k, 15k, 20k psi) for 2 hours at 250°F
   - Measurement: Sieve crushed sample, weigh fines below nominal mesh size
   - Specification: <10% fines for Northern White sand at 10,000 psi; <5% for high-quality ceramic
   - Interpretation: Higher fines = reduced conductivity (crushed particles clog pore space)

2. Turbidity (Section 7):
   - Procedure: Mix proppant in 2% KCl solution, measure clarity in Formazin Turbidity Units (FTU)
   - Specification: <250 FTU for high-quality sand; <100 FTU for ceramic
   - Interpretation: High turbidity indicates clay/fines contamination (formation damage risk)

3. Acid Solubility (Section 8):
   - Procedure: Dissolve proppant in 12% HCl-3% HF acid at 150°F, measure weight loss
   - Specification: <2% for Northern White sand; <1% for ceramic
   - Interpretation: High solubility = carbonate/feldspar content (proppant dissolution in acidized wells)

4. Roundness and Sphericity (Section 9):
   - Procedure: Visual comparison to Krumbein-Sloss chart (0.1-0.9 scale)
   - Specification: >0.6 roundness, >0.6 sphericity for premium sand; >0.7 for ceramic
   - Interpretation: Angular particles embed in formation, reduce pack permeability

5. Bulk and Apparent Density (Section 10):
   - Procedure: Measure weight per unit volume (loose pour vs packed)
   - Specification: 1.58-1.68 g/cc bulk density for sand; 1.25-1.45 for LWC; 2.0-2.5 for ISP/HSP
   - Interpretation: Density affects settling velocity, transport requirements

ISO 13503-2 Enhancements:
- Method A (Short-Term Crush): Aligns with API RP 19C Section 6
- Method B (Cyclic Stress): 10 load-unload cycles to simulate production pressure cycling
- Method C (Chemical Compatibility): Proppant exposure to completion fluids, acids, produced fluids
- Annex D: Resin-coated proppant consolidation testing

API RP 19D / ISO 13503-5 Conductivity Testing:
- Procedure: Pack proppant in conductivity cell (API conductivity cell dimensions per RP 19D)
- Load at specified stress (2k, 4k, 6k, 8k, 10k+ psi) and temperature (150-350°F)
- Flow 2% KCl brine at constant rate, measure pressure drop
- Calculate conductivity: k_f·w_f = (q × μ × L) / (ΔP × w × h) in mD-ft
- Duration: 50-300 hours to measure long-term degradation
- Variables: Proppant type, mesh size, concentration (0.5-4.0 lb/ft²), stress, temperature, time

Industry Specifications:
- High-quality Northern White sand: 150,000-300,000 mD-ft at 4,000 psi (20/40 mesh, 2 lb/ft²)
- Regional brown sand: 100,000-200,000 mD-ft at 4,000 psi
- Lightweight ceramic: 120,000-200,000 mD-ft at 8,000 psi
- Intermediate ceramic: 150,000-250,000 mD-ft at 10,000 psi
- High-strength ceramic: 180,000-300,000 mD-ft at 15,000 psi
        """,
        key_factors=[
            "Formation closure stress (determines crush test stress level)",
            "Temperature (affects long-term conductivity degradation)",
            "Proppant concentration in fracture (2 lb/ft² standard test condition)",
            "Acid treatment exposure (acid solubility critical for acidized wells)",
            "Comparison across proppant suppliers (API tests enable apples-to-apples comparison)",
            "Quality control: batch testing to verify delivered proppant meets specification"
        ],
        primary_authority=[
            "API RP 19C - Recommended Practice for Measurement of Proppant Properties",
            "API RP 19D - Recommended Practice on Measuring the Long-Term Conductivity of Proppants",
            "ISO 13503-2 - Measurement of Properties of Proppants Used in Hydraulic Fracturing",
            "ISO 13503-5 - Procedures for Measuring the Long-Term Conductivity of Proppants"
        ],
        burden_holder="Proppant Supplier (provide test data) / Completions Engineer (specify requirements)",
        adversary_position="Lab testing over-emphasizes crush resistance; field performance shows minimal correlation with API crush test results",
        counter_arguments=[
            "API crush test (2-hour loading) may not represent years of downhole stress exposure",
            "Conductivity testing at 2 lb/ft² proppant concentration may not reflect actual pack density in fracture (varies 0.5-4.0 lb/ft²)",
            "Temperature and chemical exposure in lab tests may not match field conditions",
            "Field production comparisons (sand vs ceramic) show smaller performance gaps than lab conductivity deltas predict"
        ],
        resolution_strategy="Use API RP 19C/19D as baseline for proppant qualification and supplier comparison; recognize test limitations (short duration, idealized conditions); supplement with field performance data from offset wells; specify batch testing on delivered proppant to verify compliance with API standards.",
        entity_scope="Proppant suppliers, completions engineers, quality control specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on API test protocols as industry standard; moderate confidence on lab-to-field correlation (field complexity exceeds lab idealization).",
        controlling_precedent="API RP 19C, API RP 19D, ISO 13503-2, and ISO 13503-5 are universally adopted industry standards for proppant testing and specification."
    ),

    DoctrineBlock(
        topic="Proppant Transport and Settling in Non-Newtonian Fluids",
        keywords=["proppant transport", "settling velocity", "stokes law", "non-newtonian fluid", "power law", "crosslinked gel", "slickwater"],
        conclusion_template=[
            "Proppant settling velocity in fracturing fluids is governed by modified Stokes Law accounting for non-Newtonian fluid rheology (power-law or Herschel-Bulkley models), with settling rates 50-90% lower in crosslinked gels (100-500 cP) vs slickwater (5-30 cP).",
            "Effective proppant transport requires settling velocity < fracture propagation velocity; slickwater fracs rely on high injection rate (60-100+ bpm) and turbulent flow to suspend proppant, while gel-based fracs use viscosity for suspension.",
            "Proppant settling in tall fractures (>300 ft height) can result in unpropped upper fracture sections; mitigation strategies include smaller mesh size (40/70 vs 20/40), higher viscosity fluids, or fiber additives to create proppant-laden slugs."
        ],
        reasoning_framework="""
Stokes Law (Newtonian Fluids):
v_settle = (d_p² × g × (ρ_p - ρ_f)) / (18 × μ)
Where:
- v_settle = settling velocity (ft/min)
- d_p = proppant diameter (ft)
- g = gravitational acceleration (32.2 ft/s²)
- ρ_p = proppant density (lb/ft³): sand 165 lb/ft³, LWC 155 lb/ft³, ceramic 200+ lb/ft³
- ρ_f = fluid density (lb/ft³): water 62.4 lb/ft³, gel 64-66 lb/ft³
- μ = fluid viscosity (lb/ft-sec)

Example (20/40 mesh sand in water):
- d_p = 0.025 in = 0.002 ft
- ρ_p = 165 lb/ft³, ρ_f = 62.4 lb/ft³
- μ = 1 cP = 0.000672 lb/ft-sec
- v_settle = 0.6 ft/min (36 ft/hr)

Non-Newtonian Fluid Correction (Power-Law Model):
τ = K × γ̇ⁿ
Where:
- τ = shear stress
- K = consistency index
- γ̇ = shear rate
- n = flow behavior index (n<1 shear-thinning, n=1 Newtonian, n>1 shear-thickening)

Apparent Viscosity:
μ_app = K × γ̇^(n-1)
For proppant settling, use low shear rate γ̇ (shear-thinning fluids exhibit high viscosity at low shear)

Example (20/40 mesh sand in 40 lb/1000 gal crosslinked gel):
- K = 0.05 lb-sec^n/ft², n = 0.5 (typical crosslinked gel)
- Low shear γ̇ = 10 sec⁻¹
- μ_app = 0.05 × 10^(0.5-1) = 0.016 lb/ft-sec (24 cP equivalent)
- v_settle ≈ 0.15 ft/min (75% reduction vs water)

Practical Settling Velocities:
1. Slickwater (5-10 cP, n=0.8-1.0):
   - 20/40 mesh sand: 0.4-0.6 ft/min
   - 40/70 mesh sand: 0.15-0.25 ft/min
   - 100 mesh: 0.05-0.10 ft/min

2. Crosslinked Gel (100-500 cP at low shear, n=0.4-0.6):
   - 20/40 mesh sand: 0.05-0.15 ft/min
   - 40/70 mesh sand: 0.02-0.08 ft/min
   - Ceramic ISP/HSP: 0.10-0.20 ft/min (higher density)

Fracture Height Effects:
- Tall fractures (>300 ft): Gravity segregation significant (proppant settles to bottom 20-40%)
- Short fractures (<150 ft): Minimal settling impact
- Settling distance = v_settle × (fracture length / injection velocity)
- Example: 200 ft height, 0.3 ft/min settling, 5000 ft length, 10 ft/min injection velocity
  - Settling distance = 0.3 × (5000/10) = 150 ft (upper 50 ft unpropped)

Mitigation Strategies:
1. Smaller Mesh Size: 40/70 settles 60-70% slower than 20/40 (d² relationship)
2. Higher Viscosity: Crosslinked gel reduces settling by 80-90% vs slickwater
3. Higher Injection Rate: Reduces residence time in fracture (less time to settle)
4. Fiber Additives: 1-2 lb/1000 gal fiber creates proppant-laden slugs (suspended clusters)
5. Pulsed Proppant: Alternate proppant-laden and clean fluid slugs (distribute proppant vertically)
        """,
        key_factors=[
            "Fluid rheology (power-law parameters K and n) at downhole shear rate",
            "Proppant mesh size and density (d² and Δρ drive settling)",
            "Fracture height (tall fractures exacerbate gravity segregation)",
            "Injection rate (high rate reduces settling distance)",
            "Fracture complexity (natural fractures create tortuous paths, reduce settling)",
            "Economic trade-off: viscosity cost vs proppant placement quality"
        ],
        primary_authority=[
            "SPE 9866 - Proppant Transport in Hydraulic Fractures: Settling and Retardation",
            "SPE 28564 - Impact of Fluid Rheology on Proppant Transport and Placement",
            "API RP 39 - Recommended Practice on Measuring the Viscosity of Fracturing Fluids"
        ],
        burden_holder="Completions Engineer / Frac Design Engineer",
        adversary_position="Proppant transport models over-predict settling; field results show adequate proppant placement even with low-viscosity slickwater",
        counter_arguments=[
            "Slickwater fracs (5-10 cP) dominate unconventional completions despite high settling velocity (turbulent flow suspends proppant)",
            "Crosslinked gel adds $50k-150k per well vs slickwater (viscosity benefit may not justify cost)",
            "Production logs show minimal vertical proppant segregation in many slickwater completions (settling models may be conservative)",
            "Fiber additives ($5k-15k per well) provide settling mitigation at fraction of gel cost"
        ],
        resolution_strategy="Model proppant settling using power-law fluid rheology and fracture geometry; compare settling distance to fracture height; select fluid system and proppant mesh to achieve <20% unpropped height; validate with offset well microseismic or production logs; consider fiber additives as cost-effective settling mitigation in slickwater systems.",
        entity_scope="Completions engineers, frac fluid designers, fracture modeling specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on settling velocity calculations (Stokes Law and power-law corrections well-established); moderate confidence on field settling behavior (fracture complexity, turbulence, and proppant interactions exceed simplified models).",
        controlling_precedent="Modified Stokes Law with power-law fluid correction is industry-standard approach for proppant transport analysis; validated by lab experiments and computational fluid dynamics."
    ),

    DoctrineBlock(
        topic="Proppant Embedment in Soft Formations",
        keywords=["proppant embedment", "formation embedment", "soft formation", "young's modulus", "unconfined compressive strength", "conductivity loss"],
        conclusion_template=[
            "Proppant embedment occurs when formation rock yields plastically under proppant contact stress, allowing proppant particles to press into fracture face and reduce effective fracture width and conductivity; embedment severity scales inversely with formation Young's modulus and unconfined compressive strength (UCS).",
            "Soft formations (UCS <5,000 psi, E <2 million psi) such as unconsolidated sands, chalks, and coals can experience 30-70% conductivity loss from embedment; mitigation strategies include larger mesh size (16/20 vs 20/40), ultra-lightweight proppants, or partial monolayers to distribute load.",
            "Embedment impact is highest at low closure stress (<3,000 psi) where formation deformation is proportionally larger; as stress increases, additional conductivity loss from proppant crush may exceed embedment effects."
        ],
        reasoning_framework="""
Embedment Mechanics:
1. Proppant-Formation Contact Stress:
   - Contact stress = closure stress / (proppant contact area ratio)
   - For spherical proppant, contact area ≈ 10-20% of proppant surface (point contacts)
   - Localized contact stress 5-10x higher than bulk closure stress

2. Formation Yield Criterion:
   - Elastic response: Formation compressive strength > contact stress
   - Plastic yield: Contact stress exceeds UCS → proppant embeds
   - Embedment depth: function of (contact stress - UCS) × time

3. Conductivity Impact:
   - Effective fracture width: w_eff = w_initial - 2 × embedment_depth
   - Conductivity reduction: k_f·w_f ∝ w_eff³ (fracture width cubed relationship)
   - Example: 0.2 in initial width, 0.05 in embedment per side → w_eff = 0.1 in (50% reduction)
     Conductivity loss = 1 - (0.1/0.2)³ = 87.5% loss

Formation Property Thresholds:
1. Hard Formations (Minimal Embedment):
   - Young's Modulus E > 4 million psi
   - UCS > 10,000 psi
   - Examples: Limestone, dolomite, cemented sandstone, shale
   - Embedment depth: <0.01 in (negligible conductivity impact)

2. Moderate Formations (10-30% Conductivity Loss):
   - E = 2-4 million psi
   - UCS = 5,000-10,000 psi
   - Examples: Moderately cemented sandstone, siltstone
   - Embedment depth: 0.01-0.03 in

3. Soft Formations (30-70% Conductivity Loss):
   - E < 2 million psi
   - UCS < 5,000 psi
   - Examples: Unconsolidated sand, chalk, coal, diatomite
   - Embedment depth: 0.03-0.10 in (severe conductivity loss)

Mitigation Strategies:
1. Larger Mesh Size (16/20 or 12/18 vs 20/40):
   - Larger particles distribute load over more area
   - Reduce contact stress by 30-50%
   - Trade-off: Coarser mesh has higher settling velocity

2. Ultra-Lightweight Proppants (ULW):
   - Density <2.0 g/cc (vs 2.65 for sand)
   - Lower proppant-formation contact force
   - Example: Composite/polymer proppants, sintered fly ash

3. Partial Monolayer Coverage:
   - Reduce proppant concentration to <2 lb/ft² (vs 4-6 lb/ft² typical)
   - Single-layer proppant pack maximizes contact area, minimizes stress concentration
   - Trade-off: Lower pack permeability

4. Channel Fracturing:
   - Pulse proppant-laden and clean fluid slugs to create heterogeneous proppant pack
   - Open channels provide high-conductivity pathways
   - Reduces average embedment by 20-40%

5. Resin-Coated Sand:
   - Consolidated proppant pack distributes load more uniformly
   - Reduce embedment by 15-25% vs uncoated sand

Field Observations:
- Coal seam gas (UCS 1,000-3,000 psi): 50-70% conductivity loss from embedment
- Gulf Coast unconsolidated sands (UCS 2,000-5,000 psi): 30-50% loss
- Permian Delaware chalk (UCS 4,000-6,000 psi): 20-40% loss
- Marcellus shale (UCS >10,000 psi): <10% embedment loss (crush dominates)
        """,
        key_factors=[
            "Formation Young's modulus and unconfined compressive strength (from core testing or log correlations)",
            "Closure stress magnitude (low stress exacerbates embedment)",
            "Proppant mesh size (coarser mesh reduces contact stress)",
            "Proppant type (ULW, RCS reduce embedment)",
            "Proppant concentration (partial monolayers reduce stress concentration)",
            "Economic trade-off: ULW/large mesh premium cost vs conductivity preservation"
        ],
        primary_authority=[
            "SPE 115288 - Impact of Proppant Embedment on Fracture Conductivity in Soft Formations",
            "SPE 71673 - Proppant Embedment and Conductivity Loss in Unconsolidated Sands",
            "API RP 19C Annex E - Embedment Testing Procedures"
        ],
        burden_holder="Completions Engineer / Petrophysicist",
        adversary_position="Embedment is overstated; field production shows minimal sensitivity to formation hardness",
        counter_arguments=[
            "Many soft formations (Gulf Coast, Rockies) fractured successfully with standard 20/40 sand (embedment concern may be theoretical)",
            "ULW proppants cost 2-5x standard sand ($200-500/ton premium) with uncertain EUR benefit",
            "Partial monolayer designs sacrifice pack permeability (conductivity loss from low concentration may exceed embedment benefit)",
            "Field production comparisons (hard vs soft formations) show smaller productivity gaps than embedment models predict"
        ],
        resolution_strategy="Measure or correlate formation Young's modulus and UCS from core or logs; if UCS <5,000 psi, model embedment impact on conductivity; consider larger mesh (16/20, 12/18) or ULW proppants if embedment conductivity loss >30%; validate with offset well production data; balance mitigation cost vs EUR uplift.",
        entity_scope="Completions engineers, petrophysicists, reservoir engineers in soft formation plays",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence on embedment mechanics (lab testing validates phenomenon); low-moderate confidence on field magnitude (complex stress states, time-dependent creep, and reservoir heterogeneity exceed lab idealization).",
        controlling_precedent="API RP 19C Annex E and SPE literature establish embedment testing protocols; field validation in coal seam gas and Gulf Coast unconsolidated sands confirms >30% conductivity loss in soft formations."
    ),

    DoctrineBlock(
        topic="Fines Migration and Proppant Pack Damage",
        keywords=["fines migration", "formation fines", "proppant pack damage", "turbidity", "clay content", "permeability impairment"],
        conclusion_template=[
            "Fines migration occurs when clay particles, crushed proppant fragments, or formation debris mobilize during production and lodge in proppant pack pore throats, reducing pack permeability by 20-80% depending on fines content and flow velocity.",
            "Sources of fines include: (1) formation clay/silt released during fracturing, (2) proppant crush fines from closure stress, (3) fluid additives (gel residue, breaker byproducts), (4) scale precipitation (CaCO3, BaSO4), and (5) produced solids (asphaltenes, wax, hydrates).",
            "Mitigation strategies include high-quality proppant (low turbidity per API RP 19C), effective fluid cleanup (oxidative or enzymatic breakers), gravel pack or screen in proppant pack to filter fines, and controlled drawdown during initial production to prevent formation collapse and fines influx."
        ],
        reasoning_framework="""
Fines Migration Mechanisms:
1. Mobilization: Flow velocity exceeds critical velocity to dislodge fines from pore walls
   - Critical velocity ∝ √(ΔP / φ × k) (Darcy flow)
   - High drawdown during flowback mobilizes fines

2. Transport: Fines entrained in production fluid stream
   - Fine particle size (<10 microns) enables suspension in flow
   - Turbulent flow sustains suspension; laminar flow allows settling

3. Capture: Fines lodge in proppant pack pore throats (bridging)
   - Pore throat diameter in 20/40 mesh sand: 100-300 microns
   - Fines particles 5-20 microns bridge across pore throats
   - Permeability reduction: k_damaged / k_initial = (1 - fines_fraction)³⁻⁶ (Kozeny-Carman)

Fines Sources and Characteristics:
1. Formation Fines:
   - Clay minerals: Illite, kaolinite, smectite, chlorite (1-10 microns)
   - Silt: Quartz, feldspar (5-50 microns)
   - Release mechanism: Disaggregation during fracturing, velocity-induced erosion
   - Mitigation: Clay stabilizers (KCl, polyquaternary amines), controlled drawdown

2. Proppant Crush Fines:
   - API RP 19C crush test: measure % fines below nominal mesh
   - Northern White sand: 5-10% fines at 10,000 psi
   - Regional sand: 12-18% fines at 10,000 psi
   - Ceramic: 1-5% fines at 15,000 psi
   - Mitigation: Select proppant with crush resistance exceeding closure stress

3. Fluid Residue:
   - Gel polymer residue: 10-100 microns (incompletely broken crosslinked gel)
   - Breaker byproducts: Enzyme fragments, oxidizer salts
   - Mitigation: Effective breaker systems (enzymes, oxidizers, temperature-activated)

4. Scale Precipitation:
   - CaCO3 (calcium carbonate): High CO2, high Ca²⁺ produced water
   - BaSO4 (barium sulfate): High Ba²⁺ formation water + sulfate injection water
   - Scale inhibitors: Phosphonates, polymers (inject during flowback)

5. Organic Deposition:
   - Asphaltenes, paraffins, hydrates in oil/gas production
   - Mitigation: Solvents, inhibitors, thermal management

Permeability Impairment Modeling:
Kozeny-Carman Equation:
k = (φ³ / (1-φ)²) × (d²_proppant / 180)
With fines:
k_damaged = k_initial × (1 - fines_volume_fraction)³ × (1 + fines_surface_area_increase)⁻²

Example: 20/40 mesh sand pack, 10% fines by volume (5-micron particles)
- Porosity reduction: φ = 0.35 → 0.31 (fines fill voids)
- Surface area increase: 2x (fine particles have high surface/volume ratio)
- k_damaged / k_initial = 0.30 (70% permeability loss)

Field Observations:
- High-quality Northern White sand + effective cleanup: 5-15% conductivity loss from fines
- Regional sand + poor cleanup: 40-80% conductivity loss
- Uncontrolled flowback (high drawdown): 50-90% conductivity impairment in first weeks (partial recovery over months)

Mitigation Best Practices:
1. Proppant Selection: API RP 19C turbidity <250 FTU, crush <10% fines
2. Fluid Cleanup: Oxidative breakers (persulfate, peroxide) or enzymes, 95%+ gel break
3. Clay Stabilization: 2-3% KCl, quaternary amines in frac fluid and flowback
4. Controlled Drawdown: Limit drawdown to <500 psi during initial 48-72 hours
5. Scale Prevention: Inject scale inhibitors during flowback (100-500 ppm)
6. Gravel Pack Tail-In: Final 5-10% of proppant is coarser mesh (12/20) to filter fines
        """,
        key_factors=[
            "Formation clay content and mineralogy (XRD analysis, petrographic thin sections)",
            "Proppant crush resistance and turbidity (API RP 19C testing)",
            "Fluid system cleanup efficiency (lab break tests, return permeability testing)",
            "Produced water chemistry (scaling potential, TDS, Ca/Ba content)",
            "Drawdown management during flowback (choke back to <500 psi initially)",
            "Economic impact: conductivity loss translates to 10-40% EUR reduction in severe cases"
        ],
        primary_authority=[
            "API RP 19C Section 7 - Turbidity Testing of Proppants",
            "SPE 144101 - Fines Migration and Formation Damage in Hydraulically Fractured Wells",
            "SPE 95287 - Impact of Fluid Cleanup on Long-Term Fracture Conductivity"
        ],
        burden_holder="Completions Engineer / Production Engineer",
        adversary_position="Fines migration is transient; production rates recover after initial flowback period (damage is self-cleaning)",
        counter_arguments=[
            "Many wells show productivity recovery 2-6 months post-flowback (fines clear naturally with production)",
            "Scale inhibitors and clay stabilizers add $10k-30k per well with uncertain benefit",
            "Controlled drawdown extends flowback duration 1-3 days (deferred production, rig costs)",
            "Field comparisons (aggressive vs controlled flowback) show minimal long-term EUR difference"
        ],
        resolution_strategy="Assess fines migration risk based on formation clay content, proppant quality (turbidity, crush), and fluid system; implement clay stabilizers and scale inhibitors in high-risk formations; use controlled drawdown (limit to 500 psi) during initial flowback; monitor production trends (if rates decline >20% after 30 days, consider remediation); validate mitigation effectiveness with offset well data.",
        entity_scope="Completions engineers, production engineers, reservoir engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on fines migration mechanisms and permeability impairment models (extensive lab validation); moderate confidence on field severity (site-specific, varies with formation, fluid, and operational practices).",
        controlling_precedent="API RP 19C turbidity testing and SPE literature establish fines as significant conductivity damage mechanism; field best practices include clay stabilizers, controlled drawdown, and high-quality proppants."
    ),

    DoctrineBlock(
        topic="Long-Term Conductivity Degradation (Crush, Embedment, Diagenesis)",
        keywords=["long term conductivity", "conductivity degradation", "diagenesis", "proppant dissolution", "secondary precipitation", "time dependent"],
        conclusion_template=[
            "Long-term fracture conductivity (months to years of production) degrades by 20-60% from initial post-frac values due to proppant crush under sustained stress, embedment creep in soft formations, chemical diagenesis (proppant dissolution, secondary mineral precipitation), and cyclic stress fatigue.",
            "API RP 19D conductivity tests (50-300 hours) capture initial crush and embedment but underestimate long-term degradation; field data from production logs and pressure transient analysis show conductivity half-life of 6-24 months in many formations.",
            "Design strategies for long-term conductivity preservation include over-propping (2-3x steady-state target to account for degradation), high-crush-resistance proppants (ceramic in high-stress or chemically aggressive environments), and chemical inhibitors (scale, corrosion) to minimize diagenetic reactions."
        ],
        reasoning_framework="""
Long-Term Conductivity Degradation Mechanisms:

1. Progressive Proppant Crush (Time-Dependent):
   - API RP 19C crush test: 2 hours at constant stress (captures initial breakage)
   - Field stress exposure: Years of production at closure stress
   - Cyclic Loading: Pressure cycling during shut-in/production accelerates fatigue fracture
   - Creep: Subcritical crack growth in proppant grains over time
   - Degradation: Additional 10-30% fines generation beyond initial crush over 1-2 years

2. Embedment Creep (Plastic Deformation):
   - Immediate Embedment: Occurs within hours of fracture closure (captured in short-term tests)
   - Creep Embedment: Continued plastic yield of formation rock under sustained stress
   - Time Scale: Months to years (especially in soft formations, coals, chalks)
   - Degradation: Additional 10-40% conductivity loss over 12-24 months

3. Chemical Diagenesis:
   a. Proppant Dissolution:
      - Quartz (sand) dissolution in alkaline brine (pH >9): SiO2 + 2OH⁻ → SiO3²⁻ + H2O
      - Carbonate cements in regional sands: CaCO3 dissolves in CO2-rich or acidic produced water
      - Rate: 0.1-1.0% mass loss per year (depends on pH, T, flow rate)

   b. Secondary Mineral Precipitation:
      - Scale: CaCO3, BaSO4, SrSO4 precipitate in proppant pack pores
      - Silica Diagenesis: Dissolved silica re-precipitates as quartz overgrowths, cementing pack
      - Clays: Authigenic illite, chlorite growth in pore throats
      - Impact: 20-60% permeability reduction over 1-3 years

   c. Corrosion (Ceramic Proppants):
      - Acidic produced water (pH <4) attacks ceramic binder
      - H2S/CO2 environments accelerate corrosion
      - Mitigation: Corrosion-resistant coatings, pH buffering

4. Cyclic Stress Fatigue:
   - Pressure Cycling: Shut-in (ISIP 8,000 psi) → production (BHP 3,000 psi) → shut-in
   - Fatigue Fracture: Proppant grains develop microcracks, eventual failure
   - ISO 13503-2 Method B: 10-cycle stress test (crude approximation)
   - Field Reality: 100s-1000s cycles over well life
   - Degradation: 15-30% additional crush fines beyond static stress

API RP 19D Test Limitations:
- Duration: 50-300 hours (2-12 days) vs years of field exposure
- Stress: Constant stress vs cyclic field stress
- Chemistry: 2% KCl brine vs complex produced fluids (H2S, CO2, organics, scale-forming ions)
- Temperature: Isothermal vs thermal cycling
- Result: API tests underestimate long-term degradation by 30-60%

Field Conductivity Decline Rates:
- High-quality sand, hard formation, benign chemistry: 10-20% loss over 2 years
- Regional sand, moderate formation: 30-50% loss over 2 years
- Soft formation, chemically aggressive (high CO2, H2S): 50-70% loss over 1-2 years
- Ceramic proppant: 5-15% loss over 2 years (superior long-term stability)

Design Strategies:
1. Over-Propping:
   - Design for 2-3x target conductivity to account for degradation
   - Example: Require 100,000 mD-ft steady-state → design for 200,000-300,000 mD-ft initial

2. Proppant Upgrade:
   - High-stress formations (>10,000 psi): Ceramic proppant for long-term crush resistance
   - Chemically aggressive: Ceramic or high-purity quartz (low acid-soluble content)

3. Chemical Inhibition:
   - Scale Inhibitors: Phosphonates, polymers (inject continuously or squeeze treatments)
   - Corrosion Inhibitors: Film-forming amines, phosphate esters
   - pH Control: Buffer produced fluids to pH 6-7 (minimize proppant dissolution)

4. Operational Practices:
   - Minimize Pressure Cycling: Avoid frequent shut-ins (use choke management)
   - Controlled Drawdown: Reduce stress cycling magnitude
   - Scale/Corrosion Monitoring: Water analysis, corrosion coupons, scale deposition tracking
        """,
        key_factors=[
            "Formation closure stress and hardness (higher stress + softer rock = more degradation)",
            "Produced fluid chemistry (pH, CO2, H2S, TDS, scaling ions)",
            "Production pressure profile (cyclic stress accelerates degradation)",
            "Proppant type and quality (ceramic > Northern White > regional sand for long-term stability)",
            "Expected well life (longer life justifies investment in degradation mitigation)",
            "Economic analysis: over-propping or proppant upgrade cost vs NPV of avoided production decline"
        ],
        primary_authority=[
            "API RP 19D - Measuring Long-Term Conductivity of Proppants",
            "ISO 13503-5 - Long-Term Conductivity Testing Procedures",
            "SPE 125987 - Long-Term Conductivity Degradation in Hydraulic Fractures: Mechanisms and Mitigation",
            "SPE 159218 - Field Evidence of Fracture Conductivity Decline from Production Data Analysis"
        ],
        burden_holder="Completions Engineer / Reservoir Engineer",
        adversary_position="Long-term degradation is speculative; most production decline is reservoir depletion, not conductivity loss",
        counter_arguments=[
            "Production decline analysis often attributes all decline to reservoir depletion (difficult to isolate conductivity contribution)",
            "Over-propping adds 20-50% to proppant cost ($200k-500k per well) with uncertain EUR benefit",
            "Ceramic proppant 3-10x cost premium may exceed NPV uplift from reduced degradation",
            "Many fields produce for decades with sand proppant (long-term degradation may be overstated)"
        ],
        resolution_strategy="Use pressure transient analysis or production logs to assess conductivity degradation in offset wells; if degradation >30% over 2 years, implement mitigation (over-propping, ceramic proppant, chemical inhibitors); balance mitigation cost vs NPV of avoided production decline; monitor produced water chemistry and adjust inhibitor treatments as needed.",
        entity_scope="Completions engineers, production engineers, reservoir engineers, geochemists",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence on long-term degradation mechanisms (lab studies validate phenomena); low-moderate confidence on field magnitude (difficult to isolate conductivity decline from reservoir depletion in production data).",
        controlling_precedent="API RP 19D and ISO 13503-5 establish short-term conductivity testing framework; SPE literature and field pressure transient data support 20-60% long-term degradation in many formations, validating over-design strategies."
    ),

    DoctrineBlock(
        topic="In-Basin Sand Mines and Proppant Logistics Optimization",
        keywords=["in-basin sand", "permian basin sand", "local sand mines", "last mile logistics", "silo operations", "proppant delivery"],
        conclusion_template=[
            "In-basin sand mines in the Permian Basin, Eagle Ford, and other major plays offer 40-60% delivered cost reduction vs Northern White sand by eliminating 500-1000 miles of trucking (last-mile logistics represents $15-30/ton of total delivered cost).",
            "Proppant logistics optimization requires coordination of: (1) mine production scheduling, (2) transload/silo capacity and inventory management, (3) just-in-time (JIT) delivery to frac sites, (4) on-site silo operations (loading, blending, dust control), and (5) return logistics for empty equipment.",
            "Trade-offs between in-basin and Northern White sand include: performance gap (10-15% conductivity reduction), supply reliability (local mines may lack capacity during peak demand), and quality consistency (mine-to-mine variability vs established Wisconsin/Illinois suppliers)."
        ],
        reasoning_framework="""
Proppant Delivered Cost Breakdown:
1. Mine Gate Price:
   - Northern White (Wisconsin/Illinois): $25-45/ton FOB mine
   - In-Basin Regional (Permian, Eagle Ford): $15-30/ton FOB mine

2. Transportation to Transload/Silo:
   - Rail: $0.03-0.06/ton-mile (500-1000 miles = $15-60/ton for Northern White)
   - Truck: $0.10-0.15/ton-mile (100-200 miles for in-basin = $10-30/ton)

3. Transload and Storage:
   - Railcar unloading: $3-8/ton
   - Silo storage: $2-5/ton/month
   - Inventory carrying cost: 5-10% annual (capital tied up)

4. Last-Mile Delivery (Transload to Frac Site):
   - Pneumatic truck (25-ton capacity): $2-5/ton for 10-50 mile haul
   - Diesel fuel: $0.08-0.12/ton-mile
   - Driver labor: $50-80/hr

5. On-Site Handling:
   - Silo unloading (blower, dust collection): $1-3/ton
   - Silo rental: $5k-15k/month per silo (amortized across sand volume)

Total Delivered Cost:
- Northern White Sand: $60-90/ton delivered to Permian Basin frac site
- In-Basin Regional Sand: $30-50/ton delivered (40-60% savings)
- Cost Delta: $20-40/ton × 10M lb (5,000 tons) = $100k-200k per well

In-Basin Sand Mine Development (Permian Basin Example):
- Major Operators: Hi-Crush, US Silica, Badger, Covia (Vista), Emerge Energy Services
- Locations: Kermit TX (Winkler County), Monahans TX (Ward County), Crane TX, Odessa TX
- Mine Capacity: 2-8 million tons/year per mine
- Capital Investment: $50-200M per mine (permitting, excavation, wash plant, rail/truck loadout)
- Wash Plant: Removes clay, organics; classifies by mesh size (20/40, 30/50, 40/70)
- Quality Control: API RP 19C testing (crush, turbidity, acid solubility, roundness)

Silo Operations and JIT Delivery:
1. Transload Facility:
   - Receive railcars (100-110 tons each) or trucks
   - Pneumatic unload into storage silos (500-5,000 ton capacity per silo)
   - Inventory management: Track sand by type, mesh size, quality lot

2. Dispatching to Frac Site:
   - Frac schedule: Pump 500k-1.5M lb proppant per stage × 30-50 stages = 7.5-37.5M lb per well
   - Delivery Rate: 3-8 truckloads/hour (75-200 tons/hour) during frac operations (24-72 hours)
   - Buffer Inventory: Maintain 2-4 hours of sand on location (on-site silos or ground storage)

3. On-Site Silo Management:
   - Silo Capacity: 500-2,500 tons per vertical silo (portable units)
   - Dust Control: Baghouse filters, water mist systems (OSHA silica exposure regulations <50 µg/m³)
   - Blender Integration: Gravity feed or pneumatic conveyance to blender hopper
   - Mesh Blending: Mix 20/40 + 40/70 to achieve intermediate size distribution (e.g., 30/50 equivalent)

Logistics Failure Modes and Mitigation:
1. Sand Shortage (Truck Delay):
   - Impact: Frac operations halt (rig standby cost $10k-30k/hour)
   - Mitigation: Over-order 110-120% of planned volume, maintain 4-6 hour buffer inventory on location

2. Quality Variance (Off-Spec Sand):
   - Impact: Conductivity reduction, potential screenout from high fines
   - Mitigation: Batch testing on arrival (turbidity, mesh size distribution), reject loads >10% out of spec

3. Silo Plugging (Moisture, Bridging):
   - Impact: Blender starvation, pump shutdown
   - Mitigation: Heated silos in cold weather, vibrators on silo cones, moisture content <3%

4. Dust Emissions (Regulatory Violation):
   - Impact: OSHA fines, operations shutdown
   - Mitigation: Enclosed transfer points, baghouse dust collectors, water mist, air monitoring

Economic and Operational Trade-offs:
- In-Basin Cost Savings: $100k-200k per well (significant on 20-50 well pads)
- Performance Gap: 10-15% conductivity reduction (may reduce EUR by 5-8% in high-stress formations)
- Supply Risk: In-basin mines can be capacity-limited during peak drilling (fall/spring), Northern White provides backup
- Quality Variability: Local mines may have batch-to-batch inconsistency vs established Northern White suppliers
        """,
        key_factors=[
            "Well count and proppant volume (large programs justify in-basin sand contracts)",
            "Formation closure stress (high stress may require Northern White for performance)",
            "Geographic location (proximity to in-basin mines vs Northern White rail terminals)",
            "Logistics infrastructure (available silos, transload capacity, truck fleet)",
            "Demand seasonality (peak drilling seasons strain in-basin supply)",
            "Economic break-even: in-basin savings vs potential EUR loss from conductivity gap"
        ],
        primary_authority=[
            "SPE 184835 - In-Basin Sand: Economic and Operational Considerations for Permian Basin Completions",
            "Logistics case studies from major sand suppliers (US Silica, Hi-Crush, Covia)",
            "OSHA Silica Exposure Standards - 29 CFR 1926.1153"
        ],
        burden_holder="Completions Engineer / Supply Chain / Operations",
        adversary_position="Logistics complexity and supply risk of in-basin sand outweigh cost savings; Northern White reliability justifies premium",
        counter_arguments=[
            "In-basin sand supply disruptions during peak demand can cost $100k-500k in frac delays (exceeds savings)",
            "Northern White quality consistency reduces screenout risk and QA/QC burden",
            "Rail-based Northern White supply chain more resilient to local weather/road closures",
            "Large integrated operators negotiate Northern White at $50-60/ton delivered (narrows gap vs in-basin)"
        ],
        resolution_strategy="Conduct delivered cost comparison (mine gate + transport + handling) for Northern White vs in-basin sand; assess formation stress and conductivity sensitivity (high stress = Northern White, moderate stress = in-basin acceptable); establish dual-source supply (70-80% in-basin for cost savings, 20-30% Northern White as reliability buffer); implement rigorous QA/QC on in-basin deliveries; optimize silo logistics to minimize on-site inventory and delivery coordination complexity.",
        entity_scope="Completions engineers, supply chain managers, operations coordinators, procurement specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on cost differentials and logistics mechanics (extensive industry data); moderate confidence on performance gap magnitude (varies by formation and mine source quality).",
        controlling_precedent="Permian Basin field practice establishes in-basin sand as dominant for moderate-stress formations (<7,000 psi closure), with Northern White reserved for high-stress or critical wells; logistics best practices include JIT delivery with 4-6 hour buffer inventory."
    ),

    # Additional doctrines to reach 25+ total blocks

    DoctrineBlock(
        topic="Proppant Concentration per Lateral Foot Optimization",
        keywords=["proppant loading", "pounds per foot", "lateral foot", "stage spacing", "cluster spacing", "EUR optimization"],
        conclusion_template=[
            "Optimal proppant loading per lateral foot balances conductivity benefits against diminishing returns and cost; industry practice ranges from 1000 lb/ft (Permian oil) to 2500 lb/ft (Haynesville gas), with EUR sensitivity declining above 2000 lb/ft in most formations.",
            "Stage spacing (300-500 ft typical) and cluster spacing (20-50 ft typical) determine effective propped length per stage; tighter spacing increases proppant intensity but risks stress shadowing and cluster efficiency reduction.",
            "Field data shows EUR uplift of 15-25% when increasing loading from 500 to 1500 lb/ft, but only 5-10% additional uplift from 1500 to 2500 lb/ft, indicating economic break-even around 1500-2000 lb/ft for most plays."
        ],
        reasoning_framework="""
Proppant Loading Calculation:
- Total Proppant per Stage: (PPA average) × (fluid volume per stage) × 8.34 lb/gal
- Lateral Footage per Stage: Stage spacing (typically 300-500 ft in horizontal wells)
- Loading = Total Proppant / Lateral Footage

Example:
- Stage spacing: 400 ft
- Fluid volume: 8,000 bbl (336,000 gal)
- Average PPA: 2.0 lb/gal
- Total proppant: 2.0 × 336,000 = 672,000 lb
- Loading: 672,000 / 400 = 1,680 lb/ft

Industry Benchmarks by Basin:
1. Permian Delaware/Midland (Oil):
   - 1000-1500 lb/ft standard
   - Stage spacing: 300-400 ft
   - Cluster spacing: 25-40 ft
   - Rationale: Moderate stress (4000-6000 psi), economics-driven optimization

2. Eagle Ford (Oil/Gas):
   - 1200-1800 lb/ft
   - Stage spacing: 350-500 ft
   - Cluster spacing: 30-50 ft
   - Rationale: Variable stress (5000-8000 psi), condensate-rich areas higher loading

3. Bakken (Oil):
   - 1000-1500 lb/ft
   - Stage spacing: 300-400 ft
   - Cluster spacing: 25-35 ft
   - Rationale: Low stress (3000-5000 psi), slickwater completions

4. Marcellus (Dry Gas):
   - 1500-2000 lb/ft
   - Stage spacing: 400-500 ft
   - Cluster spacing: 40-60 ft
   - Rationale: Higher stress (6000-8000 psi), gas conductivity requirements

5. Haynesville (Dry Gas):
   - 2000-2500 lb/ft
   - Stage spacing: 400-600 ft
   - Cluster spacing: 50-75 ft
   - Rationale: High stress (8000-12,000 psi), ceramic proppant common

EUR Sensitivity Analysis:
- <500 lb/ft: Severely under-propped (30-50% EUR loss vs optimal)
- 500-1000 lb/ft: Under-propped (15-30% EUR loss)
- 1000-1500 lb/ft: Approaching optimal (5-15% EUR uplift remains)
- 1500-2000 lb/ft: Near-optimal (5-10% EUR uplift at high end)
- 2000-2500 lb/ft: Diminishing returns (2-5% EUR uplift)
- >2500 lb/ft: Minimal additional EUR (<2%), cost-prohibitive for most formations

Economic Break-Even:
- Incremental proppant cost: $40-80/ton delivered (in-basin vs Northern White)
- 500 lb/ft increase = 250 tons per 1,000 ft lateral = $10k-20k incremental cost
- EUR uplift required: 5-10% to justify cost at $70/bbl oil, 3-5% at $100/bbl
- Result: 1500-2000 lb/ft optimal for most oil plays, 2000-2500 lb/ft for gas

Stage Spacing Interaction:
- Tighter spacing (200-300 ft): Higher proppant intensity (lb/ft), but more stages (higher total cost)
- Wider spacing (500-700 ft): Lower intensity, fewer stages, risk of unpropped intervals between stages
- Stress Shadow Effects: <300 ft spacing creates stress interference, reduces fracture width/height
- Optimal: 350-450 ft spacing for most formations (balance proppant efficiency and fracture geometry)
        """,
        key_factors=[
            "Formation closure stress and permeability (high stress/low perm requires higher loading)",
            "Fluid type and EUR (oil vs gas, liquids-rich vs dry gas economics)",
            "Stage and cluster spacing (affects effective propped length)",
            "Proppant delivered cost (in-basin vs Northern White, ceramic premium)",
            "Offset well EUR vs proppant loading correlation",
            "NPV optimization: balance incremental proppant cost vs EUR uplift"
        ],
        primary_authority=[
            "SPE 152596 - Optimization of Proppant Loading in Unconventional Reservoirs",
            "SPE 184862 - Impact of Stage Spacing and Proppant Intensity on EUR in Permian Basin",
            "URTeC 2902983 - Economic Analysis of Proppant Loading Strategies Across Major US Plays"
        ],
        burden_holder="Completions Engineer / Reservoir Engineer / Economics",
        adversary_position="Maximize proppant loading (2500+ lb/ft) to ensure conductivity; cost concerns are secondary to production",
        counter_arguments=[
            "Diminishing EUR returns above 2000 lb/ft do not justify incremental proppant cost ($200k-500k per well)",
            "Over-propping can exacerbate stress shadowing and reduce overall stimulated reservoir volume",
            "Many operators achieve top-quartile EURs with 1000-1500 lb/ft (execution and geology dominate over proppant intensity)",
            "Parent-child well interactions and depletion effects may limit EUR uplift from additional proppant"
        ],
        resolution_strategy="Analyze offset well EUR vs proppant loading; identify break-even loading where marginal EUR uplift equals marginal cost; design completions to 1500-2000 lb/ft for most oil plays, 2000-2500 lb/ft for high-stress gas plays; validate with ongoing field trials comparing loading strategies; adjust based on basin-specific EUR sensitivities and economic conditions.",
        entity_scope="Completions engineers, reservoir engineers, completion optimization teams, economics/planning",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on industry loading benchmarks (extensive field data); moderate confidence on EUR sensitivity curves (vary by basin, operator completion design, reservoir quality).",
        controlling_precedent="Permian Basin field practice establishes 1000-1500 lb/ft as economic optimum for oil wells; gas plays (Marcellus, Haynesville) support 2000-2500 lb/ft due to higher stress and gas productivity requirements."
    ),

    DoctrineBlock(
        topic="Tail-In Strategy with Higher Concentration Proppant",
        keywords=["tail-in", "final stage", "near wellbore", "maximum concentration", "3.0 PPA", "fracture tip"],
        conclusion_template=[
            "Tail-in with elevated proppant concentration (2.5-3.5 PPA) in the final 10-20% of pumping ensures fracture tip and near-wellbore proppant coverage, maximizing effective fracture length and near-wellbore conductivity where flow convergence is highest.",
            "Higher PPA tail-in also reduces risk of unpropped fracture tip (which would otherwise close without conductivity support) and provides high-density proppant pack near the wellbore to withstand erosion and proppant flowback during production.",
            "Tail-in design balances screenout risk (high PPA in narrow fracture sections) against performance benefit; typical approach is gradual ramp to 2.5-3.0 PPA over final 50-100 bbl, with option to spike to 3.5+ PPA in last 10-20 bbl if pressure remains stable."
        ],
        reasoning_framework="""
Tail-In Rationale:

1. Fracture Tip Coverage:
   - Fracture propagates during pumping; tip is farthest from wellbore
   - Low PPA early in stage may not reach tip before closure begins
   - High PPA tail-in ensures proppant reaches tip before fracture closes
   - Result: Propped length = created length (no unpropped tip section)

2. Near-Wellbore Conductivity:
   - Flow convergence near wellbore creates highest velocity and pressure drop
   - Conductivity bottleneck at wellbore can limit production (choke point)
   - High PPA near wellbore creates thick, high-permeability pack
   - Target: 3-6 lb/ft² proppant concentration near wellbore (vs 1-2 lb/ft² in fracture body)

3. Proppant Pack Stabilization:
   - High-density pack resists flowback during initial production
   - Interlocking proppant grains provide mechanical stability
   - Reduces proppant production and tubular erosion risk

Tail-In Design Parameters:

1. Timing and Volume:
   - Tail-in begins at 80-90% of planned fluid volume
   - Duration: Final 10-20% of fluid (e.g., 800-1,600 gal in 8,000 gal stage)
   - Allows sufficient volume to push high-PPA slugs into fracture

2. PPA Ramp Profile:
   - Bulk stage: 2.0-2.5 PPA (60-80% of proppant mass)
   - Tail-in initiation: Ramp 2.5 → 2.75 → 3.0 PPA (gradual, monitor pressure)
   - Final push: Spike to 3.0-3.5 PPA (last 50-100 bbl) if pressure stable
   - Aggressive designs: 4.0 PPA spikes in last 10-20 bbl (ultra-high near-wellbore loading)

3. Pressure Monitoring:
   - Stable or declining net pressure: Safe to increase PPA
   - Rising net pressure (>200 psi increase): Hold PPA or reduce (screenout warning)
   - Pressure spike (>500 psi rapid rise): Stop proppant, pump flush (screenout imminent)

4. Mesh Size Strategy:
   - Consistent mesh: Same size throughout (20/40 or 30/50)
   - Tail-in with smaller mesh: Final 10-20% use 40/70 or 100 mesh (ensures tip coverage in narrow sections)
   - Trade-off: Smaller mesh lower settling velocity (better tip penetration) but lower conductivity

Operational Execution:

1. Blender Programming:
   - Pre-program PPA ramp schedule (time-based or volume-based)
   - Real-time adjustment: Frac engineer overrides if pressure trends adverse
   - Automated safety limits: Max PPA cutoff at 3.5-4.0 to prevent equipment damage

2. Proppant Inventory:
   - Ensure sufficient proppant on location for tail-in (10-20% of stage total)
   - Example: 800,000 lb stage requires 80,000-160,000 lb tail-in reserves

3. Flush Strategy:
   - After final high-PPA slug, pump clean fluid "overflight" (50-200 bbl)
   - Pushes tail-in proppant into fracture (prevent wellbore screenout)
   - Overflight volume = wellbore volume + 50-100 bbl safety margin

Field Performance:

1. Success Indicators:
   - Pressure stable or declining during tail-in (no screenout)
   - Post-frac production logs show proppant to TD (fracture tip propped)
   - Production rates match or exceed pre-frac models (effective length achieved)

2. Failure Modes:
   - Premature screenout during tail-in (stage incomplete, lost footage)
   - Excessive overflight dilutes tail-in concentration (reduces near-wellbore loading)
   - Insufficient tail-in volume (fracture tip remains unpropped)

Basin-Specific Practices:

- Permian Basin: 2.5-3.0 PPA tail-in standard, 10-15% of fluid volume
- Marcellus: 3.0-3.5 PPA tail-in, 15-20% of fluid (high stress requires aggressive loading)
- Haynesville: 3.0-4.0 PPA tail-in with ceramic (ultra-high stress, premium proppant)
- Eagle Ford: 2.5-3.0 PPA, 10-15% volume (moderate stress, slickwater fracs)
        """,
        key_factors=[
            "Formation fluid-loss coefficient (high fluid-loss = conservative tail-in to avoid screenout)",
            "Net pressure response during bulk pumping (stable = aggressive tail-in, rising = conservative)",
            "Fracture complexity (natural fractures may restrict high-PPA penetration)",
            "Target propped length (ensure tail-in volume sufficient to reach fracture tip)",
            "Near-wellbore conductivity requirements (high productivity wells justify ultra-high PPA)",
            "Proppant availability and blender capacity (ensure equipment can deliver 3.0+ PPA)"
        ],
        primary_authority=[
            "SPE 119900 - Impact of Proppant Concentration on Fracture Conductivity",
            "SPE 166505 - Tail-In Design Optimization for Unconventional Completions",
            "Field best practices from major operators (EOG, Pioneer, ConocoPhillips)"
        ],
        burden_holder="Completions Engineer / Frac Operations Engineer",
        adversary_position="Tail-in at 2.5 PPA is sufficient; higher concentrations risk screenout without proportional EUR benefit",
        counter_arguments=[
            "3.5-4.0 PPA tail-in significantly increases screenout risk (potential $100k-300k stage loss)",
            "Near-wellbore conductivity often dominated by wellbore skin and perforation efficiency (high-PPA tail-in marginal benefit)",
            "Many high-performing wells use 2.0-2.5 PPA throughout with no tail-in ramp (simplicity and reliability)",
            "Incremental proppant cost for aggressive tail-in ($10k-30k) may not translate to measurable EUR uplift"
        ],
        resolution_strategy="Design tail-in PPA based on offset well screenout history and real-time pressure response; standard approach is 2.5-3.0 PPA over final 10-15% of fluid volume, with option to spike to 3.5 PPA if pressure stable; monitor net pressure closely during tail-in and reduce PPA immediately if pressure rises >200 psi; validate tail-in effectiveness with production logs (proppant coverage) and initial production rates (near-wellbore conductivity).",
        entity_scope="Completions engineers, frac operations engineers, real-time monitoring specialists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence on tail-in benefits for fracture tip coverage and near-wellbore conductivity; moderate confidence on optimal PPA targets (3.0 vs 3.5+ PPA trade-offs vary by formation and operator risk tolerance).",
        controlling_precedent="Industry practice in major unconventional plays supports 2.5-3.0 PPA tail-in as standard; aggressive operators (EOG, Pioneer) demonstrate 3.5-4.0 PPA spikes in select high-value wells."
    )
]

# ═══════════════════════════════════════════════════════════════════════════
# ENGINE STATE
# ═══════════════════════════════════════════════════════════════════════════

class EngineState:
    def __init__(self):
        self.start_time = datetime.now()
        self.total_queries = 0
        self.total_latency_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.audit_log: List[Dict[str, Any]] = []

engine_state = EngineState()

# ═══════════════════════════════════════════════════════════════════════════
# CORE INTELLIGENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def normalize_query(query: str) -> str:
    """Semantic normalization of proppant terminology."""
    normalized = query.lower()

    # Proppant type normalization
    normalized = normalized.replace("northern white sand", "wisconsin_sand")
    normalized = normalized.replace("ottawa sand", "wisconsin_sand")
    normalized = normalized.replace("regional sand", "basin_sand")
    normalized = normalized.replace("brown sand", "basin_sand")
    normalized = normalized.replace("in-basin sand", "basin_sand")
    normalized = normalized.replace("resin coated", "rcs")
    normalized = normalized.replace("resin-coated", "rcs")
    normalized = normalized.replace("lightweight ceramic", "lwc")
    normalized = normalized.replace("intermediate strength", "isp")
    normalized = normalized.replace("high strength ceramic", "hsp")
    normalized = normalized.replace("sintered bauxite", "hsp")

    # Mesh size normalization
    normalized = normalized.replace("20/40 mesh", "2040_mesh")
    normalized = normalized.replace("30/50 mesh", "3050_mesh")
    normalized = normalized.replace("40/70 mesh", "4070_mesh")
    normalized = normalized.replace("100 mesh", "100_mesh")

    # Technical terms
    normalized = normalized.replace("api rp 19c", "api_rp19c")
    normalized = normalized.replace("iso 13503", "iso13503")
    normalized = normalized.replace("pounds per gallon", "ppa")
    normalized = normalized.replace("proppant concentration", "ppa")

    return normalized

def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks."""
    query_norm = normalize_query(query)
    query_terms = set(query_norm.split())

    scored_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        # Keyword matching
        keyword_score = sum(1 for kw in doctrine.keywords if kw.lower() in query_norm)

        # Topic relevance
        topic_terms = set(doctrine.topic.lower().split())
        topic_score = len(query_terms & topic_terms)

        total_score = (keyword_score * 2) + topic_score
        if total_score > 0:
            scored_doctrines.append((total_score, doctrine))

    scored_doctrines.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored_doctrines[:top_k]]

def generate_response(
    query: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    triggered_doctrines: List[DoctrineBlock]
) -> Tuple[str, str, ConfidenceLevel]:
    """Generate response based on triggered doctrines."""

    if not triggered_doctrines:
        return (
            "Insufficient doctrine coverage for this proppant query.",
            "No relevant proppant engineering doctrines were triggered. Query may be outside engine scope (FRAC02 covers proppant selection, mesh sizing, API testing, transport, embedment, conductivity, logistics).",
            ConfidenceLevel.DISCLOSURE
        )

    primary_doctrine = triggered_doctrines[0]

    # Build conclusion
    if mode == ResponseMode.FAST:
        conclusion = primary_doctrine.conclusion_template[0]
    else:
        conclusion = " ".join(primary_doctrine.conclusion_template)

    # Build reasoning
    reasoning_parts = [primary_doctrine.reasoning_framework]

    if mode == ResponseMode.DEFENSE or mode == ResponseMode.MEMO:
        reasoning_parts.append(f"\n\nKEY FACTORS:\n" + "\n".join(f"- {kf}" for kf in primary_doctrine.key_factors))
        reasoning_parts.append(f"\n\nAUTHORITY:\n" + "\n".join(f"- {auth}" for auth in primary_doctrine.primary_authority))

    if mode == ResponseMode.MEMO:
        reasoning_parts.append(f"\n\nADVERSARY POSITION: {primary_doctrine.adversary_position}")
        reasoning_parts.append(f"\n\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"- {ca}" for ca in primary_doctrine.counter_arguments))
        reasoning_parts.append(f"\n\nRESOLUTION STRATEGY: {primary_doctrine.resolution_strategy}")

    reasoning = "".join(reasoning_parts)

    return conclusion, reasoning, primary_doctrine.confidence

def apply_epistemic_guardrails(conclusion: str, reasoning: str, confidence: ConfidenceLevel) -> List[str]:
    """Apply epistemic safety guardrails."""
    caveats = []

    if confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
        caveats.append("This analysis involves technical assumptions that may vary by formation and operating conditions.")

    if confidence == ConfidenceLevel.DISCLOSURE:
        caveats.append("Limited doctrine coverage - consult proppant supplier technical data sheets and API RP 19C/19D testing for site-specific validation.")

    # Check for banned absolute claims
    banned_phrases = ["always", "never", "guaranteed", "certain", "impossible", "must"]
    for phrase in banned_phrases:
        if phrase in conclusion.lower() or phrase in reasoning.lower():
            caveats.append(f"Note: Avoid absolute language ('{phrase}') - proppant performance is context-dependent.")

    return caveats

def calculate_determinism_hash(query: str, conclusion: str, reasoning: str) -> str:
    """Calculate SHA-256 hash for response determinism."""
    content = f"{query}|{conclusion}|{reasoning}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="FRAC02 - Proppant Selection & Performance Engine | TIE Gold Standard"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint - three-layer response with TIE-20 components."""
    start_time = datetime.now()
    query_id = str(uuid.uuid4())

    logger.info(f"Query {query_id}: {request.query} | Mode: {request.mode} | Zone: {request.zone}")

    # Layer 1: Doctrine Cache (0-200ms)
    triggered_doctrines = search_doctrines(request.query, top_k=3)

    if triggered_doctrines:
        engine_state.cache_hits += 1
        logger.info(f"Cache HIT - {len(triggered_doctrines)} doctrines triggered")
    else:
        engine_state.cache_misses += 1
        logger.warning(f"Cache MISS - no doctrines matched query")

    # Generate response
    conclusion, reasoning, confidence = generate_response(
        request.query,
        request.mode,
        request.zone,
        triggered_doctrines
    )

    # Apply epistemic guardrails
    epistemic_caveats = apply_epistemic_guardrails(conclusion, reasoning, confidence)

    # Collect authority citations
    authority_citations = []
    for doctrine in triggered_doctrines:
        authority_citations.extend(doctrine.primary_authority)
    authority_citations = list(set(authority_citations))[:5]  # Dedupe, top 5

    # Calculate determinism hash
    det_hash = calculate_determinism_hash(request.query, conclusion, reasoning)

    # Calculate latency
    latency_ms = (datetime.now() - start_time).total_seconds() * 1000

    # Update telemetry
    engine_state.total_queries += 1
    engine_state.total_latency_ms += latency_ms

    # Audit trail
    audit_entry = {
        "query_id": query_id,
        "timestamp": datetime.now().isoformat(),
        "query": request.query,
        "mode": request.mode,
        "zone": request.zone,
        "triggered_doctrines": [d.topic for d in triggered_doctrines],
        "confidence": confidence,
        "latency_ms": latency_ms
    }
    engine_state.audit_log.append(audit_entry)

    logger.info(f"Query {query_id} complete | Latency: {latency_ms:.1f}ms | Confidence: {confidence}")

    return QueryResponse(
        query_id=query_id,
        conclusion=conclusion,
        reasoning=reasoning,
        confidence=confidence,
        triggered_doctrines=[d.topic for d in triggered_doctrines],
        epistemic_caveats=epistemic_caveats,
        authority_citations=authority_citations,
        determinism_hash=det_hash,
        latency_ms=latency_ms,
        mode=request.mode,
        zone=request.zone
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    uptime = (datetime.now() - engine_state.start_time).total_seconds()
    avg_latency = (
        engine_state.total_latency_ms / engine_state.total_queries
        if engine_state.total_queries > 0
        else 0.0
    )
    cache_hit_rate = (
        engine_state.cache_hits / (engine_state.cache_hits + engine_state.cache_misses)
        if (engine_state.cache_hits + engine_state.cache_misses) > 0
        else 0.0
    )

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=uptime,
        total_queries=engine_state.total_queries,
        avg_latency_ms=avg_latency,
        cache_hit_rate=cache_hit_rate
    )

@app.get("/doctrines")
async def list_doctrines():
    """List all loaded doctrine topics."""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "authority_count": len(d.primary_authority)
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/")
async def root():
    """Engine information endpoint."""
    return {
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": VERSION,
        "port": PORT,
        "status": "operational",
        "doctrines": len(DOCTRINE_CACHE),
        "capabilities": [
            "Proppant type selection (sand, RCS, ceramic, sintered bauxite)",
            "Mesh size optimization (20/40, 30/50, 40/70, 100 mesh)",
            "API RP 19C/ISO 13503-2 testing and specifications",
            "Proppant concentration scheduling and PPA optimization",
            "Proppant transport and settling in non-Newtonian fluids",
            "Embedment analysis in soft formations",
            "Fines migration and proppant pack damage",
            "Long-term conductivity degradation mechanisms",
            "Regional sand economics and in-basin logistics",
            "Proppant loading optimization per lateral foot",
            "Tail-in strategy with elevated concentration"
        ],
        "endpoints": {
            "query": "/query (POST)",
            "health": "/health (GET)",
            "doctrines": "/doctrines (GET)"
        }
    }

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} proppant doctrine blocks")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
