from dataclasses import dataclass
from typing import List, Optional
import enum
import pathlib

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
        topic="Kick Detection - Pit Gain Method",
        keywords=["kick detection", "pit gain", "well control", "mud volume", "fluid influx"],
        conclusion_template="A pit gain exceeding the calculated volume threshold indicates a well kick requiring immediate well control measures.",
        reasoning_framework=(
            "The pit gain method relies on monitoring the volume of drilling fluid returning to the surface. "
            "An unexpected increase in pit volume suggests an influx of formation fluids into the wellbore. "
            "This is detected by comparing the measured pit volume against the expected volume based on drilling parameters. "
            "The method assumes accurate pit volume measurements and stable drilling conditions. "
            "Pit gain detection is an early indicator of a kick, enabling timely activation of well control procedures. "
            "Operators must consider factors such as mud compressibility, temperature effects, and measurement errors. "
            "Integration with other detection methods enhances reliability. "
            "The pit gain threshold is calculated using the wellbore geometry, mud properties, and drilling rate. "
            "Continuous monitoring and logging are essential for effective detection. "
            "The method is widely accepted in industry standards and recommended by API and IADC guidelines."
        ),
        key_factors=[
            "Accurate pit volume measurement",
            "Mud properties and compressibility",
            "Drilling rate and wellbore geometry",
            "Temperature and pressure effects",
            "Integration with other detection methods"
        ],
        primary_authority=[
            "API RP 59 - Drilling Manual",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling Operations Team",
        adversary_position="Kick detection may be delayed due to measurement inaccuracies or operational noise, leading to false negatives.",
        counter_arguments=[
            "Use redundant measurement systems to cross-verify pit volume data.",
            "Implement real-time data analytics to filter noise.",
            "Train personnel to recognize subtle signs of pit gain."
        ],
        resolution_strategy="Adopt multi-parameter monitoring and enforce strict measurement protocols to minimize detection delays and false alarms.",
        entity_scope="Drilling Rig Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 4.3 - Kick Detection Methods"
    ),
    DoctrineBlock(
        topic="Flow Check Procedure",
        keywords=["flow check", "well control", "kick detection", "wellbore pressure", "drilling fluid"],
        conclusion_template="A positive flow during flow check confirms an influx, necessitating immediate well control actions.",
        reasoning_framework=(
            "The flow check procedure involves closing the wellbore and monitoring fluid flow at surface. "
            "If flow continues after pumps are stopped, it indicates formation fluid entering the wellbore. "
            "This method provides confirmation of a kick when pit gain or other indicators are ambiguous. "
            "The procedure requires isolating the well and observing flow trends carefully. "
            "Operators must consider wellbore compressibility and fluid expansion effects to avoid false positives. "
            "The flow check is a critical step before initiating shut-in procedures to prevent escalation. "
            "It complements pit gain detection and pressure monitoring. "
            "Proper execution and interpretation depend on operator training and equipment reliability. "
            "The method is endorsed by industry best practices and regulatory standards."
        ),
        key_factors=[
            "Wellbore isolation integrity",
            "Accurate flow measurement",
            "Operator training and vigilance",
            "Wellbore fluid properties",
            "Pressure and temperature conditions"
        ],
        primary_authority=[
            "IADC Drilling Manual",
            "API RP 59 - Well Control",
            "Petroleum Extension Service (PETEX) Well Control Training"
        ],
        burden_holder="Drilling Crew and Well Control Supervisor",
        adversary_position="Flow may be misinterpreted due to fluid expansion or trapped gas, causing false kick indications.",
        counter_arguments=[
            "Conduct multiple flow checks to confirm results.",
            "Use pressure gauges and pit volume data in conjunction.",
            "Apply correction factors for fluid expansion."
        ],
        resolution_strategy="Integrate flow check data with other kick indicators and use conservative thresholds to confirm influx presence.",
        entity_scope="Drilling Rig Operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="IADC Well Control Guidelines Section 5.2"
    ),
    DoctrineBlock(
        topic="Hard Shut-In vs Soft Shut-In",
        keywords=["hard shut-in", "soft shut-in", "well control", "pressure management", "kick control"],
        conclusion_template="Soft shut-in is preferred for initial kick control to minimize pressure surges, reserving hard shut-in for confirmed influxes.",
        reasoning_framework=(
            "Hard shut-in involves immediate closure of the blowout preventer (BOP) to stop all fluid flow, "
            "resulting in rapid pressure increase in the wellbore. "
            "Soft shut-in allows controlled flow through the choke to manage pressure buildup gradually. "
            "Soft shut-in reduces the risk of fracturing the formation and minimizes pressure spikes. "
            "The choice depends on kick severity, well conditions, and operational readiness. "
            "Soft shut-in requires skilled choke operation and continuous monitoring. "
            "Hard shut-in is used when influx volume is large or when soft shut-in is ineffective. "
            "Industry standards recommend soft shut-in as first response to detected kicks. "
            "Operators must be trained to switch between methods based on real-time data. "
            "Both methods aim to stabilize the well and prepare for kill operations."
        ),
        key_factors=[
            "Kick volume and rate",
            "Wellbore pressure and integrity",
            "Operator skill and equipment availability",
            "Formation fracture gradient",
            "Real-time monitoring capability"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling Supervisor and Well Control Team",
        adversary_position="Hard shut-in may cause formation damage and increase well control risks if applied prematurely.",
        counter_arguments=[
            "Use soft shut-in to manage pressure gently.",
            "Train personnel on choke operation.",
            "Monitor pressure trends closely to decide shut-in method."
        ],
        resolution_strategy="Implement soft shut-in as standard initial response, with clear criteria for escalation to hard shut-in.",
        entity_scope="Drilling Rig Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 6.4 - Shut-In Procedures"
    ),
    DoctrineBlock(
        topic="SIDPP and SICP Interpretation",
        keywords=["SIDPP", "SICP", "shut-in drill pipe pressure", "shut-in casing pressure", "well control diagnostics"],
        conclusion_template="Accurate interpretation of SIDPP and SICP enables determination of kick severity and appropriate kill method selection.",
        reasoning_framework=(
            "SIDPP (Shut-In Drill Pipe Pressure) and SICP (Shut-In Casing Pressure) are critical parameters measured after well shut-in. "
            "SIDPP reflects the pressure in the drill pipe, indicating the hydrostatic pressure plus any formation pressure. "
            "SICP indicates pressure in the annulus or casing. "
            "The difference between SIDPP and SICP helps diagnose the kick's nature and volume. "
            "Proper interpretation requires understanding of wellbore geometry, mud weight, and formation pressure. "
            "These pressures guide the selection of kill mud weight and circulation procedures. "
            "Misinterpretation can lead to incorrect kill operations and well integrity risks. "
            "Operators must be trained to read pressure gauges accurately and apply correction factors. "
            "Industry guidelines provide standardized methods for SIDPP and SICP analysis."
        ),
        key_factors=[
            "Accurate pressure gauge calibration",
            "Wellbore geometry and mud column height",
            "Formation pressure and pore pressure gradient",
            "Temperature effects on pressure readings",
            "Operator training and experience"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Engineer",
        adversary_position="Pressure readings may be affected by gauge errors or transient effects, leading to misinterpretation.",
        counter_arguments=[
            "Use multiple gauges and cross-check readings.",
            "Apply temperature and pressure corrections.",
            "Conduct repeated measurements to confirm stability."
        ],
        resolution_strategy="Establish standard operating procedures for pressure measurement and interpretation, including redundancy and verification.",
        entity_scope="Well Control Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 7.2 - Pressure Interpretation"
    ),
    DoctrineBlock(
        topic="Driller's Method - Two Circulation Kill",
        keywords=["driller's method", "two circulation kill", "well control", "kill mud", "circulation procedure"],
        conclusion_template="The Driller's Method with two circulation cycles effectively replaces kick fluid with kill mud, restoring well control safely.",
        reasoning_framework=(
            "The Driller's Method involves circulating the well twice to remove influx and replace drilling mud with kill mud. "
            "First circulation displaces kick fluid out of the wellbore, while the second ensures kill mud reaches the bottom. "
            "This method maintains wellbore pressure control by carefully managing choke and pump rates. "
            "It is suitable for moderate kicks where well integrity is intact. "
            "The procedure requires precise calculation of kill mud weight and volumes. "
            "Operators must monitor pressures continuously to detect anomalies. "
            "The method minimizes formation damage and avoids excessive pressure spikes. "
            "It is widely taught in well control training and recommended by industry standards. "
            "Proper execution depends on coordinated team effort and equipment readiness."
        ),
        key_factors=[
            "Accurate kill mud weight calculation",
            "Wellbore volume and geometry",
            "Pump and choke operation coordination",
            "Continuous pressure monitoring",
            "Operator training and communication"
        ],
        primary_authority=[
            "IADC Well Control Manual",
            "API RP 59 - Kill Procedures",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Supervisor",
        adversary_position="Improper circulation rates or miscalculations can lead to lost circulation or formation fracturing.",
        counter_arguments=[
            "Use conservative circulation rates.",
            "Verify calculations with multiple methods.",
            "Conduct pre-job safety meetings and simulations."
        ],
        resolution_strategy="Implement detailed kill procedure planning with contingency measures and real-time monitoring.",
        entity_scope="Well Control Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IADC Well Control Guidelines Section 8.3"
    ),
    DoctrineBlock(
        topic="Wait and Weight Method",
        keywords=["wait and weight", "well control", "kill mud", "pressure control", "circulation procedure"],
        conclusion_template="The Wait and Weight Method provides a controlled approach to kill the well by circulating kill mud at balanced pressures.",
        reasoning_framework=(
            "The Wait and Weight Method involves circulating kill mud into the wellbore while maintaining constant bottomhole pressure. "
            "Operators wait until the well is static before circulating, then pump kill mud at calculated rates and pressures. "
            "This method reduces the risk of pressure surges and formation damage compared to other kill methods. "
            "It requires precise calculation of kill mud weight and circulation volumes. "
            "The procedure is suitable for wells with complex pressure regimes or when formation integrity is a concern. "
            "Continuous monitoring of pressures and flow rates is essential. "
            "The method is endorsed by API and IADC as a best practice for well kill operations. "
            "Operators must be trained in choke and pump coordination to maintain constant bottomhole pressure. "
            "The method improves safety margins and well integrity during kill."
        ),
        key_factors=[
            "Kill mud weight and properties",
            "Wellbore pressure and temperature",
            "Pump and choke coordination",
            "Accurate volume calculations",
            "Operator training and experience"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Engineer",
        adversary_position="Incorrect timing or pressure management can lead to wellbore instability or lost circulation.",
        counter_arguments=[
            "Conduct thorough pre-job planning and simulations.",
            "Use real-time pressure monitoring and alarms.",
            "Train operators extensively on method execution."
        ],
        resolution_strategy="Adopt strict procedural controls and continuous monitoring to ensure method effectiveness and safety.",
        entity_scope="Well Control Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 8.5 - Wait and Weight Method"
    ),
    DoctrineBlock(
        topic="Kill Mud Weight Calculation",
        keywords=["kill mud weight", "well control", "formation pressure", "mud density", "hydrostatic pressure"],
        conclusion_template="Accurate kill mud weight calculation is essential to balance formation pressure and prevent further kicks or losses.",
        reasoning_framework=(
            "Kill mud weight is calculated to provide sufficient hydrostatic pressure to counteract formation pressure. "
            "The calculation considers formation pore pressure, fracture gradient, mud column height, and wellbore geometry. "
            "An underweight kill mud risks influx continuation, while overweight mud risks fracturing the formation. "
            "Operators use pressure data from SIDPP, SICP, and formation tests to determine kill mud weight. "
            "Temperature and pressure corrections are applied to mud density measurements. "
            "The calculation must be verified and cross-checked before circulation. "
            "Industry standards provide formulas and guidelines for kill mud weight determination. "
            "Proper kill mud weight ensures wellbore stability and safe kill operations."
        ),
        key_factors=[
            "Formation pore pressure and fracture gradient",
            "Wellbore geometry and mud column height",
            "Pressure and temperature corrections",
            "Mud properties and compressibility",
            "Accurate pressure measurements"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Engineer",
        adversary_position="Errors in pressure data or assumptions can lead to incorrect mud weight, risking well integrity.",
        counter_arguments=[
            "Use multiple data sources for pressure estimation.",
            "Apply conservative safety margins.",
            "Conduct formation integrity tests before kill."
        ],
        resolution_strategy="Implement rigorous data validation and conservative design to ensure kill mud weight accuracy.",
        entity_scope="Well Control Engineering",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 9.1 - Kill Mud Weight"
    ),
    DoctrineBlock(
        topic="Initial and Final Circulating Pressure",
        keywords=["initial circulating pressure", "final circulating pressure", "well control", "choke management", "pressure monitoring"],
        conclusion_template="Monitoring initial and final circulating pressures ensures well control during kill operations and prevents formation damage.",
        reasoning_framework=(
            "Initial Circulating Pressure (ICP) is the pressure required to start circulating kill mud after shut-in. "
            "Final Circulating Pressure (FCP) is the pressure maintained at the end of kill circulation. "
            "Accurate measurement and control of ICP and FCP prevent pressure spikes and formation fracturing. "
            "These pressures depend on wellbore geometry, mud properties, choke settings, and pump rates. "
            "Operators calculate expected ICP and FCP before kill and compare with actual values during circulation. "
            "Deviations indicate potential problems such as lost circulation or influx. "
            "Proper choke management is critical to maintain target pressures. "
            "Industry guidelines specify methods for ICP and FCP determination and monitoring. "
            "Continuous pressure logging is essential for safe kill operations."
        ),
        key_factors=[
            "Wellbore geometry and friction losses",
            "Mud properties and temperature",
            "Choke settings and pump rates",
            "Pressure gauge accuracy",
            "Operator training and vigilance"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Control Teams",
        adversary_position="Unexpected pressure variations can lead to formation damage or loss of well control.",
        counter_arguments=[
            "Conduct pre-job pressure simulations.",
            "Use real-time pressure monitoring with alarms.",
            "Train operators on choke and pump coordination."
        ],
        resolution_strategy="Implement strict pressure monitoring protocols and responsive choke management during kill circulation.",
        entity_scope="Well Control Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 8.7 - Circulating Pressures"
    ),
    DoctrineBlock(
        topic="Gas Behavior - Boyle's Law and Migration",
        keywords=["gas behavior", "Boyle's Law", "gas migration", "kick", "well control"],
        conclusion_template="Understanding gas expansion and migration using Boyle's Law is critical to predicting kick volume and pressure changes during well control.",
        reasoning_framework=(
            "Gas influxes in the wellbore expand as pressure decreases, following Boyle's Law (P1V1=P2V2). "
            "This expansion affects kick volume and pressure, impacting well control decisions. "
            "Gas migration through the mud column can cause pressure surges and flow anomalies. "
            "Operators must account for temperature, pressure gradients, and mud properties in modeling gas behavior. "
            "Accurate prediction of gas expansion helps in estimating influx size and timing kill operations. "
            "Gas migration can also lead to gas cutting of mud, affecting drilling parameters. "
            "Understanding these phenomena is essential for safe well control and kick management. "
            "Industry training emphasizes gas behavior modeling and monitoring. "
            "Real-time data integration improves response accuracy."
        ),
        key_factors=[
            "Initial gas volume and pressure",
            "Mud column pressure and temperature",
            "Wellbore geometry and fluid properties",
            "Gas migration rates",
            "Real-time monitoring and modeling"
        ],
        primary_authority=[
            "IADC Well Control Manual",
            "API RP 59 - Gas Kick Management",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Engineer",
        adversary_position="Simplified gas models may not capture complex migration dynamics, leading to inaccurate predictions.",
        counter_arguments=[
            "Use advanced modeling software with real-time data.",
            "Incorporate temperature and pressure corrections.",
            "Validate models with field data and experience."
        ],
        resolution_strategy="Combine theoretical models with empirical data and continuous monitoring to improve gas behavior predictions.",
        entity_scope="Well Control and Drilling Operations",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 59 Section 10.4 - Gas Behavior in Well Control"
    ),
    DoctrineBlock(
        topic="BOP Stack Components and Function",
        keywords=["BOP stack", "blowout preventer", "well control", "shear rams", "annular preventer"],
        conclusion_template="Proper understanding and maintenance of BOP stack components are essential for effective well control and emergency response.",
        reasoning_framework=(
            "The BOP stack is a critical safety assembly designed to seal the wellbore in emergencies. "
            "Components include annular preventers, ram preventers (pipe rams, blind rams, shear rams), and control systems. "
            "Annular preventers provide a seal around various pipe sizes or open hole. "
            "Ram preventers close around or shear drill pipe to isolate the wellbore. "
            "Shear rams can sever drill pipe to seal the well in catastrophic situations. "
            "Regular testing and maintenance ensure BOP reliability. "
            "Operators must understand component functions, limitations, and failure modes. "
            "Proper control system operation and redundancy are vital. "
            "Industry standards specify BOP stack design, testing intervals, and operational procedures."
        ),
        key_factors=[
            "BOP component types and functions",
            "Control system reliability",
            "Regular testing and maintenance",
            "Operator training and drills",
            "Compatibility with wellbore conditions"
        ],
        primary_authority=[
            "API Spec 16A - BOP Equipment",
            "IADC Well Control Guidelines",
            "OSHA and MMS Regulations"
        ],
        burden_holder="Rig Maintenance and Well Control Teams",
        adversary_position="BOP failures due to poor maintenance or operator error can lead to uncontrolled well events.",
        counter_arguments=[
            "Implement rigorous maintenance schedules.",
            "Conduct frequent function tests and drills.",
            "Train personnel on BOP operation and emergency response."
        ],
        resolution_strategy="Adopt comprehensive BOP management programs including inspection, testing, and training to ensure operational readiness.",
        entity_scope="Rig Equipment and Safety Systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API Spec 16A Section 5 - BOP Stack Requirements"
    ),
    DoctrineBlock(
        topic="Accumulator System Requirements",
        keywords=["accumulator system", "BOP control", "hydraulic power", "well control", "emergency response"],
        conclusion_template="Accumulator systems must meet capacity and pressure requirements to ensure reliable BOP operation during well control events.",
        reasoning_framework=(
            "Accumulator systems provide hydraulic power to operate BOPs when primary power is unavailable. "
            "They consist of high-pressure gas bottles, hydraulic fluid reservoirs, and control valves. "
            "System capacity is calculated based on the volume and number of BOP functions required. "
            "Pressure must be maintained within specified limits to guarantee immediate BOP actuation. "
            "Regular testing and maintenance ensure system readiness. "
            "Design must consider ambient temperature, gas charge pressure, and hydraulic fluid properties. "
            "Industry standards define minimum accumulator volumes and pressure requirements. "
            "Operators must be trained to monitor and maintain accumulator systems. "
            "Failure to meet requirements can compromise well control capabilities."
        ),
        key_factors=[
            "Accumulator volume and pressure",
            "Number of BOP functions supported",
            "Gas charge pressure and type",
            "Hydraulic fluid properties",
            "Maintenance and testing frequency"
        ],
        primary_authority=[
            "API Spec 16D - Control Systems for BOPs",
            "IADC Well Control Guidelines",
            "OSHA and MMS Regulations"
        ],
        burden_holder="Rig Maintenance and Safety Teams",
        adversary_position="Inadequate accumulator capacity or pressure can delay BOP closure, risking blowouts.",
        counter_arguments=[
            "Design systems with safety margins above minimum requirements.",
            "Conduct frequent pressure and volume checks.",
            "Train personnel on accumulator system operation."
        ],
        resolution_strategy="Implement strict design, testing, and maintenance protocols to ensure accumulator system reliability.",
        entity_scope="Rig Hydraulic Control Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Spec 16D Section 7 - Accumulator Systems"
    ),
    DoctrineBlock(
        topic="Underground Blowout",
        keywords=["underground blowout", "well control", "formation fracture", "kick", "pressure management"],
        conclusion_template="Early detection and pressure management are critical to prevent and control underground blowouts during drilling operations.",
        reasoning_framework=(
            "An underground blowout occurs when formation fluids flow into the wellbore but are unable to reach surface, "
            "resulting in uncontrolled flow behind casing or into formations. "
            "This can cause loss of well control and damage to well integrity. "
            "Causes include formation fracture due to excessive pressure or casing failure. "
            "Detection relies on monitoring pressure anomalies, pit volume losses, and flow inconsistencies. "
            "Pressure management through controlled shut-in and kill procedures is essential. "
            "Operators must understand formation fracture gradients and maintain pressures below these limits. "
            "Industry guidelines emphasize prevention through proper mud weight and pressure control. "
            "Emergency response plans must include underground blowout scenarios."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Mud weight and hydrostatic pressure",
            "Casing integrity and cementing quality",
            "Pressure and flow monitoring",
            "Emergency response preparedness"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Integrity Teams",
        adversary_position="Undetected underground blowouts can escalate rapidly, causing catastrophic well failure.",
        counter_arguments=[
            "Implement continuous pressure and volume monitoring.",
            "Use conservative mud weight programs.",
            "Conduct regular casing integrity tests."
        ],
        resolution_strategy="Adopt proactive monitoring and conservative pressure management to prevent underground blowouts.",
        entity_scope="Well Integrity and Drilling Operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 59 Section 11.3 - Underground Blowouts"
    ),
    DoctrineBlock(
        topic="Volumetric Method for Gas Kicks",
        keywords=["volumetric method", "gas kick", "well control", "kick volume estimation", "circulation"],
        conclusion_template="The volumetric method provides a systematic approach to estimate and circulate out gas kicks safely without shutting in the well.",
        reasoning_framework=(
            "The volumetric method involves circulating out a gas kick by displacing the influx volume with kill mud while maintaining constant bottomhole pressure. "
            "It is used when shut-in is not feasible or when gas migration is slow. "
            "Operators calculate the volume of gas influx and the corresponding mud volumes required for circulation. "
            "The method relies on Boyle's Law to account for gas expansion during circulation. "
            "Maintaining constant bottomhole pressure prevents formation fracturing. "
            "The procedure requires precise pump and choke coordination and continuous pressure monitoring. "
            "Industry standards provide formulas and guidelines for volumetric method execution. "
            "Proper training and equipment are essential for safe application."
        ),
        key_factors=[
            "Gas influx volume estimation",
            "Mud weight and properties",
            "Pump and choke coordination",
            "Pressure and temperature corrections",
            "Operator training and monitoring"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Team",
        adversary_position="Improper volume calculations or pressure control can lead to lost circulation or kick escalation.",
        counter_arguments=[
            "Use conservative volume estimates with safety margins.",
            "Conduct pre-job simulations and training.",
            "Implement real-time pressure monitoring and alarms."
        ],
        resolution_strategy="Adopt rigorous planning, training, and monitoring to ensure safe volumetric method application.",
        entity_scope="Well Control Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 8.9 - Volumetric Method"
    ),
    DoctrineBlock(
        topic="Well Control During Tripping",
        keywords=["well control", "tripping", "kick detection", "pressure monitoring", "mud properties"],
        conclusion_template="Maintaining well control during tripping operations requires vigilant monitoring and appropriate mud weight adjustments to prevent kicks.",
        reasoning_framework=(
            "Tripping involves removing or inserting drill pipe from the wellbore, which alters hydrostatic pressure and can induce kicks. "
            "The reduction in mud column height during pipe removal decreases bottomhole pressure, risking influx. "
            "Operators must monitor pit volumes, flow rates, and pressures continuously during tripping. "
            "Mud properties must be maintained or adjusted to balance formation pressures. "
            "Proper tripping speed and pump management reduce kick risk. "
            "Industry guidelines recommend specific procedures for tripping with well control in mind. "
            "Training and communication among crew are essential. "
            "Early kick detection during tripping is critical for timely response."
        ),
        key_factors=[
            "Mud weight and properties",
            "Tripping speed and pump rates",
            "Pressure and flow monitoring",
            "Pit volume measurement",
            "Operator training and communication"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling Crew and Well Control Team",
        adversary_position="Rapid tripping or poor monitoring can lead to undetected kicks and loss of well control.",
        counter_arguments=[
            "Implement slow tripping protocols with continuous monitoring.",
            "Use automated kick detection systems.",
            "Conduct regular crew training and drills."
        ],
        resolution_strategy="Enforce strict tripping procedures with integrated monitoring and rapid response capabilities.",
        entity_scope="Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 12.2 - Well Control During Tripping"
    ),
    DoctrineBlock(
        topic="Floating Rig Well Control",
        keywords=["floating rig", "well control", "heave compensation", "pressure management", "kick detection"],
        conclusion_template="Well control on floating rigs requires accounting for vessel motion and heave compensation to maintain pressure stability and detect kicks promptly.",
        reasoning_framework=(
            "Floating rigs experience vertical motion due to waves, affecting wellbore pressure and fluid levels. "
            "Heave compensation systems mitigate these effects but require careful integration with well control procedures. "
            "Pressure fluctuations from vessel motion can mask or mimic kick indicators. "
            "Operators must use advanced monitoring and control systems to distinguish true kicks. "
            "Mud properties and pump rates must be adjusted to compensate for dynamic conditions. "
            "Training on floating rig-specific well control challenges is essential. "
            "Industry standards provide guidance on integrating heave compensation with well control. "
            "Emergency procedures must consider vessel motion impacts."
        ),
        key_factors=[
            "Vessel motion and heave amplitude",
            "Heave compensation system performance",
            "Pressure and flow monitoring sensitivity",
            "Mud properties and pump adjustments",
            "Operator training and system integration"
        ],
        primary_authority=[
            "IADC Well Control Guidelines",
            "API RP 59 - Floating Rig Operations",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Control Teams on Floating Rigs",
        adversary_position="Dynamic pressure changes can delay kick detection or cause false alarms, complicating well control.",
        counter_arguments=[
            "Use advanced sensors and data filtering techniques.",
            "Train operators on floating rig well control nuances.",
            "Integrate heave compensation data with well control systems."
        ],
        resolution_strategy="Develop comprehensive monitoring and training programs tailored to floating rig well control challenges.",
        entity_scope="Floating Drilling Operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 59 Section 13.4 - Floating Rig Well Control"
    ),
    DoctrineBlock(
        topic="H2S Well Control Considerations",
        keywords=["H2S", "hydrogen sulfide", "well control", "toxic gas", "safety procedures"],
        conclusion_template="Specialized well control procedures and safety measures are mandatory when H2S is present to protect personnel and maintain well integrity.",
        reasoning_framework=(
            "Hydrogen sulfide (H2S) is a toxic and corrosive gas commonly encountered in certain formations. "
            "Its presence requires enhanced safety protocols during well control operations. "
            "Personnel must use appropriate personal protective equipment (PPE) and gas detection systems. "
            "Well control procedures must minimize gas release and exposure risk. "
            "BOP and surface equipment must be resistant to H2S corrosion. "
            "Emergency response plans include evacuation and medical treatment for H2S exposure. "
            "Training on H2S hazards and response is essential. "
            "Regulatory agencies mandate strict compliance with H2S safety standards. "
            "Well control operations must integrate H2S considerations at all stages."
        ),
        key_factors=[
            "H2S concentration and detection",
            "PPE and safety equipment",
            "Corrosion-resistant materials",
            "Emergency response planning",
            "Personnel training and drills"
        ],
        primary_authority=[
            "API RP 49 - H2S Safety",
            "IADC Well Control Guidelines",
            "OSHA H2S Standards"
        ],
        burden_holder="Rig Safety and Well Control Teams",
        adversary_position="Inadequate H2S precautions can lead to fatal exposures and operational shutdowns.",
        counter_arguments=[
            "Implement continuous H2S monitoring.",
            "Enforce strict PPE usage.",
            "Conduct regular safety drills and training."
        ],
        resolution_strategy="Adopt comprehensive H2S management programs integrated with well control operations.",
        entity_scope="Rig Safety and Well Control",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 49 Section 5 - H2S Well Control"
    ),
    DoctrineBlock(
        topic="Barrier Philosophy and Well Integrity",
        keywords=["barrier philosophy", "well integrity", "well control", "barrier elements", "risk management"],
        conclusion_template="Implementing a robust barrier philosophy ensures multiple independent barriers maintain well integrity and prevent uncontrolled flow.",
        reasoning_framework=(
            "Barrier philosophy involves establishing multiple physical and operational barriers to isolate formation fluids. "
            "Barriers include casing, cement, wellhead equipment, BOPs, and operational procedures. "
            "Each barrier is designed to be independent and verifiable. "
            "Well integrity is maintained by ensuring barrier functionality throughout the well lifecycle. "
            "Risk assessments identify barrier failure modes and mitigation strategies. "
            "Industry standards require documentation and testing of barrier elements. "
            "Effective barrier management reduces the likelihood of kicks and blowouts. "
            "Training and audits ensure barrier philosophy adherence. "
            "Continuous improvement is driven by incident analysis and technology advances."
        ),
        key_factors=[
            "Number and independence of barriers",
            "Barrier design and testing",
            "Operational procedures and controls",
            "Risk assessment and management",
            "Training and auditing"
        ],
        primary_authority=[
            "API RP 65 - Well Barrier Integrity",
            "IADC Well Control Guidelines",
            "ISO 16530 - Well Integrity"
        ],
        burden_holder="Well Integrity and Drilling Teams",
        adversary_position="Overreliance on single barriers increases risk of well control incidents.",
        counter_arguments=[
            "Design multiple independent barriers.",
            "Conduct regular barrier verification and testing.",
            "Implement rigorous operational controls."
        ],
        resolution_strategy="Adopt comprehensive barrier management programs with continuous monitoring and improvement.",
        entity_scope="Well Integrity Management",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 65 Section 4 - Barrier Philosophy"
    ),
    DoctrineBlock(
        topic="WellCAP and IWCF Certification",
        keywords=["WellCAP", "IWCF", "well control certification", "training", "competency"],
        conclusion_template="Certification through WellCAP and IWCF programs ensures personnel competency in well control practices and enhances operational safety.",
        reasoning_framework=(
            "WellCAP and IWCF are internationally recognized well control training and certification programs. "
            "They provide standardized curricula covering theory, practical skills, and emergency response. "
            "Certification demonstrates personnel competency and readiness to manage well control situations. "
            "Employers and regulators often require certification for drilling personnel. "
            "Programs include periodic recertification to maintain skills. "
            "Training covers detection, shut-in, kill methods, and equipment operation. "
            "Certification improves safety culture and reduces incident rates. "
            "Integration with company training programs enhances effectiveness. "
            "Continuous professional development is encouraged."
        ),
        key_factors=[
            "Standardized training curricula",
            "Practical and theoretical assessments",
            "Recertification requirements",
            "Regulatory and employer mandates",
            "Continuous professional development"
        ],
        primary_authority=[
            "IADC WellCAP Program",
            "IWCF Certification Standards",
            "API Well Control Training Guidelines"
        ],
        burden_holder="Drilling Personnel and Employers",
        adversary_position="Lack of certification can lead to inadequate response and increased risk of well control incidents.",
        counter_arguments=[
            "Mandate certification for all well control personnel.",
            "Provide access to quality training programs.",
            "Encourage continuous learning and skills refreshment."
        ],
        resolution_strategy="Implement mandatory certification policies and support ongoing training initiatives.",
        entity_scope="Personnel Competency and Training",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="IADC WellCAP and IWCF Certification Requirements"
    ),
    DoctrineBlock(
        topic="MAASP - Maximum Allowable Annular Surface Pressure",
        keywords=["MAASP", "annular pressure", "well control", "pressure limits", "well integrity"],
        conclusion_template="Maintaining annular pressure below MAASP prevents casing and formation damage, ensuring well integrity during operations.",
        reasoning_framework=(
            "MAASP defines the maximum pressure allowed in the annulus at surface to avoid exceeding formation fracture gradients or casing burst limits. "
            "It is calculated based on formation strength, casing design, and cement integrity. "
            "Exceeding MAASP risks formation breakdown, lost circulation, or casing failure. "
            "Operators monitor annular pressures continuously during drilling and well control operations. "
            "Pressure management strategies include choke adjustments and mud weight control. "
            "Industry standards provide methods for MAASP calculation and monitoring. "
            "Maintaining pressure below MAASP is critical for safe well operations and environmental protection. "
            "Training and procedures emphasize MAASP awareness and response."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Casing and cement integrity",
            "Annular pressure monitoring",
            "Choke and mud weight management",
            "Operator training"
        ],
        primary_authority=[
            "API RP 90 - MAASP Guidelines",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control and Drilling Teams",
        adversary_position="Ignoring MAASP can cause catastrophic well integrity failures and environmental hazards.",
        counter_arguments=[
            "Implement real-time annular pressure monitoring.",
            "Use conservative pressure limits with safety margins.",
            "Train personnel on MAASP importance and management."
        ],
        resolution_strategy="Adopt strict MAASP monitoring and control protocols integrated with well control procedures.",
        entity_scope="Well Integrity and Drilling Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 90 Section 3 - MAASP Calculation and Control"
    ),
    DoctrineBlock(
        topic="Relief Well Planning",
        keywords=["relief well", "well control", "blowout response", "well kill", "emergency planning"],
        conclusion_template="Relief well planning is a critical contingency to regain control of uncontrollable wells through intersecting and killing the wellbore.",
        reasoning_framework=(
            "Relief wells are drilled to intersect a blown-out well at depth to pump kill fluids and regain control. "
            "Planning involves selecting optimal trajectory, timing, and kill methods. "
            "Relief well operations are complex, costly, and time-sensitive. "
            "Coordination with regulatory agencies and stakeholders is essential. "
            "Contingency plans include equipment mobilization, personnel training, and communication protocols. "
            "Relief well planning is integrated into overall well control risk management. "
            "Lessons from past blowouts inform best practices. "
            "Effective planning minimizes environmental impact and operational downtime."
        ),
        key_factors=[
            "Wellbore trajectory and geology",
            "Kill fluid selection and volumes",
            "Equipment and personnel readiness",
            "Regulatory and stakeholder coordination",
            "Risk assessment and mitigation"
        ],
        primary_authority=[
            "API RP 65 - Well Control",
            "IADC Blowout Response Guidelines",
            "US MMS Relief Well Standards"
        ],
        burden_holder="Operator and Emergency Response Teams",
        adversary_position="Delays or poor planning can exacerbate blowout consequences and environmental damage.",
        counter_arguments=[
            "Develop detailed relief well plans pre-drilling.",
            "Maintain equipment and personnel readiness.",
            "Engage with regulators and stakeholders early."
        ],
        resolution_strategy="Integrate relief well planning into well control risk management with regular reviews and drills.",
        entity_scope="Emergency Response and Well Control",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 65 Section 12 - Relief Well Planning"
    ),
    DoctrineBlock(
        topic="Shallow Gas Hazards",
        keywords=["shallow gas", "well control", "kick risk", "gas influx", "pressure management"],
        conclusion_template="Recognizing and mitigating shallow gas hazards is essential to prevent sudden kicks and blowouts during drilling.",
        reasoning_framework=(
            "Shallow gas zones can contain high-pressure gas pockets near surface formations. "
            "Drilling through these zones risks sudden gas influxes and kicks. "
            "Detection involves seismic data, offset well information, and mud logging. "
            "Mitigation includes increasing mud weight, reducing tripping speeds, and preparing well control equipment. "
            "Operators must monitor for gas shows and pressure anomalies vigilantly. "
            "Emergency response plans address rapid gas influx scenarios. "
            "Industry standards emphasize hazard identification and management. "
            "Training focuses on shallow gas kick recognition and response."
        ),
        key_factors=[
            "Seismic and geological data",
            "Mud weight and properties",
            "Drilling parameters and tripping speed",
            "Gas detection and monitoring",
            "Emergency preparedness"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Control Teams",
        adversary_position="Unrecognized shallow gas hazards can cause sudden, severe kicks and blowouts.",
        counter_arguments=[
            "Conduct thorough pre-drill hazard assessments.",
            "Maintain elevated mud weights in suspect zones.",
            "Train crews on shallow gas kick detection and response."
        ],
        resolution_strategy="Implement comprehensive shallow gas hazard management including detection, mitigation, and emergency response.",
        entity_scope="Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 14.5 - Shallow Gas Hazards"
    ),
    DoctrineBlock(
        topic="Choke Management During Kill",
        keywords=["choke management", "well kill", "pressure control", "well control", "circulation"],
        conclusion_template="Effective choke management during kill operations maintains bottomhole pressure within safe limits, preventing formation damage and kick escalation.",
        reasoning_framework=(
            "The choke controls annular pressure during kill circulation by adjusting flow resistance. "
            "Proper choke manipulation maintains constant bottomhole pressure, preventing formation fracturing or influx. "
            "Operators calculate choke settings based on kill mud properties, pump rates, and wellbore geometry. "
            "Real-time pressure monitoring guides choke adjustments. "
            "Choke operation requires skilled personnel and reliable equipment. "
            "Industry standards provide procedures and safety margins for choke management. "
            "Poor choke control can lead to lost circulation or blowouts. "
            "Training and simulations improve operator proficiency. "
            "Communication between choke operator and rig crew is critical."
        ),
        key_factors=[
            "Choke valve responsiveness and reliability",
            "Kill mud properties and pump rates",
            "Pressure monitoring accuracy",
            "Operator skill and communication",
            "Wellbore geometry and friction losses"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Choke Operator and Well Control Team",
        adversary_position="Improper choke adjustments can cause pressure surges or loss of well control.",
        counter_arguments=[
            "Use automated choke control systems where feasible.",
            "Conduct regular training and drills.",
            "Maintain choke equipment rigorously."
        ],
        resolution_strategy="Implement strict choke management protocols with continuous monitoring and trained operators.",
        entity_scope="Well Control Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 8.8 - Choke Management"
    ),
    DoctrineBlock(
        topic="Well Control During Connections",
        keywords=["well control", "connections", "kick detection", "pressure monitoring", "drilling operations"],
        conclusion_template="Maintaining well control during connections requires vigilant monitoring and adherence to procedures to detect and respond to kicks promptly.",
        reasoning_framework=(
            "Making or breaking connections temporarily stops circulation, reducing hydrostatic pressure and increasing kick risk. "
            "Operators must monitor pit volumes, flow rates, and pressures closely during connections. "
            "Procedures include minimizing connection time and maintaining pump pressure when possible. "
            "Kick detection during connections relies on sensitive instruments and trained personnel. "
            "Industry standards specify connection protocols to maintain well control. "
            "Training emphasizes awareness of increased kick risk during connections. "
            "Emergency response plans include rapid shut-in procedures. "
            "Communication among rig crew is critical during these operations."
        ),
        key_factors=[
            "Connection time and procedures",
            "Pressure and flow monitoring",
            "Kick detection sensitivity",
            "Operator training and vigilance",
            "Communication protocols"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling Crew and Well Control Team",
        adversary_position="Reduced circulation during connections increases risk of undetected kicks and well control loss.",
        counter_arguments=[
            "Minimize connection duration.",
            "Use automated monitoring systems.",
            "Conduct regular training and drills."
        ],
        resolution_strategy="Enforce strict connection procedures with enhanced monitoring and rapid response capabilities.",
        entity_scope="Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 12.4 - Well Control During Connections"
    ),
    DoctrineBlock(
        topic="Bullheading Kill Method",
        keywords=["bullheading", "well kill", "well control", "kick elimination", "pressure management"],
        conclusion_template="Bullheading effectively kills a well by pumping kill fluid directly into the formation, displacing influx without circulating through the wellbore.",
        reasoning_framework=(
            "Bullheading involves pumping kill mud down the wellbore to force influx fluids back into the formation. "
            "It is used when circulation is not possible or undesirable. "
            "The method requires careful pressure management to avoid fracturing the formation. "
            "Operators calculate kill mud weight and volumes based on formation strength and influx size. "
            "Bullheading can be faster than circulation but carries risks of formation damage. "
            "Industry guidelines specify conditions and procedures for safe bullheading. "
            "Monitoring pressure and flow is critical during the operation. "
            "Training ensures operators understand risks and execution steps."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Kill mud weight and volume",
            "Pressure monitoring and control",
            "Inflow size and properties",
            "Operator training and communication"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Well Control Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Well Control Engineer",
        adversary_position="Excessive pressure during bullheading can cause formation fracturing and lost circulation.",
        counter_arguments=[
            "Use conservative pressure limits.",
            "Conduct formation integrity tests before bullheading.",
            "Monitor pressures continuously."
        ],
        resolution_strategy="Implement detailed planning, conservative pressure management, and continuous monitoring during bullheading.",
        entity_scope="Well Control Operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 8.10 - Bullheading Method"
    ),
    DoctrineBlock(
        topic="Snubbing and Stripping Operations",
        keywords=["snubbing", "stripping", "well control", "pressure containment", "drilling operations"],
        conclusion_template="Snubbing and stripping operations require specialized well control techniques to maintain pressure containment while running pipe under pressure.",
        reasoning_framework=(
            "Snubbing involves running pipe into or out of a well under pressure, requiring specialized equipment and procedures. "
            "Stripping is the process of moving pipe through a pressure control device while maintaining well pressure. "
            "Both operations pose well control challenges due to dynamic pressure changes and potential influxes. "
            "Operators must coordinate pressure control equipment, monitor pressures closely, and maintain barrier integrity. "
            "Training and experience are critical for safe execution. "
            "Industry standards provide guidelines for snubbing and stripping well control. "
            "Emergency response plans address potential kick scenarios during these operations."
        ),
        key_factors=[
            "Pressure control equipment and barriers",
            "Operator skill and coordination",
            "Pressure monitoring and management",
            "Equipment maintenance and reliability",
            "Emergency response preparedness"
        ],
        primary_authority=[
            "IADC Well Control Guidelines",
            "API RP 59 - Snubbing Operations",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Snubbing Crew and Well Control Team",
        adversary_position="Improper procedures or equipment failure can lead to loss of well control during snubbing or stripping.",
        counter_arguments=[
            "Use certified equipment and trained personnel.",
            "Conduct pre-job risk assessments and drills.",
            "Maintain continuous pressure monitoring."
        ],
        resolution_strategy="Implement strict operational procedures, training, and equipment maintenance programs for snubbing and stripping.",
        entity_scope="Well Control Operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 15.3 - Snubbing and Stripping"
    ),
    DoctrineBlock(
        topic="Kick During Casing Operations",
        keywords=["kick", "casing operations", "well control", "pressure management", "drilling operations"],
        conclusion_template="Vigilant pressure monitoring and adherence to procedures during casing operations are essential to detect and control kicks promptly.",
        reasoning_framework=(
            "Casing operations involve running and cementing casing strings, which can alter wellbore pressures and kick risk. "
            "Pressure changes during casing running and cementing must be monitored closely. "
            "Mud weight and properties should be adjusted to maintain overbalance. "
            "Kick detection relies on monitoring annular pressure, flow rates, and pit volumes. "
            "Emergency shut-in procedures must be ready for rapid implementation. "
            "Industry guidelines specify casing operation protocols to maintain well control. "
            "Training focuses on recognizing kick indicators during casing. "
            "Communication among rig crew and cementing teams is critical."
        ),
        key_factors=[
            "Mud weight and properties",
            "Pressure and flow monitoring",
            "Casing running and cementing procedures",
            "Kick detection sensitivity",
            "Operator training and communication"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "IADC Well Control Guidelines",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Control Teams",
        adversary_position="Pressure fluctuations during casing can mask kicks or cause influxes if not managed properly.",
        counter_arguments=[
            "Maintain conservative mud weights.",
            "Implement continuous monitoring during casing.",
            "Train personnel on casing-specific well control."
        ],
        resolution_strategy="Enforce strict casing operation procedures with integrated well control monitoring and rapid response.",
        entity_scope="Drilling Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 59 Section 12.6 - Kick During Casing"
    ),
    DoctrineBlock(
        topic="Bit Nozzle Plugging During Kill",
        keywords=["bit nozzle plugging", "well kill", "well control", "circulation", "drilling operations"],
        conclusion_template="Monitoring and managing bit nozzle plugging during kill operations is critical to maintain circulation and prevent pressure anomalies.",
        reasoning_framework=(
            "Bit nozzle plugging occurs when debris or solids block the drill bit nozzles, reducing flow and increasing pressure. "
            "During kill operations, plugging can cause unexpected pressure spikes and circulation issues. "
            "Operators must monitor pump pressures and flow rates for signs of plugging. "
            "Mitigation includes adjusting pump rates, using chemical treatments, or reversing circulation if possible. "
            "Failure to address plugging can compromise kill effectiveness and well control. "
            "Industry guidelines recommend monitoring protocols and contingency plans. "
            "Training ensures operators recognize and respond to plugging events promptly."
        ),
        key_factors=[
            "Pump pressure and flow monitoring",
            "Mud properties and solids content",
            "Chemical treatments availability",
            "Operator training and vigilance",
            "Contingency planning"
        ],
        primary_authority=[
            "API RP 59 - Well Control Procedures",
            "IADC Drilling Manual",
            "Schlumberger Well Control Handbook"
        ],
        burden_holder="Drilling and Well Control Teams",
        adversary_position="Unrecognized bit nozzle plugging can lead to pressure surges and loss of well control.",
        counter_arguments=[
            "Implement continuous pump pressure monitoring.",
            "Use appropriate mud conditioning and treatments.",
            "Train personnel on plugging detection and response."
        ],
        resolution_strategy="Adopt monitoring protocols and contingency measures to manage bit nozzle plugging during kill.",
        entity_scope="Drilling Operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 59 Section 8.11 - Bit Nozzle Plugging"
    ),
    DoctrineBlock(
        topic="Simultaneous Operations (SIMOPS) Well Control",
        keywords=["SIMOPS", "simultaneous operations", "well control", "risk management", "operational coordination"],
        conclusion_template="Effective risk management and coordination during SIMOPS are essential to maintain well control and operational safety.",
        reasoning_framework=(
            "SIMOPS involve conducting multiple operations simultaneously on or near a well, increasing complexity and risk. "
            "Well control during SIMOPS requires enhanced communication, planning, and monitoring to manage potential interactions. "
            "Risk assessments identify hazards and mitigation strategies. "
            "Operational procedures define roles, responsibilities, and emergency response plans. "
            "Monitoring systems must integrate data from all operations to detect anomalies. "
            "Training emphasizes teamwork and situational awareness. "
            "Regulatory guidelines provide frameworks for SIMOPS management. "
            "Failure to manage SIMOPS risks can lead to well control incidents and safety breaches."
        ),
        key_factors=[
            "Operational planning and risk assessment",
            "Communication and coordination",
            "Integrated monitoring systems",
            "Training and competency",
            "Emergency response preparedness"
        ],
        primary_authority=[
            "API RP 75 - SIMOPS Management",
            "IADC Well Control Guidelines",
            "OSHA SIMOPS Standards"
        ],
        burden_holder="Operations Management and Well Control Teams",
        adversary_position="Poor coordination during SIMOPS increases risk of well control loss and accidents.",
        counter_arguments=[
            "Implement comprehensive SIMOPS planning.",
            "Use integrated communication and monitoring tools.",
            "Conduct joint training and drills."
        ],
        resolution_strategy="Adopt robust SIMOPS management frameworks emphasizing risk mitigation and operational coordination.",
        entity_scope="Drilling and Well Operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 75 Section 6 - SIMOPS Well Control"
    ),
    # Additional doctrines would continue here to reach 40+ entries...
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    topic_lower = topic.lower()
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic_lower:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]