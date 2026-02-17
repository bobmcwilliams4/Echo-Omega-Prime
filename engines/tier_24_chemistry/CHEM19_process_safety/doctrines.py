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
        topic="HAZOP Node Selection and Deviation Analysis",
        keywords=["HAZOP", "node selection", "deviation", "process safety", "risk assessment"],
        conclusion_template="The selection of HAZOP nodes and deviations must comprehensively cover all process sections where credible hazards may arise.",
        reasoning_framework=(
            "1. Identify process boundaries and major equipment items.\n"
            "2. Divide the process into manageable nodes based on equipment, process function, or operational boundaries.\n"
            "3. For each node, systematically apply guide words (e.g., No, More, Less, Reverse, Other than) to process parameters (flow, temperature, pressure, etc.).\n"
            "4. Evaluate the credibility and consequence of each deviation.\n"
            "5. Ensure all credible causes and consequences are captured, avoiding both excessive granularity and omission of significant hazards.\n"
            "6. Validate node selection with experienced process engineers and update as process changes occur.\n"
            "7. Document rationale for node boundaries and deviation selection.\n"
            "8. Review historical incident data for missed hazards.\n"
            "9. Ensure alignment with corporate and regulatory HAZOP standards.\n"
            "10. Integrate findings into the overall risk management framework."
        ),
        key_factors=[
            "Process complexity",
            "Historical incident data",
            "Guide word applicability",
            "Process boundaries",
            "Team experience"
        ],
        primary_authority=["IEC 61882", "CCPS Guidelines for Hazard Evaluation Procedures"],
        burden_holder="Process Safety Team",
        adversary_position="Node selection is too broad or too narrow, leading to missed hazards or inefficiency.",
        counter_arguments=[
            "Node selection follows recognized and generally accepted good engineering practices (RAGAGEP).",
            "Deviations are comprehensively addressed using guide words.",
            "Team consensus and validation steps are documented."
        ],
        resolution_strategy="Facilitate consensus through team review and reference to authoritative guidelines.",
        entity_scope="Process Units and Subsystems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61882 Section 5.2"
    ),
    DoctrineBlock(
        topic="LOPA Independent Protection Layer Criteria",
        keywords=["LOPA", "independent protection layer", "IPL", "risk reduction", "process safety"],
        conclusion_template="An IPL must be independent, reliable, and auditable, providing a quantifiable risk reduction in accordance with LOPA methodology.",
        reasoning_framework=(
            "1. Define the initiating event and consequence scenario.\n"
            "2. Identify candidate IPLs and assess their independence from initiating event and other IPLs.\n"
            "3. Evaluate IPL effectiveness, reliability (PFD), and auditability.\n"
            "4. Confirm IPLs are designed, maintained, and tested per RAGAGEP.\n"
            "5. Exclude credit for IPLs that do not meet independence or reliability criteria.\n"
            "6. Document justification for each credited IPL.\n"
            "7. Review IPL performance data and maintenance history.\n"
            "8. Validate IPLs through periodic audits and functional testing.\n"
            "9. Ensure alignment with corporate and regulatory LOPA standards.\n"
            "10. Update IPL status as process or organizational changes occur."
        ),
        key_factors=[
            "Independence from cause and consequence",
            "Reliability (PFDavg)",
            "Auditability",
            "Maintenance and testing records",
            "Design documentation"
        ],
        primary_authority=["CCPS Layer of Protection Analysis", "IEC 61511"],
        burden_holder="Risk Assessment Facilitator",
        adversary_position="Proposed IPLs are not truly independent or lack sufficient reliability.",
        counter_arguments=[
            "IPL selection follows CCPS and IEC 61511 criteria.",
            "Functional testing and maintenance records demonstrate reliability.",
            "Independence is documented and reviewed."
        ],
        resolution_strategy="Require documentation and third-party review for disputed IPLs.",
        entity_scope="Process Safety Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPS LOPA Book Section 5.3"
    ),
    DoctrineBlock(
        topic="Consequence Modeling - Toxic Gas Dispersion",
        keywords=["consequence modeling", "toxic gas", "dispersion", "process safety", "risk assessment"],
        conclusion_template="Toxic gas dispersion must be modeled using validated tools and site-specific meteorological data to estimate public and worker exposure.",
        reasoning_framework=(
            "1. Identify toxic release scenarios (source, quantity, conditions).\n"
            "2. Select appropriate dispersion modeling software (e.g., ALOHA, PHAST).\n"
            "3. Input site-specific meteorological data (wind speed, stability class, temperature).\n"
            "4. Define terrain, obstacles, and building effects.\n"
            "5. Model release under worst-case and alternative scenarios.\n"
            "6. Evaluate downwind concentrations at relevant receptors (property boundary, control room, public areas).\n"
            "7. Compare predicted concentrations with regulatory exposure limits (ERPG, AEGL, IDLH).\n"
            "8. Document modeling assumptions, input data, and results.\n"
            "9. Update models as process or site conditions change.\n"
            "10. Use results to inform emergency planning and risk communication."
        ),
        key_factors=[
            "Release rate and duration",
            "Meteorological conditions",
            "Topography and obstacles",
            "Toxicity thresholds",
            "Model validation"
        ],
        primary_authority=["EPA Risk Management Program (RMP)", "AIChE CCPS Guidelines", "OSHA PSM"],
        burden_holder="Process Safety Engineer",
        adversary_position="Modeling assumptions are not representative or tools are not validated.",
        counter_arguments=[
            "Modeling uses EPA/CCPS recommended tools and site-specific data.",
            "Assumptions are documented and conservative.",
            "Results are peer-reviewed."
        ],
        resolution_strategy="Conduct sensitivity analysis and independent model review.",
        entity_scope="Facility and Surrounding Community",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA RMP Offsite Consequence Analysis Guidance"
    ),
    DoctrineBlock(
        topic="Consequence Modeling - Fire and Thermal Radiation",
        keywords=["consequence modeling", "fire", "thermal radiation", "process safety", "risk assessment"],
        conclusion_template="Thermal radiation from fires must be modeled to assess impacts on personnel, equipment, and property using validated methodologies.",
        reasoning_framework=(
            "1. Identify credible fire scenarios (pool fire, jet fire, fireball).\n"
            "2. Estimate release quantity, composition, and ignition conditions.\n"
            "3. Select appropriate thermal radiation models (point source, solid flame, computational fluid dynamics as needed).\n"
            "4. Input relevant parameters (fuel properties, geometry, wind conditions).\n"
            "5. Calculate thermal radiation flux at various distances.\n"
            "6. Compare results to damage and injury thresholds (e.g., API 521, NFPA 30).\n"
            "7. Evaluate impacts on critical equipment, escape routes, and personnel assembly points.\n"
            "8. Document modeling assumptions, input data, and results.\n"
            "9. Update models as process or site conditions change.\n"
            "10. Use findings to inform fire protection and emergency planning."
        ),
        key_factors=[
            "Fire scenario selection",
            "Release and ignition conditions",
            "Model selection and validation",
            "Thermal flux thresholds",
            "Exposure duration"
        ],
        primary_authority=["API 521", "NFPA 30", "CCPS Guidelines"],
        burden_holder="Process Safety Engineer",
        adversary_position="Modeling underestimates potential impacts or uses inappropriate models.",
        counter_arguments=[
            "Model selection is based on API and NFPA standards.",
            "Assumptions are conservative and documented.",
            "Results are reviewed by fire protection specialists."
        ],
        resolution_strategy="Require third-party model validation for high-consequence scenarios.",
        entity_scope="Facility and Adjacent Properties",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 521 Section 5.15"
    ),
    DoctrineBlock(
        topic="Consequence Modeling - Vapor Cloud Explosion (VCE)",
        keywords=["consequence modeling", "VCE", "vapor cloud explosion", "blast", "process safety"],
        conclusion_template="VCE scenarios must be modeled using validated blast models, accounting for congestion, confinement, and source term characteristics.",
        reasoning_framework=(
            "1. Identify credible vapor cloud release scenarios.\n"
            "2. Estimate release rate, duration, and flammable mass.\n"
            "3. Assess congestion and confinement levels in the release area.\n"
            "4. Select validated blast models (e.g., Baker-Strehlow-Tang, TNO Multi-Energy).\n"
            "5. Input scenario-specific parameters (geometry, fuel properties, ignition location).\n"
            "6. Calculate overpressure and impulse at various distances.\n"
            "7. Compare results to structural and personnel vulnerability thresholds.\n"
            "8. Document modeling assumptions, input data, and results.\n"
            "9. Update models as process or site conditions change.\n"
            "10. Use findings to inform facility siting and blast protection design."
        ),
        key_factors=[
            "Flammable mass and release rate",
            "Congestion and confinement",
            "Model selection and validation",
            "Overpressure thresholds",
            "Ignition source location"
        ],
        primary_authority=["AIChE CCPS Guidelines", "API 752", "API 753"],
        burden_holder="Process Safety Engineer",
        adversary_position="Modeling does not account for worst-case congestion or uses outdated models.",
        counter_arguments=[
            "Congestion and confinement are assessed per CCPS guidance.",
            "Model selection is justified and documented.",
            "Results are peer-reviewed."
        ],
        resolution_strategy="Require scenario review by explosion modeling experts.",
        entity_scope="Facility and Surrounding Community",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="CCPS Guidelines for Vapor Cloud Explosion, Pressure Vessel Burst, BLEVE, and Flash Fire Hazards"
    ),
    DoctrineBlock(
        topic="Relief Valve Sizing - Fire Case (API 520/521)",
        keywords=["relief valve", "sizing", "fire case", "API 520", "API 521", "process safety"],
        conclusion_template="Relief valves must be sized for external fire exposure per API 520/521, considering wetted surface area and heat input.",
        reasoning_framework=(
            "1. Identify vessels and equipment subject to credible external fire exposure.\n"
            "2. Calculate wetted surface area exposed to fire.\n"
            "3. Estimate heat input using API 521 equations and site-specific fire scenarios.\n"
            "4. Determine required relief rate for vaporization of vessel contents.\n"
            "5. Size relief valve for calculated flow, accounting for backpressure and discharge conditions.\n"
            "6. Select valve type and set pressure per API 520/521.\n"
            "7. Document sizing calculations, assumptions, and input data.\n"
            "8. Review relief system adequacy during process changes.\n"
            "9. Validate calculations through independent review.\n"
            "10. Maintain records for regulatory and insurance audits."
        ),
        key_factors=[
            "Wetted surface area",
            "Heat input calculation",
            "Relief rate determination",
            "Valve sizing equations",
            "Set pressure and backpressure"
        ],
        primary_authority=["API 520", "API 521"],
        burden_holder="Process Engineer",
        adversary_position="Sizing does not account for all credible fire scenarios or uses incorrect inputs.",
        counter_arguments=[
            "Calculations follow API 520/521 methodology.",
            "Assumptions are conservative and documented.",
            "Sizing is independently reviewed."
        ],
        resolution_strategy="Require peer review and periodic revalidation of relief sizing.",
        entity_scope="Pressure Vessels and Storage Tanks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 521 Section 3.15"
    ),
    DoctrineBlock(
        topic="Relief Valve Sizing - Blocked Outlet Case",
        keywords=["relief valve", "sizing", "blocked outlet", "process safety", "overpressure"],
        conclusion_template="Relief valves must be sized for blocked outlet scenarios using process-specific flow and pressure conditions.",
        reasoning_framework=(
            "1. Identify credible blocked outlet scenarios for each process segment.\n"
            "2. Calculate maximum upstream pressure and flow rate under blocked conditions.\n"
            "3. Determine required relief rate based on process fluid properties and operating conditions.\n"
            "4. Size relief valve using appropriate equations for gas, vapor, or liquid service.\n"
            "5. Account for backpressure, set pressure, and allowable overpressure.\n"
            "6. Document all assumptions, calculations, and input data.\n"
            "7. Validate relief system adequacy during process changes.\n"
            "8. Review sizing with process and safety teams.\n"
            "9. Maintain records for regulatory compliance.\n"
            "10. Update relief device sizing as process conditions evolve."
        ),
        key_factors=[
            "Blocked outlet identification",
            "Process fluid properties",
            "Relief rate calculation",
            "Valve sizing equations",
            "Set pressure and backpressure"
        ],
        primary_authority=["API 520", "API 521"],
        burden_holder="Process Engineer",
        adversary_position="Blocked outlet scenarios are not fully identified or sizing is not conservative.",
        counter_arguments=[
            "All credible blocked outlet cases are considered.",
            "Sizing follows API methodology.",
            "Assumptions are documented and reviewed."
        ],
        resolution_strategy="Facilitate multidisciplinary review and periodic revalidation.",
        entity_scope="Process Piping and Equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 520 Section 4.4"
    ),
    DoctrineBlock(
        topic="Dust Explosion Prevention - Kst Classification",
        keywords=["dust explosion", "Kst", "classification", "process safety", "combustible dust"],
        conclusion_template="Combustible dusts must be classified by Kst value to determine explosion prevention and protection requirements.",
        reasoning_framework=(
            "1. Collect representative dust samples from process areas.\n"
            "2. Test samples for Kst (maximum rate of pressure rise) and Pmax (maximum explosion pressure) per ASTM E1226.\n"
            "3. Classify dust explosibility (St 0, St 1, St 2, St 3) based on Kst value.\n"
            "4. Identify process areas where dust accumulation or dispersion is possible.\n"
            "5. Implement explosion prevention measures (e.g., housekeeping, inerting, containment) based on classification.\n"
            "6. Specify explosion protection devices (venting, suppression) as required.\n"
            "7. Document testing results and classification rationale.\n"
            "8. Update classification as process or material changes occur.\n"
            "9. Train personnel on dust explosion hazards and controls.\n"
            "10. Review compliance with NFPA and OSHA standards."
        ),
        key_factors=[
            "Kst value",
            "Dust sample representativeness",
            "Process area identification",
            "Prevention and protection measures",
            "Regulatory requirements"
        ],
        primary_authority=["NFPA 652", "ASTM E1226", "OSHA Combustible Dust NEP"],
        burden_holder="Process Safety Manager",
        adversary_position="Dust testing is not representative or classification is not updated.",
        counter_arguments=[
            "Samples are collected per NFPA/ASTM guidance.",
            "Classification is reviewed after process changes.",
            "Controls are implemented based on current classification."
        ],
        resolution_strategy="Require periodic retesting and third-party verification.",
        entity_scope="Facilities Handling Combustible Dust",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NFPA 652 Section 5.2"
    ),
    DoctrineBlock(
        topic="Chemical Reactivity Hazards - DIERS Methodology",
        keywords=["chemical reactivity", "DIERS", "runaway reaction", "vent sizing", "process safety"],
        conclusion_template="Reactivity hazards must be evaluated using DIERS methodology to ensure adequate emergency relief system design.",
        reasoning_framework=(
            "1. Identify chemicals and mixtures with potential for runaway or reactive hazards.\n"
            "2. Conduct calorimetric testing (e.g., ARC, VSP) to characterize reaction kinetics and energetics.\n"
            "3. Apply DIERS methodology to estimate maximum pressure and gas generation rates.\n"
            "4. Size emergency relief devices for two-phase flow and reaction scenarios.\n"
            "5. Evaluate potential for foaming, solids, or non-condensable gas generation.\n"
            "6. Document all test data, calculations, and assumptions.\n"
            "7. Review relief system adequacy with process changes or new chemistries.\n"
            "8. Validate design with independent experts as needed.\n"
            "9. Train personnel on reactivity hazards and emergency procedures.\n"
            "10. Maintain records for regulatory and insurance audits."
        ),
        key_factors=[
            "Reaction kinetics and energetics",
            "Calorimetric test data",
            "Two-phase flow potential",
            "Relief device sizing",
            "Process changes"
        ],
        primary_authority=["DIERS Project Manual", "CCPS Guidelines for Chemical Reactivity Evaluation"],
        burden_holder="Process Safety Engineer",
        adversary_position="Reactivity hazards are underestimated or relief devices are undersized.",
        counter_arguments=[
            "DIERS methodology is applied using current test data.",
            "Sizing is independently reviewed.",
            "Process changes trigger re-evaluation."
        ],
        resolution_strategy="Require third-party review for high-hazard scenarios.",
        entity_scope="Reactors and Chemical Processing Units",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="CCPS Guidelines for Pressure Relief and Effluent Handling Systems"
    ),
    DoctrineBlock(
        topic="OSHA PSM 14 Elements Compliance",
        keywords=["OSHA", "PSM", "process safety management", "compliance", "14 elements"],
        conclusion_template="Facilities must implement and maintain all 14 OSHA PSM elements to ensure regulatory compliance and process safety.",
        reasoning_framework=(
            "1. Identify covered processes per OSHA PSM applicability criteria.\n"
            "2. Develop and implement written programs for each of the 14 elements.\n"
            "3. Assign responsibilities and ensure adequate resources for implementation.\n"
            "4. Conduct periodic audits and gap assessments.\n"
            "5. Document training, procedures, and compliance activities.\n"
            "6. Address audit findings and corrective actions in a timely manner.\n"
            "7. Review and update programs as processes or regulations change.\n"
            "8. Maintain records for regulatory inspection.\n"
            "9. Engage workforce in PSM activities and feedback.\n"
            "10. Benchmark performance against industry best practices."
        ),
        key_factors=[
            "Program documentation",
            "Resource allocation",
            "Audit and corrective action",
            "Employee participation",
            "Regulatory updates"
        ],
        primary_authority=["OSHA 29 CFR 1910.119"],
        burden_holder="PSM Coordinator",
        adversary_position="PSM elements are incomplete, outdated, or not effectively implemented.",
        counter_arguments=[
            "Programs are documented and audited per OSHA requirements.",
            "Corrective actions are tracked and closed.",
            "Employee participation is documented."
        ],
        resolution_strategy="Conduct regular third-party audits and management reviews.",
        entity_scope="PSM-Covered Facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119"
    ),
    DoctrineBlock(
        topic="Management of Change (MOC) Process",
        keywords=["MOC", "management of change", "process safety", "change management"],
        conclusion_template="All process changes must be evaluated and approved through a formal MOC process prior to implementation.",
        reasoning_framework=(
            "1. Define the scope and rationale for proposed changes.\n"
            "2. Assess potential safety, health, and environmental impacts.\n"
            "3. Review affected procedures, drawings, and documentation.\n"
            "4. Obtain multidisciplinary review and approval.\n"
            "5. Update process safety information and operating procedures.\n"
            "6. Communicate changes and provide training to affected personnel.\n"
            "7. Implement change and verify completion of all actions.\n"
            "8. Document the entire MOC process and retain records.\n"
            "9. Audit MOC effectiveness and address deficiencies.\n"
            "10. Integrate MOC with other PSM elements (PHA, PSSR, etc.)."
        ),
        key_factors=[
            "Scope and impact assessment",
            "Multidisciplinary review",
            "Documentation updates",
            "Training and communication",
            "Audit and verification"
        ],
        primary_authority=["OSHA 1910.119(l)", "CCPS Guidelines for MOC"],
        burden_holder="Change Initiator",
        adversary_position="Changes are implemented without adequate review or documentation.",
        counter_arguments=[
            "Formal MOC process is followed for all changes.",
            "Documentation and training are verified.",
            "Audits confirm MOC effectiveness."
        ],
        resolution_strategy="Enforce MOC policy with disciplinary action for non-compliance.",
        entity_scope="All Process Areas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(l)"
    ),
    DoctrineBlock(
        topic="Inherently Safer Design (ISD) Principles",
        keywords=["ISD", "inherently safer design", "process safety", "risk reduction"],
        conclusion_template="ISD principles must be applied to eliminate or reduce hazards at the source during process design and modification.",
        reasoning_framework=(
            "1. Identify process hazards and risk drivers early in design.\n"
            "2. Apply ISD strategies: minimize, substitute, moderate, and simplify.\n"
            "3. Evaluate alternatives for hazard elimination or reduction.\n"
            "4. Document ISD considerations and decisions in design records.\n"
            "5. Review ISD opportunities during process modifications and MOC.\n"
            "6. Engage multidisciplinary teams in ISD brainstorming.\n"
            "7. Benchmark ISD practices against industry leaders.\n"
            "8. Train design and operations personnel on ISD concepts.\n"
            "9. Monitor effectiveness of ISD measures over time.\n"
            "10. Update ISD practices as new technologies emerge."
        ),
        key_factors=[
            "Hazard identification",
            "ISD strategy selection",
            "Design documentation",
            "Team engagement",
            "Continuous improvement"
        ],
        primary_authority=["CCPS Inherently Safer Chemical Processes", "ANSI/AIChE ISD Standard"],
        burden_holder="Design Engineer",
        adversary_position="ISD is not considered or only applied superficially.",
        counter_arguments=[
            "ISD is documented in design records.",
            "Alternatives are evaluated and justified.",
            "Continuous improvement is demonstrated."
        ],
        resolution_strategy="Require ISD review at all design and MOC stages.",
        entity_scope="Process Design and Modification",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CCPS ISD Guidelines"
    ),
    DoctrineBlock(
        topic="Static Electricity Hazards in Process Operations",
        keywords=["static electricity", "hazards", "process operations", "ignition", "process safety"],
        conclusion_template="Static electricity hazards must be identified and controlled through bonding, grounding, and process design.",
        reasoning_framework=(
            "1. Identify operations with potential for static generation (e.g., liquid transfer, powder handling).\n"
            "2. Evaluate material properties (conductivity, charge relaxation time).\n"
            "3. Implement bonding and grounding for equipment and personnel.\n"
            "4. Control process conditions (flow rates, humidity) to minimize static buildup.\n"
            "5. Use antistatic additives or materials as appropriate.\n"
            "6. Train personnel on static hazard recognition and controls.\n"
            "7. Inspect and maintain grounding systems regularly.\n"
            "8. Document static hazard assessments and controls.\n"
            "9. Review incidents and near-misses for static-related events.\n"
            "10. Update controls as process or material changes occur."
        ),
        key_factors=[
            "Process operation type",
            "Material properties",
            "Bonding and grounding effectiveness",
            "Personnel training",
            "Incident history"
        ],
        primary_authority=["NFPA 77", "CCPS Guidelines for Safe Handling of Powders and Bulk Solids"],
        burden_holder="Operations Manager",
        adversary_position="Static hazards are not adequately identified or controlled.",
        counter_arguments=[
            "NFPA 77 guidelines are followed.",
            "Controls are documented and maintained.",
            "Personnel are trained and incidents are tracked."
        ],
        resolution_strategy="Require periodic static hazard audits and corrective actions.",
        entity_scope="All Process Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NFPA 77"
    ),
    DoctrineBlock(
        topic="Boiling Liquid Expanding Vapor Explosion (BLEVE) Prevention",
        keywords=["BLEVE", "boiling liquid expanding vapor explosion", "prevention", "process safety"],
        conclusion_template="BLEVE prevention requires robust vessel design, pressure relief, and fire protection measures for pressurized liquid storage.",
        reasoning_framework=(
            "1. Identify vessels containing pressurized liquefied gases.\n"
            "2. Ensure vessel design meets applicable codes (ASME, API).\n"
            "3. Install and maintain pressure relief devices sized for fire exposure.\n"
            "4. Provide passive and active fire protection (e.g., water spray, insulation).\n"
            "5. Minimize inventory and segregate high-risk vessels.\n"
            "6. Train personnel on BLEVE hazards and emergency response.\n"
            "7. Inspect vessels and relief devices regularly.\n"
            "8. Document design, protection, and inspection records.\n"
            "9. Review incident history for lessons learned.\n"
            "10. Update controls as process or inventory changes occur."
        ),
        key_factors=[
            "Vessel design and code compliance",
            "Relief device adequacy",
            "Fire protection measures",
            "Inventory management",
            "Personnel training"
        ],
        primary_authority=["API 2510", "ASME Boiler and Pressure Vessel Code", "CCPS Guidelines"],
        burden_holder="Mechanical Integrity Manager",
        adversary_position="Vessels are not adequately protected or relief devices are undersized.",
        counter_arguments=[
            "Design and protection follow API/ASME codes.",
            "Relief sizing is documented and reviewed.",
            "Fire protection is tested and maintained."
        ],
        resolution_strategy="Require third-party review for high-risk vessels.",
        entity_scope="Pressurized Liquid Storage",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 2510 Section 7"
    ),
    # Additional doctrines to reach 40+ entries...
    DoctrineBlock(
        topic="Pressure Relief System Design Basis Documentation",
        keywords=["pressure relief", "design basis", "documentation", "process safety"],
        conclusion_template="All pressure relief devices must have a documented design basis, including scenarios, calculations, and assumptions.",
        reasoning_framework=(
            "1. Identify all protected equipment and credible overpressure scenarios.\n"
            "2. Document relief device sizing calculations and input data.\n"
            "3. Record assumptions, set pressures, and allowable overpressure.\n"
            "4. Review and update design basis as process conditions change.\n"
            "5. Maintain records for regulatory and insurance audits.\n"
            "6. Validate design basis through independent review.\n"
            "7. Integrate documentation with P&IDs and process safety information.\n"
            "8. Train personnel on relief system design and operation.\n"
            "9. Audit documentation completeness and accuracy.\n"
            "10. Update as new scenarios or codes emerge."
        ),
        key_factors=[
            "Scenario identification",
            "Calculation accuracy",
            "Assumption documentation",
            "Review and update frequency",
            "Record retention"
        ],
        primary_authority=["API 521", "CCPS Guidelines"],
        burden_holder="Process Engineer",
        adversary_position="Design basis is incomplete or outdated.",
        counter_arguments=[
            "Design basis is documented and reviewed.",
            "Updates are triggered by process changes.",
            "Records are maintained for audits."
        ],
        resolution_strategy="Conduct periodic audits and require updates.",
        entity_scope="All Protected Equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 521 Section 4.2"
    ),
    DoctrineBlock(
        topic="Facility Siting and Occupied Building Risk Assessment",
        keywords=["facility siting", "occupied building", "risk assessment", "process safety"],
        conclusion_template="Facility siting studies must assess risks to occupied buildings from fires, explosions, and toxic releases.",
        reasoning_framework=(
            "1. Identify all occupied buildings and assembly areas.\n"
            "2. Model credible fire, explosion, and toxic release scenarios.\n"
            "3. Evaluate structural vulnerability and occupant exposure.\n"
            "4. Compare risk results to corporate and regulatory criteria.\n"
            "5. Recommend risk reduction measures (relocation, hardening, evacuation planning).\n"
            "6. Document study scope, assumptions, and results.\n"
            "7. Review and update siting studies as process or occupancy changes occur.\n"
            "8. Engage stakeholders in risk communication.\n"
            "9. Benchmark against industry best practices.\n"
            "10. Integrate findings into emergency planning."
        ),
        key_factors=[
            "Scenario modeling",
            "Building occupancy and vulnerability",
            "Risk criteria",
            "Stakeholder engagement",
            "Study update frequency"
        ],
        primary_authority=["API 752", "API 753", "CCPS Guidelines"],
        burden_holder="Process Safety Manager",
        adversary_position="Siting studies are outdated or do not address all hazards.",
        counter_arguments=[
            "Studies are updated per API 752/753 guidance.",
            "All credible scenarios are modeled.",
            "Stakeholder engagement is documented."
        ],
        resolution_strategy="Require periodic updates and third-party review.",
        entity_scope="Process Facilities with Occupied Buildings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 752"
    ),
    DoctrineBlock(
        topic="Process Hazard Analysis (PHA) Revalidation",
        keywords=["PHA", "process hazard analysis", "revalidation", "process safety"],
        conclusion_template="PHAs must be revalidated at least every five years or sooner if significant changes occur.",
        reasoning_framework=(
            "1. Track PHA completion and revalidation due dates.\n"
            "2. Review process changes, incident history, and new hazards.\n"
            "3. Update PHA documentation and action items.\n"
            "4. Engage multidisciplinary teams in revalidation.\n"
            "5. Address outstanding recommendations and lessons learned.\n"
            "6. Document revalidation scope, findings, and actions.\n"
            "7. Communicate results to affected personnel.\n"
            "8. Integrate revalidation with other PSM elements.\n"
            "9. Benchmark against industry practices.\n"
            "10. Maintain records for regulatory compliance."
        ),
        key_factors=[
            "PHA schedule",
            "Process changes",
            "Incident history",
            "Team participation",
            "Documentation"
        ],
        primary_authority=["OSHA 1910.119(e)", "CCPS Guidelines"],
        burden_holder="PHA Facilitator",
        adversary_position="PHA is not revalidated on schedule or does not address new hazards.",
        counter_arguments=[
            "Revalidation is tracked and documented.",
            "Team includes relevant disciplines.",
            "All changes and incidents are reviewed."
        ],
        resolution_strategy="Implement automated tracking and management oversight.",
        entity_scope="PSM-Covered Processes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(e)(6)"
    ),
    DoctrineBlock(
        topic="Mechanical Integrity Inspection Intervals",
        keywords=["mechanical integrity", "inspection", "intervals", "process safety"],
        conclusion_template="Inspection intervals for critical equipment must be established based on risk and regulatory requirements.",
        reasoning_framework=(
            "1. Identify critical process equipment (pressure vessels, piping, relief devices, etc.).\n"
            "2. Assess risk based on consequence of failure, service conditions, and history.\n"
            "3. Establish inspection intervals per API, ASME, or corporate standards.\n"
            "4. Document rationale for interval selection.\n"
            "5. Review and adjust intervals based on inspection findings and process changes.\n"
            "6. Maintain inspection records for regulatory compliance.\n"
            "7. Train inspectors and ensure qualification.\n"
            "8. Audit inspection program effectiveness.\n"
            "9. Benchmark against industry practices.\n"
            "10. Update program as new data or standards emerge."
        ),
        key_factors=[
            "Equipment criticality",
            "Risk assessment",
            "Regulatory requirements",
            "Inspection findings",
            "Documentation"
        ],
        primary_authority=["API 510", "API 570", "OSHA 1910.119(j)"],
        burden_holder="Mechanical Integrity Manager",
        adversary_position="Intervals are too long or not justified by risk.",
        counter_arguments=[
            "Intervals are based on API/ASME standards.",
            "Findings trigger interval review.",
            "Records are maintained and audited."
        ],
        resolution_strategy="Require management approval for interval changes.",
        entity_scope="Critical Process Equipment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 510 Section 6"
    ),
    DoctrineBlock(
        topic="Emergency Shutdown (ESD) System Design and Testing",
        keywords=["emergency shutdown", "ESD", "system design", "testing", "process safety"],
        conclusion_template="ESD systems must be designed for reliable operation and tested regularly to ensure functionality.",
        reasoning_framework=(
            "1. Identify process hazards requiring ESD protection.\n"
            "2. Design ESD systems per IEC 61511 and corporate standards.\n"
            "3. Specify fail-safe design and redundancy as appropriate.\n"
            "4. Develop and implement regular functional testing procedures.\n"
            "5. Document test results and corrective actions.\n"
            "6. Review ESD performance after process upsets or incidents.\n"
            "7. Train operators on ESD operation and response.\n"
            "8. Maintain records for regulatory compliance.\n"
            "9. Audit ESD system effectiveness.\n"
            "10. Update design and testing as process changes occur."
        ),
        key_factors=[
            "Hazard identification",
            "System design and redundancy",
            "Testing frequency",
            "Documentation",
            "Operator training"
        ],
        primary_authority=["IEC 61511", "OSHA 1910.119(f)"],
        burden_holder="Instrumentation Engineer",
        adversary_position="ESD systems are not tested or fail to operate as designed.",
        counter_arguments=[
            "Testing is documented and corrective actions are tracked.",
            "Design follows IEC 61511.",
            "Operator training is current."
        ],
        resolution_strategy="Implement automated test tracking and management review.",
        entity_scope="Process Units with ESD",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511 Section 16"
    ),
    DoctrineBlock(
        topic="Safe Work Permit System Implementation",
        keywords=["safe work permit", "permit to work", "process safety", "hot work", "confined space"],
        conclusion_template="A formal safe work permit system must be implemented for all non-routine and hazardous work.",
        reasoning_framework=(
            "1. Define scope of work and identify hazards.\n"
            "2. Issue permits for hot work, confined space entry, line breaking, and other hazardous tasks.\n"
            "3. Specify required controls, PPE, and isolation procedures.\n"
            "4. Obtain approvals from responsible supervisors and safety personnel.\n"
            "5. Communicate permit requirements to all affected personnel.\n"
            "6. Verify controls are in place before work begins.\n"
            "7. Monitor work and enforce permit conditions.\n"
            "8. Close permits and document completion.\n"
            "9. Audit permit system effectiveness.\n"
            "10. Update procedures as new hazards or tasks arise."
        ),
        key_factors=[
            "Hazard identification",
            "Permit controls",
            "Approval process",
            "Communication",
            "Audit and update"
        ],
        primary_authority=["OSHA 1910.119(f)", "NFPA 51B", "CCPS Guidelines"],
        burden_holder="Permit Issuer",
        adversary_position="Permits are not issued or controls are not enforced.",
        counter_arguments=[
            "Permit system is documented and audited.",
            "Supervisors are trained and accountable.",
            "Non-compliance is addressed promptly."
        ],
        resolution_strategy="Conduct regular permit audits and enforce accountability.",
        entity_scope="All Process Areas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(f)"
    ),
    DoctrineBlock(
        topic="Process Safety Information (PSI) Management",
        keywords=["process safety information", "PSI", "management", "documentation", "process safety"],
        conclusion_template="PSI must be accurate, accessible, and updated to reflect current process conditions and hazards.",
        reasoning_framework=(
            "1. Identify all required PSI per OSHA and industry standards.\n"
            "2. Maintain accurate P&IDs, process descriptions, and material safety data.\n"
            "3. Update PSI promptly after process changes.\n"
            "4. Ensure PSI is accessible to all relevant personnel.\n"
            "5. Audit PSI for completeness and accuracy.\n"
            "6. Integrate PSI with other PSM elements (PHA, MOC, training).\n"
            "7. Train personnel on PSI use and updates.\n"
            "8. Maintain records for regulatory compliance.\n"
            "9. Benchmark PSI management against industry practices.\n"
            "10. Update PSI as new hazards or regulations emerge."
        ),
        key_factors=[
            "PSI completeness",
            "Update frequency",
            "Accessibility",
            "Personnel training",
            "Audit results"
        ],
        primary_authority=["OSHA 1910.119(d)", "CCPS Guidelines"],
        burden_holder="PSI Coordinator",
        adversary_position="PSI is outdated, incomplete, or not accessible.",
        counter_arguments=[
            "PSI is audited and updated regularly.",
            "Personnel are trained on PSI management.",
            "Records are maintained for compliance."
        ],
        resolution_strategy="Implement electronic PSI management and audit systems.",
        entity_scope="PSM-Covered Facilities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(d)"
    ),
    DoctrineBlock(
        topic="Incident Investigation and Root Cause Analysis",
        keywords=["incident investigation", "root cause analysis", "process safety", "learning"],
        conclusion_template="All process safety incidents and near-misses must be investigated to identify root causes and implement corrective actions.",
        reasoning_framework=(
            "1. Report all incidents and near-misses promptly.\n"
            "2. Assign trained investigators and multidisciplinary teams.\n"
            "3. Collect evidence, interview witnesses, and document findings.\n"
            "4. Apply root cause analysis methods (e.g., 5 Whys, Fault Tree, TapRooT).\n"
            "5. Identify direct, contributing, and root causes.\n"
            "6. Develop and track corrective actions to closure.\n"
            "7. Communicate findings and lessons learned to affected personnel.\n"
            "8. Review effectiveness of corrective actions.\n"
            "9. Maintain investigation records for compliance.\n"
            "10. Benchmark investigation process against industry practices."
        ),
        key_factors=[
            "Timely reporting",
            "Investigator training",
            "Root cause methodology",
            "Corrective action tracking",
            "Communication"
        ],
        primary_authority=["OSHA 1910.119(m)", "CCPS Guidelines"],
        burden_holder="Incident Investigation Leader",
        adversary_position="Investigations are superficial or corrective actions are not implemented.",
        counter_arguments=[
            "Investigations follow CCPS and OSHA guidance.",
            "Corrective actions are tracked to closure.",
            "Lessons learned are communicated."
        ],
        resolution_strategy="Audit investigation quality and corrective action effectiveness.",
        entity_scope="All Process Areas",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(m)"
    ),
    DoctrineBlock(
        topic="Hot Work Permit Controls",
        keywords=["hot work", "permit", "controls", "fire prevention", "process safety"],
        conclusion_template="Hot work permits must specify fire prevention measures and be authorized before work begins.",
        reasoning_framework=(
            "1. Identify all hot work activities (welding, cutting, grinding, etc.).\n"
            "2. Issue hot work permits specifying required controls (fire watch, area isolation, PPE).\n"
            "3. Verify area is free of flammable materials and vapors.\n"
            "4. Assign trained fire watch personnel.\n"
            "5. Monitor work and enforce permit conditions.\n"
            "6. Document permit issuance and closure.\n"
            "7. Audit hot work permit system effectiveness.\n"
            "8. Train personnel on hot work hazards and controls.\n"
            "9. Update procedures as new hazards or tasks arise.\n"
            "10. Review incident history for lessons learned."
        ),
        key_factors=[
            "Hot work identification",
            "Permit controls",
            "Fire watch assignment",
            "Area isolation",
            "Training"
        ],
        primary_authority=["NFPA 51B", "OSHA 1910.119(f)", "CCPS Guidelines"],
        burden_holder="Permit Issuer",
        adversary_position="Hot work is performed without adequate controls or permit.",
        counter_arguments=[
            "Permit system is documented and audited.",
            "Fire watch is assigned and trained.",
            "Non-compliance is addressed promptly."
        ],
        resolution_strategy="Conduct regular hot work audits and enforce accountability.",
        entity_scope="All Process Areas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NFPA 51B"
    ),
    DoctrineBlock(
        topic="Confined Space Entry Permit System",
        keywords=["confined space", "entry", "permit system", "process safety"],
        conclusion_template="Confined space entries require a permit system with atmospheric testing, isolation, and rescue provisions.",
        reasoning_framework=(
            "1. Identify all confined spaces and maintain an inventory.\n"
            "2. Issue entry permits specifying required controls (atmospheric testing, isolation, PPE).\n"
            "3. Assign trained attendants and entry supervisors.\n"
            "4. Verify isolation and lockout/tagout of energy sources.\n"
            "5. Provide rescue equipment and trained personnel.\n"
            "6. Monitor entry and enforce permit conditions.\n"
            "7. Document permit issuance and closure.\n"
            "8. Audit confined space entry system effectiveness.\n"
            "9. Train personnel on confined space hazards and controls.\n"
            "10. Update procedures as new spaces or hazards are identified."
        ),
        key_factors=[
            "Confined space identification",
            "Permit controls",
            "Atmospheric testing",
            "Rescue provisions",
            "Training"
        ],
        primary_authority=["OSHA 1910.146", "CCPS Guidelines"],
        burden_holder="Entry Supervisor",
        adversary_position="Entries are made without permits or required controls.",
        counter_arguments=[
            "Permit system is documented and audited.",
            "Personnel are trained and assigned.",
            "Non-compliance is addressed promptly."
        ],
        resolution_strategy="Conduct regular confined space audits and enforce accountability.",
        entity_scope="All Confined Spaces",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.146"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout (LOTO) Program Effectiveness",
        keywords=["lockout/tagout", "LOTO", "program", "effectiveness", "process safety"],
        conclusion_template="LOTO programs must ensure all energy sources are isolated and verified before servicing equipment.",
        reasoning_framework=(
            "1. Identify all energy sources for process equipment.\n"
            "2. Develop written LOTO procedures for each equipment type.\n"
            "3. Train personnel on LOTO procedures and verification.\n"
            "4. Issue and track LOTO devices and tags.\n"
            "5. Verify isolation before work begins.\n"
            "6. Audit LOTO program effectiveness and address deficiencies.\n"
            "7. Document LOTO activities and maintain records.\n"
            "8. Review incident history for LOTO failures.\n"
            "9. Update procedures as equipment or hazards change.\n"
            "10. Benchmark LOTO practices against industry standards."
        ),
        key_factors=[
            "Energy source identification",
            "Procedure documentation",
            "Training",
            "Verification",
            "Audit results"
        ],
        primary_authority=["OSHA 1910.147", "CCPS Guidelines"],
        burden_holder="Maintenance Supervisor",
        adversary_position="LOTO is not consistently applied or verified.",
        counter_arguments=[
            "LOTO procedures are documented and audited.",
            "Personnel are trained and accountable.",
            "Non-compliance is addressed promptly."
        ],
        resolution_strategy="Conduct regular LOTO audits and enforce accountability.",
        entity_scope="All Process Equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.147"
    ),
    DoctrineBlock(
        topic="Process Safety Culture and Leadership",
        keywords=["process safety", "culture", "leadership", "behavior", "management commitment"],
        conclusion_template="Strong process safety culture and leadership are essential for effective risk management and incident prevention.",
        reasoning_framework=(
            "1. Define and communicate process safety values and expectations.\n"
            "2. Demonstrate visible management commitment to process safety.\n"
            "3. Empower employees to report hazards and stop unsafe work.\n"
            "4. Recognize and reward safe behaviors.\n"
            "5. Integrate process safety into performance management.\n"
            "6. Provide ongoing training and development.\n"
            "7. Measure and monitor process safety culture indicators.\n"
            "8. Address cultural barriers and resistance to change.\n"
            "9. Benchmark culture against industry leaders.\n"
            "10. Continuously improve based on feedback and lessons learned."
        ),
        key_factors=[
            "Management commitment",
            "Employee empowerment",
            "Recognition and accountability",
            "Training",
            "Culture measurement"
        ],
        primary_authority=["CCPS Guidelines for Risk Based Process Safety"],
        burden_holder="Senior Management",
        adversary_position="Process safety is not prioritized or cultural issues are ignored.",
        counter_arguments=[
            "Leadership demonstrates commitment.",
            "Employees are empowered and recognized.",
            "Culture is measured and improved."
        ],
        resolution_strategy="Conduct culture surveys and leadership training.",
        entity_scope="All Organizational Levels",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPS RBPS Element 1"
    ),
    DoctrineBlock(
        topic="Emergency Planning and Response Program",
        keywords=["emergency planning", "response", "program", "process safety"],
        conclusion_template="Facilities must maintain a comprehensive emergency planning and response program for credible process safety scenarios.",
        reasoning_framework=(
            "1. Identify credible emergency scenarios (fire, explosion, toxic release, etc.).\n"
            "2. Develop written emergency response plans and procedures.\n"
            "3. Assign roles and responsibilities for response.\n"
            "4. Train personnel and conduct regular drills.\n"
            "5. Coordinate with local emergency services and community.\n"
            "6. Maintain emergency equipment and supplies.\n"
            "7. Review and update plans after drills or incidents.\n"
            "8. Communicate plans to all personnel and contractors.\n"
            "9. Benchmark program against industry best practices.\n"
            "10. Maintain records for regulatory compliance."
        ),
        key_factors=[
            "Scenario identification",
            "Plan documentation",
            "Training and drills",
            "Coordination",
            "Program updates"
        ],
        primary_authority=["OSHA 1910.38", "EPA RMP", "CCPS Guidelines"],
        burden_holder="Emergency Response Coordinator",
        adversary_position="Plans are outdated or personnel are not trained.",
        counter_arguments=[
            "Plans are documented and updated.",
            "Drills are conducted and lessons learned applied.",
            "Coordination is documented."
        ],
        resolution_strategy="Conduct regular drills and program reviews.",
        entity_scope="All Process Facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.38"
    ),
    DoctrineBlock(
        topic="Operator Training and Competency Assurance",
        keywords=["operator training", "competency", "process safety", "qualification"],
        conclusion_template="Operators must be trained and qualified for their assigned process safety responsibilities.",
        reasoning_framework=(
            "1. Identify required competencies for each operator role.\n"
            "2. Develop and deliver process safety training programs.\n"
            "3. Assess operator knowledge and skills through testing and observation.\n"
            "4. Document training completion and competency assessments.\n"
            "5. Provide refresher training and updates as needed.\n"
            "6. Address gaps through targeted training or reassignment.\n"
            "7. Benchmark training against industry standards.\n"
            "8. Maintain training records for regulatory compliance.\n"
            "9. Review training effectiveness after incidents or changes.\n"
            "10. Integrate training with other PSM elements."
        ),
        key_factors=[
            "Competency identification",
            "Training delivery",
            "Assessment and documentation",
            "Refresher training",
            "Program effectiveness"
        ],
        primary_authority=["OSHA 1910.119(g)", "CCPS Guidelines"],
        burden_holder="Training Coordinator",
        adversary_position="Operators are not adequately trained or assessed.",
        counter_arguments=[
            "Training is documented and assessed.",
            "Refresher training is provided.",
            "Records are maintained."
        ],
        resolution_strategy="Conduct regular training audits and gap assessments.",
        entity_scope="All Process Operators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(g)"
    ),
    DoctrineBlock(
        topic="Process Safety Performance Metrics",
        keywords=["process safety", "performance metrics", "leading indicators", "lagging indicators"],
        conclusion_template="Facilities must track and analyze process safety performance metrics to drive continuous improvement.",
        reasoning_framework=(
            "1. Define leading and lagging process safety metrics (e.g., near-misses, action closure, Tier 1/2 events).\n"
            "2. Collect and analyze data regularly.\n"
            "3. Communicate metrics and trends to all organizational levels.\n"
            "4. Use metrics to identify improvement opportunities and track effectiveness of actions.\n"
            "5. Benchmark performance against industry data.\n"
            "6. Review metrics after incidents or major changes.\n"
            "7. Integrate metrics with management reviews and audits.\n"
            "8. Maintain records for regulatory and corporate reporting.\n"
            "9. Address data quality and consistency issues.\n"
            "10. Update metrics as industry practices evolve."
        ),
        key_factors=[
            "Metric selection",
            "Data collection and analysis",
            "Communication",
            "Benchmarking",
            "Continuous improvement"
        ],
        primary_authority=["CCPS Guidelines for Process Safety Metrics"],
        burden_holder="Process Safety Manager",
        adversary_position="Metrics are not meaningful or not used for improvement.",
        counter_arguments=[
            "Metrics are defined and communicated.",
            "Data is analyzed and actions tracked.",
            "Benchmarking is performed."
        ],
        resolution_strategy="Review metrics in management meetings and audits.",
        entity_scope="All Process Facilities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CCPS Metrics Guidelines"
    ),
    DoctrineBlock(
        topic="Layer of Protection Analysis (LOPA) Documentation",
        keywords=["LOPA", "documentation", "risk assessment", "process safety"],
        conclusion_template="LOPA studies must be thoroughly documented, including scenarios, IPLs, and risk decisions.",
        reasoning_framework=(
            "1. Define LOPA scope and objectives.\n"
            "2. Document initiating events, consequences, and risk criteria.\n"
            "3. List all IPLs and justify their credit.\n"
            "4. Record risk calculations and decisions.\n"
            "5. Review and update LOPA documentation as process changes occur.\n"
            "6. Integrate LOPA with PHA and MOC processes.\n"
            "7. Train personnel on LOPA methodology and documentation.\n"
            "8. Audit documentation for completeness and accuracy.\n"
            "9. Maintain records for regulatory and insurance audits.\n"
            "10. Benchmark documentation against industry practices."
        ),
        key_factors=[
            "Scenario documentation",
            "IPL justification",
            "Risk calculation",
            "Review and update",
            "Audit results"
        ],
        primary_authority=["CCPS LOPA Book", "IEC 61511"],
        burden_holder="LOPA Facilitator",
        adversary_position="LOPA is not documented or IPLs are not justified.",
        counter_arguments=[
            "Documentation is complete and audited.",
            "IPL credit is justified and reviewed.",
            "Records are maintained."
        ],
        resolution_strategy="Require management review and periodic audits.",
        entity_scope="All LOPA Studies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPS LOPA Book Section 7"
    ),
    DoctrineBlock(
        topic="SIL (Safety Integrity Level) Determination and Verification",
        keywords=["SIL", "safety integrity level", "determination", "verification", "process safety"],
        conclusion_template="SIL levels must be determined and verified for all safety instrumented functions per IEC 61511.",
        reasoning_framework=(
            "1. Identify safety instrumented functions (SIFs) and associated hazards.\n"
            "2. Perform SIL determination using risk graphs, LOPA, or other methods.\n"
            "3. Document required risk reduction and target SIL for each SIF.\n"
            "4. Design SIFs to meet target SIL, including hardware and software.\n"
            "5. Verify SIL achievement through calculation and testing.\n"
            "6. Maintain documentation for design, testing, and operation.\n"
            "7. Review SIL assignments after process changes or incidents.\n"
            "8. Train personnel on SIL concepts and responsibilities.\n"
            "9. Audit SIL determination and verification processes.\n"
            "10. Benchmark against industry best practices."
        ),
        key_factors=[
            "SIF identification",
            "Risk reduction requirement",
            "Design and verification",
            "Documentation",
            "Audit results"
        ],
        primary_authority=["IEC 61511", "CCPS Guidelines"],
        burden_holder="Instrumentation Engineer",
        adversary_position="SIL is not properly determined or verified.",
        counter_arguments=[
            "SIL determination follows IEC 61511.",
            "Verification is documented and audited.",
            "Personnel are trained."
        ],
        resolution_strategy="Require third-party SIL verification for high-risk SIFs.",
        entity_scope="All Safety Instrumented Systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511 Section 9"
    ),
    DoctrineBlock(
        topic="Combustible Gas Detection System Design",
        keywords=["combustible gas", "detection", "system design", "process safety"],
        conclusion_template="Combustible gas detection systems must be designed for early leak detection and integrated with process safety systems.",
        reasoning_framework=(
            "1. Identify high-risk areas for combustible gas releases.\n"
            "2. Select appropriate detection technology (catalytic, IR, open path, etc.).\n"
            "3. Determine detector placement for optimal coverage.\n"
            "4. Integrate detection with alarms and shutdown systems.\n"
            "5. Test and maintain detectors regularly.\n"
            "6. Document system design, testing, and maintenance.\n"
            "7. Review system performance after incidents or changes.\n"
            "8. Train personnel on gas detection response.\n"
            "9. Audit system effectiveness.\n"
            "10. Update design as process or technology changes."
        ),
        key_factors=[
            "Area risk assessment",
            "Technology selection",
            "Detector placement",
            "Integration",
            "Testing and maintenance"
        ],
        primary_authority=["NFPA 72", "CCPS Guidelines"],
        burden_holder="Instrumentation Engineer",
        adversary_position="Detection coverage is inadequate or system is not maintained.",
        counter_arguments=[
            "Coverage is based on risk assessment.",
            "Testing and maintenance are documented.",
            "Personnel are trained."
        ],
        resolution_strategy="Conduct periodic coverage reviews and system audits.",
        entity_scope="High-Risk Process Areas",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NFPA 72"
    ),
    DoctrineBlock(
        topic="Process Safety Critical Equipment Identification",
        keywords=["process safety", "critical equipment", "identification", "asset management"],
        conclusion_template="Critical equipment must be identified, documented, and managed to ensure process safety performance.",
        reasoning_framework=(
            "1. Define criteria for process safety critical equipment (impact, redundancy, failure modes).\n"
            "2. Identify and document all critical equipment in asset register.\n"
            "3. Assign ownership and maintenance responsibilities.\n"
            "4. Review and update criticality assignments as process changes occur.\n"
            "5. Integrate critical equipment management with mechanical integrity and PSM programs.\n"
            "6. Train personnel on critical equipment identification and management.\n"
            "7. Audit critical equipment management effectiveness.\n"
            "8. Benchmark against industry practices.\n"
            "9. Maintain records for regulatory and insurance audits.\n"
            "10. Update criteria as new data or standards emerge."
        ),
        key_factors=[
            "Criticality criteria",
            "Asset documentation",
            "Ownership and maintenance",
            "Program integration",
            "Audit results"
        ],
        primary_authority=["CCPS Guidelines", "API 580"],
        burden_holder="Asset Manager",
        adversary_position="Critical equipment is not identified or managed effectively.",
        counter_arguments=[
            "Criteria are defined and documented.",
            "Asset register is maintained.",
            "Program is audited."
        ],
        resolution_strategy="Require periodic criticality reviews and audits.",
        entity_scope="All Process Equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 580"
    ),
    DoctrineBlock(
        topic="Process Safety Competency for Contractors",
        keywords=["process safety", "competency", "contractors", "training"],
        conclusion_template="Contractors must demonstrate process safety competency before performing work in process areas.",
        reasoning_framework=(
            "1. Define process safety competency requirements for contractors.\n"
            "2. Verify contractor training and qualifications before site access.\n"
            "3. Provide site-specific process safety orientation.\n"
            "4. Monitor contractor performance and compliance.\n"
            "5. Address deficiencies through retraining or removal.\n"
            "6. Document contractor competency and performance records.\n"
            "7. Integrate contractor management with PSM programs.\n"
            "8. Audit contractor competency management effectiveness.\n"
            "9. Benchmark against industry practices.\n"
            "10. Update requirements as hazards or regulations change."
        ),
        key_factors=[
            "Competency requirements",
            "Training verification",
            "Performance monitoring",
            "Documentation",
            "Audit results"
        ],
        primary_authority=["OSHA 1910.119(h)", "CCPS Guidelines"],
        burden_holder="Contractor Coordinator",
        adversary_position="Contractors are not trained or do not comply with process safety requirements.",
        counter_arguments=[
            "Competency is verified before work.",
            "Performance is monitored and documented.",
            "Non-compliance is addressed promptly."
        ],
        resolution_strategy="Conduct regular contractor audits and enforce requirements.",
        entity_scope="All Process Areas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(h)"
    ),
    DoctrineBlock(
        topic="Process Safety Information Sharing and Communication",
        keywords=["process safety", "information sharing", "communication", "learning"],
        conclusion_template="Process safety information and lessons learned must be communicated effectively across the organization.",
        reasoning_framework=(
            "1. Identify key process safety information and lessons learned.\n"
            "2. Develop communication channels (meetings, bulletins, electronic systems).\n"
            "3. Ensure timely dissemination to all relevant personnel.\n"
            "4. Encourage feedback and questions.\n"
            "5. Integrate communication with training and PSM programs.\n"
            "6. Audit effectiveness of information sharing.\n"
            "7. Benchmark against industry practices.\n"
            "8. Update communication methods as technology or organization changes.\n"
            "9. Maintain records of communication activities.\n"
            "10. Address barriers to effective communication."
        ),
        key_factors=[
            "Information identification",
            "Communication channels",
            "Timeliness",
            "Feedback",
            "Audit results"
        ],
        primary_authority=["CCPS Guidelines for Risk Based Process Safety"],
        burden_holder="Process Safety Manager",
        adversary_position="Information is not shared or lessons are not learned.",
        counter_arguments=[
            "Communication is documented and audited.",
            "Feedback is encouraged and addressed.",
            "Methods are updated as needed."
        ],
        resolution_strategy="Conduct communication effectiveness surveys and reviews.",
        entity_scope="All Organizational Levels",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPS RBPS Element 2"
    ),
    DoctrineBlock(
        topic="Process Safety Management System Auditing",
        keywords=["process safety", "management system", "auditing", "compliance"],
        conclusion_template="Process safety management systems must be audited regularly to verify compliance and drive improvement.",
        reasoning_framework=(
            "1. Develop an audit program covering all PSM elements.\n"
            "2. Assign qualified auditors independent of the audited area.\n"
            "3. Use checklists and protocols based on regulatory and corporate standards.\n"
            "4. Document findings and corrective actions.\n"
            "5. Track corrective actions to closure.\n"
            "6. Communicate audit results to management and affected personnel.\n"
            "7. Review audit program effectiveness and update as needed.\n"
            "8. Benchmark against industry practices.\n"
            "9. Maintain audit records for compliance.\n"
            "10. Integrate audits with continuous improvement programs."
        ),
        key_factors=[
            "Audit program scope",
            "Auditor qualification",
            "Documentation",
            "Corrective action tracking",
            "Program improvement"
        ],
        primary_authority=["OSHA 1910.119(o)", "CCPS Guidelines"],
        burden_holder="PSM Coordinator",
        adversary_position="Audits are not independent or findings are not addressed.",
        counter_arguments=[
            "Audits are conducted by qualified personnel.",
            "Corrective actions are tracked and closed.",
            "Audit program is reviewed regularly."
        ],
        resolution_strategy="Require management oversight and third-party audits.",
        entity_scope="All Process Facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(o)"
    ),
    DoctrineBlock(
        topic="Process Safety Near-Miss Reporting and Analysis",
        keywords=["process safety", "near-miss", "reporting", "analysis", "learning"],
        conclusion_template="Near-miss events must be reported, analyzed, and used to drive process safety improvements.",
        reasoning_framework=(
            "1. Define near-miss reporting criteria and process.\n"
            "2. Encourage and reward reporting by all personnel.\n"
            "3. Analyze near-miss events for root and contributing causes.\n"
            "4. Develop and implement corrective actions.\n"
            "5. Communicate lessons learned to all personnel.\n"
            "6. Track near-miss trends and metrics.\n"
            "7. Integrate near-miss analysis with other PSM elements.\n"
            "8. Audit near-miss program effectiveness.\n"
            "9. Benchmark against industry practices.\n"
            "10. Update program as hazards or organization changes."
        ),
        key_factors=[
            "Reporting criteria",
            "Analysis methodology",
            "Corrective action",
            "Communication",
            "Program effectiveness"
        ],
        primary_authority=["CCPS Guidelines for Risk Based Process Safety"],
        burden_holder="Process Safety Manager",
        adversary_position="Near-misses are not reported or analyzed.",
        counter_arguments=[
            "Reporting is encouraged and rewarded.",
            "Analysis is documented and actions tracked.",
            "Lessons learned are communicated."
        ],
        resolution_strategy="Conduct program audits and feedback sessions.",
        entity_scope="All Process Areas",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CCPS RBPS Element 3"
    ),
    DoctrineBlock(
        topic="Process Safety Critical Alarm Management",
        keywords=["process safety", "critical alarm", "management", "operator response"],
        conclusion_template="Critical alarms must be identified, prioritized, and managed to ensure timely and effective operator response.",
        reasoning_framework=(
            "1. Define criteria for process safety critical alarms.\n"
            "2. Identify and document all critical alarms in the control system.\n"
            "3. Prioritize alarms to prevent overload and ensure operator focus.\n"
            "4. Test and maintain alarm functionality.\n"
            "5. Train operators on alarm response procedures.\n"
            "6. Review alarm performance after incidents or changes.\n"
            "7. Audit alarm management program effectiveness.\n"
            "8. Benchmark against industry practices.\n"
            "9. Maintain records for regulatory and insurance audits.\n"
            "10. Update alarm management as process or technology changes."
        ),
        key_factors=[
            "Alarm criteria",
            "Documentation",
            "Prioritization",
            "Testing and maintenance",
            "Operator training"
        ],
        primary_authority=["ISA 18.2", "CCPS Guidelines"],
        burden_holder="Control Systems Engineer",
        adversary_position="Critical alarms are not identified or managed effectively.",
        counter_arguments=[
            "Criteria and documentation are maintained.",
            "Operators are trained and alarms are tested.",
            "Program is audited."
        ],
        resolution_strategy="Conduct periodic alarm rationalization and audits.",
        entity_scope="All Process Control Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISA 18.2"
    ),
    DoctrineBlock(
        topic="Process Safety Management of Aging Equipment",
        keywords=["process safety", "aging equipment", "asset management", "integrity"],
        conclusion_template="Aging equipment must be assessed and managed to ensure continued process safety performance.",
        reasoning_framework=(
            "1. Identify aging equipment based on age, service, and condition.\n"
            "2. Assess risk of failure and potential consequences.\n"
            "3. Develop and implement inspection, testing, and replacement plans.\n"
            "4. Document assessment and management actions.\n"
            "5. Review and update plans as equipment ages or process changes occur.\n"
            "6. Train personnel on aging equipment risks and controls.\n"
            "7. Audit program effectiveness and address deficiencies.\n"
            "8. Benchmark against industry practices.\n"
            "9. Maintain records for regulatory and insurance audits.\n"
            "10. Update management strategies as new data or standards emerge."
        ),
        key_factors=[
            "Equipment identification",
            "Risk assessment",
            "Inspection and testing",
            "Documentation",
            "Program updates"
        ],
        primary_authority=["API 570", "CCPS Guidelines"],
        burden_holder="Asset Integrity Manager",
        adversary_position="Aging equipment is not assessed or managed.",
        counter_arguments=[
            "Assessment and management plans are documented.",
            "Inspections and replacements are tracked.",
            "Program is audited."
        ],
        resolution_strategy="Require management review and third-party audits.",
        entity_scope="All Process Equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Process Safety Risk Assessment Methodology Selection",
        keywords=["process safety", "risk assessment", "methodology", "selection"],
        conclusion_template="Risk assessment methodologies must be selected based on process complexity, hazard potential, and regulatory requirements.",
        reasoning_framework=(
            "1. Identify process hazards and risk drivers.\n"
            "2. Evaluate process complexity and potential consequences.\n"
            "3. Select appropriate risk assessment methodology (HAZOP, What-If, FMEA, LOPA, QRA, etc.).\n"
            "4. Document rationale for methodology selection.\n"
            "5. Train personnel on selected methodology.\n"
            "6. Review effectiveness after assessments or incidents.\n"
            "7. Benchmark against industry practices.\n"
            "8. Update methodology selection as process or regulations change.\n"
            "9. Maintain records for regulatory compliance.\n"
            "10. Integrate methodology selection with PSM programs."
        ),
        key_factors=[
            "Hazard identification",
            "Process complexity",
            "Consequence potential",
            "Regulatory requirements",
            "Documentation"
        ],
        primary_authority=["CCPS Guidelines for Hazard Evaluation Procedures"],
        burden_holder="Risk Assessment Facilitator",
        adversary_position="Methodology is not appropriate for the process or hazards.",
        counter_arguments=[
            "Selection is documented and reviewed.",
            "Personnel are trained.",
            "Methodology is updated as needed."
        ],
        resolution_strategy="Require management review and periodic benchmarking.",
        entity_scope="All Process Hazard Analyses",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPS Hazard Evaluation Guidelines"
    ),
    DoctrineBlock(
        topic="Process Safety Management of Temporary Changes",
        keywords=["process safety", "management", "temporary changes", "MOC"],
        conclusion_template="Temporary changes must be managed through the MOC process with defined duration, controls, and reversion plans.",
        reasoning_framework=(
            "1. Define scope and duration of temporary change.\n"
            "2. Assess potential safety, health, and environmental impacts.\n"
            "3. Review and approve temporary change through MOC process.\n"
            "4. Implement additional controls as needed.\n"
            "5. Communicate change and provide training to affected personnel.\n"
            "6. Monitor and document effectiveness of controls.\n"
            "7. Define and implement reversion plan to original state.\n"
            "8. Review temporary change after completion.\n"
            "9. Audit temporary change management effectiveness.\n"
            "10. Update procedures as needed."
        ),
        key_factors=[
            "Scope and duration",
            "Impact assessment",
            "MOC approval",
            "Control implementation",
            "Reversion plan"
        ],
        primary_authority=["OSHA 1910.119(l)", "CCPS Guidelines"],
        burden_holder="Change Initiator",
        adversary_position="Temporary changes bypass MOC or lack controls.",
        counter_arguments=[
            "Temporary changes are managed through MOC.",
            "Controls and reversion plans are documented.",
            "Effectiveness is audited."
        ],
        resolution_strategy="Require management approval and periodic audits.",
        entity_scope="All Process Areas",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(l)"
    ),
    DoctrineBlock(
        topic="Process Safety Pre-Startup Safety Review (PSSR)",
        keywords=["process safety", "pre-startup safety review", "PSSR", "commissioning"],
        conclusion_template="PSSR must be conducted before startup of new or modified processes to verify readiness and safety.",
        reasoning_framework=(
            "1. Define PSSR scope and checklist based on process and changes.\n"
            "2. Verify completion of construction, installation, and testing.\n"
            "3. Confirm process safety information is current and accurate.\n"
            "4. Review operating procedures and training.\n"
            "5. Inspect equipment and safety systems for readiness.\n"
            "6. Document PSSR findings and approvals.\n"
            "7. Address outstanding actions before startup.\n"
            "8. Train personnel on PSSR requirements.\n"
            "9. Audit PSSR program effectiveness.\n"
            "10. Update PSSR procedures as process or regulations change."
        ),
        key_factors=[
            "Scope and checklist",
            "Completion verification",
            "Documentation",
            "Training",
            "Audit results"
        ],
        primary_authority=["OSHA 1910.119(i)", "CCPS Guidelines"],
        burden_holder="Startup Manager",
        adversary_position="PSSR is not conducted or actions are not closed before startup.",
        counter_arguments=[
            "PSSR is documented and audited.",
            "Actions are tracked to closure.",
            "Personnel are trained."
        ],
        resolution_strategy="Require management approval before startup.",
        entity_scope="All New or Modified Processes",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.119(i)"
    ),
    DoctrineBlock(
        topic="Process Safety Management of Change Communication",
        keywords=["process safety", "management of change", "MOC", "communication"],
        conclusion_template="All MOC actions and impacts must be communicated to affected personnel before implementation.",
        reasoning_framework=(
            "1. Identify all personnel affected by the proposed change.\n"
            "2. Communicate scope, rationale, and impacts of the change.\n"
            "3. Provide training or instruction as needed.\n"
            "4. Document communication activities and personnel acknowledgment.\n"
            "5. Verify understanding before implementing the change.\n"
            "6. Review communication effectiveness after implementation.\n"
            "7. Integrate communication with other PSM elements.\n"
            "8. Audit MOC communication effectiveness.\n"
            "9. Update communication procedures as organization or hazards change.\n"
            "10. Benchmark against industry practices."
        ),
        key_factors=[
            "Personnel identification",
            "Communication methods",
            "Training",
            "Documentation",
            "Audit results"
        ],
        primary_authority=["CCPS Guidelines for MOC"],
        burden_holder="Change Initiator",
        adversary_position="Personnel are not informed or trained on changes.",
        counter_arguments=[
            "Communication is