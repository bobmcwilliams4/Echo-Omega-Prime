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
        topic="Control Valve Cv Sizing per ISA-75.01.01",
        keywords=["Cv sizing", "ISA-75.01.01", "control valve", "flow coefficient", "valve selection"],
        conclusion_template="The required Cv for the control valve shall be calculated per ISA-75.01.01, ensuring the selected valve meets process flow requirements under all operating conditions.",
        reasoning_framework=(
            "1. Identify process flow rate, pressure drop, fluid properties, and temperature.\n"
            "2. Apply ISA-75.01.01 equations to calculate required Cv.\n"
            "3. Consider minimum, normal, and maximum flow scenarios.\n"
            "4. Evaluate valve sizing against process variability and turndown requirements.\n"
            "5. Factor in piping geometry and upstream/downstream conditions.\n"
            "6. Validate Cv selection with manufacturer data and performance curves.\n"
            "7. Ensure margin for fouling, future expansion, and operational flexibility.\n"
            "8. Document calculation basis and assumptions.\n"
            "9. Review with process and instrumentation teams.\n"
            "10. Confirm compliance with ISA-75.01.01 and site standards."
        ),
        key_factors=[
            "Process flow rate",
            "Pressure drop",
            "Fluid properties",
            "Temperature",
            "Minimum/maximum flow scenarios",
            "Turndown ratio",
            "Piping geometry"
        ],
        primary_authority=["ISA-75.01.01", "Manufacturer Cv data"],
        burden_holder="Valve design engineer",
        adversary_position="Cv calculated may be insufficient for abnormal conditions or future expansion.",
        counter_arguments=[
            "Oversizing leads to poor control and instability.",
            "Undersizing results in inability to meet maximum flow.",
            "Manufacturer's Cv may differ from theoretical values."
        ],
        resolution_strategy="Perform sensitivity analysis and validate with field data; select valve with adjustable trim if needed.",
        entity_scope="Process control valves in industrial facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ISA-75.01.01 Section 6"
    ),
    DoctrineBlock(
        topic="Globe Valve vs Butterfly Valve Selection",
        keywords=["globe valve", "butterfly valve", "valve selection", "control", "isolation"],
        conclusion_template="Globe valves are preferred for precise throttling and severe service, while butterfly valves are selected for larger sizes and lower pressure drops.",
        reasoning_framework=(
            "1. Assess process requirements: throttling, isolation, flow control.\n"
            "2. Compare globe valve characteristics: linear flow, high shutoff, precise control.\n"
            "3. Compare butterfly valve characteristics: compact, low cost, suitable for large diameters.\n"
            "4. Evaluate pressure drop and flow capacity.\n"
            "5. Consider maintenance, accessibility, and actuator compatibility.\n"
            "6. Analyze material compatibility and temperature/pressure limits.\n"
            "7. Review site standards and historical performance.\n"
            "8. Factor in lifecycle cost and reliability.\n"
            "9. Consult with process and maintenance teams.\n"
            "10. Document selection rationale."
        ),
        key_factors=[
            "Throttling requirements",
            "Pressure drop",
            "Valve size",
            "Material compatibility",
            "Cost",
            "Maintenance"
        ],
        primary_authority=["ISA standards", "API 609", "API 602"],
        burden_holder="Valve selection engineer",
        adversary_position="Butterfly valves may not provide adequate shutoff or control in severe service.",
        counter_arguments=[
            "Globe valves are more expensive and require more space.",
            "Butterfly valves may leak at low pressures.",
            "Globe valves have higher pressure drop."
        ],
        resolution_strategy="Select based on process criticality and operational requirements; use hybrid solutions where appropriate.",
        entity_scope="Control and isolation valves in process industries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 609 Section 4"
    ),
    DoctrineBlock(
        topic="Safety Relief Valve Sizing per API 520",
        keywords=["safety relief valve", "API 520", "sizing", "overpressure protection", "relief"],
        conclusion_template="Safety relief valves shall be sized per API 520, ensuring adequate capacity to relieve overpressure scenarios in accordance with regulatory requirements.",
        reasoning_framework=(
            "1. Identify protected equipment and potential overpressure sources.\n"
            "2. Determine worst-case relief scenario: fire, blocked outlet, thermal expansion.\n"
            "3. Calculate required relief rate using API 520 equations.\n"
            "4. Select valve size and set pressure to match process requirements.\n"
            "5. Consider backpressure, built-up and superimposed.\n"
            "6. Validate sizing with manufacturer performance data.\n"
            "7. Ensure compliance with local regulations and insurance requirements.\n"
            "8. Document calculation basis and assumptions.\n"
            "9. Review with process safety and operations teams.\n"
            "10. Maintain records for regulatory audits."
        ),
        key_factors=[
            "Relief scenario",
            "Required relief rate",
            "Set pressure",
            "Backpressure",
            "Regulatory compliance"
        ],
        primary_authority=["API 520", "ASME Section VIII"],
        burden_holder="Process safety engineer",
        adversary_position="Valve may be undersized for unforeseen scenarios or oversized for normal operation.",
        counter_arguments=[
            "Oversizing can cause valve chatter and premature wear.",
            "Undersizing risks equipment damage and regulatory non-compliance.",
            "Manufacturer data may differ from API calculations."
        ],
        resolution_strategy="Perform scenario analysis and validate with field data; use conservative sizing where uncertainty exists.",
        entity_scope="Safety relief valves in process plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 520 Part I Section 3"
    ),
    DoctrineBlock(
        topic="Equal Percentage vs Linear Control Valve Characteristics",
        keywords=["equal percentage", "linear", "control valve", "characteristics", "valve selection"],
        conclusion_template="Equal percentage valves are preferred for applications with varying pressure drops, while linear valves are suitable for constant pressure drop and proportional control.",
        reasoning_framework=(
            "1. Analyze process control requirements and pressure drop profile.\n"
            "2. Compare equal percentage characteristics: exponential flow change, suited for varying pressure drops.\n"
            "3. Compare linear characteristics: proportional flow change, suited for constant pressure drops.\n"
            "4. Evaluate process stability and control accuracy.\n"
            "5. Consider actuator compatibility and response.\n"
            "6. Factor in process variability and turndown ratio.\n"
            "7. Review historical performance and site standards.\n"
            "8. Consult with process control engineers.\n"
            "9. Document selection rationale.\n"
            "10. Validate with manufacturer performance curves."
        ),
        key_factors=[
            "Pressure drop profile",
            "Control accuracy",
            "Process variability",
            "Turndown ratio"
        ],
        primary_authority=["ISA-75.11.01", "Manufacturer valve curves"],
        burden_holder="Control systems engineer",
        adversary_position="Linear valves may provide better control in some applications.",
        counter_arguments=[
            "Equal percentage valves can be less intuitive for operators.",
            "Linear valves may not handle varying pressure drops well.",
            "Process dynamics may favor one characteristic over another."
        ],
        resolution_strategy="Select based on process modeling and simulation; validate with pilot testing.",
        entity_scope="Control valves in process industries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISA-75.11.01 Section 5"
    ),
    DoctrineBlock(
        topic="Pneumatic vs Electric Actuator Selection",
        keywords=["pneumatic actuator", "electric actuator", "valve actuator", "selection", "automation"],
        conclusion_template="Pneumatic actuators are preferred for fast response and hazardous environments, while electric actuators are selected for precise control and remote operation.",
        reasoning_framework=(
            "1. Assess process automation requirements and site infrastructure.\n"
            "2. Compare pneumatic actuators: fast response, fail-safe, suitable for hazardous areas.\n"
            "3. Compare electric actuators: precise positioning, remote control, lower maintenance.\n"
            "4. Evaluate compatibility with control systems and safety protocols.\n"
            "5. Consider environmental conditions: temperature, humidity, explosion risk.\n"
            "6. Factor in maintenance, reliability, and lifecycle cost.\n"
            "7. Review site standards and historical performance.\n"
            "8. Consult with instrumentation and electrical engineers.\n"
            "9. Document selection rationale.\n"
            "10. Validate with manufacturer data and site trials."
        ),
        key_factors=[
            "Response time",
            "Hazardous area suitability",
            "Control precision",
            "Maintenance",
            "Site infrastructure"
        ],
        primary_authority=["ISA standards", "IECEx", "Manufacturer actuator data"],
        burden_holder="Instrumentation engineer",
        adversary_position="Electric actuators may not perform reliably in hazardous or remote locations.",
        counter_arguments=[
            "Pneumatic actuators require air supply and maintenance.",
            "Electric actuators may fail in power outages.",
            "Site-specific conditions may favor one type."
        ],
        resolution_strategy="Select based on site risk assessment and operational requirements; use hybrid systems where feasible.",
        entity_scope="Valve actuators in industrial facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISA-96.02.01 Section 7"
    ),
    DoctrineBlock(
        topic="NACE MR0175 Material Selection for Sour Service",
        keywords=["NACE MR0175", "material selection", "sour service", "valve", "corrosion"],
        conclusion_template="Materials for valves in sour service shall comply with NACE MR0175 requirements to prevent sulfide stress cracking and ensure long-term integrity.",
        reasoning_framework=(
            "1. Identify process conditions: H2S concentration, temperature, pressure.\n"
            "2. Review NACE MR0175 material requirements for sour service.\n"
            "3. Select materials resistant to sulfide stress cracking and corrosion.\n"
            "4. Validate material compatibility with manufacturer certifications.\n"
            "5. Consider weldability, mechanical properties, and cost.\n"
            "6. Factor in maintenance and inspection requirements.\n"
            "7. Document material selection and compliance.\n"
            "8. Review with corrosion and materials engineers.\n"
            "9. Ensure traceability and certification for all valve components.\n"
            "10. Maintain records for regulatory audits."
        ),
        key_factors=[
            "H2S concentration",
            "Temperature",
            "Pressure",
            "Material resistance",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "API 6A", "Manufacturer material certificates"],
        burden_holder="Materials engineer",
        adversary_position="Non-compliant materials may be cheaper but risk failure.",
        counter_arguments=[
            "Compliant materials can be expensive and harder to source.",
            "Operational conditions may change, affecting material suitability.",
            "Manufacturer certifications may not cover all components."
        ],
        resolution_strategy="Select materials per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in sour service environments",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="NACE MR0175 Section 2"
    ),
    DoctrineBlock(
        topic="API 6A Wellhead and Christmas Tree Valve Requirements",
        keywords=["API 6A", "wellhead", "christmas tree", "valve requirements", "oilfield"],
        conclusion_template="Valves for wellhead and Christmas tree applications shall comply with API 6A requirements, including material, pressure rating, and testing protocols.",
        reasoning_framework=(
            "1. Identify wellhead and Christmas tree service conditions.\n"
            "2. Review API 6A requirements for valve design, materials, and pressure ratings.\n"
            "3. Select valves with appropriate PSL and PR levels.\n"
            "4. Validate compliance with manufacturer certifications and test reports.\n"
            "5. Consider compatibility with other wellhead components.\n"
            "6. Factor in maintenance, inspection, and replacement schedules.\n"
            "7. Document selection and compliance.\n"
            "8. Review with drilling and production engineers.\n"
            "9. Ensure traceability and certification for all valve components.\n"
            "10. Maintain records for regulatory audits and client requirements."
        ),
        key_factors=[
            "Service conditions",
            "Pressure rating",
            "Material compliance",
            "Testing protocols",
            "Certification"
        ],
        primary_authority=["API 6A", "Manufacturer test reports"],
        burden_holder="Wellhead engineer",
        adversary_position="Non-compliant valves may reduce cost but risk catastrophic failure.",
        counter_arguments=[
            "API 6A compliant valves are more expensive.",
            "Testing protocols may delay project timelines.",
            "Compatibility issues with legacy equipment."
        ],
        resolution_strategy="Select valves per API 6A and validate with third-party testing; maintain strict traceability.",
        entity_scope="Wellhead and Christmas tree valves in oilfield operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 6A Section 4"
    ),
    DoctrineBlock(
        topic="Valve Noise Prediction per IEC 60534-8-3",
        keywords=["valve noise", "IEC 60534-8-3", "prediction", "control valve", "acoustics"],
        conclusion_template="Valve noise shall be predicted per IEC 60534-8-3, ensuring compliance with site noise limits and occupational health requirements.",
        reasoning_framework=(
            "1. Identify process conditions: flow rate, pressure drop, fluid properties.\n"
            "2. Apply IEC 60534-8-3 equations for noise prediction.\n"
            "3. Consider valve type, trim design, and installation geometry.\n"
            "4. Evaluate predicted noise against site limits and regulatory requirements.\n"
            "5. Factor in mitigation measures: silencers, insulation, low-noise trims.\n"
            "6. Validate predictions with manufacturer data and field measurements.\n"
            "7. Document calculation basis and assumptions.\n"
            "8. Review with process and safety teams.\n"
            "9. Ensure compliance with occupational health standards.\n"
            "10. Maintain records for regulatory audits."
        ),
        key_factors=[
            "Flow rate",
            "Pressure drop",
            "Valve type",
            "Trim design",
            "Site noise limits"
        ],
        primary_authority=["IEC 60534-8-3", "Manufacturer noise data"],
        burden_holder="Acoustics engineer",
        adversary_position="Predicted noise may underestimate actual field conditions.",
        counter_arguments=[
            "Field conditions may differ from calculation assumptions.",
            "Mitigation measures may not be fully effective.",
            "Regulatory limits may change."
        ],
        resolution_strategy="Validate predictions with field measurements and adjust mitigation measures as needed.",
        entity_scope="Control valves in industrial facilities",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="IEC 60534-8-3 Section 6"
    ),
    DoctrineBlock(
        topic="Cavitation and Flashing in Control Valves",
        keywords=["cavitation", "flashing", "control valve", "damage", "sizing"],
        conclusion_template="Control valves shall be selected and sized to minimize cavitation and flashing, ensuring long-term reliability and process stability.",
        reasoning_framework=(
            "1. Identify process conditions: pressure drop, fluid properties, temperature.\n"
            "2. Calculate cavitation and flashing indices per ISA-75.01.01.\n"
            "3. Select valve type and trim to minimize risk.\n"
            "4. Consider mitigation measures: anti-cavitation trim, downstream piping.\n"
            "5. Validate with manufacturer data and field experience.\n"
            "6. Document calculation basis and assumptions.\n"
            "7. Review with process and maintenance teams.\n"
            "8. Ensure compliance with site standards.\n"
            "9. Maintain records for reliability analysis.\n"
            "10. Monitor valve performance and adjust as needed."
        ),
        key_factors=[
            "Pressure drop",
            "Fluid properties",
            "Valve type",
            "Trim design",
            "Mitigation measures"
        ],
        primary_authority=["ISA-75.01.01", "Manufacturer anti-cavitation trim data"],
        burden_holder="Valve design engineer",
        adversary_position="Cavitation and flashing may occur under abnormal conditions.",
        counter_arguments=[
            "Mitigation measures may increase cost and complexity.",
            "Process variability may lead to unexpected cavitation.",
            "Manufacturer data may not reflect field conditions."
        ],
        resolution_strategy="Validate with field data and adjust valve selection as needed; use conservative design margins.",
        entity_scope="Control valves in process industries",
        confidence=0.90,
        confidence_zone="Medium",
        controlling_precedent="ISA-75.01.01 Section 8"
    ),
    DoctrineBlock(
        topic="Fugitive Emissions Standards for Valve Packing",
        keywords=["fugitive emissions", "valve packing", "standards", "environmental", "API 622"],
        conclusion_template="Valve packing shall comply with fugitive emissions standards (API 622, ISO 15848) to minimize environmental impact and regulatory risk.",
        reasoning_framework=(
            "1. Identify process conditions and regulatory requirements for emissions.\n"
            "2. Select valve packing materials and designs certified to API 622 or ISO 15848.\n"
            "3. Validate compliance with manufacturer test reports.\n"
            "4. Factor in maintenance, inspection, and replacement schedules.\n"
            "5. Document selection and compliance.\n"
            "6. Review with environmental and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve packing.\n"
            "8. Maintain records for regulatory audits.\n"
            "9. Monitor emissions and adjust packing as needed.\n"
            "10. Train operators on proper maintenance and inspection."
        ),
        key_factors=[
            "Regulatory requirements",
            "Packing material",
            "Certification",
            "Maintenance",
            "Inspection"
        ],
        primary_authority=["API 622", "ISO 15848", "Manufacturer test reports"],
        burden_holder="Environmental engineer",
        adversary_position="Non-compliant packing may reduce cost but increase emissions risk.",
        counter_arguments=[
            "Certified packing can be expensive and harder to source.",
            "Maintenance may be more frequent with low-emission packing.",
            "Regulatory requirements may change."
        ],
        resolution_strategy="Select packing per API 622 and ISO 15848; validate with third-party testing and maintain strict traceability.",
        entity_scope="Valves in regulated environments",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 622 Section 3"
    ),
    DoctrineBlock(
        topic="Fire-Safe Valve Design per API 607",
        keywords=["fire-safe", "valve design", "API 607", "safety", "testing"],
        conclusion_template="Valves in fire-prone areas shall be fire-safe per API 607, ensuring continued isolation and containment during fire scenarios.",
        reasoning_framework=(
            "1. Identify fire-prone areas and process conditions.\n"
            "2. Select valves certified to API 607 fire-safe standards.\n"
            "3. Validate compliance with manufacturer test reports.\n"
            "4. Factor in maintenance, inspection, and replacement schedules.\n"
            "5. Document selection and compliance.\n"
            "6. Review with safety and maintenance teams.\n"
            "7. Ensure traceability and certification for all fire-safe valves.\n"
            "8. Maintain records for regulatory audits.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on fire-safe valve maintenance."
        ),
        key_factors=[
            "Fire risk",
            "Valve certification",
            "Maintenance",
            "Inspection",
            "Regulatory compliance"
        ],
        primary_authority=["API 607", "Manufacturer fire-safe test reports"],
        burden_holder="Safety engineer",
        adversary_position="Non-fire-safe valves may reduce cost but risk catastrophic failure.",
        counter_arguments=[
            "Fire-safe valves are more expensive.",
            "Testing protocols may delay project timelines.",
            "Maintenance may be more frequent."
        ],
        resolution_strategy="Select valves per API 607 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in fire-prone areas",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 607 Section 4"
    ),
    DoctrineBlock(
        topic="Choke Valve Sizing for Oilfield Production",
        keywords=["choke valve", "sizing", "oilfield", "production", "API 6A"],
        conclusion_template="Choke valves shall be sized per API 6A and site-specific requirements to ensure stable flow and prevent erosion in oilfield production.",
        reasoning_framework=(
            "1. Identify production flow rates, pressure drops, and fluid properties.\n"
            "2. Apply API 6A equations for choke valve sizing.\n"
            "3. Factor in erosion risk and material selection.\n"
            "4. Validate sizing with manufacturer performance data.\n"
            "5. Consider operational flexibility and turndown requirements.\n"
            "6. Document calculation basis and assumptions.\n"
            "7. Review with production and maintenance teams.\n"
            "8. Ensure compliance with site standards.\n"
            "9. Maintain records for reliability analysis.\n"
            "10. Monitor valve performance and adjust as needed."
        ),
        key_factors=[
            "Flow rate",
            "Pressure drop",
            "Erosion risk",
            "Material selection",
            "Operational flexibility"
        ],
        primary_authority=["API 6A", "Manufacturer choke valve data"],
        burden_holder="Production engineer",
        adversary_position="Valve may be undersized for abnormal conditions or oversized for normal operation.",
        counter_arguments=[
            "Oversizing can cause instability and poor control.",
            "Undersizing risks erosion and equipment damage.",
            "Manufacturer data may differ from API calculations."
        ],
        resolution_strategy="Perform scenario analysis and validate with field data; use conservative sizing where uncertainty exists.",
        entity_scope="Choke valves in oilfield production",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 6A Section 7"
    ),
    DoctrineBlock(
        topic="Pressure Regulating Valve Selection and Sizing",
        keywords=["pressure regulating valve", "selection", "sizing", "pressure control", "regulator"],
        conclusion_template="Pressure regulating valves shall be selected and sized to maintain stable downstream pressure under all operating conditions.",
        reasoning_framework=(
            "1. Identify upstream and downstream pressure requirements.\n"
            "2. Select valve type: direct-acting, pilot-operated, or control valve.\n"
            "3. Calculate required flow capacity and pressure drop.\n"
            "4. Factor in process variability and turndown ratio.\n"
            "5. Validate sizing with manufacturer performance data.\n"
            "6. Consider material compatibility and maintenance requirements.\n"
            "7. Document calculation basis and assumptions.\n"
            "8. Review with process and instrumentation teams.\n"
            "9. Ensure compliance with site standards.\n"
            "10. Monitor valve performance and adjust as needed."
        ),
        key_factors=[
            "Upstream/downstream pressure",
            "Valve type",
            "Flow capacity",
            "Material compatibility",
            "Turndown ratio"
        ],
        primary_authority=["ISA standards", "Manufacturer regulator data"],
        burden_holder="Process engineer",
        adversary_position="Valve may not maintain stable pressure under variable conditions.",
        counter_arguments=[
            "Direct-acting valves may be less precise.",
            "Pilot-operated valves require maintenance.",
            "Control valves may be more expensive."
        ],
        resolution_strategy="Select based on process modeling and operational requirements; validate with pilot testing.",
        entity_scope="Pressure regulating valves in process industries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISA-75.12.01 Section 4"
    ),
    DoctrineBlock(
        topic="Gate Valve vs Ball Valve for Isolation Service",
        keywords=["gate valve", "ball valve", "isolation", "valve selection", "API 600"],
        conclusion_template="Gate valves are preferred for isolation in high-pressure, high-temperature service, while ball valves are selected for quick shutoff and low-pressure applications.",
        reasoning_framework=(
            "1. Assess isolation requirements and process conditions.\n"
            "2. Compare gate valve characteristics: robust, suitable for high-pressure/high-temperature.\n"
            "3. Compare ball valve characteristics: quick shutoff, low-pressure, minimal leakage.\n"
            "4. Evaluate maintenance, accessibility, and actuator compatibility.\n"
            "5. Factor in material compatibility and site standards.\n"
            "6. Review historical performance and reliability.\n"
            "7. Consult with maintenance and operations teams.\n"
            "8. Document selection rationale.\n"
            "9. Validate with manufacturer data.\n"
            "10. Monitor valve performance and adjust as needed."
        ),
        key_factors=[
            "Pressure/temperature",
            "Isolation requirements",
            "Valve type",
            "Material compatibility",
            "Maintenance"
        ],
        primary_authority=["API 600", "API 608", "Manufacturer valve data"],
        burden_holder="Valve selection engineer",
        adversary_position="Ball valves may not provide adequate isolation in severe service.",
        counter_arguments=[
            "Gate valves are slower to operate and require more space.",
            "Ball valves may leak under high pressure.",
            "Site-specific conditions may favor one type."
        ],
        resolution_strategy="Select based on process criticality and operational requirements; use hybrid solutions where appropriate.",
        entity_scope="Isolation valves in process industries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 600 Section 5"
    ),
    DoctrineBlock(
        topic="Check Valve Selection and Slam Prevention",
        keywords=["check valve", "slam prevention", "valve selection", "reverse flow", "API 594"],
        conclusion_template="Check valves shall be selected and installed to prevent slam and minimize reverse flow, ensuring process stability and equipment protection.",
        reasoning_framework=(
            "1. Identify process conditions and reverse flow risk.\n"
            "2. Select check valve type: swing, lift, piston, or silent.\n"
            "3. Factor in slam prevention measures: dampers, spring-loaded designs.\n"
            "4. Validate with manufacturer performance data.\n"
            "5. Consider installation geometry and piping layout.\n"
            "6. Document selection and rationale.\n"
            "7. Review with process and maintenance teams.\n"
            "8. Ensure compliance with site standards.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Maintain records for reliability analysis."
        ),
        key_factors=[
            "Reverse flow risk",
            "Valve type",
            "Slam prevention",
            "Installation geometry",
            "Maintenance"
        ],
        primary_authority=["API 594", "Manufacturer check valve data"],
        burden_holder="Process engineer",
        adversary_position="Check valves may slam under rapid flow reversal.",
        counter_arguments=[
            "Silent check valves can be more expensive.",
            "Spring-loaded designs may require maintenance.",
            "Installation geometry may limit options."
        ],
        resolution_strategy="Select based on process modeling and operational requirements; validate with pilot testing.",
        entity_scope="Check valves in process industries",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 594 Section 6"
    ),
    DoctrineBlock(
        topic="Valve Body Material Selection for Temperature Service",
        keywords=["valve body", "material selection", "temperature service", "thermal", "API 600"],
        conclusion_template="Valve body materials shall be selected to withstand process temperature extremes, ensuring long-term reliability and compliance with site standards.",
        reasoning_framework=(
            "1. Identify process temperature range and pressure conditions.\n"
            "2. Review material properties: thermal expansion, strength, corrosion resistance.\n"
            "3. Select materials per API 600 and site standards.\n"
            "4. Validate compatibility with manufacturer certifications.\n"
            "5. Factor in maintenance and inspection requirements.\n"
            "6. Document material selection and compliance.\n"
            "7. Review with materials and maintenance teams.\n"
            "8. Ensure traceability and certification for all valve components.\n"
            "9. Maintain records for reliability analysis.\n"
            "10. Monitor valve performance and adjust as needed."
        ),
        key_factors=[
            "Temperature range",
            "Pressure",
            "Material properties",
            "Certification",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer material certificates"],
        burden_holder="Materials engineer",
        adversary_position="Non-compliant materials may reduce cost but risk failure.",
        counter_arguments=[
            "Compliant materials can be expensive and harder to source.",
            "Operational conditions may change, affecting material suitability.",
            "Manufacturer certifications may not cover all components."
        ],
        resolution_strategy="Select materials per API 600 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in temperature extremes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 7"
    ),
    DoctrineBlock(
        topic="Valve End Connection Selection: Flanged vs Threaded vs Welded",
        keywords=["valve end connection", "flanged", "threaded", "welded", "selection"],
        conclusion_template="Valve end connections shall be selected based on process pressure, temperature, maintenance, and site standards, prioritizing flanged for accessibility, welded for high integrity, and threaded for small sizes.",
        reasoning_framework=(
            "1. Identify process pressure, temperature, and maintenance requirements.\n"
            "2. Compare flanged connections: accessible, easy to maintain, suitable for most applications.\n"
            "3. Compare welded connections: high integrity, suitable for high-pressure/high-temperature, less maintenance.\n"
            "4. Compare threaded connections: suitable for small sizes, low-pressure applications.\n"
            "5. Factor in site standards and historical performance.\n"
            "6. Review compatibility with piping and valve materials.\n"
            "7. Document selection rationale.\n"
            "8. Consult with maintenance and piping teams.\n"
            "9. Validate with manufacturer data.\n"
            "10. Monitor performance and adjust as needed."
        ),
        key_factors=[
            "Pressure",
            "Temperature",
            "Maintenance",
            "Connection type",
            "Site standards"
        ],
        primary_authority=["API 600", "ASME B16.5", "Manufacturer data"],
        burden_holder="Piping engineer",
        adversary_position="Welded connections may complicate maintenance; flanged may leak.",
        counter_arguments=[
            "Threaded connections are limited to small sizes.",
            "Welded connections require skilled labor.",
            "Flanged connections may be more expensive."
        ],
        resolution_strategy="Select based on process criticality and operational requirements; use hybrid solutions where appropriate.",
        entity_scope="Valve connections in process industries",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME B16.5 Section 3"
    ),
    DoctrineBlock(
        topic="Valve Stem Sealing: Packing vs Bellows Seal",
        keywords=["valve stem sealing", "packing", "bellows seal", "fugitive emissions", "maintenance"],
        conclusion_template="Bellows seal valves are preferred for zero emissions and high integrity, while packing is suitable for standard applications with regular maintenance.",
        reasoning_framework=(
            "1. Identify process conditions and emissions requirements.\n"
            "2. Compare packing: standard sealing, requires maintenance, suitable for most applications.\n"
            "3. Compare bellows seal: zero emissions, high integrity, suitable for hazardous or toxic service.\n"
            "4. Factor in maintenance, inspection, and replacement schedules.\n"
            "5. Review site standards and historical performance.\n"
            "6. Document selection rationale.\n"
            "7. Consult with environmental and maintenance teams.\n"
            "8. Validate with manufacturer data.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Emissions requirements",
            "Sealing integrity",
            "Maintenance",
            "Inspection",
            "Service type"
        ],
        primary_authority=["API 622", "ISO 15848", "Manufacturer data"],
        burden_holder="Environmental engineer",
        adversary_position="Packing may leak and require frequent maintenance.",
        counter_arguments=[
            "Bellows seal valves are more expensive.",
            "Packing is easier to replace.",
            "Site-specific conditions may favor one type."
        ],
        resolution_strategy="Select based on emissions risk and operational requirements; validate with pilot testing.",
        entity_scope="Valve stem sealing in process industries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 622 Section 4"
    ),
    DoctrineBlock(
        topic="Valve Testing Requirements per API and ASME Standards",
        keywords=["valve testing", "API", "ASME", "standards", "quality assurance"],
        conclusion_template="Valves shall be tested per API and ASME standards to ensure compliance, integrity, and performance prior to installation.",
        reasoning_framework=(
            "1. Identify applicable API and ASME testing standards.\n"
            "2. Review manufacturer test protocols and certifications.\n"
            "3. Validate test results against site requirements.\n"
            "4. Document testing procedures and results.\n"
            "5. Factor in maintenance and inspection schedules.\n"
            "6. Review with quality assurance and maintenance teams.\n"
            "7. Ensure traceability and certification for all valves.\n"
            "8. Maintain records for regulatory audits.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper testing and inspection."
        ),
        key_factors=[
            "Testing standards",
            "Certification",
            "Quality assurance",
            "Maintenance",
            "Inspection"
        ],
        primary_authority=["API 598", "ASME B16.34", "Manufacturer test reports"],
        burden_holder="Quality assurance engineer",
        adversary_position="Non-tested valves may reduce cost but risk failure.",
        counter_arguments=[
            "Testing protocols may delay project timelines.",
            "Certified valves are more expensive.",
            "Maintenance may be more frequent."
        ],
        resolution_strategy="Test valves per API and ASME standards; validate with third-party testing and maintain strict traceability.",
        entity_scope="Valves in regulated environments",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 598 Section 3"
    ),
    DoctrineBlock(
        topic="Valve Maintenance and Testing Schedules",
        keywords=["valve maintenance", "testing schedules", "inspection", "reliability", "preventive"],
        conclusion_template="Valves shall be maintained and tested per site schedules and manufacturer recommendations to ensure reliability and compliance.",
        reasoning_framework=(
            "1. Identify site maintenance and testing schedules.\n"
            "2. Review manufacturer maintenance recommendations.\n"
            "3. Document maintenance and testing procedures.\n"
            "4. Factor in process criticality and operational requirements.\n"
            "5. Review with maintenance and operations teams.\n"
            "6. Monitor valve performance and adjust schedules as needed.\n"
            "7. Maintain records for reliability analysis and regulatory audits.\n"
            "8. Train operators on proper maintenance and testing.\n"
            "9. Validate with field data and adjust as needed.\n"
            "10. Ensure compliance with site standards."
        ),
        key_factors=[
            "Maintenance schedule",
            "Testing procedures",
            "Process criticality",
            "Operational requirements",
            "Reliability"
        ],
        primary_authority=["Manufacturer recommendations", "Site standards"],
        burden_holder="Maintenance engineer",
        adversary_position="Maintenance may be deferred due to operational constraints.",
        counter_arguments=[
            "Deferred maintenance increases failure risk.",
            "Testing may disrupt operations.",
            "Manufacturer recommendations may not fit site conditions."
        ],
        resolution_strategy="Maintain strict schedules and adjust based on field data; prioritize critical valves.",
        entity_scope="Valves in process industries",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Site maintenance standard Section 5"
    ),
    DoctrineBlock(
        topic="Double Block and Bleed (DBB) Valve Configuration",
        keywords=["double block and bleed", "DBB", "valve configuration", "isolation", "API 6D"],
        conclusion_template="DBB valve configurations shall be used for critical isolation, ensuring zero leakage and safe maintenance per API 6D requirements.",
        reasoning_framework=(
            "1. Identify critical isolation points and process conditions.\n"
            "2. Select DBB valve configuration per API 6D.\n"
            "3. Validate compliance with manufacturer certifications.\n"
            "4. Factor in maintenance, inspection, and replacement schedules.\n"
            "5. Document selection and compliance.\n"
            "6. Review with safety and maintenance teams.\n"
            "7. Ensure traceability and certification for all DBB valves.\n"
            "8. Maintain records for regulatory audits.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on DBB valve maintenance."
        ),
        key_factors=[
            "Critical isolation",
            "DBB configuration",
            "Zero leakage",
            "Maintenance",
            "Certification"
        ],
        primary_authority=["API 6D", "Manufacturer DBB valve data"],
        burden_holder="Safety engineer",
        adversary_position="Non-DBB configurations may reduce cost but risk leakage.",
        counter_arguments=[
            "DBB valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit DBB use."
        ],
        resolution_strategy="Select DBB valves per API 6D and validate with third-party testing; maintain strict traceability.",
        entity_scope="Critical isolation valves in process industries",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 6D Section 4"
    ),
    DoctrineBlock(
        topic="Valve Selection for Abrasive Service",
        keywords=["valve selection", "abrasive service", "erosion", "material", "hard trim"],
        conclusion_template="Valves for abrasive service shall be selected with hard trim materials and erosion-resistant designs to ensure long-term reliability.",
        reasoning_framework=(
            "1. Identify process conditions: particle concentration, velocity, and fluid properties.\n"
            "2. Select valve types and trims designed for abrasive service.\n"
            "3. Validate material compatibility and erosion resistance.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Particle concentration",
            "Velocity",
            "Material resistance",
            "Trim design",
            "Maintenance"
        ],
        primary_authority=["Manufacturer data", "API 6A"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid erosion.",
        counter_arguments=[
            "Hard trim valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves with hard trim and validate with field data; maintain strict traceability.",
        entity_scope="Valves in abrasive service",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 6A Section 8"
    ),
    DoctrineBlock(
        topic="Valve Selection for Cryogenic Service",
        keywords=["valve selection", "cryogenic service", "low temperature", "material", "API 598"],
        conclusion_template="Valves for cryogenic service shall be selected with materials and designs suitable for low temperatures, ensuring compliance with API 598 and site standards.",
        reasoning_framework=(
            "1. Identify process temperature and pressure conditions.\n"
            "2. Select materials and designs certified for cryogenic service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification",
            "Maintenance"
        ],
        primary_authority=["API 598", "Manufacturer cryogenic valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk failure at low temperatures.",
        counter_arguments=[
            "Cryogenic valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 598 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in cryogenic service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 598 Section 7"
    ),
    DoctrineBlock(
        topic="Valve Selection for High Pressure Service",
        keywords=["valve selection", "high pressure", "pressure rating", "API 6A", "ASME B16.34"],
        conclusion_template="Valves for high pressure service shall be selected with appropriate pressure ratings and materials per API 6A and ASME B16.34.",
        reasoning_framework=(
            "1. Identify process pressure and temperature conditions.\n"
            "2. Select valve types and materials certified for high pressure service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Pressure",
            "Temperature",
            "Material compatibility",
            "Certification",
            "Maintenance"
        ],
        primary_authority=["API 6A", "ASME B16.34", "Manufacturer data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk failure at high pressure.",
        counter_arguments=[
            "High pressure valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 6A and ASME B16.34; validate with third-party testing and maintain strict traceability.",
        entity_scope="Valves in high pressure service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 6A Section 9"
    ),
    DoctrineBlock(
        topic="Valve Selection for High Temperature Service",
        keywords=["valve selection", "high temperature", "thermal", "material", "API 600"],
        conclusion_template="Valves for high temperature service shall be selected with materials and designs suitable for thermal extremes, ensuring compliance with API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process temperature and pressure conditions.\n"
            "2. Select materials and designs certified for high temperature service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer high temperature valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk failure at high temperature.",
        counter_arguments=[
            "High temperature valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in high temperature service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 8"
    ),
    DoctrineBlock(
        topic="Valve Selection for Corrosive Service",
        keywords=["valve selection", "corrosive service", "material", "corrosion", "NACE MR0175"],
        conclusion_template="Valves for corrosive service shall be selected with corrosion-resistant materials per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: corrosive agents, temperature, pressure.\n"
            "2. Select materials certified for corrosive service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Corrosive agents",
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "Manufacturer data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Corrosion-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in corrosive service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 3"
    ),
    DoctrineBlock(
        topic="Valve Selection for Slurry Service",
        keywords=["valve selection", "slurry service", "abrasive", "erosion", "hard trim"],
        conclusion_template="Valves for slurry service shall be selected with hard trim materials and erosion-resistant designs to ensure long-term reliability.",
        reasoning_framework=(
            "1. Identify process conditions: particle concentration, velocity, and fluid properties.\n"
            "2. Select valve types and trims designed for slurry service.\n"
            "3. Validate material compatibility and erosion resistance.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Particle concentration",
            "Velocity",
            "Material resistance",
            "Trim design",
            "Maintenance"
        ],
        primary_authority=["Manufacturer data", "API 6A"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid erosion.",
        counter_arguments=[
            "Hard trim valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves with hard trim and validate with field data; maintain strict traceability.",
        entity_scope="Valves in slurry service",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 6A Section 10"
    ),
    DoctrineBlock(
        topic="Valve Selection for Steam Service",
        keywords=["valve selection", "steam service", "thermal", "material", "API 600"],
        conclusion_template="Valves for steam service shall be selected with materials and designs suitable for thermal extremes and steam conditions, ensuring compliance with API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process temperature and pressure conditions.\n"
            "2. Select materials and designs certified for steam service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer steam valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk failure in steam service.",
        counter_arguments=[
            "Steam valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in steam service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 9"
    ),
    DoctrineBlock(
        topic="Valve Selection for Oxygen Service",
        keywords=["valve selection", "oxygen service", "cleanliness", "material", "fire risk"],
        conclusion_template="Valves for oxygen service shall be selected with materials and designs suitable for oxygen compatibility and fire risk, ensuring compliance with site standards.",
        reasoning_framework=(
            "1. Identify process conditions: oxygen concentration, pressure, temperature.\n"
            "2. Select materials certified for oxygen service and fire risk.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in cleaning and maintenance requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with safety and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance and cleaning."
        ),
        key_factors=[
            "Oxygen concentration",
            "Pressure",
            "Material compatibility",
            "Fire risk",
            "Maintenance"
        ],
        primary_authority=["Manufacturer data", "Site standards"],
        burden_holder="Safety engineer",
        adversary_position="Standard valves may reduce cost but risk fire or contamination.",
        counter_arguments=[
            "Oxygen-compatible valves are more expensive.",
            "Cleaning protocols may delay installation.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves with oxygen-compatible materials and validate with manufacturer data; maintain strict cleaning protocols.",
        entity_scope="Valves in oxygen service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Site oxygen valve standard Section 3"
    ),
    DoctrineBlock(
        topic="Valve Selection for Vacuum Service",
        keywords=["valve selection", "vacuum service", "leak tightness", "material", "API 600"],
        conclusion_template="Valves for vacuum service shall be selected with designs and materials suitable for leak tightness and vacuum compatibility, ensuring compliance with API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: vacuum level, pressure, temperature.\n"
            "2. Select valve types and materials certified for vacuum service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Vacuum level",
            "Pressure",
            "Material compatibility",
            "Leak tightness",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer vacuum valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk leakage in vacuum service.",
        counter_arguments=[
            "Vacuum valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in vacuum service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 10"
    ),
    DoctrineBlock(
        topic="Valve Selection for Food and Pharmaceutical Service",
        keywords=["valve selection", "food service", "pharmaceutical", "cleanliness", "material"],
        conclusion_template="Valves for food and pharmaceutical service shall be selected with materials and designs suitable for cleanliness and regulatory compliance.",
        reasoning_framework=(
            "1. Identify process conditions: cleanliness, pressure, temperature.\n"
            "2. Select materials certified for food and pharmaceutical service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in cleaning and maintenance requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with quality assurance and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for regulatory audits.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance and cleaning."
        ),
        key_factors=[
            "Cleanliness",
            "Pressure",
            "Material compatibility",
            "Regulatory compliance",
            "Maintenance"
        ],
        primary_authority=["FDA", "Manufacturer data"],
        burden_holder="Quality assurance engineer",
        adversary_position="Standard valves may reduce cost but risk contamination.",
        counter_arguments=[
            "Food/pharma valves are more expensive.",
            "Cleaning protocols may delay installation.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves with food/pharma-compatible materials and validate with manufacturer data; maintain strict cleaning protocols.",
        entity_scope="Valves in food and pharmaceutical service",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FDA valve standard Section 2"
    ),
    DoctrineBlock(
        topic="Valve Selection for Water Service",
        keywords=["valve selection", "water service", "material", "corrosion", "API 600"],
        conclusion_template="Valves for water service shall be selected with materials and designs suitable for corrosion resistance and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: water quality, pressure, temperature.\n"
            "2. Select materials certified for water service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Water quality",
            "Pressure",
            "Material compatibility",
            "Corrosion resistance",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer water valve data"],
        burden_holder="Maintenance engineer",
        adversary_position="Standard valves may reduce cost but risk corrosion.",
        counter_arguments=[
            "Corrosion-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in water service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 11"
    ),
    DoctrineBlock(
        topic="Valve Selection for Gas Service",
        keywords=["valve selection", "gas service", "material", "leak tightness", "API 600"],
        conclusion_template="Valves for gas service shall be selected with designs and materials suitable for leak tightness and gas compatibility, ensuring compliance with API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: gas type, pressure, temperature.\n"
            "2. Select valve types and materials certified for gas service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Gas type",
            "Pressure",
            "Material compatibility",
            "Leak tightness",
            "Maintenance"
        ],
        primary_authority=["API 600", "Manufacturer gas valve data"],
        burden_holder="Maintenance engineer",
        adversary_position="Standard valves may reduce cost but risk leakage.",
        counter_arguments=[
            "Gas valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in gas service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 12"
    ),
    DoctrineBlock(
        topic="Valve Selection for Chemical Service",
        keywords=["valve selection", "chemical service", "material", "corrosion", "NACE MR0175"],
        conclusion_template="Valves for chemical service shall be selected with corrosion-resistant materials per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: chemical agents, temperature, pressure.\n"
            "2. Select materials certified for chemical service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Chemical agents",
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "Manufacturer data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Chemical-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in chemical service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 4"
    ),
    DoctrineBlock(
        topic="Valve Selection for Hydrocarbon Service",
        keywords=["valve selection", "hydrocarbon service", "material", "fire-safe", "API 607"],
        conclusion_template="Valves for hydrocarbon service shall be selected with fire-safe designs and materials per API 607 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: hydrocarbon type, pressure, temperature.\n"
            "2. Select fire-safe valve designs and materials certified for hydrocarbon service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with safety and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Hydrocarbon type",
            "Pressure",
            "Material compatibility",
            "Fire-safe design",
            "Maintenance"
        ],
        primary_authority=["API 607", "Manufacturer hydrocarbon valve data"],
        burden_holder="Safety engineer",
        adversary_position="Standard valves may reduce cost but risk fire or leakage.",
        counter_arguments=[
            "Fire-safe valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 607 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in hydrocarbon service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 607 Section 5"
    ),
    DoctrineBlock(
        topic="Valve Selection for Acid Service",
        keywords=["valve selection", "acid service", "material", "corrosion", "NACE MR0175"],
        conclusion_template="Valves for acid service shall be selected with acid-resistant materials per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: acid type, concentration, temperature, pressure.\n"
            "2. Select materials certified for acid service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Acid type",
            "Concentration",
            "Temperature",
            "Pressure",
            "Material compatibility"
        ],
        primary_authority=["NACE MR0175", "Manufacturer acid valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Acid-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in acid service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 5"
    ),
    DoctrineBlock(
        topic="Valve Selection for Chlorine Service",
        keywords=["valve selection", "chlorine service", "material", "corrosion", "NACE MR0175"],
        conclusion_template="Valves for chlorine service shall be selected with chlorine-resistant materials per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: chlorine concentration, temperature, pressure.\n"
            "2. Select materials certified for chlorine service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Chlorine concentration",
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "Manufacturer chlorine valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Chlorine-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in chlorine service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 6"
    ),
    DoctrineBlock(
        topic="Valve Selection for Ammonia Service",
        keywords=["valve selection", "ammonia service", "material", "corrosion", "API 600"],
        conclusion_template="Valves for ammonia service shall be selected with ammonia-compatible materials and designs per API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: ammonia concentration, temperature, pressure.\n"
            "2. Select materials certified for ammonia service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Ammonia concentration",
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification"
        ],
        primary_authority=["API 600", "Manufacturer ammonia valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Ammonia-compatible valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in ammonia service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 13"
    ),
    DoctrineBlock(
        topic="Valve Selection for Hydrogen Service",
        keywords=["valve selection", "hydrogen service", "material", "leak tightness", "NACE MR0175"],
        conclusion_template="Valves for hydrogen service shall be selected with hydrogen-compatible materials and designs per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: hydrogen concentration, pressure, temperature.\n"
            "2. Select materials certified for hydrogen service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Hydrogen concentration",
            "Pressure",
            "Material compatibility",
            "Leak tightness",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "Manufacturer hydrogen valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk leakage or rapid corrosion.",
        counter_arguments=[
            "Hydrogen-compatible valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in hydrogen service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 7"
    ),
    DoctrineBlock(
        topic="Valve Selection for Nitrogen Service",
        keywords=["valve selection", "nitrogen service", "material", "leak tightness", "API 600"],
        conclusion_template="Valves for nitrogen service shall be selected with nitrogen-compatible materials and designs per API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: nitrogen concentration, pressure, temperature.\n"
            "2. Select materials certified for nitrogen service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Nitrogen concentration",
            "Pressure",
            "Material compatibility",
            "Leak tightness",
            "Certification"
        ],
        primary_authority=["API 600", "Manufacturer nitrogen valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk leakage.",
        counter_arguments=[
            "Nitrogen-compatible valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in nitrogen service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 14"
    ),
    DoctrineBlock(
        topic="Valve Selection for Sulfur Service",
        keywords=["valve selection", "sulfur service", "material", "corrosion", "NACE MR0175"],
        conclusion_template="Valves for sulfur service shall be selected with sulfur-resistant materials per NACE MR0175 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: sulfur concentration, temperature, pressure.\n"
            "2. Select materials certified for sulfur service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "Sulfur concentration",
            "Temperature",
            "Pressure",
            "Material compatibility",
            "Certification"
        ],
        primary_authority=["NACE MR0175", "Manufacturer sulfur valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "Sulfur-resistant valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per NACE MR0175 and validate with third-party testing; maintain strict traceability.",
        entity_scope="Valves in sulfur service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 8"
    ),
    DoctrineBlock(
        topic="Valve Selection for CO2 Service",
        keywords=["valve selection", "CO2 service", "material", "corrosion", "API 600"],
        conclusion_template="Valves for CO2 service shall be selected with CO2-compatible materials and designs per API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: CO2 concentration, pressure, temperature.\n"
            "2. Select materials certified for CO2 service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with materials and maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis.\n"
            "9. Monitor valve performance and adjust as needed.\n"
            "10. Train operators on proper maintenance."
        ),
        key_factors=[
            "CO2 concentration",
            "Pressure",
            "Material compatibility",
            "Corrosion resistance",
            "Certification"
        ],
        primary_authority=["API 600", "Manufacturer CO2 valve data"],
        burden_holder="Materials engineer",
        adversary_position="Standard valves may reduce cost but risk rapid corrosion.",
        counter_arguments=[
            "CO2-compatible valves are more expensive.",
            "Maintenance may be more frequent.",
            "Site-specific conditions may limit options."
        ],
        resolution_strategy="Select valves per API 600 and validate with manufacturer data; maintain strict traceability.",
        entity_scope="Valves in CO2 service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 600 Section 15"
    ),
    DoctrineBlock(
        topic="Valve Selection for Wastewater Service",
        keywords=["valve selection", "wastewater service", "material", "corrosion", "API 600"],
        conclusion_template="Valves for wastewater service shall be selected with corrosion-resistant materials and designs per API 600 and site standards.",
        reasoning_framework=(
            "1. Identify process conditions: wastewater composition, pressure, temperature.\n"
            "2. Select materials certified for wastewater service.\n"
            "3. Validate compatibility with manufacturer certifications.\n"
            "4. Factor in maintenance and inspection requirements.\n"
            "5. Document selection rationale and compliance.\n"
            "6. Review with maintenance teams.\n"
            "7. Ensure traceability and certification for all valve components.\n"
            "8. Maintain records for reliability analysis