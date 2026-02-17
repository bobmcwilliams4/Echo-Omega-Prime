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
        topic="Optimal Frac Fleet Configuration: Pump Count and Horsepower",
        keywords=["pump count", "horsepower", "fleet sizing", "frac fleet", "stage efficiency"],
        conclusion_template="The optimal frac fleet configuration requires balancing pump count and horsepower to maximize stage efficiency while minimizing NPT and operational costs.",
        reasoning_framework=(
            "Evaluate the number of pumps required based on target stage rate, expected pressure, and redundancy needs. "
            "Horsepower per pump should be matched to anticipated treating pressures, with a typical range of 2,000–2,500 HP per pump. "
            "Fleet sizing must account for planned stages per day, expected downtime, and maintenance cycles. "
            "Redundancy is critical to mitigate unplanned failures; a minimum of 10% spare capacity is recommended. "
            "Operational data from prior jobs, pressure charts, and pump performance curves inform the configuration. "
            "Cost-benefit analysis should consider fuel consumption, crew size, and mobilization logistics. "
            "Environmental and regulatory constraints may impact allowable horsepower and fleet footprint."
        ),
        key_factors=[
            "Target stage rate (BPM)",
            "Treating pressure",
            "Pump reliability",
            "Maintenance schedule",
            "Fleet redundancy",
            "Operational cost",
            "Regulatory limits"
        ],
        primary_authority=[
            "Frac Fleet OEM Specifications",
            "API RP 100-1",
            "Field Operations Manual"
        ],
        burden_holder="Fleet Operations Manager",
        adversary_position="Over-sizing increases cost and environmental impact; under-sizing risks NPT and stage failures.",
        counter_arguments=[
            "Smaller fleets can be more agile and cost-effective.",
            "Over-reliance on redundancy increases idle asset costs.",
            "Higher horsepower pumps may not be needed for all formations."
        ],
        resolution_strategy="Apply historical job data and simulation models to optimize configuration for the specific well program.",
        entity_scope="Frac Fleet Operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 4.2"
    ),
    DoctrineBlock(
        topic="Frac Pump Types: Triplex vs Quintuplex Plunger",
        keywords=["triplex", "quintuplex", "plunger pump", "pump selection", "maintenance"],
        conclusion_template="Selection between triplex and quintuplex plunger pumps depends on desired flow rate, pressure, maintenance profile, and operational reliability.",
        reasoning_framework=(
            "Triplex pumps offer simplicity and lower initial cost, with three plungers providing robust performance for moderate rates and pressures. "
            "Quintuplex pumps, with five plungers, deliver smoother flow, higher rates, and reduced pulsation, which is critical for high-rate, high-pressure applications. "
            "Maintenance intervals for quintuplex pumps are typically longer, but parts are more expensive. "
            "Triplex pumps are easier to service in the field and have a smaller footprint. "
            "Fleet integration should consider compatibility with existing manifold and iron. "
            "Operational reliability is improved with quintuplex pumps in challenging formations."
        ),
        key_factors=[
            "Desired flow rate",
            "Treating pressure",
            "Pump maintenance profile",
            "Fleet integration",
            "Cost of ownership"
        ],
        primary_authority=[
            "Pump OEM Manuals",
            "API RP 100-1",
            "Field Maintenance Logs"
        ],
        burden_holder="Fleet Engineering Lead",
        adversary_position="Triplex pumps are sufficient for most jobs; quintuplex adds unnecessary complexity.",
        counter_arguments=[
            "Quintuplex pumps reduce NPT and improve stage consistency.",
            "Triplex pumps are more cost-effective for low-rate jobs."
        ],
        resolution_strategy="Match pump type to job requirements and maintenance capabilities; pilot quintuplex in high-rate wells.",
        entity_scope="Frac Fleet Engineering",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 5.1"
    ),
    DoctrineBlock(
        topic="Electric Frac Fleet (E-Frac) Direct Drive Turbine",
        keywords=["electric frac", "e-frac", "direct drive", "turbine", "emissions", "fuel efficiency"],
        conclusion_template="E-Frac fleets utilizing direct drive turbines offer significant emissions reduction and fuel efficiency, but require robust grid or field gas supply.",
        reasoning_framework=(
            "Direct drive turbines eliminate hydraulic transmission losses, improving overall efficiency. "
            "E-Frac reduces diesel consumption and emissions, aligning with ESG goals and regulatory requirements. "
            "Grid connection or field gas supply must be reliable and capable of meeting peak demand. "
            "Turbine maintenance is less frequent but requires specialized technicians. "
            "Initial capital expenditure is higher, but operational savings accrue over time. "
            "Integration with SCADA systems enables real-time monitoring and optimization."
        ),
        key_factors=[
            "Grid or field gas availability",
            "Emissions targets",
            "Capital expenditure",
            "Operational savings",
            "Maintenance requirements"
        ],
        primary_authority=[
            "OEM Turbine Manuals",
            "EPA Emissions Standards",
            "Field Case Studies"
        ],
        burden_holder="Fleet Sustainability Officer",
        adversary_position="E-Frac is cost-prohibitive and dependent on unreliable power sources.",
        counter_arguments=[
            "Long-term savings outweigh initial costs.",
            "Field gas supply can be stabilized with proper infrastructure."
        ],
        resolution_strategy="Conduct feasibility analysis and pilot E-Frac on select pads; monitor performance and emissions.",
        entity_scope="Frac Fleet Sustainability",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Tier 4 Standards"
    ),
    DoctrineBlock(
        topic="Diesel Frac Fleet: Conventional and Tier 4 DGB",
        keywords=["diesel frac", "tier 4", "DGB", "dual-fuel", "emissions", "fleet compliance"],
        conclusion_template="Tier 4 DGB diesel frac fleets achieve lower emissions and fuel costs, but require careful management of substitution ratios and fuel logistics.",
        reasoning_framework=(
            "Tier 4 engines meet stringent EPA emissions standards, reducing NOx and particulate output. "
            "Dual-fuel (DGB) systems allow substitution of field gas or CNG for diesel, lowering fuel costs and emissions. "
            "Substitution ratio depends on engine load, gas quality, and operational parameters. "
            "Fleet compliance requires regular emissions testing and reporting. "
            "Fuel logistics must ensure consistent supply of both diesel and gas. "
            "Maintenance intervals may be extended with cleaner-burning fuels."
        ),
        key_factors=[
            "Emissions compliance",
            "Fuel substitution ratio",
            "Fuel logistics",
            "Operational cost",
            "Engine maintenance"
        ],
        primary_authority=[
            "EPA Tier 4 Regulations",
            "OEM Engine Manuals",
            "Field Emissions Reports"
        ],
        burden_holder="Fleet Compliance Manager",
        adversary_position="Tier 4 DGB increases complexity and upfront cost; conventional diesel is more reliable.",
        counter_arguments=[
            "Regulatory penalties for non-compliance outweigh cost savings.",
            "Dual-fuel systems improve operational flexibility."
        ],
        resolution_strategy="Phase in Tier 4 DGB engines and monitor substitution ratios; optimize logistics for dual-fuel supply.",
        entity_scope="Frac Fleet Compliance",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Tier 4 Final Rule"
    ),
    DoctrineBlock(
        topic="Pump Rate Capacity: 100 BPM per Pump",
        keywords=["pump rate", "BPM", "capacity", "fleet sizing", "stage design"],
        conclusion_template="Each frac pump is rated for 100 BPM, but actual capacity depends on treating pressure, fluid properties, and maintenance condition.",
        reasoning_framework=(
            "OEM specifications rate pumps at 100 BPM under optimal conditions. "
            "Treating pressure and fluid viscosity can reduce effective rate. "
            "Pump wear and maintenance status impact achievable BPM. "
            "Fleet sizing must account for actual, not theoretical, pump capacity. "
            "Stage design should match pump rate to proppant and fluid requirements. "
            "Redundancy ensures target rates are met despite individual pump limitations."
        ),
        key_factors=[
            "OEM pump rating",
            "Treating pressure",
            "Fluid viscosity",
            "Pump maintenance",
            "Stage design"
        ],
        primary_authority=[
            "OEM Pump Specifications",
            "API RP 100-1",
            "Field Performance Data"
        ],
        burden_holder="Fleet Operations Supervisor",
        adversary_position="Actual pump rates are often lower than rated; over-reliance on ratings risks stage failures.",
        counter_arguments=[
            "Redundant pumps can compensate for lower rates.",
            "Maintenance programs improve rate reliability."
        ],
        resolution_strategy="Validate pump rates with field data; adjust fleet sizing accordingly.",
        entity_scope="Frac Fleet Operations",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 4.4"
    ),
    DoctrineBlock(
        topic="Treating Iron: High-Pressure Manifold and Missile",
        keywords=["treating iron", "manifold", "missile", "high-pressure", "safety", "maintenance"],
        conclusion_template="High-pressure manifold and missile systems must be rated for maximum anticipated treating pressure and regularly inspected for integrity.",
        reasoning_framework=(
            "Treating iron must meet or exceed maximum expected pressure during stimulation. "
            "Manifold and missile design should minimize flow restrictions and facilitate safe operation. "
            "Regular inspection and pressure testing are required to prevent failures. "
            "Maintenance logs should track replacement intervals and pressure cycles. "
            "Safety protocols mandate use of certified iron and proper rig-up procedures."
        ),
        key_factors=[
            "Maximum treating pressure",
            "Iron certification",
            "Inspection frequency",
            "Maintenance records",
            "Safety protocols"
        ],
        primary_authority=[
            "API Spec 6A",
            "OEM Iron Certifications",
            "Field Safety Manual"
        ],
        burden_holder="Frac Safety Officer",
        adversary_position="Frequent iron replacement increases cost; less frequent inspection is sufficient.",
        counter_arguments=[
            "Iron failures risk catastrophic safety incidents.",
            "Regulatory requirements mandate strict inspection schedules."
        ],
        resolution_strategy="Adhere to API and OEM standards; maintain rigorous inspection and replacement schedule.",
        entity_scope="Frac Fleet Safety",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 6A Section 3"
    ),
    DoctrineBlock(
        topic="Blender Tub: Proppant Addition Rate and Mixing",
        keywords=["blender tub", "proppant addition", "mixing", "stage design", "quality control"],
        conclusion_template="Blender tub proppant addition rate and mixing quality are critical to stage success and must be matched to pump rate and fluid properties.",
        reasoning_framework=(
            "Proppant addition rate must be synchronized with pump rate to ensure consistent slurry concentration. "
            "Mixing quality impacts proppant distribution and stage performance. "
            "Blender tub design and agitation system must accommodate target rates and fluid viscosities. "
            "Quality control protocols require real-time monitoring of proppant concentration and mixing efficiency. "
            "Maintenance of blender tub and agitation system is essential for reliable operation."
        ),
        key_factors=[
            "Pump rate",
            "Proppant addition rate",
            "Mixing quality",
            "Fluid viscosity",
            "Blender tub maintenance"
        ],
        primary_authority=[
            "OEM Blender Specifications",
            "API RP 100-1",
            "Stage Quality Reports"
        ],
        burden_holder="Frac Quality Control Lead",
        adversary_position="Higher proppant rates risk poor mixing and stage failures.",
        counter_arguments=[
            "Advanced agitation systems improve mixing at higher rates.",
            "Real-time monitoring enables rapid adjustments."
        ],
        resolution_strategy="Implement real-time monitoring and adjust proppant addition rate to match pump and fluid properties.",
        entity_scope="Frac Quality Control",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 6.2"
    ),
    DoctrineBlock(
        topic="Hydration Unit: Gel Mixing and Chemical Addition",
        keywords=["hydration unit", "gel mixing", "chemical addition", "fluid quality", "stage design"],
        conclusion_template="Hydration units must ensure consistent gel mixing and accurate chemical addition to achieve target fluid properties for each stage.",
        reasoning_framework=(
            "Gel mixing must be uniform to prevent viscosity variations and stage failures. "
            "Chemical addition rates are determined by stage design and fluid requirements. "
            "Hydration unit design should facilitate real-time adjustment and monitoring. "
            "Quality control protocols require sampling and testing of mixed fluid. "
            "Maintenance of hydration unit and chemical dosing systems is essential for reliability."
        ),
        key_factors=[
            "Gel mixing quality",
            "Chemical addition accuracy",
            "Fluid property targets",
            "Hydration unit maintenance",
            "Quality control sampling"
        ],
        primary_authority=[
            "OEM Hydration Unit Manuals",
            "API RP 100-1",
            "Fluid Quality Reports"
        ],
        burden_holder="Frac Fluid Engineer",
        adversary_position="Manual chemical addition is sufficient; automation increases complexity.",
        counter_arguments=[
            "Automated systems improve accuracy and consistency.",
            "Manual addition risks human error and stage failures."
        ],
        resolution_strategy="Implement automated chemical dosing and real-time monitoring; validate with quality control sampling.",
        entity_scope="Frac Fluid Engineering",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 7.1"
    ),
    DoctrineBlock(
        topic="Data Van: Treatment Monitoring and SCADA Integration",
        keywords=["data van", "SCADA", "treatment monitoring", "real-time data", "stage optimization"],
        conclusion_template="Data van and SCADA integration enable real-time treatment monitoring and stage optimization, improving operational efficiency and safety.",
        reasoning_framework=(
            "Data van collects real-time data from pumps, blender, hydration unit, and treating iron. "
            "SCADA integration allows remote monitoring, control, and data archiving. "
            "Real-time analytics enable rapid adjustments to stage parameters. "
            "Data van must be equipped with redundant communication systems and secure data storage. "
            "Operational protocols require regular calibration and validation of sensors and data streams."
        ),
        key_factors=[
            "Real-time data collection",
            "SCADA integration",
            "Data reliability",
            "Sensor calibration",
            "Operational protocols"
        ],
        primary_authority=[
            "OEM Data Van Manuals",
            "API RP 100-1",
            "Field Data Analytics Reports"
        ],
        burden_holder="Frac Data Analyst",
        adversary_position="Manual monitoring is sufficient; SCADA integration adds unnecessary complexity.",
        counter_arguments=[
            "SCADA improves efficiency and reduces NPT.",
            "Manual monitoring risks delayed response and stage failures."
        ],
        resolution_strategy="Implement SCADA integration and real-time analytics; validate with operational data.",
        entity_scope="Frac Data Analytics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 8.3"
    ),
    DoctrineBlock(
        topic="Wireline Operations: Plug Pump-Down and Gun Deployment",
        keywords=["wireline", "plug pump-down", "gun deployment", "stage completion", "safety"],
        conclusion_template="Wireline operations for plug pump-down and gun deployment must be coordinated with frac fleet to ensure stage completion and safety.",
        reasoning_framework=(
            "Plug pump-down requires synchronization of pump rates and wireline operations. "
            "Gun deployment must follow strict safety protocols and regulatory requirements. "
            "Operational coordination minimizes NPT and ensures timely stage completion. "
            "Wireline crew must be trained and certified for high-pressure operations. "
            "Data van integration enables real-time monitoring of wireline activity."
        ),
        key_factors=[
            "Pump rate coordination",
            "Wireline crew certification",
            "Safety protocols",
            "Operational coordination",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 100-1",
            "Wireline OEM Manuals",
            "Field Safety Reports"
        ],
        burden_holder="Wireline Operations Supervisor",
        adversary_position="Wireline operations can be conducted independently; coordination is unnecessary.",
        counter_arguments=[
            "Lack of coordination increases NPT and safety risks.",
            "Integrated operations improve stage efficiency."
        ],
        resolution_strategy="Establish integrated operational protocols and real-time monitoring for wireline operations.",
        entity_scope="Wireline Operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 9.1"
    ),
    DoctrineBlock(
        topic="Coiled Tubing: Milling, Drillout, and Cleanout",
        keywords=["coiled tubing", "milling", "drillout", "cleanout", "stage completion", "fluid management"],
        conclusion_template="Coiled tubing operations for milling, drillout, and cleanout must be integrated with frac fleet fluid management to ensure stage completion and minimize NPT.",
        reasoning_framework=(
            "Milling and drillout require precise control of coiled tubing parameters and fluid properties. "
            "Cleanout operations must remove debris and ensure wellbore integrity. "
            "Integration with frac fleet fluid management optimizes stage completion and reduces NPT. "
            "Coiled tubing crew must be trained and certified for high-pressure operations. "
            "Real-time monitoring enables rapid response to operational challenges."
        ),
        key_factors=[
            "Coiled tubing parameters",
            "Fluid management",
            "Crew certification",
            "Operational integration",
            "Real-time monitoring"
        ],
        primary_authority=[
            "API RP 100-1",
            "Coiled Tubing OEM Manuals",
            "Field Completion Reports"
        ],
        burden_holder="Coiled Tubing Operations Lead",
        adversary_position="Coiled tubing can operate independently; integration adds complexity.",
        counter_arguments=[
            "Integrated operations reduce NPT and improve stage completion.",
            "Independent operations risk fluid management failures."
        ],
        resolution_strategy="Establish integrated protocols and real-time monitoring for coiled tubing operations.",
        entity_scope="Coiled Tubing Operations",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 10.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Fuel Consumption: Diesel, CNG, and Field Gas",
        keywords=["fuel consumption", "diesel", "CNG", "field gas", "emissions", "cost"],
        conclusion_template="Frac fleet fuel consumption must be optimized across diesel, CNG, and field gas to minimize cost and emissions while ensuring operational reliability.",
        reasoning_framework=(
            "Fuel consumption is a major operational cost and emissions driver. "
            "Diesel is reliable but has higher emissions and cost. "
            "CNG and field gas offer lower emissions and cost, but require infrastructure and quality control. "
            "Fleet configuration should maximize use of cleaner fuels where feasible. "
            "Operational protocols require monitoring of fuel quality and consumption rates."
        ),
        key_factors=[
            "Fuel cost",
            "Emissions profile",
            "Infrastructure availability",
            "Operational reliability",
            "Fuel quality"
        ],
        primary_authority=[
            "EPA Emissions Reports",
            "OEM Engine Manuals",
            "Field Fuel Consumption Data"
        ],
        burden_holder="Fleet Fuel Manager",
        adversary_position="Diesel is more reliable; CNG and field gas increase operational risk.",
        counter_arguments=[
            "Cleaner fuels reduce emissions and cost.",
            "Proper infrastructure mitigates reliability risks."
        ],
        resolution_strategy="Optimize fuel mix based on infrastructure and operational requirements; monitor consumption and emissions.",
        entity_scope="Frac Fleet Fuel Management",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Tier 4 Standards"
    ),
    DoctrineBlock(
        topic="Dual-Fuel Substitution Ratio and Field Gas Economics",
        keywords=["dual-fuel", "substitution ratio", "field gas", "economics", "emissions", "cost"],
        conclusion_template="Dual-fuel substitution ratio must be optimized based on field gas economics and engine performance to maximize cost savings and emissions reduction.",
        reasoning_framework=(
            "Substitution ratio is determined by engine load, gas quality, and operational parameters. "
            "Higher substitution ratios reduce diesel consumption and emissions, but may impact engine performance. "
            "Field gas economics depend on supply, quality, and processing costs. "
            "Operational protocols require monitoring of substitution ratio and engine performance. "
            "Regulatory compliance requires emissions reporting and validation."
        ),
        key_factors=[
            "Engine load",
            "Gas quality",
            "Field gas supply",
            "Processing cost",
            "Emissions profile"
        ],
        primary_authority=[
            "EPA Emissions Reports",
            "OEM Engine Manuals",
            "Field Fuel Economics Data"
        ],
        burden_holder="Fleet Fuel Economics Analyst",
        adversary_position="High substitution ratios risk engine performance and reliability.",
        counter_arguments=[
            "Proper monitoring and control mitigate performance risks.",
            "Cost savings and emissions reduction justify optimization."
        ],
        resolution_strategy="Monitor substitution ratio and engine performance; optimize based on field gas economics.",
        entity_scope="Frac Fleet Fuel Economics",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Tier 4 Final Rule"
    ),
    DoctrineBlock(
        topic="Frac Fleet Mobilization, Demobilization, and Rig-Up",
        keywords=["mobilization", "demobilization", "rig-up", "logistics", "fleet deployment"],
        conclusion_template="Frac fleet mobilization, demobilization, and rig-up require coordinated logistics and adherence to safety protocols to minimize NPT and operational risk.",
        reasoning_framework=(
            "Mobilization and demobilization involve transport of pumps, treating iron, blender, hydration unit, and data van. "
            "Rig-up must follow certified procedures to ensure safety and operational readiness. "
            "Logistics coordination minimizes NPT and ensures timely fleet deployment. "
            "Safety protocols require inspection and certification of equipment prior to rig-up. "
            "Operational data from prior jobs inform logistics planning."
        ),
        key_factors=[
            "Logistics coordination",
            "Safety protocols",
            "Equipment certification",
            "Operational readiness",
            "NPT minimization"
        ],
        primary_authority=[
            "Fleet Logistics Manual",
            "API RP 100-1",
            "Field Safety Reports"
        ],
        burden_holder="Fleet Logistics Coordinator",
        adversary_position="Mobilization and rig-up can be conducted independently; coordination adds cost.",
        counter_arguments=[
            "Coordinated logistics reduce NPT and operational risk.",
            "Independent operations risk safety incidents."
        ],
        resolution_strategy="Establish coordinated logistics protocols and safety checks for mobilization and rig-up.",
        entity_scope="Fleet Logistics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 11.1"
    ),
    DoctrineBlock(
        topic="Pump Maintenance: Plunger, Fluid End, and Power End",
        keywords=["pump maintenance", "plunger", "fluid end", "power end", "reliability", "NPT"],
        conclusion_template="Pump maintenance protocols must address plunger, fluid end, and power end to maximize reliability and minimize NPT.",
        reasoning_framework=(
            "Plunger wear is a primary driver of pump maintenance; regular inspection and replacement are required. "
            "Fluid end maintenance addresses seals, valves, and pressure cycles. "
            "Power end maintenance includes lubrication, bearing inspection, and vibration monitoring. "
            "Maintenance intervals should be based on operational hours and stage data. "
            "Failure to maintain pumps increases NPT and operational risk."
        ),
        key_factors=[
            "Plunger wear",
            "Fluid end maintenance",
            "Power end maintenance",
            "Operational hours",
            "Stage data"
        ],
        primary_authority=[
            "OEM Pump Manuals",
            "API RP 100-1",
            "Field Maintenance Logs"
        ],
        burden_holder="Fleet Maintenance Supervisor",
        adversary_position="Extended maintenance intervals reduce cost; frequent maintenance is unnecessary.",
        counter_arguments=[
            "Frequent maintenance reduces NPT and improves reliability.",
            "Extended intervals risk pump failures."
        ],
        resolution_strategy="Establish maintenance protocols based on operational hours and stage data; monitor reliability metrics.",
        entity_scope="Fleet Maintenance",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 12.2"
    ),
    DoctrineBlock(
        topic="Equipment Reliability: MTBF and Pump Hours",
        keywords=["equipment reliability", "MTBF", "pump hours", "fleet performance", "NPT"],
        conclusion_template="Equipment reliability must be tracked using MTBF and pump hours to inform maintenance schedules and fleet performance optimization.",
        reasoning_framework=(
            "MTBF (Mean Time Between Failure) is a key metric for equipment reliability. "
            "Pump hours should be logged and analyzed to predict maintenance needs. "
            "Fleet performance optimization requires tracking reliability metrics and adjusting maintenance schedules. "
            "Operational protocols require real-time logging and reporting of failures and maintenance events. "
            "Reliability data informs fleet configuration and asset management."
        ),
        key_factors=[
            "MTBF",
            "Pump hours",
            "Failure logging",
            "Maintenance schedule",
            "Fleet performance"
        ],
        primary_authority=[
            "OEM Reliability Reports",
            "API RP 100-1",
            "Field Maintenance Logs"
        ],
        burden_holder="Fleet Reliability Engineer",
        adversary_position="Reliability tracking adds administrative burden; maintenance schedules are sufficient.",
        counter_arguments=[
            "Reliability tracking improves fleet performance and reduces NPT.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement real-time reliability tracking and adjust maintenance schedules based on MTBF and pump hours.",
        entity_scope="Fleet Reliability",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 13.1"
    ),
    DoctrineBlock(
        topic="Frac Crew Scheduling: 24-Hour Operations and Shift Management",
        keywords=["crew scheduling", "24-hour operations", "shift management", "fatigue", "NPT"],
        conclusion_template="Frac crew scheduling must support 24-hour operations with effective shift management to minimize fatigue and NPT.",
        reasoning_framework=(
            "24-hour operations require multiple shifts and effective management of crew fatigue. "
            "Shift management protocols should ensure adequate rest and rotation. "
            "Fatigue increases risk of operational errors and NPT. "
            "Crew scheduling must account for operational demands and regulatory requirements. "
            "Real-time monitoring of crew performance and fatigue is recommended."
        ),
        key_factors=[
            "Shift rotation",
            "Crew fatigue",
            "Operational demands",
            "Regulatory requirements",
            "Performance monitoring"
        ],
        primary_authority=[
            "Fleet Operations Manual",
            "API RP 100-1",
            "Field Crew Scheduling Reports"
        ],
        burden_holder="Fleet Operations Manager",
        adversary_position="Single shift operations are sufficient; 24-hour operations increase cost.",
        counter_arguments=[
            "24-hour operations reduce NPT and improve stage completion.",
            "Effective shift management mitigates fatigue risks."
        ],
        resolution_strategy="Implement shift management protocols and real-time performance monitoring for 24-hour operations.",
        entity_scope="Fleet Operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 14.2"
    ),
    DoctrineBlock(
        topic="Zipper Frac Operations: Simultaneous Multi-Well Stimulation",
        keywords=["zipper frac", "multi-well", "simultaneous stimulation", "stage efficiency", "NPT"],
        conclusion_template="Zipper frac operations enable simultaneous multi-well stimulation, improving stage efficiency and reducing NPT.",
        reasoning_framework=(
            "Zipper frac involves alternating stimulation between multiple wells, reducing idle time and improving efficiency. "
            "Operational coordination is critical to manage pump rates, treating iron, and wireline operations. "
            "Stage efficiency is improved by minimizing downtime between stages. "
            "Safety protocols require real-time monitoring and coordination between crews. "
            "NPT analysis informs operational adjustments and optimization."
        ),
        key_factors=[
            "Operational coordination",
            "Pump rate management",
            "Treating iron integration",
            "Wireline operations",
            "Stage efficiency"
        ],
        primary_authority=[
            "API RP 100-1",
            "Fleet Operations Manual",
            "Field Stage Efficiency Reports"
        ],
        burden_holder="Fleet Operations Supervisor",
        adversary_position="Zipper frac increases operational complexity and safety risk.",
        counter_arguments=[
            "Operational coordination and real-time monitoring mitigate risks.",
            "Efficiency gains justify complexity."
        ],
        resolution_strategy="Establish coordinated protocols and real-time monitoring for zipper frac operations.",
        entity_scope="Fleet Operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 15.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Efficiency: NPT Analysis and Stages per Day",
        keywords=["fleet efficiency", "NPT", "stages per day", "performance optimization", "operational data"],
        conclusion_template="Frac fleet efficiency must be tracked using NPT analysis and stages per day to inform performance optimization and operational adjustments.",
        reasoning_framework=(
            "NPT (Non-Productive Time) analysis identifies operational bottlenecks and informs optimization. "
            "Stages per day is a key metric for fleet efficiency. "
            "Operational data should be collected and analyzed in real-time. "
            "Performance optimization requires regular review of NPT and stage metrics. "
            "Fleet configuration and crew scheduling should be adjusted based on efficiency data."
        ),
        key_factors=[
            "NPT analysis",
            "Stages per day",
            "Operational data collection",
            "Performance review",
            "Fleet configuration"
        ],
        primary_authority=[
            "Fleet Operations Manual",
            "API RP 100-1",
            "Field Efficiency Reports"
        ],
        burden_holder="Fleet Performance Analyst",
        adversary_position="Efficiency tracking adds administrative burden; operational adjustments are sufficient.",
        counter_arguments=[
            "Efficiency tracking improves performance and reduces NPT.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement real-time efficiency tracking and adjust fleet configuration based on NPT and stages per day.",
        entity_scope="Fleet Performance",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 16.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Cost per Stage and Market Pricing Trends",
        keywords=["cost per stage", "market pricing", "fleet economics", "operational cost", "pricing trends"],
        conclusion_template="Frac fleet cost per stage must be tracked and benchmarked against market pricing trends to inform fleet economics and operational decisions.",
        reasoning_framework=(
            "Cost per stage is a primary metric for fleet economics. "
            "Market pricing trends inform operational decisions and fleet configuration. "
            "Operational cost data should be collected and analyzed in real-time. "
            "Benchmarking against market trends enables competitive pricing and cost optimization. "
            "Fleet configuration and operational protocols should be adjusted based on cost and pricing data."
        ),
        key_factors=[
            "Cost per stage",
            "Market pricing trends",
            "Operational cost data",
            "Benchmarking",
            "Fleet configuration"
        ],
        primary_authority=[
            "Fleet Economics Manual",
            "API RP 100-1",
            "Field Pricing Reports"
        ],
        burden_holder="Fleet Economics Analyst",
        adversary_position="Cost tracking adds administrative burden; market pricing is sufficient.",
        counter_arguments=[
            "Cost tracking improves fleet economics and competitiveness.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement real-time cost tracking and benchmarking against market pricing trends.",
        entity_scope="Fleet Economics",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 17.1"
    ),
    DoctrineBlock(
        topic="Multi-Doctrine Synthesis",
        keywords=["multi-doctrine", "synthesis", "fleet optimization", "integrated operations", "decision framework"],
        conclusion_template="Multi-doctrine synthesis enables integrated fleet optimization by combining operational, economic, and safety doctrines into a unified decision framework.",
        reasoning_framework=(
            "Integrated fleet optimization requires synthesis of operational, economic, and safety doctrines. "
            "Decision framework should incorporate real-time data from all fleet components. "
            "Operational protocols must be coordinated across pumps, treating iron, blender, hydration unit, data van, wireline, and coiled tubing. "
            "Economic analysis informs fleet configuration and cost optimization. "
            "Safety protocols ensure operational integrity and regulatory compliance. "
            "Multi-doctrine synthesis enables rapid response to operational challenges and market trends."
        ),
        key_factors=[
            "Integrated operations",
            "Decision framework",
            "Real-time data",
            "Economic analysis",
            "Safety protocols"
        ],
        primary_authority=[
            "Fleet Operations Manual",
            "API RP 100-1",
            "Field Synthesis Reports"
        ],
        burden_holder="Fleet Optimization Lead",
        adversary_position="Multi-doctrine synthesis increases complexity and administrative burden.",
        counter_arguments=[
            "Integrated operations improve fleet performance and competitiveness.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Establish integrated decision framework and real-time data synthesis for fleet optimization.",
        entity_scope="Fleet Optimization",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 18.3"
    ),
    # Additional DoctrineBlocks for domain completeness
    DoctrineBlock(
        topic="Frac Fluid Recycling and Water Management",
        keywords=["fluid recycling", "water management", "environmental compliance", "cost reduction", "ESG"],
        conclusion_template="Frac fluid recycling and water management protocols must be implemented to reduce environmental impact and operational costs.",
        reasoning_framework=(
            "Recycling frac fluids reduces freshwater demand and disposal costs. "
            "Water management strategies must comply with environmental regulations and ESG targets. "
            "Operational protocols require real-time monitoring of fluid quality and recycling rates. "
            "Cost reduction is achieved by minimizing water transport and disposal. "
            "Integration with fleet operations ensures consistent fluid supply and quality."
        ),
        key_factors=[
            "Fluid recycling rate",
            "Water quality",
            "Environmental compliance",
            "Operational cost",
            "ESG targets"
        ],
        primary_authority=[
            "EPA Water Management Guidelines",
            "API RP 100-1",
            "Field Water Management Reports"
        ],
        burden_holder="Fleet Environmental Manager",
        adversary_position="Fluid recycling increases operational complexity and cost.",
        counter_arguments=[
            "Environmental compliance and cost reduction justify recycling.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement real-time monitoring and integrated water management protocols.",
        entity_scope="Fleet Environmental Management",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Water Management Guidelines Section 5"
    ),
    DoctrineBlock(
        topic="Frac Fleet Digital Twin and Predictive Analytics",
        keywords=["digital twin", "predictive analytics", "fleet optimization", "real-time monitoring", "AI"],
        conclusion_template="Digital twin and predictive analytics enable real-time fleet optimization and proactive maintenance, improving efficiency and reducing NPT.",
        reasoning_framework=(
            "Digital twin technology creates a real-time virtual model of the frac fleet. "
            "Predictive analytics use operational data to forecast maintenance needs and optimize performance. "
            "Integration with SCADA and data van enables real-time monitoring and rapid response to operational challenges. "
            "AI algorithms improve accuracy of predictions and decision-making. "
            "Operational protocols require regular validation of digital twin and analytics models."
        ),
        key_factors=[
            "Digital twin accuracy",
            "Predictive analytics",
            "Real-time data integration",
            "AI algorithms",
            "Maintenance forecasting"
        ],
        primary_authority=[
            "OEM Digital Twin Manuals",
            "API RP 100-1",
            "Field Predictive Analytics Reports"
        ],
        burden_holder="Fleet Digital Lead",
        adversary_position="Digital twin and analytics add cost and complexity; manual protocols are sufficient.",
        counter_arguments=[
            "Efficiency gains and NPT reduction justify investment.",
            "Integration improves operational decision-making."
        ],
        resolution_strategy="Pilot digital twin and predictive analytics; validate with operational data.",
        entity_scope="Fleet Digital Operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 19.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Remote Operations and Automation",
        keywords=["remote operations", "automation", "SCADA", "fleet efficiency", "safety"],
        conclusion_template="Remote operations and automation protocols must be implemented to improve fleet efficiency and safety, enabling real-time control and monitoring.",
        reasoning_framework=(
            "Remote operations enable centralized control of frac fleet components. "
            "Automation protocols improve operational efficiency and reduce human error. "
            "SCADA integration allows real-time monitoring and rapid response to operational challenges. "
            "Safety is improved by reducing crew exposure to high-pressure environments. "
            "Operational protocols require regular validation of automation systems."
        ),
        key_factors=[
            "Remote control capability",
            "Automation protocols",
            "SCADA integration",
            "Operational efficiency",
            "Safety improvement"
        ],
        primary_authority=[
            "OEM Automation Manuals",
            "API RP 100-1",
            "Field Remote Operations Reports"
        ],
        burden_holder="Fleet Automation Lead",
        adversary_position="Remote operations increase complexity and risk; manual control is safer.",
        counter_arguments=[
            "Automation reduces human error and improves safety.",
            "Centralized control enables rapid response."
        ],
        resolution_strategy="Pilot remote operations and automation; validate with operational and safety data.",
        entity_scope="Fleet Automation",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 20.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet ESG Compliance and Reporting",
        keywords=["ESG", "compliance", "reporting", "emissions", "environmental impact"],
        conclusion_template="Frac fleet ESG compliance and reporting protocols must be implemented to meet regulatory and stakeholder requirements.",
        reasoning_framework=(
            "ESG compliance requires tracking and reporting of emissions, water usage, and environmental impact. "
            "Operational protocols must align with regulatory and stakeholder requirements. "
            "Real-time monitoring enables rapid response to compliance challenges. "
            "Reporting systems must be integrated with fleet operations and data van. "
            "ESG targets inform fleet configuration and operational decisions."
        ),
        key_factors=[
            "ESG targets",
            "Emissions tracking",
            "Water usage reporting",
            "Regulatory compliance",
            "Stakeholder requirements"
        ],
        primary_authority=[
            "EPA ESG Guidelines",
            "API RP 100-1",
            "Field ESG Reports"
        ],
        burden_holder="Fleet ESG Manager",
        adversary_position="ESG compliance increases operational cost and complexity.",
        counter_arguments=[
            "Regulatory penalties and stakeholder requirements justify compliance.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated ESG compliance and reporting systems.",
        entity_scope="Fleet ESG Management",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA ESG Guidelines Section 7"
    ),
    DoctrineBlock(
        topic="Frac Fleet Safety Incident Response and Investigation",
        keywords=["safety incident", "response", "investigation", "protocols", "regulatory compliance"],
        conclusion_template="Frac fleet safety incident response and investigation protocols must be implemented to ensure regulatory compliance and operational integrity.",
        reasoning_framework=(
            "Safety incident response protocols require immediate action and reporting. "
            "Investigation procedures must identify root causes and inform operational adjustments. "
            "Regulatory compliance requires documentation and reporting of incidents. "
            "Operational integrity is maintained by implementing corrective actions and tracking incident metrics. "
            "Crew training and certification are essential for effective response."
        ),
        key_factors=[
            "Incident response protocols",
            "Investigation procedures",
            "Regulatory compliance",
            "Corrective actions",
            "Crew training"
        ],
        primary_authority=[
            "API RP 100-1",
            "Fleet Safety Manual",
            "Field Incident Reports"
        ],
        burden_holder="Fleet Safety Officer",
        adversary_position="Incident response adds administrative burden; operational adjustments are sufficient.",
        counter_arguments=[
            "Regulatory compliance and operational integrity justify protocols.",
            "Incident tracking improves fleet safety."
        ],
        resolution_strategy="Implement integrated incident response and investigation protocols.",
        entity_scope="Fleet Safety",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 21.3"
    ),
    DoctrineBlock(
        topic="Frac Fleet Crew Training and Certification",
        keywords=["crew training", "certification", "safety", "operational readiness", "regulatory compliance"],
        conclusion_template="Frac fleet crew training and certification protocols must be implemented to ensure operational readiness and regulatory compliance.",
        reasoning_framework=(
            "Crew training ensures operational readiness and reduces safety risks. "
            "Certification protocols must align with regulatory requirements and fleet operations. "
            "Operational protocols require regular training and certification updates. "
            "Real-time monitoring of crew performance informs training needs. "
            "Regulatory compliance requires documentation of training and certification."
        ),
        key_factors=[
            "Training protocols",
            "Certification requirements",
            "Operational readiness",
            "Safety improvement",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 100-1",
            "Fleet Training Manual",
            "Field Crew Certification Reports"
        ],
        burden_holder="Fleet Training Coordinator",
        adversary_position="Training and certification add cost and administrative burden.",
        counter_arguments=[
            "Operational readiness and safety justify investment.",
            "Regulatory compliance mandates protocols."
        ],
        resolution_strategy="Implement integrated crew training and certification protocols.",
        entity_scope="Fleet Training",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 22.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Asset Management and Lifecycle Optimization",
        keywords=["asset management", "lifecycle optimization", "fleet performance", "cost reduction", "maintenance"],
        conclusion_template="Frac fleet asset management and lifecycle optimization protocols must be implemented to maximize fleet performance and reduce operational costs.",
        reasoning_framework=(
            "Asset management requires tracking operational hours, maintenance intervals, and performance metrics. "
            "Lifecycle optimization informs asset replacement and upgrade decisions. "
            "Operational protocols require real-time monitoring and reporting of asset status. "
            "Cost reduction is achieved by optimizing asset utilization and maintenance schedules. "
            "Integration with fleet operations ensures consistent asset performance."
        ),
        key_factors=[
            "Asset tracking",
            "Lifecycle optimization",
            "Performance metrics",
            "Maintenance schedules",
            "Cost reduction"
        ],
        primary_authority=[
            "Fleet Asset Management Manual",
            "API RP 100-1",
            "Field Asset Reports"
        ],
        burden_holder="Fleet Asset Manager",
        adversary_position="Asset management adds administrative burden; operational adjustments are sufficient.",
        counter_arguments=[
            "Lifecycle optimization improves fleet performance and reduces cost.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement integrated asset management and lifecycle optimization protocols.",
        entity_scope="Fleet Asset Management",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 23.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Regulatory Compliance and Audit",
        keywords=["regulatory compliance", "audit", "fleet operations", "documentation", "reporting"],
        conclusion_template="Frac fleet regulatory compliance and audit protocols must be implemented to ensure operational integrity and avoid penalties.",
        reasoning_framework=(
            "Regulatory compliance requires tracking and reporting of operational data, emissions, and safety incidents. "
            "Audit protocols must align with regulatory requirements and fleet operations. "
            "Operational protocols require regular documentation and reporting updates. "
            "Real-time monitoring of compliance metrics informs audit readiness. "
            "Regulatory penalties are avoided by maintaining audit-ready documentation."
        ),
        key_factors=[
            "Compliance tracking",
            "Audit protocols",
            "Documentation",
            "Reporting",
            "Operational integrity"
        ],
        primary_authority=[
            "API RP 100-1",
            "Fleet Compliance Manual",
            "Field Audit Reports"
        ],
        burden_holder="Fleet Compliance Auditor",
        adversary_position="Compliance and audit add cost and administrative burden.",
        counter_arguments=[
            "Operational integrity and penalty avoidance justify protocols.",
            "Audit readiness improves fleet operations."
        ],
        resolution_strategy="Implement integrated compliance and audit protocols.",
        entity_scope="Fleet Compliance",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 24.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Supply Chain and Inventory Management",
        keywords=["supply chain", "inventory management", "fleet operations", "cost optimization", "logistics"],
        conclusion_template="Frac fleet supply chain and inventory management protocols must be implemented to optimize operational cost and logistics.",
        reasoning_framework=(
            "Supply chain management requires tracking inventory levels, procurement schedules, and logistics coordination. "
            "Inventory management protocols ensure consistent supply of pumps, iron, proppant, chemicals, and fuel. "
            "Operational protocols require real-time monitoring and reporting of inventory status. "
            "Cost optimization is achieved by minimizing excess inventory and optimizing procurement schedules. "
            "Integration with fleet operations ensures timely supply and operational readiness."
        ),
        key_factors=[
            "Inventory tracking",
            "Procurement schedules",
            "Logistics coordination",
            "Cost optimization",
            "Operational readiness"
        ],
        primary_authority=[
            "Fleet Supply Chain Manual",
            "API RP 100-1",
            "Field Inventory Reports"
        ],
        burden_holder="Fleet Supply Chain Manager",
        adversary_position="Supply chain and inventory management add cost and administrative burden.",
        counter_arguments=[
            "Cost optimization and operational readiness justify protocols.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement integrated supply chain and inventory management protocols.",
        entity_scope="Fleet Supply Chain",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 25.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Proppant Logistics and Quality Control",
        keywords=["proppant logistics", "quality control", "fleet operations", "stage design", "cost optimization"],
        conclusion_template="Frac fleet proppant logistics and quality control protocols must be implemented to optimize stage design and operational cost.",
        reasoning_framework=(
            "Proppant logistics require tracking supply, transport, and storage of proppant materials. "
            "Quality control protocols ensure consistent proppant size, shape, and concentration. "
            "Operational protocols require real-time monitoring and reporting of proppant quality and logistics status. "
            "Stage design is optimized by matching proppant quality to formation requirements. "
            "Cost optimization is achieved by minimizing transport and storage costs."
        ),
        key_factors=[
            "Proppant supply",
            "Transport logistics",
            "Storage protocols",
            "Quality control",
            "Stage design"
        ],
        primary_authority=[
            "Fleet Proppant Logistics Manual",
            "API RP 100-1",
            "Field Proppant Quality Reports"
        ],
        burden_holder="Fleet Proppant Logistics Manager",
        adversary_position="Proppant logistics and quality control add cost and administrative burden.",
        counter_arguments=[
            "Stage optimization and cost reduction justify protocols.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement integrated proppant logistics and quality control protocols.",
        entity_scope="Fleet Proppant Logistics",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 26.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Chemical Supply and Dosing Accuracy",
        keywords=["chemical supply", "dosing accuracy", "fleet operations", "fluid quality", "cost optimization"],
        conclusion_template="Frac fleet chemical supply and dosing accuracy protocols must be implemented to optimize fluid quality and operational cost.",
        reasoning_framework=(
            "Chemical supply management requires tracking procurement, transport, and storage of chemicals. "
            "Dosing accuracy protocols ensure consistent fluid quality and stage performance. "
            "Operational protocols require real-time monitoring and reporting of chemical supply and dosing status. "
            "Fluid quality is optimized by matching chemical dosing to stage requirements. "
            "Cost optimization is achieved by minimizing excess chemical usage and optimizing procurement schedules."
        ),
        key_factors=[
            "Chemical supply",
            "Procurement schedules",
            "Transport logistics",
            "Dosing accuracy",
            "Fluid quality"
        ],
        primary_authority=[
            "Fleet Chemical Supply Manual",
            "API RP 100-1",
            "Field Chemical Quality Reports"
        ],
        burden_holder="Fleet Chemical Supply Manager",
        adversary_position="Chemical supply and dosing accuracy add cost and administrative burden.",
        counter_arguments=[
            "Fluid quality and cost optimization justify protocols.",
            "Administrative burden is offset by operational savings."
        ],
        resolution_strategy="Implement integrated chemical supply and dosing accuracy protocols.",
        entity_scope="Fleet Chemical Supply",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 27.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Real-Time Communication and Coordination",
        keywords=["real-time communication", "coordination", "fleet operations", "efficiency", "safety"],
        conclusion_template="Frac fleet real-time communication and coordination protocols must be implemented to optimize operational efficiency and safety.",
        reasoning_framework=(
            "Real-time communication enables rapid response to operational challenges and improves coordination between fleet components. "
            "Coordination protocols ensure pumps, treating iron, blender, hydration unit, data van, wireline, and coiled tubing operate in sync. "
            "Operational efficiency is improved by minimizing downtime and optimizing stage completion. "
            "Safety is improved by reducing risk of miscommunication and operational errors. "
            "Operational protocols require regular validation of communication systems."
        ),
        key_factors=[
            "Communication systems",
            "Coordination protocols",
            "Operational efficiency",
            "Safety improvement",
            "Validation procedures"
        ],
        primary_authority=[
            "Fleet Communication Manual",
            "API RP 100-1",
            "Field Coordination Reports"
        ],
        burden_holder="Fleet Communication Lead",
        adversary_position="Real-time communication and coordination add cost and complexity.",
        counter_arguments=[
            "Efficiency and safety gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated real-time communication and coordination protocols.",
        entity_scope="Fleet Communication",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 28.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Emergency Shutdown and Response",
        keywords=["emergency shutdown", "response", "fleet operations", "safety", "regulatory compliance"],
        conclusion_template="Frac fleet emergency shutdown and response protocols must be implemented to ensure safety and regulatory compliance.",
        reasoning_framework=(
            "Emergency shutdown protocols require immediate action and coordination between fleet components. "
            "Response procedures must align with regulatory requirements and operational safety standards. "
            "Operational protocols require real-time monitoring and reporting of shutdown events. "
            "Safety is improved by reducing risk of catastrophic incidents. "
            "Regulatory compliance requires documentation and reporting of shutdowns."
        ),
        key_factors=[
            "Shutdown protocols",
            "Response procedures",
            "Safety improvement",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "API RP 100-1",
            "Fleet Safety Manual",
            "Field Shutdown Reports"
        ],
        burden_holder="Fleet Safety Lead",
        adversary_position="Emergency shutdown protocols add cost and administrative burden.",
        counter_arguments=[
            "Safety and regulatory compliance justify protocols.",
            "Operational protocols mitigate administrative burden."
        ],
        resolution_strategy="Implement integrated emergency shutdown and response protocols.",
        entity_scope="Fleet Safety",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 29.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Weather Impact and Contingency Planning",
        keywords=["weather impact", "contingency planning", "fleet operations", "NPT", "safety"],
        conclusion_template="Frac fleet weather impact and contingency planning protocols must be implemented to minimize NPT and ensure operational safety.",
        reasoning_framework=(
            "Weather impact protocols require real-time monitoring of weather conditions and operational readiness. "
            "Contingency planning ensures rapid response to weather-related challenges. "
            "Operational protocols require coordination between fleet components and logistics. "
            "NPT is minimized by proactive planning and rapid response. "
            "Safety is improved by reducing risk of weather-related incidents."
        ),
        key_factors=[
            "Weather monitoring",
            "Contingency planning",
            "Operational readiness",
            "NPT minimization",
            "Safety improvement"
        ],
        primary_authority=[
            "Fleet Weather Manual",
            "API RP 100-1",
            "Field Contingency Reports"
        ],
        burden_holder="Fleet Contingency Planner",
        adversary_position="Weather impact and contingency planning add cost and complexity.",
        counter_arguments=[
            "NPT and safety gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated weather impact and contingency planning protocols.",
        entity_scope="Fleet Contingency Planning",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 30.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Pad Layout and Equipment Placement",
        keywords=["pad layout", "equipment placement", "fleet operations", "safety", "efficiency"],
        conclusion_template="Frac fleet pad layout and equipment placement protocols must be implemented to optimize operational efficiency and safety.",
        reasoning_framework=(
            "Pad layout protocols require strategic placement of pumps, treating iron, blender, hydration unit, data van, wireline, and coiled tubing. "
            "Equipment placement must optimize operational efficiency and minimize safety risks. "
            "Operational protocols require real-time monitoring and validation of pad layout. "
            "Safety is improved by reducing risk of equipment collisions and operational errors. "
            "Efficiency is improved by minimizing transport and setup time."
        ),
        key_factors=[
            "Pad layout design",
            "Equipment placement",
            "Operational efficiency",
            "Safety improvement",
            "Validation procedures"
        ],
        primary_authority=[
            "Fleet Pad Layout Manual",
            "API RP 100-1",
            "Field Pad Layout Reports"
        ],
        burden_holder="Fleet Pad Layout Lead",
        adversary_position="Pad layout and equipment placement add cost and complexity.",
        counter_arguments=[
            "Efficiency and safety gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated pad layout and equipment placement protocols.",
        entity_scope="Fleet Pad Layout",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 31.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Stage Design and Optimization",
        keywords=["stage design", "optimization", "fleet operations", "performance", "cost reduction"],
        conclusion_template="Frac fleet stage design and optimization protocols must be implemented to maximize performance and reduce operational costs.",
        reasoning_framework=(
            "Stage design protocols require matching pump rate, proppant concentration, and fluid properties to formation requirements. "
            "Optimization is achieved by analyzing operational data and adjusting stage parameters. "
            "Operational protocols require real-time monitoring and reporting of stage performance. "
            "Performance is maximized by minimizing NPT and optimizing stage completion. "
            "Cost reduction is achieved by optimizing stage parameters and minimizing excess material usage."
        ),
        key_factors=[
            "Stage parameters",
            "Operational data analysis",
            "Performance metrics",
            "Cost reduction",
            "Optimization protocols"
        ],
        primary_authority=[
            "Fleet Stage Design Manual",
            "API RP 100-1",
            "Field Stage Performance Reports"
        ],
        burden_holder="Fleet Stage Design Lead",
        adversary_position="Stage design and optimization add cost and complexity.",
        counter_arguments=[
            "Performance and cost gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated stage design and optimization protocols.",
        entity_scope="Fleet Stage Design",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 32.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Proppant Concentration and Distribution",
        keywords=["proppant concentration", "distribution", "fleet operations", "stage performance", "quality control"],
        conclusion_template="Frac fleet proppant concentration and distribution protocols must be implemented to optimize stage performance and quality control.",
        reasoning_framework=(
            "Proppant concentration protocols require matching slurry concentration to stage requirements. "
            "Distribution protocols ensure consistent proppant placement in the formation. "
            "Operational protocols require real-time monitoring and reporting of proppant concentration and distribution. "
            "Stage performance is optimized by minimizing NPT and maximizing proppant placement. "
            "Quality control is achieved by validating proppant concentration and distribution metrics."
        ),
        key_factors=[
            "Slurry concentration",
            "Distribution protocols",
            "Stage requirements",
            "Quality control",
            "Performance metrics"
        ],
        primary_authority=[
            "Fleet Proppant Concentration Manual",
            "API RP 100-1",
            "Field Proppant Distribution Reports"
        ],
        burden_holder="Fleet Proppant Concentration Lead",
        adversary_position="Proppant concentration and distribution add cost and complexity.",
        counter_arguments=[
            "Stage performance and quality gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated proppant concentration and distribution protocols.",
        entity_scope="Fleet Proppant Concentration",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 33.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Fluid Property Monitoring and Adjustment",
        keywords=["fluid property", "monitoring", "adjustment", "fleet operations", "stage performance"],
        conclusion_template="Frac fleet fluid property monitoring and adjustment protocols must be implemented to optimize stage performance and operational efficiency.",
        reasoning_framework=(
            "Fluid property monitoring protocols require real-time tracking of viscosity, pH, and chemical concentration. "
            "Adjustment protocols enable rapid response to operational challenges and stage requirements. "
            "Operational protocols require integration with hydration unit and blender. "
            "Stage performance is optimized by matching fluid properties to formation requirements. "
            "Operational efficiency is improved by minimizing downtime and optimizing stage completion."
        ),
        key_factors=[
            "Viscosity monitoring",
            "pH tracking",
            "Chemical concentration",
            "Adjustment protocols",
            "Stage requirements"
        ],
        primary_authority=[
            "Fleet Fluid Property Manual",
            "API RP 100-1",
            "Field Fluid Property Reports"
        ],
        burden_holder="Fleet Fluid Property Lead",
        adversary_position="Fluid property monitoring and adjustment add cost and complexity.",
        counter_arguments=[
            "Stage performance and efficiency gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated fluid property monitoring and adjustment protocols.",
        entity_scope="Fleet Fluid Property",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 34.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Chemical Compatibility and Formation Integrity",
        keywords=["chemical compatibility", "formation integrity", "fleet operations", "stage design", "quality control"],
        conclusion_template="Frac fleet chemical compatibility and formation integrity protocols must be implemented to optimize stage design and quality control.",
        reasoning_framework=(
            "Chemical compatibility protocols require matching chemical properties to formation requirements. "
            "Formation integrity protocols ensure chemicals do not damage the formation or reduce stage performance. "
            "Operational protocols require real-time monitoring and reporting of chemical compatibility and formation integrity. "
            "Stage design is optimized by validating chemical compatibility and formation integrity metrics. "
            "Quality control is achieved by minimizing formation damage and maximizing stage performance."
        ),
        key_factors=[
            "Chemical properties",
            "Formation requirements",
            "Compatibility protocols",
            "Integrity metrics",
            "Quality control"
        ],
        primary_authority=[
            "Fleet Chemical Compatibility Manual",
            "API RP 100-1",
            "Field Formation Integrity Reports"
        ],
        burden_holder="Fleet Chemical Compatibility Lead",
        adversary_position="Chemical compatibility and formation integrity add cost and complexity.",
        counter_arguments=[
            "Stage design and quality gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated chemical compatibility and formation integrity protocols.",
        entity_scope="Fleet Chemical Compatibility",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 35.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Data Integration and Analytics",
        keywords=["data integration", "analytics", "fleet operations", "performance optimization", "real-time monitoring"],
        conclusion_template="Frac fleet data integration and analytics protocols must be implemented to optimize performance and operational efficiency.",
        reasoning_framework=(
            "Data integration protocols require real-time collection and aggregation of operational data. "
            "Analytics protocols enable rapid response to operational challenges and performance optimization. "
            "Operational protocols require integration with data van and SCADA systems. "
            "Performance is optimized by analyzing operational data and adjusting fleet configuration. "
            "Operational efficiency is improved by minimizing downtime and optimizing stage completion."
        ),
        key_factors=[
            "Data collection",
            "Integration protocols",
            "Analytics systems",
            "Performance optimization",
            "Operational efficiency"
        ],
        primary_authority=[
            "Fleet Data Integration Manual",
            "API RP 100-1",
            "Field Data Analytics Reports"
        ],
        burden_holder="Fleet Data Integration Lead",
        adversary_position="Data integration and analytics add cost and complexity.",
        counter_arguments=[
            "Performance and efficiency gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated data integration and analytics protocols.",
        entity_scope="Fleet Data Integration",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 36.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Operational Risk Assessment and Mitigation",
        keywords=["operational risk", "assessment", "mitigation", "fleet operations", "safety"],
        conclusion_template="Frac fleet operational risk assessment and mitigation protocols must be implemented to optimize safety and operational integrity.",
        reasoning_framework=(
            "Operational risk assessment protocols require identification and analysis of operational risks. "
            "Mitigation protocols enable rapid response to operational challenges and safety incidents. "
            "Operational protocols require integration with fleet operations and safety systems. "
            "Safety is optimized by minimizing operational risks and implementing mitigation strategies. "
            "Operational integrity is improved by tracking risk metrics and implementing corrective actions."
        ),
        key_factors=[
            "Risk identification",
            "Assessment protocols",
            "Mitigation strategies",
            "Safety improvement",
            "Operational integrity"
        ],
        primary_authority=[
            "Fleet Risk Assessment Manual",
            "API RP 100-1",
            "Field Risk Assessment Reports"
        ],
        burden_holder="Fleet Risk Assessment Lead",
        adversary_position="Risk assessment and mitigation add cost and complexity.",
        counter_arguments=[
            "Safety and operational integrity gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated operational risk assessment and mitigation protocols.",
        entity_scope="Fleet Risk Assessment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 37.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Continuous Improvement and Operational Excellence",
        keywords=["continuous improvement", "operational excellence", "fleet operations", "performance optimization", "cost reduction"],
        conclusion_template="Frac fleet continuous improvement and operational excellence protocols must be implemented to optimize performance and reduce operational costs.",
        reasoning_framework=(
            "Continuous improvement protocols require regular review and analysis of operational data. "
            "Operational excellence is achieved by implementing best practices and optimizing fleet configuration. "
            "Operational protocols require integration with fleet operations and performance metrics. "
            "Performance is optimized by minimizing NPT and maximizing stage completion. "
            "Cost reduction is achieved by implementing continuous improvement strategies."
        ),
        key_factors=[
            "Operational data review",
            "Best practices",
            "Performance metrics",
            "Continuous improvement",
            "Cost reduction"
        ],
        primary_authority=[
            "Fleet Continuous Improvement Manual",
            "API RP 100-1",
            "Field Operational Excellence Reports"
        ],
        burden_holder="Fleet Continuous Improvement Lead",
        adversary_position="Continuous improvement and operational excellence add cost and complexity.",
        counter_arguments=[
            "Performance and cost gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated continuous improvement and operational excellence protocols.",
        entity_scope="Fleet Continuous Improvement",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 38.1"
    ),
    DoctrineBlock(
        topic="Frac Fleet Stakeholder Engagement and Communication",
        keywords=["stakeholder engagement", "communication", "fleet operations", "ESG", "regulatory compliance"],
        conclusion_template="Frac fleet stakeholder engagement and communication protocols must be implemented to optimize ESG compliance and operational integrity.",
        reasoning_framework=(
            "Stakeholder engagement protocols require regular communication with regulatory agencies, landowners, and community stakeholders. "
            "Operational protocols require integration with fleet operations and ESG reporting systems. "
            "ESG compliance is optimized by engaging stakeholders and addressing concerns. "
            "Operational integrity is improved by maintaining transparent communication and reporting. "
            "Regulatory compliance is achieved by documenting stakeholder engagement and communication."
        ),
        key_factors=[
            "Stakeholder engagement",
            "Communication protocols",
            "ESG compliance",
            "Operational integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Fleet Stakeholder Engagement Manual",
            "API RP 100-1",
            "Field Stakeholder Reports"
        ],
        burden_holder="Fleet Stakeholder Engagement Lead",
        adversary_position="Stakeholder engagement and communication add cost and complexity.",
        counter_arguments=[
            "ESG compliance and operational integrity gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated stakeholder engagement and communication protocols.",
        entity_scope="Fleet Stakeholder Engagement",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 39.2"
    ),
    DoctrineBlock(
        topic="Frac Fleet Technology Adoption and Innovation",
        keywords=["technology adoption", "innovation", "fleet operations", "performance optimization", "cost reduction"],
        conclusion_template="Frac fleet technology adoption and innovation protocols must be implemented to optimize performance and reduce operational costs.",
        reasoning_framework=(
            "Technology adoption protocols require evaluation and integration of new technologies into fleet operations. "
            "Innovation is achieved by piloting new equipment, automation systems, and analytics tools. "
            "Operational protocols require real-time monitoring and validation of technology performance. "
            "Performance is optimized by implementing innovative solutions and adjusting fleet configuration. "
            "Cost reduction is achieved by adopting technologies that improve efficiency and reduce material usage."
        ),
        key_factors=[
            "Technology evaluation",
            "Innovation protocols",
            "Performance optimization",
            "Cost reduction",
            "Operational integration"
        ],
        primary_authority=[
            "Fleet Technology Adoption Manual",
            "API RP 100-1",
            "Field Technology Innovation Reports"
        ],
        burden_holder="Fleet Technology Adoption Lead",
        adversary_position="Technology adoption and innovation add cost and complexity.",
        counter_arguments=[
            "Performance and cost gains justify investment.",
            "Operational protocols mitigate complexity."
        ],
        resolution_strategy="Implement integrated technology adoption and innovation protocols.",
        entity_scope="Fleet Technology Adoption",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 100-1 Section 40.1"
    )
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
        if any(keyword_lower in k.lower() for k in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]