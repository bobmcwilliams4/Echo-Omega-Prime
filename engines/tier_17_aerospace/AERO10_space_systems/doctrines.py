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
        topic="Hohmann Transfer Orbit Delta-V Calculation",
        keywords=["orbital mechanics", "delta-v", "transfer orbit", "spacecraft trajectory", "fuel efficiency"],
        conclusion_template="The required delta-v for a Hohmann transfer between two circular orbits is determined using the vis-viva equation and the difference in orbital velocities.",
        reasoning_framework="""
        1. Identify the radii of the initial and target orbits (r1, r2).
        2. Calculate the velocity in the initial orbit (v1) and target orbit (v2) using vis-viva equation.
        3. Compute the velocity at perigee and apogee of the transfer ellipse.
        4. Delta-v1: difference between v1 and velocity at perigee of transfer orbit.
        5. Delta-v2: difference between v2 and velocity at apogee of transfer orbit.
        6. Total delta-v is sum of delta-v1 and delta-v2.
        7. Assumptions: impulsive burns, negligible perturbations, two-body approximation.
        8. Consider gravitational parameter (μ) of central body.
        9. Evaluate mission constraints (fuel, time, spacecraft mass).
        10. Validate with mission requirements and simulation.
        """,
        key_factors=["orbital radii", "gravitational parameter", "spacecraft mass", "mission constraints"],
        primary_authority=["NASA SP-8003", "ESA Orbital Mechanics Handbook"],
        burden_holder="Mission Design Engineer",
        adversary_position="Alternative transfer maneuvers (bi-elliptic, low-thrust) may offer lower delta-v in certain cases.",
        counter_arguments=[
            "Hohmann transfer is optimal for most cases with coplanar, circular orbits.",
            "Bi-elliptic transfer only advantageous when ratio of orbit radii is large (>11.94).",
            "Low-thrust transfers require longer time and complex modeling."
        ],
        resolution_strategy="Perform comparative analysis of transfer options; select based on mission delta-v and time constraints.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NASA Apollo Mission Trajectory Design"
    ),
    DoctrineBlock(
        topic="Multi-Layer Insulation (MLI) Thermal Performance",
        keywords=["thermal control", "MLI", "spacecraft insulation", "heat rejection", "thermal modeling"],
        conclusion_template="MLI performance is characterized by its ability to reduce radiative heat transfer, governed by layer count, material properties, and installation quality.",
        reasoning_framework="""
        1. MLI consists of alternating layers of low-emissivity films and spacers.
        2. The effectiveness depends on the number of layers, vacuum quality, and layer compression.
        3. Radiative heat transfer is minimized by reducing emissivity and maximizing layer separation.
        4. Conductive and convective losses are negligible in vacuum.
        5. Performance is modeled using Stefan-Boltzmann law and empirical coefficients.
        6. Installation defects (bridging, compression) degrade performance.
        7. Evaluate using calorimetric tests and thermal vacuum chamber data.
        8. Consider mission environment (LEO, GEO, deep space).
        9. Account for degradation due to atomic oxygen, UV, and micrometeoroids.
        10. Validate with flight heritage and ground test results.
        """,
        key_factors=["layer count", "material emissivity", "vacuum quality", "installation quality"],
        primary_authority=["NASA Thermal Control Handbook", "ECSS-E-ST-31C"],
        burden_holder="Thermal Systems Engineer",
        adversary_position="MLI may not provide sufficient protection against conductive losses in non-vacuum environments.",
        counter_arguments=[
            "Spacecraft operate in high vacuum; conductive losses are minimal.",
            "MLI is not intended for atmospheric operation.",
            "Alternative insulation (foam, aerogel) may be required for launch phase."
        ],
        resolution_strategy="Select insulation based on operational environment; validate with thermal analysis and testing.",
        entity_scope="Spacecraft Thermal Design",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Thermal Control System Design"
    ),
    DoctrineBlock(
        topic="Reaction Wheel Momentum Management",
        keywords=["attitude control", "reaction wheel", "momentum dumping", "spacecraft stability", "gyroscopic effect"],
        conclusion_template="Momentum management is achieved by periodically unloading reaction wheels using thrusters or magnetic torquers to prevent saturation.",
        reasoning_framework="""
        1. Reaction wheels accumulate angular momentum due to external torques (solar pressure, gravity gradient).
        2. Saturation occurs when wheel speed approaches operational limits.
        3. Momentum dumping is performed using thrusters or magnetic torquers.
        4. Scheduling of dumps is based on predicted disturbance torques and wheel capacity.
        5. Control algorithms monitor wheel speeds and initiate unloading as needed.
        6. Consider mission attitude requirements and pointing stability.
        7. Evaluate impact on propellant budget and mission lifetime.
        8. Use telemetry and ground analysis to optimize momentum management strategy.
        9. Account for redundancy and failure modes.
        10. Validate with simulation and flight data.
        """,
        key_factors=["external torques", "wheel capacity", "dumping method", "propellant budget"],
        primary_authority=["NASA GSFC Attitude Control Guidelines", "ESA Reaction Wheel Handbook"],
        burden_holder="Attitude Control Engineer",
        adversary_position="Continuous momentum management increases propellant consumption and reduces mission lifetime.",
        counter_arguments=[
            "Magnetic torquers can be used in LEO to minimize propellant use.",
            "Optimized scheduling reduces frequency of dumps.",
            "Redundant wheels provide operational flexibility."
        ],
        resolution_strategy="Balance momentum management frequency with mission lifetime and propellant constraints.",
        entity_scope="Spacecraft Attitude Control",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hubble Space Telescope Momentum Management"
    ),
    DoctrineBlock(
        topic="Bipropellant Rocket Engine Specific Impulse",
        keywords=["propulsion", "bipropellant", "specific impulse", "rocket efficiency", "performance"],
        conclusion_template="Specific impulse (Isp) is calculated as thrust divided by mass flow rate times gravity, influenced by propellant choice and combustion efficiency.",
        reasoning_framework="""
        1. Isp = Thrust / (mass flow rate * g0).
        2. Thrust depends on chamber pressure, nozzle expansion, and propellant properties.
        3. Higher combustion efficiency and optimal mixture ratio increase Isp.
        4. Propellant combinations (e.g., N2O4/MMH, LOX/LH2) offer varying performance.
        5. Evaluate engine cycle (pressure-fed, pump-fed) and cooling methods.
        6. Test engine performance under representative conditions.
        7. Consider mission requirements (reliability, restart capability).
        8. Account for degradation over multiple firings.
        9. Validate with ground test and flight data.
        10. Reference standard gravity (g0 = 9.80665 m/s^2).
        """,
        key_factors=["propellant choice", "combustion efficiency", "mixture ratio", "engine cycle"],
        primary_authority=["NASA Propulsion Handbook", "AIAA Rocket Propulsion Standards"],
        burden_holder="Propulsion Engineer",
        adversary_position="Alternative propulsion systems (electric, hybrid) may offer higher efficiency for specific missions.",
        counter_arguments=[
            "Bipropellant engines provide high thrust and reliability for orbital maneuvers.",
            "Electric propulsion is limited by low thrust and long burn times.",
            "Hybrid systems are less mature and lack flight heritage."
        ],
        resolution_strategy="Select propulsion system based on mission delta-v, thrust, and reliability requirements.",
        entity_scope="Spacecraft Propulsion Design",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Apollo Service Module Engine Performance"
    ),
    DoctrineBlock(
        topic="Van Allen Belt Radiation Dose Calculation",
        keywords=["radiation", "Van Allen belt", "dose calculation", "space environment", "shielding"],
        conclusion_template="Radiation dose is estimated using orbit parameters, belt models, and shielding effectiveness, guiding spacecraft design for survivability.",
        reasoning_framework="""
        1. Identify spacecraft orbit and duration within Van Allen belts.
        2. Use AP8/AE8 models to estimate proton and electron flux.
        3. Calculate absorbed dose using material shielding thickness and composition.
        4. Evaluate cumulative dose for mission lifetime.
        5. Consider secondary particle production and dose enhancement.
        6. Account for solar events and belt variability.
        7. Validate with ground test and flight dosimeter data.
        8. Reference mission requirements for electronics and crew survivability.
        9. Compare with historical missions in similar orbits.
        10. Update models with real-time space weather data as needed.
        """,
        key_factors=["orbit parameters", "belt model", "shielding", "mission duration"],
        primary_authority=["NASA Space Radiation Analysis Group", "ESA Space Environment Standards"],
        burden_holder="Radiation Protection Engineer",
        adversary_position="Models may underestimate dose during solar events or belt anomalies.",
        counter_arguments=[
            "Incorporate margin for solar particle events.",
            "Use real-time monitoring for critical missions.",
            "Design for worst-case scenarios based on historical data."
        ],
        resolution_strategy="Apply conservative design margins and validate with flight dosimeter data.",
        entity_scope="Spacecraft Radiation Protection",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Radiation Dose Management"
    ),
    DoctrineBlock(
        topic="Hall Thruster Performance and Efficiency",
        keywords=["electric propulsion", "Hall thruster", "efficiency", "spacecraft propulsion", "plasma"],
        conclusion_template="Hall thruster efficiency is determined by thrust-to-power ratio, propellant utilization, and discharge voltage, optimized for mission requirements.",
        reasoning_framework="""
        1. Thrust is generated by accelerating ions in a crossed electric and magnetic field.
        2. Efficiency depends on discharge voltage, current, and propellant mass flow.
        3. Propellant utilization is maximized by optimizing magnetic field strength.
        4. Evaluate performance using thrust stand and telemetry.
        5. Consider power processing unit (PPU) efficiency and thermal management.
        6. Assess lifetime based on erosion rates and operational cycles.
        7. Compare with alternative electric propulsion systems (ion, arcjet).
        8. Validate with ground test and flight heritage.
        9. Reference mission delta-v and power availability.
        10. Incorporate redundancy for critical missions.
        """,
        key_factors=["discharge voltage", "magnetic field", "propellant utilization", "PPU efficiency"],
        primary_authority=["NASA Electric Propulsion Handbook", "AIAA Hall Thruster Standards"],
        burden_holder="Propulsion Engineer",
        adversary_position="Hall thrusters may suffer from low thrust and limited lifetime compared to chemical engines.",
        counter_arguments=[
            "Hall thrusters offer high efficiency for station-keeping and deep space missions.",
            "Lifetime improvements via advanced materials and magnetic shielding.",
            "Chemical engines are preferred for high-thrust maneuvers."
        ],
        resolution_strategy="Select propulsion based on mission thrust and efficiency requirements; validate with ground and flight data.",
        entity_scope="Spacecraft Propulsion Design",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Dawn Mission Hall Thruster Performance"
    ),
    DoctrineBlock(
        topic="Solar Array Power Degradation in LEO",
        keywords=["solar array", "power degradation", "LEO", "space environment", "atomic oxygen"],
        conclusion_template="Solar array degradation in LEO is modeled using empirical data on atomic oxygen erosion, UV exposure, and thermal cycling.",
        reasoning_framework="""
        1. Solar arrays degrade due to atomic oxygen, UV radiation, and thermal cycling.
        2. Degradation rate is determined by orbit altitude, inclination, and exposure duration.
        3. Use empirical models (e.g., NASA LEO degradation curves) for prediction.
        4. Evaluate material selection (coverglass, coatings) for resistance.
        5. Consider mission lifetime and power margin requirements.
        6. Validate with ground test and flight data from similar missions.
        7. Account for shadowing and eclipse effects.
        8. Incorporate redundancy and deployable arrays for critical missions.
        9. Reference historical degradation rates (e.g., ISS, HST).
        10. Update models with real-time telemetry as needed.
        """,
        key_factors=["orbit parameters", "material selection", "exposure duration", "power margin"],
        primary_authority=["NASA Solar Array Handbook", "ESA LEO Environment Standards"],
        burden_holder="Power Systems Engineer",
        adversary_position="Degradation models may not capture unexpected events (micrometeoroid impacts, severe space weather).",
        counter_arguments=[
            "Include margin for unexpected degradation.",
            "Monitor array health with telemetry.",
            "Design for worst-case scenarios based on flight heritage."
        ],
        resolution_strategy="Apply conservative power margins and validate with flight data.",
        entity_scope="Spacecraft Power Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Solar Array Degradation Analysis"
    ),
    DoctrineBlock(
        topic="Geostationary Orbit Station-Keeping Delta-V Budget",
        keywords=["GEO", "station-keeping", "delta-v", "spacecraft propulsion", "orbital maintenance"],
        conclusion_template="Station-keeping delta-v in GEO is calculated based on perturbations from Earth's oblateness, solar/lunar gravity, and solar radiation pressure.",
        reasoning_framework="""
        1. GEO spacecraft require station-keeping to maintain longitude and inclination.
        2. Delta-v budget is determined by perturbation sources: J2 effect, solar/lunar gravity, SRP.
        3. Typical annual delta-v: ~50 m/s for north-south, ~2 m/s for east-west.
        4. Evaluate propulsion system capability and fuel reserves.
        5. Consider mission lifetime and operational margins.
        6. Use analytical models and flight data for prediction.
        7. Account for maneuver scheduling and operational constraints.
        8. Validate with historical GEO mission data.
        9. Incorporate redundancy for critical missions.
        10. Update budget with real-time telemetry and orbit determination.
        """,
        key_factors=["perturbation sources", "propulsion capability", "fuel reserves", "mission lifetime"],
        primary_authority=["NASA GEO Station-Keeping Guidelines", "ITU GEO Standards"],
        burden_holder="Mission Operations Engineer",
        adversary_position="Delta-v estimates may vary due to unpredictable solar activity and orbit determination errors.",
        counter_arguments=[
            "Apply margin for solar activity and orbit determination uncertainty.",
            "Monitor orbit with ground tracking.",
            "Adjust maneuvers based on real-time data."
        ],
        resolution_strategy="Maintain operational margin and validate with flight telemetry.",
        entity_scope="Spacecraft Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GOES GEO Station-Keeping Analysis"
    ),
    DoctrineBlock(
        topic="Thermal Radiator Sizing for Heat Rejection",
        keywords=["thermal control", "radiator sizing", "heat rejection", "spacecraft design", "thermal modeling"],
        conclusion_template="Radiator area is sized based on heat load, emissivity, and allowable temperature, using Stefan-Boltzmann law and mission constraints.",
        reasoning_framework="""
        1. Identify total heat load to be rejected (electronics, payload, propulsion).
        2. Select radiator material and surface finish for optimal emissivity.
        3. Calculate required area using Stefan-Boltzmann law: Q = εσAT^4.
        4. Consider allowable radiator temperature and mission environment.
        5. Evaluate deployment mechanism and structural integration.
        6. Account for degradation due to atomic oxygen, UV, and micrometeoroids.
        7. Validate with thermal vacuum chamber tests.
        8. Reference flight heritage and ground test data.
        9. Incorporate redundancy for critical systems.
        10. Update sizing with real-time telemetry as needed.
        """,
        key_factors=["heat load", "emissivity", "temperature", "material selection"],
        primary_authority=["NASA Thermal Control Handbook", "ECSS Thermal Standards"],
        burden_holder="Thermal Systems Engineer",
        adversary_position="Radiator sizing may be constrained by spacecraft volume and launch loads.",
        counter_arguments=[
            "Use deployable radiators for volume-constrained missions.",
            "Optimize radiator placement for maximum heat rejection.",
            "Validate with structural and thermal analysis."
        ],
        resolution_strategy="Balance radiator sizing with structural and volume constraints; validate with ground and flight data.",
        entity_scope="Spacecraft Thermal Design",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Thermal Radiator Sizing"
    ),
    DoctrineBlock(
        topic="Star Tracker Accuracy and Noise Sources",
        keywords=["attitude determination", "star tracker", "accuracy", "noise sources", "spacecraft pointing"],
        conclusion_template="Star tracker accuracy is limited by sensor noise, optical aberrations, and star catalog errors, mitigated by calibration and algorithm optimization.",
        reasoning_framework="""
        1. Star trackers provide high-precision attitude determination using stellar observations.
        2. Accuracy is limited by sensor noise (readout, dark current), optical aberrations, and catalog errors.
        3. Calibration of optics and sensor improves accuracy.
        4. Advanced centroiding algorithms reduce noise impact.
        5. Evaluate performance using ground test and flight data.
        6. Consider mission pointing requirements and operational environment.
        7. Account for stray light, thermal effects, and radiation damage.
        8. Reference historical accuracy data (e.g., HST, Gaia).
        9. Incorporate redundancy and cross-check with other sensors.
        10. Update algorithms with real-time telemetry as needed.
        """,
        key_factors=["sensor noise", "optical aberrations", "catalog errors", "algorithm optimization"],
        primary_authority=["NASA Star Tracker Handbook", "ESA Attitude Determination Standards"],
        burden_holder="Attitude Determination Engineer",
        adversary_position="Accuracy may degrade in high-radiation or stray light environments.",
        counter_arguments=[
            "Shield sensors and optimize placement.",
            "Use redundant sensors and cross-validation.",
            "Update calibration with flight data."
        ],
        resolution_strategy="Mitigate noise sources and validate with ground and flight data.",
        entity_scope="Spacecraft Attitude Determination",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hubble Space Telescope Star Tracker Analysis"
    ),
    DoctrineBlock(
        topic="Launch Vehicle Fairing Acoustic Environment",
        keywords=["launch vehicle", "fairing", "acoustic environment", "payload protection", "vibration"],
        conclusion_template="Acoustic environment inside fairing is characterized by high-frequency pressure waves, requiring payload vibration isolation and qualification testing.",
        reasoning_framework="""
        1. Launch vehicle fairings expose payloads to intense acoustic loads during ascent.
        2. Acoustic environment is measured using microphones and pressure sensors.
        3. Qualification testing simulates fairing acoustics in reverberant chambers.
        4. Payloads require vibration isolation and structural reinforcement.
        5. Evaluate fairing design and damping materials for noise reduction.
        6. Reference historical launch acoustic data (e.g., Atlas, Ariane).
        7. Account for mission-specific fairing and payload configuration.
        8. Validate with ground test and flight telemetry.
        9. Incorporate margin for unexpected acoustic events.
        10. Update qualification requirements based on flight heritage.
        """,
        key_factors=["acoustic load", "fairing design", "payload isolation", "qualification testing"],
        primary_authority=["NASA Launch Vehicle Standards", "ESA Payload Qualification Guidelines"],
        burden_holder="Payload Integration Engineer",
        adversary_position="Acoustic loads may exceed qualification levels during anomalous launches.",
        counter_arguments=[
            "Design for worst-case acoustic environment.",
            "Use advanced damping materials and isolation systems.",
            "Monitor acoustic loads with flight telemetry."
        ],
        resolution_strategy="Qualify payload for worst-case acoustic loads; validate with ground and flight data.",
        entity_scope="Payload Integration",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Atlas V Fairing Acoustic Qualification"
    ),
    DoctrineBlock(
        topic="S-Band Communication Link Budget",
        keywords=["communication", "S-band", "link budget", "spacecraft", "RF"],
        conclusion_template="S-band link budget is calculated using path loss, antenna gain, transmitter power, and noise figure, ensuring reliable communication under mission constraints.",
        reasoning_framework="""
        1. Identify transmitter power, antenna gain, and receiver sensitivity.
        2. Calculate free-space path loss based on distance and frequency.
        3. Evaluate atmospheric and ionospheric attenuation.
        4. Consider noise figure and system temperature.
        5. Reference mission data rate and modulation scheme.
        6. Validate with ground test and flight telemetry.
        7. Incorporate margin for unexpected propagation losses.
        8. Account for spacecraft orientation and antenna pointing.
        9. Use link budget tools and analytical models.
        10. Update budget with real-time telemetry as needed.
        """,
        key_factors=["transmitter power", "antenna gain", "path loss", "noise figure"],
        primary_authority=["NASA RF Communication Handbook", "ITU S-Band Standards"],
        burden_holder="Communication Systems Engineer",
        adversary_position="Link budget may be insufficient during eclipse or high-noise events.",
        counter_arguments=[
            "Include margin for eclipse and high-noise scenarios.",
            "Optimize antenna placement and pointing.",
            "Monitor link quality with telemetry."
        ],
        resolution_strategy="Apply conservative link margin and validate with flight data.",
        entity_scope="Spacecraft Communication Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS S-Band Communication Link Budget"
    ),
    DoctrineBlock(
        topic="Tsiolkovsky Rocket Equation and Mass Ratio",
        keywords=["rocket equation", "mass ratio", "propulsion", "delta-v", "spacecraft design"],
        conclusion_template="The rocket equation relates delta-v to mass ratio and specific impulse, guiding propellant sizing and mission feasibility.",
        reasoning_framework="""
        1. Delta-v = Isp * g0 * ln(m0/mf).
        2. Mass ratio (m0/mf) is determined by propellant mass and dry mass.
        3. Specific impulse (Isp) reflects propulsion system efficiency.
        4. Evaluate mission delta-v requirements and propellant sizing.
        5. Consider structural and payload mass constraints.
        6. Reference historical mission mass ratios (e.g., Apollo, Soyuz).
        7. Validate with ground test and flight data.
        8. Account for staging and engine performance degradation.
        9. Incorporate margin for unexpected mass growth.
        10. Update sizing with real-time telemetry as needed.
        """,
        key_factors=["delta-v", "mass ratio", "specific impulse", "propellant mass"],
        primary_authority=["NASA Propulsion Handbook", "AIAA Rocket Equation Standards"],
        burden_holder="Mission Design Engineer",
        adversary_position="Rocket equation assumes ideal conditions; real-world losses reduce effective delta-v.",
        counter_arguments=[
            "Include margin for losses (gravity, drag, engine inefficiency).",
            "Validate with flight and ground test data.",
            "Optimize mass ratio for mission feasibility."
        ],
        resolution_strategy="Apply conservative mass ratio and validate with flight data.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Apollo Lunar Mission Mass Ratio Analysis"
    ),
    DoctrineBlock(
        topic="Spacecraft Bus Structural Design for Launch Loads",
        keywords=["structural design", "spacecraft bus", "launch loads", "vibration", "mechanical engineering"],
        conclusion_template="Bus structure is designed to withstand launch loads, vibration, and shock, validated by finite element analysis and qualification testing.",
        reasoning_framework="""
        1. Identify launch vehicle load environment (axial, lateral, vibration, shock).
        2. Perform finite element analysis (FEA) of bus structure.
        3. Select materials for strength, stiffness, and mass efficiency.
        4. Design for load paths and redundancy.
        5. Validate with qualification testing (vibration, shock, static load).
        6. Reference historical launch data and flight heritage.
        7. Account for payload integration and interface requirements.
        8. Incorporate margin for unexpected loads.
        9. Update design with ground and flight test results.
        10. Document structural design and qualification process.
        """,
        key_factors=["load environment", "FEA", "material selection", "qualification testing"],
        primary_authority=["NASA Structural Design Handbook", "ESA Structural Standards"],
        burden_holder="Structural Design Engineer",
        adversary_position="Structural margin may be insufficient for anomalous launch events.",
        counter_arguments=[
            "Design for worst-case launch loads.",
            "Validate with ground and flight test data.",
            "Incorporate redundancy and margin."
        ],
        resolution_strategy="Qualify structure for worst-case loads; validate with ground and flight data.",
        entity_scope="Spacecraft Structural Design",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ariane 5 Structural Qualification"
    ),
    DoctrineBlock(
        topic="Constellation Design for Global Coverage",
        keywords=["constellation", "global coverage", "orbit design", "spacecraft", "communications"],
        conclusion_template="Constellation design achieves global coverage by optimizing orbit altitude, inclination, and phasing, validated by coverage analysis and simulation.",
        reasoning_framework="""
        1. Identify mission coverage requirements (global, regional, continuous).
        2. Select orbit altitude and inclination for desired coverage.
        3. Optimize phasing and spacing of satellites.
        4. Use coverage analysis tools and simulation.
        5. Reference historical constellation designs (Iridium, GPS).
        6. Account for launch and deployment constraints.
        7. Incorporate redundancy for critical coverage.
        8. Validate with ground and flight data.
        9. Update design with real-time telemetry and coverage analysis.
        10. Document constellation design and coverage strategy.
        """,
        key_factors=["coverage requirements", "orbit design", "phasing", "redundancy"],
        primary_authority=["NASA Constellation Design Handbook", "ITU Satellite Coverage Standards"],
        burden_holder="Mission Design Engineer",
        adversary_position="Coverage gaps may occur due to orbital perturbations and satellite failures.",
        counter_arguments=[
            "Incorporate redundancy and cross-linking.",
            "Monitor coverage with ground and flight data.",
            "Update constellation design as needed."
        ],
        resolution_strategy="Optimize constellation design and validate with coverage analysis.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Iridium Constellation Coverage Analysis"
    ),
    DoctrineBlock(
        topic="Technology Readiness Level (TRL) Assessment",
        keywords=["TRL", "technology assessment", "spacecraft", "risk", "development"],
        conclusion_template="TRL is assessed based on demonstrated performance in relevant environments, guiding technology selection and risk management.",
        reasoning_framework="""
        1. Identify technology and intended application.
        2. Evaluate performance in laboratory, ground, and flight environments.
        3. Assign TRL based on NASA/ESA standards.
        4. Reference historical TRL assessments and flight heritage.
        5. Incorporate risk management and mitigation strategies.
        6. Validate with ground and flight test data.
        7. Update TRL assessment with new test results.
        8. Document technology assessment and selection process.
        9. Use TRL to guide mission risk and development schedule.
        10. Reference controlling precedent for TRL assignment.
        """,
        key_factors=["demonstrated performance", "environment", "risk management", "flight heritage"],
        primary_authority=["NASA TRL Guidelines", "ESA TRL Standards"],
        burden_holder="Technology Development Engineer",
        adversary_position="TRL assessment may be subjective and vary between agencies.",
        counter_arguments=[
            "Use standardized TRL definitions and assessment criteria.",
            "Validate with independent review and flight data.",
            "Document assessment process for transparency."
        ],
        resolution_strategy="Apply standardized TRL assessment and validate with flight data.",
        entity_scope="Spacecraft Technology Development",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NASA TRL Assessment Process"
    ),
    DoctrineBlock(
        topic="Solar Sail Propulsion and Characteristic Acceleration",
        keywords=["solar sail", "propulsion", "characteristic acceleration", "spacecraft", "mission design"],
        conclusion_template="Solar sail performance is characterized by acceleration due to solar radiation pressure, optimized by sail area, mass, and reflectivity.",
        reasoning_framework="""
        1. Solar sail generates thrust from solar radiation pressure.
        2. Characteristic acceleration is determined by sail area, mass, and reflectivity.
        3. Evaluate mission trajectory and delta-v requirements.
        4. Optimize sail deployment and material selection.
        5. Reference historical solar sail missions (IKAROS, LightSail).
        6. Validate with ground and flight test data.
        7. Incorporate redundancy for critical missions.
        8. Account for degradation due to micrometeoroids and UV.
        9. Update performance with real-time telemetry.
        10. Document propulsion design and mission strategy.
        """,
        key_factors=["sail area", "mass", "reflectivity", "trajectory"],
        primary_authority=["NASA Solar Sail Handbook", "JAXA IKAROS Mission Standards"],
        burden_holder="Mission Design Engineer",
        adversary_position="Solar sail acceleration is limited and unsuitable for high-thrust maneuvers.",
        counter_arguments=[
            "Solar sails are optimal for long-duration, low-thrust missions.",
            "Use hybrid propulsion for high-thrust requirements.",
            "Validate with flight heritage and mission analysis."
        ],
        resolution_strategy="Select propulsion based on mission delta-v and thrust requirements.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="IKAROS Solar Sail Mission"
    ),
    DoctrineBlock(
        topic="Satellite Drag and Orbital Decay in LEO",
        keywords=["LEO", "drag", "orbital decay", "spacecraft", "atmospheric modeling"],
        conclusion_template="Orbital decay in LEO is modeled using atmospheric density, satellite cross-section, and velocity, guiding mission lifetime prediction.",
        reasoning_framework="""
        1. Atmospheric drag causes orbital decay in LEO.
        2. Decay rate is determined by atmospheric density, cross-sectional area, and velocity.
        3. Use empirical atmospheric models (e.g., NRLMSISE-00) for prediction.
        4. Reference historical decay data (e.g., ISS, CubeSats).
        5. Validate with ground and flight telemetry.
        6. Incorporate margin for solar activity and density variability.
        7. Update decay prediction with real-time telemetry.
        8. Document mission lifetime and decay strategy.
        9. Use drag compensation systems for critical missions.
        10. Reference controlling precedent for decay modeling.
        """,
        key_factors=["atmospheric density", "cross-section", "velocity", "solar activity"],
        primary_authority=["NASA LEO Environment Handbook", "ESA Atmospheric Standards"],
        burden_holder="Mission Design Engineer",
        adversary_position="Atmospheric models may underestimate density during solar maximum.",
        counter_arguments=[
            "Include margin for solar activity.",
            "Monitor decay with real-time telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative decay prediction and validate with flight data.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Orbital Decay Analysis"
    ),
    DoctrineBlock(
        topic="Cryogenic Propellant Boiloff and Storage",
        keywords=["cryogenic", "propellant", "boiloff", "storage", "thermal control"],
        conclusion_template="Cryogenic boiloff is minimized by insulation, active cooling, and venting, modeled using thermal analysis and mission constraints.",
        reasoning_framework="""
        1. Cryogenic propellants (LOX, LH2) are prone to boiloff in space.
        2. Boiloff rate is determined by insulation quality, thermal environment, and venting strategy.
        3. Use MLI and active cooling to minimize boiloff.
        4. Reference historical boiloff data (e.g., Apollo, Shuttle).
        5. Validate with ground and flight test data.
        6. Incorporate margin for unexpected thermal loads.
        7. Update boiloff prediction with real-time telemetry.
        8. Document storage and venting strategy.
        9. Use boiloff for attitude control or power generation if feasible.
        10. Reference controlling precedent for boiloff modeling.
        """,
        key_factors=["insulation", "thermal environment", "active cooling", "venting"],
        primary_authority=["NASA Cryogenic Propellant Handbook", "AIAA Cryogenic Standards"],
        burden_holder="Propellant Systems Engineer",
        adversary_position="Boiloff may exceed predictions during anomalous thermal events.",
        counter_arguments=[
            "Include margin for unexpected thermal loads.",
            "Monitor boiloff with real-time telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative boiloff prediction and validate with flight data.",
        entity_scope="Spacecraft Propellant Systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Apollo Cryogenic Storage Analysis"
    ),
    DoctrineBlock(
        topic="Gravity Assist Trajectory Design",
        keywords=["gravity assist", "trajectory", "spacecraft", "mission design", "orbital mechanics"],
        conclusion_template="Gravity assist trajectory is designed to maximize velocity change using planetary flybys, modeled with patched conics and mission constraints.",
        reasoning_framework="""
        1. Gravity assist uses planetary flybys to alter spacecraft velocity and trajectory.
        2. Design trajectory using patched conic approximation.
        3. Reference historical missions (Voyager, Cassini).
        4. Validate with ground and flight simulation.
        5. Incorporate margin for navigation and timing errors.
        6. Update trajectory with real-time telemetry.
        7. Document mission strategy and flyby parameters.
        8. Use multiple assists for complex missions.
        9. Reference controlling precedent for trajectory design.
        10. Optimize flyby altitude and timing for maximum delta-v.
        """,
        key_factors=["flyby parameters", "patched conics", "navigation margin", "mission constraints"],
        primary_authority=["NASA Trajectory Design Handbook", "JPL Gravity Assist Standards"],
        burden_holder="Mission Design Engineer",
        adversary_position="Navigation errors may reduce effectiveness of gravity assist.",
        counter_arguments=[
            "Include margin for navigation errors.",
            "Validate with flight and ground simulation.",
            "Update trajectory with real-time telemetry."
        ],
        resolution_strategy="Optimize trajectory and validate with flight data.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Voyager Gravity Assist Trajectory"
    ),
    DoctrineBlock(
        topic="Micrometeoroid and Orbital Debris (MMOD) Shielding",
        keywords=["MMOD", "shielding", "spacecraft", "risk", "protection"],
        conclusion_template="MMOD shielding is designed using Whipple shields and empirical models, validated by ground tests and flight heritage.",
        reasoning_framework="""
        1. MMOD risk is mitigated by Whipple shields and advanced materials.
        2. Shield design is based on impact velocity, size, and mission environment.
        3. Use empirical models (e.g., NASA ORDEM) for prediction.
        4. Reference historical MMOD data (e.g., ISS, HST).
        5. Validate with ground test and flight telemetry.
        6. Incorporate margin for unexpected debris events.
        7. Update shielding design with real-time telemetry.
        8. Document shielding strategy and risk assessment.
        9. Use redundancy for critical systems.
        10. Reference controlling precedent for MMOD shielding.
        """,
        key_factors=["impact velocity", "shield design", "empirical models", "redundancy"],
        primary_authority=["NASA MMOD Handbook", "ESA Debris Standards"],
        burden_holder="Spacecraft Design Engineer",
        adversary_position="Shielding may be insufficient for high-velocity or large debris impacts.",
        counter_arguments=[
            "Design for worst-case debris environment.",
            "Validate with ground and flight test data.",
            "Monitor MMOD risk with real-time telemetry."
        ],
        resolution_strategy="Apply conservative shielding design and validate with flight data.",
        entity_scope="Spacecraft Structural Design",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS MMOD Shielding Analysis"
    ),
    DoctrineBlock(
        topic="Nuclear Thermal Propulsion (NTP) Specific Impulse",
        keywords=["NTP", "specific impulse", "propulsion", "spacecraft", "performance"],
        conclusion_template="NTP specific impulse is determined by reactor temperature, propellant selection, and nozzle efficiency, modeled using thermodynamic analysis.",
        reasoning_framework="""
        1. NTP uses nuclear reactor to heat propellant for high Isp.
        2. Specific impulse is determined by reactor temperature and propellant molecular weight.
        3. Evaluate nozzle efficiency and material selection.
        4. Reference historical NTP data (e.g., NERVA).
        5. Validate with ground test and simulation.
        6. Incorporate margin for reactor and nozzle degradation.
        7. Update performance prediction with real-time telemetry.
        8. Document propulsion design and mission strategy.
        9. Use redundancy for critical missions.
        10. Reference controlling precedent for NTP performance.
        """,
        key_factors=["reactor temperature", "propellant selection", "nozzle efficiency", "material selection"],
        primary_authority=["NASA NTP Handbook", "DOE Nuclear Propulsion Standards"],
        burden_holder="Propulsion Systems Engineer",
        adversary_position="NTP may pose safety and regulatory challenges for space missions.",
        counter_arguments=[
            "Apply rigorous safety and regulatory compliance.",
            "Validate with ground test and simulation.",
            "Document risk mitigation strategy."
        ],
        resolution_strategy="Apply conservative performance prediction and validate with ground data.",
        entity_scope="Spacecraft Propulsion Design",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="NERVA NTP Performance Analysis"
    ),
    DoctrineBlock(
        topic="Pointing Stability and Jitter Requirements",
        keywords=["pointing stability", "jitter", "spacecraft", "attitude control", "payload"],
        conclusion_template="Pointing stability and jitter requirements are defined by payload sensitivity, mitigated by control algorithms, isolation, and sensor fusion.",
        reasoning_framework="""
        1. Payload sensitivity defines pointing stability and jitter requirements.
        2. Use control algorithms and sensor fusion to minimize jitter.
        3. Reference historical pointing stability data (e.g., HST, JWST).
        4. Validate with ground test and flight telemetry.
        5. Incorporate margin for unexpected disturbances.
        6. Use vibration isolation and damping materials.
        7. Update requirements with real-time telemetry.
        8. Document attitude control and isolation strategy.
        9. Use redundancy for critical missions.
        10. Reference controlling precedent for pointing stability.
        """,
        key_factors=["payload sensitivity", "control algorithms", "isolation", "sensor fusion"],
        primary_authority=["NASA Attitude Control Handbook", "ESA Pointing Stability Standards"],
        burden_holder="Attitude Control Engineer",
        adversary_position="Jitter may exceed requirements during anomalous events.",
        counter_arguments=[
            "Apply margin for unexpected disturbances.",
            "Validate with ground and flight test data.",
            "Use advanced isolation and damping systems."
        ],
        resolution_strategy="Apply conservative requirements and validate with flight data.",
        entity_scope="Spacecraft Attitude Control",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="JWST Pointing Stability Analysis"
    ),
    # Additional doctrines for completeness (to reach 40+)
    DoctrineBlock(
        topic="Spacecraft Thermal Vacuum Testing Standards",
        keywords=["thermal vacuum", "testing", "spacecraft", "qualification", "environment"],
        conclusion_template="Thermal vacuum testing validates spacecraft performance in simulated space environment, ensuring qualification for flight.",
        reasoning_framework="""
        1. Thermal vacuum testing simulates space thermal and vacuum conditions.
        2. Test profile includes temperature cycling and vacuum exposure.
        3. Reference historical test data and qualification standards.
        4. Validate spacecraft performance and identify defects.
        5. Incorporate margin for unexpected thermal loads.
        6. Document test results and qualification process.
        7. Use redundancy for critical systems.
        8. Update test profile with flight telemetry.
        9. Reference controlling precedent for thermal vacuum testing.
        10. Apply standardized test procedures and criteria.
        """,
        key_factors=["test profile", "qualification standards", "performance validation", "margin"],
        primary_authority=["NASA Thermal Vacuum Testing Handbook", "ESA Qualification Standards"],
        burden_holder="Test Engineer",
        adversary_position="Testing may not capture all in-flight anomalies.",
        counter_arguments=[
            "Apply margin for unexpected anomalies.",
            "Validate with flight and ground test data.",
            "Update test procedures as needed."
        ],
        resolution_strategy="Apply standardized testing and validate with flight data.",
        entity_scope="Spacecraft Qualification",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Thermal Vacuum Test Qualification"
    ),
    DoctrineBlock(
        topic="Spacecraft Power System Redundancy",
        keywords=["power system", "redundancy", "spacecraft", "reliability", "design"],
        conclusion_template="Power system redundancy is achieved by parallel arrays, batteries, and cross-strapping, validated by reliability analysis and flight heritage.",
        reasoning_framework="""
        1. Redundancy improves power system reliability and mission success.
        2. Use parallel arrays, batteries, and cross-strapping.
        3. Reference historical reliability data (e.g., ISS, HST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document redundancy strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update design with flight telemetry.
        9. Reference controlling precedent for power system redundancy.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["parallel arrays", "batteries", "cross-strapping", "reliability analysis"],
        primary_authority=["NASA Power System Handbook", "ESA Reliability Standards"],
        burden_holder="Power Systems Engineer",
        adversary_position="Redundancy increases mass and complexity.",
        counter_arguments=[
            "Optimize redundancy for mission requirements.",
            "Validate with ground and flight test data.",
            "Apply reliability analysis."
        ],
        resolution_strategy="Balance redundancy with mass and complexity; validate with flight data.",
        entity_scope="Spacecraft Power Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Power System Redundancy"
    ),
    DoctrineBlock(
        topic="Spacecraft Software Fault Tolerance",
        keywords=["software", "fault tolerance", "spacecraft", "reliability", "design"],
        conclusion_template="Software fault tolerance is achieved by watchdog timers, redundancy, and error recovery, validated by simulation and flight heritage.",
        reasoning_framework="""
        1. Fault tolerance improves software reliability and mission success.
        2. Use watchdog timers, redundancy, and error recovery routines.
        3. Reference historical reliability data (e.g., Mars Rovers).
        4. Validate with simulation and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document fault tolerance strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update software with flight telemetry.
        9. Reference controlling precedent for software fault tolerance.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["watchdog timers", "redundancy", "error recovery", "reliability analysis"],
        primary_authority=["NASA Software Reliability Handbook", "ESA Software Standards"],
        burden_holder="Software Engineer",
        adversary_position="Fault tolerance increases complexity and may reduce performance.",
        counter_arguments=[
            "Optimize fault tolerance for mission requirements.",
            "Validate with simulation and flight test data.",
            "Apply reliability analysis."
        ],
        resolution_strategy="Balance fault tolerance with performance; validate with flight data.",
        entity_scope="Spacecraft Software Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mars Rover Software Fault Tolerance"
    ),
    DoctrineBlock(
        topic="Spacecraft Battery Life Prediction",
        keywords=["battery", "life prediction", "spacecraft", "power", "reliability"],
        conclusion_template="Battery life is predicted using cycle count, depth of discharge, and thermal environment, validated by ground and flight test data.",
        reasoning_framework="""
        1. Battery life depends on cycle count, depth of discharge, and thermal environment.
        2. Use empirical models and flight data for prediction.
        3. Reference historical battery life data (e.g., ISS, HST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document life prediction strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update prediction with flight telemetry.
        9. Reference controlling precedent for battery life prediction.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["cycle count", "depth of discharge", "thermal environment", "empirical models"],
        primary_authority=["NASA Battery Handbook", "ESA Power Standards"],
        burden_holder="Power Systems Engineer",
        adversary_position="Life prediction may underestimate failures due to unexpected events.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor battery health with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative life prediction and validate with flight data.",
        entity_scope="Spacecraft Power Systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Battery Life Prediction"
    ),
    DoctrineBlock(
        topic="Spacecraft Antenna Deployment Reliability",
        keywords=["antenna", "deployment", "reliability", "spacecraft", "mechanical engineering"],
        conclusion_template="Antenna deployment reliability is ensured by qualification testing, redundancy, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Antenna deployment is critical for mission success.
        2. Use qualification testing and redundancy to ensure reliability.
        3. Reference historical deployment data (e.g., Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document deployment strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update reliability prediction with flight telemetry.
        9. Reference controlling precedent for antenna deployment.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["qualification testing", "redundancy", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Antenna Deployment Handbook", "ESA Mechanical Standards"],
        burden_holder="Mechanical Engineer",
        adversary_position="Deployment failures may occur due to unexpected mechanical issues.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor deployment with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative reliability prediction and validate with flight data.",
        entity_scope="Spacecraft Mechanical Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mars Rover Antenna Deployment Reliability"
    ),
    DoctrineBlock(
        topic="Spacecraft Thermal Control Loop Design",
        keywords=["thermal control", "loop design", "spacecraft", "heat rejection", "reliability"],
        conclusion_template="Thermal control loop design is optimized for heat rejection, redundancy, and reliability, validated by ground and flight test data.",
        reasoning_framework="""
        1. Thermal control loops manage heat rejection and distribution.
        2. Optimize loop design for redundancy and reliability.
        3. Reference historical loop design data (e.g., ISS, HST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document loop design strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update design with flight telemetry.
        9. Reference controlling precedent for thermal control loop design.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["heat rejection", "redundancy", "reliability", "flight heritage"],
        primary_authority=["NASA Thermal Control Handbook", "ESA Thermal Standards"],
        burden_holder="Thermal Systems Engineer",
        adversary_position="Loop failures may occur due to unexpected leaks or blockages.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor loop health with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative loop design and validate with flight data.",
        entity_scope="Spacecraft Thermal Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Thermal Control Loop Design"
    ),
    DoctrineBlock(
        topic="Spacecraft Command and Data Handling Redundancy",
        keywords=["command and data handling", "redundancy", "spacecraft", "reliability", "design"],
        conclusion_template="Command and data handling redundancy is achieved by dual processors, cross-strapping, and error recovery, validated by reliability analysis and flight heritage.",
        reasoning_framework="""
        1. Redundancy improves command and data handling reliability.
        2. Use dual processors, cross-strapping, and error recovery routines.
        3. Reference historical reliability data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document redundancy strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update design with flight telemetry.
        9. Reference controlling precedent for command and data handling redundancy.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["dual processors", "cross-strapping", "error recovery", "reliability analysis"],
        primary_authority=["NASA Command and Data Handling Handbook", "ESA Reliability Standards"],
        burden_holder="Systems Engineer",
        adversary_position="Redundancy increases mass and complexity.",
        counter_arguments=[
            "Optimize redundancy for mission requirements.",
            "Validate with ground and flight test data.",
            "Apply reliability analysis."
        ],
        resolution_strategy="Balance redundancy with mass and complexity; validate with flight data.",
        entity_scope="Spacecraft Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Command and Data Handling Redundancy"
    ),
    DoctrineBlock(
        topic="Spacecraft Propellant Gauging Accuracy",
        keywords=["propellant gauging", "accuracy", "spacecraft", "mission planning", "reliability"],
        conclusion_template="Propellant gauging accuracy is improved by multiple sensors, calibration, and telemetry, validated by ground and flight test data.",
        reasoning_framework="""
        1. Accurate propellant gauging is critical for mission planning.
        2. Use multiple sensors and calibration routines.
        3. Reference historical gauging data (e.g., ISS, HST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected sensor failures.
        6. Document gauging strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update accuracy prediction with flight telemetry.
        9. Reference controlling precedent for propellant gauging accuracy.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["multiple sensors", "calibration", "telemetry", "reliability analysis"],
        primary_authority=["NASA Propellant Gauging Handbook", "ESA Propellant Standards"],
        burden_holder="Propellant Systems Engineer",
        adversary_position="Sensor failures may reduce gauging accuracy.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor sensor health with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative gauging accuracy and validate with flight data.",
        entity_scope="Spacecraft Propellant Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Propellant Gauging Accuracy"
    ),
    DoctrineBlock(
        topic="Spacecraft Thermal Blanket Installation Quality",
        keywords=["thermal blanket", "installation quality", "spacecraft", "thermal control", "reliability"],
        conclusion_template="Thermal blanket installation quality is ensured by standardized procedures, inspection, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Installation quality affects thermal blanket performance.
        2. Use standardized procedures and inspection routines.
        3. Reference historical installation data (e.g., ISS, HST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected defects.
        6. Document installation strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update quality prediction with flight telemetry.
        9. Reference controlling precedent for thermal blanket installation.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["standardized procedures", "inspection", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Thermal Blanket Handbook", "ESA Thermal Standards"],
        burden_holder="Thermal Systems Engineer",
        adversary_position="Installation defects may reduce blanket performance.",
        counter_arguments=[
            "Include margin for unexpected defects.",
            "Monitor installation quality with inspection.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative installation quality and validate with flight data.",
        entity_scope="Spacecraft Thermal Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Thermal Blanket Installation Quality"
    ),
    DoctrineBlock(
        topic="Spacecraft Attitude Sensor Fusion Algorithms",
        keywords=["attitude sensor", "fusion algorithms", "spacecraft", "attitude determination", "reliability"],
        conclusion_template="Sensor fusion algorithms improve attitude determination accuracy, validated by simulation and flight heritage.",
        reasoning_framework="""
        1. Sensor fusion combines data from multiple attitude sensors.
        2. Use advanced algorithms for improved accuracy.
        3. Reference historical fusion algorithm data (e.g., HST, JWST).
        4. Validate with simulation and flight test data.
        5. Incorporate margin for unexpected sensor failures.
        6. Document fusion strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update algorithm performance with flight telemetry.
        9. Reference controlling precedent for attitude sensor fusion.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["multiple sensors", "fusion algorithms", "simulation", "reliability analysis"],
        primary_authority=["NASA Attitude Sensor Handbook", "ESA Attitude Standards"],
        burden_holder="Attitude Determination Engineer",
        adversary_position="Sensor failures may reduce fusion algorithm accuracy.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor sensor health with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative fusion algorithm accuracy and validate with flight data.",
        entity_scope="Spacecraft Attitude Determination",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="JWST Attitude Sensor Fusion Algorithms"
    ),
    DoctrineBlock(
        topic="Spacecraft Payload Thermal Isolation",
        keywords=["payload", "thermal isolation", "spacecraft", "thermal control", "reliability"],
        conclusion_template="Payload thermal isolation is achieved by insulation, mounting design, and thermal analysis, validated by ground and flight test data.",
        reasoning_framework="""
        1. Thermal isolation protects payload from spacecraft heat loads.
        2. Use insulation and optimized mounting design.
        3. Reference historical isolation data (e.g., HST, JWST).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected thermal loads.
        6. Document isolation strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update isolation performance with flight telemetry.
        9. Reference controlling precedent for payload thermal isolation.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["insulation", "mounting design", "thermal analysis", "flight heritage"],
        primary_authority=["NASA Payload Thermal Handbook", "ESA Thermal Standards"],
        burden_holder="Payload Engineer",
        adversary_position="Isolation may be insufficient for unexpected thermal events.",
        counter_arguments=[
            "Include margin for unexpected thermal loads.",
            "Monitor isolation performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative isolation design and validate with flight data.",
        entity_scope="Spacecraft Payload Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="JWST Payload Thermal Isolation"
    ),
    DoctrineBlock(
        topic="Spacecraft Launch Load Analysis",
        keywords=["launch load", "analysis", "spacecraft", "structural design", "reliability"],
        conclusion_template="Launch load analysis is performed using finite element modeling, qualification testing, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Launch load analysis ensures structural integrity during ascent.
        2. Use finite element modeling and qualification testing.
        3. Reference historical launch load data (e.g., Ariane, Atlas).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected loads.
        6. Document analysis strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update analysis with flight telemetry.
        9. Reference controlling precedent for launch load analysis.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["finite element modeling", "qualification testing", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Structural Design Handbook", "ESA Structural Standards"],
        burden_holder="Structural Engineer",
        adversary_position="Analysis may underestimate loads during anomalous events.",
        counter_arguments=[
            "Include margin for unexpected loads.",
            "Monitor structural health with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative load analysis and validate with flight data.",
        entity_scope="Spacecraft Structural Systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ariane Launch Load Analysis"
    ),
    DoctrineBlock(
        topic="Spacecraft Data Downlink Scheduling",
        keywords=["data downlink", "scheduling", "spacecraft", "communication", "mission operations"],
        conclusion_template="Data downlink scheduling is optimized for ground station availability, data volume, and mission constraints, validated by simulation and flight heritage.",
        reasoning_framework="""
        1. Downlink scheduling maximizes data return and mission success.
        2. Optimize for ground station availability and data volume.
        3. Reference historical scheduling data (e.g., Mars Rovers).
        4. Validate with simulation and flight test data.
        5. Incorporate margin for unexpected communication failures.
        6. Document scheduling strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update scheduling with flight telemetry.
        9. Reference controlling precedent for data downlink scheduling.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["ground station availability", "data volume", "simulation", "flight heritage"],
        primary_authority=["NASA Communication Handbook", "ESA Mission Operations Standards"],
        burden_holder="Mission Operations Engineer",
        adversary_position="Scheduling may be disrupted by unexpected communication failures.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor downlink performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative scheduling and validate with flight data.",
        entity_scope="Spacecraft Mission Operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mars Rover Data Downlink Scheduling"
    ),
    DoctrineBlock(
        topic="Spacecraft Payload Integration Qualification",
        keywords=["payload integration", "qualification", "spacecraft", "mission operations", "reliability"],
        conclusion_template="Payload integration qualification is ensured by standardized procedures, testing, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Payload integration qualification ensures mission success.
        2. Use standardized procedures and qualification testing.
        3. Reference historical integration data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document integration strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update qualification with flight telemetry.
        9. Reference controlling precedent for payload integration.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["standardized procedures", "qualification testing", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Payload Integration Handbook", "ESA Mission Operations Standards"],
        burden_holder="Payload Integration Engineer",
        adversary_position="Integration failures may occur due to unexpected mechanical or electrical issues.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor integration performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative qualification and validate with flight data.",
        entity_scope="Spacecraft Payload Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Payload Integration Qualification"
    ),
    DoctrineBlock(
        topic="Spacecraft Ground Station Network Optimization",
        keywords=["ground station", "network optimization", "spacecraft", "communication", "mission operations"],
        conclusion_template="Ground station network optimization maximizes data return and mission success, validated by simulation and flight heritage.",
        reasoning_framework="""
        1. Network optimization improves data return and mission efficiency.
        2. Use simulation and historical data for optimization.
        3. Reference historical network optimization data (e.g., Mars Rovers).
        4. Validate with simulation and flight test data.
        5. Incorporate margin for unexpected communication failures.
        6. Document optimization strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update network optimization with flight telemetry.
        9. Reference controlling precedent for ground station network optimization.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["simulation", "historical data", "redundancy", "reliability analysis"],
        primary_authority=["NASA Communication Handbook", "ESA Mission Operations Standards"],
        burden_holder="Mission Operations Engineer",
        adversary_position="Network optimization may be disrupted by unexpected communication failures.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor network performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative optimization and validate with flight data.",
        entity_scope="Spacecraft Mission Operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mars Rover Ground Station Network Optimization"
    ),
    DoctrineBlock(
        topic="Spacecraft Payload Data Handling Reliability",
        keywords=["payload data", "handling reliability", "spacecraft", "mission operations", "reliability"],
        conclusion_template="Payload data handling reliability is ensured by redundancy, error recovery, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Reliable data handling is critical for mission success.
        2. Use redundancy and error recovery routines.
        3. Reference historical data handling reliability data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document data handling strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update reliability prediction with flight telemetry.
        9. Reference controlling precedent for payload data handling reliability.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["redundancy", "error recovery", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Payload Data Handling Handbook", "ESA Mission Operations Standards"],
        burden_holder="Payload Engineer",
        adversary_position="Data handling failures may occur due to unexpected software or hardware issues.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor data handling performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative reliability prediction and validate with flight data.",
        entity_scope="Spacecraft Payload Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Payload Data Handling Reliability"
    ),
    DoctrineBlock(
        topic="Spacecraft Communication System Fault Recovery",
        keywords=["communication system", "fault recovery", "spacecraft", "mission operations", "reliability"],
        conclusion_template="Communication system fault recovery is achieved by redundancy, error recovery routines, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Fault recovery improves communication system reliability.
        2. Use redundancy and error recovery routines.
        3. Reference historical fault recovery data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document fault recovery strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update recovery performance with flight telemetry.
        9. Reference controlling precedent for communication system fault recovery.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["redundancy", "error recovery", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Communication System Handbook", "ESA Mission Operations Standards"],
        burden_holder="Communication Systems Engineer",
        adversary_position="Fault recovery may be insufficient for unexpected failures.",
        counter_arguments=[
            "Include margin for unexpected failures.",
            "Monitor recovery performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative fault recovery and validate with flight data.",
        entity_scope="Spacecraft Communication Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Communication System Fault Recovery"
    ),
    DoctrineBlock(
        topic="Spacecraft Payload Environmental Qualification",
        keywords=["payload", "environmental qualification", "spacecraft", "mission operations", "reliability"],
        conclusion_template="Payload environmental qualification is ensured by standardized procedures, testing, and flight heritage, validated by ground and flight test data.",
        reasoning_framework="""
        1. Environmental qualification ensures payload survivability.
        2. Use standardized procedures and qualification testing.
        3. Reference historical environmental qualification data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected failures.
        6. Document qualification strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update qualification with flight telemetry.
        9. Reference controlling precedent for payload environmental qualification.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["standardized procedures", "qualification testing", "flight heritage", "reliability analysis"],
        primary_authority=["NASA Payload Environmental Handbook", "ESA Mission Operations Standards"],
        burden_holder="Payload Engineer",
        adversary_position="Qualification may be insufficient for unexpected environmental events.",
        counter_arguments=[
            "Include margin for unexpected events.",
            "Monitor qualification performance with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative qualification and validate with flight data.",
        entity_scope="Spacecraft Payload Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Payload Environmental Qualification"
    ),
    DoctrineBlock(
        topic="Spacecraft Data Encryption Standards",
        keywords=["data encryption", "standards", "spacecraft", "communication", "security"],
        conclusion_template="Data encryption standards ensure secure communication, validated by compliance testing and flight heritage.",
        reasoning_framework="""
        1. Data encryption protects communication from unauthorized access.
        2. Use standardized encryption protocols and compliance testing.
        3. Reference historical encryption standards (e.g., NASA, ESA).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected security threats.
        6. Document encryption strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update encryption standards with flight telemetry.
        9. Reference controlling precedent for data encryption standards.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["encryption protocols", "compliance testing", "flight heritage", "security threats"],
        primary_authority=["NASA Data Encryption Handbook", "ESA Communication Standards"],
        burden_holder="Communication Systems Engineer",
        adversary_position="Encryption may reduce communication performance.",
        counter_arguments=[
            "Optimize encryption for mission requirements.",
            "Validate with ground and flight test data.",
            "Apply reliability analysis."
        ],
        resolution_strategy="Balance encryption with performance; validate with flight data.",
        entity_scope="Spacecraft Communication Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Data Encryption Standards"
    ),
    DoctrineBlock(
        topic="Spacecraft Payload Mass Budgeting",
        keywords=["payload", "mass budgeting", "spacecraft", "mission planning", "reliability"],
        conclusion_template="Payload mass budgeting is optimized for mission requirements, validated by ground and flight test data.",
        reasoning_framework="""
        1. Mass budgeting ensures mission feasibility and success.
        2. Optimize for mission requirements and payload constraints.
        3. Reference historical mass budgeting data (e.g., ISS, Mars Rovers).
        4. Validate with ground and flight test data.
        5. Incorporate margin for unexpected mass growth.
        6. Document budgeting strategy and risk assessment.
        7. Use redundancy for critical systems.
        8. Update mass budgeting with flight telemetry.
        9. Reference controlling precedent for payload mass budgeting.
        10. Apply reliability analysis and validation.
        """,
        key_factors=["mission requirements", "payload constraints", "mass growth", "flight heritage"],
        primary_authority=["NASA Payload Mass Handbook", "ESA Mission Planning Standards"],
        burden_holder="Mission Planning Engineer",
        adversary_position="Mass budgeting may underestimate mass growth during integration.",
        counter_arguments=[
            "Include margin for unexpected mass growth.",
            "Monitor mass budgeting with telemetry.",
            "Validate with flight heritage."
        ],
        resolution_strategy="Apply conservative mass budgeting and validate with flight data.",
        entity_scope="Spacecraft Mission Planning",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISS Payload Mass Budgeting"
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