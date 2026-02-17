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
        topic="TCEQ Permit Requirements for Oilfield Operations",
        keywords=["TCEQ", "permit", "oilfield", "Texas", "environmental compliance"],
        conclusion_template="Oilfield operations in Texas must obtain applicable TCEQ permits prior to construction and operation.",
        reasoning_framework="""
        1. Determine whether the oilfield operation constitutes a 'facility' under 30 TAC §116.
        2. Assess the types of emissions, discharges, or waste streams generated.
        3. Review applicability of New Source Review (NSR) permitting, Standard Permits, and Permit by Rule (PBR).
        4. Evaluate the need for water, air, and waste permits based on operational scope.
        5. Confirm compliance with state and federal environmental regulations incorporated by reference.
        6. Analyze any exemptions or exclusions under TCEQ rules.
        7. Document all permitting decisions and maintain records for inspection.
        """,
        key_factors=[
            "Facility location within Texas",
            "Nature and scale of operations",
            "Type and quantity of emissions or discharges",
            "Exemptions under 30 TAC",
            "Prior enforcement history"
        ],
        primary_authority=[
            "30 TAC §116",
            "Texas Water Code",
            "Texas Health & Safety Code"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may assert that a permit is required for any emission-generating operation.",
        counter_arguments=[
            "Operation qualifies for a Permit by Rule (PBR)",
            "Activity is specifically exempted under 30 TAC",
            "No regulated emissions or discharges"
        ],
        resolution_strategy="Submit permit applications or exemption justifications to TCEQ and obtain written confirmation.",
        entity_scope="Oilfield operators in Texas",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="TCEQ v. Texas Oil & Gas Co., 2015"
    ),
    DoctrineBlock(
        topic="EPA NPDES Permit Applicability",
        keywords=["EPA", "NPDES", "permit", "discharge", "water", "oilfield"],
        conclusion_template="Discharges of pollutants from oilfield operations to waters of the United States require an NPDES permit.",
        reasoning_framework="""
        1. Identify all points of discharge to surface waters.
        2. Determine if the receiving water is a 'water of the United States' under 40 CFR §122.2.
        3. Assess whether the discharge contains pollutants as defined by the Clean Water Act.
        4. Evaluate the applicability of general or individual NPDES permits.
        5. Review any categorical exclusions or waivers.
        6. Coordinate with state agencies if delegated NPDES authority exists.
        7. Maintain monitoring and reporting as required by the permit.
        """,
        key_factors=[
            "Presence of a discharge to surface water",
            "Nature of pollutants",
            "Jurisdictional status of receiving water",
            "State vs. federal permitting authority"
        ],
        primary_authority=[
            "Clean Water Act §402",
            "40 CFR Part 122"
        ],
        burden_holder="Operator",
        adversary_position="EPA may assert jurisdiction over any discharge to surface water.",
        counter_arguments=[
            "Discharge is to non-jurisdictional water",
            "No pollutants present",
            "Covered by an existing general permit"
        ],
        resolution_strategy="Obtain NPDES permit or demonstrate non-applicability through technical and legal analysis.",
        entity_scope="Oilfield operators with water discharges",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Rapanos v. United States, 547 U.S. 715 (2006)"
    ),
    DoctrineBlock(
        topic="Clean Water Act Section 402 Compliance",
        keywords=["CWA", "Section 402", "NPDES", "compliance", "oilfield", "discharge"],
        conclusion_template="Oilfield operators must comply with all NPDES permit conditions under CWA Section 402.",
        reasoning_framework="""
        1. Review all applicable NPDES permit terms and conditions.
        2. Implement monitoring, sampling, and reporting protocols.
        3. Maintain records of discharge monitoring reports (DMRs).
        4. Respond promptly to any exceedances or violations.
        5. Train personnel on permit requirements and best management practices.
        6. Prepare for EPA or state inspections and audits.
        7. Update compliance plans as regulations or permits change.
        """,
        key_factors=[
            "Permit terms and conditions",
            "Monitoring and reporting frequency",
            "Corrective action procedures",
            "Employee training"
        ],
        primary_authority=[
            "Clean Water Act §402",
            "40 CFR Part 122"
        ],
        burden_holder="Operator",
        adversary_position="EPA may allege non-compliance for any deviation from permit terms.",
        counter_arguments=[
            "De minimis or excusable non-compliance",
            "Force majeure events",
            "Timely self-reporting and corrective action"
        ],
        resolution_strategy="Demonstrate good faith compliance and document all actions taken.",
        entity_scope="NPDES permit holders",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000)"
    ),
    DoctrineBlock(
        topic="Clean Air Act Permit by Rule (PBR) Applicability",
        keywords=["Clean Air Act", "PBR", "permit by rule", "air", "oilfield", "Texas"],
        conclusion_template="Oilfield operations may qualify for Permit by Rule if they meet the criteria in 30 TAC §106.",
        reasoning_framework="""
        1. Identify emission sources and quantify potential to emit (PTE).
        2. Compare emissions to PBR thresholds in 30 TAC §106.
        3. Review specific PBR requirements for oil and gas operations.
        4. Ensure compliance with recordkeeping and notification provisions.
        5. Evaluate cumulative impacts if multiple PBRs are used at a single site.
        6. Document eligibility and maintain supporting calculations.
        7. Submit PBR registration to TCEQ if required.
        """,
        key_factors=[
            "Potential to emit (PTE)",
            "Type of emission sources",
            "PBR eligibility criteria",
            "Notification and recordkeeping"
        ],
        primary_authority=[
            "Clean Air Act",
            "30 TAC §106"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may require a case-by-case permit if PBR criteria are not met.",
        counter_arguments=[
            "Emissions below PBR thresholds",
            "Site qualifies for multiple PBRs",
            "No significant cumulative impacts"
        ],
        resolution_strategy="Maintain documentation and seek TCEQ concurrence on PBR applicability.",
        entity_scope="Oilfield air emission sources in Texas",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="TCEQ Guidance Document RG-378"
    ),
    DoctrineBlock(
        topic="SPCC Plan Requirements",
        keywords=["SPCC", "oil", "spill", "prevention", "plan", "EPA", "40 CFR 112"],
        conclusion_template="Facilities with aboveground oil storage >1,320 gallons must prepare and implement an SPCC Plan.",
        reasoning_framework="""
        1. Inventory all aboveground and buried oil storage containers.
        2. Calculate total aboveground storage capacity.
        3. Determine if the facility could reasonably discharge oil to navigable waters.
        4. Prepare an SPCC Plan certified by a Professional Engineer, if required.
        5. Implement secondary containment and inspection protocols.
        6. Train personnel and conduct regular drills.
        7. Review and update the SPCC Plan every five years or after significant changes.
        """,
        key_factors=[
            "Total aboveground oil storage capacity",
            "Proximity to navigable waters",
            "Secondary containment measures",
            "Plan certification"
        ],
        primary_authority=[
            "40 CFR Part 112",
            "Clean Water Act §311"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA may enforce penalties for failure to prepare or implement an SPCC Plan.",
        counter_arguments=[
            "Storage below threshold",
            "No reasonable pathway to navigable waters",
            "Temporary storage"
        ],
        resolution_strategy="Maintain current SPCC Plan and evidence of compliance.",
        entity_scope="Oilfield facilities with oil storage",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Guidance for Regional Inspectors (2013)"
    ),
    DoctrineBlock(
        topic="Tier II Chemical Reporting (EPCRA §312)",
        keywords=["Tier II", "EPCRA", "chemical reporting", "hazardous chemicals", "SERC", "LEPC"],
        conclusion_template="Facilities storing hazardous chemicals above threshold quantities must submit Tier II reports annually.",
        reasoning_framework="""
        1. Identify all hazardous chemicals present at the facility.
        2. Compare quantities to EPCRA §312 thresholds (e.g., 10,000 lbs for most chemicals).
        3. Prepare Tier II forms with required information.
        4. Submit reports to the State Emergency Response Commission (SERC), Local Emergency Planning Committee (LEPC), and local fire department.
        5. Update reports annually or upon significant changes.
        6. Maintain records for at least three years.
        7. Train staff on reporting obligations and emergency response.
        """,
        key_factors=[
            "Type and quantity of hazardous chemicals",
            "EPCRA threshold levels",
            "Timeliness and accuracy of reporting",
            "Recordkeeping"
        ],
        primary_authority=[
            "EPCRA §312",
            "40 CFR Part 370"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="State or EPA may penalize for late or incomplete reporting.",
        counter_arguments=[
            "Chemicals below threshold",
            "Exempted substances (e.g., food, tobacco)",
            "No significant changes since last report"
        ],
        resolution_strategy="Implement robust inventory and reporting systems.",
        entity_scope="Facilities storing hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Tier II Chemical Inventory Reporting Guidance"
    ),
    DoctrineBlock(
        topic="RCRA Hazardous Waste Determination",
        keywords=["RCRA", "hazardous waste", "determination", "generator", "EPA", "40 CFR 262"],
        conclusion_template="Generators must determine if waste is hazardous under RCRA before disposal.",
        reasoning_framework="""
        1. Identify all waste streams generated by the operation.
        2. Apply the RCRA hazardous waste definition (characteristic and listed wastes).
        3. Test waste for ignitability, corrosivity, reactivity, and toxicity.
        4. Check for inclusion on EPA hazardous waste lists (F, K, P, U).
        5. Document the determination process and analytical results.
        6. Classify generator status (CESQG, SQG, LQG) based on monthly generation.
        7. Manage hazardous waste in accordance with applicable requirements.
        """,
        key_factors=[
            "Waste composition and characteristics",
            "Volume of waste generated",
            "Analytical testing results",
            "Documentation"
        ],
        primary_authority=[
            "RCRA",
            "40 CFR Part 262"
        ],
        burden_holder="Generator",
        adversary_position="EPA may assert waste is hazardous based on sampling or process knowledge.",
        counter_arguments=[
            "Waste meets solid waste exclusions",
            "Analytical data supports non-hazardous classification",
            "Process knowledge documentation"
        ],
        resolution_strategy="Maintain defensible records and conduct periodic reviews.",
        entity_scope="Waste generators",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="40 CFR 262.11"
    ),
    DoctrineBlock(
        topic="NORM Disposal Compliance",
        keywords=["NORM", "naturally occurring radioactive material", "disposal", "oilfield", "Texas", "TCEQ"],
        conclusion_template="NORM waste must be managed and disposed in accordance with state and federal regulations.",
        reasoning_framework="""
        1. Identify sources of NORM in oilfield equipment and waste streams.
        2. Characterize NORM levels using appropriate sampling and analysis.
        3. Segregate NORM waste from non-radioactive waste.
        4. Select disposal options authorized by TCEQ and Texas Department of State Health Services (DSHS).
        5. Maintain manifests and disposal records.
        6. Train personnel on NORM handling and safety.
        7. Notify regulatory agencies as required by state law.
        """,
        key_factors=[
            "Presence and concentration of NORM",
            "Disposal facility authorization",
            "Recordkeeping",
            "Personnel training"
        ],
        primary_authority=[
            "30 TAC §336",
            "Texas Health & Safety Code Chapter 401"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/DSHS may allege improper disposal or handling.",
        counter_arguments=[
            "Material below regulatory thresholds",
            "Disposal at licensed facility",
            "Proper documentation"
        ],
        resolution_strategy="Follow state-approved procedures and retain disposal records.",
        entity_scope="Oilfield operators handling NORM",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="TCEQ RG-173"
    ),
    DoctrineBlock(
        topic="Air Quality Standard Permit Applicability",
        keywords=["air quality", "standard permit", "TCEQ", "oilfield", "emissions"],
        conclusion_template="Oilfield operations may require a Standard Permit if emissions exceed PBR thresholds.",
        reasoning_framework="""
        1. Quantify emissions from all sources at the facility.
        2. Compare total emissions to Permit by Rule (PBR) thresholds.
        3. If emissions exceed PBR limits, evaluate Standard Permit applicability under 30 TAC §116.
        4. Review Standard Permit requirements for oil and gas facilities.
        5. Prepare permit application and supporting documentation.
        6. Submit application to TCEQ and await approval before commencing operations.
        7. Implement monitoring and recordkeeping as required by the permit.
        """,
        key_factors=[
            "Total facility emissions",
            "PBR threshold exceedance",
            "Standard Permit eligibility",
            "Application completeness"
        ],
        primary_authority=[
            "30 TAC §116",
            "Clean Air Act"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may require a case-by-case NSR permit if Standard Permit criteria are not met.",
        counter_arguments=[
            "Emissions below Standard Permit thresholds",
            "Facility qualifies for PBR",
            "No significant air impacts"
        ],
        resolution_strategy="Engage TCEQ early and maintain clear emissions records.",
        entity_scope="Oilfield facilities in Texas",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="TCEQ Standard Permit for Oil & Gas Facilities"
    ),
    DoctrineBlock(
        topic="Flaring and Venting Regulations",
        keywords=["flaring", "venting", "air", "emissions", "oilfield", "TCEQ", "GHG"],
        conclusion_template="Flaring and venting of gas must comply with state and federal limitations and reporting requirements.",
        reasoning_framework="""
        1. Identify all sources of flaring and venting at the facility.
        2. Review TCEQ and Railroad Commission of Texas (RRC) rules on allowable flaring/venting.
        3. Quantify volumes and durations of flaring/venting events.
        4. Obtain necessary authorizations or permits for routine and emergency flaring.
        5. Monitor and report emissions as required by TCEQ, RRC, and EPA.
        6. Implement measures to minimize flaring/venting and recover gas where feasible.
        7. Maintain records for inspection and enforcement purposes.
        """,
        key_factors=[
            "Volume and duration of flaring/venting",
            "Permit or authorization status",
            "Reporting and recordkeeping",
            "Emission minimization"
        ],
        primary_authority=[
            "16 TAC §3.32",
            "30 TAC §101",
            "EPA GHG Reporting Rule"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/RRC may allege unauthorized or excessive flaring.",
        counter_arguments=[
            "Events within permit limits",
            "Emergency or unavoidable releases",
            "Emission minimization efforts"
        ],
        resolution_strategy="Obtain all required authorizations and document compliance.",
        entity_scope="Oilfield operators in Texas",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="RRC Statewide Rule 32"
    ),
    DoctrineBlock(
        topic="Stormwater SWPPP Requirements",
        keywords=["stormwater", "SWPPP", "oilfield", "construction", "EPA", "TCEQ"],
        conclusion_template="Construction and industrial oilfield sites must implement a SWPPP and obtain stormwater permit coverage.",
        reasoning_framework="""
        1. Determine if the site meets the definition of a construction or industrial activity under 40 CFR 122.26(b).
        2. Prepare a Stormwater Pollution Prevention Plan (SWPPP) addressing site-specific controls.
        3. Apply for coverage under the EPA or TCEQ General Permit for stormwater discharges.
        4. Implement best management practices (BMPs) to minimize pollutant runoff.
        5. Conduct regular inspections and maintain records.
        6. Train personnel on SWPPP implementation and spill response.
        7. Update SWPPP as site conditions or regulations change.
        """,
        key_factors=[
            "Site activity type",
            "Permit coverage status",
            "SWPPP completeness",
            "BMP implementation"
        ],
        primary_authority=[
            "Clean Water Act §402",
            "40 CFR Part 122",
            "TCEQ TXR050000"
        ],
        burden_holder="Operator",
        adversary_position="EPA/TCEQ may allege unpermitted stormwater discharges.",
        counter_arguments=[
            "Site below regulatory thresholds",
            "No stormwater discharges",
            "Alternative compliance measures"
        ],
        resolution_strategy="Maintain current SWPPP and evidence of permit coverage.",
        entity_scope="Oilfield construction and industrial sites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA Multi-Sector General Permit"
    ),
    DoctrineBlock(
        topic="Spill Notification Thresholds",
        keywords=["spill", "notification", "threshold", "oil", "hazardous substance", "reporting"],
        conclusion_template="Spills exceeding reportable quantities must be reported to the appropriate agencies within required timeframes.",
        reasoning_framework="""
        1. Identify the substance and quantity released.
        2. Compare the release amount to federal and state reportable quantities (RQs).
        3. Determine the pathway and potential impacts of the release.
        4. Notify the National Response Center (NRC), TCEQ, and local authorities as required.
        5. Document the release, notifications, and response actions.
        6. Conduct root cause analysis and implement corrective actions.
        7. Retain records for regulatory review.
        """,
        key_factors=[
            "Substance released",
            "Quantity and duration",
            "Pathway to environment",
            "Timeliness of notification"
        ],
        primary_authority=[
            "CERCLA §103",
            "EPCRA §304",
            "30 TAC §327"
        ],
        burden_holder="Operator",
        adversary_position="Agencies may allege failure to report or delayed notification.",
        counter_arguments=[
            "Release below RQ",
            "Contained on-site",
            "No environmental impact"
        ],
        resolution_strategy="Implement spill response and notification protocols.",
        entity_scope="All oilfield facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA List of Lists (2022)"
    ),
    DoctrineBlock(
        topic="CERCLA Reporting Requirements",
        keywords=["CERCLA", "reporting", "release", "hazardous substance", "NRC", "oilfield"],
        conclusion_template="Releases of hazardous substances above CERCLA RQs must be reported to the NRC immediately.",
        reasoning_framework="""
        1. Identify the hazardous substance released and calculate the quantity.
        2. Compare the amount to the CERCLA reportable quantity (RQ) for that substance.
        3. If the RQ is exceeded, notify the National Response Center (NRC) without delay.
        4. Document the time, location, and circumstances of the release.
        5. Implement response and remediation measures.
        6. Submit follow-up written reports as required.
        7. Retain records for at least three years.
        """,
        key_factors=[
            "Substance and RQ",
            "Timeliness of notification",
            "Documentation",
            "Remediation actions"
        ],
        primary_authority=[
            "CERCLA §103",
            "40 CFR Part 302"
        ],
        burden_holder="Operator",
        adversary_position="EPA may pursue penalties for failure to report or late notification.",
        counter_arguments=[
            "Release below RQ",
            "Contained and remediated immediately",
            "No off-site impact"
        ],
        resolution_strategy="Establish clear release reporting procedures and train staff.",
        entity_scope="Oilfield operators handling hazardous substances",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="40 CFR 302.6"
    ),
    DoctrineBlock(
        topic="EPCRA Tier II Reporting",
        keywords=["EPCRA", "Tier II", "chemical inventory", "reporting", "hazardous chemicals"],
        conclusion_template="Facilities must submit Tier II reports for hazardous chemicals above threshold quantities annually.",
        reasoning_framework="""
        1. Inventory all hazardous chemicals on-site.
        2. Compare quantities to EPCRA Tier II reporting thresholds.
        3. Prepare and submit Tier II forms to SERC, LEPC, and local fire department.
        4. Update reports annually or upon significant changes.
        5. Maintain records for regulatory review.
        6. Train staff on chemical inventory and reporting requirements.
        7. Respond promptly to agency inquiries.
        """,
        key_factors=[
            "Chemical inventory accuracy",
            "Threshold determination",
            "Timeliness of reporting",
            "Recordkeeping"
        ],
        primary_authority=[
            "EPCRA §312",
            "40 CFR Part 370"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA or state may allege incomplete or late reporting.",
        counter_arguments=[
            "Chemicals below thresholds",
            "Exempted substances",
            "No significant changes"
        ],
        resolution_strategy="Implement robust inventory tracking and reporting systems.",
        entity_scope="Facilities with hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Tier II Reporting Guidance"
    ),
    DoctrineBlock(
        topic="State Implementation Plan (SIP) Compliance",
        keywords=["SIP", "state implementation plan", "Clean Air Act", "air quality", "TCEQ"],
        conclusion_template="Oilfield operations must comply with all SIP-approved air quality requirements.",
        reasoning_framework="""
        1. Review the applicable SIP for the state and region of operation.
        2. Identify all emission limits, control requirements, and monitoring obligations.
        3. Implement controls and practices to ensure compliance.
        4. Maintain records of emissions, monitoring, and corrective actions.
        5. Prepare for periodic inspections by TCEQ or EPA.
        6. Update compliance strategies as SIPs are revised.
        7. Engage with regulatory agencies on SIP interpretations as needed.
        """,
        key_factors=[
            "Applicable SIP provisions",
            "Emission limits",
            "Monitoring and recordkeeping",
            "Agency inspections"
        ],
        primary_authority=[
            "Clean Air Act §110",
            "40 CFR Part 52"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/EPA may allege non-compliance with SIP requirements.",
        counter_arguments=[
            "Demonstrated compliance",
            "Alternative control measures approved",
            "Recordkeeping supports compliance"
        ],
        resolution_strategy="Maintain up-to-date compliance plans and engage with agencies proactively.",
        entity_scope="Oilfield air emission sources",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas SIP, 40 CFR 52.2270"
    ),
    DoctrineBlock(
        topic="Opacity Monitoring Requirements",
        keywords=["opacity", "monitoring", "air emissions", "visible emissions", "TCEQ", "oilfield"],
        conclusion_template="Facilities must monitor and control visible emissions to meet opacity standards.",
        reasoning_framework="""
        1. Identify emission points subject to opacity limits.
        2. Install and operate continuous opacity monitoring systems (COMS) if required.
        3. Conduct periodic visual inspections using EPA Method 9.
        4. Record and report opacity exceedances as required by permit or regulation.
        5. Implement corrective actions for exceedances.
        6. Maintain monitoring and inspection records.
        7. Train personnel on opacity monitoring protocols.
        """,
        key_factors=[
            "Emission point classification",
            "Monitoring system installation",
            "Inspection frequency",
            "Corrective action procedures"
        ],
        primary_authority=[
            "30 TAC §111",
            "40 CFR Part 60"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may allege violations based on opacity exceedances.",
        counter_arguments=[
            "Exceedances due to startup/shutdown",
            "Demonstrated corrective action",
            "Permitted variances"
        ],
        resolution_strategy="Maintain robust monitoring and documentation systems.",
        entity_scope="Oilfield facilities with air emissions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Method 9"
    ),
    DoctrineBlock(
        topic="VOC Emissions Calculation and Control",
        keywords=["VOC", "volatile organic compounds", "emissions", "calculation", "control", "oilfield"],
        conclusion_template="Operators must calculate and control VOC emissions to comply with permit and regulatory limits.",
        reasoning_framework="""
        1. Identify all VOC emission sources at the facility.
        2. Quantify emissions using EPA-approved methods (e.g., AP-42, TANKS).
        3. Compare total VOC emissions to permit and regulatory limits.
        4. Implement control technologies (e.g., VRUs, flares, condensers) as needed.
        5. Monitor and record emissions data.
        6. Report emissions as required by TCEQ/EPA.
        7. Review and update calculations annually or after process changes.
        """,
        key_factors=[
            "Emission source identification",
            "Calculation methodology",
            "Control technology effectiveness",
            "Reporting accuracy"
        ],
        primary_authority=[
            "30 TAC §115",
            "40 CFR Part 60 Subpart OOOO"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/EPA may allege underestimation or lack of controls.",
        counter_arguments=[
            "Use of conservative calculation methods",
            "Demonstrated control efficiency",
            "No exceedance of limits"
        ],
        resolution_strategy="Maintain transparent calculation and control documentation.",
        entity_scope="Oilfield VOC sources",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA AP-42"
    ),
    DoctrineBlock(
        topic="Greenhouse Gas (GHG) Reporting",
        keywords=["GHG", "greenhouse gas", "reporting", "EPA", "oilfield", "Subpart W"],
        conclusion_template="Facilities emitting ≥25,000 metric tons CO2e/year must report GHG emissions to EPA.",
        reasoning_framework="""
        1. Calculate total GHG emissions from all sources using EPA methodologies.
        2. Determine if emissions exceed the 25,000 metric ton CO2e threshold.
        3. Register with EPA's e-GGRT system.
        4. Prepare and submit annual GHG reports by March 31.
        5. Maintain supporting records for at least three years.
        6. Implement QA/QC procedures for data accuracy.
        7. Respond to EPA inquiries or audits.
        """,
        key_factors=[
            "Total GHG emissions",
            "Calculation methodology",
            "Reporting timeliness",
            "Record retention"
        ],
        primary_authority=[
            "40 CFR Part 98 Subpart W",
            "Clean Air Act"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA may allege under-reporting or non-reporting.",
        counter_arguments=[
            "Emissions below threshold",
            "Methodology disputes",
            "Demonstrated good faith efforts"
        ],
        resolution_strategy="Implement robust GHG inventory and reporting systems.",
        entity_scope="Large oilfield facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA GHG Reporting Rule"
    ),
    DoctrineBlock(
        topic="Title V Operating Permit Applicability",
        keywords=["Title V", "operating permit", "Clean Air Act", "major source", "TCEQ", "oilfield"],
        conclusion_template="Major sources of air emissions must obtain a Title V Operating Permit.",
        reasoning_framework="""
        1. Calculate facility-wide potential to emit (PTE) for regulated pollutants.
        2. Compare PTE to major source thresholds (e.g., 100 tpy for criteria pollutants).
        3. If major source, prepare and submit Title V application to TCEQ.
        4. Implement monitoring, recordkeeping, and reporting as required by the permit.
        5. Update permit as operations change.
        6. Prepare for periodic compliance certifications and inspections.
        7. Maintain permit and supporting documentation on-site.
        """,
        key_factors=[
            "Facility PTE",
            "Major source threshold",
            "Application completeness",
            "Ongoing compliance"
        ],
        primary_authority=[
            "Clean Air Act Title V",
            "30 TAC §122"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/EPA may allege unpermitted major source operation.",
        counter_arguments=[
            "PTE below threshold",
            "Federally enforceable limits",
            "Temporary exceedance"
        ],
        resolution_strategy="Maintain accurate PTE calculations and engage with TCEQ.",
        entity_scope="Major air emission sources",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="40 CFR Part 70"
    ),
    DoctrineBlock(
        topic="Area Source NESHAP Applicability",
        keywords=["NESHAP", "area source", "hazardous air pollutants", "oilfield", "40 CFR 63"],
        conclusion_template="Oilfield area sources may be subject to NESHAP standards for specific HAPs.",
        reasoning_framework="""
        1. Identify all processes and equipment emitting hazardous air pollutants (HAPs).
        2. Determine if the facility is a major or area source under 40 CFR 63.
        3. Review applicable NESHAP subparts (e.g., HH, HHH).
        4. Implement required controls, monitoring, and recordkeeping.
        5. Submit notifications and reports as required.
        6. Train personnel on NESHAP compliance.
        7. Maintain records for at least five years.
        """,
        key_factors=[
            "HAP emission sources",
            "Area vs. major source status",
            "Applicable NESHAP subparts",
            "Compliance documentation"
        ],
        primary_authority=[
            "40 CFR Part 63",
            "Clean Air Act §112"
        ],
        burden_holder="Operator",
        adversary_position="EPA may allege non-compliance with NESHAP standards.",
        counter_arguments=[
            "Not subject to specific subpart",
            "Emissions below thresholds",
            "Alternative compliance options"
        ],
        resolution_strategy="Conduct applicability determinations and maintain records.",
        entity_scope="Oilfield area sources",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="40 CFR 63 Subpart HH"
    ),
    # Additional doctrines for completeness (total 40+)
    DoctrineBlock(
        topic="Produced Water Management and Beneficial Use",
        keywords=["produced water", "management", "beneficial use", "disposal", "TCEQ", "RRC"],
        conclusion_template="Produced water must be managed in accordance with TCEQ and RRC rules; beneficial use may require additional approvals.",
        reasoning_framework="""
        1. Characterize produced water for constituents and volume.
        2. Evaluate disposal options (injection, surface discharge, reuse).
        3. Obtain necessary permits from TCEQ and RRC.
        4. For beneficial use (e.g., irrigation), assess water quality and end use.
        5. Implement monitoring and reporting protocols.
        6. Maintain records of treatment and disposition.
        7. Engage with agencies on innovative reuse proposals.
        """,
        key_factors=[
            "Produced water composition",
            "Disposal/reuse method",
            "Permit status",
            "End use controls"
        ],
        primary_authority=[
            "16 TAC §3.8",
            "30 TAC §327"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ/RRC may restrict beneficial use or require additional controls.",
        counter_arguments=[
            "Demonstrated treatment effectiveness",
            "No adverse environmental impacts",
            "Agency concurrence"
        ],
        resolution_strategy="Engage with agencies early and maintain robust records.",
        entity_scope="Oilfield operators managing produced water",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="RRC SWR 8"
    ),
    DoctrineBlock(
        topic="Waste Minimization Certification",
        keywords=["waste minimization", "certification", "hazardous waste", "RCRA", "generator"],
        conclusion_template="Generators must certify that they have a waste minimization program in place.",
        reasoning_framework="""
        1. Develop and implement a waste minimization program.
        2. Document efforts to reduce hazardous waste generation.
        3. Certify waste minimization on manifests and biennial reports.
        4. Review program effectiveness annually.
        5. Train personnel on waste minimization practices.
        6. Update program as processes change.
        7. Maintain records for regulatory review.
        """,
        key_factors=[
            "Program implementation",
            "Documentation",
            "Personnel training",
            "Annual review"
        ],
        primary_authority=[
            "RCRA §3002(b)",
            "40 CFR 262.27"
        ],
        burden_holder="Generator",
        adversary_position="EPA may allege inadequate waste minimization efforts.",
        counter_arguments=[
            "Documented program",
            "Continuous improvement",
            "Industry best practices"
        ],
        resolution_strategy="Maintain and periodically update waste minimization program.",
        entity_scope="Hazardous waste generators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Waste Minimization Guidance"
    ),
    DoctrineBlock(
        topic="Universal Waste Management",
        keywords=["universal waste", "management", "batteries", "lamps", "hazardous waste", "RCRA"],
        conclusion_template="Universal wastes must be managed under streamlined RCRA standards.",
        reasoning_framework="""
        1. Identify all universal wastes generated (e.g., batteries, lamps, mercury devices).
        2. Store universal waste in labeled containers.
        3. Accumulate universal waste for no more than one year.
        4. Ship universal waste to authorized handlers or destination facilities.
        5. Train employees on universal waste requirements.
        6. Maintain shipping and disposal records.
        7. Respond to releases or spills promptly.
        """,
        key_factors=[
            "Waste classification",
            "Storage and labeling",
            "Accumulation time",
            "Employee training"
        ],
        primary_authority=[
            "40 CFR Part 273",
            "30 TAC §335 Subchapter H"
        ],
        burden_holder="Generator",
        adversary_position="EPA/TCEQ may allege improper management or disposal.",
        counter_arguments=[
            "Proper labeling and storage",
            "Timely shipment",
            "Employee training records"
        ],
        resolution_strategy="Implement universal waste management procedures.",
        entity_scope="Facilities generating universal waste",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Universal Waste Rule"
    ),
    DoctrineBlock(
        topic="Used Oil Management Standards",
        keywords=["used oil", "management", "RCRA", "recycling", "storage", "disposal"],
        conclusion_template="Used oil must be managed in accordance with EPA and state standards to avoid hazardous waste classification.",
        reasoning_framework="""
        1. Store used oil in containers/tanks labeled 'Used Oil'.
        2. Prevent releases to the environment.
        3. Recycle used oil through authorized facilities where possible.
        4. Dispose of used oil at permitted facilities if not recycled.
        5. Maintain records of shipments and receipts.
        6. Train personnel on used oil management.
        7. Respond to spills and releases promptly.
        """,
        key_factors=[
            "Storage and labeling",
            "Recycling vs. disposal",
            "Release prevention",
            "Recordkeeping"
        ],
        primary_authority=[
            "40 CFR Part 279",
            "30 TAC §324"
        ],
        burden_holder="Generator",
        adversary_position="EPA/TCEQ may allege improper management or disposal.",
        counter_arguments=[
            "Proper labeling and storage",
            "Recycling documentation",
            "Timely spill response"
        ],
        resolution_strategy="Implement used oil management procedures and maintain records.",
        entity_scope="Facilities generating used oil",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA Used Oil Management Standards"
    ),
    DoctrineBlock(
        topic="Hazardous Materials Transportation Compliance",
        keywords=["hazardous materials", "transportation", "DOT", "PHMSA", "oilfield", "shipping"],
        conclusion_template="Hazardous materials must be transported in accordance with DOT and PHMSA regulations.",
        reasoning_framework="""
        1. Classify hazardous materials for transport.
        2. Package, label, and mark materials per DOT requirements.
        3. Prepare shipping papers and emergency response information.
        4. Use authorized transporters with valid DOT registration.
        5. Train employees on hazardous materials shipping.
        6. Report releases or incidents as required.
        7. Maintain shipping and training records.
        """,
        key_factors=[
            "Material classification",
            "Packaging and labeling",
            "Transporter authorization",
            "Employee training"
        ],
        primary_authority=[
            "49 CFR Parts 171-180",
            "Hazardous Materials Transportation Act"
        ],
        burden_holder="Shipper",
        adversary_position="DOT/PHMSA may allege violations for improper shipping.",
        counter_arguments=[
            "Proper documentation",
            "Employee training",
            "Incident response"
        ],
        resolution_strategy="Implement DOT-compliant shipping procedures.",
        entity_scope="Oilfield hazardous materials shippers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="DOT Hazardous Materials Regulations"
    ),
    DoctrineBlock(
        topic="Emergency Planning and Community Right-to-Know",
        keywords=["emergency planning", "community right-to-know", "EPCRA", "SERC", "LEPC"],
        conclusion_template="Facilities must comply with EPCRA emergency planning and notification requirements.",
        reasoning_framework="""
        1. Identify extremely hazardous substances (EHS) present above threshold planning quantities.
        2. Notify SERC and LEPC of EHS presence.
        3. Participate in local emergency planning as requested.
        4. Submit emergency and hazardous chemical inventory forms (Tier II).
        5. Provide MSDS/SDS to local agencies upon request.
        6. Update notifications as inventory changes.
        7. Train personnel on emergency response procedures.
        """,
        key_factors=[
            "EHS inventory",
            "Notification timeliness",
            "Participation in planning",
            "Personnel training"
        ],
        primary_authority=[
            "EPCRA §§302-312",
            "40 CFR Part 355"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA/state may allege failure to notify or participate.",
        counter_arguments=[
            "No EHS above thresholds",
            "Timely notifications",
            "Active participation"
        ],
        resolution_strategy="Maintain up-to-date notifications and participate in planning.",
        entity_scope="Facilities with EHS",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA EPCRA Guidance"
    ),
    DoctrineBlock(
        topic="Oil Spill Response Plan (OSRP) Requirements",
        keywords=["oil spill", "response plan", "OSRP", "EPA", "preparedness"],
        conclusion_template="Facilities subject to SPCC may also require an OSRP if certain thresholds are met.",
        reasoning_framework="""
        1. Assess oil storage capacity and proximity to navigable waters.
        2. Determine if the facility meets OSRP applicability under 40 CFR 112.20.
        3. Prepare an OSRP addressing response actions, resources, and coordination.
        4. Submit OSRP to EPA if required.
        5. Conduct drills and exercises.
        6. Update OSRP as facility conditions change.
        7. Train personnel on OSRP implementation.
        """,
        key_factors=[
            "Oil storage capacity",
            "Proximity to navigable waters",
            "Plan completeness",
            "Personnel training"
        ],
        primary_authority=[
            "40 CFR 112.20",
            "Clean Water Act §311(j)"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA may allege inadequate preparedness or plan implementation.",
        counter_arguments=[
            "Below OSRP thresholds",
            "Integrated with SPCC Plan",
            "Regular drills and updates"
        ],
        resolution_strategy="Maintain current OSRP and conduct regular drills.",
        entity_scope="Large oil storage facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Oil Pollution Prevention Regulation"
    ),
    DoctrineBlock(
        topic="Well Plugging and Abandonment Environmental Compliance",
        keywords=["well plugging", "abandonment", "environmental compliance", "RRC", "TCEQ"],
        conclusion_template="Wells must be plugged and abandoned in accordance with RRC and TCEQ environmental requirements.",
        reasoning_framework="""
        1. Notify RRC and TCEQ of intent to plug and abandon wells.
        2. Develop plugging plan addressing environmental protection.
        3. Remove surface equipment and remediate surface contamination.
        4. Plug wellbore per RRC rules.
        5. Dispose of wastes at authorized facilities.
        6. Submit plugging reports and closure documentation.
        7. Conduct post-closure monitoring if required.
        """,
        key_factors=[
            "Plugging plan approval",
            "Waste disposal",
            "Surface remediation",
            "Reporting"
        ],
        primary_authority=[
            "16 TAC §3.14",
            "30 TAC §327"
        ],
        burden_holder="Operator",
        adversary_position="RRC/TCEQ may allege improper plugging or remediation.",
        counter_arguments=[
            "Plan approval",
            "Proper waste disposal",
            "Surface restoration"
        ],
        resolution_strategy="Follow approved plugging plan and document all actions.",
        entity_scope="Oilfield operators plugging wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RRC Well Plugging Rules"
    ),
    DoctrineBlock(
        topic="Air Emission Inventory Reporting",
        keywords=["air emission inventory", "reporting", "TCEQ", "oilfield", "annual"],
        conclusion_template="Facilities meeting reporting thresholds must submit annual air emission inventories to TCEQ.",
        reasoning_framework="""
        1. Quantify emissions from all sources using approved methods.
        2. Compare emissions to TCEQ reporting thresholds.
        3. Prepare and submit emission inventory reports by the annual deadline.
        4. Maintain supporting calculations and records.
        5. Respond to TCEQ requests for clarification or additional data.
        6. Update inventory as facility operations change.
        7. Train staff on inventory preparation.
        """,
        key_factors=[
            "Total emissions",
            "Reporting thresholds",
            "Calculation methodology",
            "Timeliness"
        ],
        primary_authority=[
            "30 TAC §101.10",
            "Clean Air Act"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="TCEQ may allege under-reporting or late submission.",
        counter_arguments=[
            "Emissions below threshold",
            "Timely submission",
            "Supporting documentation"
        ],
        resolution_strategy="Implement robust emission tracking and reporting systems.",
        entity_scope="Facilities with significant air emissions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="TCEQ Emissions Inventory Guidance"
    ),
    DoctrineBlock(
        topic="Hazardous Waste Manifest Requirements",
        keywords=["hazardous waste", "manifest", "shipping", "RCRA", "EPA"],
        conclusion_template="Hazardous waste shipments must be accompanied by a properly completed manifest.",
        reasoning_framework="""
        1. Prepare EPA Form 8700-22 for each hazardous waste shipment.
        2. Ensure all information is accurate and complete.
        3. Obtain signatures from generator, transporter, and TSDF.
        4. Retain copies of completed manifests for at least three years.
        5. Reconcile returned manifests and resolve discrepancies.
        6. Submit exception reports if manifests are not returned.
        7. Train personnel on manifest procedures.
        """,
        key_factors=[
            "Manifest accuracy",
            "Signature chain",
            "Record retention",
            "Exception reporting"
        ],
        primary_authority=[
            "40 CFR Part 262 Subpart B",
            "RCRA"
        ],
        burden_holder="Generator",
        adversary_position="EPA/state may allege incomplete or missing manifests.",
        counter_arguments=[
            "Properly completed manifests",
            "Timely exception reports",
            "Employee training"
        ],
        resolution_strategy="Implement manifest tracking and reconciliation procedures.",
        entity_scope="Hazardous waste generators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Manifest System"
    ),
    DoctrineBlock(
        topic="Underground Injection Control (UIC) Compliance",
        keywords=["UIC", "underground injection", "disposal well", "EPA", "RRC", "Class II"],
        conclusion_template="Operators must comply with UIC permit conditions for disposal and enhanced recovery wells.",
        reasoning_framework="""
        1. Obtain UIC permit from RRC or EPA for Class II wells.
        2. Monitor injection pressures, rates, and volumes.
        3. Conduct mechanical integrity tests as required.
        4. Report monitoring data to the permitting agency.
        5. Respond to excursions or violations promptly.
        6. Maintain well construction and operation records.
        7. Plug and abandon wells per permit conditions.
        """,
        key_factors=[
            "Permit status",
            "Monitoring and reporting",
            "Mechanical integrity",
            "Well abandonment"
        ],
        primary_authority=[
            "Safe Drinking Water Act",
            "40 CFR Parts 144-147",
            "16 TAC §3.9"
        ],
        burden_holder="Operator",
        adversary_position="EPA/RRC may allege permit violations or endangerment.",
        counter_arguments=[
            "Demonstrated compliance",
            "Prompt corrective action",
            "Agency notifications"
        ],
        resolution_strategy="Maintain robust monitoring and reporting systems.",
        entity_scope="Operators of injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA UIC Program"
    ),
    DoctrineBlock(
        topic="Oil and Gas Exploration and Production (E&P) Waste Exemption",
        keywords=["E&P waste", "exemption", "RCRA", "oilfield", "solid waste"],
        conclusion_template="Certain E&P wastes are exempt from RCRA Subtitle C hazardous waste regulation.",
        reasoning_framework="""
        1. Identify waste streams generated from exploration, development, or production.
        2. Determine if wastes are covered by the E&P exemption.
        3. Manage exempt wastes under state solid waste rules.
        4. Document exemption applicability and management practices.
        5. Review EPA and state guidance on E&P waste classification.
        6. Train personnel on proper waste segregation.
        7. Reassess exemption status as operations change.
        """,
        key_factors=[
            "Waste origin and process",
            "Exemption criteria",
            "State solid waste rules",
            "Documentation"
        ],
        primary_authority=[
            "RCRA",
            "EPA E&P Waste Exemption Guidance"
        ],
        burden_holder="Operator",
        adversary_position="EPA/state may allege misclassification or improper management.",
        counter_arguments=[
            "Waste meets exemption criteria",
            "Proper documentation",
            "State concurrence"
        ],
        resolution_strategy="Maintain clear records and consult with agencies as needed.",
        entity_scope="Oil and gas E&P operators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="53 FR 25446 (July 6, 1988)"
    ),
    DoctrineBlock(
        topic="Facility Response Plan (FRP) Applicability",
        keywords=["facility response plan", "FRP", "oil storage", "EPA", "emergency response"],
        conclusion_template="Facilities with oil storage >1 million gallons may require an FRP under 40 CFR 112.",
        reasoning_framework="""
        1. Calculate total oil storage capacity at the facility.
        2. Assess proximity to navigable waters and sensitive environments.
        3. Determine if the facility meets FRP applicability criteria.
        4. Prepare and submit an FRP to EPA if required.
        5. Conduct drills and exercises.
        6. Update FRP as facility conditions change.
        7. Train personnel on FRP implementation.
        """,
        key_factors=[
            "Oil storage capacity",
            "Proximity to sensitive environments",
            "Plan completeness",
            "Personnel training"
        ],
        primary_authority=[
            "40 CFR 112.20",
            "Clean Water Act §311(j)"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA may allege inadequate preparedness or plan implementation.",
        counter_arguments=[
            "Below FRP thresholds",
            "Integrated with SPCC/OSRP",
            "Regular drills and updates"
        ],
        resolution_strategy="Maintain current FRP and conduct regular drills.",
        entity_scope="Large oil storage facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Oil Pollution Prevention Regulation"
    ),
    DoctrineBlock(
        topic="Air Permit Deviation and Excursion Reporting",
        keywords=["air permit", "deviation", "excursion", "reporting", "TCEQ"],
        conclusion_template="Permit deviations and excursions must be reported to TCEQ as required by permit conditions.",
        reasoning_framework="""
        1. Identify and document all permit deviations and excursions.
        2. Notify TCEQ within the timeframe specified in the permit.
        3. Investigate root causes and implement corrective actions.
        4. Submit written reports detailing the event and response.
        5. Maintain records of all deviations and agency communications.
        6. Train personnel on deviation reporting procedures.
        7. Review and update reporting protocols as needed.
        """,
        key_factors=[
            "Deviation documentation",
            "Notification timeliness",
            "Corrective action",
            "Recordkeeping"
        ],
        primary_authority=[
            "30 TAC §122.145",
            "Clean Air Act"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may allege failure to report or inadequate response.",
        counter_arguments=[
            "Timely notification",
            "Comprehensive corrective action",
            "Supporting documentation"
        ],
        resolution_strategy="Implement deviation tracking and reporting systems.",
        entity_scope="Title V and NSR permit holders",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="TCEQ Deviation Reporting Guidance"
    ),
    DoctrineBlock(
        topic="Hazardous Waste Contingency Plan Requirements",
        keywords=["hazardous waste", "contingency plan", "emergency response", "RCRA", "generator"],
        conclusion_template="Large Quantity Generators must maintain a hazardous waste contingency plan.",
        reasoning_framework="""
        1. Prepare a written contingency plan addressing emergency response to hazardous waste incidents.
        2. Designate emergency coordinators and provide contact information.
        3. Distribute plan to local emergency responders.
        4. Train personnel on plan implementation.
        5. Review and update plan as operations change.
        6. Maintain plan and training records on-site.
        7. Conduct periodic drills.
        """,
        key_factors=[
            "Plan completeness",
            "Personnel training",
            "Distribution to responders",
            "Drills and updates"
        ],
        primary_authority=[
            "40 CFR 262.261",
            "RCRA"
        ],
        burden_holder="Large Quantity Generator",
        adversary_position="EPA/state may allege inadequate planning or training.",
        counter_arguments=[
            "Comprehensive plan",
            "Regular training and drills",
            "Timely updates"
        ],
        resolution_strategy="Maintain current plan and conduct regular training.",
        entity_scope="Large Quantity Generators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Contingency Plan Guidance"
    ),
    DoctrineBlock(
        topic="Stormwater Discharge Monitoring and Reporting",
        keywords=["stormwater", "discharge monitoring", "reporting", "SWPPP", "oilfield"],
        conclusion_template="Facilities must monitor and report stormwater discharges as required by permit.",
        reasoning_framework="""
        1. Implement monitoring protocols specified in the SWPPP and permit.
        2. Collect and analyze stormwater samples at required intervals.
        3. Record monitoring data and compare to permit benchmarks.
        4. Submit discharge monitoring reports (DMRs) to agencies.
        5. Investigate and address benchmark exceedances.
        6. Maintain monitoring and reporting records.
        7. Update SWPPP as monitoring results dictate.
        """,
        key_factors=[
            "Monitoring protocol implementation",
            "Sampling frequency",
            "Reporting accuracy",
            "Corrective actions"
        ],
        primary_authority=[
            "40 CFR 122.44",
            "TCEQ TXR050000"
        ],
        burden_holder="Operator",
        adversary_position="EPA/TCEQ may allege monitoring or reporting deficiencies.",
        counter_arguments=[
            "Timely and accurate reporting",
            "Corrective action documentation",
            "No exceedances"
        ],
        resolution_strategy="Maintain robust monitoring and reporting systems.",
        entity_scope="Facilities with stormwater discharges",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA MSGP"
    ),
    DoctrineBlock(
        topic="Air Emission Control Device Maintenance",
        keywords=["air emission", "control device", "maintenance", "TCEQ", "compliance"],
        conclusion_template="Control devices must be maintained to ensure continuous compliance with emission limits.",
        reasoning_framework="""
        1. Develop and implement maintenance schedules for all emission control devices.
        2. Conduct inspections and preventive maintenance.
        3. Record maintenance activities and repairs.
        4. Respond promptly to device malfunctions or failures.
        5. Notify TCEQ of significant control device outages as required.
        6. Maintain records for regulatory review.
        7. Train personnel on maintenance procedures.
        """,
        key_factors=[
            "Maintenance schedule adherence",
            "Inspection frequency",
            "Malfunction response",
            "Recordkeeping"
        ],
        primary_authority=[
            "30 TAC §101.211",
            "Clean Air Act"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may allege non-compliance due to control device failures.",
        counter_arguments=[
            "Documented maintenance",
            "Prompt repairs",
            "Notification of outages"
        ],
        resolution_strategy="Implement preventive maintenance and recordkeeping systems.",
        entity_scope="Facilities with emission controls",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="TCEQ Maintenance, Startup, and Shutdown Rules"
    ),
    DoctrineBlock(
        topic="Hazardous Waste Satellite Accumulation Area Management",
        keywords=["hazardous waste", "satellite accumulation", "area management", "RCRA", "generator"],
        conclusion_template="Satellite accumulation areas must be managed in accordance with RCRA standards.",
        reasoning_framework="""
        1. Accumulate hazardous waste at or near the point of generation.
        2. Limit accumulation to 55 gallons per waste stream.
        3. Label containers with 'Hazardous Waste' and accumulation start date.
        4. Move containers to central storage within three days of reaching limits.
        5. Inspect areas weekly and maintain records.
        6. Train personnel on satellite accumulation requirements.
        7. Respond to spills or releases promptly.
        """,
        key_factors=[
            "Location and volume limits",
            "Labeling and dating",
            "Inspection and recordkeeping",
            "Personnel training"
        ],
        primary_authority=[
            "40 CFR 262.15",
            "RCRA"
        ],
        burden_holder="Generator",
        adversary_position="EPA/state may allege improper accumulation or labeling.",
        counter_arguments=[
            "Compliance with volume and time limits",
            "Proper labeling",
            "Employee training"
        ],
        resolution_strategy="Implement satellite accumulation procedures and training.",
        entity_scope="Hazardous waste generators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Satellite Accumulation Guidance"
    ),
    DoctrineBlock(
        topic="Air Quality Modeling for Permit Applications",
        keywords=["air quality modeling", "permit application", "TCEQ", "oilfield", "dispersion modeling"],
        conclusion_template="Air quality modeling may be required to demonstrate permit compliance.",
        reasoning_framework="""
        1. Determine if modeling is required based on emission rates and location.
        2. Select appropriate modeling protocol (e.g., AERMOD).
        3. Develop input data and run simulations.
        4. Compare modeled concentrations to NAAQS and state standards.
        5. Document modeling methodology and results.
        6. Submit modeling report with permit application.
        7. Respond to agency questions or requests for additional analysis.
        """,
        key_factors=[
            "Emission rates",
            "Model selection",
            "Input data quality",
            "Compliance with standards"
        ],
        primary_authority=[
            "30 TAC §116.111",
            "EPA Guideline on Air Quality Models"
        ],
        burden_holder="Applicant",
        adversary_position="TCEQ may require additional modeling or controls.",
        counter_arguments=[
            "Conservative modeling assumptions",
            "Demonstrated compliance",
            "Mitigation measures"
        ],
        resolution_strategy="Engage with TCEQ early and document all modeling decisions.",
        entity_scope="Facilities seeking air permits",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Guideline on Air Quality Models"
    ),
    DoctrineBlock(
        topic="Hazardous Waste Generator Category Determination",
        keywords=["hazardous waste", "generator category", "CESQG", "SQG", "LQG", "RCRA"],
        conclusion_template="Generator category determines applicable hazardous waste requirements.",
        reasoning_framework="""
        1. Calculate total hazardous waste generated per calendar month.
        2. Classify as CESQG, SQG, or LQG based on generation rates.
        3. Apply corresponding accumulation, storage, and reporting requirements.
        4. Update category as generation rates change.
        5. Maintain records of monthly generation.
        6. Train personnel on category-specific requirements.
        7. Notify agencies of category changes as required.
        """,
        key_factors=[
            "Monthly generation rates",
            "Category thresholds",
            "Recordkeeping",
            "Personnel training"
        ],
        primary_authority=[
            "40 CFR 262.13",
            "RCRA"
        ],
        burden_holder="Generator",
        adversary_position="EPA/state may allege misclassification or non-compliance.",
        counter_arguments=[
            "Accurate records",
            "Timely updates",
            "Employee training"
        ],
        resolution_strategy="Implement tracking and review of generation rates.",
        entity_scope="Hazardous waste generators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Generator Improvements Rule"
    ),
    DoctrineBlock(
        topic="Oilfield Pit and Impoundment Closure",
        keywords=["pit closure", "impoundment", "oilfield", "RRC", "environmental compliance"],
        conclusion_template="Oilfield pits and impoundments must be closed in accordance with RRC rules.",
        reasoning_framework="""
        1. Notify RRC of intent to close pit or impoundment.
        2. Remove all fluids and solids for proper disposal.
        3. Sample and analyze residuals for contaminants.
        4. Backfill and grade site to prevent erosion.
        5. Submit closure documentation to RRC.
        6. Conduct post-closure monitoring if required.
        7. Maintain closure records for regulatory review.
        """,
        key_factors=[
            "Notification and approval",
            "Waste removal and disposal",
            "Site restoration",
            "Recordkeeping"
        ],
        primary_authority=[
            "16 TAC §3.8",
            "RRC Pit Closure Guidance"
        ],
        burden_holder="Operator",
        adversary_position="RRC may allege improper closure or remediation.",
        counter_arguments=[
            "Closure plan approval",
            "Proper waste disposal",
            "Site restoration"
        ],
        resolution_strategy="Follow approved closure plan and document all actions.",
        entity_scope="Oilfield operators closing pits",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RRC Pit Closure Rules"
    ),
    DoctrineBlock(
        topic="Facility Security and Access Control",
        keywords=["facility security", "access control", "oilfield", "environmental compliance"],
        conclusion_template="Facilities must implement security measures to prevent unauthorized access and environmental releases.",
        reasoning_framework="""
        1. Assess facility security risks and vulnerabilities.
        2. Install fencing, gates, and signage as appropriate.
        3. Control access to hazardous materials and waste storage areas.
        4. Implement visitor and contractor check-in procedures.
        5. Train personnel on security protocols.
        6. Review and update security measures periodically.
        7. Document security incidents and corrective actions.
        """,
        key_factors=[
            "Physical barriers",
            "Access control procedures",
            "Personnel training",
            "Incident documentation"
        ],
        primary_authority=[
            "40 CFR 264.14",
            "RCRA"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA/state may allege inadequate security or access control.",
        counter_arguments=[
            "Documented security measures",
            "Incident response procedures",
            "Periodic reviews"
        ],
        resolution_strategy="Implement and periodically review security protocols.",
        entity_scope="Oilfield facilities",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA Security Guidance for Hazardous Waste Facilities"
    ),
    DoctrineBlock(
        topic="Environmental Training and Awareness Programs",
        keywords=["environmental training", "awareness", "oilfield", "compliance", "personnel"],
        conclusion_template="Facilities must provide environmental compliance training to relevant personnel.",
        reasoning_framework="""
        1. Identify personnel with environmental compliance responsibilities.
        2. Develop training programs covering applicable regulations and procedures.
        3. Conduct initial and periodic refresher training.
        4. Maintain training records for regulatory review.
        5. Evaluate training effectiveness through testing or observation.
        6. Update training content as regulations or operations change.
        7. Encourage a culture of environmental awareness.
        """,
        key_factors=[
            "Training program content",
            "Frequency of training",
            "Recordkeeping",
            "Evaluation of effectiveness"
        ],
        primary_authority=[
            "40 CFR 265.16",
            "RCRA"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA/state may allege inadequate training.",
        counter_arguments=[
            "Documented training",
            "Periodic refreshers",
            "Employee testing"
        ],
        resolution_strategy="Implement and document comprehensive training programs.",
        entity_scope="Oilfield facilities",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Training Requirements for Hazardous Waste Facilities"
    ),
    DoctrineBlock(
        topic="Environmental Audit Privilege and Immunity",
        keywords=["environmental audit", "privilege", "immunity", "Texas", "self-disclosure"],
        conclusion_template="Texas law provides limited privilege and immunity for voluntary environmental audits.",
        reasoning_framework="""
        1. Conduct voluntary environmental audits in accordance with Texas Environmental, Health, and Safety Audit Privilege Act.
        2. Document audit scope, findings, and corrective actions.
        3. Submit self-disclosure to TCEQ within 45 days of discovery.
        4. Cooperate with TCEQ investigations.
        5. Privilege does not apply to criminal conduct or imminent harm.
        6. Maintain audit records as confidential where applicable.
        7. Update compliance programs based on audit findings.
        """,
        key_factors=[
            "Voluntary audit status",
            "Timeliness of self-disclosure",
            "Corrective action",
            "Scope of privilege"
        ],
        primary_authority=[
            "Texas Health & Safety Code Chapter 1101",
            "TCEQ Audit Privilege Guidance"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may challenge privilege or immunity claims.",
        counter_arguments=[
            "Good faith audit",
            "Timely disclosure",
            "No criminal conduct"
        ],
        resolution_strategy="Follow statutory audit procedures and maintain documentation.",
        entity_scope="Texas facilities",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Audit Privilege Act"
    ),
    DoctrineBlock(
        topic="Environmental Justice and Community Engagement",
        keywords=["environmental justice", "community engagement", "oilfield", "EPA", "TCEQ"],
        conclusion_template="Operators must consider environmental justice concerns and engage with affected communities.",
        reasoning_framework="""
        1. Identify potentially affected communities, especially those with environmental justice concerns.
        2. Assess potential disproportionate impacts from facility operations.
        3. Engage in meaningful outreach and consultation.
        4. Incorporate community feedback into project planning.
        5. Document engagement activities and outcomes.
        6. Respond to agency requests for environmental justice analysis.
        7. Update engagement strategies as needed.
        """,
        key_factors=[
            "Community demographics",
            "Potential impacts",
            "Outreach effectiveness",
            "Documentation"
        ],
        primary_authority=[
            "Executive Order 12898",
            "EPA EJ Guidance"
        ],
        burden_holder="Operator",
        adversary_position="EPA/TCEQ may require additional analysis or mitigation.",
        counter_arguments=[
            "Comprehensive engagement",
            "Mitigation of impacts",
            "Agency concurrence"
        ],
        resolution_strategy="Implement and document robust community engagement.",
        entity_scope="Oilfield operators",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="EPA Environmental Justice Policy"
    ),
    DoctrineBlock(
        topic="Endangered Species Act (ESA) Consultation",
        keywords=["ESA", "endangered species", "consultation", "USFWS", "oilfield"],
        conclusion_template="Projects with potential impacts to listed species require ESA consultation.",
        reasoning_framework="""
        1. Identify presence of listed species or critical habitat in project area.
        2. Assess potential impacts from construction or operations.
        3. Initiate consultation with USFWS if impacts are likely.
        4. Implement avoidance, minimization, or mitigation measures.
        5. Document consultation process and outcomes.
        6. Update project plans as required by USFWS.
        7. Train personnel on ESA compliance.
        """,
        key_factors=[
            "Species/habitat presence",
            "Impact assessment",
            "Consultation initiation",
            "Mitigation measures"
        ],
        primary_authority=[
            "Endangered Species Act §7",
            "USFWS Consultation Handbook"
        ],
        burden_holder="Project proponent",
        adversary_position="USFWS may require additional mitigation or deny authorization.",
        counter_arguments=[
            "No listed species present",
            "No adverse impacts",
            "Effective mitigation"
        ],
        resolution_strategy="Engage with USFWS early and document all steps.",
        entity_scope="Oilfield projects with potential ESA impacts",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="USFWS ESA Consultation Handbook"
    ),
    DoctrineBlock(
        topic="Migratory Bird Treaty Act (MBTA) Compliance",
        keywords=["MBTA", "migratory birds", "compliance", "oilfield", "USFWS"],
        conclusion_template="Operators must avoid unauthorized take of migratory birds during operations.",
        reasoning_framework="""
        1. Identify presence of migratory birds in project area.
        2. Implement measures to avoid take (e.g., timing, deterrents).
        3. Train personnel on MBTA requirements.
        4. Document avoidance and minimization efforts.
        5. Notify USFWS of incidental take as required.
        6. Update procedures as guidance evolves.
        7. Respond to agency inquiries or enforcement actions.
        """,
        key_factors=[
            "Bird presence",
            "Avoidance measures",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "Migratory Bird Treaty Act",
            "USFWS Guidance"
        ],
        burden_holder="Operator",
        adversary_position="USFWS may allege unauthorized take.",
        counter_arguments=[
            "No take occurred",
            "Effective avoidance measures",
            "Agency concurrence"
        ],
        resolution_strategy="Implement and document avoidance measures.",
        entity_scope="Oilfield operators",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="USFWS MBTA Guidance"
    ),
    DoctrineBlock(
        topic="Cultural Resource Protection (NHPA Section 106)",
        keywords=["NHPA", "cultural resource", "Section 106", "oilfield", "SHPO"],
        conclusion_template="Projects with federal involvement must comply with NHPA Section 106 review.",
        reasoning_framework="""
        1. Determine if project involves federal permits, funding, or lands.
        2. Identify and evaluate cultural resources in project area.
        3. Consult with State Historic Preservation Officer (SHPO).
        4. Assess project impacts and develop mitigation as needed.
        5. Document Section 106 process and outcomes.
        6. Update project plans per SHPO recommendations.
        7. Train personnel on cultural resource protection.
        """,
        key_factors=[
            "Federal nexus",
            "Resource identification",
            "Consultation",
            "Mitigation"
        ],
        primary_authority=[
            "NHPA Section 106",
            "36 CFR Part 800"
        ],
        burden_holder="Project proponent",
        adversary_position="SHPO/agency may require additional mitigation or deny approval.",
        counter_arguments=[
            "No adverse effects",
            "Mitigation measures",
            "Agency concurrence"
        ],
        resolution_strategy="Engage with SHPO early and document all steps.",
        entity_scope="Oilfield projects with federal involvement",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NHPA Section 106 Regulations"
    ),
    DoctrineBlock(
        topic="Environmental Permitting Due Diligence",
        keywords=["permitting", "due diligence", "environmental compliance", "oilfield", "acquisition"],
        conclusion_template="Due diligence must assess all environmental permitting requirements for oilfield assets.",
        reasoning_framework="""
        1. Inventory all permits, authorizations, and registrations for the asset.
        2. Assess permit status, expiration, and compliance history.
        3. Identify permit transfer or re-application requirements.
        4. Review pending enforcement actions or violations.
        5. Evaluate potential permitting gaps or deficiencies.
        6. Document findings and recommendations.
        7. Address permitting issues prior to acquisition or operation.
        """,
        key_factors=[
            "Permit inventory",
            "Compliance history",
            "Transfer requirements",
            "Pending enforcement"
        ],
        primary_authority=[
            "EPA Audit Policy",
            "TCEQ Permitting Guidance"
        ],
        burden_holder="Acquirer/operator",
        adversary_position="Regulators may require corrective action or deny transfers.",
        counter_arguments=[
            "Complete and current permits",
            "No outstanding violations",
            "Agency engagement"
        ],
        resolution_strategy="Conduct thorough due diligence and address issues proactively.",
        entity_scope="Oilfield asset transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Environmental Due Diligence Guidance"
    ),
    DoctrineBlock(
        topic="Environmental Recordkeeping and Retention",
        keywords=["environmental recordkeeping", "retention", "compliance", "oilfield"],
        conclusion_template="Facilities must retain environmental records for the periods specified by law and permit.",
        reasoning_framework="""
        1. Identify all required environmental records (e.g., permits, reports, monitoring data).
        2. Implement systems for secure storage and retrieval.
        3. Retain records for the minimum period specified by regulation or permit (typically 3-5 years).
        4. Ensure records are available for agency inspection.
        5. Train personnel on recordkeeping requirements.
        6. Review and update record retention schedules as needed.
        7. Securely dispose of records after retention period.
        """,
        key_factors=[
            "Record type",
            "Retention period",
            "Storage and retrieval",
            "Personnel training"
        ],
        primary_authority=[
            "40 CFR 262.40",
            "TCEQ Recordkeeping Guidance"
        ],
        burden_holder="Facility owner/operator",
        adversary_position="EPA/state may allege missing or incomplete records.",
        counter_arguments=[
            "Records maintained",
            "Timely retrieval",
            "Employee training"
        ],
        resolution_strategy="Implement and periodically review recordkeeping systems.",
        entity_scope="Oilfield facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Recordkeeping Requirements"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in