"""
ENRG06 Geothermal Energy Systems Intelligence Engine
TIE-Grade Domain Expert: Geothermal resource assessment, well design,
power plant technology, enhanced geothermal systems (EGS), heat pumps

Port: 9241
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# ENUMS & DATA CLASSES
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
    RESOURCE_ASSESSMENT = "RESOURCE_ASSESSMENT"
    WELL_DESIGN = "WELL_DESIGN"
    POWER_PLANT_TECH = "POWER_PLANT_TECH"
    RESERVOIR_ENGINEERING = "RESERVOIR_ENGINEERING"
    EGS_DEVELOPMENT = "EGS_DEVELOPMENT"
    HEAT_PUMP_SYSTEMS = "HEAT_PUMP_SYSTEMS"
    SCALING_CORROSION = "SCALING_CORROSION"
    INDUCED_SEISMICITY = "INDUCED_SEISMICITY"
    ENVIRONMENTAL_IMPACT = "ENVIRONMENTAL_IMPACT"
    ECONOMICS_LCOE = "ECONOMICS_LCOE"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    DESIGN = "DESIGN"
    OPERATIONS = "OPERATIONS"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    fragility_score: float = 0.5


@dataclass
class TelemetryEvent:
    timestamp: str
    query: str
    mode: str
    latency_ms: float
    doctrines_triggered: List[str]
    cache_hit: bool
    confidence: str
    zone: str
    determinism_hash: str


# ============================================================================
# DOCTRINE CACHE - 25+ GEOTHERMAL EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="USGS Geothermal Resource Classification System",
        keywords=["resource classification", "USGS", "identified", "undiscovered", "reserves", "proven", "probable", "possible"],
        conclusion_template="Geothermal resources are classified using the USGS framework into identified (proven, probable, possible) and undiscovered categories. Classification determines project financing viability, regulatory approvals, and risk profiles for development.",
        reasoning_framework="""
The USGS circular 726 and 790 establish a three-tier classification:
1. Proven reserves: drilled confirmation, production test data, reservoir modeling complete, >90% confidence in recovery
2. Probable reserves: limited drilling, geological/geophysical evidence, reservoir boundaries inferred, 50-90% confidence
3. Possible reserves: regional heat flow data, geological analogs, no direct drilling, <50% confidence

Assessment factors:
- Temperature at depth (measured or inferred from gradient)
- Permeability (transmissivity from well tests or seismic)
- Reservoir volume (geological model boundaries)
- Recharge rate (tracer studies, pressure maintenance)
- Fluid chemistry (silica geothermometry, gas composition)

Monte Carlo simulation required for probable/possible categories.
Reserve booking follows SEC guidelines for public companies.
Bankability threshold typically requires proven reserves for >70% of project capacity.
        """,
        key_factors=[
            "Drilling confirmation (number of wells, spacing)",
            "Temperature profile (bottom-hole temps, gradient)",
            "Well test data (flow rates, drawdown, buildup)",
            "Reservoir volume estimation (geological model)",
            "Recovery factor (typically 10-25% for hydrothermal)",
            "Economic cutoff (minimum plant size, LCOE threshold)"
        ],
        primary_authority=[
            "USGS Circular 726 - Assessment of Geothermal Resources (1978)",
            "USGS Circular 790 - Assessment of Geothermal Resources (1979)",
            "SEC Staff Accounting Bulletin Topic 12 - Oil and Gas Producing Activities"
        ],
        burden_holder="Developer to prove reserves adequate for project life",
        adversary_position="Lenders require proven reserves; regulators may challenge volumetric assumptions",
        counter_arguments=[
            "Sparse drilling leaves uncertainty in lateral extent",
            "Temperature may decline over production (requires reinjection modeling)",
            "Permeability can be fracture-dominated (heterogeneous)",
            "Recharge rates difficult to quantify without long-term production history"
        ],
        resolution_strategy="Phase development: Phase 1 on proven reserves, expansion on probable once production confirms. Use conservative recovery factors (10-15%). Independent reservoir engineer certification.",
        entity_scope="All geothermal projects seeking financing or regulatory approval",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="USGS framework is industry-standard for reserve classification; conservative application minimizes financing risk",
        controlling_precedent="USGS Circular 790 (1979) established volumetric method for geothermal reserves",
        issue_category=IssueCategory.RESOURCE_ASSESSMENT,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Geothermal Gradient and Heat Flow Assessment",
        keywords=["geothermal gradient", "heat flow", "temperature profile", "conductive gradient", "basement depth", "thermal conductivity"],
        conclusion_template="Geothermal gradient (degC/km) and heat flow (mW/m2) determine resource temperature at economically drillable depths. Normal continental gradient is 25-30 degC/km; high-grade resources exceed 50 degC/km. Flash steam requires >180 degC, binary cycle viable at 100-180 degC.",
        reasoning_framework="""
Temperature at depth calculation:
T(z) = T_surface + Gradient * z
where z = depth in km, Gradient in degC/km

Heat flow q = k * dT/dz
where k = thermal conductivity (W/m/K), dT/dz = gradient

Assessment methods:
1. Direct measurement: Bottom-hole temperature (BHT) logs in exploration wells
   - Correct for drilling disturbance (Horner plot extrapolation)
   - Multiple logs over time to equilibrium
2. Geochemical: Silica and cation geothermometers
   - Quartz geothermometer: T = 1309/(5.19 - log(SiO2)) - 273.15
   - Na-K geothermometer: T = 1217/(log(Na/K) + 1.483) - 273.15
3. Geophysical: Magnetotelluric (MT) surveys for resistivity anomalies
   - Low resistivity indicates hot brine or partial melt
   - 3D inversion for subsurface temperature structure

Power plant technology selection:
- >240 degC: Dry steam (rare, e.g., The Geysers)
- 180-240 degC: Flash steam (single or double flash)
- 100-180 degC: Binary cycle (ORC or Kalina)
- 50-100 degC: Enhanced binary or direct use
- <50 degC: Ground-source heat pumps only

Economic depth limit typically 3-4 km for current drilling technology.
        """,
        key_factors=[
            "Measured BHT data (corrected for thermal equilibration)",
            "Thermal conductivity of rock formations (lab measurements)",
            "Basement depth and geology (sedimentary insulation effect)",
            "Magmatic heat source proximity (Quaternary volcanism)",
            "Hydrothermal convection (can steepen gradients locally)",
            "Regional tectonic setting (extensional > compressional for heat flow)"
        ],
        primary_authority=[
            "Muffler & Cataldi (1978) - Methods for regional assessment of geothermal resources",
            "Fournier (1977) - Chemical geothermometers and mixing models",
            "DiPippo (2012) - Geothermal Power Plants 3rd ed."
        ],
        burden_holder="Developer to demonstrate sufficient temperature at drillable depth",
        adversary_position="Regulators may require conservative gradient assumptions; community concerned about resource depletion",
        counter_arguments=[
            "Sparse well control may miss lateral temperature variations",
            "Geochemical thermometers assume water-rock equilibrium (may not be met)",
            "Convective systems can have irregular temperature profiles",
            "Drilling deeper increases costs exponentially (25-50% cost increase per km)"
        ],
        resolution_strategy="Multi-method temperature assessment (BHT + geochemistry + geophysics). Staged drilling: slim holes first, then production-size. Conservative gradient for financing, best estimate for design.",
        entity_scope="All geothermal exploration projects pre-drilling",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gradient assessment is standard exploration practice; uncertainty quantified via Monte Carlo",
        controlling_precedent="Muffler & Cataldi (1978) volumetric method remains industry standard",
        issue_category=IssueCategory.RESOURCE_ASSESSMENT,
        fragility_score=0.4
    ),

    DoctrineBlock(
        topic="Flash Steam vs Binary Cycle Technology Selection",
        keywords=["flash steam", "binary cycle", "ORC", "organic rankine cycle", "isobutane", "separation", "single flash", "double flash"],
        conclusion_template="Flash steam plants are economically superior for high-temperature resources (>180 degC) due to simpler design and no working fluid costs. Binary cycle required for moderate temps (100-180 degC) but adds working fluid inventory and heat exchanger costs. Double flash adds 15-25% power output vs single flash for same resource.",
        reasoning_framework="""
Flash steam process:
1. High-pressure geothermal brine enters separator
2. Pressure drop causes partial vaporization (flashing)
3. Steam drives turbine, separated brine reinjected or sent to 2nd flash stage
4. Efficiency 10-20% (limited by non-condensable gases, ambient temp)

Single flash: One separation stage at ~5-7 bar
Double flash: Two stages (high ~5 bar, low ~1.2 bar) for 15-25% more power

Binary cycle (ORC) process:
1. Geothermal brine transfers heat to working fluid (isobutane, R245fa, etc.) via heat exchanger
2. Working fluid vaporizes at lower temp than water (higher efficiency at <180 degC)
3. Vapor drives turbine, condenses, pumps back to heat exchanger
4. Geothermal brine reinjected (closed loop, zero emissions)
5. Efficiency 8-15% (limited by Carnot efficiency, pinch point in HX)

Decision criteria:
Temperature >180 degC: Flash steam (lower capital cost, simpler)
100-180 degC: Binary cycle (only option)
High non-condensables (>5% CO2): Binary preferred (no steam turbine issues)
Environmental restrictions: Binary (zero emissions, closed loop)

Capital cost (USD/kW installed):
Flash steam: $2500-4500/kW
Binary cycle: $3500-6000/kW (higher due to heat exchangers, working fluid)

Operating costs:
Flash: Higher parasitic load (gas extraction), scaling in turbines
Binary: Working fluid inventory, heat exchanger fouling
        """,
        key_factors=[
            "Geothermal fluid temperature (determines max Carnot efficiency)",
            "Non-condensable gas content (CO2, H2S impair flash turbines)",
            "Fluid chemistry (silica/calcite scaling risk in flash)",
            "Ambient temperature (affects condenser performance)",
            "Environmental permits (air emissions limit flash in some regions)",
            "Project scale (economies of scale favor flash for >20 MW)"
        ],
        primary_authority=[
            "DiPippo (2012) - Geothermal Power Plants ch 5-8",
            "EPRI (2011) - Geothermal Power Plant Performance Handbook",
            "GEA Best Practices (2016) - Power plant design"
        ],
        burden_holder="Developer to justify technology choice in feasibility study",
        adversary_position="Environmental groups may oppose flash due to emissions; lenders prefer proven flash technology",
        counter_arguments=[
            "Binary plants have longer equipment life (no steam erosion)",
            "Flash plants produce H2S odor (community opposition)",
            "Binary allows utilization of lower-temp wells (more drilling targets)",
            "Hybrid flash-binary captures tail heat (optimizes total output)"
        ],
        resolution_strategy="Detailed techno-economic model comparing LCOE for both technologies. If temp >180 degC and emissions acceptable, flash preferred. If 150-180 degC, run hybrid sensitivity. Binary mandatory below 150 degC.",
        entity_scope="All geothermal power projects >5 MW",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Technology selection methodology well-established in industry; LCOE comparison standard practice",
        controlling_precedent="DiPippo (2012) technology selection framework used globally",
        issue_category=IssueCategory.POWER_PLANT_TECH,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Enhanced Geothermal Systems (EGS) Hydraulic Stimulation",
        keywords=["EGS", "enhanced geothermal", "hydraulic stimulation", "fracturing", "engineered reservoir", "HDR", "hot dry rock", "microseismic"],
        conclusion_template="EGS creates permeability in low-permeability hot rock via hydraulic stimulation. Requires injection pressures exceeding minimum principal stress (typically 50-80 MPa at 3-5 km depth). Success depends on pre-existing fracture networks and stress regime. Induced seismicity is primary risk requiring traffic light protocol.",
        reasoning_framework="""
EGS concept:
1. Drill into hot crystalline rock (typically granite) at 3-5 km depth
2. Hydraulically fracture to create connected flow paths
3. Drill production wells into stimulated volume
4. Circulate water: cold injection well -> hot rock -> production well -> power plant -> reinject

Stimulation process:
- Inject water at high pressure (Pinj > sigma_min + tensile strength)
- Typical volumes: 10,000-50,000 m3 per stage
- Pressure monitoring: Avoid exceeding sigma_H (maximum horizontal stress) to prevent vertical fractures
- Microseismic monitoring: Map fracture growth in real-time (15-30 geophones)
- Shear stimulation preferred over tensile (creates rough fractures with more surface area)

Key parameters:
- Minimum principal stress: sigma_min = rho*g*z + P_pore - alpha*P_pore (typical 15-25 MPa/km depth)
- Fracture aperture: typically 0.1-1.0 mm after stimulation
- Stimulated volume: target 0.1-0.5 km3 for 5-10 MW plant
- Impedance: P_inj / Q_inj, monitor for declining impedance (improving permeability)

Induced seismicity management:
- Traffic light protocol: Green (M<1.5), Amber (1.5<M<2.5, reduce rate), Red (M>2.5, stop)
- Seismic moment vs injected volume: log(M0) ~ log(V_inj), typical b-value 1.0-1.5
- Avoid proximity to mapped faults (>1 km buffer)

Success rate:
- Commercial EGS projects: ~30% achieve target flow rates (10-50 kg/s per well)
- Technical challenges: short-circuiting (thermal breakthrough <5 years), high parasitic pumping load
        """,
        key_factors=[
            "In-situ stress regime (determined from LOT, FIT, breakout analysis)",
            "Pre-existing fracture density (image logs, core analysis)",
            "Rock mechanical properties (Young's modulus, Poisson's ratio, tensile strength)",
            "Injection rate and pressure control (real-time adjustment)",
            "Microseismic monitoring array geometry (adequate coverage of stimulated volume)",
            "Distance to population centers (seismic risk perception)"
        ],
        primary_authority=[
            "Tester et al. (2006) - The Future of Geothermal Energy (MIT report)",
            "Majer et al. (2007) - Induced seismicity associated with EGS",
            "DOE GTO (2019) - GeoVision report on EGS potential"
        ],
        burden_holder="Developer to demonstrate seismic risk is manageable and reservoir can sustain production",
        adversary_position="Public concerned about earthquakes; regulators require extensive monitoring and protocols",
        counter_arguments=[
            "Basel, Switzerland EGS project canceled after M3.4 event (2006)",
            "Thermal drawdown faster than predicted in many pilots",
            "High pump power (20-30% of gross power) reduces net output",
            "Uncertain reservoir longevity (few projects have >10 year history)"
        ],
        resolution_strategy="Adaptive traffic light protocol with automated shutdown. Start with low injection rates, ramp up slowly while monitoring seismicity. Select sites in low-seismic-hazard regions. Extensive public engagement before stimulation. Insurance for induced seismic events.",
        entity_scope="EGS projects in low-permeability crystalline basement",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="EGS technology is pre-commercial; success rates low; seismic risk requires careful management",
        controlling_precedent="MIT Future of Geothermal Energy (2006) outlined EGS potential but acknowledged challenges",
        issue_category=IssueCategory.EGS_DEVELOPMENT,
        fragility_score=0.7
    ),

    DoctrineBlock(
        topic="Geothermal Well Design for High Temperature Environments",
        keywords=["well design", "casing", "cement", "thermal expansion", "expansion joints", "slotted liner", "high temperature", "lost circulation"],
        conclusion_template="Geothermal wells require specialized design to handle temperatures up to 350 degC, thermal expansion, corrosive fluids, and lost circulation zones. Key elements: multiple casing strings, high-temp cement (Class G with silica flour), expansion joints or slotted liners, and wellhead rated for 200+ degC.",
        reasoning_framework="""
Typical geothermal well casing program (3 km depth):
1. Conductor casing: 20-24 inch, 30-50 m depth, cement to surface
2. Surface casing: 13-3/8 inch, 300-500 m, isolate freshwater aquifers
3. Intermediate casing: 9-5/8 inch, 1000-1500 m, seal lost circulation zones
4. Production casing: 7 inch, to TD or to production zone
5. Slotted liner: 5-1/2 inch across production interval (allows fluid entry)

Thermal expansion challenges:
- Steel thermal expansion coefficient: ~12e-6 /degC
- 3 km well heated from 20 degC to 250 degC: expansion = 3000m * 230K * 12e-6 = 8.3 m
- Without expansion accommodation, casing will buckle or part at connections

Solutions:
A) Expansion joints: telescoping sections allow axial movement (10-20 m capacity)
B) Slotted liner: slots cut in casing allow radial expansion, hung from above (not cemented)
C) Compliant cement: latex-modified cement allows small deformation
D) Pre-stressing: heat well before cementing production casing

Cement design:
- Class G cement + 35-40% silica flour (prevents strength retrogression >110 degC)
- Retarder to extend thickening time (formations may be >100 degC)
- Lost circulation materials (LCM): cellophane flakes, nut shells, sized calcium carbonate
- Weighted cement (>16 ppg) to combat gas migration

Lost circulation mitigation:
- Fracture gradient often exceeded in geothermal (high temp reduces rock strength)
- Drill with aerated fluid or foam to reduce ECD
- Cement in stages: set plug, drill out, continue
- Expendable casing if total losses prevent cement returns

Wellhead requirements:
- Flanged connections rated 150-600 psi, 200-350 degC
- Thermal insulation to reduce heat loss and protect personnel
- Master valve, flow control wing valves, bleed valve
        """,
        key_factors=[
            "Maximum anticipated temperature (determines cement and casing grade)",
            "Lost circulation zones (plan cement volumes and LCM)",
            "Freshwater aquifer depth (surface casing setting depth)",
            "Production zone permeability (slotted liner design)",
            "Wellhead pressure rating (based on reservoir pressure)",
            "Thermal cycling frequency (affects expansion joint fatigue life)"
        ],
        primary_authority=[
            "IGA Best Practices Guide for Geothermal Drilling (2013)",
            "ASME PTC 4.4 - Gas Turbine Heat Recovery Steam Generators",
            "API RP 10B-2 - Recommended Practice for Testing Well Cements"
        ],
        burden_holder="Operator to design well to withstand thermal and chemical conditions for 30+ year life",
        adversary_position="Regulators require protection of groundwater; investors concerned about well integrity failures",
        counter_arguments=[
            "Thermal expansion can cause casing damage if not designed properly",
            "Lost circulation can prevent adequate cementing (flow behind casing)",
            "High-temp cement is expensive and may not set properly if too hot",
            "Corrosion from H2S and CO2 can shorten casing life"
        ],
        resolution_strategy="Use industry-standard casing program with expansion accommodation. Require cement bond logs and temperature surveys. Install corrosion-resistant alloys (13Cr) in production string if H2S >100 ppm. Plan contingencies for lost circulation (aerated drilling, stage cementing).",
        entity_scope="All geothermal production and injection wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well design practices based on decades of geothermal industry experience; IGA guidelines widely accepted",
        controlling_precedent="IGA Best Practices (2013) is international standard for geothermal drilling",
        issue_category=IssueCategory.WELL_DESIGN,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Silica and Calcite Scaling Management",
        keywords=["scaling", "silica", "calcite", "amorphous silica", "precipitation", "saturation index", "pH control", "inhibitors"],
        conclusion_template="Silica and calcite scaling occurs when geothermal brine cools or pressure drops, precipitating minerals in wells, pipelines, and heat exchangers. Silica scaling is kinetically controlled (slow, predictable); calcite is instantaneous at supersaturation. Management: pH adjustment, inhibitors, controlled cooling rates, periodic acid cleaning.",
        reasoning_framework="""
Silica scaling mechanism:
- Solubility of amorphous silica: log(SiO2_ppm) = -731/T(K) + 4.52 (Fournier correlation)
  At 250 degC: ~900 ppm; at 100 degC: ~120 ppm
- As brine cools from reservoir to surface, dissolved silica exceeds saturation
- Polymerization: monomeric -> dimeric -> colloidal silica -> amorphous precipitate
- Kinetics: induction time hours to days (allows operational window)

Calcite scaling mechanism:
- Solubility product: Ksp = [Ca2+][CO3^2-] decreases with temperature (retrograde solubility)
- Pressure drop causes CO2 degassing, pH increases, carbonate ion increases
- Instantaneous precipitation when saturation index SI = log([Ca][CO3]/Ksp) > 0
- Scale forms in flash separators, wellbores, pipelines

Prevention strategies:
1. Silica control:
   - Keep brine above silica saturation temp until after use (insulated pipes)
   - Acidify to pH 5-6 (slows polymerization kinetics)
   - Seed with fine silica particles (controlled precipitation in settling pond)
   - Inhibitors: polyacrylates, phosphonates (delay nucleation)

2. Calcite control:
   - pH control: inject CO2 or HCl to maintain pH <7 (keeps carbonate ion low)
   - Scale inhibitors: phosphonates (HEDP, ATMP) chelate Ca2+
   - Avoid pressure drops (keep CO2 in solution)

3. Mechanical removal:
   - Periodic acid cleaning (HCl for calcite, HF for silica - dangerous)
   - Pigging of pipelines
   - Well workovers to remove near-wellbore scale

Monitoring:
- Online pH, conductivity, silica analyzers
- Coupon racks to measure scaling rate
- Saturation index calculations from geochemistry (PHREEQC, SOLMINEQ)

Cost impact:
- Untreated scaling can reduce heat transfer by 50% in 1-2 years
- Chemical treatment: $0.5-2.0/MWh (relatively low cost)
- Well workover: $500K-2M per well (major expense)
        """,
        key_factors=[
            "Brine silica concentration (measure in wellhead samples)",
            "Calcium and bicarbonate concentrations (calcite risk)",
            "Cooling rate and final temperature (determines supersaturation)",
            "pH of brine (affects both silica and calcite solubility)",
            "Pressure profile (CO2 degassing drives calcite)",
            "Operational variability (startups/shutdowns accelerate scaling)"
        ],
        primary_authority=[
            "Gallup (1989) - Aluminum silicate scale formation and inhibition",
            "Mroczek et al. (2015) - Silica scaling in geothermal systems",
            "Bremere et al. (2000) - Prevention of silica scale in membrane systems"
        ],
        burden_holder="Operator to prevent scaling that degrades plant performance",
        adversary_position="Equipment vendors warranty may exclude damage from scaling; insurance may not cover production loss",
        counter_arguments=[
            "Inhibitors are expensive and may not be effective at very high supersaturation",
            "Acid cleaning is hazardous (HF) and requires plant shutdown",
            "pH control with CO2 injection adds capital cost (compressors)",
            "Some brines have complex chemistry where multiple scales co-precipitate"
        ],
        resolution_strategy="Implement comprehensive water chemistry monitoring. Use conservative operating limits (stay below 80% of silica saturation). Inject scale inhibitors continuously. Plan annual shutdowns for inspection and cleaning. Design heat exchangers with high fouling factors.",
        entity_scope="All geothermal plants using brines with >100 ppm silica or >50 ppm calcium",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Scaling chemistry well-understood; inhibitor technology proven; monitoring systems standard",
        controlling_precedent="Fournier (1985) silica solubility correlations used industry-wide",
        issue_category=IssueCategory.SCALING_CORROSION,
        fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Induced Seismicity Traffic Light Protocol",
        keywords=["induced seismicity", "earthquakes", "traffic light", "magnitude", "injection rate", "microseismic", "ground motion", "seismic hazard"],
        conclusion_template="Geothermal operations (injection, production, hydraulic stimulation) can induce seismicity by altering pore pressure and effective stress on faults. Traffic light protocol establishes magnitude thresholds: Green (continue), Amber (reduce rate), Red (stop). Typical thresholds M<1.5 green, 1.5<M<2.5 amber, M>2.5 red. Real-time seismic monitoring mandatory.",
        reasoning_framework="""
Induced seismicity mechanism:
- Effective stress: sigma_eff = sigma_total - alpha*P_pore
- Injection increases pore pressure, reduces effective stress on faults
- Mohr-Coulomb failure: tau = c + sigma_eff * tan(phi)
- When tau exceeds shear strength, fault slips (earthquake)

Seismic moment vs volume relationship:
- McGarr (2014): M0_max = G * V_inj
  where G = shear modulus (~30 GPa), V_inj = net injected volume
- Moment magnitude: Mw = (2/3) * log(M0) - 6.05
- Empirical: maximum magnitude typically 1-2 units above background

Traffic light protocol:
GREEN: M < M_green (typically 1.5)
  - Continue normal operations
  - Monitor seismicity rate and locations

AMBER: M_green < M < M_red (typically 1.5 to 2.5)
  - Reduce injection/stimulation rate by 20-50%
  - Increase monitoring frequency
  - Prepare to shut in if seismicity continues

RED: M > M_red (typically 2.5) or ground motion > 0.5 cm/s
  - Immediate cessation of injection/stimulation
  - Vent wells to reduce pressure
  - Do not resume until seismicity decays and investigation complete

Threshold setting considerations:
- Local background seismicity (set M_green above background)
- Distance to population (farther allows higher threshold)
- Building codes and vulnerability (older buildings require lower threshold)
- Public risk tolerance (may require M_red < 2.0 in populated areas)

Monitoring system:
- Network of 10-30 seismometers within 5 km of operation
- Real-time processing and magnitude determination (<5 min latency)
- Automated alerts to operators when thresholds approached
- Publicly accessible web portal for transparency

Case studies:
- Basel EGS (2006): M3.4 event, project canceled, $9M damages
- Pohang EGS (2017): M5.5 event, project terminated, regulatory changes
- The Geysers (California): successful traffic light implementation since 2012, M<4 maintained
        """,
        key_factors=[
            "Proximity to mapped faults (avoid known active faults by >1 km)",
            "Maximum historical seismicity in region (sets baseline)",
            "Population density and distance (determines acceptable risk)",
            "Injection/production rate and cumulative volume (scales with seismic potential)",
            "Seismic network detection threshold (must detect M<1 events reliably)",
            "Stakeholder engagement (public acceptance critical)"
        ],
        primary_authority=[
            "Mignan et al. (2017) - Induced seismicity risk analysis",
            "Majer et al. (2012) - Protocol for induced seismicity (DOE)",
            "Bachmann et al. (2011) - Basel EGS lessons learned"
        ],
        burden_holder="Operator to demonstrate seismic risk is managed and public safety protected",
        adversary_position="Public fears earthquakes; regulators may impose very conservative thresholds; insurance costly",
        counter_arguments=[
            "Even small events (M2-3) cause public alarm and media attention",
            "Seismicity can continue after injection stops (pore pressure diffusion)",
            "Difficult to distinguish induced vs natural events in seismically active areas",
            "Economic impact of shutdowns (lost revenue, sunk drilling costs)"
        ],
        resolution_strategy="Engage public early and transparently. Set conservative initial thresholds (M_red=2.0), increase if no seismicity after 6 months. Require independent seismologist oversight. Establish damage compensation fund. Site selection avoiding known faults. Gradual ramp-up of injection rates (allows fault stress redistribution).",
        entity_scope="All geothermal projects with injection >10 L/s or hydraulic stimulation",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Induced seismicity is complex and site-specific; conservative protocols reduce but cannot eliminate risk; public perception is critical",
        controlling_precedent="DOE Protocol for Induced Seismicity (2012) widely adopted; Basel and Pohang cases reinforce need for caution",
        issue_category=IssueCategory.INDUCED_SEISMICITY,
        fragility_score=0.65
    ),

    DoctrineBlock(
        topic="Ground-Source Heat Pump Coefficient of Performance (COP)",
        keywords=["heat pump", "COP", "coefficient of performance", "ground-source", "geothermal heat pump", "GSHP", "EER", "SEER", "closed loop"],
        conclusion_template="Ground-source heat pumps (GSHPs) extract heat from shallow ground (1-100 m depth) for space heating/cooling. COP for heating typically 3.5-5.0 (350-500% efficient vs 100% for resistance heating). Ground temperature is stable year-round (10-15 degC), providing efficiency advantage over air-source heat pumps. System sizing requires thermal conductivity testing and loop design.",
        reasoning_framework="""
Heat pump fundamentals:
- Carnot COP_heating = T_hot / (T_hot - T_cold)
  For T_hot=40 degC (313K), T_cold=10 degC (283K): COP_Carnot = 313/30 = 10.4
- Real COP is 50-60% of Carnot due to compressor inefficiency, heat exchanger losses
- Typical residential GSHP: COP_heating = 3.5-5.0, COP_cooling = 4.0-6.0

Ground-source advantage:
- Ground temperature stable at 10-15 degC (below frost depth, >3 m)
- Air-source heat pumps face -10 to +35 degC air temps (COP varies widely)
- GSHP provides consistent performance year-round

System components:
1. Ground loop: HDPE pipe buried vertically (boreholes 50-150 m) or horizontally (trenches 1.5-3 m)
   - Closed loop: water + antifreeze circulates, no groundwater use
   - Open loop: extract groundwater, pass through heat exchanger, reinject (requires permits)
2. Heat pump unit: compressor, condenser, evaporator, expansion valve
3. Distribution: forced air or hydronic (radiant floor)

Design calculations:
- Heating load: Q_heat (kW) from building heat loss calc
- Cooling load: Q_cool (kW) from building heat gain calc
- Ground loop length: L = Q / (q_effective)
  where q_effective = thermal extraction rate per meter (30-70 W/m depending on soil)

Thermal conductivity testing:
- Thermal Response Test (TRT): circulate heated fluid in test borehole, measure temp rise
- Analyze with line-source model to extract k (W/m/K) and undisturbed ground temp
- Typical k: dry soil 0.5-1.0, saturated soil 1.5-2.5, rock 2.0-4.0

Installation cost:
- Vertical loops: $2500-4000 per ton (12,000 BTU/hr)
- Horizontal loops: $1500-3000 per ton (requires large land area)
- Payback vs air-source: 5-15 years (depends on energy prices)

Sustainability:
- Ground thermal recharge: must balance heating and cooling extraction to avoid long-term drift
- Typical recharge: solar heating, groundwater flow, geothermal gradient
- Monitoring: measure loop temperatures annually, ensure returning to baseline
        """,
        key_factors=[
            "Building heating and cooling loads (determines system size)",
            "Soil thermal conductivity (affects loop length required)",
            "Available land area (limits horizontal loop option)",
            "Groundwater availability for open loop (permits, aquifer yield)",
            "Climate balance (heating-dominated or cooling-dominated affects ground temp drift)",
            "Electricity rates vs gas/oil rates (determines economic payback)"
        ],
        primary_authority=[
            "ASHRAE Handbook - HVAC Applications ch 34 Geothermal Energy",
            "IGSHPA Design and Installation Standards (2017)",
            "ISO 13256-1 Water-source heat pumps testing and rating"
        ],
        burden_holder="Installer to design system that achieves rated COP for building loads",
        adversary_position="Building owners may prefer lower upfront cost of air-source; utilities may not offer incentives",
        counter_arguments=[
            "High upfront cost vs air-source heat pumps ($15K-30K premium)",
            "Requires drilling or excavation (not feasible in dense urban areas)",
            "Ground loop can fail (leak in buried pipe hard to locate/repair)",
            "Oversized systems waste money; undersized fail to meet loads"
        ],
        resolution_strategy="Detailed load calculation (Manual J for residential). Thermal conductivity testing mandatory for vertical systems >10 tons. Use conservative design margins (10-20% extra loop length). Pressure test loops before backfilling. Offer 30-year loop warranty. Monitor loop temps first 2 years to validate design.",
        entity_scope="Residential and commercial buildings in climates with heating/cooling needs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GSHP technology mature; COP values well-documented; design methodology standardized (IGSHPA)",
        controlling_precedent="IGSHPA standards (2017) define industry best practices for GSHP design",
        issue_category=IssueCategory.HEAT_PUMP_SYSTEMS,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Geothermal Reservoir Modeling with TOUGH2",
        keywords=["reservoir simulation", "TOUGH2", "numerical modeling", "recharge", "pressure decline", "thermal drawdown", "production forecast"],
        conclusion_template="TOUGH2 (Transport of Unsaturated Groundwater and Heat) is industry-standard simulator for geothermal reservoirs. Solves coupled mass and energy conservation in 3D porous/fractured media. Used to forecast production rates, pressure decline, thermal drawdown, and optimize injection for 30+ year project life. Model calibration requires history matching to production data.",
        reasoning_framework="""
TOUGH2 governing equations:
Mass conservation: d/dt(integral(rho*phi*dV)) = integral(rho*v*dA) + sources
Energy conservation: d/dt(integral(rho*h*phi*dV)) = integral(rho*h*v*dA) + integral(k*grad(T)*dA) + sources

Discretization:
- Integral Finite Difference (IFD) method
- Grid: 10,000-100,000 elements for field-scale (1-10 km)
- Time steps: adaptive, seconds to years

Input data requirements:
1. Geological model: layering, faults, permeability distribution
   - Typically from seismic interpretation, well logs, core data
2. Rock properties: porosity, permeability, heat capacity, thermal conductivity
   - Anisotropic permeability for fractured systems (k_horizontal >> k_vertical)
3. Fluid properties: density, viscosity, enthalpy as f(T, P)
   - IAPWS-97 water/steam correlations built in
4. Initial conditions: pressure and temperature profile (pre-production)
5. Boundary conditions: lateral no-flow or constant P/T, bottom heat flux

Production simulation:
- Specify well locations, depths, open intervals
- Production constraint: either fixed flow rate or fixed bottomhole pressure
- Injection constraint: fixed rate, max wellhead pressure
- Simulate 30-50 years at monthly time steps

Key outputs:
- Pressure and temperature evolution at each gridblock
- Well flow rates and enthalpies
- Power output forecast: P = m_dot * (h_production - h_injection) * efficiency
- Thermal breakthrough time: when injection cooling reaches production wells

Calibration (history matching):
- Minimize misfit between simulated and observed well pressures, temps, flow rates
- Adjust uncertain parameters: permeability field, recharge rate, boundary conditions
- Use inverse modeling (PEST, iTOUGH2) or manual trial-and-error

Uncertainty quantification:
- Monte Carlo: run 100s of realizations with varying parameters
- P10/P50/P90 production forecasts for financing
        """,
        key_factors=[
            "Permeability distribution (most uncertain parameter, controls flow paths)",
            "Recharge rate (determines sustainability of production)",
            "Injection strategy (rate, location, temperature affects thermal drawdown)",
            "Well spacing (too close causes interference, too far is inefficient)",
            "Simulation time horizon (30 years minimum for project life)",
            "Calibration data quality (more wells and longer history improves confidence)"
        ],
        primary_authority=[
            "Pruess et al. (1999) - TOUGH2 User's Guide",
            "O'Sullivan et al. (2001) - State of the art of geothermal reservoir simulation",
            "Grant & Bixley (2011) - Geothermal Reservoir Engineering 2nd ed."
        ],
        burden_holder="Developer to demonstrate reservoir can sustain production via numerical simulation",
        adversary_position="Lenders require P90 (conservative) forecasts; regulators may challenge recharge assumptions",
        counter_arguments=[
            "Models are non-unique (many parameter sets fit history equally well)",
            "Sparse well data leaves large uncertainty in permeability structure",
            "Natural state calibration may not predict production response accurately",
            "Recharge processes poorly understood (diffuse vs fault-controlled)"
        ],
        resolution_strategy="Use multiple conceptual models (layered vs fractured, different fault interpretations). Calibrate to natural state (pre-production) and any production history. Run sensitivity analyses on key uncertainties. Report P10/P50/P90 cases. Update model as new data acquired (Bayesian updating).",
        entity_scope="All geothermal projects >10 MW requiring reservoir management plan",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TOUGH2 is peer-reviewed, validated code used globally; uncertainty quantification standard practice",
        controlling_precedent="TOUGH2 has been industry-standard for geothermal simulation since 1990s",
        issue_category=IssueCategory.RESERVOIR_ENGINEERING,
        fragility_score=0.4
    ),

    DoctrineBlock(
        topic="Geothermal Levelized Cost of Energy (LCOE) Analysis",
        keywords=["LCOE", "economics", "capital cost", "O&M", "capacity factor", "discount rate", "levelized cost", "PPA", "power purchase agreement"],
        conclusion_template="Geothermal LCOE ranges $50-150/MWh depending on resource quality, drilling depth, and plant size. Capital cost dominates (70-80% of LCOE): exploration, drilling, plant construction. Geothermal has high capacity factor (90-95%) vs solar (25%) or wind (35%), improving competitiveness. LCOE must be below local wholesale power price or PPA rate for project viability.",
        reasoning_framework="""
LCOE definition:
LCOE = (Sum of lifetime costs discounted) / (Sum of lifetime energy discounted)
     = [CAPEX + Sum(OPEX_t / (1+r)^t)] / [Sum(E_t / (1+r)^t)]

where:
CAPEX = capital expenditure (USD)
OPEX_t = operating expense in year t (USD/year)
E_t = energy produced in year t (MWh/year)
r = discount rate (typically 7-10%)
t = project life (typically 30 years)

Geothermal cost breakdown:
1. Exploration: $2-10M (geological surveys, slim holes, temperature gradient wells)
2. Drilling: $3-8M per production well, $2-5M per injection well
   - Typical project: 4-8 production wells, 2-4 injection wells
   - Drilling is largest cost component (40-50% of CAPEX)
3. Plant construction: $2500-6000/kW installed
   - Flash steam: $2500-4500/kW
   - Binary cycle: $3500-6000/kW
4. O&M: $10-25/MWh (labor, chemicals, maintenance, insurance)

Example calculation (20 MW binary plant):
CAPEX:
- Exploration: $5M
- Drilling: 6 wells * $5M = $30M
- Plant: 20 MW * $4000/kW = $80M
- Total CAPEX: $115M

Annual energy production:
- Capacity: 20 MW
- Capacity factor: 92%
- E_annual = 20 MW * 8760 hr/yr * 0.92 = 161,184 MWh/yr

Annual OPEX:
- O&M: 161,184 MWh * $15/MWh = $2.4M/yr

LCOE calculation (7% discount, 30 years):
- CAPEX: $115M
- OPEX PV: $2.4M/yr * 12.4 (annuity factor) = $29.8M
- Total cost PV: $144.8M
- Energy PV: 161,184 MWh/yr * 12.4 = 1,998,682 MWh
- LCOE = $144.8M / 1,998,682 MWh = $72/MWh

Sensitivity:
- Drilling cost +50%: LCOE increases to $84/MWh (+17%)
- Capacity factor -5% (92% to 87%): LCOE increases to $76/MWh (+5%)
- Plant cost +20%: LCOE increases to $80/MWh (+11%)

Comparison to other renewables (2024 US averages):
- Solar PV utility-scale: $30-50/MWh (but capacity factor 25%)
- Onshore wind: $35-60/MWh (capacity factor 35%)
- Natural gas combined cycle: $40-70/MWh (fuel price dependent)
- Geothermal: $50-150/MWh (but 90%+ capacity factor, baseload)

Value proposition:
- Baseload, dispatchable power (no storage needed)
- Hedge against fuel price volatility
- Small land footprint (1-8 acres/MW vs 40-50 for solar)
- Long plant life (30-50 years)
        """,
        key_factors=[
            "Drilling success rate (dry holes increase cost dramatically)",
            "Resource temperature (higher temp improves power output per well)",
            "Well productivity (flow rate per well affects number needed)",
            "Plant technology (flash vs binary cost and efficiency)",
            "Capacity factor (geothermal advantage is high utilization)",
            "Discount rate (reflects project risk, financing cost)"
        ],
        primary_authority=[
            "NREL Annual Technology Baseline (2024) - Geothermal LCOE",
            "IRENA Renewable Power Generation Costs (2023)",
            "Lazard LCOE Analysis (2024)"
        ],
        burden_holder="Developer to demonstrate LCOE competitive with alternative power sources",
        adversary_position="Utilities may prefer proven technologies (natural gas); investors concerned about drilling risk",
        counter_arguments=[
            "High upfront cost requires large capital commitment before revenue",
            "Drilling risk (1 in 3 wells may be dry or low productivity)",
            "Resource decline over time (pressure/temperature drawdown)",
            "Limited to regions with geothermal resources (not universally available)"
        ],
        resolution_strategy="Phase development to reduce initial capital requirement. Secure PPA before construction (locks in revenue). Obtain drilling success insurance or reserves certification to reduce risk. Emphasize baseload value and capacity factor advantage. Target markets with high power prices or renewable mandates.",
        entity_scope="All geothermal power projects seeking financing or PPA negotiation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="LCOE methodology standard across energy industry; geothermal cost data well-documented",
        controlling_precedent="NREL ATB (2024) provides authoritative geothermal LCOE benchmarks",
        issue_category=IssueCategory.ECONOMICS_LCOE,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Non-Condensable Gas (NCG) Extraction and H2S Abatement",
        keywords=["NCG", "non-condensable gas", "CO2", "H2S", "hydrogen sulfide", "vacuum pump", "gas extraction", "Stretford process", "LO-CAT", "sulfur recovery"],
        conclusion_template="Non-condensable gases (primarily CO2 and H2S) in geothermal steam reduce turbine efficiency and create environmental/safety hazards. NCG content ranges 0.5-15% by weight. Extraction required via steam jet ejectors or vacuum pumps. H2S must be abated to <30 ppm emissions via chemical processes (Stretford, LO-CAT) or reinjection. NCG management is 20-30% of plant capital cost for high-NCG fields.",
        reasoning_framework="""
NCG composition:
- CO2: typically 80-99% of NCG (not toxic but reduces turbine efficiency)
- H2S: 1-20% of NCG (toxic at >10 ppm, corrosive, rotten egg odor at 0.5 ppm)
- Trace: CH4, NH3, N2, Ar

Impact on power generation:
- NCG in steam reduces partial pressure of steam -> lower turbine efficiency
- Rule of thumb: 1% NCG by weight reduces efficiency by 1-2%
- High-NCG fields (>5%) require larger condensers and extraction systems

Extraction process (flash steam plants):
1. Steam condenser: steam turbine exhaust condenses to water at 40-50 degC
2. NCG accumulates in condenser (doesn't condense)
3. Extraction: vacuum pump or steam jet ejector removes NCG from condenser
4. NCG treatment: H2S abatement before atmospheric venting

Steam jet ejector:
- Uses high-pressure steam to create vacuum via Venturi effect
- Simple, no moving parts, but consumes 5-10% of steam production
- Multi-stage (3-4 stages) to compress NCG from 0.1 bar to 1 bar

Liquid ring vacuum pump:
- Mechanical pump using water seal
- More efficient than ejectors (parasitic load 2-5% vs 5-10%)
- Requires maintenance (rotating parts)

H2S abatement technologies:

1) Stretford process (wet scrubbing):
   - NCG bubbles through alkaline solution (Na2CO3 + vanadium catalyst)
   - H2S oxidized to elemental sulfur: H2S + V^5+ -> S + V^4+
   - Vanadium regenerated with air: V^4+ + O2 -> V^5+
   - Produces sulfur cake (saleable byproduct)
   - Operates at near-atmospheric pressure
   - Efficiency: >99% H2S removal (outlet <10 ppm)

2) LO-CAT process:
   - Similar to Stretford but uses iron chelate catalyst instead of vanadium
   - Lower operating cost, less hazardous chemicals
   - Produces sulfur slurry

3) Caustic scrubbing:
   - NaOH solution absorbs H2S: H2S + 2NaOH -> Na2S + 2H2O
   - Simple but produces hazardous waste (Na2S solution)
   - Used for low H2S concentrations (<100 ppm)

4) Reinjection:
   - NCG compressed and reinjected with condensate
   - No chemical treatment, zero emissions
   - Requires high-pressure compressors (20-50 bar)
   - Limited by injection well capacity

Capital cost impact:
- Low NCG (<1%): minimal, included in standard condenser
- Moderate NCG (1-5%): +10-15% plant cost (extraction + basic abatement)
- High NCG (>5%): +20-30% plant cost (large extraction + Stretford/LO-CAT)

Environmental regulations:
- US: H2S emissions <30 ppm (New Source Performance Standards)
- California: stricter limits in some air districts (<1 ppm)
- Binary plants: zero emissions (closed loop, NCG stays in brine)
        """,
        key_factors=[
            "NCG content (% by weight, determines extraction system size)",
            "H2S concentration in NCG (determines abatement technology)",
            "Air quality regulations (local emission limits)",
            "Turbine size (larger units more tolerant of NCG)",
            "Condenser design (affects NCG accumulation)",
            "Disposal options for sulfur byproduct (saleable or waste)"
        ],
        primary_authority=[
            "DiPippo (2012) - Geothermal Power Plants ch 11 NCG systems",
            "EPA New Source Performance Standards 40 CFR 60 Subpart XX",
            "URS Corp (2003) - H2S Abatement at Geysers Geothermal Field"
        ],
        burden_holder="Operator to meet air emissions regulations and maintain turbine efficiency",
        adversary_position="Environmental groups oppose H2S odor; regulators enforce emission limits; neighbors complain",
        counter_arguments=[
            "High NCG fields have lower net power output (parasitic load for extraction)",
            "Stretford/LO-CAT systems are expensive to operate (chemicals, maintenance)",
            "Sulfur byproduct may have no market (disposal cost)",
            "Reinjection requires high-pressure compressors (capital and power consumption)"
        ],
        resolution_strategy="Characterize NCG content early in exploration (drill stem tests). If >5% NCG, plan for Stretford or reinjection in project budget. Site selection: avoid high-NCG fields if possible. Binary cycle option eliminates emissions (trade higher capital cost for regulatory simplicity). Public outreach regarding H2S monitoring and abatement systems.",
        entity_scope="Flash steam geothermal plants with NCG >0.5%",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NCG extraction technology mature; abatement processes proven; regulatory limits well-defined",
        controlling_precedent="EPA NSPS 40 CFR 60 Subpart XX sets federal H2S emission limits",
        issue_category=IssueCategory.ENVIRONMENTAL_IMPACT,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Geothermal Reinjection Strategy and Pressure Maintenance",
        keywords=["reinjection", "injection well", "pressure support", "thermal breakthrough", "tracer test", "sustainability", "reservoir management"],
        conclusion_template="Reinjection of spent geothermal fluid is essential for pressure maintenance and sustainability. Injection location must balance pressure support (close to producers) vs avoiding thermal breakthrough (far from producers). Typical spacing 500-1500 m. Tracer tests quantify recharge time (5-30 years for well-managed systems). Reinjection enables 100+ year reservoir life vs 20-30 years for depletion-drive.",
        reasoning_framework="""
Reinjection benefits:
1. Pressure maintenance: replenishes reservoir, sustains production rates
2. Fluid disposal: avoids surface discharge (environmental regulations)
3. Thermal sustainability: manages heat extraction rate vs natural recharge
4. Seismicity management: can reduce risk by maintaining stress state

Injection well design:
- Same casing program as production wells (withstand thermal cycling)
- Larger diameter (9-5/8 in vs 7 in production) allows higher rates
- Downhole temperature lower (100-150 degC) than production (200-300 degC)
- Filters required to remove suspended solids (prevent plugging)

Injection rate:
- Typical: 50-150 kg/s per well (similar to production well output)
- Limited by formation injectivity: I = Q / (P_inj - P_reservoir)
- Monitor injection pressure: keep below fracture gradient (avoid hydrofracturing)
- Decline in injectivity over time due to scaling, silica deposition

Spacing optimization:
Trade-off:
- Close spacing (<500 m): rapid pressure support, but early thermal breakthrough (cold injectate cools production)
- Far spacing (>1500 m): delayed breakthrough, but poor pressure support

Optimal spacing: 800-1200 m for most fields
- Allows 10-20 year delay before breakthrough
- Provides adequate pressure maintenance

Tracer testing:
- Inject chemical tracer (fluorescein, rhodamine, SF6) into injection well
- Monitor production wells for tracer appearance
- Measure breakthrough time and peak concentration
- Calculate reservoir volume and flow paths

Thermal breakthrough detection:
- Production well temperature declines (1-5 degC drop indicative)
- Production rate declines as fluid density increases (heavier cold water)
- Mitigation: reduce injection rate, relocate injection, drill new production well in hotter zone

Sustainability metrics:
- Recovery factor: cumulative heat extracted / initial heat in place (target <10-15% over 30 years)
- Recharge time: volume of reservoir / injection rate (target >20 years)
- Pressure decline: monitor reservoir-wide (target <2 bar/year)

Case study: The Geysers (California):
- Largest geothermal field in US (1500 MW peak, now ~800 MW)
- Experienced severe pressure decline 1980s-1990s (no reinjection)
- Reinjection program started 1997 (60 ML/day municipal wastewater)
- Pressure recovered, production stabilized
- Demonstrates importance of reinjection for long-term sustainability
        """,
        key_factors=[
            "Injection rate vs production rate (aim for 80-100% reinjection)",
            "Well spacing (determines breakthrough time)",
            "Reservoir permeability structure (controls fluid flow paths)",
            "Injection temperature (affects density-driven flow)",
            "Suspended solids in injectate (requires filtration)",
            "Monitoring program (pressure, temperature, tracer surveys)"
        ],
        primary_authority=[
            "Axelsson et al. (2001) - Sustainable management of geothermal resources",
            "O'Sullivan et al. (2010) - Reinjection in geothermal fields",
            "Stefansson (1997) - Geothermal reinjection experience"
        ],
        burden_holder="Operator to design reinjection strategy that maintains reservoir for project life",
        adversary_position="Regulators require proof of sustainability; environmental groups concerned about induced seismicity from injection",
        counter_arguments=[
            "Thermal breakthrough can occur faster than predicted (preferential flow paths)",
            "Injection well injectivity declines over time (scaling, formation damage)",
            "Induced seismicity from injection pressure (requires monitoring)",
            "Initial lack of injection wells (high capital cost to add later)"
        ],
        resolution_strategy="Plan injection wells from project start (not afterthought). Conservative spacing (1000+ m). Implement tracer test program in first 2 years. Monitor production temps and pressures continuously. Adaptive management: adjust injection rates and locations based on monitoring. Budget for periodic injection well workovers (acid stimulation to restore injectivity).",
        entity_scope="All geothermal projects >5 MW and >20 year life expectancy",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Reinjection is proven best practice globally; spacing guidelines based on field experience; monitoring technology mature",
        controlling_precedent="Axelsson et al. (2001) established sustainability framework for geothermal management",
        issue_category=IssueCategory.RESERVOIR_ENGINEERING,
        fragility_score=0.35
    ),

    DoctrineBlock(
        topic="Geothermal Exploration Risk and Drilling Success Rates",
        keywords=["exploration risk", "drilling success", "dry hole", "temperature gradient", "slim hole", "production test", "reserves certification"],
        conclusion_template="Geothermal drilling success rates average 60-70% for production wells in proven fields, but only 20-40% for exploration wildcats. Dry hole costs $3-8M. Risk mitigation: geophysical surveys (MT, seismic), temperature gradient holes (slim holes $200-500K), phased exploration. Reserves certification by independent engineer required for project financing.",
        reasoning_framework="""
Exploration phases:

Phase 1: Regional reconnaissance
- Desktop study: geology, tectonics, heat flow, thermal springs
- Satellite thermal imagery, aeromagnetic surveys
- Cost: $100-500K
- Success indicator: identify 3-5 prospect areas

Phase 2: Detailed surveys
- Magnetotelluric (MT): maps subsurface resistivity (low resistivity = hot brine or clay alteration)
- Seismic reflection: identifies faults (fluid conduits) and reservoir structure
- Gravity/magnetics: delineates basement depth, intrusions
- Geochemistry: sample thermal springs, analyze for reservoir temp indicators
- Cost: $500K-2M
- Success indicator: define drillable target with >150 degC predicted temp

Phase 3: Temperature gradient drilling
- Slim holes: 6-8 inch diameter, 500-1500 m depth
- Bottom-hole temperature (BHT) logs confirm gradient
- Cost: $200-500K per hole
- Drill 2-4 holes to define thermal anomaly
- Success indicator: >50 degC/km gradient, T>150 degC at 3 km projected depth

Phase 4: Exploration drilling
- Full-size well (13-3/8 in surface casing, 7-9-5/8 in production)
- 2000-4000 m depth
- Production test: flow test at 50-150 kg/s for 3-7 days
- Cost: $4-10M per well
- Success criteria:
  - Temperature >150 degC (binary) or >180 degC (flash)
  - Flow rate >30 kg/s (50 kg/s preferred)
  - Reservoir pressure >20 bar
  - Chemistry acceptable (silica <600 ppm, calcite not supersaturated)

Drilling risk statistics:
- Proven field (infill drilling): 70-80% success
- Step-out wells (extending field): 50-70% success
- Wildcat exploration: 20-40% success

Failure modes:
- Insufficient temperature (30% of failures)
- Insufficient permeability (40% of failures)
- Lost circulation prevents completion (20% of failures)
- Chemistry issues (high NCG, scaling) (10% of failures)

Risk mitigation:
- Drill multiple wells before committing to plant construction
  Rule of thumb: 1.5 wells per MW for 20 MW plant (30 wells for contingency)
- Reserves certification: independent engineer (e.g., GeothermEx, GEIE) certifies proven reserves
  Required for project financing (lenders want proven reserves for 80%+ of capacity)
- Drilling success insurance: available but expensive (10-20% of drilling cost)
  Covers dry hole risk for exploration phase

Staged development:
- Phase 1: 5-10 MW plant on proven reserves (3-6 wells)
- Prove reservoir, secure offtake contract
- Phase 2: Expand to 20-50 MW with additional drilling
- Reduces upfront risk, allows learning

Probability of field success:
P_success = P_resource * P_drilling * P_commercial
where:
P_resource = 0.3-0.7 (probability adequate resource exists)
P_drilling = 0.6-0.8 (probability wells are successful)
P_commercial = 0.7-0.9 (probability project economics viable)
Overall: P_success = 0.15-0.50 for exploration projects
        """,
        key_factors=[
            "Quality of geophysical data (reduces resource risk)",
            "Number of temperature gradient holes (validates thermal model)",
            "Drilling contractor experience (reduces mechanical failure risk)",
            "Geological complexity (faults can enhance or compartmentalize reservoir)",
            "Proximity to proven fields (analogs reduce uncertainty)",
            "Financial capacity to drill contingency wells (minimum 3 wells before concluding field uneconomic)"
        ],
        primary_authority=[
            "Sanyal (2005) - Sustainability and renewability of geothermal power capacity",
            "Clauser & Huenges (1995) - Thermal conductivity of rocks and minerals",
            "GEA/World Bank (2013) - Geothermal Handbook Planning and Financing Power Generation"
        ],
        burden_holder="Developer to demonstrate resource exists and wells will be productive",
        adversary_position="Lenders require proven reserves before financing; equity investors concerned about dry hole losses",
        counter_arguments=[
            "Geophysical surveys are ambiguous (resistivity low could be clay, not hot brine)",
            "Temperature gradient holes may miss lateral reservoir structure",
            "First well may intersect fault (high flow) but second well dry (heterogeneity)",
            "Exploration drilling is capital-intensive with binary outcome (success or failure)"
        ],
        resolution_strategy="Sequential decision-making: invest in each exploration phase only if previous phase successful. Use probabilistic resource assessment (Monte Carlo on temp, permeability, area). Secure drilling success insurance or partner with experienced geothermal developer (farm-out exploration risk). Plan for 50% contingency wells in budget.",
        entity_scope="All greenfield geothermal projects and field extensions",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Exploration risk is inherent and high; success rates documented but variable by region; phased approach is industry best practice but doesn't eliminate risk",
        controlling_precedent="GEA/World Bank Handbook (2013) establishes exploration best practices",
        issue_category=IssueCategory.RESOURCE_ASSESSMENT,
        fragility_score=0.65
    ),

    DoctrineBlock(
        topic="Binary Cycle Organic Rankine Cycle (ORC) Working Fluid Selection",
        keywords=["ORC", "organic rankine cycle", "working fluid", "isobutane", "isopentane", "R245fa", "R134a", "ammonia", "critical temperature"],
        conclusion_template="Binary cycle efficiency depends critically on working fluid selection. Fluid must have boiling point below geothermal brine temp and critical temp above turbine inlet. Common fluids: isobutane (low-temp 100-130 degC), isopentane (mid-temp 120-160 degC), R245fa (high-temp 150-180 degC). Higher molecular weight fluids have lower turbine work but simpler turbines (fewer stages). Environmental regulations favor low-GWP fluids.",
        reasoning_framework="""
ORC thermodynamic cycle:
1. Vaporizer: liquid working fluid heated by geothermal brine to vapor
2. Turbine: vapor expands, drives generator, exits at low pressure
3. Condenser: vapor condenses to liquid via air or water cooling
4. Pump: liquid pumped back to high pressure, returns to vaporizer

Working fluid selection criteria:

1) Thermal match:
   - Boiling point <T_brine - 10 degC (ensure vaporization)
   - Critical temperature >T_turbine_inlet (supercritical improves efficiency)

2) Thermodynamic properties:
   - High latent heat of vaporization (more energy absorbed per kg)
   - Low specific volume (smaller turbine size)
   - Steep saturation curve (reduces moisture in turbine)

3) Environmental/Safety:
   - Global Warming Potential (GWP) <1000 preferred (R245fa GWP=1030, under phase-out)
   - Ozone Depletion Potential (ODP) = 0 (Montreal Protocol)
   - Flammability: hydrocarbons (isobutane) flammable, require safety systems
   - Toxicity: ammonia toxic but excellent thermodynamic properties

4) Economic:
   - Cost of working fluid inventory (10-50 tons for 10 MW plant)
   - Availability and supply chain

Common working fluids:

| Fluid        | Boiling Pt (°C) | Critical Temp (°C) | GWP  | Flammable | Best T_brine Range |
|--------------|-----------------|-------------------|------|-----------|-------------------|
| Isobutane    | -11.7          | 134.7             | 3    | Yes       | 100-130           |
| Isopentane   | 27.8           | 187.2             | 5    | Yes       | 120-160           |
| R245fa       | 15.1           | 154.0             | 1030 | No        | 130-170           |
| R134a        | -26.1          | 101.0             | 1430 | No        | 80-110            |
| Ammonia      | -33.3          | 132.3             | 0    | No (toxic)| 90-130            |
| R1233zd      | 18.3           | 165.6             | 7    | No        | 120-170           |

Efficiency comparison (for T_brine=150 degC, T_ambient=20 degC):
- Isopentane: ~11% (baseline)
- R245fa: ~12% (+1% vs isopentane, but higher GWP)
- Ammonia: ~13% (best, but safety concerns)

Turbine design impact:
- Low molecular weight (NH3, R134a): high turbine work per stage, requires multi-stage (higher cost)
- High molecular weight (isopentane): lower turbine work, single-stage sufficient (simpler, cheaper)

Flammability mitigation (for hydrocarbons):
- Nitrogen blanketing of equipment (inert atmosphere)
- Flame detection and suppression systems
- Explosion-proof electrical (Class I Div 2 rating)
- Adds 5-10% to capital cost vs non-flammable fluids

Regulatory trend:
- Kigali Amendment to Montreal Protocol: phase down high-GWP HFCs
- R245fa (GWP=1030) being phased out, replaced by R1233zd (GWP=7)
- Hydrocarbons (isobutane, isopentane) gaining favor (low GWP, natural)
        """,
        key_factors=[
            "Geothermal brine temperature (determines fluid choice range)",
            "Ambient temperature (affects condenser pressure and efficiency)",
            "Environmental regulations on GWP (limits fluid options)",
            "Flammability codes and insurance requirements (affect hydrocarbon use)",
            "Turbine vendor capabilities (some specialize in certain fluids)",
            "Working fluid cost and availability (ammonia cheap, R245fa expensive)"
        ],
        primary_authority=[
            "Tchanche et al. (2009) - Low-grade heat conversion into power using ORCs - A review",
            "Calm & Hourahan (2011) - Refrigerant Data Summary",
            "Quoilin et al. (2013) - Techno-economic survey of ORC systems"
        ],
        burden_holder="Developer to select working fluid that maximizes efficiency within safety and regulatory constraints",
        adversary_position="Regulators enforcing GWP limits; insurers concerned about flammability; communities oppose toxic fluids",
        counter_arguments=[
            "High-GWP fluids (R245fa) face phase-out and may require replacement mid-project-life",
            "Hydrocarbons require expensive safety systems (reduces cost advantage)",
            "Ammonia toxicity creates public perception risk (even though zero GWP)",
            "Emerging fluids (R1233zd) have limited field experience (performance uncertainty)"
        ],
        resolution_strategy="Use decision matrix: rank fluids by efficiency, GWP, safety, cost. For new plants, prefer low-GWP options (hydrocarbons or R1233zd) to avoid future regulatory risk. If hydrocarbons, invest in robust safety systems and operator training. Ammonia viable for remote sites away from population. Detailed thermodynamic modeling to confirm performance for site-specific conditions.",
        entity_scope="All binary cycle geothermal plants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ORC working fluid selection methodology well-established; thermodynamic analysis standard practice; regulatory trends clear",
        controlling_precedent="Kigali Amendment (2016) drives phase-out of high-GWP fluids",
        issue_category=IssueCategory.POWER_PLANT_TECH,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Geothermal Power Plant Capacity Factor and Availability",
        keywords=["capacity factor", "availability", "reliability", "forced outage", "planned maintenance", "downtime", "baseload"],
        conclusion_template="Geothermal plants achieve 90-95% capacity factors, highest among renewables. Availability limited by planned maintenance (annual turbine inspection, 1-2 weeks) and forced outages (scaling, equipment failure, <5% of time). Baseload operation provides revenue certainty vs intermittent renewables requiring storage or backup.",
        reasoning_framework="""
Definitions:
Capacity factor = (Actual energy produced) / (Nameplate capacity * hours in period)
Availability = (Hours available) / (Total hours)
Reliability = (Hours operated without forced outage) / (Hours operated)

Geothermal typical performance:
- Capacity factor: 90-95% annually
- Availability: 95-98% (97% target)
- Forced outage rate: 2-5%
- Planned outage: 1-3% (1-2 weeks per year)

Downtime categories:

1) Planned maintenance (1-2 weeks/year):
   - Turbine inspection and cleaning (deposits, erosion)
   - Heat exchanger cleaning (scaling in binary plants)
   - Well workovers (1-2 wells per year on rotation)
   - Control system updates
   - Scheduled in low-demand season (spring or fall)

2) Forced outages (2-5% of time):
   - Turbine trip (over-speed, vibration, bearing failure)
   - Scaling blockage (sudden pressure drop)
   - NCG extraction failure (condenser pressure rises)
   - Electrical grid fault (external)
   - Well problems (casing leak, sand production)

3) Partial load operation (<1% of time):
   - Reduced output due to seasonal temperature effects (condenser performance)
   - Well decline (gradually ramp down over years)
   - Transmission constraints (grid operator curtailment - rare)

Comparison to other generation:

| Technology     | Capacity Factor | Availability | Dispatchable |
|----------------|-----------------|-------------|-------------|
| Geothermal     | 90-95%         | 95-98%      | Yes (baseload) |
| Nuclear        | 90-93%         | 90-95%      | Yes (baseload) |
| Coal           | 40-60% (declining) | 85-90% | Yes          |
| CCGT (gas)     | 30-60% (economic dispatch) | 90-95% | Yes |
| Solar PV       | 20-30%         | 98%+        | No (intermittent) |
| Wind           | 30-40%         | 95%+        | No (intermittent) |

Value of high capacity factor:
- Revenue stability: 90% CF means 7884 MWh per MW per year vs 2190 for solar (25% CF)
- For $50/MWh PPA: geothermal earns $394K/MW/yr vs solar $110K/MW/yr
- Enables debt financing (predictable cash flows)
- No storage required (solar/wind need batteries for baseload equivalent)

Performance degradation:
- New plant: 95% CF typical
- Year 10: 93% CF (minor well decline, equipment aging)
- Year 20: 90% CF (more frequent maintenance, well replacements)
- Year 30+: 85-90% CF (sustained with ongoing investment)

Maintenance strategy:
- Predictive: vibration monitoring, thermography, oil analysis (detect issues before failure)
- Preventive: scheduled inspections per OEM recommendations
- Corrective: repair after failure (minimized via predictive/preventive)

Improvement opportunities:
- Redundant equipment (standby pumps, spare turbine stages)
- Advanced diagnostics (real-time corrosion monitoring, scaling prediction)
- Modular design (isolate failed section, continue partial operation)
        """,
        key_factors=[
            "Planned maintenance schedule (minimize duration, coordinate with grid)",
            "Equipment reliability (turbine MTBF, pump life)",
            "Scaling management (reduces forced outages)",
            "Well productivity maintenance (workovers, stimulation)",
            "Grid connection reliability (transmission outages are external factor)",
            "Spare parts inventory (reduces downtime waiting for parts)"
        ],
        primary_authority=[
            "NERC Generating Availability Data System (GADS) - industry reliability database",
            "EPRI (2011) - Geothermal Power Plant Performance Handbook",
            "EIA Electric Power Annual - capacity factor statistics"
        ],
        burden_holder="Operator to achieve contractual availability (PPA typically requires 90-95% CF)",
        adversary_position="Offtaker in PPA penalizes shortfalls in delivered energy; investors expect consistent cash flows",
        counter_arguments=[
            "Well decline can reduce output faster than expected (reservoir modeling uncertainty)",
            "Scaling events can cause sudden loss of capacity (unpredictable timing)",
            "Equipment failures (turbine blade, heat exchanger tube) require long-lead replacement parts",
            "Remote locations increase time to obtain parts and repair crews"
        ],
        resolution_strategy="Design for 97% availability (allows 3% downtime margin). Implement robust maintenance program with annual outage <2 weeks. Stock critical spare parts on site (turbine rotor, heat exchanger bundles). Contract with equipment OEMs for rapid response service. Monitor well productivity quarterly, plan workovers proactively. PPA terms allow force majeure for events beyond operator control.",
        entity_scope="All geothermal power plants with offtake contracts or merchant operation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Capacity factor data from industry well-documented; availability targets standard in PPAs; maintenance practices proven",
        controlling_precedent="NERC GADS provides authoritative industry performance data",
        issue_category=IssueCategory.POWER_PLANT_TECH,
        fragility_score=0.25
    ),

    DoctrineBlock(
        topic="Geothermal Direct Use Applications",
        keywords=["direct use", "district heating", "greenhouse", "aquaculture", "balneology", "industrial process heat", "low temperature"],
        conclusion_template="Geothermal direct use applications consume thermal energy without power generation, viable for 40-150 degC resources. Common uses: district heating (Iceland, France), greenhouses (Netherlands, Kenya), aquaculture (fish farming), spa/bathing, industrial drying. Economics favorable where energy demand is co-located with resource. CHP (combined heat and power) maximizes resource utilization.",
        reasoning_framework="""
Direct use categories:

1) District heating:
   - Geothermal water (70-90 degC) distributed via insulated pipelines to buildings
   - Heat exchangers in buildings transfer heat to building loops
   - Return water reinjected at 30-40 degC
   - Economics: replaces natural gas/oil for heating (cost savings 30-60%)
   - Examples: Reykjavik (Iceland, 95% of buildings), Paris Basin (France, 150,000 homes)
   - Requires dense heat load (urban areas) to justify pipeline infrastructure

2) Greenhouse heating:
   - Maintains 15-25 degC in winter for vegetable/flower production
   - Floor heating, overhead hot water pipes, or forced air
   - Resources 50-80 degC sufficient
   - Cost: geothermal reduces heating cost by 50-80% vs fossil fuels
   - Examples: Netherlands (>500 hectares geothermal greenhouses), Kenya, Iceland

3) Aquaculture:
   - Warm water fish/shrimp farming (tilapia, shrimp prefer 25-30 degC)
   - Geothermal maintains optimal temp year-round
   - Resource: 30-60 degC
   - Examples: Iceland (Arctic char), USA (tilapia in Idaho, Oregon)

4) Industrial process heat:
   - Drying (lumber, crops, minerals): 60-120 degC
   - Food processing (pasteurization, sterilization): 80-130 degC
   - Pulp and paper: 120-180 degC
   - Chemical processes: varies by process
   - Replaces boilers (natural gas or oil)

5) Balneology (spas, bathing):
   - Therapeutic bathing, hot springs resorts
   - Minimal processing, direct use of thermal water
   - Major industry in Japan, Iceland, New Zealand

Combined Heat and Power (CHP):
- Binary geothermal plant generates electricity from 120-180 degC brine
- Spent brine exits plant at 70-90 degC (still warm)
- Use waste heat for district heating or greenhouses (cascade use)
- Overall resource utilization: 60-80% vs 10-15% for power-only

Economic analysis:
Geothermal district heating LCOH (Levelized Cost of Heat):
- Capital: $1000-3000/kW_thermal (wells + distribution pipelines)
- O&M: $5-15/MWh_thermal
- LCOH: $30-70/MWh_thermal
- Natural gas heating: $40-100/MWh_thermal (variable with gas price)
- Payback: 5-15 years for geothermal district heating investment

Resource assessment for direct use:
- Temperature requirement: match resource to application (don't need 200 degC for 70 degC heating)
- Flow rate: Q_thermal = m_dot * Cp * delta_T
  Example: 10 MW_thermal at delta_T=40 degC requires m_dot=60 kg/s
- Proximity to demand: pipelines cost $500-1500/m, distance <10 km preferred

Regulatory advantages:
- Simpler permitting than power plants (no turbine, no emissions)
- Lower temperature wells are shallower and cheaper
- Can use existing oil/gas wells in some cases (repurposing)
        """,
        key_factors=[
            "Resource temperature and flow rate (determines capacity)",
            "Proximity to heat demand (pipeline cost increases with distance)",
            "Competing energy prices (natural gas, electricity for heat pumps)",
            "Heat load profile (constant vs seasonal affects capacity factor)",
            "Water quality (corrosion, scaling may require heat exchangers)",
            "Regulatory framework (permitting, water rights)"
        ],
        primary_authority=[
            "Lund & Boyd (2015) - Direct Utilization of Geothermal Energy 2015 Worldwide Review",
            "IGA Best Practices Guide for Direct Use (2014)",
            "Bloomquist (2003) - Geothermal District Heating"
        ],
        burden_holder="Developer to demonstrate heat demand exists and economics are favorable vs alternatives",
        adversary_position="Natural gas utilities oppose loss of customers; municipalities may be reluctant to invest in infrastructure",
        counter_arguments=[
            "High upfront capital for distribution pipelines (must have dense heat load)",
            "Heat demand is seasonal (low summer utilization unless cooling added)",
            "Existing natural gas infrastructure is sunk cost (hard to compete on short-term marginal cost)",
            "Temperature losses in long pipelines (insulation expensive)"
        ],
        resolution_strategy="Target high-density developments (new urban districts, industrial parks, university campuses). Use CHP to maximize value (sell electricity, use waste heat). Start with anchor loads (large greenhouse, industrial customer) then expand. Public-private partnerships for infrastructure financing. Include cooling in summer (absorption chillers use geothermal heat).",
        entity_scope="Moderate-temperature geothermal resources (40-150 degC) near heat demand",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Direct use technology proven globally; economics site-specific but methodology established",
        controlling_precedent="Lund & Boyd (2015) WGC review is authoritative global survey",
        issue_category=IssueCategory.HEAT_PUMP_SYSTEMS,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Geothermal Environmental Impact Assessment",
        keywords=["environmental impact", "EIA", "land use", "water consumption", "emissions", "subsidence", "seismicity", "noise", "visual"],
        conclusion_template="Geothermal has minimal environmental footprint vs fossil fuels: 1-8 acres/MW land use (vs 40+ for solar), near-zero air emissions for binary plants, low water consumption (closed-loop reinjection), no fuel supply chain. Primary impacts: land disturbance during construction, H2S emissions (flash plants), induced seismicity risk (managed via protocols), subsidence (rare, monitored). Environmental permitting requires EIA addressing 10+ impact categories.",
        reasoning_framework="""
Environmental Impact Assessment (EIA) components:

1) Air quality:
   - Binary plants: zero emissions (closed loop)
   - Flash plants: CO2 (0.1-0.5 kg/kWh), H2S (<30 ppm with abatement)
   - Comparison: coal 1.0 kg CO2/kWh, natural gas 0.4 kg CO2/kWh
   - Mitigation: Stretford/LO-CAT for H2S, continuous monitoring

2) Water use:
   - Geothermal is closed-loop: 100% reinjection (no net water consumption)
   - Air-cooled condensers: zero water for cooling (vs 1-3 L/kWh for wet cooling)
   - Drilling phase: temporary water use for mud (returned after drilling)
   - Comparison: coal/nuclear 2-3 L/kWh, solar thermal 3-4 L/kWh

3) Land use:
   - Geothermal: 1-8 acres/MW (compact, drilling pads + plant)
   - Solar PV: 40-50 acres/MW
   - Wind: 50-100 acres/MW (including spacing)
   - Coal: 10-20 acres/MW (including mine, ash ponds)

4) Subsidence:
   - Mechanism: pressure drawdown + thermal contraction -> ground surface lowering
   - Risk highest in sedimentary basins (compressible formations)
   - Rare: <2 cm/year for well-managed fields
   - Mitigation: pressure maintenance via reinjection, InSAR monitoring
   - Example: Wairakei (NZ) experienced 15 m subsidence (no reinjection 1950s-1990s)

5) Induced seismicity:
   - Addressed in separate doctrine (traffic light protocol)
   - Requires seismic monitoring network and response plan

6) Noise:
   - Drilling phase: 70-90 dB at 100 m (temporary, 24/7 for 30-60 days per well)
   - Operations: 50-70 dB at plant boundary (cooling fans, turbine)
   - Mitigation: sound walls, setbacks from residences (500 m typical)

7) Visual impact:
   - Cooling towers (20-40 m height, steam plume in cold weather)
   - Wellhead structures (2-5 m height)
   - Pipelines (above-ground insulated, can be buried for aesthetics)
   - Mitigation: earth-tone colors, landscaping, screening

8) Ecosystem disturbance:
   - Construction footprint: access roads, drill pads, pipelines
   - Permanent disturbance: 2-5% of project area
   - Habitat fragmentation (roads), erosion during construction
   - Mitigation: minimize road width, erosion controls, restoration of temporary areas

9) Groundwater impacts:
   - Risk: casing leak -> contamination of shallow aquifers
   - Prevention: multiple casing strings, cement bond logs, pressure testing
   - Monitoring: baseline groundwater quality, quarterly sampling
   - Regulations: isolation of freshwater aquifers (surface casing >50 m below deepest aquifer)

10) Cultural/archaeological:
    - Geothermal areas often sacred to indigenous peoples (hot springs, fumaroles)
    - Archaeological sites may be present in volcanic regions
    - Consultation with tribes/communities required
    - Mitigation: avoidance of sacred sites, archaeological surveys before construction

Permitting process:
- Federal (US): NEPA Environmental Assessment (EA) or Environmental Impact Statement (EIS)
  - EA: for minor impacts, 6-12 months
  - EIS: for significant impacts, 18-36 months
- State: air quality permits, water discharge permits, drilling permits
- Local: land use approval, building permits

Public engagement:
- Scoping meetings to identify community concerns
- Draft EIA public comment period (30-90 days)
- Public hearings before approval
- Common concerns: seismicity, noise, visual, property values

Best practices:
- Baseline environmental monitoring (1 year before construction)
- Adaptive management: adjust operations if monitoring shows impacts
- Financial assurance (bond) for reclamation
- Decommissioning plan (well plugging, site restoration)
        """,
        key_factors=[
            "Proximity to sensitive receptors (residents, schools, hospitals)",
            "Air quality attainment status (non-attainment areas have stricter limits)",
            "Groundwater quality baseline (determine pre-existing contamination)",
            "Presence of endangered species or critical habitat",
            "Cultural resources (sacred sites, archaeological)",
            "Seismic risk perception (public acceptance)"
        ],
        primary_authority=[
            "IFC Environmental, Health, and Safety Guidelines for Geothermal Power (2015)",
            "NEPA 40 CFR 1500-1508 - Environmental Impact Statement requirements",
            "DiPippo (2012) - Geothermal Power Plants ch 18 Environmental Impact"
        ],
        burden_holder="Developer to demonstrate impacts are minimized and meet regulatory standards",
        adversary_position="Environmental groups may oppose any development; community concerned about property values and quality of life",
        counter_arguments=[
            "Binary plants have zero emissions but are more expensive (trade-off)",
            "Subsidence risk requires long-term monitoring (liability uncertainty)",
            "Visual impact of cooling towers objectionable to some (NIMBYism)",
            "Drilling noise is temporary but severe (affects nearby residents)"
        ],
        resolution_strategy="Comprehensive EIA addressing all impact categories. Use binary cycle in environmentally sensitive areas (zero emissions). Commit to traffic light seismic protocol. Offer to relocate affected residents if subsidence >5 cm. Establish community benefit fund (royalty sharing, local hiring). Transparent monitoring with public web portal.",
        entity_scope="All geothermal projects requiring environmental permits",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="EIA methodology well-established; geothermal environmental profile favorable vs fossil fuels; impacts manageable with best practices",
        controlling_precedent="NEPA (1970) and IFC EHS Guidelines (2015) define impact assessment requirements",
        issue_category=IssueCategory.ENVIRONMENTAL_IMPACT,
        fragility_score=0.35
    ),

]


# ============================================================================
# GEOTHERMAL ENGINE CORE
# ============================================================================

class GeothermalEngine:
    """ENRG06 Geothermal Energy Systems Intelligence Engine - TIE Grade"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9241
        self.telemetry_events: List[TelemetryEvent] = []
        self.doctrine_triggers: Dict[str, int] = {}
        self.metrics = {
            "queries_total": 0,
            "cache_hits": 0,
            "avg_latency_ms": 0.0,
            "doctrines_available": len(DOCTRINE_CACHE)
        }
        logger.info(f"ENRG06 Geothermal Engine initialized v{self.version} on port {self.port}")
        logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """
        TIE-20 Component: Three-layer response architecture
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-2000ms)
        Layer 3: Deep analysis with external data (2000ms+)
        """
        start_time = time.time()

        # Layer 1: Doctrine cache lookup
        matched_doctrines = self._doctrine_cache_lookup(query)

        if matched_doctrines:
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Cache hit: {len(matched_doctrines)} doctrines matched in {latency_ms:.1f}ms")
            self.metrics["cache_hits"] += 1

            response = self._format_response(matched_doctrines, mode, zone)
            self._record_telemetry(query, mode, zone, latency_ms, matched_doctrines, cache_hit=True)
            return response

        # Layer 2: Semantic retrieval (fallback)
        logger.info("Cache miss, attempting semantic retrieval")
        semantic_results = self._semantic_retrieval(query)

        latency_ms = (time.time() - start_time) * 1000
        response = self._format_response(semantic_results, mode, zone)
        self._record_telemetry(query, mode, zone, latency_ms, semantic_results, cache_hit=False)

        return response

    def _doctrine_cache_lookup(self, query: str) -> List[DoctrineBlock]:
        """Match query against doctrine block keywords"""
        query_lower = query.lower()
        matches = []

        for doctrine in DOCTRINE_CACHE:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = any(word in doctrine.topic.lower() for word in query_lower.split())

            if keyword_matches >= 2 or topic_match:
                matches.append(doctrine)
                self.doctrine_triggers[doctrine.topic] = self.doctrine_triggers.get(doctrine.topic, 0) + 1

        return matches

    def _semantic_retrieval(self, query: str) -> List[DoctrineBlock]:
        """Fallback semantic matching when cache misses"""
        # Simple semantic matching via query term overlap
        query_terms = set(query.lower().split())
        scored_doctrines = []

        for doctrine in DOCTRINE_CACHE:
            all_terms = set(" ".join(doctrine.keywords).lower().split())
            all_terms.update(doctrine.topic.lower().split())
            overlap = len(query_terms & all_terms)
            if overlap > 0:
                scored_doctrines.append((overlap, doctrine))

        scored_doctrines.sort(reverse=True, key=lambda x: x[0])
        return [d for _, d in scored_doctrines[:3]]

    def _format_response(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Dict[str, Any]:
        """Format response based on mode (FAST/DEFENSE/MEMO)"""

        if not doctrines:
            return {
                "answer": "No specific geothermal doctrine matched. Please refine query with terms like: resource assessment, well design, flash steam, binary cycle, EGS, heat pump, scaling, seismicity, LCOE.",
                "confidence": ConfidenceLevel.DISCLOSURE.value,
                "doctrines_triggered": [],
                "mode": mode.value,
                "zone": zone.value
            }

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            answer = f"{primary.conclusion_template}\n\nKey factors: {'; '.join(primary.key_factors[:3])}"

        elif mode == ResponseMode.DEFENSE:
            answer = f"CONCLUSION: {primary.conclusion_template}\n\n"
            answer += f"REASONING:\n{primary.reasoning_framework[:500]}...\n\n"
            answer += f"AUTHORITY: {', '.join(primary.primary_authority)}\n\n"
            answer += f"RISK FACTORS: {'; '.join(primary.counter_arguments[:3])}\n\n"
            answer += f"MITIGATION: {primary.resolution_strategy}"

        else:  # MEMO
            answer = f"GEOTHERMAL ENERGY ANALYSIS - {primary.topic.upper()}\n\n"
            answer += f"ISSUE CATEGORY: {primary.issue_category.value}\n"
            answer += f"ANALYSIS ZONE: {zone.value}\n\n"
            answer += f"EXECUTIVE SUMMARY:\n{primary.conclusion_template}\n\n"
            answer += f"DETAILED REASONING:\n{primary.reasoning_framework}\n\n"
            answer += f"KEY TECHNICAL FACTORS:\n" + "\n".join(f"- {f}" for f in primary.key_factors) + "\n\n"
            answer += f"AUTHORITATIVE SOURCES:\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"
            answer += f"RISK ANALYSIS:\n" + "\n".join(f"- {c}" for c in primary.counter_arguments) + "\n\n"
            answer += f"RECOMMENDED STRATEGY:\n{primary.resolution_strategy}\n\n"
            answer += f"CONFIDENCE ASSESSMENT: {primary.confidence_stratification}"

        return {
            "answer": answer,
            "confidence": primary.confidence.value,
            "doctrines_triggered": [d.topic for d in doctrines],
            "issue_categories": list(set(d.issue_category.value for d in doctrines)),
            "authorities": primary.primary_authority,
            "mode": mode.value,
            "zone": zone.value,
            "fragility_score": primary.fragility_score
        }

    def _record_telemetry(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        latency_ms: float,
        doctrines: List[DoctrineBlock],
        cache_hit: bool
    ):
        """TIE-20 Component: Telemetry collection"""
        event = TelemetryEvent(
            timestamp=datetime.utcnow().isoformat(),
            query=query[:200],
            mode=mode.value,
            latency_ms=round(latency_ms, 2),
            doctrines_triggered=[d.topic for d in doctrines],
            cache_hit=cache_hit,
            confidence=doctrines[0].confidence.value if doctrines else "NONE",
            zone=zone.value,
            determinism_hash=self._determinism_hash(query, mode, zone)
        )
        self.telemetry_events.append(event)
        self.metrics["queries_total"] += 1

        # Update rolling average latency
        n = self.metrics["queries_total"]
        old_avg = self.metrics["avg_latency_ms"]
        self.metrics["avg_latency_ms"] = ((old_avg * (n - 1)) + latency_ms) / n

    def _determinism_hash(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """TIE-20 Component: SHA-256 determinism hash"""
        content = f"{query}|{mode.value}|{zone.value}|v{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def coverage_map(self) -> Dict[str, Any]:
        """TIE-20 Component: Doctrine coverage analysis"""
        triggered = set(self.doctrine_triggers.keys())
        available = set(d.topic for d in DOCTRINE_CACHE)
        missed = available - triggered

        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "triggered": len(triggered),
            "missed": len(missed),
            "coverage_percent": round(len(triggered) / len(DOCTRINE_CACHE) * 100, 1),
            "triggered_topics": list(triggered),
            "missed_topics": list(missed)
        }

    def drift_watcher(self) -> Dict[str, Any]:
        """TIE-20 Component: Detect doctrinal drift over time"""
        # Simplified: track doctrine trigger frequency
        if not self.doctrine_triggers:
            return {"status": "insufficient_data", "queries_needed": 10}

        total_triggers = sum(self.doctrine_triggers.values())
        freq_dist = {k: v/total_triggers for k, v in self.doctrine_triggers.items()}

        # Flag doctrines never triggered (potential gaps)
        never_triggered = [d.topic for d in DOCTRINE_CACHE if d.topic not in self.doctrine_triggers]

        return {
            "total_queries": self.metrics["queries_total"],
            "unique_doctrines_triggered": len(self.doctrine_triggers),
            "never_triggered": never_triggered,
            "most_frequent": sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)[:5]
        }


# ============================================================================
# FASTAPI SERVER
# ============================================================================

APP = FastAPI(
    title="ENRG06 Geothermal Energy Systems Intelligence Engine",
    version="1.0.0",
    description="TIE-Grade expert system for geothermal resource assessment, well design, power plant technology, EGS, and heat pumps"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GeothermalEngine()


class QueryRequest(BaseModel):
    query: str = Field(..., description="Geothermal engineering question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.DESIGN, description="Analysis context zone")


class QueryResponse(BaseModel):
    answer: str
    confidence: str
    doctrines_triggered: List[str]
    issue_categories: List[str]
    authorities: List[str]
    mode: str
    zone: str
    fragility_score: float


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint - TIE three-layer response"""
    logger.info(f"Query received: {req.query[:100]} [mode={req.mode.value}, zone={req.zone.value}]")
    result = engine.three_layer_response(req.query, req.mode, req.zone)
    return result


@APP.get("/health")
async def health_check():
    """TIE-20 Component: Health endpoint"""
    return {
        "status": "operational",
        "engine": "ENRG06_geothermal_energy",
        "version": engine.version,
        "port": engine.port,
        "metrics": engine.metrics,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "uptime_queries": engine.metrics["queries_total"]
    }


@APP.get("/coverage")
async def coverage_endpoint():
    """TIE-20 Component: Coverage map"""
    return engine.coverage_map()


@APP.get("/drift")
async def drift_endpoint():
    """TIE-20 Component: Drift watcher"""
    return engine.drift_watcher()


@APP.get("/telemetry")
async def telemetry_endpoint(limit: int = 50):
    """TIE-20 Component: Telemetry retrieval"""
    recent = engine.telemetry_events[-limit:]
    return {
        "total_events": len(engine.telemetry_events),
        "returned": len(recent),
        "events": [asdict(e) for e in recent]
    }


@APP.get("/doctrines")
async def doctrines_list():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "fragility": d.fragility_score
            }
            for d in DOCTRINE_CACHE
        ]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting ENRG06 Geothermal Engine on port {engine.port}")
    uvicorn.run(APP, host="0.0.0.0", port=engine.port)
