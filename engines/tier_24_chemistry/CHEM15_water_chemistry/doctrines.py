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
        topic="pH_control_treatment_systems",
        keywords=["pH", "control", "treatment", "neutralization", "alkalinity", "acid dosing", "base dosing"],
        conclusion_template="pH must be maintained within the optimal range for the specific treatment process, typically 6.5-8.5 for potable water, to ensure process efficacy and regulatory compliance.",
        reasoning_framework=(
            "1. Identify the target pH range based on downstream process requirements and regulatory standards.\n"
            "2. Assess raw water pH and buffering capacity (alkalinity).\n"
            "3. Select appropriate acid or base for dosing (e.g., sulfuric acid, sodium hydroxide).\n"
            "4. Calculate required chemical dose considering flow rate, alkalinity, and desired pH shift.\n"
            "5. Implement feedback control using online pH sensors and automated dosing pumps.\n"
            "6. Monitor effluent pH and adjust setpoints as needed.\n"
            "7. Document compliance with NPDES or SDWA pH limits.\n"
            "8. Evaluate impacts on corrosion, scaling, and disinfection efficacy.\n"
            "9. Review historical data for process optimization.\n"
            "10. Ensure operator training and maintenance of pH control equipment."
        ),
        key_factors=[
            "Raw water pH and alkalinity",
            "Target pH for process and compliance",
            "Chemical selection and dosing accuracy",
            "Sensor calibration and reliability",
            "Regulatory limits (e.g., NPDES, SDWA)"
        ],
        primary_authority=[
            "EPA National Primary Drinking Water Regulations",
            "40 CFR 136",
            "AWWA Standard B201"
        ],
        burden_holder="Treatment plant operator",
        adversary_position="pH control is unnecessary if downstream processes are robust.",
        counter_arguments=[
            "Improper pH can reduce disinfection efficacy.",
            "Corrosion and scaling risks increase outside optimal pH.",
            "Regulatory violations may occur without pH control."
        ],
        resolution_strategy="Implement automated pH control with continuous monitoring and regular calibration.",
        entity_scope="Water treatment plants, industrial pretreatment, distribution systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Guidance Manual for Compliance with the Filtration and Disinfection Requirements for Public Water Systems"
    ),
    DoctrineBlock(
        topic="langelier_saturation_index_lsi",
        keywords=["LSI", "Langelier Index", "scaling", "corrosion", "calcium carbonate", "water stability"],
        conclusion_template="The Langelier Saturation Index (LSI) must be calculated to assess the scaling or corrosive potential of water, maintaining LSI between -0.5 and +0.5 for optimal system protection.",
        reasoning_framework=(
            "1. Measure water parameters: pH, temperature, calcium hardness, alkalinity, total dissolved solids (TDS).\n"
            "2. Calculate LSI using the standard formula: LSI = pH - pHs, where pHs is the pH at which water is saturated with calcium carbonate.\n"
            "3. Interpret LSI:\n"
            "   - LSI < 0: Water is undersaturated (corrosive).\n"
            "   - LSI = 0: Water is at equilibrium.\n"
            "   - LSI > 0: Water is oversaturated (scaling tendency).\n"
            "4. Adjust treatment (e.g., pH, alkalinity, hardness) to maintain LSI near zero.\n"
            "5. Monitor system for evidence of scaling or corrosion.\n"
            "6. Document LSI calculations for compliance and operational records."
        ),
        key_factors=[
            "pH",
            "Calcium hardness",
            "Alkalinity",
            "Temperature",
            "TDS"
        ],
        primary_authority=[
            "AWWA Manual M58",
            "EPA Corrosion Control Guidance",
            "Standard Methods 2330"
        ],
        burden_holder="Water quality manager",
        adversary_position="LSI is not necessary if corrosion inhibitors are used.",
        counter_arguments=[
            "LSI provides a predictive measure for both scaling and corrosion.",
            "Corrosion inhibitors may not address underlying water chemistry.",
            "Regulatory agencies may require LSI documentation."
        ],
        resolution_strategy="Integrate LSI calculation into routine water quality monitoring and adjust treatment accordingly.",
        entity_scope="Municipal and industrial water systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AWWA M58: Internal Corrosion Control in Water Distribution Systems"
    ),
    DoctrineBlock(
        topic="coagulation_flocculation_jar_testing",
        keywords=["coagulation", "flocculation", "jar test", "alum", "polymer", "turbidity removal"],
        conclusion_template="Jar testing must be performed to optimize coagulant and polymer dosages for effective turbidity and contaminant removal.",
        reasoning_framework=(
            "1. Collect representative raw water samples.\n"
            "2. Select coagulants (e.g., alum, ferric chloride) and polymers for testing.\n"
            "3. Prepare a series of jars with varying dosages.\n"
            "4. Rapid mix to disperse chemicals, followed by slow mixing for floc formation.\n"
            "5. Allow settling and measure turbidity in supernatant.\n"
            "6. Identify optimal dose based on lowest turbidity and best floc characteristics.\n"
            "7. Repeat as needed for seasonal or source water changes.\n"
            "8. Document results for process control."
        ),
        key_factors=[
            "Raw water quality (turbidity, TOC, color)",
            "Coagulant and polymer type",
            "Mixing intensity and duration",
            "Settling time",
            "Temperature"
        ],
        primary_authority=[
            "Standard Methods 2540",
            "AWWA C401",
            "EPA Jar Testing Guidance"
        ],
        burden_holder="Process engineer",
        adversary_position="Jar testing is unnecessary with fixed dosing.",
        counter_arguments=[
            "Raw water quality varies seasonally.",
            "Overdosing increases sludge production and cost.",
            "Underdosing reduces contaminant removal."
        ],
        resolution_strategy="Conduct regular jar tests and adjust dosing accordingly.",
        entity_scope="Surface water treatment plants",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA Surface Water Treatment Rule Guidance Manual"
    ),
    DoctrineBlock(
        topic="chlorination_disinfection_ct_values",
        keywords=["chlorination", "disinfection", "CT", "contact time", "residual", "pathogen inactivation"],
        conclusion_template="Chlorine dose and contact time (CT) must meet or exceed regulatory requirements for inactivation of target pathogens, with CT values documented and verified.",
        reasoning_framework=(
            "1. Identify target pathogens (e.g., Giardia, viruses) and required log inactivation.\n"
            "2. Determine minimum CT value from EPA or state regulations.\n"
            "3. Measure chlorine residual and water temperature.\n"
            "4. Calculate actual CT: CT = residual (mg/L) × contact time (min).\n"
            "5. Adjust chlorine dose or contact time to achieve required CT.\n"
            "6. Monitor and record CT values continuously.\n"
            "7. Maintain backup disinfection systems as needed.\n"
            "8. Document compliance for regulatory reporting."
        ),
        key_factors=[
            "Chlorine residual",
            "Contact time",
            "Temperature",
            "pH",
            "Target pathogens"
        ],
        primary_authority=[
            "EPA Surface Water Treatment Rule",
            "40 CFR 141.72",
            "AWWA C652"
        ],
        burden_holder="Disinfection supervisor",
        adversary_position="High chlorine doses alone ensure disinfection.",
        counter_arguments=[
            "Contact time is critical for pathogen inactivation.",
            "High doses may create disinfection byproducts.",
            "Regulatory compliance requires CT documentation."
        ],
        resolution_strategy="Automate CT calculation and integrate alarms for non-compliance.",
        entity_scope="Municipal water treatment, distribution systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Guidance Manual for Compliance with the Filtration and Disinfection Requirements"
    ),
    DoctrineBlock(
        topic="membrane_filtration_microfiltration_ultrafiltration",
        keywords=["membrane filtration", "microfiltration", "ultrafiltration", "pathogen removal", "turbidity", "integrity testing"],
        conclusion_template="Membrane filtration systems must achieve required log removal credits for pathogens and maintain integrity through regular testing and monitoring.",
        reasoning_framework=(
            "1. Select membrane type (microfiltration or ultrafiltration) based on target contaminants and regulatory requirements.\n"
            "2. Design system to achieve required log removal (e.g., 2-log for Giardia, 3-log for viruses).\n"
            "3. Monitor turbidity and particle counts in filtrate.\n"
            "4. Conduct integrity tests (e.g., pressure decay, diffusive air) at required intervals.\n"
            "5. Record and review integrity test results.\n"
            "6. Respond to integrity breaches with corrective action and notification.\n"
            "7. Maintain membrane cleaning and replacement schedules.\n"
            "8. Document compliance for regulatory reporting."
        ),
        key_factors=[
            "Membrane pore size",
            "Integrity testing frequency",
            "Filtrate turbidity",
            "Log removal requirements",
            "Cleaning protocols"
        ],
        primary_authority=[
            "EPA Membrane Filtration Guidance Manual",
            "40 CFR 141.403",
            "AWWA M53"
        ],
        burden_holder="Membrane system operator",
        adversary_position="Membrane systems are inherently reliable and do not require frequent testing.",
        counter_arguments=[
            "Membrane breaches can occur due to fouling or damage.",
            "Regulations require documented integrity testing.",
            "Undetected failures can lead to pathogen breakthrough."
        ],
        resolution_strategy="Implement automated integrity testing and alarm systems.",
        entity_scope="Municipal and industrial membrane filtration plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Membrane Filtration Guidance Manual"
    ),
    DoctrineBlock(
        topic="produced_water_oil_removal_daf",
        keywords=["produced water", "oil removal", "DAF", "dissolved air flotation", "hydrocarbons", "pretreatment"],
        conclusion_template="Produced water must undergo oil removal using dissolved air flotation (DAF) or equivalent technology to meet discharge or reuse standards.",
        reasoning_framework=(
            "1. Characterize produced water for oil and grease content.\n"
            "2. Select DAF or alternative technology based on influent quality and required effluent limits.\n"
            "3. Optimize chemical addition (e.g., coagulants, flocculants) for effective separation.\n"
            "4. Adjust air-to-solids ratio and recycle rates for efficient flotation.\n"
            "5. Monitor effluent oil and grease concentrations.\n"
            "6. Maintain equipment and monitor for upsets.\n"
            "7. Document compliance with NPDES or reuse criteria."
        ),
        key_factors=[
            "Influent oil and grease concentration",
            "DAF design and operation",
            "Chemical dosing",
            "Effluent standards",
            "Sludge management"
        ],
        primary_authority=[
            "EPA Oil and Grease Test Method 1664",
            "40 CFR 435",
            "API RP 421"
        ],
        burden_holder="Produced water treatment operator",
        adversary_position="Gravity separation is sufficient for oil removal.",
        counter_arguments=[
            "DAF achieves lower effluent oil concentrations.",
            "Gravity separation may not meet regulatory limits.",
            "DAF allows for chemical enhancement and finer control."
        ],
        resolution_strategy="Incorporate DAF with online monitoring and periodic performance reviews.",
        entity_scope="Oil and gas produced water treatment",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 421: Design and Operation of Produced Water Treatment Systems"
    ),
    DoctrineBlock(
        topic="ion_exchange_water_softening",
        keywords=["ion exchange", "water softening", "hardness removal", "resin", "regeneration", "calcium", "magnesium"],
        conclusion_template="Ion exchange softening must be operated and regenerated to maintain effluent hardness below specified limits, preventing scaling and ensuring compliance.",
        reasoning_framework=(
            "1. Analyze influent hardness (calcium and magnesium).\n"
            "2. Select appropriate ion exchange resin and system configuration.\n"
            "3. Monitor effluent hardness and schedule regeneration based on breakthrough.\n"
            "4. Use sodium chloride or potassium chloride for resin regeneration.\n"
            "5. Control regeneration frequency to minimize salt usage and waste generation.\n"
            "6. Maintain resin integrity through periodic cleaning and replacement.\n"
            "7. Document operational data and compliance with discharge or reuse standards."
        ),
        key_factors=[
            "Influent and effluent hardness",
            "Resin type and condition",
            "Regeneration frequency",
            "Salt dosage",
            "Waste brine management"
        ],
        primary_authority=[
            "AWWA B200",
            "EPA Water Softening Guidance",
            "Standard Methods 2340"
        ],
        burden_holder="Softening system operator",
        adversary_position="Softening is unnecessary if scaling is not observed.",
        counter_arguments=[
            "Hardness can cause scaling in downstream equipment.",
            "Regulatory or customer limits may require softening.",
            "Proactive softening reduces maintenance costs."
        ],
        resolution_strategy="Automate regeneration based on online hardness monitoring.",
        entity_scope="Municipal, industrial, and commercial water softening",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AWWA B200: Softening and Ion Exchange Processes"
    ),
    DoctrineBlock(
        topic="npdes_permit_discharge_limits",
        keywords=["NPDES", "permit", "discharge", "limits", "compliance", "monitoring", "reporting"],
        conclusion_template="All discharges must comply with NPDES permit limits, with continuous monitoring and timely reporting to regulatory agencies.",
        reasoning_framework=(
            "1. Review NPDES permit for applicable discharge limits and monitoring requirements.\n"
            "2. Implement sampling and analysis plan for all regulated parameters.\n"
            "3. Maintain continuous or frequent monitoring for critical parameters (e.g., pH, flow, oil and grease).\n"
            "4. Record and review monitoring data for compliance.\n"
            "5. Report exceedances and submit Discharge Monitoring Reports (DMRs) as required.\n"
            "6. Investigate and correct causes of non-compliance.\n"
            "7. Maintain records for regulatory inspections."
        ),
        key_factors=[
            "Permit limits for each parameter",
            "Sampling and analysis frequency",
            "Data integrity",
            "Reporting deadlines",
            "Corrective action procedures"
        ],
        primary_authority=[
            "40 CFR 122",
            "EPA NPDES Permit Writers’ Manual",
            "State environmental agencies"
        ],
        burden_holder="Permittee (facility owner/operator)",
        adversary_position="Occasional exceedances are acceptable if average values are compliant.",
        counter_arguments=[
            "Permits require compliance at all times.",
            "Chronic exceedances can result in enforcement actions.",
            "Timely reporting is a legal obligation."
        ],
        resolution_strategy="Establish robust compliance monitoring and reporting systems.",
        entity_scope="All NPDES-permitted facilities",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="40 CFR 122: EPA Administered Permit Programs"
    ),
    DoctrineBlock(
        topic="safe_drinking_water_act_mcl_compliance",
        keywords=["SDWA", "MCL", "maximum contaminant level", "compliance", "drinking water", "regulations"],
        conclusion_template="Finished water must comply with all applicable Maximum Contaminant Levels (MCLs) as set by the Safe Drinking Water Act.",
        reasoning_framework=(
            "1. Identify all regulated contaminants and their MCLs.\n"
            "2. Implement monitoring for each contaminant at required frequencies.\n"
            "3. Compare analytical results to MCLs and take corrective action if exceeded.\n"
            "4. Notify public and regulatory agencies of MCL violations as required.\n"
            "5. Maintain records of monitoring and corrective actions.\n"
            "6. Review new or revised MCLs and update treatment as necessary."
        ),
        key_factors=[
            "List of regulated contaminants",
            "Analytical methods and detection limits",
            "Monitoring frequency",
            "Public notification requirements",
            "Corrective action procedures"
        ],
        primary_authority=[
            "Safe Drinking Water Act (SDWA)",
            "40 CFR 141",
            "EPA National Primary Drinking Water Regulations"
        ],
        burden_holder="Public water system owner/operator",
        adversary_position="Short-term MCL exceedances do not require action.",
        counter_arguments=[
            "MCLs are enforceable at all times.",
            "Public health may be at risk during exceedances.",
            "Regulatory penalties apply for non-compliance."
        ],
        resolution_strategy="Implement robust monitoring and rapid response protocols.",
        entity_scope="Community and non-community water systems",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="40 CFR 141: National Primary Drinking Water Regulations"
    ),
    DoctrineBlock(
        topic="reverse_osmosis_desalination_design",
        keywords=["reverse osmosis", "RO", "desalination", "membrane", "design", "pretreatment", "scaling"],
        conclusion_template="Reverse osmosis systems must be designed with appropriate pretreatment, membrane selection, and operational controls to ensure reliable desalination and minimize fouling.",
        reasoning_framework=(
            "1. Characterize feedwater for salinity, silt density index (SDI), and scaling potential.\n"
            "2. Design pretreatment (e.g., filtration, antiscalant dosing) to protect membranes.\n"
            "3. Select membrane type and array configuration for target recovery and rejection.\n"
            "4. Control operating parameters (pressure, flux, crossflow velocity) to minimize fouling.\n"
            "5. Monitor permeate quality and system performance.\n"
            "6. Schedule regular cleaning and membrane replacement.\n"
            "7. Document operational data for compliance and optimization."
        ),
        key_factors=[
            "Feedwater quality",
            "Pretreatment effectiveness",
            "Membrane selection",
            "Operating conditions",
            "Cleaning protocols"
        ],
        primary_authority=[
            "AWWA M46",
            "EPA Desalination and Membrane Technology Fact Sheet",
            "Standard Methods 9221"
        ],
        burden_holder="RO system designer/operator",
        adversary_position="RO can operate reliably without extensive pretreatment.",
        counter_arguments=[
            "Fouling and scaling reduce membrane life and performance.",
            "Pretreatment is essential for regulatory compliance.",
            "Operational costs increase without proper design."
        ],
        resolution_strategy="Integrate pretreatment and real-time monitoring into RO system design.",
        entity_scope="Municipal and industrial desalination plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AWWA M46: Reverse Osmosis and Nanofiltration"
    ),
    DoctrineBlock(
        topic="uv_disinfection_cryptosporidium",
        keywords=["UV disinfection", "Cryptosporidium", "inactivation", "dose", "validation", "log removal"],
        conclusion_template="UV disinfection systems must deliver validated doses to achieve required log inactivation of Cryptosporidium and other pathogens.",
        reasoning_framework=(
            "1. Determine required log inactivation for Cryptosporidium (e.g., 3-log).\n"
            "2. Select UV system validated for target dose and flow conditions.\n"
            "3. Monitor UV intensity, flow rate, and transmittance.\n"
            "4. Calculate delivered UV dose and verify compliance with validation reports.\n"
            "5. Respond to alarms or low-dose events with corrective action.\n"
            "6. Maintain lamp replacement and cleaning schedules.\n"
            "7. Document UV system performance and compliance."
        ),
        key_factors=[
            "Required log inactivation",
            "UV dose (mJ/cm2)",
            "System validation",
            "Lamp intensity and maintenance",
            "Water UV transmittance"
        ],
        primary_authority=[
            "EPA UV Disinfection Guidance Manual",
            "40 CFR 141.720",
            "AWWA C653"
        ],
        burden_holder="UV system operator",
        adversary_position="UV dose calculations are unnecessary if system is certified.",
        counter_arguments=[
            "Site-specific validation is required.",
            "Lamp aging and fouling reduce dose.",
            "Continuous monitoring is mandated by regulations."
        ],
        resolution_strategy="Automate UV dose monitoring and integrate with SCADA alarms.",
        entity_scope="Surface water and groundwater treatment plants",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA UV Disinfection Guidance Manual"
    ),
    DoctrineBlock(
        topic="water_quality_parameters_monitoring",
        keywords=["water quality", "monitoring", "parameters", "sampling", "compliance", "continuous monitoring"],
        conclusion_template="All required water quality parameters must be monitored at specified frequencies to ensure compliance and optimize treatment processes.",
        reasoning_framework=(
            "1. Identify all parameters required by permit or regulation (e.g., turbidity, chlorine, pH, TOC).\n"
            "2. Establish sampling locations and frequencies.\n"
            "3. Implement continuous or grab sampling as required.\n"
            "4. Calibrate and maintain analytical instruments.\n"
            "5. Record, review, and archive monitoring data.\n"
            "6. Investigate and respond to out-of-range values.\n"
            "7. Report results to regulatory agencies as required."
        ),
        key_factors=[
            "List of required parameters",
            "Sampling frequency",
            "Instrument calibration",
            "Data management",
            "Regulatory reporting"
        ],
        primary_authority=[
            "40 CFR 141",
            "Standard Methods for the Examination of Water and Wastewater",
            "AWWA M32"
        ],
        burden_holder="Water quality laboratory manager",
        adversary_position="Less frequent monitoring is sufficient if historical data is stable.",
        counter_arguments=[
            "Regulations specify minimum frequencies.",
            "Process upsets may go undetected with infrequent monitoring.",
            "Continuous data supports process optimization."
        ],
        resolution_strategy="Automate data collection and integrate with process control systems.",
        entity_scope="All regulated water systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="40 CFR 141: National Primary Drinking Water Regulations"
    ),
    DoctrineBlock(
        topic="stiff_diagram_water_typing",
        keywords=["Stiff diagram", "water typing", "hydrochemistry", "major ions", "graphical analysis"],
        conclusion_template="Stiff diagrams must be used to visualize and compare major ion compositions for water typing and source identification.",
        reasoning_framework=(
            "1. Analyze water samples for major cations (Ca, Mg, Na, K) and anions (Cl, SO4, HCO3).\n"
            "2. Convert concentrations to milliequivalents per liter (meq/L).\n"
            "3. Plot values on a Stiff diagram for each sample.\n"
            "4. Compare diagram shapes to identify water types and mixing trends.\n"
            "5. Use results for source identification, process optimization, and regulatory reporting.\n"
            "6. Archive diagrams for historical reference."
        ),
        key_factors=[
            "Major ion analysis",
            "Data conversion to meq/L",
            "Graphical plotting",
            "Interpretation of diagram shapes",
            "Historical comparison"
        ],
        primary_authority=[
            "Standard Methods 1030E",
            "USGS Techniques of Water-Resources Investigations",
            "AWWA M36"
        ],
        burden_holder="Hydrochemist",
        adversary_position="Tabular data is sufficient for water typing.",
        counter_arguments=[
            "Graphical analysis reveals trends not evident in tables.",
            "Stiff diagrams facilitate rapid comparison.",
            "Regulators may require graphical summaries."
        ],
        resolution_strategy="Standardize Stiff diagram preparation and integrate into routine reporting.",
        entity_scope="Groundwater and surface water studies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="USGS TWRI Book 5, Chapter A1"
    ),
    DoctrineBlock(
        topic="boiler_feedwater_quality_specs",
        keywords=["boiler feedwater", "quality", "specifications", "corrosion", "scaling", "treatment"],
        conclusion_template="Boiler feedwater must meet quality specifications for parameters such as hardness, silica, and dissolved oxygen to prevent corrosion and scaling.",
        reasoning_framework=(
            "1. Identify boiler type and operating pressure.\n"
            "2. Review recommended feedwater quality specifications (e.g., ASME, manufacturer).\n"
            "3. Monitor key parameters: hardness, silica, alkalinity, dissolved oxygen, iron, copper.\n"
            "4. Implement treatment (e.g., softening, deaeration, chemical addition) to meet specs.\n"
            "5. Continuously monitor and adjust treatment as needed.\n"
            "6. Document compliance and investigate deviations."
        ),
        key_factors=[
            "Boiler pressure and type",
            "Feedwater hardness and silica",
            "Dissolved oxygen",
            "Corrosion and scaling indices",
            "Treatment system performance"
        ],
        primary_authority=[
            "ASME Consensus on Operating Practices for the Control of Feedwater and Boiler Water Chemistry",
            "AWWA B200",
            "EPA Industrial Water Treatment Guidance"
        ],
        burden_holder="Boiler operator",
        adversary_position="Feedwater quality is less critical for low-pressure boilers.",
        counter_arguments=[
            "Corrosion and scaling occur at all pressures.",
            "Manufacturer warranties may be voided by poor water quality.",
            "Regulatory inspections may cite non-compliance."
        ],
        resolution_strategy="Implement routine monitoring and adjust treatment to maintain compliance.",
        entity_scope="Industrial and power plant boilers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Consensus on Operating Practices"
    ),
    # Additional doctrines to reach 40+ entries:
    DoctrineBlock(
        topic="chlorine_dioxide_disinfection",
        keywords=["chlorine dioxide", "disinfection", "byproducts", "CT", "chlorite", "chlorate"],
        conclusion_template="Chlorine dioxide must be dosed and monitored to achieve disinfection goals while maintaining chlorite and chlorate below regulatory limits.",
        reasoning_framework=(
            "1. Determine required CT for target pathogen inactivation.\n"
            "2. Dose chlorine dioxide using controlled generation and dosing systems.\n"
            "3. Monitor residual chlorine dioxide, chlorite, and chlorate in finished water.\n"
            "4. Adjust dosing to balance disinfection efficacy and byproduct minimization.\n"
            "5. Maintain generator and dosing equipment.\n"
            "6. Document compliance with byproduct limits and CT requirements."
        ),
        key_factors=[
            "Target CT value",
            "Chlorite and chlorate limits",
            "Generator reliability",
            "Residual monitoring",
            "Byproduct minimization"
        ],
        primary_authority=[
            "40 CFR 141.131",
            "EPA Disinfectants and Disinfection Byproducts Rule",
            "AWWA C655"
        ],
        burden_holder="Disinfection system operator",
        adversary_position="Chlorine dioxide is less effective than chlorine.",
        counter_arguments=[
            "Chlorine dioxide is effective against certain pathogens.",
            "Byproduct control is achievable with proper dosing.",
            "Regulatory limits are enforceable."
        ],
        resolution_strategy="Automate dosing and integrate residual/byproduct monitoring.",
        entity_scope="Municipal water treatment plants",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA Disinfectants and Disinfection Byproducts Rule"
    ),
    DoctrineBlock(
        topic="total_organic_carbon_removal",
        keywords=["TOC", "total organic carbon", "removal", "precursor", "DBP", "enhanced coagulation"],
        conclusion_template="Total organic carbon (TOC) must be reduced to minimize disinfection byproduct (DBP) formation, using enhanced coagulation or alternative processes.",
        reasoning_framework=(
            "1. Measure influent TOC and determine DBP precursor levels.\n"
            "2. Implement enhanced coagulation or alternative TOC removal processes.\n"
            "3. Monitor TOC removal efficiency and adjust process as needed.\n"
            "4. Document compliance with DBP precursor removal requirements.\n"
            "5. Report results to regulatory agencies."
        ),
        key_factors=[
            "Influent TOC concentration",
            "DBP precursor removal requirements",
            "Coagulation process optimization",
            "Alternative removal technologies",
            "Monitoring and reporting"
        ],
        primary_authority=[
            "40 CFR 141.135",
            "EPA Stage 1 and 2 DBP Rules",
            "AWWA M37"
        ],
        burden_holder="Water treatment process engineer",
        adversary_position="TOC removal is unnecessary if DBPs are below limits.",
        counter_arguments=[
            "TOC is a regulated DBP precursor.",
            "Enhanced coagulation is required by rule.",
            "DBP formation can increase with seasonal changes."
        ],
        resolution_strategy="Optimize coagulation and monitor TOC removal continuously.",
        entity_scope="Surface water treatment plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Stage 1 and 2 Disinfectants and Disinfection Byproducts Rules"
    ),
    DoctrineBlock(
        topic="lead_and_copper_rule_compliance",
        keywords=["lead", "copper", "LCR", "compliance", "corrosion control", "sampling"],
        conclusion_template="Water systems must implement corrosion control and sampling protocols to comply with the Lead and Copper Rule (LCR).",
        reasoning_framework=(
            "1. Identify action levels for lead (0.015 mg/L) and copper (1.3 mg/L).\n"
            "2. Implement corrosion control treatment (e.g., pH adjustment, orthophosphate addition).\n"
            "3. Conduct first-draw tap sampling at required locations and frequencies.\n"
            "4. Notify customers and regulatory agencies of exceedances.\n"
            "5. Maintain records of sampling and corrective actions."
        ),
        key_factors=[
            "Lead and copper action levels",
            "Corrosion control effectiveness",
            "Sampling protocol",
            "Public notification",
            "Recordkeeping"
        ],
        primary_authority=[
            "40 CFR 141.80",
            "EPA Lead and Copper Rule",
            "AWWA M58"
        ],
        burden_holder="Public water system operator",
        adversary_position="Lead and copper are not a concern in new systems.",
        counter_arguments=[
            "Lead and copper can leach from premise plumbing.",
            "Regulations apply to all systems.",
            "Public health risks are significant."
        ],
        resolution_strategy="Maintain corrosion control and conduct required sampling.",
        entity_scope="Community and non-community water systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Lead and Copper Rule"
    ),
    DoctrineBlock(
        topic="arsenic_removal_technologies",
        keywords=["arsenic", "removal", "adsorption", "coagulation", "membrane", "compliance"],
        conclusion_template="Arsenic removal must achieve concentrations below the MCL (0.010 mg/L) using appropriate technologies such as adsorption, coagulation, or membrane processes.",
        reasoning_framework=(
            "1. Measure influent arsenic concentration and speciation.\n"
            "2. Select removal technology based on water quality and operational considerations.\n"
            "3. Optimize process for maximum removal efficiency.\n"
            "4. Monitor effluent arsenic and adjust treatment as needed.\n"
            "5. Document compliance and report to regulatory agencies."
        ),
        key_factors=[
            "Influent arsenic concentration",
            "Technology selection",
            "Process optimization",
            "Effluent monitoring",
            "Regulatory reporting"
        ],
        primary_authority=[
            "40 CFR 141.62",
            "EPA Arsenic Rule",
            "AWWA M37"
        ],
        burden_holder="Water treatment plant operator",
        adversary_position="Arsenic removal is only needed for high concentrations.",
        counter_arguments=[
            "MCL applies to all systems.",
            "Arsenic speciation affects removal efficiency.",
            "Public health risks require proactive removal."
        ],
        resolution_strategy="Select and optimize technology based on site-specific conditions.",
        entity_scope="Community water systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Arsenic Rule"
    ),
    DoctrineBlock(
        topic="perchlorate_removal",
        keywords=["perchlorate", "removal", "ion exchange", "biological treatment", "MCL", "compliance"],
        conclusion_template="Perchlorate must be removed to meet state or federal MCLs using ion exchange, biological, or other proven technologies.",
        reasoning_framework=(
            "1. Measure perchlorate in source water.\n"
            "2. Select removal technology (e.g., selective ion exchange, biological reduction).\n"
            "3. Optimize process for site-specific conditions.\n"
            "4. Monitor effluent perchlorate and adjust treatment as needed.\n"
            "5. Document compliance and report results."
        ),
        key_factors=[
            "Influent perchlorate concentration",
            "Technology selection",
            "Process optimization",
            "Effluent monitoring",
            "Regulatory limits"
        ],
        primary_authority=[
            "EPA Perchlorate Drinking Water Recommendations",
            "AWWA M62",
            "State MCLs"
        ],
        burden_holder="Water system operator",
        adversary_position="Perchlorate is not regulated federally.",
        counter_arguments=[
            "Several states have enforceable MCLs.",
            "EPA provides health advisory levels.",
            "Public concern drives removal even without federal MCL."
        ],
        resolution_strategy="Monitor regulatory developments and implement removal as required.",
        entity_scope="Community water systems in affected regions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="State MCLs and EPA Guidance"
    ),
    DoctrineBlock(
        topic="iron_and_manganese_removal",
        keywords=["iron", "manganese", "removal", "oxidation", "filtration", "aesthetic", "MCL"],
        conclusion_template="Iron and manganese must be removed to below secondary MCLs to prevent aesthetic issues and distribution system problems.",
        reasoning_framework=(
            "1. Measure influent iron and manganese concentrations.\n"
            "2. Select removal method (oxidation/filtration, greensand, ion exchange).\n"
            "3. Optimize process for removal efficiency.\n"
            "4. Monitor effluent concentrations and adjust treatment as needed.\n"
            "5. Maintain filters and document performance."
        ),
        key_factors=[
            "Influent iron and manganese",
            "Removal technology selection",
            "Process optimization",
            "Filter maintenance",
            "Secondary MCLs"
        ],
        primary_authority=[
            "40 CFR 143.3",
            "EPA Secondary Drinking Water Regulations",
            "AWWA M37"
        ],
        burden_holder="Water treatment operator",
        adversary_position="Aesthetic standards are not enforceable.",
        counter_arguments=[
            "Iron and manganese cause taste, staining, and complaints.",
            "Distribution system impacts can be severe.",
            "Some states enforce secondary MCLs."
        ],
        resolution_strategy="Maintain removal processes and monitor performance.",
        entity_scope="Community and non-community water systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA Secondary Drinking Water Regulations"
    ),
    DoctrineBlock(
        topic="nitrate_removal",
        keywords=["nitrate", "removal", "ion exchange", "biological denitrification", "MCL", "compliance"],
        conclusion_template="Nitrate must be removed to below the MCL (10 mg/L as N) using ion exchange, biological, or membrane processes.",
        reasoning_framework=(
            "1. Measure influent nitrate concentration.\n"
            "2. Select removal technology (e.g., ion exchange, biological denitrification, reverse osmosis).\n"
            "3. Optimize process for removal efficiency.\n"
            "4. Monitor effluent nitrate and adjust treatment as needed.\n"
            "5. Document compliance and report to regulatory agencies."
        ),
        key_factors=[
            "Influent nitrate concentration",
            "Technology selection",
            "Process optimization",
            "Effluent monitoring",
            "MCL compliance"
        ],
        primary_authority=[
            "40 CFR 141.62",
            "EPA Nitrate Rule",
            "AWWA M37"
        ],
        burden_holder="Water treatment plant operator",
        adversary_position="Nitrate is only a concern for infants.",
        counter_arguments=[
            "MCL applies to all water systems.",
            "Nitrate is acutely toxic to infants and pregnant women.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Select and optimize removal technology as needed.",
        entity_scope="Community and non-community water systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Nitrate Rule"
    ),
    DoctrineBlock(
        topic="fluoridation_control",
        keywords=["fluoridation", "control", "fluoride", "optimal concentration", "public health"],
        conclusion_template="Fluoride addition must be controlled to maintain concentrations within the optimal range (0.7 mg/L) for dental health, without exceeding the MCL.",
        reasoning_framework=(
            "1. Measure natural fluoride in source water.\n"
            "2. Dose fluoride to achieve optimal concentration (0.7 mg/L).\n"
            "3. Monitor finished water fluoride daily.\n"
            "4. Adjust dosing for changes in flow or source water.\n"
            "5. Maintain dosing equipment and document performance.\n"
            "6. Report results to regulatory agencies."
        ),
        key_factors=[
            "Source water fluoride",
            "Dosing accuracy",
            "Monitoring frequency",
            "MCL compliance",
            "Equipment maintenance"
        ],
        primary_authority=[
            "40 CFR 141.62",
            "CDC Community Water Fluoridation Guidelines",
            "AWWA B701"
        ],
        burden_holder="Water system operator",
        adversary_position="Fluoridation is controversial and unnecessary.",
        counter_arguments=[
            "CDC and EPA endorse optimal fluoridation.",
            "MCL prevents overexposure.",
            "Public health benefits are well documented."
        ],
        resolution_strategy="Automate dosing and monitor fluoride daily.",
        entity_scope="Community water systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="CDC Community Water Fluoridation Guidelines"
    ),
    DoctrineBlock(
        topic="microbial_source_tracking",
        keywords=["microbial source tracking", "MST", "fecal contamination", "pathogen", "source identification"],
        conclusion_template="Microbial source tracking must be used to identify sources of fecal contamination for targeted remediation.",
        reasoning_framework=(
            "1. Collect water samples from impacted areas.\n"
            "2. Apply MST methods (e.g., host-specific markers, genetic analysis).\n"
            "3. Analyze results to differentiate human, livestock, or wildlife sources.\n"
            "4. Use findings to inform remediation and management actions.\n"
            "5. Document and report results to stakeholders."
        ),
        key_factors=[
            "Sampling strategy",
            "MST method selection",
            "Data interpretation",
            "Remediation planning",
            "Stakeholder communication"
        ],
        primary_authority=[
            "EPA Microbial Source Tracking Guide",
            "USGS MST Methods",
            "AWWA Research Foundation"
        ],
        burden_holder="Water quality manager",
        adversary_position="MST is too costly and unnecessary.",
        counter_arguments=[
            "MST enables targeted remediation.",
            "Cost is justified by improved outcomes.",
            "Regulators may require source identification."
        ],
        resolution_strategy="Apply MST as part of watershed management.",
        entity_scope="Watershed and source water protection",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Microbial Source Tracking Guide"
    ),
    DoctrineBlock(
        topic="emerging_contaminants_monitoring",
        keywords=["emerging contaminants", "PFAS", "pharmaceuticals", "monitoring", "unregulated", "health advisory"],
        conclusion_template="Emerging contaminants must be monitored and reported as required by health advisories or state regulations.",
        reasoning_framework=(
            "1. Identify emerging contaminants of concern (e.g., PFAS, pharmaceuticals).\n"
            "2. Implement monitoring using appropriate analytical methods.\n"
            "3. Compare results to health advisory levels or state limits.\n"
            "4. Notify public and regulators of exceedances.\n"
            "5. Evaluate treatment options if required."
        ),
        key_factors=[
            "Contaminant list",
            "Analytical methods",
            "Health advisory levels",
            "Public notification",
            "Treatment evaluation"
        ],
        primary_authority=[
            "EPA Health Advisories",
            "State regulations",
            "AWWA M71"
        ],
        burden_holder="Water system manager",
        adversary_position="Emerging contaminants are not regulated federally.",
        counter_arguments=[
            "State and local regulations may apply.",
            "Public concern drives monitoring.",
            "Health advisories are enforceable in some jurisdictions."
        ],
        resolution_strategy="Monitor regulatory developments and implement monitoring as required.",
        entity_scope="Community water systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA Health Advisories"
    ),
    DoctrineBlock(
        topic="distribution_system_residual_maintenance",
        keywords=["distribution system", "chlorine residual", "maintenance", "biofilm", "regrowth"],
        conclusion_template="A disinfectant residual must be maintained throughout the distribution system to prevent microbial regrowth and ensure compliance.",
        reasoning_framework=(
            "1. Monitor chlorine residual at representative locations.\n"
            "2. Adjust booster chlorination as needed to maintain minimum residual.\n"
            "3. Investigate and address low residuals or regrowth events.\n"
            "4. Document monitoring and corrective actions.\n"
            "5. Report compliance to regulatory agencies."
        ),
        key_factors=[
            "Residual monitoring",
            "Booster chlorination",
            "Biofilm control",
            "Compliance documentation",
            "Distribution system hydraulics"
        ],
        primary_authority=[
            "40 CFR 141.72",
            "EPA Distribution System Optimization",
            "AWWA M68"
        ],
        burden_holder="Distribution system operator",
        adversary_position="Residual is unnecessary if source water is disinfected.",
        counter_arguments=[
            "Biofilm can regrow in distribution systems.",
            "Residual is required by regulation.",
            "Customer complaints increase without residual."
        ],
        resolution_strategy="Maintain booster stations and monitor residuals continuously.",
        entity_scope="All public water distribution systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Distribution System Optimization"
    ),
    DoctrineBlock(
        topic="taste_and_odor_control",
        keywords=["taste", "odor", "control", "geosmin", "MIB", "activated carbon"],
        conclusion_template="Taste and odor issues must be controlled using appropriate treatment such as activated carbon or advanced oxidation.",
        reasoning_framework=(
            "1. Identify taste and odor compounds (e.g., geosmin, MIB).\n"
            "2. Select control technology (powdered or granular activated carbon, ozone, advanced oxidation).\n"
            "3. Monitor effectiveness and adjust treatment as needed.\n"
            "4. Investigate and address source water causes.\n"
            "5. Communicate with customers regarding taste and odor events."
        ),
        key_factors=[
            "Compound identification",
            "Technology selection",
            "Treatment optimization",
            "Source water management",
            "Customer communication"
        ],
        primary_authority=[
            "AWWA M62",
            "EPA Taste and Odor Guidance",
            "Standard Methods 2150"
        ],
        burden_holder="Water treatment plant manager",
        adversary_position="Taste and odor are aesthetic and not regulated.",
        counter_arguments=[
            "Customer complaints can lead to regulatory action.",
            "Some states enforce secondary standards.",
            "Proactive control improves public confidence."
        ],
        resolution_strategy="Integrate taste and odor control into routine operations.",
        entity_scope="Surface water and groundwater systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AWWA M62: Taste and Odor Control"
    ),
    DoctrineBlock(
        topic="sludge_management_and_disposal",
        keywords=["sludge", "management", "disposal", "dewatering", "landfill", "biosolids"],
        conclusion_template="Sludge generated from water treatment must be managed and disposed of in accordance with federal, state, and local regulations.",
        reasoning_framework=(
            "1. Characterize sludge for volume, solids content, and contaminants.\n"
            "2. Select dewatering and stabilization methods (e.g., centrifuge, belt press, lime stabilization).\n"
            "3. Identify disposal options (landfill, land application, incineration).\n"
            "4. Comply with all regulatory requirements for handling and disposal.\n"
            "5. Maintain records of sludge management and disposal."
        ),
        key_factors=[
            "Sludge characteristics",
            "Dewatering technology",
            "Disposal options",
            "Regulatory compliance",
            "Recordkeeping"
        ],
        primary_authority=[
            "40 CFR 257",
            "EPA Biosolids Rule",
            "AWWA M37"
        ],
        burden_holder="Water treatment plant manager",
        adversary_position="Sludge can be disposed of as regular waste.",
        counter_arguments=[
            "Sludge may contain regulated contaminants.",
            "Improper disposal can result in penalties.",
            "Land application requires special permits."
        ],
        resolution_strategy="Develop and follow a sludge management plan.",
        entity_scope="Water and wastewater treatment plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Biosolids Rule"
    ),
    DoctrineBlock(
        topic="chemical_storage_and_handling",
        keywords=["chemical storage", "handling", "safety", "spill prevention", "secondary containment"],
        conclusion_template="All treatment chemicals must be stored and handled safely, with secondary containment and spill prevention measures in place.",
        reasoning_framework=(
            "1. Store chemicals in designated, labeled areas with secondary containment.\n"
            "2. Train staff in safe handling and emergency response.\n"
            "3. Inspect storage areas regularly for leaks or deterioration.\n"
            "4. Maintain spill kits and emergency procedures.\n"
            "5. Comply with OSHA and EPA requirements."
        ),
        key_factors=[
            "Chemical compatibility",
            "Secondary containment",
            "Staff training",
            "Inspection frequency",
            "Emergency response"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.1200",
            "EPA SPCC Rule",
            "AWWA B601"
        ],
        burden_holder="Facility manager",
        adversary_position="Small quantities do not require special handling.",
        counter_arguments=[
            "All chemicals pose risks.",
            "Regulations apply regardless of quantity.",
            "Spills can cause environmental harm."
        ],
        resolution_strategy="Implement chemical management SOPs and regular training.",
        entity_scope="All water treatment facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA Hazard Communication Standard"
    ),
    DoctrineBlock(
        topic="operator_certification_and_training",
        keywords=["operator", "certification", "training", "continuing education", "competency"],
        conclusion_template="All operators must be certified and receive ongoing training to maintain competency and regulatory compliance.",
        reasoning_framework=(
            "1. Verify operator certification meets state requirements.\n"
            "2. Provide initial and continuing education on treatment processes, safety, and regulations.\n"
            "3. Document training and certification status.\n"
            "4. Address knowledge gaps through targeted training.\n"
            "5. Prepare for regulatory inspections and audits."
        ),
        key_factors=[
            "Certification level",
            "Training frequency",
            "Documentation",
            "Knowledge assessment",
            "Regulatory compliance"
        ],
        primary_authority=[
            "State operator certification programs",
            "EPA Guidelines for the Certification and Recertification of the Operators of Community and Nontransient Noncommunity Public Water Systems",
            "AWWA G100"
        ],
        burden_holder="Utility manager",
        adversary_position="On-the-job training is sufficient.",
        counter_arguments=[
            "Certification is required by law.",
            "Continuing education ensures up-to-date knowledge.",
            "Competency reduces operational risks."
        ],
        resolution_strategy="Maintain a training program and track certification status.",
        entity_scope="All public water systems",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="EPA Operator Certification Guidelines"
    ),
    DoctrineBlock(
        topic="cross_connection_control_and_backflow_prevention",
        keywords=["cross connection", "backflow prevention", "potable water", "contamination", "testing"],
        conclusion_template="Cross connections must be controlled and backflow prevention devices tested regularly to protect potable water supplies.",
        reasoning_framework=(
            "1. Identify potential cross connections in the distribution system.\n"
            "2. Install appropriate backflow prevention devices (e.g., RPZ, double check valves).\n"
            "3. Test devices at required intervals and maintain records.\n"
            "4. Respond to test failures with immediate corrective action.\n"
            "5. Educate customers and staff on cross connection risks."
        ),
        key_factors=[
            "System survey",
            "Device selection",
            "Testing frequency",
            "Recordkeeping",
            "Customer education"
        ],
        primary_authority=[
            "EPA Cross-Connection Control Manual",
            "State plumbing codes",
            "AWWA M14"
        ],
        burden_holder="Distribution system manager",
        adversary_position="Backflow is unlikely with positive pressure.",
        counter_arguments=[
            "Pressure fluctuations can cause backflow.",
            "Regulations require device testing.",
            "Contamination events have occurred historically."
        ],
        resolution_strategy="Implement a cross connection control program with regular testing.",
        entity_scope="All public water distribution systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Cross-Connection Control Manual"
    ),
    DoctrineBlock(
        topic="emergency_response_and_contingency_planning",
        keywords=["emergency response", "contingency planning", "water system", "security", "natural disaster"],
        conclusion_template="Water systems must maintain and regularly update emergency response and contingency plans for all hazards.",
        reasoning_framework=(
            "1. Identify potential hazards (natural, technological, security).\n"
            "2. Develop and maintain an emergency response plan (ERP).\n"
            "3. Train staff and conduct regular drills.\n"
            "4. Update ERP based on lessons learned and regulatory changes.\n"
            "5. Coordinate with local emergency management agencies."
        ),
        key_factors=[
            "Hazard identification",
            "ERP documentation",
            "Training and drills",
            "Plan updates",
            "Agency coordination"
        ],
        primary_authority=[
            "Bioterrorism Act of 2002",
            "EPA Emergency Response Planning Guidance",
            "AWWA G440"
        ],
        burden_holder="Utility manager",
        adversary_position="Emergencies are rare and do not justify planning.",
        counter_arguments=[
            "Preparedness reduces risk and liability.",
            "Regulations require ERPs.",
            "Rapid response minimizes service disruptions."
        ],
        resolution_strategy="Maintain and exercise ERP regularly.",
        entity_scope="All public water systems",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="EPA Emergency Response Planning Guidance"
    ),
    DoctrineBlock(
        topic="asset_management_and_capital_planning",
        keywords=["asset management", "capital planning", "infrastructure", "maintenance", "replacement"],
        conclusion_template="Asset management and capital planning must be implemented to ensure sustainable water system operation and regulatory compliance.",
        reasoning_framework=(
            "1. Inventory all system assets and assess condition.\n"
            "2. Prioritize maintenance and replacement based on risk and criticality.\n"
            "3. Develop a capital improvement plan (CIP).\n"
            "4. Secure funding and track progress.\n"
            "5. Update asset inventory and CIP regularly."
        ),
        key_factors=[
            "Asset inventory",
            "Condition assessment",
            "Risk prioritization",
            "Capital planning",
            "Funding"
        ],
        primary_authority=[
            "EPA Asset Management Guidance",
            "AWWA G400",
            "State DWSRF requirements"
        ],
        burden_holder="Utility manager",
        adversary_position="Reactive maintenance is sufficient.",
        counter_arguments=[
            "Proactive management reduces costs and failures.",
            "Funding agencies require asset management plans.",
            "Regulatory compliance is linked to asset condition."
        ],
        resolution_strategy="Implement asset management software and update plans annually.",
        entity_scope="All public water systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Asset Management Guidance"
    ),
    DoctrineBlock(
        topic="source_water_protection",
        keywords=["source water", "protection", "watershed", "contamination prevention", "land use"],
        conclusion_template="Source water protection programs must be implemented to prevent contamination and reduce treatment costs.",
        reasoning_framework=(
            "1. Delineate source water protection area.\n"
            "2. Identify potential contaminant sources and risks.\n"
            "3. Implement best management practices (BMPs) and land use controls.\n"
            "4. Monitor water quality and update protection strategies.\n"
            "5. Engage stakeholders and public in protection efforts."
        ),
        key_factors=[
            "Protection area delineation",
            "Contaminant source inventory",
            "BMP implementation",
            "Monitoring",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Safe Drinking Water Act, Section 1453",
            "EPA Source Water Protection Guidance",
            "AWWA G300"
        ],
        burden_holder="Source water manager",
        adversary_position="Treatment can address any contamination.",
        counter_arguments=[
            "Prevention is more cost-effective than treatment.",
            "Some contaminants are difficult to remove.",
            "Regulations require source water assessments."
        ],
        resolution_strategy="Develop and implement a source water protection plan.",
        entity_scope="All public water systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Source Water Protection Guidance"
    ),
    DoctrineBlock(
        topic="public_notification_and_communication",
        keywords=["public notification", "communication", "MCL violation", "boil water", "customer advisory"],
        conclusion_template="Water systems must provide timely public notification and communication for MCL violations and other significant events.",
        reasoning_framework=(
            "1. Identify events requiring public notification (e.g., MCL violations, boil water advisories).\n"
            "2. Prepare notification materials in accordance with regulatory requirements.\n"
            "3. Deliver notifications through approved channels (mail, media, website).\n"
            "4. Maintain records of notification and customer communication.\n"
            "5. Follow up with corrective action and updates."
        ),
        key_factors=[
            "Notification triggers",
            "Content and format",
            "Delivery methods",
            "Recordkeeping",
            "Follow-up communication"
        ],
        primary_authority=[
            "40 CFR 141.201",
            "EPA Public Notification Rule",
            "AWWA G200"
        ],
        burden_holder="Water system manager",
        adversary_position="Notification can be delayed until after resolution.",
        counter_arguments=[
            "Timely notification is required by law.",
            "Delays can endanger public health.",
            "Regulators may impose penalties for late notification."
        ],
        resolution_strategy="Develop notification templates and maintain readiness.",
        entity_scope="All public water systems",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="EPA Public Notification Rule"
    ),
    DoctrineBlock(
        topic="water_loss_control_and_audit",
        keywords=["water loss", "control", "audit", "non-revenue water", "leak detection"],
        conclusion_template="Water loss control and annual audits must be conducted to minimize non-revenue water and improve system efficiency.",
        reasoning_framework=(
            "1. Conduct annual water audits using AWWA or state methodology.\n"
            "2. Identify and quantify real and apparent losses.\n"
            "3. Implement leak detection and repair programs.\n"
            "4. Monitor and report water loss metrics.\n"
            "5. Update loss control strategies based on audit results."
        ),
        key_factors=[
            "Audit methodology",
            "Loss quantification",
            "Leak detection",
            "Repair programs",
            "Reporting"
        ],
        primary_authority=[
            "AWWA M36",
            "EPA Water Loss Control Guidance",
            "State DWSRF requirements"
        ],
        burden_holder="Utility manager",
        adversary_position="Water loss is inevitable and not worth addressing.",
        counter_arguments=[
            "Water loss increases costs and reduces revenue.",
            "Funding agencies require loss control programs.",
            "Leak detection improves system reliability."
        ],
        resolution_strategy="Implement annual audits and proactive loss control.",
        entity_scope="All public water systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AWWA M36: Water Audits and Loss Control Programs"
    ),
    DoctrineBlock(
        topic="disinfection_byproducts_control",
        keywords=["disinfection byproducts", "DBP", "THM", "HAA5", "control", "compliance"],
        conclusion_template="Disinfection byproducts must be controlled to below MCLs using precursor removal, process optimization, and monitoring.",
        reasoning_framework=(
            "1. Monitor DBP precursors (TOC, bromide) and finished water DBPs (THMs, HAA5).\n"
            "2. Optimize precursor removal (e.g., enhanced coagulation).\n"
            "3. Adjust disinfection practices (e.g., alternative disinfectants, contact time).\n"
            "4. Monitor DBP levels at required locations and frequencies.\n"
            "5. Report results and take corrective action if MCLs are exceeded."
        ),
        key_factors=[
            "Precursor monitoring",
            "DBP formation potential",
            "Process optimization",
            "Monitoring frequency",
            "MCL compliance"
        ],
        primary_authority=[
            "40 CFR 141.64",
            "EPA Stage 1 and 2 DBP Rules",
            "AWWA M37"
        ],
        burden_holder="Water treatment process engineer",
        adversary_position="DBPs are only a concern for large systems.",
        counter_arguments=[
            "DBP rules apply to all community systems.",
            "DBPs pose long-term health risks.",
            "Process optimization can reduce DBPs."
        ],
        resolution_strategy="Integrate DBP control into routine process monitoring.",
        entity_scope="All community water systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA Stage 1 and 2 DBP Rules"
    ),
    DoctrineBlock(
        topic="groundwater_rule_compliance",
        keywords=["groundwater rule", "compliance", "sanitary survey", "corrective action", "fecal indicators"],
        conclusion_template="Groundwater systems must comply with the Groundwater Rule by conducting sanitary surveys, monitoring for fecal indicators, and implementing corrective actions.",
        reasoning_framework=(
            "1. Conduct periodic sanitary surveys as required.\n"
            "2. Monitor source water for fecal indicators (e.g., E. coli).\n"
            "3. Implement corrective action if contamination is detected.\n"
            "4. Maintain records and report compliance to regulators.\n"
            "5. Review and update source protection measures."
        ),
        key_factors=[
            "Sanitary survey frequency",
            "Fecal indicator monitoring",
            "Corrective action procedures",
            "Recordkeeping",
            "Source protection"
        ],
        primary_authority=[
            "40 CFR 141.400",
            "EPA Groundwater Rule",
            "AWWA G200"
        ],
        burden_holder="Groundwater system operator",
        adversary_position="Groundwater is inherently safe and does not require monitoring.",
        counter_arguments=[
            "Contamination events have occurred in groundwater systems.",
            "Regulations require monitoring and corrective action.",
            "Sanitary surveys identify vulnerabilities."
        ],
        resolution_strategy="Integrate compliance into routine operations and training.",
        entity_scope="All groundwater systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Groundwater Rule"
    ),
    DoctrineBlock(
        topic="water_main_flushing_program",
        keywords=["water main", "flushing", "distribution system", "sediment removal", "water quality"],
        conclusion_template="A routine water main flushing program must be implemented to maintain distribution system water quality and remove sediment.",
        reasoning_framework=(
            "1. Develop a flushing schedule covering all system areas.\n"
            "2. Use unidirectional flushing where possible for maximum velocity.\n"
            "3. Monitor water quality parameters (e.g., turbidity, chlorine) during flushing.\n"
            "4. Document flushing activities and outcomes.\n"
            "5. Adjust program based on system changes and water quality trends."
        ),
        key_factors=[
            "Flushing schedule",
            "Velocity and flow direction",
            "Water quality monitoring",
            "Documentation",
            "Program adjustment"
        ],
        primary_authority=[
            "AWWA M17",
            "EPA Distribution System Optimization",
            "State DWSRF requirements"
        ],
        burden_holder="Distribution system manager",
        adversary_position="Flushing is only needed after main breaks.",
        counter_arguments=[
            "Routine flushing prevents water quality deterioration.",
            "Sediment can harbor pathogens and reduce disinfectant residual.",
            "Regulators may require flushing programs."
        ],
        resolution_strategy="Implement and document a routine flushing program.",
        entity_scope="All public water distribution systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AWWA M17: Distribution System Flushing"
    ),
    DoctrineBlock(
        topic="hydraulic_modeling_and_system_analysis",
        keywords=["hydraulic modeling", "system analysis", "distribution system", "pressure", "flow"],
        conclusion_template="Hydraulic modeling and system analysis must be performed to ensure adequate pressure, flow, and fire protection throughout the distribution system.",
        reasoning_framework=(
            "1. Develop and calibrate a hydraulic model of the distribution system.\n"
            "2. Analyze system performance under normal and emergency conditions.\n"
            "3. Identify areas of low pressure or inadequate flow.\n"
            "4. Use results to inform system improvements and capital planning.\n"
            "5. Update model as system changes occur."
        ),
        key_factors=[
            "Model calibration",
            "Pressure and flow data",
            "Scenario analysis",
            "System improvements",
            "Model updates"
        ],
        primary_authority=[
            "AWWA M32",
            "EPA Distribution System Optimization",
            "ISO Fire Flow Requirements"
        ],
        burden_holder="System engineer",
        adversary_position="Modeling is unnecessary for small systems.",
        counter_arguments=[
            "Modeling identifies hidden deficiencies.",
            "Fire protection standards require analysis.",
            "System changes require updated analysis."
        ],
        resolution_strategy="Maintain and update hydraulic models regularly.",
        entity_scope="All public water distribution systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AWWA M32: Computer Modeling of Water Distribution Systems"
    ),
    DoctrineBlock(
        topic="chloramination_process_control",
        keywords=["chloramination", "ammonia addition", "process control", "nitrification", "DBP reduction"],
        conclusion_template="Chloramination must be controlled to maintain target chlorine to ammonia ratios, prevent nitrification, and reduce DBP formation.",
        reasoning_framework=(
            "1. Dose chlorine and ammonia to achieve target ratio (typically 4:1 to 5:1).\n"
            "2. Monitor residuals and adjust dosing for process stability.\n"
            "3. Monitor for nitrification indicators (nitrite, loss of residual).\n"
            "4. Respond to nitrification events with corrective action.\n"
            "5. Document process control and compliance."
        ),
        key_factors=[
            "Chlorine to ammonia ratio",
            "Residual monitoring",
            "Nitrification indicators",
            "Process adjustment",
            "Documentation"
        ],
        primary_authority=[
            "EPA Alternative Disinfectants Guidance",
            "AWWA M56",
            "40 CFR 141.132"
        ],
        burden_holder="Disinfection process operator",
        adversary_position="Chloramination is less effective than free chlorine.",
        counter_arguments=[
            "Chloramination reduces DBPs.",
            "Proper control prevents nitrification.",
            "Regulations allow chloramination."
        ],
        resolution_strategy="Automate dosing and monitor for nitrification.",
        entity_scope="Community water systems using chloramination",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Alternative Disinfectants Guidance"
    ),
    DoctrineBlock(
        topic="pharmaceuticals_and_personal_care_products_removal",
        keywords=["pharmaceuticals", "PPCPs", "removal", "advanced oxidation", "activated carbon"],
        conclusion_template="Pharmaceuticals and personal care products (PPCPs) must be monitored and removed as required by health advisories or local regulations.",
        reasoning_framework=(
            "1. Monitor for PPCPs using sensitive analytical methods.\n"
            "2. Evaluate treatment options (e.g., advanced oxidation, activated carbon).\n"
            "3. Optimize processes for PPCP removal.\n"
            "4. Report results to stakeholders and regulators.\n"
            "5. Update treatment as regulations evolve."
        ),
        key_factors=[
            "PPCP monitoring",
            "Treatment technology",
            "Process optimization",
            "Reporting",
            "Regulatory developments"
        ],
        primary_authority=[
            "EPA PPCP Guidance",
            "AWWA Research Foundation",
            "State health advisories"
        ],
        burden_holder="Water quality manager",
        adversary_position="PPCPs are not regulated and do not require removal.",
        counter_arguments=[
            "Public concern and health advisories drive action.",
            "Some states regulate PPCPs.",
            "Advanced treatment can achieve removal."
        ],
        resolution_strategy="Monitor for PPCPs and implement removal as required.",
        entity_scope="Community water systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA PPCP Guidance"
    ),
    DoctrineBlock(
        topic="water_reuse_and_reclamation",
        keywords=["water reuse", "reclamation", "advanced treatment", "indirect potable reuse", "regulations"],
        conclusion_template="Water reuse and reclamation projects must comply with all applicable treatment, monitoring, and regulatory requirements to protect public health.",
        reasoning_framework=(
            "1. Identify end use and applicable regulations (e.g., indirect potable reuse, irrigation).\n"
            "2. Design advanced treatment processes (e.g., MF/UF, RO, UV, AOP) to meet standards.\n"
            "3. Monitor water quality and process performance.\n"
            "4. Report results and engage stakeholders.\n"
            "5. Update processes as regulations and end uses evolve."
        ),
        key_factors=[
            "End use and regulations",
            "Treatment process selection",
            "Monitoring and reporting",
            "Stakeholder engagement",
            "Process updates"
        ],
        primary_authority=[
            "EPA Guidelines for Water Reuse",
            "State water reuse regulations",
            "AWWA M62"
        ],
        burden_holder="Project manager",
        adversary_position="Reuse is not necessary with adequate supply.",
        counter_arguments=[
            "Water scarcity drives reuse.",
            "Regulations ensure public health protection.",
            "Advanced treatment achieves high quality."
        ],
        resolution_strategy="Design and operate reuse systems to meet or exceed standards.",
        entity_scope="Municipal and industrial water reuse projects",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Guidelines for Water Reuse"
    ),
    DoctrineBlock(
        topic="microbial_risk_assessment",
        keywords=["microbial risk", "QMRA", "quantitative microbial risk assessment", "pathogen", "public health"],
        conclusion_template="Quantitative microbial risk assessment (QMRA) must be conducted to evaluate pathogen risks and inform treatment and monitoring strategies.",
        reasoning_framework=(
            "1. Identify target pathogens and exposure scenarios.\n"
            "2. Collect occurrence and concentration data.\n"
            "3. Model exposure and dose-response relationships.\n"
            "4. Estimate risk and compare to health benchmarks.\n"
            "5. Use results to optimize treatment and monitoring."
        ),
        key_factors=[
            "Pathogen identification",
            "Exposure assessment",
            "Dose-response modeling",
            "Risk estimation",
            "Treatment optimization"
        ],
        primary_authority=[
            "EPA QMRA Guidelines",
            "WHO Guidelines for Drinking-water Quality",
            "AWWA Research Foundation"
        ],
        burden_holder="Water quality risk assessor",
        adversary_position="QMRA is too complex for routine use.",
        counter_arguments=[
            "QMRA informs evidence-based decisions.",
            "Regulators may require risk assessment.",
            "QMRA supports public health protection."
        ],
        resolution_strategy="Integrate QMRA into source water and treatment planning.",
        entity_scope="All water systems with pathogen risks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA QMRA Guidelines"
    ),
    DoctrineBlock(
        topic="continuous_improvement_and_quality_management",
        keywords=["continuous improvement", "quality management", "ISO 9001", "process optimization", "PDCA"],
        conclusion_template="Continuous improvement and quality management systems must be implemented to optimize water treatment processes and ensure compliance.",
        reasoning_framework=(
            "1. Establish quality management objectives and metrics.\n"
            "2. Implement the Plan-Do-Check-Act (PDCA) cycle for process improvement.\n"
            "3. Monitor performance and identify areas for improvement.\n"
            "4. Document changes and outcomes.\n"
            "5. Review and update quality management plans regularly."
        ),
        key_factors=[
            "Quality objectives",
            "Process monitoring",
            "PDCA cycle",
            "Documentation",
            "Management review"
        ],
        primary_authority=[
            "ISO 9001",
            "AWWA G200",
            "EPA Quality Management Guidance"
        ],
        burden_holder="Quality manager",
        adversary_position="Existing processes are sufficient.",
        counter_arguments=[
            "Continuous improvement reduces costs and risks.",
            "ISO 9001 certification may be required.",
            "Quality management ensures compliance."
        ],
        resolution_strategy="Implement and maintain a quality management system.",
        entity_scope="All water treatment organizations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
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