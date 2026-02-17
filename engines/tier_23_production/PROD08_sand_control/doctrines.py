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
        topic="Critical Drawdown Pressure",
        keywords=["drawdown", "sand production", "pressure", "wellbore stability", "formation failure"],
        conclusion_template="The critical drawdown pressure for sand onset is determined by integrating formation mechanical properties and operational constraints.",
        reasoning_framework="""
        1. Assess formation strength via laboratory testing (e.g., unconfined compressive strength, triaxial tests).
        2. Evaluate in-situ stress and pore pressure using well logs and pressure measurements.
        3. Model wellbore stability with numerical simulations (e.g., Mohr-Coulomb, Drucker-Prager).
        4. Identify operational drawdown limits based on reservoir management objectives.
        5. Correlate sand onset data from field observations and acoustic monitoring.
        6. Integrate uncertainty analysis to account for heterogeneity and anisotropy.
        7. Establish critical drawdown threshold for safe production.
        """,
        key_factors=["Formation strength", "Pore pressure", "In-situ stress", "Operational drawdown", "Reservoir heterogeneity"],
        primary_authority=["API RP 58", "SPE 28890", "Petroleum Engineering Handbook"],
        burden_holder="Operator",
        adversary_position="Aggressive production may exceed critical drawdown, risking sand influx.",
        counter_arguments=[
            "Conservative drawdown limits reduce production rates.",
            "Formation strength may be underestimated due to testing limitations."
        ],
        resolution_strategy="Apply real-time sand monitoring and adaptive drawdown management.",
        entity_scope="Reservoir engineering, production operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 28890: Sand Production Prediction"
    ),
    DoctrineBlock(
        topic="Thick Wall Cylinder Testing",
        keywords=["cylinder test", "formation strength", "mechanical properties", "laboratory analysis"],
        conclusion_template="Thick wall cylinder testing provides reliable formation strength estimates for sand control design.",
        reasoning_framework="""
        1. Prepare core samples according to API standards.
        2. Apply radial pressure to simulate wellbore conditions.
        3. Measure failure pressure and deformation.
        4. Analyze stress distribution and fracture patterns.
        5. Compare results with field sand production data.
        6. Use outcomes to calibrate sand onset models.
        7. Document uncertainties and limitations.
        """,
        key_factors=["Sample quality", "Test pressure", "Stress distribution", "Failure mode"],
        primary_authority=["API RP 60", "SPE 37239"],
        burden_holder="Laboratory analyst",
        adversary_position="Field conditions may not be fully replicated in laboratory tests.",
        counter_arguments=[
            "Sample disturbance affects test reliability.",
            "Scaling effects may distort results."
        ],
        resolution_strategy="Combine cylinder testing with field calibration and numerical modeling.",
        entity_scope="Formation evaluation, laboratory testing",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 60: Thick Wall Cylinder Testing"
    ),
    DoctrineBlock(
        topic="Formation Sand Analysis",
        keywords=["sand analysis", "particle size", "mineralogy", "formation evaluation"],
        conclusion_template="Comprehensive formation sand analysis informs optimal sand control selection.",
        reasoning_framework="""
        1. Collect representative sand samples from core, cuttings, or produced fluids.
        2. Perform sieve analysis for particle size distribution.
        3. Conduct mineralogical assessment using XRD and SEM.
        4. Evaluate grain shape and angularity.
        5. Assess fines content and clay presence.
        6. Integrate results with reservoir petrophysics.
        7. Use findings to guide screen and gravel pack design.
        """,
        key_factors=["Particle size", "Mineralogy", "Fines content", "Grain shape"],
        primary_authority=["API RP 56", "SPE 16954"],
        burden_holder="Geologist",
        adversary_position="Sample contamination may bias analysis.",
        counter_arguments=[
            "Produced sand may differ from in-situ formation.",
            "Sample handling can alter grain properties."
        ],
        resolution_strategy="Use multiple sampling methods and cross-validation.",
        entity_scope="Formation evaluation, geoscience",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 56: Sand Analysis"
    ),
    DoctrineBlock(
        topic="Gravel Sizing Criteria",
        keywords=["gravel pack", "sizing", "screen selection", "sand exclusion"],
        conclusion_template="Gravel sizing criteria are based on formation sand size and screen aperture compatibility.",
        reasoning_framework="""
        1. Analyze formation sand size distribution.
        2. Select gravel size using the 6-to-8 rule (gravel diameter 6-8 times median sand diameter).
        3. Match gravel size to screen slot width for optimal exclusion.
        4. Consider fines migration and bridging efficiency.
        5. Validate sizing with laboratory pack tests.
        6. Document sizing rationale and operational constraints.
        """,
        key_factors=["Sand size", "Gravel size", "Screen aperture", "Fines migration"],
        primary_authority=["API RP 58", "SPE 16954"],
        burden_holder="Completion engineer",
        adversary_position="Oversized gravel may allow sand bypass; undersized gravel increases plugging risk.",
        counter_arguments=[
            "Formation sand size may vary along wellbore.",
            "Fines may migrate despite optimal sizing."
        ],
        resolution_strategy="Use zone-specific sizing and adaptive pack design.",
        entity_scope="Completion engineering",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 58: Gravel Pack Design"
    ),
    DoctrineBlock(
        topic="Gravel Pack Placement",
        keywords=["gravel pack", "placement", "completion", "fluid dynamics", "packing efficiency"],
        conclusion_template="Effective gravel pack placement requires optimized carrier fluid and placement technique.",
        reasoning_framework="""
        1. Select carrier fluid based on formation compatibility and pack stability.
        2. Design placement method (e.g., alpha-beta, single-phase, alternate path).
        3. Monitor pack integrity with pressure and flow measurements.
        4. Evaluate packing efficiency using post-placement logging.
        5. Address voids and channeling with remedial operations if necessary.
        6. Document placement parameters and outcomes.
        """,
        key_factors=["Carrier fluid", "Placement method", "Packing efficiency", "Formation compatibility"],
        primary_authority=["API RP 58", "SPE 16954", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Improper placement leads to incomplete sand exclusion.",
        counter_arguments=[
            "Fluid loss may compromise pack integrity.",
            "Channeling reduces effectiveness."
        ],
        resolution_strategy="Use real-time monitoring and adaptive placement techniques.",
        entity_scope="Completion operations",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Gravel Pack Placement"
    ),
    DoctrineBlock(
        topic="Wire-Wrapped Screen Design",
        keywords=["screen", "wire-wrapped", "slot width", "sand exclusion", "mechanical strength"],
        conclusion_template="Wire-wrapped screens are designed for optimal sand exclusion and mechanical durability.",
        reasoning_framework="""
        1. Select slot width based on formation sand size and gravel pack compatibility.
        2. Specify wire material for corrosion resistance and strength.
        3. Design wrap geometry to maximize open area and minimize plugging.
        4. Validate mechanical integrity with laboratory testing.
        5. Integrate screen design with completion architecture.
        6. Document design parameters and performance criteria.
        """,
        key_factors=["Slot width", "Wire material", "Open area", "Mechanical strength"],
        primary_authority=["API RP 58", "SPE 16954"],
        burden_holder="Completion engineer",
        adversary_position="Slot width may not exclude all sand; wire failure risks production.",
        counter_arguments=[
            "Formation sand size variability challenges slot selection.",
            "Corrosive environments may degrade wire."
        ],
        resolution_strategy="Use multi-layer screens and corrosion-resistant alloys.",
        entity_scope="Completion design",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 58: Screen Design"
    ),
    DoctrineBlock(
        topic="Premium Mesh Screen Selection",
        keywords=["premium screen", "mesh", "sand exclusion", "fine sand", "completion"],
        conclusion_template="Premium mesh screens are selected for high-efficiency sand exclusion in fine-grained formations.",
        reasoning_framework="""
        1. Evaluate formation sand size and fines content.
        2. Select mesh type and aperture based on exclusion requirements.
        3. Assess screen plugging risk and flow capacity.
        4. Validate performance with laboratory and field trials.
        5. Integrate screen selection with completion objectives.
        6. Document selection criteria and operational limitations.
        """,
        key_factors=["Mesh type", "Aperture size", "Plugging risk", "Flow capacity"],
        primary_authority=["SPE 185646", "API RP 58"],
        burden_holder="Completion engineer",
        adversary_position="Mesh screens may plug with fines, reducing productivity.",
        counter_arguments=[
            "High fines content increases plugging risk.",
            "Mesh screens may not withstand high mechanical loads."
        ],
        resolution_strategy="Combine mesh screens with pre-packed gravel and anti-plugging treatments.",
        entity_scope="Completion design",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Mesh Screen Selection"
    ),
    DoctrineBlock(
        topic="Expandable Sand Screen Technology",
        keywords=["expandable screen", "sand control", "wellbore", "completion", "technology"],
        conclusion_template="Expandable sand screens provide adaptable sand exclusion in challenging wellbore geometries.",
        reasoning_framework="""
        1. Assess wellbore geometry and completion requirements.
        2. Select expandable screen type based on formation and operational constraints.
        3. Design expansion process to ensure screen integrity and sand exclusion.
        4. Validate performance with laboratory and field trials.
        5. Monitor screen expansion and placement with real-time data.
        6. Document technology selection and deployment outcomes.
        """,
        key_factors=["Screen type", "Expansion process", "Wellbore geometry", "Sand exclusion"],
        primary_authority=["SPE 185646", "API RP 58"],
        burden_holder="Completion engineer",
        adversary_position="Expansion may compromise screen integrity or sand exclusion.",
        counter_arguments=[
            "Wellbore irregularities may hinder expansion.",
            "Screen may deform under high loads."
        ],
        resolution_strategy="Use pre-expansion modeling and post-placement verification.",
        entity_scope="Completion technology",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Expandable Screen Technology"
    ),
    DoctrineBlock(
        topic="Frac Pack vs Gravel Pack Decision",
        keywords=["frac pack", "gravel pack", "completion", "sand control", "decision criteria"],
        conclusion_template="Frac pack or gravel pack selection is based on formation properties, production objectives, and operational risks.",
        reasoning_framework="""
        1. Evaluate formation permeability and sand production risk.
        2. Assess reservoir pressure and fracture gradient.
        3. Compare productivity enhancement and sand exclusion efficiency.
        4. Analyze operational complexity and cost.
        5. Integrate field experience and precedent.
        6. Document decision rationale and expected outcomes.
        """,
        key_factors=["Formation permeability", "Sand production risk", "Productivity", "Cost"],
        primary_authority=["SPE 185646", "API RP 58"],
        burden_holder="Completion engineer",
        adversary_position="Frac pack may increase sand production risk; gravel pack may limit productivity.",
        counter_arguments=[
            "Frac pack complexity increases operational risk.",
            "Gravel pack may not provide sufficient productivity."
        ],
        resolution_strategy="Use pilot tests and multi-criteria decision analysis.",
        entity_scope="Completion decision-making",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Frac Pack vs Gravel Pack"
    ),
    DoctrineBlock(
        topic="Proppant Selection for Frac Pack",
        keywords=["proppant", "frac pack", "sand control", "completion", "selection"],
        conclusion_template="Proppant selection for frac pack is based on formation compatibility, strength, and conductivity.",
        reasoning_framework="""
        1. Analyze formation properties and fracture geometry.
        2. Select proppant type (sand, ceramic, resin-coated) based on strength and conductivity.
        3. Evaluate proppant transport and placement efficiency.
        4. Assess compatibility with reservoir fluids and completion hardware.
        5. Validate selection with laboratory and field tests.
        6. Document selection criteria and operational risks.
        """,
        key_factors=["Proppant type", "Strength", "Conductivity", "Compatibility"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Incompatible proppant may reduce fracture conductivity or cause screen plugging.",
        counter_arguments=[
            "Ceramic proppants are costly.",
            "Resin-coated proppants may degrade over time."
        ],
        resolution_strategy="Use multi-proppant blends and adaptive placement strategies.",
        entity_scope="Completion operations",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Proppant Selection"
    ),
    DoctrineBlock(
        topic="Resin Consolidation Systems",
        keywords=["resin", "consolidation", "sand control", "formation", "completion"],
        conclusion_template="Resin consolidation systems are applied to stabilize formation sand and reduce production of fines.",
        reasoning_framework="""
        1. Evaluate formation sand properties and fines content.
        2. Select resin type based on compatibility and consolidation strength.
        3. Design resin placement method to ensure uniform coverage.
        4. Monitor consolidation effectiveness with post-treatment logging.
        5. Assess impact on productivity and sand exclusion.
        6. Document system selection and operational outcomes.
        """,
        key_factors=["Resin type", "Consolidation strength", "Placement method", "Formation compatibility"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Resin may impair productivity or fail to consolidate all sand.",
        counter_arguments=[
            "Resin placement may be uneven.",
            "Resin degradation may occur over time."
        ],
        resolution_strategy="Use staged placement and post-treatment verification.",
        entity_scope="Completion technology",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Resin Consolidation"
    ),
    DoctrineBlock(
        topic="Acoustic Sand Monitoring",
        keywords=["acoustic monitoring", "sand production", "real-time", "well surveillance", "completion"],
        conclusion_template="Acoustic sand monitoring enables real-time detection and management of sand production events.",
        reasoning_framework="""
        1. Install acoustic sensors at strategic well locations.
        2. Calibrate sensors to distinguish sand impact signals from background noise.
        3. Integrate monitoring with production control systems.
        4. Analyze acoustic data for sand onset and severity.
        5. Use findings to adjust drawdown and completion parameters.
        6. Document monitoring outcomes and intervention actions.
        """,
        key_factors=["Sensor placement", "Calibration", "Data analysis", "Integration"],
        primary_authority=["SPE 185646", "API RP 58"],
        burden_holder="Production engineer",
        adversary_position="Acoustic monitoring may miss low-rate sand events or generate false positives.",
        counter_arguments=[
            "Sensor sensitivity may be insufficient.",
            "Data interpretation requires expertise."
        ],
        resolution_strategy="Combine acoustic monitoring with other surveillance methods.",
        entity_scope="Production operations",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Acoustic Sand Monitoring"
    ),
    DoctrineBlock(
        topic="Erosion Monitoring and Inspection",
        keywords=["erosion", "monitoring", "inspection", "sand production", "completion"],
        conclusion_template="Erosion monitoring and inspection are essential for maintaining well integrity in sand-producing environments.",
        reasoning_framework="""
        1. Install erosion sensors and inspection tools in critical well sections.
        2. Monitor erosion rates and patterns with real-time data.
        3. Conduct periodic visual and ultrasonic inspections.
        4. Analyze erosion impact on completion hardware and production rates.
        5. Use findings to plan maintenance and intervention.
        6. Document inspection outcomes and remedial actions.
        """,
        key_factors=["Sensor placement", "Inspection frequency", "Erosion rate", "Hardware integrity"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Production engineer",
        adversary_position="Erosion may occur between inspection intervals, risking hardware failure.",
        counter_arguments=[
            "Sensor coverage may be incomplete.",
            "Inspection may miss early-stage erosion."
        ],
        resolution_strategy="Increase inspection frequency and use redundant monitoring.",
        entity_scope="Production operations",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 58: Erosion Monitoring"
    ),
    DoctrineBlock(
        topic="Sand Control Economics",
        keywords=["economics", "sand control", "cost-benefit", "completion", "production"],
        conclusion_template="Sand control economics are evaluated by balancing intervention costs against production and risk mitigation benefits.",
        reasoning_framework="""
        1. Quantify sand control intervention costs (hardware, installation, maintenance).
        2. Estimate production gains and risk reduction from sand exclusion.
        3. Analyze cost-benefit using NPV and ROI metrics.
        4. Consider long-term operational risks and maintenance costs.
        5. Integrate economic analysis with field experience and precedent.
        6. Document economic rationale and decision outcomes.
        """,
        key_factors=["Intervention cost", "Production gain", "Risk reduction", "Long-term maintenance"],
        primary_authority=["API RP 58", "SPE 185646", "Petroleum Economics Handbook"],
        burden_holder="Asset manager",
        adversary_position="High sand control costs may not be justified by incremental production.",
        counter_arguments=[
            "Production gains may be overestimated.",
            "Maintenance costs may escalate over time."
        ],
        resolution_strategy="Use sensitivity analysis and phased investment.",
        entity_scope="Asset management",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Petroleum Economics Handbook: Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Management vs Sand Exclusion",
        keywords=["sand management", "sand exclusion", "completion", "production", "risk"],
        conclusion_template="Sand management or exclusion strategy is selected based on formation risk, production objectives, and operational constraints.",
        reasoning_framework="""
        1. Evaluate formation sand production risk and operational tolerance.
        2. Assess production objectives and hardware limitations.
        3. Compare sand management (allowing controlled sand production) with exclusion (preventing sand ingress).
        4. Analyze impact on productivity, hardware integrity, and maintenance.
        5. Integrate field experience and precedent.
        6. Document strategy selection and expected outcomes.
        """,
        key_factors=["Sand production risk", "Operational tolerance", "Productivity", "Hardware integrity"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Asset manager",
        adversary_position="Sand management may increase maintenance costs; exclusion may limit productivity.",
        counter_arguments=[
            "Hardware may not withstand sand influx.",
            "Exclusion may reduce production rates."
        ],
        resolution_strategy="Use hybrid strategies and adaptive management.",
        entity_scope="Asset management",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Sand Management vs Exclusion"
    ),
    DoctrineBlock(
        topic="Perforation Strategy for Sand Control",
        keywords=["perforation", "strategy", "sand control", "completion", "production"],
        conclusion_template="Perforation strategy is optimized for sand exclusion and productivity by selecting orientation, density, and phasing.",
        reasoning_framework="""
        1. Analyze formation properties and sand production risk.
        2. Select perforation density and phasing to balance productivity and sand exclusion.
        3. Use oriented perforation to minimize sand ingress.
        4. Validate strategy with laboratory and field trials.
        5. Monitor sand production post-perforation.
        6. Document strategy parameters and outcomes.
        """,
        key_factors=["Perforation density", "Phasing", "Orientation", "Formation properties"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="High-density perforation may increase sand production risk.",
        counter_arguments=[
            "Orientation may not be feasible in deviated wells.",
            "Perforation may damage formation."
        ],
        resolution_strategy="Use adaptive perforation and post-placement monitoring.",
        entity_scope="Completion operations",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Perforation Strategy"
    ),
    DoctrineBlock(
        topic="Slotted Liner vs Screen Completions",
        keywords=["slotted liner", "screen", "completion", "sand control", "selection"],
        conclusion_template="Slotted liner or screen completion is selected based on formation properties, sand exclusion efficiency, and operational risks.",
        reasoning_framework="""
        1. Evaluate formation sand size and production risk.
        2. Compare slotted liner and screen exclusion efficiency.
        3. Analyze operational complexity and cost.
        4. Integrate field experience and precedent.
        5. Document selection rationale and expected outcomes.
        """,
        key_factors=["Sand size", "Exclusion efficiency", "Operational complexity", "Cost"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Slotted liner may allow sand bypass; screens may plug with fines.",
        counter_arguments=[
            "Formation sand size variability challenges selection.",
            "Screens may require frequent maintenance."
        ],
        resolution_strategy="Use hybrid completions and adaptive maintenance.",
        entity_scope="Completion design",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Slotted Liner vs Screen"
    ),
    DoctrineBlock(
        topic="Oriented Perforation for Sand Control",
        keywords=["oriented perforation", "sand control", "completion", "wellbore", "productivity"],
        conclusion_template="Oriented perforation enhances sand exclusion by targeting stable formation zones and optimizing flow paths.",
        reasoning_framework="""
        1. Analyze wellbore geometry and formation stability.
        2. Select perforation orientation to minimize sand ingress.
        3. Validate orientation with laboratory and field trials.
        4. Monitor sand production post-perforation.
        5. Document orientation parameters and outcomes.
        """,
        key_factors=["Orientation", "Formation stability", "Flow path", "Sand exclusion"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Orientation may not be feasible in complex wellbores.",
        counter_arguments=[
            "Formation heterogeneity may limit effectiveness.",
            "Orientation tools may fail in high-angle wells."
        ],
        resolution_strategy="Use adaptive orientation and post-placement monitoring.",
        entity_scope="Completion operations",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Oriented Perforation"
    ),
    DoctrineBlock(
        topic="Multi-Zone Sand Control Completions",
        keywords=["multi-zone", "sand control", "completion", "production", "technology"],
        conclusion_template="Multi-zone sand control completions require integrated design and deployment to ensure sand exclusion across all producing intervals.",
        reasoning_framework="""
        1. Analyze formation properties and sand production risk in each zone.
        2. Design completion architecture for multi-zone exclusion.
        3. Select sand control technology for each interval.
        4. Monitor sand production and hardware integrity across zones.
        5. Document design parameters and operational outcomes.
        """,
        key_factors=["Zone properties", "Completion architecture", "Sand control technology", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Multi-zone completions increase operational complexity and risk.",
        counter_arguments=[
            "Hardware may fail in one or more zones.",
            "Sand exclusion efficiency may vary across intervals."
        ],
        resolution_strategy="Use integrated monitoring and adaptive intervention.",
        entity_scope="Completion technology",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Multi-Zone Sand Control"
    ),
    DoctrineBlock(
        topic="Horizontal Well Sand Control Challenges",
        keywords=["horizontal well", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in horizontal wells is challenged by uneven sand production, completion hardware placement, and flow dynamics.",
        reasoning_framework="""
        1. Analyze horizontal well geometry and formation properties.
        2. Design sand control hardware placement for uniform exclusion.
        3. Monitor sand production along wellbore length.
        4. Address uneven flow and sand ingress with adaptive completion.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Well geometry", "Hardware placement", "Flow dynamics", "Sand production"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Horizontal wells may experience localized sand production and hardware failure.",
        counter_arguments=[
            "Hardware placement may be uneven.",
            "Flow dynamics may cause sand bypass."
        ],
        resolution_strategy="Use zonal isolation and real-time monitoring.",
        entity_scope="Completion operations",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Horizontal Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Production Prediction Models",
        keywords=["sand production", "prediction", "modeling", "numerical simulation", "reservoir"],
        conclusion_template="Sand production prediction models integrate formation properties, operational parameters, and historical data for risk assessment.",
        reasoning_framework="""
        1. Collect formation mechanical and petrophysical data.
        2. Select appropriate numerical model (e.g., Mohr-Coulomb, finite element).
        3. Calibrate model with historical sand production data.
        4. Integrate operational parameters (drawdown, flow rate).
        5. Run simulations to predict sand onset and severity.
        6. Document model assumptions and uncertainty.
        """,
        key_factors=["Formation properties", "Operational parameters", "Historical data", "Model calibration"],
        primary_authority=["SPE 28890", "API RP 58"],
        burden_holder="Reservoir engineer",
        adversary_position="Model predictions may not match field reality due to data limitations.",
        counter_arguments=[
            "Formation heterogeneity may not be captured.",
            "Operational changes may invalidate model assumptions."
        ],
        resolution_strategy="Update models with real-time data and adaptive calibration.",
        entity_scope="Reservoir engineering",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 28890: Sand Production Prediction"
    ),
    DoctrineBlock(
        topic="Sand Control Hardware Reliability",
        keywords=["hardware", "reliability", "sand control", "completion", "maintenance"],
        conclusion_template="Sand control hardware reliability is ensured through material selection, design validation, and proactive maintenance.",
        reasoning_framework="""
        1. Select materials for corrosion and erosion resistance.
        2. Validate hardware design with laboratory and field testing.
        3. Monitor hardware performance with real-time sensors.
        4. Conduct periodic maintenance and inspection.
        5. Document reliability metrics and intervention outcomes.
        """,
        key_factors=["Material selection", "Design validation", "Maintenance", "Performance monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Hardware may fail under extreme conditions or due to manufacturing defects.",
        counter_arguments=[
            "Material degradation may occur over time.",
            "Design validation may not capture all failure modes."
        ],
        resolution_strategy="Use redundant hardware and proactive maintenance.",
        entity_scope="Completion operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 58: Hardware Reliability"
    ),
    DoctrineBlock(
        topic="Sand Control Completion Optimization",
        keywords=["completion", "optimization", "sand control", "production", "design"],
        conclusion_template="Sand control completion optimization balances productivity, sand exclusion, and operational risk.",
        reasoning_framework="""
        1. Analyze formation properties and production objectives.
        2. Select completion hardware and placement strategy.
        3. Optimize design with numerical modeling and field trials.
        4. Monitor production and sand exclusion post-completion.
        5. Document optimization parameters and outcomes.
        """,
        key_factors=["Formation properties", "Hardware selection", "Placement strategy", "Production monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Optimization may compromise sand exclusion for productivity.",
        counter_arguments=[
            "Production objectives may conflict with sand control.",
            "Hardware limitations may restrict optimization."
        ],
        resolution_strategy="Use multi-objective optimization and adaptive design.",
        entity_scope="Completion engineering",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Completion Optimization"
    ),
    DoctrineBlock(
        topic="Sand Control in Deepwater Wells",
        keywords=["deepwater", "sand control", "completion", "production", "technology"],
        conclusion_template="Sand control in deepwater wells requires robust hardware and adaptive completion strategies to address high-pressure, high-temperature conditions.",
        reasoning_framework="""
        1. Analyze deepwater formation properties and production risks.
        2. Select hardware rated for high-pressure, high-temperature environments.
        3. Design completion architecture for sand exclusion and operational reliability.
        4. Monitor sand production and hardware integrity with real-time sensors.
        5. Document technology selection and deployment outcomes.
        """,
        key_factors=["Formation properties", "HPHT hardware", "Completion architecture", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Deepwater conditions may exceed hardware limits or complicate completion.",
        counter_arguments=[
            "Hardware may fail under extreme conditions.",
            "Completion may be challenging due to operational constraints."
        ],
        resolution_strategy="Use redundant hardware and adaptive completion strategies.",
        entity_scope="Deepwater operations",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Deepwater Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in High-Rate Gas Wells",
        keywords=["gas well", "high-rate", "sand control", "completion", "production"],
        conclusion_template="Sand control in high-rate gas wells is challenged by high velocity, erosion risk, and hardware selection.",
        reasoning_framework="""
        1. Analyze gas well production rates and sand production risk.
        2. Select hardware for erosion resistance and sand exclusion.
        3. Monitor sand production and erosion with real-time sensors.
        4. Address high velocity with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Production rate", "Erosion risk", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="High-rate gas flow may cause rapid erosion and hardware failure.",
        counter_arguments=[
            "Hardware may not withstand high velocity.",
            "Sand exclusion efficiency may decrease at high rates."
        ],
        resolution_strategy="Use erosion-resistant hardware and frequent monitoring.",
        entity_scope="Gas well operations",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: High-Rate Gas Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Unconsolidated Formations",
        keywords=["unconsolidated formation", "sand control", "completion", "production", "risk"],
        conclusion_template="Sand control in unconsolidated formations requires robust exclusion strategies and frequent monitoring.",
        reasoning_framework="""
        1. Analyze formation properties and sand production risk.
        2. Select hardware and completion strategy for robust exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address formation instability with adaptive intervention.
        5. Document exclusion strategy and operational outcomes.
        """,
        key_factors=["Formation properties", "Exclusion strategy", "Monitoring", "Intervention"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Unconsolidated formations may produce sand despite exclusion efforts.",
        counter_arguments=[
            "Formation instability may cause hardware failure.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Unconsolidated formation operations",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Unconsolidated Formation Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Mature Fields",
        keywords=["mature field", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in mature fields addresses declining formation stability and increased sand production risk.",
        reasoning_framework="""
        1. Analyze mature field formation properties and sand production history.
        2. Select hardware and completion strategy for increased exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address declining stability with adaptive intervention.
        5. Document exclusion strategy and operational outcomes.
        """,
        key_factors=["Formation properties", "Production history", "Exclusion strategy", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Mature fields may produce sand at unpredictable rates.",
        counter_arguments=[
            "Formation instability may cause hardware failure.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Mature field operations",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Mature Field Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Heavy Oil Wells",
        keywords=["heavy oil", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in heavy oil wells is challenged by high viscosity, fines migration, and hardware selection.",
        reasoning_framework="""
        1. Analyze heavy oil properties and sand production risk.
        2. Select hardware for fines exclusion and compatibility with viscous fluids.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address fines migration with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Oil viscosity", "Fines migration", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="High viscosity may impair sand exclusion and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with heavy oil.",
            "Fines migration may cause plugging."
        ],
        resolution_strategy="Use fines-resistant hardware and frequent monitoring.",
        entity_scope="Heavy oil operations",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Heavy Oil Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Thermal Recovery Wells",
        keywords=["thermal recovery", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in thermal recovery wells is challenged by temperature-induced formation changes and hardware degradation.",
        reasoning_framework="""
        1. Analyze thermal recovery process and formation properties.
        2. Select hardware for high-temperature resistance and sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address temperature-induced changes with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Thermal process", "Formation changes", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="High temperature may degrade hardware and impair sand exclusion.",
        counter_arguments=[
            "Hardware may fail under thermal stress.",
            "Formation changes may increase sand production."
        ],
        resolution_strategy="Use temperature-resistant hardware and frequent monitoring.",
        entity_scope="Thermal recovery operations",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Thermal Recovery Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Multilateral Wells",
        keywords=["multilateral well", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in multilateral wells requires integrated hardware and completion strategies to address multiple production branches.",
        reasoning_framework="""
        1. Analyze multilateral well geometry and formation properties.
        2. Design hardware and completion strategy for each branch.
        3. Monitor sand production and hardware integrity across branches.
        4. Address branch-specific challenges with adaptive intervention.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Well geometry", "Branch design", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Multilateral wells may experience uneven sand production and hardware failure.",
        counter_arguments=[
            "Hardware placement may be uneven.",
            "Branch-specific challenges may complicate exclusion."
        ],
        resolution_strategy="Use integrated monitoring and adaptive intervention.",
        entity_scope="Multilateral well operations",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Multilateral Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Carbonate Reservoirs",
        keywords=["carbonate reservoir", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in carbonate reservoirs addresses variable formation properties and increased fines production risk.",
        reasoning_framework="""
        1. Analyze carbonate reservoir properties and sand production risk.
        2. Select hardware and completion strategy for fines exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address variable properties with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Reservoir properties", "Fines exclusion", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Variable properties may impair sand exclusion and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with carbonate formations.",
            "Fines production may cause plugging."
        ],
        resolution_strategy="Use fines-resistant hardware and frequent monitoring.",
        entity_scope="Carbonate reservoir operations",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Carbonate Reservoir Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Sandstone Reservoirs",
        keywords=["sandstone reservoir", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in sandstone reservoirs is based on formation properties, sand production risk, and hardware selection.",
        reasoning_framework="""
        1. Analyze sandstone reservoir properties and sand production risk.
        2. Select hardware and completion strategy for robust exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address formation-specific challenges with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Reservoir properties", "Exclusion strategy", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Sandstone reservoirs may produce sand at unpredictable rates.",
        counter_arguments=[
            "Formation instability may cause hardware failure.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Sandstone reservoir operations",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Sandstone Reservoir Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Shallow Wells",
        keywords=["shallow well", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in shallow wells is challenged by low formation strength and increased sand production risk.",
        reasoning_framework="""
        1. Analyze shallow well formation properties and sand production risk.
        2. Select hardware and completion strategy for robust exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address formation-specific challenges with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Formation properties", "Exclusion strategy", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Low formation strength may impair sand exclusion and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with shallow wells.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Shallow well operations",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Shallow Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in High-Angle Wells",
        keywords=["high-angle well", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in high-angle wells requires adaptive hardware placement and monitoring to address uneven sand production.",
        reasoning_framework="""
        1. Analyze high-angle well geometry and formation properties.
        2. Design hardware placement for uniform sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address uneven sand production with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Well geometry", "Hardware placement", "Sand production", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="High-angle wells may experience uneven sand production and hardware failure.",
        counter_arguments=[
            "Hardware placement may be uneven.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use zonal isolation and real-time monitoring.",
        entity_scope="High-angle well operations",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: High-Angle Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Deviated Wells",
        keywords=["deviated well", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in deviated wells is challenged by hardware placement and uneven sand production.",
        reasoning_framework="""
        1. Analyze deviated well geometry and formation properties.
        2. Design hardware placement for uniform sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address uneven sand production with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Well geometry", "Hardware placement", "Sand production", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Deviated wells may experience uneven sand production and hardware failure.",
        counter_arguments=[
            "Hardware placement may be uneven.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use zonal isolation and real-time monitoring.",
        entity_scope="Deviated well operations",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Deviated Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Artificial Lift Wells",
        keywords=["artificial lift", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in artificial lift wells requires hardware compatibility and frequent monitoring to address sand production and lift efficiency.",
        reasoning_framework="""
        1. Analyze artificial lift system and sand production risk.
        2. Select hardware compatible with lift system and sand exclusion.
        3. Monitor sand production and lift efficiency with real-time sensors.
        4. Address sand production with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Lift system", "Hardware compatibility", "Sand production", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Sand production may impair lift efficiency and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with artificial lift.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Artificial lift operations",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Artificial Lift Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Smart Well Completions",
        keywords=["smart well", "sand control", "completion", "production", "technology"],
        conclusion_template="Sand control in smart well completions integrates real-time monitoring and adaptive hardware for optimal exclusion and productivity.",
        reasoning_framework="""
        1. Analyze smart well completion architecture and sand production risk.
        2. Select hardware for real-time monitoring and adaptive exclusion.
        3. Integrate sand control with smart well control systems.
        4. Monitor sand production and hardware integrity with real-time sensors.
        5. Document technology selection and operational outcomes.
        """,
        key_factors=["Completion architecture", "Monitoring", "Hardware selection", "Integration"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Smart well technology may not be compatible with sand control hardware.",
        counter_arguments=[
            "Integration challenges may impair performance.",
            "Hardware may fail under complex conditions."
        ],
        resolution_strategy="Use integrated monitoring and adaptive hardware.",
        entity_scope="Smart well operations",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Smart Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Subsea Wells",
        keywords=["subsea well", "sand control", "completion", "production", "technology"],
        conclusion_template="Sand control in subsea wells requires robust hardware and adaptive completion strategies to address remote operation and high-pressure conditions.",
        reasoning_framework="""
        1. Analyze subsea well formation properties and sand production risk.
        2. Select hardware rated for high-pressure, remote operation.
        3. Design completion architecture for sand exclusion and operational reliability.
        4. Monitor sand production and hardware integrity with real-time sensors.
        5. Document technology selection and deployment outcomes.
        """,
        key_factors=["Formation properties", "Hardware selection", "Completion architecture", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Subsea conditions may exceed hardware limits or complicate completion.",
        counter_arguments=[
            "Hardware may fail under extreme conditions.",
            "Completion may be challenging due to operational constraints."
        ],
        resolution_strategy="Use redundant hardware and adaptive completion strategies.",
        entity_scope="Subsea operations",
        confidence=0.70,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Subsea Well Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Tight Reservoirs",
        keywords=["tight reservoir", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in tight reservoirs is challenged by low permeability, fines migration, and hardware selection.",
        reasoning_framework="""
        1. Analyze tight reservoir properties and sand production risk.
        2. Select hardware for fines exclusion and compatibility with low-permeability formations.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address fines migration with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Reservoir properties", "Fines migration", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Low permeability may impair sand exclusion and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with tight reservoirs.",
            "Fines migration may cause plugging."
        ],
        resolution_strategy="Use fines-resistant hardware and frequent monitoring.",
        entity_scope="Tight reservoir operations",
        confidence=0.69,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Tight Reservoir Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Fractured Reservoirs",
        keywords=["fractured reservoir", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in fractured reservoirs addresses variable sand production risk and hardware placement challenges.",
        reasoning_framework="""
        1. Analyze fractured reservoir properties and sand production risk.
        2. Select hardware and completion strategy for robust exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address variable properties with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Reservoir properties", "Exclusion strategy", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Variable properties may impair sand exclusion and hardware performance.",
        counter_arguments=[
            "Hardware may not be compatible with fractured formations.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Fractured reservoir operations",
        confidence=0.68,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Fractured Reservoir Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Green Fields",
        keywords=["green field", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in green fields is based on formation properties, sand production risk, and hardware selection.",
        reasoning_framework="""
        1. Analyze green field formation properties and sand production risk.
        2. Select hardware and completion strategy for robust exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address formation-specific challenges with adaptive completion design.
        5. Document strategy and operational outcomes.
        """,
        key_factors=["Formation properties", "Exclusion strategy", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Green fields may produce sand at unpredictable rates.",
        counter_arguments=[
            "Formation instability may cause hardware failure.",
            "Sand exclusion efficiency may decrease over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Green field operations",
        confidence=0.67,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Green Field Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Enhanced Oil Recovery Wells",
        keywords=["enhanced oil recovery", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in EOR wells addresses increased sand production risk due to reservoir stimulation and fluid injection.",
        reasoning_framework="""
        1. Analyze EOR process and formation properties.
        2. Select hardware for robust exclusion and compatibility with injected fluids.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address stimulation-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["EOR process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="EOR may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Injected fluids may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="EOR operations",
        confidence=0.66,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: EOR Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Water Injection Wells",
        keywords=["water injection", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in water injection wells addresses sand production risk due to injection-induced formation changes.",
        reasoning_framework="""
        1. Analyze water injection process and formation properties.
        2. Select hardware for robust exclusion and compatibility with injected water.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address injection-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Injection process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Water injection may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Injected water may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Water injection operations",
        confidence=0.65,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Water Injection Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in CO2 Injection Wells",
        keywords=["CO2 injection", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in CO2 injection wells addresses sand production risk due to injection-induced formation changes and hardware compatibility.",
        reasoning_framework="""
        1. Analyze CO2 injection process and formation properties.
        2. Select hardware for robust exclusion and compatibility with injected CO2.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address injection-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Injection process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="CO2 injection may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Injected CO2 may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="CO2 injection operations",
        confidence=0.64,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: CO2 Injection Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Steam Injection Wells",
        keywords=["steam injection", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in steam injection wells addresses sand production risk due to injection-induced formation changes and hardware degradation.",
        reasoning_framework="""
        1. Analyze steam injection process and formation properties.
        2. Select hardware for high-temperature resistance and sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address injection-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Injection process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Steam injection may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Injected steam may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use temperature-resistant hardware and frequent monitoring.",
        entity_scope="Steam injection operations",
        confidence=0.63,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Steam Injection Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Gas Injection Wells",
        keywords=["gas injection", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in gas injection wells addresses sand production risk due to injection-induced formation changes and hardware compatibility.",
        reasoning_framework="""
        1. Analyze gas injection process and formation properties.
        2. Select hardware for robust exclusion and compatibility with injected gas.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address injection-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Injection process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Gas injection may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Injected gas may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use frequent monitoring and staged intervention.",
        entity_scope="Gas injection operations",
        confidence=0.62,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Gas Injection Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Acid Stimulation Wells",
        keywords=["acid stimulation", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in acid stimulation wells addresses sand production risk due to acid-induced formation changes and hardware compatibility.",
        reasoning_framework="""
        1. Analyze acid stimulation process and formation properties.
        2. Select hardware for acid resistance and sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address acid-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Stimulation process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Acid stimulation may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Acid may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use acid-resistant hardware and frequent monitoring.",
        entity_scope="Acid stimulation operations",
        confidence=0.61,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Acid Stimulation Sand Control"
    ),
    DoctrineBlock(
        topic="Sand Control in Hydraulic Fracturing Wells",
        keywords=["hydraulic fracturing", "sand control", "completion", "production", "challenges"],
        conclusion_template="Sand control in hydraulic fracturing wells addresses sand production risk due to fracture-induced formation changes and hardware compatibility.",
        reasoning_framework="""
        1. Analyze hydraulic fracturing process and formation properties.
        2. Select hardware for fracture compatibility and sand exclusion.
        3. Monitor sand production and hardware integrity with real-time sensors.
        4. Address fracture-induced sand production with adaptive completion design.
        5. Document challenges and mitigation strategies.
        """,
        key_factors=["Fracturing process", "Formation properties", "Hardware selection", "Monitoring"],
        primary_authority=["API RP 58", "SPE 185646"],
        burden_holder="Completion engineer",
        adversary_position="Hydraulic fracturing may increase sand production and hardware failure risk.",
        counter_arguments=[
            "Fracturing may impair hardware performance.",
            "Sand production may increase over time."
        ],
        resolution_strategy="Use fracture-compatible hardware and frequent monitoring.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.60,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185646: Hydraulic Fracturing Sand Control"
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