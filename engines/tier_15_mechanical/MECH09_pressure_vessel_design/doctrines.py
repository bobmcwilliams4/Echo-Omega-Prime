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
        topic="ASME Section VIII Division 1 Shell Thickness Calculation",
        keywords=["shell thickness", "ASME VIII-1", "pressure vessel", "design", "minimum thickness"],
        conclusion_template="The minimum required shell thickness for a pressure vessel shall be calculated per ASME Section VIII Division 1, considering internal pressure, corrosion allowance, and manufacturing tolerances.",
        reasoning_framework=(
            "1. Identify vessel internal design pressure and diameter.\n"
            "2. Select material and determine allowable stress per ASME VIII-1.\n"
            "3. Apply formula: t = (P*R)/(SE-0.6P) + CA, where P=pressure, R=radius, S=allowable stress, E=weld efficiency, CA=corrosion allowance.\n"
            "4. Factor in minimum thickness requirements per UG-16.\n"
            "5. Consider manufacturing tolerances and joint efficiency.\n"
            "6. Validate against code minimums and adjust for corrosion allowance.\n"
            "7. Document calculations and reference material properties.\n"
            "8. Ensure compliance with ASME VIII-1 and local regulations.\n"
            "9. Review by qualified engineer.\n"
            "10. Update design as necessary based on feedback or changes in service conditions."
        ),
        key_factors=[
            "Design pressure",
            "Internal diameter",
            "Material allowable stress",
            "Corrosion allowance",
            "Weld efficiency",
            "Manufacturing tolerances",
            "Code minimum thickness"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-27", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Shell thickness may be over-conservative, increasing cost and weight.",
        counter_arguments=[
            "Safety margin is necessary for long-term reliability.",
            "Code minimums are based on historical failure data.",
            "Reduced thickness may compromise vessel integrity."
        ],
        resolution_strategy="Apply ASME VIII-1 formulas and document rationale for selected thickness; review with safety and cost optimization in mind.",
        entity_scope="Pressure vessel shell design",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-27"
    ),
    DoctrineBlock(
        topic="Ellipsoidal Head Design per ASME VIII-1",
        keywords=["ellipsoidal head", "ASME VIII-1", "pressure vessel", "head thickness", "design"],
        conclusion_template="Ellipsoidal heads shall be designed per ASME Section VIII Division 1, using the prescribed formulas for thickness and allowable stress.",
        reasoning_framework=(
            "1. Determine vessel internal pressure and head diameter.\n"
            "2. Select material and allowable stress from ASME Section II.\n"
            "3. Use ASME VIII-1 formula: t = (P*D)/(2SE-0.2P), where D=diameter, S=allowable stress, E=weld efficiency.\n"
            "4. Include corrosion allowance and manufacturing tolerances.\n"
            "5. Validate minimum thickness per UG-16 and code requirements.\n"
            "6. Consider elliptical ratio (2:1 is standard).\n"
            "7. Document calculations and reference material properties.\n"
            "8. Review design for manufacturability and compliance."
        ),
        key_factors=[
            "Internal pressure",
            "Head diameter",
            "Material allowable stress",
            "Corrosion allowance",
            "Weld efficiency",
            "Elliptical ratio"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-32(c)", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Ellipsoidal heads may be less efficient than hemispherical heads.",
        counter_arguments=[
            "Ellipsoidal heads are easier to fabricate and cost-effective.",
            "ASME formulas ensure adequate safety margins.",
            "Hemispherical heads require more material and higher cost."
        ],
        resolution_strategy="Apply ASME VIII-1 formulas for ellipsoidal heads; optimize for cost and manufacturability.",
        entity_scope="Pressure vessel head design",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-32(c)"
    ),
    DoctrineBlock(
        topic="Hemispherical Head Design - Most Efficient Geometry",
        keywords=["hemispherical head", "pressure vessel", "ASME VIII-1", "head thickness", "geometry"],
        conclusion_template="Hemispherical heads are the most efficient geometry for pressure vessels, requiring the least thickness for a given pressure and diameter.",
        reasoning_framework=(
            "1. Assess vessel internal pressure and diameter.\n"
            "2. Select material and allowable stress per ASME Section II.\n"
            "3. Use ASME VIII-1 formula: t = (P*R)/(2SE-0.2P), where R=radius, S=allowable stress, E=weld efficiency.\n"
            "4. Include corrosion allowance and manufacturing tolerances.\n"
            "5. Validate minimum thickness per UG-16.\n"
            "6. Consider fabrication complexity and cost.\n"
            "7. Document calculations and reference material properties.\n"
            "8. Review design for compliance and efficiency."
        ),
        key_factors=[
            "Internal pressure",
            "Head diameter",
            "Material allowable stress",
            "Corrosion allowance",
            "Weld efficiency",
            "Fabrication complexity"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-32(d)", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Hemispherical heads are more expensive to fabricate.",
        counter_arguments=[
            "Efficiency in material usage offsets fabrication cost.",
            "Hemispherical heads provide superior stress distribution.",
            "Long-term reliability justifies initial investment."
        ],
        resolution_strategy="Select hemispherical heads for high-pressure applications; balance efficiency and cost.",
        entity_scope="Pressure vessel head design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-32(d)"
    ),
    DoctrineBlock(
        topic="Torispherical Head Design (ASME F&D Head)",
        keywords=["torispherical head", "ASME F&D", "pressure vessel", "head thickness", "design"],
        conclusion_template="Torispherical heads (ASME Flanged and Dished) shall be designed per ASME Section VIII Division 1, using prescribed formulas for thickness and allowable stress.",
        reasoning_framework=(
            "1. Determine vessel internal pressure and head diameter.\n"
            "2. Select material and allowable stress from ASME Section II.\n"
            "3. Use ASME VIII-1 formula: t = (P*D)/(SE-0.2P), where D=diameter, S=allowable stress, E=weld efficiency.\n"
            "4. Include corrosion allowance and manufacturing tolerances.\n"
            "5. Validate minimum thickness per UG-16.\n"
            "6. Consider standard F&D geometry (crown radius = D, knuckle radius = 0.06D).\n"
            "7. Document calculations and reference material properties.\n"
            "8. Review design for manufacturability and compliance."
        ),
        key_factors=[
            "Internal pressure",
            "Head diameter",
            "Material allowable stress",
            "Corrosion allowance",
            "Weld efficiency",
            "F&D geometry"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-32(e)", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Torispherical heads may require thicker material than ellipsoidal heads.",
        counter_arguments=[
            "Torispherical heads are easier to fabricate.",
            "Standard geometry simplifies manufacturing.",
            "ASME formulas ensure safety and reliability."
        ],
        resolution_strategy="Apply ASME VIII-1 formulas for F&D heads; optimize for manufacturability.",
        entity_scope="Pressure vessel head design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-32(e)"
    ),
    DoctrineBlock(
        topic="Nozzle Reinforcement - Area Replacement Method",
        keywords=["nozzle reinforcement", "area replacement", "ASME VIII-1", "pressure vessel", "design"],
        conclusion_template="Nozzle reinforcement shall be calculated using the area replacement method per ASME Section VIII Division 1, ensuring the required area is provided to compensate for material removed.",
        reasoning_framework=(
            "1. Identify nozzle size, location, and vessel wall thickness.\n"
            "2. Calculate area removed by the nozzle opening.\n"
            "3. Determine required reinforcement area per ASME VIII-1 Appendix 1.\n"
            "4. Evaluate available reinforcement from nozzle, vessel wall, and added pads.\n"
            "5. Ensure reinforcement is within code limits and does not exceed maximum allowable.\n"
            "6. Document calculations and reference material properties.\n"
            "7. Review design for compliance and manufacturability."
        ),
        key_factors=[
            "Nozzle size",
            "Vessel wall thickness",
            "Material allowable stress",
            "Reinforcement pad dimensions",
            "Code limits"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-37", "ASME Section VIII Division 1 Appendix 1"],
        burden_holder="Design Engineer",
        adversary_position="Area replacement method may not account for complex stress distributions.",
        counter_arguments=[
            "ASME method is conservative and widely accepted.",
            "Finite element analysis can supplement if needed.",
            "Code compliance is mandatory for registration."
        ],
        resolution_strategy="Apply area replacement method per ASME VIII-1; supplement with analysis if required.",
        entity_scope="Pressure vessel nozzle design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-37"
    ),
    DoctrineBlock(
        topic="ASME Section VIII Division 2 - Design by Analysis",
        keywords=["ASME VIII-2", "design by analysis", "pressure vessel", "finite element", "stress analysis"],
        conclusion_template="Design by analysis per ASME Section VIII Division 2 requires detailed stress analysis, including linear and nonlinear methods, to demonstrate compliance with allowable limits.",
        reasoning_framework=(
            "1. Identify vessel geometry, loading conditions, and material properties.\n"
            "2. Develop finite element model representing vessel and attachments.\n"
            "3. Apply internal and external loads, including pressure, temperature, and wind/seismic.\n"
            "4. Perform linear elastic analysis for primary stresses.\n"
            "5. Conduct nonlinear analysis for plasticity and creep if required.\n"
            "6. Compare calculated stresses to allowable limits in ASME VIII-2.\n"
            "7. Document analysis methodology, assumptions, and results.\n"
            "8. Review by qualified engineer and submit for code compliance."
        ),
        key_factors=[
            "Vessel geometry",
            "Loading conditions",
            "Material properties",
            "Finite element modeling",
            "Code allowable limits"
        ],
        primary_authority=["ASME Section VIII Division 2 Part 5", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Design by analysis is more complex and costly than design by rules.",
        counter_arguments=[
            "Allows for optimized designs and reduced material usage.",
            "Necessary for non-standard geometries and high-pressure vessels.",
            "Provides detailed insight into stress distributions."
        ],
        resolution_strategy="Apply design by analysis for complex vessels; document and validate results per ASME VIII-2.",
        entity_scope="Pressure vessel advanced design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 2 Part 5"
    ),
    DoctrineBlock(
        topic="Maximum Allowable Working Pressure (MAWP) Calculation",
        keywords=["MAWP", "maximum allowable working pressure", "pressure vessel", "ASME VIII-1", "calculation"],
        conclusion_template="MAWP shall be calculated based on the minimum thickness and material properties, per ASME Section VIII Division 1, and stamped on the vessel nameplate.",
        reasoning_framework=(
            "1. Identify minimum thickness of vessel components.\n"
            "2. Select material and allowable stress per ASME Section II.\n"
            "3. Use ASME VIII-1 formulas to calculate MAWP for shell, heads, and nozzles.\n"
            "4. Include corrosion allowance and manufacturing tolerances.\n"
            "5. Validate against code minimums and safety margins.\n"
            "6. Document calculations and reference material properties.\n"
            "7. Stamp MAWP on vessel nameplate per ASME requirements."
        ),
        key_factors=[
            "Minimum thickness",
            "Material allowable stress",
            "Corrosion allowance",
            "Weld efficiency",
            "Code formulas"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-98", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="MAWP may be limited by weakest component.",
        counter_arguments=[
            "Ensures overall vessel safety.",
            "Code requires MAWP based on minimum thickness.",
            "Allows for clear identification of vessel limits."
        ],
        resolution_strategy="Calculate MAWP per ASME VIII-1; document and stamp on vessel.",
        entity_scope="Pressure vessel certification",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 1 UG-98"
    ),
    DoctrineBlock(
        topic="Hydrostatic Testing Requirements per ASME VIII-1",
        keywords=["hydrostatic test", "ASME VIII-1", "pressure vessel", "testing", "code compliance"],
        conclusion_template="Hydrostatic testing shall be performed per ASME Section VIII Division 1, at a pressure not less than 1.3 times the MAWP, to verify vessel integrity.",
        reasoning_framework=(
            "1. Determine MAWP and test pressure per ASME VIII-1 UG-99.\n"
            "2. Prepare vessel for testing, including venting and draining provisions.\n"
            "3. Fill vessel with water and apply test pressure.\n"
            "4. Inspect for leaks, deformation, and other defects.\n"
            "5. Maintain test pressure for required duration.\n"
            "6. Document test results and corrective actions.\n"
            "7. Review by qualified inspector and submit for code compliance."
        ),
        key_factors=[
            "MAWP",
            "Test pressure",
            "Test medium",
            "Inspection procedures",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-99", "ASME Section VIII Division 1 UG-100"],
        burden_holder="Manufacturer",
        adversary_position="Hydrostatic testing may not detect all defects.",
        counter_arguments=[
            "Hydrostatic test is a code requirement and industry standard.",
            "Supplementary NDE can be used for additional assurance.",
            "Test pressure provides safety margin."
        ],
        resolution_strategy="Perform hydrostatic test per ASME VIII-1; supplement with NDE as needed.",
        entity_scope="Pressure vessel testing",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 1 UG-99"
    ),
    DoctrineBlock(
        topic="Saddle Support Design Using Zick Analysis",
        keywords=["saddle support", "Zick analysis", "pressure vessel", "support design", "ASME VIII-1"],
        conclusion_template="Saddle supports shall be designed using Zick analysis to ensure adequate support and minimize local stresses in horizontal pressure vessels.",
        reasoning_framework=(
            "1. Identify vessel diameter, length, and weight.\n"
            "2. Determine number and location of saddles.\n"
            "3. Apply Zick analysis to calculate local shell stresses under saddle loads.\n"
            "4. Evaluate bending moments and stress concentrations.\n"
            "5. Design saddle geometry for load distribution and stability.\n"
            "6. Validate against ASME VIII-1 and local codes.\n"
            "7. Document calculations and review design for compliance."
        ),
        key_factors=[
            "Vessel diameter",
            "Vessel length",
            "Saddle location",
            "Shell thickness",
            "Load distribution"
        ],
        primary_authority=["ASME Section VIII Division 1", "Zick's Saddle Support Analysis"],
        burden_holder="Design Engineer",
        adversary_position="Zick analysis may not account for dynamic loads or seismic events.",
        counter_arguments=[
            "Supplement with ASCE 7 for wind/seismic loads.",
            "Zick analysis is industry standard for static loads.",
            "Dynamic loads can be addressed with additional supports."
        ],
        resolution_strategy="Apply Zick analysis for static loads; supplement with ASCE 7 for dynamic loads.",
        entity_scope="Pressure vessel support design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Zick's Saddle Support Analysis"
    ),
    DoctrineBlock(
        topic="Material Selection - Carbon Steel SA-516 Grade 70",
        keywords=["material selection", "carbon steel", "SA-516 Grade 70", "pressure vessel", "ASME II"],
        conclusion_template="Carbon steel SA-516 Grade 70 is a preferred material for pressure vessel shells and heads, offering high strength and good weldability.",
        reasoning_framework=(
            "1. Assess service conditions, including pressure, temperature, and corrosion.\n"
            "2. Review material properties in ASME Section II Part D.\n"
            "3. Confirm SA-516 Grade 70 meets design requirements for strength and toughness.\n"
            "4. Evaluate weldability and fabrication considerations.\n"
            "5. Validate material selection against code and client specifications.\n"
            "6. Document rationale for material selection."
        ),
        key_factors=[
            "Service conditions",
            "Material strength",
            "Weldability",
            "Code compliance",
            "Cost"
        ],
        primary_authority=["ASME Section II Part D", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="SA-516 Grade 70 may not be suitable for low-temperature service.",
        counter_arguments=[
            "Impact testing can qualify material for low temperatures.",
            "Alternative materials (e.g., SA-203) may be used for cryogenic service.",
            "SA-516 Grade 70 is widely used and cost-effective."
        ],
        resolution_strategy="Select SA-516 Grade 70 for standard service; qualify for low temperatures as needed.",
        entity_scope="Pressure vessel material selection",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section II Part D"
    ),
    DoctrineBlock(
        topic="Stainless Steel SA-240 Type 304/316 for Pressure Vessels",
        keywords=["stainless steel", "SA-240", "Type 304", "Type 316", "pressure vessel", "ASME II"],
        conclusion_template="Stainless steel SA-240 Type 304/316 is suitable for pressure vessels requiring corrosion resistance, per ASME Section II Part D.",
        reasoning_framework=(
            "1. Assess service conditions, including corrosive environment and temperature.\n"
            "2. Review material properties in ASME Section II Part D.\n"
            "3. Confirm SA-240 Type 304/316 meets design requirements for corrosion resistance and strength.\n"
            "4. Evaluate weldability and fabrication considerations.\n"
            "5. Validate material selection against code and client specifications.\n"
            "6. Document rationale for material selection."
        ),
        key_factors=[
            "Corrosive environment",
            "Material strength",
            "Weldability",
            "Code compliance",
            "Cost"
        ],
        primary_authority=["ASME Section II Part D", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Stainless steel may be more expensive and difficult to fabricate.",
        counter_arguments=[
            "Corrosion resistance justifies higher cost.",
            "SA-240 is widely used for chemical and food industries.",
            "Weldability is good with proper procedures."
        ],
        resolution_strategy="Select SA-240 Type 304/316 for corrosive service; optimize fabrication methods.",
        entity_scope="Pressure vessel material selection",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section II Part D"
    ),
    DoctrineBlock(
        topic="Post-Weld Heat Treatment (PWHT) Requirements",
        keywords=["PWHT", "post-weld heat treatment", "pressure vessel", "ASME VIII-1", "fabrication"],
        conclusion_template="PWHT shall be performed per ASME Section VIII Division 1, based on material thickness, type, and service conditions, to relieve residual stresses and improve toughness.",
        reasoning_framework=(
            "1. Identify material type and thickness.\n"
            "2. Review ASME VIII-1 requirements for PWHT (UCS-56, UHA-32, etc.).\n"
            "3. Determine necessity based on weld type and service conditions.\n"
            "4. Specify PWHT temperature and duration per code.\n"
            "5. Document PWHT procedure and verify compliance.\n"
            "6. Review by qualified inspector."
        ),
        key_factors=[
            "Material type",
            "Thickness",
            "Weld type",
            "Service conditions",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1 UCS-56", "ASME Section VIII Division 1 UHA-32"],
        burden_holder="Fabricator",
        adversary_position="PWHT may increase fabrication time and cost.",
        counter_arguments=[
            "PWHT improves weld quality and vessel reliability.",
            "Code requires PWHT for certain thicknesses and materials.",
            "Skipping PWHT may compromise vessel integrity."
        ],
        resolution_strategy="Perform PWHT as required by ASME VIII-1; document procedures and results.",
        entity_scope="Pressure vessel fabrication",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UCS-56"
    ),
    DoctrineBlock(
        topic="Non-Destructive Examination (NDE) Requirements",
        keywords=["NDE", "non-destructive examination", "pressure vessel", "ASME VIII-1", "inspection"],
        conclusion_template="NDE shall be performed per ASME Section VIII Division 1, including radiography, ultrasonic, and magnetic particle testing, to verify weld integrity.",
        reasoning_framework=(
            "1. Identify weld types and critical areas.\n"
            "2. Review ASME VIII-1 requirements for NDE (UW-11, UW-12, etc.).\n"
            "3. Select appropriate NDE methods based on material and geometry.\n"
            "4. Perform examinations per code procedures.\n"
            "5. Document results and corrective actions.\n"
            "6. Review by qualified inspector and submit for code compliance."
        ),
        key_factors=[
            "Weld type",
            "Material",
            "Geometry",
            "Code requirements",
            "Inspector qualifications"
        ],
        primary_authority=["ASME Section VIII Division 1 UW-11", "ASME Section VIII Division 1 UW-12"],
        burden_holder="Fabricator",
        adversary_position="NDE may increase fabrication time and cost.",
        counter_arguments=[
            "NDE ensures weld quality and vessel safety.",
            "Code requires NDE for critical welds.",
            "Skipping NDE may compromise vessel integrity."
        ],
        resolution_strategy="Perform NDE as required by ASME VIII-1; document procedures and results.",
        entity_scope="Pressure vessel inspection",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 1 UW-11"
    ),
    DoctrineBlock(
        topic="API 510 In-Service Inspection and Remaining Life Assessment",
        keywords=["API 510", "in-service inspection", "pressure vessel", "remaining life", "assessment"],
        conclusion_template="In-service inspection and remaining life assessment shall be performed per API 510, including thickness measurements, NDE, and fitness-for-service evaluation.",
        reasoning_framework=(
            "1. Review vessel history and previous inspection reports.\n"
            "2. Perform thickness measurements and compare to minimum required.\n"
            "3. Conduct NDE to detect flaws and corrosion.\n"
            "4. Apply API 510 remaining life formulas: Remaining Life = (Current Thickness - Minimum Required Thickness) / Corrosion Rate.\n"
            "5. Evaluate fitness-for-service per API 579-1/ASME FFS-1 if defects are found.\n"
            "6. Document inspection results and recommended actions.\n"
            "7. Schedule next inspection based on risk assessment."
        ),
        key_factors=[
            "Current thickness",
            "Minimum required thickness",
            "Corrosion rate",
            "NDE results",
            "Inspection history"
        ],
        primary_authority=["API 510", "API 579-1/ASME FFS-1"],
        burden_holder="Owner/User",
        adversary_position="Inspection intervals may be too conservative.",
        counter_arguments=[
            "Risk-based inspection can optimize intervals.",
            "API 510 provides minimum requirements for safety.",
            "Frequent inspections reduce risk of failure."
        ],
        resolution_strategy="Apply API 510 and risk-based inspection; document rationale for intervals.",
        entity_scope="Pressure vessel in-service inspection",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 510"
    ),
    DoctrineBlock(
        topic="Fitness-for-Service Assessment per API 579-1/ASME FFS-1",
        keywords=["fitness-for-service", "API 579-1", "ASME FFS-1", "pressure vessel", "assessment"],
        conclusion_template="Fitness-for-service assessment shall be performed per API 579-1/ASME FFS-1, evaluating flaws, corrosion, and mechanical damage to determine vessel suitability for continued operation.",
        reasoning_framework=(
            "1. Identify flaws, corrosion, or mechanical damage from inspection.\n"
            "2. Review API 579-1/ASME FFS-1 assessment procedures.\n"
            "3. Perform Level 1, 2, or 3 assessment based on severity and complexity.\n"
            "4. Calculate remaining strength and life using code formulas.\n"
            "5. Recommend repair, replacement, or continued operation based on results.\n"
            "6. Document assessment and submit for review."
        ),
        key_factors=[
            "Flaw size and location",
            "Corrosion rate",
            "Material properties",
            "Assessment level",
            "Code requirements"
        ],
        primary_authority=["API 579-1/ASME FFS-1"],
        burden_holder="Owner/User",
        adversary_position="Fitness-for-service may allow operation with reduced safety margin.",
        counter_arguments=[
            "Assessment is rigorous and code-based.",
            "Allows for continued operation with risk mitigation.",
            "Provides clear criteria for repair or replacement."
        ],
        resolution_strategy="Perform fitness-for-service assessment per API 579-1/ASME FFS-1; document and review results.",
        entity_scope="Pressure vessel in-service assessment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 579-1/ASME FFS-1"
    ),
    DoctrineBlock(
        topic="Oilfield Production Vessels per API 12F and 12J",
        keywords=["oilfield production vessel", "API 12F", "API 12J", "pressure vessel", "design"],
        conclusion_template="Oilfield production vessels shall be designed and fabricated per API 12F and 12J, considering standard dimensions, materials, and code requirements.",
        reasoning_framework=(
            "1. Review API 12F and 12J standard vessel dimensions and configurations.\n"
            "2. Select materials and thicknesses per API and ASME requirements.\n"
            "3. Apply standard fabrication and inspection procedures.\n"
            "4. Validate design against API and ASME codes.\n"
            "5. Document design and fabrication for client and regulatory review."
        ),
        key_factors=[
            "Standard vessel dimensions",
            "Material selection",
            "Fabrication procedures",
            "Inspection requirements",
            "Code compliance"
        ],
        primary_authority=["API 12F", "API 12J", "ASME Section VIII Division 1"],
        burden_holder="Manufacturer",
        adversary_position="Standard vessels may not meet unique site requirements.",
        counter_arguments=[
            "Custom modifications can be made as needed.",
            "API standards ensure reliability and safety.",
            "Standardization reduces cost and lead time."
        ],
        resolution_strategy="Design per API 12F/12J; customize as required for site conditions.",
        entity_scope="Oilfield production vessel design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 12F"
    ),
    DoctrineBlock(
        topic="Wind and Seismic Loads per ASCE 7",
        keywords=["wind load", "seismic load", "ASCE 7", "pressure vessel", "external loads"],
        conclusion_template="Wind and seismic loads shall be considered in pressure vessel design per ASCE 7, ensuring stability and integrity under external forces.",
        reasoning_framework=(
            "1. Identify site location and applicable wind/seismic zones.\n"
            "2. Review ASCE 7 load requirements and factors.\n"
            "3. Calculate wind and seismic loads based on vessel geometry and site conditions.\n"
            "4. Design supports and anchorage to resist calculated loads.\n"
            "5. Validate design against ASME and local codes.\n"
            "6. Document calculations and review design for compliance."
        ),
        key_factors=[
            "Site location",
            "Wind/seismic zone",
            "Vessel geometry",
            "Support design",
            "Code requirements"
        ],
        primary_authority=["ASCE 7", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Wind/seismic loads may increase design complexity and cost.",
        counter_arguments=[
            "External loads are critical for vessel stability.",
            "ASCE 7 provides standardized load calculations.",
            "Ignoring loads may result in catastrophic failure."
        ],
        resolution_strategy="Apply ASCE 7 load calculations; optimize support design for cost and safety.",
        entity_scope="Pressure vessel external load design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASCE 7"
    ),
    DoctrineBlock(
        topic="National Board Registration and R-Stamp",
        keywords=["National Board", "registration", "R-Stamp", "pressure vessel", "repair", "certification"],
        conclusion_template="Pressure vessels shall be registered with the National Board and repairs performed under an R-Stamp, ensuring traceability and code compliance.",
        reasoning_framework=(
            "1. Complete fabrication per ASME VIII-1 and obtain Manufacturer's Data Report.\n"
            "2. Submit vessel for National Board registration.\n"
            "3. For repairs, engage R-Stamp certified contractor.\n"
            "4. Document repair procedures and submit for review.\n"
            "5. Maintain records for regulatory compliance and traceability."
        ),
        key_factors=[
            "Fabrication records",
            "Repair procedures",
            "Certification",
            "Regulatory compliance",
            "Traceability"
        ],
        primary_authority=["National Board Inspection Code", "ASME Section VIII Division 1"],
        burden_holder="Manufacturer/Repair Contractor",
        adversary_position="Registration and R-Stamp may increase administrative burden.",
        counter_arguments=[
            "Ensures vessel traceability and compliance.",
            "Required for legal operation and insurance.",
            "Provides assurance of quality repairs."
        ],
        resolution_strategy="Register vessels and repairs per National Board requirements; maintain documentation.",
        entity_scope="Pressure vessel certification and repair",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="National Board Inspection Code"
    ),
    DoctrineBlock(
        topic="Corrosion Allowance Selection and Design Life",
        keywords=["corrosion allowance", "design life", "pressure vessel", "ASME VIII-1", "material selection"],
        conclusion_template="Corrosion allowance shall be selected based on expected service conditions and desired design life, per ASME Section VIII Division 1 recommendations.",
        reasoning_framework=(
            "1. Assess service environment and expected corrosion rate.\n"
            "2. Review ASME VIII-1 recommendations for minimum corrosion allowance.\n"
            "3. Calculate required allowance for desired design life.\n"
            "4. Factor in inspection and maintenance intervals.\n"
            "5. Document rationale for selected corrosion allowance."
        ),
        key_factors=[
            "Service environment",
            "Corrosion rate",
            "Design life",
            "Inspection intervals",
            "Code recommendations"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-16", "API 510"],
        burden_holder="Design Engineer",
        adversary_position="Excessive corrosion allowance increases material cost.",
        counter_arguments=[
            "Adequate allowance ensures long-term reliability.",
            "Code minimums are based on historical data.",
            "Optimized allowance balances cost and safety."
        ],
        resolution_strategy="Select corrosion allowance per ASME VIII-1 and service conditions; document rationale.",
        entity_scope="Pressure vessel material selection",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-16"
    ),
    DoctrineBlock(
        topic="Minimum Design Metal Temperature (MDMT) and Impact Testing",
        keywords=["MDMT", "minimum design metal temperature", "impact testing", "ASME VIII-1", "pressure vessel"],
        conclusion_template="MDMT and impact testing requirements shall be determined per ASME Section VIII Division 1, ensuring material toughness at low temperatures.",
        reasoning_framework=(
            "1. Identify minimum service temperature and material type.\n"
            "2. Review ASME VIII-1 requirements for MDMT and impact testing (UG-84).\n"
            "3. Select materials qualified for MDMT or specify impact testing.\n"
            "4. Document test procedures and results.\n"
            "5. Review by qualified inspector and submit for code compliance."
        ),
        key_factors=[
            "Minimum service temperature",
            "Material toughness",
            "Impact test results",
            "Code requirements",
            "Inspector qualifications"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-84", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Impact testing adds cost and time to fabrication.",
        counter_arguments=[
            "Ensures vessel reliability at low temperatures.",
            "Code requires impact testing for certain materials and thicknesses.",
            "Skipping testing may compromise safety."
        ],
        resolution_strategy="Determine MDMT and perform impact testing per ASME VIII-1; document results.",
        entity_scope="Pressure vessel material qualification",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-84"
    ),
    DoctrineBlock(
        topic="Fabrication Tolerances per ASME VIII-1 UG-80 and UG-81",
        keywords=["fabrication tolerances", "ASME VIII-1", "UG-80", "UG-81", "pressure vessel"],
        conclusion_template="Fabrication tolerances shall be maintained per ASME Section VIII Division 1 UG-80 and UG-81, ensuring vessel geometry and integrity.",
        reasoning_framework=(
            "1. Review ASME VIII-1 UG-80 and UG-81 tolerance requirements for shell and head geometry.\n"
            "2. Specify allowable deviations for diameter, thickness, and roundness.\n"
            "3. Inspect fabricated vessel for compliance.\n"
            "4. Document inspection results and corrective actions.\n"
            "5. Submit for code compliance and review."
        ),
        key_factors=[
            "Diameter tolerance",
            "Thickness tolerance",
            "Roundness",
            "Code requirements",
            "Inspection procedures"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-80", "ASME Section VIII Division 1 UG-81"],
        burden_holder="Fabricator",
        adversary_position="Tight tolerances may increase fabrication cost.",
        counter_arguments=[
            "Ensures vessel integrity and code compliance.",
            "Tolerances are based on historical failure data.",
            "Optimized fabrication methods can reduce cost."
        ],
        resolution_strategy="Maintain tolerances per ASME VIII-1; document inspection and corrective actions.",
        entity_scope="Pressure vessel fabrication",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-80"
    ),
    DoctrineBlock(
        topic="Weld Joint Efficiency Determination",
        keywords=["weld joint efficiency", "ASME VIII-1", "pressure vessel", "weld type", "radiography"],
        conclusion_template="Weld joint efficiency shall be determined per ASME Section VIII Division 1, based on weld type and extent of radiographic examination.",
        reasoning_framework=(
            "1. Identify weld type (butt, lap, fillet, etc.) and location.\n"
            "2. Review ASME VIII-1 requirements for joint efficiency (UW-12).\n"
            "3. Specify radiographic examination extent.\n"
            "4. Assign joint efficiency value per code tables.\n"
            "5. Document rationale and inspection results."
        ),
        key_factors=[
            "Weld type",
            "Radiographic examination",
            "Code requirements",
            "Joint efficiency tables",
            "Inspection procedures"
        ],
        primary_authority=["ASME Section VIII Division 1 UW-12"],
        burden_holder="Design Engineer",
        adversary_position="Higher joint efficiency requires more extensive NDE.",
        counter_arguments=[
            "Higher efficiency allows for thinner vessel walls.",
            "Code requires minimum NDE for certain efficiencies.",
            "Optimized inspection balances cost and safety."
        ],
        resolution_strategy="Determine joint efficiency per ASME VIII-1; document inspection and rationale.",
        entity_scope="Pressure vessel weld design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UW-12"
    ),
    DoctrineBlock(
        topic="Design Pressure Selection and Safety Margin",
        keywords=["design pressure", "safety margin", "pressure vessel", "ASME VIII-1", "operating pressure"],
        conclusion_template="Design pressure shall be selected per ASME Section VIII Division 1, with appropriate safety margin above maximum operating pressure.",
        reasoning_framework=(
            "1. Identify maximum operating pressure and transient conditions.\n"
            "2. Review ASME VIII-1 recommendations for safety margin.\n"
            "3. Select design pressure to accommodate surges and upset conditions.\n"
            "4. Document rationale for selected design pressure.\n"
            "5. Validate against code and client requirements."
        ),
        key_factors=[
            "Maximum operating pressure",
            "Transient conditions",
            "Safety margin",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-98"],
        burden_holder="Design Engineer",
        adversary_position="Excessive safety margin increases material cost.",
        counter_arguments=[
            "Adequate margin ensures vessel reliability.",
            "Code minimums are based on historical failure data.",
            "Optimized margin balances cost and safety."
        ],
        resolution_strategy="Select design pressure per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel design",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-98"
    ),
    DoctrineBlock(
        topic="Pressure Relief Device Sizing per ASME VIII-1",
        keywords=["pressure relief", "device sizing", "ASME VIII-1", "pressure vessel", "safety valve"],
        conclusion_template="Pressure relief devices shall be sized per ASME Section VIII Division 1, ensuring adequate capacity to protect vessel from overpressure.",
        reasoning_framework=(
            "1. Identify maximum credible overpressure scenario.\n"
            "2. Review ASME VIII-1 requirements for relief device sizing (UG-125).\n"
            "3. Calculate required relief capacity based on vessel volume and process conditions.\n"
            "4. Select relief device type and set pressure.\n"
            "5. Document sizing calculations and device specifications."
        ),
        key_factors=[
            "Overpressure scenario",
            "Relief capacity",
            "Device type",
            "Set pressure",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-125"],
        burden_holder="Design Engineer",
        adversary_position="Oversized relief devices may cause nuisance trips.",
        counter_arguments=[
            "Proper sizing prevents vessel rupture.",
            "Code provides clear sizing criteria.",
            "Optimized sizing balances safety and operability."
        ],
        resolution_strategy="Size relief devices per ASME VIII-1; document calculations and device selection.",
        entity_scope="Pressure vessel safety",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 1 UG-125"
    ),
    DoctrineBlock(
        topic="External Pressure Design per ASME VIII-1",
        keywords=["external pressure", "vacuum", "pressure vessel", "ASME VIII-1", "buckling"],
        conclusion_template="Pressure vessels subjected to external pressure shall be designed per ASME Section VIII Division 1, considering buckling and collapse resistance.",
        reasoning_framework=(
            "1. Identify external pressure conditions and vessel geometry.\n"
            "2. Review ASME VIII-1 requirements for external pressure design (UG-28).\n"
            "3. Use code charts and formulas to calculate minimum thickness.\n"
            "4. Validate design against buckling and collapse criteria.\n"
            "5. Document calculations and review design for compliance."
        ),
        key_factors=[
            "External pressure",
            "Vessel geometry",
            "Material properties",
            "Buckling resistance",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-28"],
        burden_holder="Design Engineer",
        adversary_position="External pressure design may require thicker walls.",
        counter_arguments=[
            "Ensures vessel integrity under vacuum or external loads.",
            "Code provides conservative design criteria.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for external pressure per ASME VIII-1; document calculations.",
        entity_scope="Pressure vessel external pressure design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-28"
    ),
    DoctrineBlock(
        topic="Weld Overlay and Cladding for Corrosion Protection",
        keywords=["weld overlay", "cladding", "corrosion protection", "pressure vessel", "ASME VIII-1"],
        conclusion_template="Weld overlay and cladding may be used for corrosion protection in pressure vessels, per ASME Section VIII Division 1, with proper qualification and inspection.",
        reasoning_framework=(
            "1. Assess service environment and corrosion risk.\n"
            "2. Review ASME VIII-1 requirements for overlay and cladding (UCL-1).\n"
            "3. Select overlay/cladding material compatible with base metal.\n"
            "4. Specify welding procedures and qualification tests.\n"
            "5. Perform inspection and document results."
        ),
        key_factors=[
            "Corrosive environment",
            "Overlay/cladding material",
            "Welding procedures",
            "Inspection requirements",
            "Code compliance"
        ],
        primary_authority=["ASME Section VIII Division 1 UCL-1"],
        burden_holder="Fabricator",
        adversary_position="Overlay/cladding increases fabrication complexity.",
        counter_arguments=[
            "Provides long-term corrosion protection.",
            "Code requires qualification and inspection.",
            "Optimized procedures can reduce complexity."
        ],
        resolution_strategy="Apply overlay/cladding per ASME VIII-1; document qualification and inspection.",
        entity_scope="Pressure vessel corrosion protection",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UCL-1"
    ),
    DoctrineBlock(
        topic="Fatigue Analysis for Cyclic Service per ASME VIII-2",
        keywords=["fatigue analysis", "cyclic service", "ASME VIII-2", "pressure vessel", "design"],
        conclusion_template="Fatigue analysis shall be performed for pressure vessels in cyclic service per ASME Section VIII Division 2, evaluating stress ranges and cycle counts.",
        reasoning_framework=(
            "1. Identify cyclic loading conditions and expected number of cycles.\n"
            "2. Review ASME VIII-2 requirements for fatigue analysis (Part 5).\n"
            "3. Calculate stress ranges using finite element analysis.\n"
            "4. Compare calculated cycles to allowable per code charts.\n"
            "5. Document analysis and review design for compliance."
        ),
        key_factors=[
            "Cyclic loading",
            "Stress range",
            "Cycle count",
            "Material properties",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 2 Part 5"],
        burden_holder="Design Engineer",
        adversary_position="Fatigue analysis increases design complexity.",
        counter_arguments=[
            "Necessary for vessels in cyclic service.",
            "Code provides clear analysis procedures.",
            "Optimized design reduces risk of fatigue failure."
        ],
        resolution_strategy="Perform fatigue analysis per ASME VIII-2; document results.",
        entity_scope="Pressure vessel cyclic service",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 2 Part 5"
    ),
    DoctrineBlock(
        topic="Weld Repair Procedures per ASME VIII-1",
        keywords=["weld repair", "procedures", "ASME VIII-1", "pressure vessel", "fabrication"],
        conclusion_template="Weld repairs shall be performed per ASME Section VIII Division 1, following qualified procedures and inspection requirements.",
        reasoning_framework=(
            "1. Identify weld defects and repair scope.\n"
            "2. Review ASME VIII-1 requirements for weld repair (UW-35).\n"
            "3. Develop qualified repair procedures and obtain approval.\n"
            "4. Perform repair and inspect per code requirements.\n"
            "5. Document repair and submit for code compliance."
        ),
        key_factors=[
            "Defect type",
            "Repair procedure",
            "Inspection requirements",
            "Code compliance",
            "Documentation"
        ],
        primary_authority=["ASME Section VIII Division 1 UW-35"],
        burden_holder="Fabricator",
        adversary_position="Weld repair may compromise vessel integrity.",
        counter_arguments=[
            "Qualified procedures ensure repair quality.",
            "Code requires inspection and documentation.",
            "Repair is preferable to scrapping vessel."
        ],
        resolution_strategy="Perform weld repair per ASME VIII-1; document procedures and inspection.",
        entity_scope="Pressure vessel fabrication",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UW-35"
    ),
    DoctrineBlock(
        topic="Heat Exchanger Design per TEMA and ASME VIII-1",
        keywords=["heat exchanger", "TEMA", "ASME VIII-1", "pressure vessel", "design"],
        conclusion_template="Heat exchangers shall be designed per TEMA and ASME Section VIII Division 1, considering shell and tube configuration, materials, and code requirements.",
        reasoning_framework=(
            "1. Select heat exchanger type and configuration per TEMA standards.\n"
            "2. Review ASME VIII-1 requirements for pressure-containing components.\n"
            "3. Specify materials and thicknesses per code.\n"
            "4. Design for thermal and pressure loads.\n"
            "5. Document design and review for compliance."
        ),
        key_factors=[
            "Heat exchanger type",
            "Shell and tube configuration",
            "Material selection",
            "Thermal and pressure loads",
            "Code requirements"
        ],
        primary_authority=["TEMA", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="TEMA and ASME requirements may conflict.",
        counter_arguments=[
            "TEMA addresses thermal design; ASME addresses pressure integrity.",
            "Both standards are widely accepted.",
            "Design must comply with both for safety and performance."
        ],
        resolution_strategy="Design per TEMA and ASME VIII-1; resolve conflicts through engineering review.",
        entity_scope="Pressure vessel heat exchanger design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="TEMA"
    ),
    DoctrineBlock(
        topic="Design for Fire Exposure per API 521",
        keywords=["fire exposure", "API 521", "pressure vessel", "relief sizing", "emergency"],
        conclusion_template="Pressure vessels shall be designed for fire exposure scenarios per API 521, including relief device sizing and emergency procedures.",
        reasoning_framework=(
            "1. Identify credible fire exposure scenarios.\n"
            "2. Review API 521 requirements for relief device sizing under fire conditions.\n"
            "3. Calculate required relief capacity and set pressure.\n"
            "4. Document emergency procedures and device specifications.\n"
            "5. Review design for compliance and safety."
        ),
        key_factors=[
            "Fire exposure scenario",
            "Relief device sizing",
            "Emergency procedures",
            "Code requirements",
            "Documentation"
        ],
        primary_authority=["API 521", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Fire exposure scenarios may be rare.",
        counter_arguments=[
            "Code requires consideration for emergency events.",
            "Proper relief sizing prevents vessel rupture.",
            "Emergency procedures improve safety."
        ],
        resolution_strategy="Design for fire exposure per API 521; document relief sizing and procedures.",
        entity_scope="Pressure vessel emergency design",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 521"
    ),
    DoctrineBlock(
        topic="Design for Internal Pressure Surges",
        keywords=["internal pressure surge", "pressure vessel", "ASME VIII-1", "transient pressure"],
        conclusion_template="Pressure vessels shall be designed to withstand internal pressure surges, considering transient conditions and safety margin per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify potential pressure surge scenarios and magnitude.\n"
            "2. Review ASME VIII-1 requirements for transient pressure design.\n"
            "3. Select design pressure to accommodate surges.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Pressure surge scenario",
            "Transient pressure",
            "Safety margin",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-98"],
        burden_holder="Design Engineer",
        adversary_position="Design for surges may increase material cost.",
        counter_arguments=[
            "Ensures vessel reliability under upset conditions.",
            "Code requires consideration of transient pressures.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for pressure surges per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel transient design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-98"
    ),
    DoctrineBlock(
        topic="Design for Vacuum and Internal Collapse",
        keywords=["vacuum", "internal collapse", "pressure vessel", "ASME VIII-1", "external pressure"],
        conclusion_template="Pressure vessels shall be designed to withstand vacuum and internal collapse per ASME Section VIII Division 1, considering external pressure and buckling resistance.",
        reasoning_framework=(
            "1. Identify vacuum conditions and vessel geometry.\n"
            "2. Review ASME VIII-1 requirements for external pressure design (UG-28).\n"
            "3. Use code charts and formulas to calculate minimum thickness.\n"
            "4. Validate design against buckling and collapse criteria.\n"
            "5. Document calculations and review design for compliance."
        ),
        key_factors=[
            "Vacuum conditions",
            "Vessel geometry",
            "Material properties",
            "Buckling resistance",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-28"],
        burden_holder="Design Engineer",
        adversary_position="Vacuum design may require thicker walls.",
        counter_arguments=[
            "Ensures vessel integrity under vacuum.",
            "Code provides conservative design criteria.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for vacuum per ASME VIII-1; document calculations.",
        entity_scope="Pressure vessel vacuum design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-28"
    ),
    DoctrineBlock(
        topic="Design for Thermal Expansion and Contraction",
        keywords=["thermal expansion", "thermal contraction", "pressure vessel", "ASME VIII-1", "temperature effects"],
        conclusion_template="Pressure vessels shall be designed to accommodate thermal expansion and contraction, considering material properties and operating temperature range per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify operating temperature range and material properties.\n"
            "2. Review ASME VIII-1 requirements for thermal effects.\n"
            "3. Design expansion joints or allow for movement as needed.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Operating temperature range",
            "Material properties",
            "Expansion joints",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Thermal design increases complexity and cost.",
        counter_arguments=[
            "Ensures vessel reliability under temperature changes.",
            "Code requires consideration of thermal effects.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for thermal effects per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel thermal design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Cyclic Loading and Pressure Fluctuations",
        keywords=["cyclic loading", "pressure fluctuations", "fatigue", "ASME VIII-2", "pressure vessel"],
        conclusion_template="Pressure vessels subjected to cyclic loading and pressure fluctuations shall be designed per ASME Section VIII Division 2, including fatigue analysis and material selection.",
        reasoning_framework=(
            "1. Identify cyclic loading conditions and expected number of cycles.\n"
            "2. Review ASME VIII-2 requirements for fatigue analysis (Part 5).\n"
            "3. Select materials with adequate fatigue resistance.\n"
            "4. Document analysis and review design for compliance."
        ),
        key_factors=[
            "Cyclic loading",
            "Pressure fluctuations",
            "Fatigue resistance",
            "Material selection",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 2 Part 5"],
        burden_holder="Design Engineer",
        adversary_position="Fatigue analysis increases design complexity.",
        counter_arguments=[
            "Necessary for vessels in cyclic service.",
            "Code provides clear analysis procedures.",
            "Optimized design reduces risk of fatigue failure."
        ],
        resolution_strategy="Perform fatigue analysis per ASME VIII-2; document results.",
        entity_scope="Pressure vessel cyclic design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 2 Part 5"
    ),
    DoctrineBlock(
        topic="Design for External Loads (Wind, Seismic, Snow)",
        keywords=["external loads", "wind", "seismic", "snow", "ASCE 7", "pressure vessel"],
        conclusion_template="Pressure vessels shall be designed to resist external loads including wind, seismic, and snow per ASCE 7 and ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify site location and applicable external load conditions.\n"
            "2. Review ASCE 7 and ASME VIII-1 requirements for external loads.\n"
            "3. Calculate loads based on vessel geometry and site conditions.\n"
            "4. Design supports and anchorage to resist calculated loads.\n"
            "5. Document calculations and review design for compliance."
        ),
        key_factors=[
            "Site location",
            "External load conditions",
            "Vessel geometry",
            "Support design",
            "Code requirements"
        ],
        primary_authority=["ASCE 7", "ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="External load design increases complexity and cost.",
        counter_arguments=[
            "Ensures vessel stability and safety.",
            "Code provides standardized load calculations.",
            "Ignoring loads may result in catastrophic failure."
        ],
        resolution_strategy="Design for external loads per ASCE 7 and ASME VIII-1; document calculations.",
        entity_scope="Pressure vessel external load design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASCE 7"
    ),
    DoctrineBlock(
        topic="Design for High Temperature Service",
        keywords=["high temperature", "pressure vessel", "ASME VIII-1", "creep", "material selection"],
        conclusion_template="Pressure vessels for high temperature service shall be designed per ASME Section VIII Division 1, considering material properties, creep, and thermal effects.",
        reasoning_framework=(
            "1. Identify operating temperature and material properties.\n"
            "2. Review ASME VIII-1 requirements for high temperature service.\n"
            "3. Select materials with adequate high temperature strength and creep resistance.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Operating temperature",
            "Material properties",
            "Creep resistance",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="High temperature design increases material cost.",
        counter_arguments=[
            "Ensures vessel reliability under high temperature.",
            "Code requires consideration of creep and thermal effects.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for high temperature per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel high temperature design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Low Temperature and Cryogenic Service",
        keywords=["low temperature", "cryogenic", "pressure vessel", "ASME VIII-1", "material selection"],
        conclusion_template="Pressure vessels for low temperature and cryogenic service shall be designed per ASME Section VIII Division 1, considering material toughness and impact testing.",
        reasoning_framework=(
            "1. Identify minimum operating temperature and material properties.\n"
            "2. Review ASME VIII-1 requirements for low temperature service and impact testing.\n"
            "3. Select materials qualified for low temperature or specify impact testing.\n"
            "4. Document rationale and test results.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Minimum operating temperature",
            "Material toughness",
            "Impact test results",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1 UG-84", "ASME Section II Part D"],
        burden_holder="Design Engineer",
        adversary_position="Low temperature design increases material and testing cost.",
        counter_arguments=[
            "Ensures vessel reliability under cryogenic conditions.",
            "Code requires impact testing for certain materials and thicknesses.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for low temperature per ASME VIII-1; document rationale and test results.",
        entity_scope="Pressure vessel low temperature design",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1 UG-84"
    ),
    DoctrineBlock(
        topic="Design for Internal Corrosion and Erosion",
        keywords=["internal corrosion", "erosion", "pressure vessel", "ASME VIII-1", "material selection"],
        conclusion_template="Pressure vessels shall be designed to resist internal corrosion and erosion, considering material selection, corrosion allowance, and protective coatings per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Assess service environment and corrosion/erosion risk.\n"
            "2. Review ASME VIII-1 requirements for corrosion allowance and protective coatings.\n"
            "3. Select materials and coatings compatible with service conditions.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Service environment",
            "Corrosion/erosion risk",
            "Material selection",
            "Corrosion allowance",
            "Protective coatings"
        ],
        primary_authority=["ASME Section VIII Division 1", "API 510"],
        burden_holder="Design Engineer",
        adversary_position="Corrosion/erosion protection increases material and coating cost.",
        counter_arguments=[
            "Ensures vessel reliability and longevity.",
            "Code requires minimum corrosion allowance.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for corrosion/erosion per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel corrosion/erosion design",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Internal and External Attachments",
        keywords=["attachments", "internal", "external", "pressure vessel", "ASME VIII-1", "design"],
        conclusion_template="Internal and external attachments shall be designed per ASME Section VIII Division 1, considering load transfer, weld design, and code requirements.",
        reasoning_framework=(
            "1. Identify attachment type, location, and load.\n"
            "2. Review ASME VIII-1 requirements for attachment design.\n"
            "3. Design welds and reinforcement as needed.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Attachment type",
            "Load transfer",
            "Weld design",
            "Reinforcement",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Attachment design increases fabrication complexity.",
        counter_arguments=[
            "Ensures vessel integrity and load transfer.",
            "Code provides clear requirements for attachments.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design attachments per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel attachment design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Transport and Handling Loads",
        keywords=["transport", "handling", "pressure vessel", "ASME VIII-1", "external loads"],
        conclusion_template="Pressure vessels shall be designed to withstand transport and handling loads, considering lifting, rigging, and support requirements per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify transport and handling scenarios and loads.\n"
            "2. Review ASME VIII-1 requirements for lifting and rigging.\n"
            "3. Design supports and lifting lugs for calculated loads.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Transport scenario",
            "Handling loads",
            "Support design",
            "Lifting lugs",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Transport/handling design increases complexity and cost.",
        counter_arguments=[
            "Ensures vessel safety during transport and installation.",
            "Code requires consideration of handling loads.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for transport/handling per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel transport/handling design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Insulation and Fireproofing",
        keywords=["insulation", "fireproofing", "pressure vessel", "ASME VIII-1", "thermal protection"],
        conclusion_template="Pressure vessels shall be designed to accommodate insulation and fireproofing, considering material selection and attachment methods per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify insulation/fireproofing requirements and materials.\n"
            "2. Review ASME VIII-1 requirements for insulation and attachment.\n"
            "3. Design attachment methods compatible with vessel geometry.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Insulation/fireproofing requirements",
            "Material selection",
            "Attachment methods",
            "Vessel geometry",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Insulation/fireproofing increases fabrication complexity.",
        counter_arguments=[
            "Ensures vessel reliability and safety.",
            "Code provides clear requirements for insulation/fireproofing.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for insulation/fireproofing per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel insulation/fireproofing design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Accessibility and Maintenance",
        keywords=["accessibility", "maintenance", "pressure vessel", "ASME VIII-1", "inspection"],
        conclusion_template="Pressure vessels shall be designed for accessibility and maintenance, including manways, inspection ports, and removable components per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify maintenance and inspection requirements.\n"
            "2. Review ASME VIII-1 requirements for accessibility and manways.\n"
            "3. Design ports and removable components for ease of access.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Maintenance requirements",
            "Accessibility",
            "Manways",
            "Inspection ports",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Accessibility design increases fabrication complexity.",
        counter_arguments=[
            "Ensures ease of maintenance and inspection.",
            "Code provides clear requirements for accessibility.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design for accessibility per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel accessibility/maintenance design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Expansion and Contraction Joints",
        keywords=["expansion joint", "contraction joint", "pressure vessel", "ASME VIII-1", "thermal effects"],
        conclusion_template="Expansion and contraction joints shall be designed per ASME Section VIII Division 1, considering thermal effects and material properties.",
        reasoning_framework=(
            "1. Identify operating temperature range and material properties.\n"
            "2. Review ASME VIII-1 requirements for expansion/contraction joints.\n"
            "3. Design joints to accommodate expected movement.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Operating temperature range",
            "Material properties",
            "Expansion/contraction joint design",
            "Code requirements",
            "Client specifications"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Expansion/contraction joint design increases complexity and cost.",
        counter_arguments=[
            "Ensures vessel reliability under thermal effects.",
            "Code provides clear requirements for joints.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design expansion/contraction joints per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel expansion/contraction joint design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Pressure Vessel Internals",
        keywords=["pressure vessel internals", "design", "ASME VIII-1", "support", "attachments"],
        conclusion_template="Pressure vessel internals shall be designed per ASME Section VIII Division 1, considering support, attachment, and material selection.",
        reasoning_framework=(
            "1. Identify internal components and support requirements.\n"
            "2. Review ASME VIII-1 requirements for internal attachments.\n"
            "3. Design supports and attachments for load transfer and accessibility.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Internal component type",
            "Support requirements",
            "Attachment design",
            "Material selection",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Internal design increases fabrication complexity.",
        counter_arguments=[
            "Ensures vessel reliability and performance.",
            "Code provides clear requirements for internals.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design internals per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel internal design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Vessel Orientation (Vertical vs Horizontal)",
        keywords=["vessel orientation", "vertical", "horizontal", "pressure vessel", "ASME VIII-1"],
        conclusion_template="Pressure vessel orientation (vertical vs horizontal) shall be selected based on process requirements, site constraints, and support design per ASME Section VIII Division 1.",
        reasoning_framework=(
            "1. Identify process requirements and site constraints.\n"
            "2. Review ASME VIII-1 requirements for vessel orientation and supports.\n"
            "3. Design supports and anchorage for selected orientation.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Process requirements",
            "Site constraints",
            "Support design",
            "Orientation selection",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Orientation selection may increase support complexity.",
        counter_arguments=[
            "Ensures vessel reliability and performance.",
            "Code provides clear requirements for orientation and supports.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Select vessel orientation per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel orientation design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Vessel Foundation and Anchorage",
        keywords=["foundation", "anchorage", "pressure vessel", "ASME VIII-1", "support"],
        conclusion_template="Pressure vessel foundation and anchorage shall be designed per ASME Section VIII Division 1 and local codes, considering load transfer and site conditions.",
        reasoning_framework=(
            "1. Identify vessel loads and site conditions.\n"
            "2. Review ASME VIII-1 and local code requirements for foundation and anchorage.\n"
            "3. Design foundation and anchorage for load transfer and stability.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Vessel loads",
            "Site conditions",
            "Foundation design",
            "Anchorage",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1", "Local Building Codes"],
        burden_holder="Design Engineer",
        adversary_position="Foundation/anchorage design increases complexity and cost.",
        counter_arguments=[
            "Ensures vessel stability and safety.",
            "Code provides clear requirements for foundation and anchorage.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design foundation/anchorage per ASME VIII-1 and local codes; document rationale.",
        entity_scope="Pressure vessel foundation/anchorage design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Vessel Drainage and Venting",
        keywords=["drainage", "venting", "pressure vessel", "ASME VIII-1", "operational safety"],
        conclusion_template="Pressure vessels shall be designed with adequate drainage and venting provisions per ASME Section VIII Division 1, ensuring operational safety and maintenance accessibility.",
        reasoning_framework=(
            "1. Identify drainage and venting requirements based on process and maintenance needs.\n"
            "2. Review ASME VIII-1 requirements for drainage and venting.\n"
            "3. Design ports and connections for accessibility and safety.\n"
            "4. Document rationale and calculations.\n"
            "5. Validate design against code and client requirements."
        ),
        key_factors=[
            "Drainage requirements",
            "Venting requirements",
            "Port design",
            "Accessibility",
            "Code requirements"
        ],
        primary_authority=["ASME Section VIII Division 1"],
        burden_holder="Design Engineer",
        adversary_position="Drainage/venting design increases fabrication complexity.",
        counter_arguments=[
            "Ensures operational safety and ease of maintenance.",
            "Code provides clear requirements for drainage and venting.",
            "Optimized design balances cost and safety."
        ],
        resolution_strategy="Design drainage/venting per ASME VIII-1; document rationale.",
        entity_scope="Pressure vessel drainage/venting design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Design for Vessel Painting and Coating",
        keywords=["painting", "coating", "pressure vessel", "ASME VIII-1", "corrosion protection"],
        conclusion_template="Pressure vessels shall be painted and coated per ASME Section VIII Division 1 and client specifications, ensuring corrosion protection and durability.",
        reasoning_framework=(
            "1. Identify painting/coating requirements based on service environment.\n