from dataclasses import dataclass, field
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
        topic="Conductor Casing Design - Minimum Depth Requirements",
        keywords=["conductor casing", "minimum depth", "well control", "surface stability"],
        conclusion_template="The conductor casing shall be set at a minimum depth sufficient to prevent surface formation washout and provide well control during drilling operations.",
        reasoning_framework=(
            "The design of the conductor casing is governed by the need to stabilize unconsolidated surface formations and prevent washout or collapse during initial drilling. "
            "Regulatory requirements (e.g., API RP 65, NORSOK D-010) specify minimum setting depths, typically ranging from 30-60 meters below ground level, depending on local geology and anticipated surface loads. "
            "The design must consider historical washout incidents, local groundwater tables, and the potential for shallow gas. "
            "Geotechnical surveys and offset well data inform the selection of the minimum depth. "
            "The casing must also withstand installation loads and provide a foundation for subsequent casing strings. "
            "In areas with permafrost or high groundwater, additional depth or cementing requirements may apply. "
            "The operator is responsible for demonstrating that the selected depth meets or exceeds regulatory and operational requirements."
        ),
        key_factors=[
            "Local geotechnical conditions",
            "Historical surface washout incidents",
            "Regulatory minimums (API, NORSOK, local authorities)",
            "Groundwater table depth",
            "Presence of shallow gas or permafrost"
        ],
        primary_authority=["API RP 65", "NORSOK D-010", "Local Regulatory Authority"],
        burden_holder="Operator",
        adversary_position="Setting depth is excessive and increases cost without added safety benefit.",
        counter_arguments=[
            "Insufficient depth may result in surface formation collapse.",
            "Regulatory non-compliance exposes operator to penalties.",
            "Offset data supports deeper setting for well control."
        ],
        resolution_strategy="Demonstrate compliance with regulatory minimums and justify additional depth with site-specific data.",
        entity_scope="All onshore and offshore DRL04 wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 65 Section 5.2"
    ),
    DoctrineBlock(
        topic="Surface Casing Seat Selection - Pore Pressure and Fracture Gradient",
        keywords=["surface casing", "seat selection", "pore pressure", "fracture gradient", "kick tolerance"],
        conclusion_template="The surface casing seat shall be set above the first major pore pressure increase and below the lowest anticipated fracture gradient to ensure kick tolerance and well integrity.",
        reasoning_framework=(
            "Surface casing seat selection is a critical aspect of well integrity, balancing the need to isolate shallow aquifers and provide a competent formation for pressure control. "
            "The seat must be set above the first significant increase in pore pressure to avoid encountering overpressured zones without adequate protection. "
            "Simultaneously, the seat must be below the lowest anticipated fracture gradient to prevent lost circulation during cementing or drilling. "
            "Kick tolerance calculations, offset well data, and formation pressure tests inform the optimal setting depth. "
            "Failure to select an appropriate seat can result in well control incidents or loss of zonal isolation. "
            "Regulatory agencies (e.g., BSEE, API) require documentation of the selection process."
        ),
        key_factors=[
            "Pore pressure profile",
            "Fracture gradient data",
            "Kick tolerance analysis",
            "Offset well experiences",
            "Regulatory requirements"
        ],
        primary_authority=["API Bulletin 92", "BSEE Well Control Regulations", "NORSOK D-010"],
        burden_holder="Operator",
        adversary_position="Deeper seat increases drilling risk and cost.",
        counter_arguments=[
            "Shallower seat may compromise well control.",
            "Deeper seat may be necessary to ensure adequate kick tolerance.",
            "Regulatory minimums must be met."
        ],
        resolution_strategy="Document pore pressure and fracture gradient analysis; justify seat selection with risk assessment.",
        entity_scope="All DRL04 surface casing designs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API Bulletin 92 Section 3.1"
    ),
    DoctrineBlock(
        topic="Casing Grade Selection - Burst Design",
        keywords=["casing grade", "burst pressure", "design factor", "internal pressure"],
        conclusion_template="Casing grade shall be selected such that the burst resistance exceeds the maximum anticipated internal pressure by the required design factor.",
        reasoning_framework=(
            "Burst design for casing involves selecting a steel grade with sufficient yield strength to withstand the highest internal pressures expected during drilling, completion, and production. "
            "API TR 5C3 provides calculation methods for burst resistance, incorporating design factors (typically 1.1 to 1.25 for surface/intermediate casing, higher for production casing). "
            "Maximum internal pressure scenarios include gas kicks, cementing pressures, and formation fluid influx. "
            "Material properties, manufacturing tolerances, and corrosion allowances must be considered. "
            "The selected grade must also be compatible with sour service (H2S/CO2) if present. "
            "Documentation of calculations and selection rationale is required for regulatory compliance."
        ),
        key_factors=[
            "Maximum anticipated internal pressure",
            "API burst resistance equations",
            "Design factors (regulatory and company standards)",
            "Material properties and sour service compatibility",
            "Manufacturing tolerances"
        ],
        primary_authority=["API TR 5C3", "ISO 10400", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Higher grade increases cost without proportional safety benefit.",
        counter_arguments=[
            "Lower grade may not withstand burst scenarios.",
            "Regulatory design factors are mandatory.",
            "Sour service may require premium grades."
        ],
        resolution_strategy="Provide burst calculations and demonstrate grade selection meets or exceeds all requirements.",
        entity_scope="All DRL04 casing strings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 6"
    ),
    DoctrineBlock(
        topic="Casing Grade Selection - Collapse Design",
        keywords=["casing grade", "collapse pressure", "external pressure", "design factor"],
        conclusion_template="Casing grade and wall thickness shall be selected to ensure collapse resistance exceeds the maximum anticipated external pressure by the required design factor.",
        reasoning_framework=(
            "Collapse design addresses the risk of casing failure due to external pressure exceeding internal pressure, particularly during cementing, evacuation, or lost circulation events. "
            "API TR 5C3 provides equations for collapse resistance, considering wall thickness, ovality, and material yield strength. "
            "Design factors (typically 1.0-1.1) are applied based on regulatory and company standards. "
            "Worst-case scenarios include full evacuation of the casing and maximum formation pressure. "
            "Corrosion allowances and manufacturing tolerances must be included. "
            "The selected grade and wall thickness must be justified with calculations and documented for audit."
        ),
        key_factors=[
            "Maximum external pressure",
            "Minimum internal pressure",
            "API collapse resistance equations",
            "Wall thickness and ovality",
            "Design factors"
        ],
        primary_authority=["API TR 5C3", "ISO 10400", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Overly conservative design increases cost.",
        counter_arguments=[
            "Non-conservative design risks catastrophic collapse.",
            "Regulatory factors are not negotiable.",
            "Offset failures support conservative approach."
        ],
        resolution_strategy="Submit collapse calculations and demonstrate compliance with regulatory and company standards.",
        entity_scope="All DRL04 casing strings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 7"
    ),
    DoctrineBlock(
        topic="Casing Tensile Design - Worst-Case Loading",
        keywords=["casing tensile", "axial load", "worst-case", "safety factor"],
        conclusion_template="Casing string shall be designed to withstand the worst-case axial load with the required safety factor, considering buoyancy and dynamic effects.",
        reasoning_framework=(
            "Tensile design ensures the casing can support its own weight, the weight of subsequent strings, and any additional loads during running or cementing. "
            "API TR 5C3 and ISO 10400 provide guidance on calculating tensile capacity, factoring in buoyancy, dynamic loads, and connection efficiency. "
            "Worst-case scenarios include running in hole, landing, and emergency situations (e.g., stuck pipe). "
            "A minimum safety factor (typically 1.6 for surface/intermediate, 1.8 for production) is applied. "
            "Connection ratings must be verified, as they often govern the string's tensile capacity. "
            "Documentation must include load cases, calculations, and connection selection rationale."
        ),
        key_factors=[
            "Casing weight and length",
            "Buoyancy effects",
            "Dynamic loading during running",
            "Connection efficiency",
            "Safety factors"
        ],
        primary_authority=["API TR 5C3", "ISO 10400", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Safety factor is excessive and increases cost.",
        counter_arguments=[
            "Lower safety factor increases risk of string failure.",
            "Connection ratings may govern design.",
            "Dynamic loads are unpredictable."
        ],
        resolution_strategy="Document all load cases and demonstrate safety factor compliance.",
        entity_scope="All DRL04 casing strings",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 8"
    ),
    DoctrineBlock(
        topic="Biaxial/Triaxial Stress Analysis - Combined Loads",
        keywords=["biaxial", "triaxial", "stress analysis", "combined loads", "casing"],
        conclusion_template="Casing design must include biaxial/triaxial stress analysis to ensure integrity under combined burst, collapse, and tensile loads.",
        reasoning_framework=(
            "Modern casing design requires assessment of combined loading scenarios, as casing is rarely subjected to pure burst, collapse, or tension. "
            "Biaxial and triaxial analysis methods (API TR 5C3, ISO 10400) account for the interaction of internal and external pressures with axial loads. "
            "The von Mises or Tresca criteria are typically used to evaluate combined stress states. "
            "Design must ensure that the combined stress does not exceed the yield strength of the selected grade, applying appropriate safety factors. "
            "Special attention is required for HPHT wells and deepwater operations, where load combinations are more severe. "
            "Documentation must include analysis methodology, input parameters, and results."
        ),
        key_factors=[
            "Internal and external pressures",
            "Axial load",
            "Material yield strength",
            "Safety factors",
            "Analysis methodology"
        ],
        primary_authority=["API TR 5C3", "ISO 10400", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Uniaxial analysis is sufficient for most wells.",
        counter_arguments=[
            "Combined loading is common in modern wells.",
            "Regulatory and company standards require triaxial analysis.",
            "Offset failures support more rigorous analysis."
        ],
        resolution_strategy="Provide triaxial analysis results and demonstrate compliance.",
        entity_scope="All DRL04 casing designs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 9"
    ),
    DoctrineBlock(
        topic="Casing Wear Analysis - Eccentric Loading",
        keywords=["casing wear", "eccentric loading", "drilling", "centralization"],
        conclusion_template="Casing wear analysis must be performed for all casing strings exposed to rotating drill pipe, with mitigation measures for high-wear zones.",
        reasoning_framework=(
            "Casing wear is a significant risk in deviated and horizontal wells, where rotating drill pipe can erode the casing wall. "
            "Wear analysis involves modeling contact forces, rotation rates, and mud properties to predict wear depth. "
            "High-wear zones are typically at doglegs, build sections, and near the kick-off point. "
            "Mitigation includes use of centralizers, wear-resistant materials, and limiting rotation. "
            "API RP 7G and company standards provide guidance on wear prediction and monitoring. "
            "Documentation must include wear analysis results and mitigation strategies."
        ),
        key_factors=[
            "Well trajectory",
            "Drill pipe rotation and contact force",
            "Mud properties",
            "Centralization",
            "Wear-resistant materials"
        ],
        primary_authority=["API RP 7G", "Company Casing Wear Policy"],
        burden_holder="Operator",
        adversary_position="Wear analysis is unnecessary for vertical wells.",
        counter_arguments=[
            "Even slight deviation can cause significant wear.",
            "Regulatory and company standards require wear analysis.",
            "Offset failures support wear mitigation."
        ],
        resolution_strategy="Document wear analysis and implement mitigation for high-risk zones.",
        entity_scope="All DRL04 wells with deviated or horizontal sections",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 7G Section 10"
    ),
    DoctrineBlock(
        topic="Pore Pressure and Fracture Gradient Modeling",
        keywords=["pore pressure", "fracture gradient", "well control", "kick tolerance"],
        conclusion_template="Pore pressure and fracture gradient models must be developed and updated throughout drilling to inform casing design and well control strategies.",
        reasoning_framework=(
            "Accurate modeling of pore pressure and fracture gradient is essential for safe and efficient casing design. "
            "Models are built using offset well data, seismic surveys, and real-time drilling parameters (e.g., d-exponent, mud weight trends). "
            "Models must be updated as new data becomes available, particularly after formation pressure tests or well control events. "
            "Kick tolerance calculations and casing seat selection depend on these models. "
            "Regulatory agencies require submission and justification of models for critical wells."
        ),
        key_factors=[
            "Offset well data",
            "Seismic surveys",
            "Real-time drilling data",
            "Formation pressure tests",
            "Regulatory requirements"
        ],
        primary_authority=["API Bulletin 92", "BSEE Regulations", "NORSOK D-010"],
        burden_holder="Operator",
        adversary_position="Static models are sufficient; updates are unnecessary.",
        counter_arguments=[
            "Real-time updates improve safety and efficiency.",
            "Regulatory agencies require dynamic modeling.",
            "Offset incidents support continuous model updates."
        ],
        resolution_strategy="Maintain and document dynamic models throughout drilling.",
        entity_scope="All DRL04 wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Bulletin 92 Section 2"
    ),
    DoctrineBlock(
        topic="Premium Connections - Gas Tightness",
        keywords=["premium connections", "gas tight", "leak resistance", "HPHT"],
        conclusion_template="Premium connections must be used for casing strings exposed to high internal gas pressure or HPHT conditions to ensure gas tightness and prevent leaks.",
        reasoning_framework=(
            "Standard API connections may not provide adequate gas tightness in HPHT or sour service wells. "
            "Premium connections are designed with metal-to-metal seals or special thread forms to prevent gas leakage under high pressure and temperature. "
            "Selection must consider connection test results (ISO 13679 CAL IV), compatibility with casing grade, and operational requirements. "
            "Documentation must include connection type, test data, and rationale for selection."
        ),
        key_factors=[
            "Internal gas pressure",
            "HPHT conditions",
            "Connection test results",
            "Compatibility with casing grade",
            "Leak resistance"
        ],
        primary_authority=["ISO 13679", "API 5C5", "Company Connection Policy"],
        burden_holder="Operator",
        adversary_position="Premium connections are unnecessary and increase cost.",
        counter_arguments=[
            "Standard connections may leak under HPHT conditions.",
            "Regulatory and company standards require premium connections for critical service.",
            "Offset leaks support premium connection use."
        ],
        resolution_strategy="Document connection selection and provide test data for justification.",
        entity_scope="All DRL04 HPHT and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 13679 CAL IV"
    ),
    DoctrineBlock(
        topic="Liner Design and Tieback - Zonal Isolation",
        keywords=["liner design", "tieback", "zonal isolation", "casing integrity"],
        conclusion_template="Liner and tieback systems must be designed to provide equivalent zonal isolation and integrity as full casing strings.",
        reasoning_framework=(
            "Liner systems are used to reduce cost and complexity but must provide the same level of zonal isolation as full casing. "
            "Tieback design must consider connection integrity, cementing quality, and pressure testing. "
            "API TR 5C3 and ISO 14310 provide guidance on liner and tieback qualification. "
            "Documentation must include liner hanger ratings, tieback connection test results, and cement evaluation logs."
        ),
        key_factors=[
            "Liner hanger and tieback connection ratings",
            "Cementing quality",
            "Pressure testing",
            "Zonal isolation requirements",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "ISO 14310", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Liner systems are less reliable than full casing.",
        counter_arguments=[
            "Modern liner systems meet or exceed full casing performance.",
            "Proper design and testing ensure integrity.",
            "Offset failures support robust liner qualification."
        ],
        resolution_strategy="Document liner and tieback design, testing, and cement evaluation.",
        entity_scope="All DRL04 liner installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 11"
    ),
    DoctrineBlock(
        topic="Casing Centralizer Placement - Eccentricity Control",
        keywords=["casing centralizer", "placement", "eccentricity", "cement sheath"],
        conclusion_template="Centralizers must be placed at intervals sufficient to minimize casing eccentricity and ensure effective cement sheath formation.",
        reasoning_framework=(
            "Centralizer placement is critical for achieving uniform cement sheath and zonal isolation. "
            "API RP 10D and company standards specify centralizer spacing based on well deviation, casing size, and mud properties. "
            "Eccentricity modeling should be performed for deviated and horizontal wells. "
            "Documentation must include centralizer type, spacing, and simulation results."
        ),
        key_factors=[
            "Well deviation and trajectory",
            "Casing size and weight",
            "Mud and cement properties",
            "Centralizer type and spacing",
            "Eccentricity modeling"
        ],
        primary_authority=["API RP 10D", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Centralizer placement is excessive and increases cost.",
        counter_arguments=[
            "Insufficient centralization leads to poor cementing.",
            "Regulatory and company standards require modeling.",
            "Offset failures support robust centralization."
        ],
        resolution_strategy="Document centralizer placement and modeling results.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 10D Section 4"
    ),
    DoctrineBlock(
        topic="HPHT Casing Design - Material Selection",
        keywords=["HPHT", "casing design", "material selection", "yield strength"],
        conclusion_template="Casing material for HPHT wells must be selected for enhanced yield strength, ductility, and resistance to sour service.",
        reasoning_framework=(
            "HPHT wells (typically >150°C and >10,000 psi) require special material selection due to elevated risk of collapse, burst, and sour service corrosion. "
            "API 5CT and ISO 15156 provide guidance on material properties, including yield strength, ductility, and H2S/CO2 resistance. "
            "Material selection must be supported by laboratory test data and field experience. "
            "Documentation must include material certificates, test results, and compatibility with well fluids."
        ),
        key_factors=[
            "Well temperature and pressure",
            "Material yield strength and ductility",
            "Sour service resistance",
            "Laboratory test data",
            "Material certification"
        ],
        primary_authority=["API 5CT", "ISO 15156", "Company HPHT Policy"],
        burden_holder="Operator",
        adversary_position="Standard materials are sufficient for HPHT wells.",
        counter_arguments=[
            "Standard grades may fail under HPHT conditions.",
            "Regulatory and company standards require HPHT qualification.",
            "Offset failures support enhanced material selection."
        ],
        resolution_strategy="Document material selection, test data, and certification.",
        entity_scope="All DRL04 HPHT wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 5CT Section 7"
    ),
    DoctrineBlock(
        topic="Casing Running and Landing Procedures",
        keywords=["casing running", "landing", "procedures", "well control"],
        conclusion_template="Standardized running and landing procedures must be followed to prevent casing damage and ensure well control.",
        reasoning_framework=(
            "Casing running and landing are critical operations with risk of string damage, stuck pipe, or loss of well control. "
            "API RP 5C1 and company procedures specify running speed, make-up torque, and well control measures. "
            "Pre-job planning, crew training, and contingency planning are required. "
            "Documentation must include procedures, crew qualifications, and incident reports."
        ),
        key_factors=[
            "Running speed and make-up torque",
            "Well control measures",
            "Crew training and qualification",
            "Pre-job planning",
            "Incident reporting"
        ],
        primary_authority=["API RP 5C1", "Company Operations Manual"],
        burden_holder="Operator",
        adversary_position="Standard procedures are overly restrictive.",
        counter_arguments=[
            "Deviation from procedures increases risk.",
            "Regulatory and company standards require compliance.",
            "Incident history supports strict adherence."
        ],
        resolution_strategy="Document procedures and crew training; monitor compliance.",
        entity_scope="All DRL04 casing operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 5C1 Section 5"
    ),
    DoctrineBlock(
        topic="Corrosion Design - H2S and CO2 Service",
        keywords=["corrosion", "H2S", "CO2", "sour service", "casing selection"],
        conclusion_template="Casing exposed to H2S or CO2 must be selected and qualified for sour service in accordance with ISO 15156 and NACE MR0175.",
        reasoning_framework=(
            "Sour service environments (H2S/CO2) pose significant risk of sulfide stress cracking and general corrosion. "
            "ISO 15156 and NACE MR0175 specify material selection, testing, and qualification for sour service. "
            "Material certificates, laboratory test data, and field experience must support selection. "
            "Corrosion inhibitors and monitoring may be required. "
            "Documentation must include material selection rationale and test results."
        ),
        key_factors=[
            "H2S/CO2 concentration",
            "Material qualification",
            "Corrosion inhibitor program",
            "Laboratory test data",
            "Field experience"
        ],
        primary_authority=["ISO 15156", "NACE MR0175", "API 5CT"],
        burden_holder="Operator",
        adversary_position="Standard grades are adequate for mild sour service.",
        counter_arguments=[
            "Even low concentrations can cause failure.",
            "Regulatory and company standards require sour service qualification.",
            "Offset failures support robust material selection."
        ],
        resolution_strategy="Document material selection, test data, and corrosion mitigation.",
        entity_scope="All DRL04 sour service wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 15156 Section 4"
    ),
    DoctrineBlock(
        topic="Expandable Casing Technology - Qualification and Application",
        keywords=["expandable casing", "qualification", "application", "well remediation"],
        conclusion_template="Expandable casing must be qualified for pressure, collapse, and connection integrity prior to application in DRL04 wells.",
        reasoning_framework=(
            "Expandable casing is used for well remediation, diameter preservation, and zonal isolation. "
            "API TR 5C3 and ISO 14310 provide guidance on qualification testing for burst, collapse, and connection integrity. "
            "Field trials and laboratory testing must demonstrate performance under anticipated well conditions. "
            "Documentation must include test results, installation procedures, and post-installation evaluation."
        ),
        key_factors=[
            "Burst and collapse ratings",
            "Connection integrity",
            "Installation procedures",
            "Field trial results",
            "Post-installation evaluation"
        ],
        primary_authority=["API TR 5C3", "ISO 14310", "Company Expandable Policy"],
        burden_holder="Operator",
        adversary_position="Expandable casing is unproven and risky.",
        counter_arguments=[
            "Qualification testing demonstrates reliability.",
            "Field trials support application.",
            "Regulatory and company standards require qualification."
        ],
        resolution_strategy="Document qualification testing and field performance.",
        entity_scope="All DRL04 wells using expandable casing",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 12"
    ),
    DoctrineBlock(
        topic="Casing Design Software Validation",
        keywords=["casing design", "software validation", "QA/QC", "model verification"],
        conclusion_template="All casing design software must be validated and verified against industry standards and field data prior to use.",
        reasoning_framework=(
            "Casing design software is used to model burst, collapse, tensile, and triaxial scenarios. "
            "Validation involves comparing software output to hand calculations, industry standards (API TR 5C3), and field data. "
            "QA/QC procedures must be documented, and software updates must be re-validated. "
            "User training and version control are required. "
            "Documentation must include validation reports and user qualifications."
        ),
        key_factors=[
            "Software validation reports",
            "Comparison to hand calculations",
            "QA/QC procedures",
            "User training",
            "Version control"
        ],
        primary_authority=["API TR 5C3", "Company QA/QC Policy"],
        burden_holder="Operator",
        adversary_position="Software validation is unnecessary for commercial packages.",
        counter_arguments=[
            "Validation ensures accuracy and compliance.",
            "Regulatory and company standards require validation.",
            "Offset incidents support robust QA/QC."
        ],
        resolution_strategy="Maintain validation documentation and user training records.",
        entity_scope="All DRL04 casing design activities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API TR 5C3 Section 13"
    ),
    # --- Additional DoctrineBlocks for comprehensive coverage ---
    DoctrineBlock(
        topic="Casing Float Equipment - Selection and Placement",
        keywords=["float equipment", "casing shoe", "float collar", "cementing"],
        conclusion_template="Float equipment must be selected and placed to ensure effective cementing and prevent backflow during casing operations.",
        reasoning_framework=(
            "Float equipment, including float shoes and collars, prevent cement backflow and support casing during cementing. "
            "Selection must consider pressure rating, compatibility with casing grade, and mud/cement properties. "
            "Placement is typically at the bottom of the casing string, with additional float collars as needed for long strings. "
            "API RP 10F provides testing and selection guidelines. "
            "Documentation must include equipment ratings and placement diagrams."
        ),
        key_factors=[
            "Pressure rating",
            "Compatibility with casing and cement",
            "Placement depth",
            "Mud/cement properties",
            "Equipment testing"
        ],
        primary_authority=["API RP 10F", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Float equipment is unnecessary for short strings.",
        counter_arguments=[
            "Backflow can occur even in short strings.",
            "Regulatory and company standards require float equipment.",
            "Offset failures support robust selection."
        ],
        resolution_strategy="Document equipment selection and placement.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 10F Section 3"
    ),
    DoctrineBlock(
        topic="Casing Accessories - Scratchers and Stop Collars",
        keywords=["casing accessories", "scratchers", "stop collars", "cementing"],
        conclusion_template="Scratchers and stop collars must be used as required to improve mud removal and ensure cement bond quality.",
        reasoning_framework=(
            "Effective mud removal is critical for cement bond quality. "
            "Scratchers and stop collars are used to agitate mud and ensure centralizer placement. "
            "API RP 10D and company standards specify when and where to use these accessories. "
            "Documentation must include accessory type, placement, and justification."
        ),
        key_factors=[
            "Mud removal requirements",
            "Cement bond quality",
            "Well deviation",
            "Accessory type and placement",
            "Regulatory standards"
        ],
        primary_authority=["API RP 10D", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Accessories are unnecessary in vertical wells.",
        counter_arguments=[
            "Even minor deviation can affect cement bond.",
            "Regulatory and company standards require accessories.",
            "Offset failures support robust accessory use."
        ],
        resolution_strategy="Document accessory selection and placement.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10D Section 5"
    ),
    DoctrineBlock(
        topic="Casing Shoe Track Length - Pressure Testing",
        keywords=["casing shoe track", "length", "pressure testing", "well control"],
        conclusion_template="Shoe track length must be sufficient to allow effective pressure testing and prevent cement contamination.",
        reasoning_framework=(
            "The shoe track is the section of casing between the float collar and the casing shoe. "
            "A sufficient length (typically 30-60 ft) allows for effective pressure testing and prevents cement contamination of the float equipment. "
            "API RP 10F and company standards provide guidance on shoe track length. "
            "Documentation must include shoe track length and justification."
        ),
        key_factors=[
            "Pressure testing requirements",
            "Cement contamination risk",
            "Float equipment compatibility",
            "Regulatory standards",
            "Offset well experience"
        ],
        primary_authority=["API RP 10F", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Shorter shoe track reduces cost and time.",
        counter_arguments=[
            "Insufficient shoe track may compromise pressure testing.",
            "Cement contamination can damage float equipment.",
            "Regulatory and company standards specify minimum lengths."
        ],
        resolution_strategy="Document shoe track length and pressure testing results.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API RP 10F Section 4"
    ),
    DoctrineBlock(
        topic="Casing Wear Monitoring - Real-Time Data",
        keywords=["casing wear", "monitoring", "real-time", "drilling operations"],
        conclusion_template="Real-time casing wear monitoring must be implemented in extended reach and high-deviation wells.",
        reasoning_framework=(
            "Real-time monitoring of casing wear using sensors and modeling software allows early detection of excessive wear. "
            "Extended reach and high-deviation wells are particularly vulnerable. "
            "API RP 7G and company standards recommend real-time monitoring for high-risk wells. "
            "Documentation must include monitoring system, data interpretation, and mitigation actions."
        ),
        key_factors=[
            "Well deviation and reach",
            "Wear monitoring system",
            "Data interpretation",
            "Mitigation actions",
            "Regulatory requirements"
        ],
        primary_authority=["API RP 7G", "Company Casing Wear Policy"],
        burden_holder="Operator",
        adversary_position="Real-time monitoring is unnecessary for most wells.",
        counter_arguments=[
            "Early detection prevents catastrophic failure.",
            "Regulatory and company standards require monitoring for high-risk wells.",
            "Offset incidents support real-time monitoring."
        ],
        resolution_strategy="Document monitoring system and mitigation actions.",
        entity_scope="All DRL04 extended reach and high-deviation wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API RP 7G Section 11"
    ),
    DoctrineBlock(
        topic="Casing Centralization - Simulation and Verification",
        keywords=["casing centralization", "simulation", "verification", "cementing"],
        conclusion_template="Centralization must be verified by simulation and, where possible, by field measurement prior to cementing.",
        reasoning_framework=(
            "Simulation of centralizer placement and casing eccentricity is required for all deviated and horizontal wells. "
            "Verification by field measurement (e.g., caliper logs) is recommended where feasible. "
            "API RP 10D and company standards provide guidance on simulation and verification. "
            "Documentation must include simulation results and field measurements."
        ),
        key_factors=[
            "Simulation results",
            "Field measurement (caliper logs)",
            "Well deviation",
            "Centralizer placement",
            "Regulatory standards"
        ],
        primary_authority=["API RP 10D", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Simulation is unnecessary for simple wells.",
        counter_arguments=[
            "Even minor deviation can affect cementing.",
            "Regulatory and company standards require simulation.",
            "Offset failures support robust simulation."
        ],
        resolution_strategy="Document simulation and field measurement results.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10D Section 6"
    ),
    DoctrineBlock(
        topic="Casing Pressure Testing - Acceptance Criteria",
        keywords=["casing pressure testing", "acceptance criteria", "leak-off", "well integrity"],
        conclusion_template="Casing pressure tests must meet acceptance criteria for leak-off and pressure drop as specified by API and company standards.",
        reasoning_framework=(
            "Pressure testing verifies casing integrity after cementing and before drilling out. "
            "API RP 5C1 and company standards specify minimum test pressures, hold times, and allowable pressure drops. "
            "Test failures require investigation and remediation. "
            "Documentation must include test results and remediation actions."
        ),
        key_factors=[
            "Test pressure and hold time",
            "Allowable pressure drop",
            "Leak-off criteria",
            "Remediation actions",
            "Regulatory standards"
        ],
        primary_authority=["API RP 5C1", "Company Operations Manual"],
        burden_holder="Operator",
        adversary_position="Acceptance criteria are overly stringent.",
        counter_arguments=[
            "Stringent criteria ensure well integrity.",
            "Regulatory and company standards require compliance.",
            "Offset failures support robust testing."
        ],
        resolution_strategy="Document test results and remediation actions.",
        entity_scope="All DRL04 casing pressure tests",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 5C1 Section 6"
    ),
    DoctrineBlock(
        topic="Casing Leak Detection - Post-Cementing",
        keywords=["casing leak", "detection", "post-cementing", "well integrity"],
        conclusion_template="Casing leak detection must be performed after cementing using pressure tests and/or logging tools.",
        reasoning_framework=(
            "Leak detection after cementing is critical for ensuring well integrity. "
            "Pressure tests, temperature logs, and noise logs are commonly used. "
            "API RP 10B and company standards specify leak detection methods and acceptance criteria. "
            "Documentation must include test results and remediation actions."
        ),
        key_factors=[
            "Pressure test results",
            "Logging tool data",
            "Acceptance criteria",
            "Remediation actions",
            "Regulatory standards"
        ],
        primary_authority=["API RP 10B", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Leak detection is unnecessary if pressure test passes.",
        counter_arguments=[
            "Some leaks may not be detected by pressure test alone.",
            "Regulatory and company standards require multiple methods.",
            "Offset failures support robust leak detection."
        ],
        resolution_strategy="Document leak detection methods and results.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API RP 10B Section 7"
    ),
    DoctrineBlock(
        topic="Casing Annulus Pressure Management",
        keywords=["casing annulus", "pressure management", "well integrity", "monitoring"],
        conclusion_template="Annulus pressure must be monitored and managed to prevent sustained casing pressure and ensure well integrity.",
        reasoning_framework=(
            "Sustained casing pressure (SCP) can compromise well integrity and lead to regulatory non-compliance. "
            "Continuous monitoring and management of annulus pressure is required. "
            "API RP 90 and company standards specify monitoring frequency, allowable limits, and remediation actions. "
            "Documentation must include monitoring records and remediation actions."
        ),
        key_factors=[
            "Annulus pressure monitoring",
            "Allowable pressure limits",
            "Remediation actions",
            "Regulatory standards",
            "Offset well experience"
        ],
        primary_authority=["API RP 90", "Company Well Integrity Policy"],
        burden_holder="Operator",
        adversary_position="Continuous monitoring is unnecessary for low-risk wells.",
        counter_arguments=[
            "SCP can develop in any well.",
            "Regulatory and company standards require monitoring.",
            "Offset incidents support robust pressure management."
        ],
        resolution_strategy="Document monitoring and remediation actions.",
        entity_scope="All DRL04 wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 90 Section 2"
    ),
    DoctrineBlock(
        topic="Casing Cement Evaluation - Logging and Acceptance",
        keywords=["casing cement", "evaluation", "logging", "acceptance criteria"],
        conclusion_template="Cement evaluation must be performed using logging tools and meet acceptance criteria for zonal isolation.",
        reasoning_framework=(
            "Cement evaluation is critical for verifying zonal isolation. "
            "Logging tools (e.g., CBL, VDL) are used to assess cement bond quality. "
            "API RP 10B and company standards specify acceptance criteria and remediation actions. "
            "Documentation must include log data and acceptance/rejection rationale."
        ),
        key_factors=[
            "Log data (CBL, VDL, etc.)",
            "Acceptance criteria",
            "Remediation actions",
            "Regulatory standards",
            "Offset well experience"
        ],
        primary_authority=["API RP 10B", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Logging is unnecessary if cementing is performed as planned.",
        counter_arguments=[
            "Cementing failures may not be detected visually.",
            "Regulatory and company standards require logging.",
            "Offset failures support robust evaluation."
        ],
        resolution_strategy="Document log data and acceptance/rejection rationale.",
        entity_scope="All DRL04 casing cementing operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10B Section 8"
    ),
    DoctrineBlock(
        topic="Casing Design for Lost Circulation Zones",
        keywords=["casing design", "lost circulation", "well control", "cementing"],
        conclusion_template="Casing design must account for lost circulation zones with appropriate cementing and contingency plans.",
        reasoning_framework=(
            "Lost circulation zones can compromise cementing and well control. "
            "Casing design must include contingency plans such as lightweight cement, stage cementing, or lost circulation materials. "
            "API RP 10B and company standards provide guidance. "
            "Documentation must include lost circulation mitigation plans and results."
        ),
        key_factors=[
            "Lost circulation risk assessment",
            "Cementing contingency plans",
            "Stage cementing",
            "Lost circulation materials",
            "Regulatory standards"
        ],
        primary_authority=["API RP 10B", "Company Cementing Policy"],
        burden_holder="Operator",
        adversary_position="Standard cementing is sufficient.",
        counter_arguments=[
            "Lost circulation can lead to well control incidents.",
            "Regulatory and company standards require contingency planning.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document risk assessment and mitigation plans.",
        entity_scope="All DRL04 wells with lost circulation risk",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API RP 10B Section 9"
    ),
    DoctrineBlock(
        topic="Casing Design for Shallow Gas Zones",
        keywords=["casing design", "shallow gas", "well control", "kick tolerance"],
        conclusion_template="Casing design must ensure well control and kick tolerance in shallow gas zones.",
        reasoning_framework=(
            "Shallow gas zones pose a high risk of blowout and require special casing design considerations. "
            "Kick tolerance calculations, rapid casing installation, and contingency planning are required. "
            "API Bulletin 92 and company standards provide guidance. "
            "Documentation must include kick tolerance analysis and contingency plans."
        ),
        key_factors=[
            "Shallow gas risk assessment",
            "Kick tolerance calculations",
            "Contingency planning",
            "Casing installation procedures",
            "Regulatory standards"
        ],
        primary_authority=["API Bulletin 92", "Company Well Control Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for shallow gas.",
        counter_arguments=[
            "Shallow gas can cause catastrophic blowouts.",
            "Regulatory and company standards require special design.",
            "Offset incidents support robust planning."
        ],
        resolution_strategy="Document risk assessment and kick tolerance analysis.",
        entity_scope="All DRL04 wells with shallow gas risk",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API Bulletin 92 Section 4"
    ),
    DoctrineBlock(
        topic="Casing Design for Salt Zones",
        keywords=["casing design", "salt zones", "wellbore stability", "creep"],
        conclusion_template="Casing design must account for salt zone creep and wellbore stability.",
        reasoning_framework=(
            "Salt zones can deform over time (creep), leading to casing collapse or buckling. "
            "Casing design must include enhanced collapse resistance, centralization, and cementing practices. "
            "API TR 5C3 and company standards provide guidance. "
            "Documentation must include salt zone risk assessment and design modifications."
        ),
        key_factors=[
            "Salt zone identification",
            "Collapse resistance",
            "Wellbore stability analysis",
            "Centralization and cementing",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "Company Salt Zone Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for salt zones.",
        counter_arguments=[
            "Salt creep can cause catastrophic casing failure.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document salt zone risk assessment and design modifications.",
        entity_scope="All DRL04 wells intersecting salt zones",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 14"
    ),
    DoctrineBlock(
        topic="Casing Design for Permafrost Zones",
        keywords=["casing design", "permafrost", "thermal stress", "well integrity"],
        conclusion_template="Casing design must account for thermal stress and thaw settlement in permafrost zones.",
        reasoning_framework=(
            "Permafrost zones require special casing design to accommodate thermal stress and potential thaw settlement. "
            "Casing must be insulated or designed to minimize heat transfer. "
            "API RP 65 and company standards provide guidance. "
            "Documentation must include permafrost risk assessment and design modifications."
        ),
        key_factors=[
            "Permafrost identification",
            "Thermal stress analysis",
            "Insulation requirements",
            "Thaw settlement risk",
            "Regulatory standards"
        ],
        primary_authority=["API RP 65", "Company Permafrost Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for permafrost.",
        counter_arguments=[
            "Thaw settlement can cause casing collapse.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document permafrost risk assessment and design modifications.",
        entity_scope="All DRL04 wells in permafrost regions",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API RP 65 Section 6"
    ),
    DoctrineBlock(
        topic="Casing Design for Abandonment",
        keywords=["casing design", "abandonment", "well integrity", "zonal isolation"],
        conclusion_template="Casing design must facilitate future well abandonment and ensure long-term zonal isolation.",
        reasoning_framework=(
            "Well abandonment requires long-term integrity of casing and cement. "
            "Casing design must facilitate placement of abandonment plugs and ensure compatibility with abandonment materials. "
            "API RP 65 and company standards provide guidance. "
            "Documentation must include abandonment planning and design considerations."
        ),
        key_factors=[
            "Abandonment planning",
            "Plug placement",
            "Material compatibility",
            "Long-term integrity",
            "Regulatory standards"
        ],
        primary_authority=["API RP 65", "Company Abandonment Policy"],
        burden_holder="Operator",
        adversary_position="Abandonment is a future concern.",
        counter_arguments=[
            "Design decisions impact future abandonment.",
            "Regulatory and company standards require planning.",
            "Offset failures support robust abandonment design."
        ],
        resolution_strategy="Document abandonment planning and design considerations.",
        entity_scope="All DRL04 wells",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API RP 65 Section 7"
    ),
    DoctrineBlock(
        topic="Casing Design for Multi-Lateral Wells",
        keywords=["casing design", "multi-lateral", "junction integrity", "zonal isolation"],
        conclusion_template="Casing design for multi-lateral wells must ensure junction integrity and zonal isolation.",
        reasoning_framework=(
            "Multi-lateral wells require special casing design to ensure integrity at junctions and maintain zonal isolation. "
            "API TR 5C3 and company standards provide guidance on junction qualification and cementing. "
            "Documentation must include junction design, qualification test results, and cementing plans."
        ),
        key_factors=[
            "Junction design and qualification",
            "Zonal isolation",
            "Cementing plans",
            "Regulatory standards",
            "Offset well experience"
        ],
        primary_authority=["API TR 5C3", "Company Multi-Lateral Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for multi-laterals.",
        counter_arguments=[
            "Junction failure can compromise well integrity.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust qualification."
        ],
        resolution_strategy="Document junction design and qualification.",
        entity_scope="All DRL04 multi-lateral wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 15"
    ),
    DoctrineBlock(
        topic="Casing Design for Geothermal Wells",
        keywords=["casing design", "geothermal", "thermal cycling", "well integrity"],
        conclusion_template="Casing design for geothermal wells must account for thermal cycling and expansion/contraction.",
        reasoning_framework=(
            "Geothermal wells experience significant thermal cycling, leading to casing expansion and contraction. "
            "Material selection, centralization, and cementing practices must accommodate thermal movement. "
            "API 5CT and company standards provide guidance. "
            "Documentation must include thermal analysis and design modifications."
        ),
        key_factors=[
            "Thermal cycling analysis",
            "Material selection",
            "Centralization",
            "Cementing practices",
            "Regulatory standards"
        ],
        primary_authority=["API 5CT", "Company Geothermal Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for geothermal wells.",
        counter_arguments=[
            "Thermal cycling can cause casing failure.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document thermal analysis and design modifications.",
        entity_scope="All DRL04 geothermal wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API 5CT Section 8"
    ),
    DoctrineBlock(
        topic="Casing Design for CO2 Sequestration Wells",
        keywords=["casing design", "CO2 sequestration", "corrosion", "well integrity"],
        conclusion_template="Casing design for CO2 sequestration wells must ensure long-term corrosion resistance and well integrity.",
        reasoning_framework=(
            "CO2 sequestration wells require casing with enhanced corrosion resistance and long-term integrity. "
            "Material selection, cementing, and monitoring must be robust. "
            "ISO 15156 and company standards provide guidance. "
            "Documentation must include corrosion analysis and long-term monitoring plans."
        ),
        key_factors=[
            "CO2 corrosion analysis",
            "Material selection",
            "Cementing practices",
            "Long-term monitoring",
            "Regulatory standards"
        ],
        primary_authority=["ISO 15156", "Company CO2 Sequestration Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for CO2 wells.",
        counter_arguments=[
            "CO2 can cause rapid corrosion.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document corrosion analysis and monitoring plans.",
        entity_scope="All DRL04 CO2 sequestration wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="ISO 15156 Section 5"
    ),
    DoctrineBlock(
        topic="Casing Design for High Angle and Horizontal Wells",
        keywords=["casing design", "high angle", "horizontal", "centralization", "casing wear"],
        conclusion_template="Casing design for high angle and horizontal wells must ensure enhanced centralization and wear resistance.",
        reasoning_framework=(
            "High angle and horizontal wells require special attention to centralization and casing wear. "
            "Centralizer placement, wear-resistant materials, and real-time monitoring are recommended. "
            "API RP 10D and company standards provide guidance. "
            "Documentation must include centralization and wear mitigation plans."
        ),
        key_factors=[
            "Well trajectory",
            "Centralizer placement",
            "Wear-resistant materials",
            "Real-time monitoring",
            "Regulatory standards"
        ],
        primary_authority=["API RP 10D", "Company Horizontal Well Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for horizontal wells.",
        counter_arguments=[
            "High deviation increases wear risk.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document centralization and wear mitigation plans.",
        entity_scope="All DRL04 high angle and horizontal wells",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API RP 10D Section 7"
    ),
    DoctrineBlock(
        topic="Casing Design for Deepwater Wells",
        keywords=["casing design", "deepwater", "well control", "collapse resistance"],
        conclusion_template="Casing design for deepwater wells must ensure enhanced collapse resistance and well control.",
        reasoning_framework=(
            "Deepwater wells experience high external pressures and require casing with enhanced collapse resistance. "
            "Well control and cementing practices must be robust. "
            "API TR 5C3 and company standards provide guidance. "
            "Documentation must include collapse analysis and well control plans."
        ),
        key_factors=[
            "External pressure analysis",
            "Collapse resistance",
            "Well control plans",
            "Cementing practices",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "Company Deepwater Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for deepwater wells.",
        counter_arguments=[
            "High external pressure increases collapse risk.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document collapse analysis and well control plans.",
        entity_scope="All DRL04 deepwater wells",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 16"
    ),
    DoctrineBlock(
        topic="Casing Design for HPHT Gas Condensate Wells",
        keywords=["casing design", "HPHT", "gas condensate", "premium connections"],
        conclusion_template="Casing design for HPHT gas condensate wells must use premium connections and materials qualified for high pressure and temperature.",
        reasoning_framework=(
            "HPHT gas condensate wells require casing and connections qualified for high pressure, temperature, and sour service. "
            "Premium connections and enhanced material grades are required. "
            "ISO 13679 and company standards provide guidance. "
            "Documentation must include qualification test results and selection rationale."
        ),
        key_factors=[
            "Pressure and temperature ratings",
            "Premium connection qualification",
            "Material selection",
            "Sour service compatibility",
            "Regulatory standards"
        ],
        primary_authority=["ISO 13679", "Company HPHT Policy"],
        burden_holder="Operator",
        adversary_position="Standard connections are sufficient.",
        counter_arguments=[
            "HPHT conditions require premium qualification.",
            "Regulatory and company standards require compliance.",
            "Offset failures support robust selection."
        ],
        resolution_strategy="Document qualification test results and selection rationale.",
        entity_scope="All DRL04 HPHT gas condensate wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 13679 Section 6"
    ),
    DoctrineBlock(
        topic="Casing Design for Unconventional Wells",
        keywords=["casing design", "unconventional", "hydraulic fracturing", "burst resistance"],
        conclusion_template="Casing design for unconventional wells must ensure burst resistance for hydraulic fracturing operations.",
        reasoning_framework=(
            "Unconventional wells (e.g., shale, tight gas) require casing with enhanced burst resistance for hydraulic fracturing. "
            "API TR 5C3 and company standards provide guidance. "
            "Documentation must include burst analysis and fracturing plans."
        ),
        key_factors=[
            "Hydraulic fracturing pressure",
            "Burst resistance",
            "Material selection",
            "Cementing practices",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "Company Unconventional Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for unconventional wells.",
        counter_arguments=[
            "Fracturing pressures can exceed standard ratings.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document burst analysis and fracturing plans.",
        entity_scope="All DRL04 unconventional wells",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 17"
    ),
    DoctrineBlock(
        topic="Casing Design for Slimhole Wells",
        keywords=["casing design", "slimhole", "diameter preservation", "expandable casing"],
        conclusion_template="Casing design for slimhole wells must ensure diameter preservation and may require expandable casing.",
        reasoning_framework=(
            "Slimhole wells require careful diameter management to avoid restrictions. "
            "Expandable casing may be used to preserve diameter. "
            "API TR 5C3 and company standards provide guidance. "
            "Documentation must include diameter analysis and expandable casing qualification."
        ),
        key_factors=[
            "Diameter analysis",
            "Expandable casing qualification",
            "Cementing practices",
            "Material selection",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "Company Slimhole Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for slimhole wells.",
        counter_arguments=[
            "Diameter loss can compromise well objectives.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document diameter analysis and expandable casing qualification.",
        entity_scope="All DRL04 slimhole wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 18"
    ),
    DoctrineBlock(
        topic="Casing Design for HPHT Oil Wells",
        keywords=["casing design", "HPHT", "oil", "material selection"],
        conclusion_template="Casing design for HPHT oil wells must use materials and connections qualified for high pressure, temperature, and sour service.",
        reasoning_framework=(
            "HPHT oil wells require casing and connections with enhanced ratings for pressure, temperature, and sour service. "
            "API 5CT, ISO 15156, and ISO 13679 provide guidance. "
            "Documentation must include qualification test results and selection rationale."
        ),
        key_factors=[
            "Pressure and temperature ratings",
            "Material selection",
            "Premium connection qualification",
            "Sour service compatibility",
            "Regulatory standards"
        ],
        primary_authority=["API 5CT", "ISO 15156", "ISO 13679"],
        burden_holder="Operator",
        adversary_position="Standard materials are sufficient.",
        counter_arguments=[
            "HPHT conditions require enhanced qualification.",
            "Regulatory and company standards require compliance.",
            "Offset failures support robust selection."
        ],
        resolution_strategy="Document qualification test results and selection rationale.",
        entity_scope="All DRL04 HPHT oil wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 5CT Section 9"
    ),
    DoctrineBlock(
        topic="Casing Design for High Dogleg Severity Wells",
        keywords=["casing design", "dogleg severity", "fatigue", "casing wear"],
        conclusion_template="Casing design for high dogleg severity wells must address fatigue and wear risks.",
        reasoning_framework=(
            "High dogleg severity increases casing fatigue and wear risk. "
            "Material selection, centralization, and wear mitigation are critical. "
            "API RP 7G and company standards provide guidance. "
            "Documentation must include fatigue analysis and wear mitigation plans."
        ),
        key_factors=[
            "Dogleg severity analysis",
            "Fatigue analysis",
            "Centralization",
            "Wear mitigation",
            "Regulatory standards"
        ],
        primary_authority=["API RP 7G", "Company Dogleg Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for high doglegs.",
        counter_arguments=[
            "High doglegs increase fatigue and wear.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document fatigue analysis and wear mitigation plans.",
        entity_scope="All DRL04 high dogleg wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="API RP 7G Section 12"
    ),
    DoctrineBlock(
        topic="Casing Design for HTHP Exploration Wells",
        keywords=["casing design", "HTHP", "exploration", "material selection"],
        conclusion_template="Casing design for HTHP exploration wells must use materials and connections qualified for extreme pressure and temperature.",
        reasoning_framework=(
            "HTHP exploration wells require casing and connections with the highest ratings for pressure and temperature. "
            "API 5CT, ISO 15156, and ISO 13679 provide guidance. "
            "Documentation must include qualification test results and selection rationale."
        ),
        key_factors=[
            "Pressure and temperature ratings",
            "Material selection",
            "Premium connection qualification",
            "Sour service compatibility",
            "Regulatory standards"
        ],
        primary_authority=["API 5CT", "ISO 15156", "ISO 13679"],
        burden_holder="Operator",
        adversary_position="Standard materials are sufficient.",
        counter_arguments=[
            "HTHP conditions require enhanced qualification.",
            "Regulatory and company standards require compliance.",
            "Offset failures support robust selection."
        ],
        resolution_strategy="Document qualification test results and selection rationale.",
        entity_scope="All DRL04 HTHP exploration wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 5CT Section 10"
    ),
    DoctrineBlock(
        topic="Casing Design for Subsea Wells",
        keywords=["casing design", "subsea", "wellhead", "collapse resistance"],
        conclusion_template="Casing design for subsea wells must ensure wellhead support and enhanced collapse resistance.",
        reasoning_framework=(
            "Subsea wells require casing with enhanced collapse resistance and wellhead support. "
            "API TR 5C3 and company standards provide guidance. "
            "Documentation must include collapse analysis and wellhead support plans."
        ),
        key_factors=[
            "Wellhead support analysis",
            "Collapse resistance",
            "Cementing practices",
            "Material selection",
            "Regulatory standards"
        ],
        primary_authority=["API TR 5C3", "Company Subsea Policy"],
        burden_holder="Operator",
        adversary_position="Standard design is sufficient for subsea wells.",
        counter_arguments=[
            "Subsea conditions increase collapse risk.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document collapse analysis and wellhead support plans.",
        entity_scope="All DRL04 subsea wells",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="API TR 5C3 Section 19"
    ),
    DoctrineBlock(
        topic="Casing Design for Sour Gas Wells",
        keywords=["casing design", "sour gas", "H2S", "corrosion resistance"],
        conclusion_template="Casing design for sour gas wells must use materials qualified for H2S service in accordance with ISO 15156.",
        reasoning_framework=(
            "Sour gas wells require casing with enhanced H2S resistance. "
            "ISO 15156 and company standards provide guidance. "
            "Documentation must include material qualification and corrosion analysis."
        ),
        key_factors=[
            "H2S concentration",
            "Material qualification",
            "Corrosion analysis",
            "Cementing practices",
            "Regulatory standards"
        ],
        primary_authority=["ISO 15156", "Company Sour Gas Policy"],
        burden_holder="Operator",
        adversary_position="Standard materials are sufficient for sour gas.",
        counter_arguments=[
            "H2S can cause rapid failure.",
            "Regulatory and company standards require special design.",
            "Offset failures support robust mitigation."
        ],
        resolution_strategy="Document material qualification and corrosion analysis.",
        entity_scope="All DRL04 sour gas wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 15156 Section 6"
    ),
    DoctrineBlock(
        topic="Casing Design for HPHT Exploration Gas Wells",
        keywords=["casing design", "HPHT", "exploration gas", "premium connections"],
        conclusion_template="Casing design for HPHT exploration gas wells must use premium connections and materials qualified for high pressure and temperature.",
        reasoning_framework=(
            "HPHT exploration gas wells require casing and connections with the highest ratings for pressure, temperature, and sour service. "
            "ISO 13679 and company standards provide guidance. "
            "Documentation must include qualification test results and selection rationale."
        ),
        key_factors=[
            "Pressure and temperature ratings",
            "Premium connection qualification",
            "Material selection",
            "Sour service compatibility",
            "Regulatory standards"
        ],
        primary_authority=["ISO 13679", "Company HPHT Policy"],
        burden_holder="Operator",
        adversary_position="Standard connections are sufficient.",
        counter_arguments=[
            "HPHT conditions require premium qualification.",
            "Regulatory and company standards require compliance.",
            "Offset failures support robust selection."
        ],
        resolution_strategy="Document qualification test results and selection rationale.",
        entity_scope="All DRL04 HPHT exploration gas wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 13679 Section 7"
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