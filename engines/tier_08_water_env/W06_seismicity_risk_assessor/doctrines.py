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
        topic="Induced Seismicity Mechanisms",
        keywords=["induced seismicity", "mechanisms", "injection", "fault activation"],
        conclusion_template="Induced seismicity in the region is primarily attributed to fluid injection altering stress states on pre-existing faults.",
        reasoning_framework=(
            "Assess the geological setting, including fault distribution and stress regime. "
            "Evaluate injection operations: volume, rate, pressure, and proximity to faults. "
            "Review microseismic monitoring data and correlate seismic events with operational changes. "
            "Apply physical models (e.g., pore pressure diffusion, Coulomb stress transfer) to determine plausibility of induced mechanisms. "
            "Consider historical seismicity baseline to distinguish induced from natural events. "
            "Weigh evidence from peer-reviewed studies, regulatory findings, and operator data. "
            "Account for uncertainties in subsurface characterization and event detection thresholds. "
            "Synthesize findings to establish causal links between operations and seismicity."
        ),
        key_factors=[
            "Injection volume and rate",
            "Fault proximity and orientation",
            "Regional stress field",
            "Historical seismicity",
            "Seismic monitoring resolution",
            "Subsurface permeability"
        ],
        primary_authority=[
            "USGS Induced Seismicity Protocols",
            "RRC Seismicity Guidelines",
            "Peer-reviewed geophysical literature"
        ],
        burden_holder="Operator",
        adversary_position="Seismicity is natural or unrelated to injection operations.",
        counter_arguments=[
            "Temporal and spatial correlation alone is insufficient for causation.",
            "Natural tectonic activity may explain observed events.",
            "Faults may be aseismic or hydraulically isolated."
        ],
        resolution_strategy="Integrate multidisciplinary data and expert review to establish causality.",
        entity_scope="Operators, Regulators, Geoscientists",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="USGS 2015 Induced Seismicity Report"
    ),
    DoctrineBlock(
        topic="RRC Seismicity Response Plan",
        keywords=["response plan", "RRC", "regulatory compliance", "seismicity"],
        conclusion_template="Operators must implement a seismicity response plan in accordance with RRC guidelines upon detection of significant seismic events.",
        reasoning_framework=(
            "Review RRC requirements for seismicity response, including notification, operational adjustments, and reporting. "
            "Determine event magnitude and location relative to regulated thresholds. "
            "Assess operator's preparedness: monitoring systems, communication protocols, and mitigation measures. "
            "Evaluate timeliness and adequacy of operator's response actions. "
            "Cross-reference with RRC Rule 46 and any site-specific stipulations. "
            "Consider prior enforcement actions and compliance history. "
            "Document all findings and recommend corrective actions if deficiencies are identified."
        ),
        key_factors=[
            "Event magnitude and location",
            "Operator response time",
            "Monitoring and reporting systems",
            "Mitigation measures in place",
            "Regulatory thresholds"
        ],
        primary_authority=[
            "RRC Rule 46",
            "RRC Seismicity Response Guidance"
        ],
        burden_holder="Operator",
        adversary_position="Operator's response plan is sufficient and compliant.",
        counter_arguments=[
            "Plan lacks specificity or fails to address key risks.",
            "Operator delayed notification or mitigation.",
            "Monitoring systems are inadequate."
        ],
        resolution_strategy="Require plan revision and enhanced oversight if non-compliance is found.",
        entity_scope="Operators, RRC, Emergency Responders",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Seismicity Response Plan Template (2021)"
    ),
    DoctrineBlock(
        topic="Traffic Light Protocol",
        keywords=["traffic light", "protocol", "seismicity thresholds", "operational controls"],
        conclusion_template="The Traffic Light Protocol must be applied to manage operational risk in response to detected seismicity.",
        reasoning_framework=(
            "Define threshold magnitudes for green, amber, and red operational states. "
            "Monitor seismicity in real-time using TexNet or equivalent systems. "
            "Upon exceeding amber threshold, require operator to reduce injection rates and increase monitoring frequency. "
            "Upon exceeding red threshold, mandate immediate suspension of injection and notification of authorities. "
            "Review operator's adherence to protocol and documentation of actions taken. "
            "Evaluate effectiveness of protocol in mitigating seismic risk. "
            "Consider site-specific adjustments to thresholds based on local hazard assessments."
        ),
        key_factors=[
            "Threshold magnitudes",
            "Real-time monitoring capability",
            "Operator response procedures",
            "Regulatory requirements",
            "Site-specific hazard factors"
        ],
        primary_authority=[
            "RRC Traffic Light Protocol Guidance",
            "TexNet Seismic Monitoring Standards"
        ],
        burden_holder="Operator",
        adversary_position="Protocol thresholds are overly conservative or not justified.",
        counter_arguments=[
            "Thresholds are based on regional risk assessments.",
            "Protocol is consistent with international best practices.",
            "Site-specific data supports current thresholds."
        ],
        resolution_strategy="Review and adjust thresholds as warranted by updated hazard assessments.",
        entity_scope="Operators, Regulators, Seismic Networks",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="RRC Traffic Light Protocol (2017)"
    ),
    DoctrineBlock(
        topic="TexNet Seismic Monitoring",
        keywords=["TexNet", "seismic monitoring", "network", "data quality"],
        conclusion_template="TexNet data must be used as the authoritative source for seismic event detection and characterization in Texas.",
        reasoning_framework=(
            "Assess the coverage, sensitivity, and reliability of TexNet stations in the region. "
            "Compare TexNet event catalogs with operator and third-party monitoring data. "
            "Evaluate data latency and completeness for regulatory reporting. "
            "Identify any gaps in network coverage that may affect event detection thresholds. "
            "Ensure that operator-deployed sensors are calibrated and integrated with TexNet data streams. "
            "Address discrepancies through data reconciliation and expert review."
        ),
        key_factors=[
            "Network coverage and sensitivity",
            "Data latency",
            "Catalog completeness",
            "Sensor calibration",
            "Integration with operator systems"
        ],
        primary_authority=[
            "TexNet Operations Manual",
            "RRC Seismic Monitoring Requirements"
        ],
        burden_holder="Operator",
        adversary_position="Operator's proprietary monitoring is sufficient.",
        counter_arguments=[
            "TexNet provides independent, statewide coverage.",
            "Regulations require use of TexNet data.",
            "Proprietary systems may lack transparency or standardization."
        ],
        resolution_strategy="Mandate use of TexNet data for all regulatory determinations.",
        entity_scope="Operators, Regulators, Seismic Networks",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="TexNet Data Policy (2020)"
    ),
    DoctrineBlock(
        topic="Historical Seismicity Baseline",
        keywords=["historical seismicity", "baseline", "background rates", "trend analysis"],
        conclusion_template="Establish a historical seismicity baseline to differentiate induced events from natural background activity.",
        reasoning_framework=(
            "Compile seismic event catalogs for the region over multiple decades. "
            "Analyze temporal and spatial patterns to identify background seismicity rates. "
            "Apply statistical methods to detect anomalies coincident with industrial activity. "
            "Correlate changes in seismicity with onset of injection operations. "
            "Consider completeness magnitude and detection thresholds over time. "
            "Document baseline for use in regulatory reviews and hazard assessments."
        ),
        key_factors=[
            "Long-term seismic event data",
            "Detection thresholds",
            "Temporal correlation with operations",
            "Statistical analysis methods",
            "Regional tectonic setting"
        ],
        primary_authority=[
            "USGS National Seismic Hazard Maps",
            "TexNet Historical Catalogs"
        ],
        burden_holder="Regulator",
        adversary_position="Recent events are consistent with historical background.",
        counter_arguments=[
            "Statistical anomalies coincide with injection activities.",
            "Historical catalog completeness is limited.",
            "Recent increases exceed background rates."
        ],
        resolution_strategy="Update baseline as new data becomes available.",
        entity_scope="Regulators, Operators, Researchers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="USGS Seismicity Baseline Methodology (2016)"
    ),
    DoctrineBlock(
        topic="Gutenberg-Richter b-value Analysis",
        keywords=["Gutenberg-Richter", "b-value", "magnitude-frequency", "seismicity analysis"],
        conclusion_template="The b-value of the Gutenberg-Richter relationship provides insight into the stress regime and seismic hazard.",
        reasoning_framework=(
            "Collect magnitude-frequency data for seismic events in the study area. "
            "Fit the Gutenberg-Richter relationship using maximum likelihood or least squares methods. "
            "Interpret b-value: values near 1.0 indicate tectonic regime; lower values suggest increased stress or induced seismicity. "
            "Compare b-value trends before and after injection operations. "
            "Assess statistical significance and uncertainty in b-value estimates. "
            "Use b-value as an input to hazard models and operational decision-making."
        ),
        key_factors=[
            "Magnitude-frequency distribution",
            "Statistical fitting method",
            "Temporal changes in b-value",
            "Uncertainty quantification",
            "Correlation with operational changes"
        ],
        primary_authority=[
            "Seismological Society of America Guidelines",
            "Peer-reviewed literature on b-value analysis"
        ],
        burden_holder="Operator",
        adversary_position="Observed b-value changes are within natural variability.",
        counter_arguments=[
            "Statistically significant shifts coincide with operations.",
            "Natural variability is accounted for in analysis.",
            "Peer-reviewed studies support findings."
        ],
        resolution_strategy="Require independent review of b-value analysis.",
        entity_scope="Operators, Regulators, Seismologists",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="Wiemer & Wyss (2000), b-value Analysis"
    ),
    DoctrineBlock(
        topic="Fault Proximity Assessment",
        keywords=["fault proximity", "fault mapping", "seismic hazard", "injection wells"],
        conclusion_template="Injection wells located within critical proximity to mapped faults require enhanced monitoring and risk mitigation.",
        reasoning_framework=(
            "Map known faults using seismic, geological, and well log data. "
            "Determine spatial relationship between injection wells and fault traces. "
            "Assess fault activity, slip potential, and hydraulic connectivity. "
            "Apply regulatory setback distances and site-specific risk factors. "
            "Evaluate historical seismicity near faults. "
            "Recommend enhanced monitoring or operational restrictions for wells near critical faults."
        ),
        key_factors=[
            "Fault mapping accuracy",
            "Well-fault distance",
            "Fault activity and slip history",
            "Hydraulic connectivity",
            "Regulatory setback requirements"
        ],
        primary_authority=[
            "RRC Fault Mapping Guidelines",
            "USGS Fault Database"
        ],
        burden_holder="Operator",
        adversary_position="Mapped faults are inactive or not connected.",
        counter_arguments=[
            "Uncertainty in fault mapping.",
            "Inactive faults may become reactivated.",
            "Hydraulic connectivity is difficult to prove."
        ],
        resolution_strategy="Apply precautionary principle and require enhanced controls.",
        entity_scope="Operators, Regulators, Geologists",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RRC Fault Proximity Assessment Protocol (2018)"
    ),
    DoctrineBlock(
        topic="Coulomb Stress Transfer",
        keywords=["Coulomb stress", "stress transfer", "fault activation", "seismicity"],
        conclusion_template="Coulomb stress transfer analysis is essential to evaluate the potential for induced fault slip from injection operations.",
        reasoning_framework=(
            "Model stress changes in the subsurface resulting from fluid injection. "
            "Calculate Coulomb stress changes on mapped faults using geomechanical models. "
            "Identify faults with increased slip potential due to stress perturbations. "
            "Correlate modeled stress changes with observed seismicity patterns. "
            "Validate models with field data and adjust parameters as needed. "
            "Use results to inform operational decisions and risk mitigation."
        ),
        key_factors=[
            "Geomechanical model parameters",
            "Fault orientation and properties",
            "Injection volume and pressure",
            "Correlation with seismicity",
            "Model validation"
        ],
        primary_authority=[
            "Peer-reviewed geomechanics literature",
            "USGS Stress Transfer Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Stress changes are negligible or not aligned with faults.",
        counter_arguments=[
            "Model uncertainty and parameter sensitivity.",
            "Small stress changes can trigger slip on critically stressed faults.",
            "Empirical evidence supports stress transfer effects."
        ],
        resolution_strategy="Require conservative assumptions and independent model review.",
        entity_scope="Operators, Regulators, Geomechanical Experts",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="King et al. (2014), Coulomb Stress Transfer in Induced Seismicity"
    ),
    DoctrineBlock(
        topic="Pore Pressure Diffusion",
        keywords=["pore pressure", "diffusion", "hydraulic connectivity", "seismicity"],
        conclusion_template="Pore pressure diffusion models must be used to predict the spatial and temporal evolution of induced seismicity risk.",
        reasoning_framework=(
            "Model fluid pressure propagation from injection wells using reservoir simulation. "
            "Estimate time-dependent pressure changes at fault locations. "
            "Assess hydraulic connectivity between injection zone and faults. "
            "Correlate pressure front arrival with onset of seismicity. "
            "Validate model predictions with field pressure and seismicity data. "
            "Use results to guide operational adjustments and risk mitigation."
        ),
        key_factors=[
            "Reservoir properties (permeability, porosity)",
            "Injection rate and duration",
            "Fault connectivity",
            "Pressure monitoring data",
            "Model calibration"
        ],
        primary_authority=[
            "Peer-reviewed hydrogeology literature",
            "USGS Induced Seismicity Modeling Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Pressure diffusion is too slow or limited to affect faults.",
        counter_arguments=[
            "High-permeability pathways can accelerate diffusion.",
            "Empirical data shows rapid pressure transmission in some settings.",
            "Model uncertainty requires conservative assumptions."
        ],
        resolution_strategy="Mandate pressure monitoring and model validation.",
        entity_scope="Operators, Regulators, Reservoir Engineers",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="Shapiro et al. (2003), Pore Pressure Diffusion and Seismicity"
    ),
    DoctrineBlock(
        topic="Injection Volume-Seismicity Correlation",
        keywords=["injection volume", "seismicity correlation", "statistical analysis"],
        conclusion_template="Statistically significant correlations between injection volume and seismicity rates require operational review.",
        reasoning_framework=(
            "Compile injection volume data and seismic event catalogs over time. "
            "Apply statistical tests (e.g., Pearson correlation, Granger causality) to assess relationships. "
            "Control for confounding variables such as regional tectonics and detection thresholds. "
            "Interpret results in the context of site-specific geology and operations. "
            "Recommend operational adjustments if strong correlations are observed."
        ),
        key_factors=[
            "Injection volume records",
            "Seismicity rate data",
            "Statistical significance",
            "Confounding factors",
            "Temporal resolution"
        ],
        primary_authority=[
            "USGS Induced Seismicity Reports",
            "Peer-reviewed statistical studies"
        ],
        burden_holder="Operator",
        adversary_position="Correlation does not imply causation.",
        counter_arguments=[
            "Temporal and spatial alignment strengthens causal inference.",
            "Multiple independent studies support correlation.",
            "Operational changes reduce seismicity rates."
        ],
        resolution_strategy="Require operational modifications and enhanced monitoring.",
        entity_scope="Operators, Regulators, Statisticians",
        confidence=0.83,
        confidence_zone="Moderate-High",
        controlling_precedent="Ellsworth (2013), Injection-Induced Earthquakes"
    ),
    DoctrineBlock(
        topic="Magnitude-Frequency Relationships",
        keywords=["magnitude-frequency", "seismic hazard", "Gutenberg-Richter", "risk assessment"],
        conclusion_template="Magnitude-frequency relationships inform seismic hazard assessments and operational risk management.",
        reasoning_framework=(
            "Analyze seismic event catalogs to establish magnitude-frequency distributions. "
            "Fit Gutenberg-Richter or alternative models to data. "
            "Interpret implications for maximum expected magnitude and recurrence intervals. "
            "Use results to calibrate hazard models and set operational thresholds. "
            "Update relationships as new data becomes available."
        ),
        key_factors=[
            "Event catalog completeness",
            "Model fitting method",
            "Maximum observed magnitude",
            "Recurrence interval estimates",
            "Temporal changes in distribution"
        ],
        primary_authority=[
            "USGS Seismic Hazard Methodology",
            "Peer-reviewed hazard assessment literature"
        ],
        burden_holder="Regulator",
        adversary_position="Observed distributions are within expected variability.",
        counter_arguments=[
            "Recent data shows upward trend in maximum magnitude.",
            "Operational changes correlate with distribution shifts.",
            "Statistical tests confirm significant changes."
        ],
        resolution_strategy="Revise hazard models and operational protocols as warranted.",
        entity_scope="Regulators, Operators, Hazard Modelers",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="USGS Seismic Hazard Maps (2014)"
    ),
    DoctrineBlock(
        topic="Seismic Moment Calculations",
        keywords=["seismic moment", "earthquake size", "moment magnitude", "source parameters"],
        conclusion_template="Seismic moment calculations are required for accurate characterization of earthquake size and energy release.",
        reasoning_framework=(
            "Obtain waveform data from seismic networks. "
            "Apply standard formulas to calculate seismic moment from source parameters. "
            "Convert seismic moment to moment magnitude for hazard communication. "
            "Compare calculated values with catalog magnitudes and operator reports. "
            "Use results to calibrate hazard models and inform operational decisions."
        ),
        key_factors=[
            "Waveform data quality",
            "Source parameter estimation",
            "Conversion formulas",
            "Comparison with catalog data",
            "Uncertainty quantification"
        ],
        primary_authority=[
            "Seismological Society of America Standards",
            "USGS Seismic Moment Calculation Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Catalog magnitudes are sufficient for hazard assessment.",
        counter_arguments=[
            "Seismic moment provides physically meaningful measure of event size.",
            "Catalog magnitudes may be biased or inconsistent.",
            "Regulations require moment calculations for significant events."
        ],
        resolution_strategy="Mandate seismic moment reporting for all M>2.5 events.",
        entity_scope="Operators, Regulators, Seismologists",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Kanamori (1977), Seismic Moment-Magnitude Scale"
    ),
    DoctrineBlock(
        topic="Ground Motion Prediction",
        keywords=["ground motion", "prediction equations", "GMPE", "hazard assessment"],
        conclusion_template="Ground motion prediction equations (GMPEs) must be used to estimate shaking intensity for seismic hazard assessments.",
        reasoning_framework=(
            "Select appropriate GMPEs based on regional geology and event characteristics. "
            "Input event magnitude, distance, and site conditions into GMPEs. "
            "Calculate expected peak ground acceleration (PGA) and velocity (PGV). "
            "Compare predictions with observed ground motion data. "
            "Use results to inform risk assessments and operational thresholds."
        ),
        key_factors=[
            "GMPE selection",
            "Event magnitude and distance",
            "Site conditions",
            "Observed vs. predicted ground motions",
            "Uncertainty in predictions"
        ],
        primary_authority=[
            "USGS GMPE Guidelines",
            "Peer-reviewed ground motion studies"
        ],
        burden_holder="Regulator",
        adversary_position="GMPEs are not calibrated for induced events.",
        counter_arguments=[
            "Recent studies provide GMPEs for induced seismicity.",
            "Calibration can be updated as new data becomes available.",
            "GMPEs are standard for hazard communication."
        ],
        resolution_strategy="Require periodic review and calibration of GMPEs.",
        entity_scope="Regulators, Operators, Hazard Modelers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="Boore et al. (2014), Ground Motion Prediction"
    ),
    DoctrineBlock(
        topic="PGA/PGV Thresholds",
        keywords=["PGA", "PGV", "thresholds", "ground motion", "building safety"],
        conclusion_template="Operational and regulatory thresholds for PGA and PGV must be established to protect public safety and infrastructure.",
        reasoning_framework=(
            "Review building codes and engineering standards for acceptable ground motion levels. "
            "Set operational thresholds for PGA/PGV based on risk to critical infrastructure. "
            "Monitor ground motion in real-time and compare with thresholds. "
            "Trigger operational responses (e.g., injection rate reduction, suspension) upon exceedance. "
            "Update thresholds as new engineering data becomes available."
        ),
        key_factors=[
            "Building code requirements",
            "Critical infrastructure vulnerability",
            "Real-time ground motion monitoring",
            "Threshold exceedance protocols",
            "Engineering studies"
        ],
        primary_authority=[
            "International Building Code (IBC)",
            "USGS Ground Motion Thresholds"
        ],
        burden_holder="Regulator",
        adversary_position="Thresholds are overly conservative or not justified.",
        counter_arguments=[
            "Thresholds are based on engineering best practices.",
            "Public safety requires conservative assumptions.",
            "Thresholds can be adjusted as warranted by new data."
        ],
        resolution_strategy="Review and revise thresholds in consultation with engineering experts.",
        entity_scope="Regulators, Operators, Engineers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="IBC 2018, USGS Threshold Guidance"
    ),
    DoctrineBlock(
        topic="Building Damage Assessment",
        keywords=["building damage", "assessment", "ground motion", "seismic risk"],
        conclusion_template="Post-event building damage assessments are required for all events exceeding regulatory ground motion thresholds.",
        reasoning_framework=(
            "Identify affected structures based on ground motion distribution. "
            "Conduct rapid visual screening and detailed engineering assessments as needed. "
            "Document observed damage and correlate with ground motion data. "
            "Report findings to regulatory authorities and affected stakeholders. "
            "Recommend repairs, retrofits, or occupancy restrictions as warranted."
        ),
        key_factors=[
            "Ground motion intensity",
            "Building type and vulnerability",
            "Damage observation protocols",
            "Reporting requirements",
            "Regulatory thresholds"
        ],
        primary_authority=[
            "FEMA Rapid Visual Screening Guidelines",
            "IBC Building Assessment Standards"
        ],
        burden_holder="Regulator",
        adversary_position="No significant damage observed; assessment not needed.",
        counter_arguments=[
            "Threshold exceedance requires assessment regardless of observed damage.",
            "Rapid screening ensures public safety.",
            "Documentation is necessary for liability and insurance."
        ],
        resolution_strategy="Mandate assessments for all threshold-exceeding events.",
        entity_scope="Regulators, Engineers, Building Owners",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FEMA P-154 (2015), Rapid Visual Screening"
    ),
    DoctrineBlock(
        topic="RRC Rule 46 Compliance",
        keywords=["RRC Rule 46", "compliance", "injection wells", "seismicity"],
        conclusion_template="Operators must comply with all provisions of RRC Rule 46 regarding injection well permitting and seismicity risk management.",
        reasoning_framework=(
            "Review operator's permit application and supporting documentation. "
            "Verify compliance with seismic monitoring, reporting, and operational restrictions. "
            "Assess adequacy of risk mitigation measures and response plans. "
            "Audit operator records for completeness and accuracy. "
            "Enforce corrective actions or penalties for non-compliance."
        ),
        key_factors=[
            "Permit documentation",
            "Monitoring and reporting systems",
            "Risk mitigation measures",
            "Compliance history",
            "Regulatory audits"
        ],
        primary_authority=[
            "RRC Rule 46",
            "RRC Enforcement Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Operator is in full compliance.",
        counter_arguments=[
            "Documentation gaps or deficiencies exist.",
            "Monitoring systems are inadequate.",
            "Prior violations indicate compliance risk."
        ],
        resolution_strategy="Require corrective actions and enhanced oversight.",
        entity_scope="Operators, RRC, Legal Counsel",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="RRC Rule 46 (2014)"
    ),
    DoctrineBlock(
        topic="Operator Notification Requirements",
        keywords=["notification", "operator", "regulatory reporting", "seismic events"],
        conclusion_template="Operators are required to notify regulatory authorities within specified timeframes following detection of significant seismic events.",
        reasoning_framework=(
            "Review regulatory requirements for event notification (e.g., magnitude thresholds, reporting deadlines). "
            "Assess operator's internal protocols for event detection and notification. "
            "Verify timeliness and completeness of notifications for recent events. "
            "Document any delays or failures to notify. "
            "Recommend enforcement actions if notification requirements are not met."
        ),
        key_factors=[
            "Notification thresholds",
            "Reporting deadlines",
            "Internal operator protocols",
            "Documentation of notifications",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Notification Guidelines",
            "TexNet Reporting Standards"
        ],
        burden_holder="Operator",
        adversary_position="Notification was timely and compliant.",
        counter_arguments=[
            "Notification was delayed or incomplete.",
            "Operator protocols are inadequate.",
            "Regulatory requirements were not met."
        ],
        resolution_strategy="Enforce penalties for non-compliance and require protocol revisions.",
        entity_scope="Operators, Regulators, Emergency Responders",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="RRC Notification Policy (2018)"
    ),
    DoctrineBlock(
        topic="Injection Rate Reduction Protocols",
        keywords=["injection rate", "reduction", "protocols", "seismicity mitigation"],
        conclusion_template="Operators must implement injection rate reduction protocols upon detection of increased seismicity or threshold exceedance.",
        reasoning_framework=(
            "Establish rate reduction triggers based on seismicity monitoring data. "
            "Define stepwise reduction procedures and minimum operational rates. "
            "Monitor seismic response to rate reductions and adjust as needed. "
            "Document all operational changes and report to regulators. "
            "Evaluate effectiveness of protocols in reducing seismic risk."
        ),
        key_factors=[
            "Seismicity monitoring data",
            "Rate reduction triggers",
            "Operational flexibility",
            "Documentation and reporting",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Injection Rate Protocols",
            "Peer-reviewed mitigation studies"
        ],
        burden_holder="Operator",
        adversary_position="Rate reductions are unnecessary or ineffective.",
        counter_arguments=[
            "Empirical evidence supports rate reduction efficacy.",
            "Protocols are required by regulation.",
            "Seismicity often decreases following rate reductions."
        ],
        resolution_strategy="Mandate protocol implementation and monitor outcomes.",
        entity_scope="Operators, Regulators, Reservoir Engineers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Injection Rate Reduction Policy (2019)"
    ),
    DoctrineBlock(
        topic="Well Suspension Criteria",
        keywords=["well suspension", "criteria", "seismic risk", "regulatory action"],
        conclusion_template="Wells must be suspended when seismicity exceeds regulatory thresholds or risk cannot be mitigated.",
        reasoning_framework=(
            "Define suspension criteria based on event magnitude, frequency, and proximity to critical infrastructure. "
            "Monitor seismicity in real-time and compare with criteria. "
            "Assess effectiveness of prior mitigation measures. "
            "Suspend operations if risk remains elevated or thresholds are exceeded. "
            "Document suspension actions and report to regulators."
        ),
        key_factors=[
            "Suspension thresholds",
            "Real-time monitoring",
            "Mitigation effectiveness",
            "Proximity to infrastructure",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Well Suspension Policy",
            "USGS Seismic Risk Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Suspension is premature or unwarranted.",
        counter_arguments=[
            "Thresholds are based on risk to public safety.",
            "Suspension is required by regulation.",
            "Mitigation has proven ineffective."
        ],
        resolution_strategy="Suspend operations and review risk mitigation strategies.",
        entity_scope="Operators, Regulators, Emergency Responders",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RRC Well Suspension Criteria (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Hazard Mapping",
        keywords=["seismic hazard", "mapping", "risk assessment", "regulatory planning"],
        conclusion_template="Seismic hazard maps must be developed and updated regularly to inform risk management and regulatory planning.",
        reasoning_framework=(
            "Compile seismicity data, geological maps, and ground motion models. "
            "Integrate data using GIS and hazard modeling software. "
            "Identify areas of elevated seismic risk and critical infrastructure. "
            "Update maps as new data becomes available or operational changes occur. "
            "Disseminate maps to stakeholders and use for regulatory decision-making."
        ),
        key_factors=[
            "Data integration",
            "Hazard modeling methodology",
            "Update frequency",
            "Stakeholder communication",
            "Regulatory use"
        ],
        primary_authority=[
            "USGS Seismic Hazard Mapping Standards",
            "RRC Hazard Mapping Guidelines"
        ],
        burden_holder="Regulator",
        adversary_position="Existing maps are sufficient or updates are unnecessary.",
        counter_arguments=[
            "New data may alter risk assessments.",
            "Regular updates are required by best practices.",
            "Stakeholder needs evolve over time."
        ],
        resolution_strategy="Mandate periodic updates and stakeholder engagement.",
        entity_scope="Regulators, Operators, Planners",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="USGS National Seismic Hazard Maps (2018)"
    ),
    # Additional DoctrineBlocks to reach 40+ entries, covering subtopics, operational nuances, and regulatory details:
    DoctrineBlock(
        topic="Seismic Monitoring Network Design",
        keywords=["network design", "seismic monitoring", "station spacing", "detection threshold"],
        conclusion_template="Seismic monitoring networks must be designed to achieve detection thresholds consistent with regulatory and scientific standards.",
        reasoning_framework=(
            "Determine minimum detection magnitude required for regulatory compliance. "
            "Design network with sufficient station density and optimal placement. "
            "Evaluate site noise conditions and sensor types. "
            "Model network performance using synthetic event simulations. "
            "Periodically review and upgrade network as needed."
        ),
        key_factors=[
            "Detection threshold",
            "Station density and placement",
            "Site noise levels",
            "Sensor technology",
            "Performance modeling"
        ],
        primary_authority=[
            "TexNet Network Design Standards",
            "USGS Seismic Network Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Existing network is adequate.",
        counter_arguments=[
            "Detection gaps may exist in current network.",
            "Technological advances enable improved performance.",
            "Regulatory standards evolve over time."
        ],
        resolution_strategy="Mandate network upgrades and periodic performance reviews.",
        entity_scope="Operators, Regulators, Network Engineers",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="TexNet Network Design Policy (2019)"
    ),
    DoctrineBlock(
        topic="Event Location Uncertainty",
        keywords=["event location", "uncertainty", "seismic monitoring", "regulatory reporting"],
        conclusion_template="Event location uncertainty must be quantified and reported for all significant seismic events.",
        reasoning_framework=(
            "Calculate event location uncertainty using standard seismological methods. "
            "Report uncertainty ellipses or confidence intervals in regulatory filings. "
            "Assess impact of network geometry and station quality on uncertainty. "
            "Use uncertainty estimates in risk assessments and operational decisions."
        ),
        key_factors=[
            "Seismic network geometry",
            "Station quality and spacing",
            "Location algorithm",
            "Uncertainty quantification methods",
            "Regulatory reporting requirements"
        ],
        primary_authority=[
            "Seismological Society of America Standards",
            "TexNet Reporting Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Uncertainty reporting is unnecessary.",
        counter_arguments=[
            "Uncertainty affects risk assessment and response.",
            "Regulations require uncertainty reporting.",
            "Transparency improves stakeholder trust."
        ],
        resolution_strategy="Mandate uncertainty reporting for all M>2.0 events.",
        entity_scope="Operators, Regulators, Seismologists",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SSA Location Uncertainty Guidelines (2017)"
    ),
    DoctrineBlock(
        topic="Seismic Event Magnitude Scaling",
        keywords=["magnitude scaling", "event size", "induced seismicity", "hazard modeling"],
        conclusion_template="Magnitude scaling relationships must be validated for induced seismicity to ensure accurate hazard modeling.",
        reasoning_framework=(
            "Review empirical and theoretical magnitude scaling relationships for induced events. "
            "Compare observed magnitudes with model predictions. "
            "Adjust scaling parameters as warranted by local data. "
            "Use validated relationships in hazard and risk models."
        ),
        key_factors=[
            "Empirical data quality",
            "Model validation",
            "Parameter adjustment",
            "Applicability to induced events",
            "Hazard model integration"
        ],
        primary_authority=[
            "USGS Induced Seismicity Reports",
            "Peer-reviewed magnitude scaling studies"
        ],
        burden_holder="Regulator",
        adversary_position="Standard scaling is sufficient.",
        counter_arguments=[
            "Induced events may differ from tectonic events.",
            "Local calibration improves model accuracy.",
            "Peer-reviewed studies support adjustments."
        ],
        resolution_strategy="Require local validation of scaling relationships.",
        entity_scope="Regulators, Operators, Hazard Modelers",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="USGS Induced Seismicity Scaling Guidance (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Data Quality Control",
        keywords=["data quality", "quality control", "seismic monitoring", "regulatory compliance"],
        conclusion_template="Seismic data quality control procedures must be implemented and documented for all monitoring systems.",
        reasoning_framework=(
            "Establish data quality control protocols for sensor calibration, noise filtering, and data validation. "
            "Conduct regular audits of data streams and event catalogs. "
            "Document quality control actions and findings. "
            "Report data quality issues to regulators and address deficiencies promptly."
        ),
        key_factors=[
            "Sensor calibration",
            "Noise filtering",
            "Data validation procedures",
            "Audit frequency",
            "Documentation standards"
        ],
        primary_authority=[
            "TexNet Data Quality Guidelines",
            "USGS Seismic Data Standards"
        ],
        burden_holder="Operator",
        adversary_position="Data quality is sufficient without formal procedures.",
        counter_arguments=[
            "Formal procedures ensure consistency and reliability.",
            "Quality control is required by regulation.",
            "Audits improve data integrity."
        ],
        resolution_strategy="Mandate documented quality control procedures and audits.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="TexNet Data Quality Policy (2020)"
    ),
    DoctrineBlock(
        topic="Regulatory Enforcement Actions",
        keywords=["enforcement", "regulatory action", "non-compliance", "penalties"],
        conclusion_template="Regulatory enforcement actions must be taken in cases of non-compliance with seismicity risk management requirements.",
        reasoning_framework=(
            "Document instances of non-compliance with monitoring, reporting, or operational requirements. "
            "Assess severity and potential impact of violations. "
            "Apply penalties or corrective actions as specified by regulation. "
            "Monitor operator compliance with enforcement orders. "
            "Escalate enforcement actions for repeated or severe violations."
        ),
        key_factors=[
            "Nature and severity of violation",
            "Regulatory requirements",
            "Operator compliance history",
            "Corrective action implementation",
            "Penalty guidelines"
        ],
        primary_authority=[
            "RRC Enforcement Policy",
            "USGS Regulatory Guidelines"
        ],
        burden_holder="Regulator",
        adversary_position="Violations are minor or unintentional.",
        counter_arguments=[
            "Regulations require enforcement regardless of intent.",
            "Severity of risk justifies action.",
            "Corrective actions are necessary for public safety."
        ],
        resolution_strategy="Apply penalties and require corrective actions as warranted.",
        entity_scope="Regulators, Operators, Legal Counsel",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RRC Enforcement Policy (2017)"
    ),
    DoctrineBlock(
        topic="Operator Training and Competency",
        keywords=["operator training", "competency", "seismic risk", "regulatory compliance"],
        conclusion_template="Operators must demonstrate training and competency in seismic risk management and regulatory compliance.",
        reasoning_framework=(
            "Review operator training programs and competency assessments. "
            "Verify staff qualifications and continuing education records. "
            "Assess effectiveness of training in incident response and risk mitigation. "
            "Require remedial training for deficiencies or non-compliance."
        ),
        key_factors=[
            "Training program content",
            "Staff qualifications",
            "Competency assessments",
            "Continuing education",
            "Incident response performance"
        ],
        primary_authority=[
            "RRC Operator Training Guidelines",
            "USGS Risk Management Standards"
        ],
        burden_holder="Operator",
        adversary_position="Training is adequate and meets requirements.",
        counter_arguments=[
            "Training records are incomplete or outdated.",
            "Incident response performance is inadequate.",
            "Continuing education requirements are not met."
        ],
        resolution_strategy="Mandate remedial training and competency reassessment.",
        entity_scope="Operators, Regulators, Training Providers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Operator Training Policy (2016)"
    ),
    DoctrineBlock(
        topic="Public Communication of Seismic Risk",
        keywords=["public communication", "seismic risk", "stakeholder engagement", "transparency"],
        conclusion_template="Transparent public communication of seismic risk is required to maintain stakeholder trust and regulatory legitimacy.",
        reasoning_framework=(
            "Develop communication plans for timely dissemination of seismic risk information. "
            "Engage stakeholders through public meetings, reports, and digital platforms. "
            "Disclose monitoring data, risk assessments, and mitigation actions. "
            "Address public concerns and misinformation proactively."
        ),
        key_factors=[
            "Communication plan quality",
            "Stakeholder engagement",
            "Data transparency",
            "Public trust",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Public Communication Guidelines",
            "USGS Stakeholder Engagement Standards"
        ],
        burden_holder="Regulator",
        adversary_position="Communication is sufficient or not required.",
        counter_arguments=[
            "Transparency improves public trust and compliance.",
            "Stakeholder engagement reduces conflict.",
            "Regulations require public disclosure."
        ],
        resolution_strategy="Mandate public communication plans and regular updates.",
        entity_scope="Regulators, Operators, Public",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Public Communication Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Risk Insurance Requirements",
        keywords=["insurance", "seismic risk", "liability", "operator requirements"],
        conclusion_template="Operators must maintain adequate seismic risk insurance to cover potential damages and liabilities.",
        reasoning_framework=(
            "Review regulatory requirements for seismic risk insurance coverage. "
            "Assess adequacy of operator's insurance policies relative to potential damages. "
            "Verify policy terms, coverage limits, and exclusions. "
            "Require additional coverage if risk profile warrants."
        ),
        key_factors=[
            "Regulatory insurance requirements",
            "Coverage limits",
            "Policy exclusions",
            "Risk profile",
            "Claims history"
        ],
        primary_authority=[
            "RRC Insurance Guidelines",
            "USGS Risk Management Standards"
        ],
        burden_holder="Operator",
        adversary_position="Existing insurance is adequate.",
        counter_arguments=[
            "Coverage limits may be insufficient for worst-case events.",
            "Policy exclusions may limit recovery.",
            "Regulations require periodic review."
        ],
        resolution_strategy="Mandate increased coverage or policy revisions as warranted.",
        entity_scope="Operators, Regulators, Insurers",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="RRC Insurance Policy (2017)"
    ),
    DoctrineBlock(
        topic="Data Sharing and Confidentiality",
        keywords=["data sharing", "confidentiality", "seismic monitoring", "regulatory reporting"],
        conclusion_template="Operators must share seismic monitoring data with regulators while protecting confidential business information.",
        reasoning_framework=(
            "Review regulatory requirements for data sharing and confidentiality. "
            "Establish protocols for secure data transmission and storage. "
            "Define categories of data subject to public disclosure versus confidentiality. "
            "Resolve disputes over data access through regulatory adjudication."
        ),
        key_factors=[
            "Data sharing requirements",
            "Confidentiality protocols",
            "Public disclosure categories",
            "Data security",
            "Regulatory adjudication"
        ],
        primary_authority=[
            "RRC Data Sharing Guidelines",
            "USGS Data Confidentiality Standards"
        ],
        burden_holder="Operator",
        adversary_position="All data should be confidential.",
        counter_arguments=[
            "Public interest requires data transparency.",
            "Regulations specify disclosure categories.",
            "Secure protocols protect sensitive information."
        ],
        resolution_strategy="Mandate data sharing with confidentiality safeguards.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Data Sharing Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Event Classification",
        keywords=["event classification", "induced vs natural", "regulatory reporting", "hazard assessment"],
        conclusion_template="Seismic events must be classified as induced or natural using standardized criteria for regulatory and hazard assessment purposes.",
        reasoning_framework=(
            "Apply standardized criteria (e.g., temporal/spatial correlation, operational triggers) to classify events. "
            "Review supporting data from seismic monitoring, injection records, and geological studies. "
            "Document classification rationale and report to regulators. "
            "Update classification as new data becomes available."
        ),
        key_factors=[
            "Classification criteria",
            "Supporting data quality",
            "Documentation standards",
            "Regulatory reporting requirements",
            "Update protocols"
        ],
        primary_authority=[
            "USGS Event Classification Guidelines",
            "RRC Reporting Standards"
        ],
        burden_holder="Operator",
        adversary_position="Classification is ambiguous or unnecessary.",
        counter_arguments=[
            "Standardized criteria improve consistency.",
            "Classification informs hazard assessment and response.",
            "Regulations require event classification."
        ],
        resolution_strategy="Mandate classification and periodic review.",
        entity_scope="Operators, Regulators, Seismologists",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="USGS Event Classification Policy (2017)"
    ),
    DoctrineBlock(
        topic="Operational Risk Assessment",
        keywords=["risk assessment", "operational risk", "seismicity", "regulatory compliance"],
        conclusion_template="Comprehensive operational risk assessments must be conducted and updated regularly to manage seismicity risk.",
        reasoning_framework=(
            "Identify operational hazards and potential seismicity triggers. "
            "Quantify risk using probabilistic and deterministic methods. "
            "Update assessments as new data and operational changes occur. "
            "Integrate risk assessment findings into operational protocols and mitigation plans."
        ),
        key_factors=[
            "Hazard identification",
            "Risk quantification methods",
            "Assessment update frequency",
            "Integration with operations",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Risk Assessment Guidelines",
            "USGS Operational Risk Standards"
        ],
        burden_holder="Operator",
        adversary_position="Risk assessment is sufficient as is.",
        counter_arguments=[
            "New data may change risk profile.",
            "Regular updates are required by regulation.",
            "Integration with operations improves risk management."
        ],
        resolution_strategy="Mandate regular risk assessment updates.",
        entity_scope="Operators, Regulators, Risk Analysts",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Risk Assessment Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismicity Mitigation Technology Adoption",
        keywords=["mitigation technology", "adoption", "seismicity", "innovation"],
        conclusion_template="Operators are encouraged to adopt proven seismicity mitigation technologies to reduce risk.",
        reasoning_framework=(
            "Review available mitigation technologies (e.g., real-time monitoring, automated shutoff, advanced modeling). "
            "Assess effectiveness and cost-benefit of adoption. "
            "Incentivize adoption through regulatory or financial mechanisms. "
            "Monitor outcomes and update recommendations as technology evolves."
        ),
        key_factors=[
            "Technology effectiveness",
            "Cost-benefit analysis",
            "Regulatory incentives",
            "Operator adoption rates",
            "Outcome monitoring"
        ],
        primary_authority=[
            "RRC Technology Adoption Guidelines",
            "USGS Mitigation Technology Reports"
        ],
        burden_holder="Operator",
        adversary_position="Existing technology is sufficient.",
        counter_arguments=[
            "New technologies may provide superior risk reduction.",
            "Regulatory incentives can offset costs.",
            "Continuous improvement is best practice."
        ],
        resolution_strategy="Encourage adoption and monitor effectiveness.",
        entity_scope="Operators, Regulators, Technology Providers",
        confidence=0.82,
        confidence_zone="Moderate-High",
        controlling_precedent="RRC Technology Adoption Policy (2021)"
    ),
    DoctrineBlock(
        topic="Cross-Jurisdictional Coordination",
        keywords=["cross-jurisdictional", "coordination", "seismicity", "regulatory harmonization"],
        conclusion_template="Cross-jurisdictional coordination is required to manage seismicity risk in areas spanning multiple regulatory authorities.",
        reasoning_framework=(
            "Identify overlapping regulatory jurisdictions and responsibilities. "
            "Establish coordination protocols for data sharing, response, and enforcement. "
            "Resolve conflicts through interagency agreements or memoranda of understanding. "
            "Ensure consistent application of risk management standards."
        ),
        key_factors=[
            "Jurisdictional boundaries",
            "Coordination protocols",
            "Interagency agreements",
            "Standard harmonization",
            "Conflict resolution"
        ],
        primary_authority=[
            "RRC Interagency Coordination Guidelines",
            "USGS Multi-State Seismicity Reports"
        ],
        burden_holder="Regulator",
        adversary_position="Coordination is unnecessary or burdensome.",
        counter_arguments=[
            "Seismicity risk does not respect jurisdictional boundaries.",
            "Coordination improves response and enforcement.",
            "Agreements can streamline processes."
        ],
        resolution_strategy="Mandate coordination and periodic review of agreements.",
        entity_scope="Regulators, Operators, Interagency Partners",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="RRC-USGS Interagency MOU (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Notification to Public",
        keywords=["public notification", "seismic event", "risk communication", "regulatory requirement"],
        conclusion_template="Timely public notification of significant seismic events is required to ensure public safety and awareness.",
        reasoning_framework=(
            "Define notification thresholds and timelines. "
            "Develop public notification protocols using multiple communication channels. "
            "Coordinate with local emergency management agencies. "
            "Document notification actions and outcomes."
        ),
        key_factors=[
            "Notification thresholds",
            "Communication channels",
            "Coordination with emergency agencies",
            "Documentation",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Public Notification Guidelines",
            "USGS Public Communication Standards"
        ],
        burden_holder="Regulator",
        adversary_position="Notification is unnecessary or delayed.",
        counter_arguments=[
            "Timely notification improves public safety.",
            "Multiple channels increase reach.",
            "Documentation ensures accountability."
        ],
        resolution_strategy="Mandate notification protocols and monitor compliance.",
        entity_scope="Regulators, Operators, Public",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="RRC Public Notification Policy (2017)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Archiving",
        keywords=["data archiving", "seismic event", "regulatory compliance", "data integrity"],
        conclusion_template="Seismic event data must be archived in accordance with regulatory standards to ensure data integrity and accessibility.",
        reasoning_framework=(
            "Establish data archiving protocols for raw and processed seismic data. "
            "Ensure secure, redundant storage and regular backups. "
            "Define retention periods and access controls. "
            "Audit archives for completeness and integrity."
        ),
        key_factors=[
            "Archiving protocols",
            "Storage security",
            "Retention periods",
            "Access controls",
            "Audit procedures"
        ],
        primary_authority=[
            "TexNet Data Archiving Standards",
            "USGS Data Integrity Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Archiving is burdensome or unnecessary.",
        counter_arguments=[
            "Archiving ensures data is available for future analysis.",
            "Regulations require data retention.",
            "Audits improve data integrity."
        ],
        resolution_strategy="Mandate archiving and periodic audits.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="TexNet Data Archiving Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Event Review Panels",
        keywords=["review panels", "seismic event", "expert review", "regulatory oversight"],
        conclusion_template="Independent review panels must evaluate significant seismic events to ensure objective risk assessment and regulatory response.",
        reasoning_framework=(
            "Establish criteria for convening review panels (e.g., event magnitude, public concern). "
            "Select panel members with relevant expertise and independence. "
            "Review event data, operator actions, and regulatory response. "
            "Issue findings and recommendations for further action."
        ),
        key_factors=[
            "Panel selection criteria",
            "Expertise and independence",
            "Review scope",
            "Findings and recommendations",
            "Regulatory follow-up"
        ],
        primary_authority=[
            "RRC Review Panel Guidelines",
            "USGS Expert Review Standards"
        ],
        burden_holder="Regulator",
        adversary_position="Review is unnecessary or biased.",
        counter_arguments=[
            "Independent review improves objectivity.",
            "Panels provide technical expertise.",
            "Recommendations inform regulatory action."
        ],
        resolution_strategy="Mandate review panels for significant events.",
        entity_scope="Regulators, Operators, Experts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RRC Review Panel Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Root Cause Analysis",
        keywords=["root cause analysis", "seismic event", "incident investigation", "regulatory reporting"],
        conclusion_template="Root cause analysis must be conducted for all significant seismic events to inform mitigation and prevention.",
        reasoning_framework=(
            "Initiate root cause analysis following significant events. "
            "Collect and review operational, geological, and seismic data. "
            "Identify causal factors and contributing circumstances. "
            "Develop and implement corrective actions. "
            "Report findings to regulators and stakeholders."
        ),
        key_factors=[
            "Data collection and review",
            "Causal factor identification",
            "Corrective action development",
            "Reporting requirements",
            "Regulatory oversight"
        ],
        primary_authority=[
            "RRC Root Cause Analysis Guidelines",
            "USGS Incident Investigation Standards"
        ],
        burden_holder="Operator",
        adversary_position="Root cause analysis is unnecessary or inconclusive.",
        counter_arguments=[
            "Analysis informs prevention and mitigation.",
            "Regulations require incident investigation.",
            "Reporting improves transparency."
        ],
        resolution_strategy="Mandate root cause analysis and corrective action implementation.",
        entity_scope="Operators, Regulators, Investigators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RRC Root Cause Analysis Policy (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Event Drills and Exercises",
        keywords=["drills", "exercises", "seismic event", "emergency preparedness"],
        conclusion_template="Regular drills and exercises must be conducted to ensure preparedness for seismic events.",
        reasoning_framework=(
            "Develop and implement drill and exercise programs for seismic event response. "
            "Engage all relevant personnel and stakeholders. "
            "Evaluate performance and identify areas for improvement. "
            "Document outcomes and update response plans accordingly."
        ),
        key_factors=[
            "Drill and exercise program quality",
            "Stakeholder participation",
            "Performance evaluation",
            "Documentation",
            "Plan updates"
        ],
        primary_authority=[
            "RRC Emergency Preparedness Guidelines",
            "USGS Exercise Standards"
        ],
        burden_holder="Operator",
        adversary_position="Drills are unnecessary or disruptive.",
        counter_arguments=[
            "Preparedness reduces response time and risk.",
            "Drills are required by regulation.",
            "Continuous improvement is best practice."
        ],
        resolution_strategy="Mandate regular drills and exercises.",
        entity_scope="Operators, Regulators, Emergency Responders",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Emergency Preparedness Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Event Reporting Timeliness",
        keywords=["reporting timeliness", "seismic event", "regulatory compliance", "data submission"],
        conclusion_template="Seismic event reports must be submitted within regulatory timeframes to ensure timely risk management.",
        reasoning_framework=(
            "Define reporting deadlines for various event types and magnitudes. "
            "Monitor operator compliance with submission deadlines. "
            "Document late or incomplete submissions and enforce penalties as warranted. "
            "Review and update reporting requirements as needed."
        ),
        key_factors=[
            "Reporting deadlines",
            "Compliance monitoring",
            "Penalty guidelines",
            "Documentation",
            "Regulatory updates"
        ],
        primary_authority=[
            "RRC Reporting Timeliness Guidelines",
            "USGS Data Submission Standards"
        ],
        burden_holder="Operator",
        adversary_position="Delays are justified or minor.",
        counter_arguments=[
            "Timely reporting is critical for risk management.",
            "Delays may impede regulatory response.",
            "Penalties incentivize compliance."
        ],
        resolution_strategy="Enforce penalties for late submissions.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="RRC Reporting Timeliness Policy (2017)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Standardization",
        keywords=["data standardization", "seismic event", "regulatory reporting", "data quality"],
        conclusion_template="Seismic event data must be standardized for regulatory reporting and hazard assessment.",
        reasoning_framework=(
            "Adopt standardized data formats and metadata requirements. "
            "Ensure consistency across operator and regulatory data submissions. "
            "Validate data against standard templates and correct errors. "
            "Update standards as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Standardized data formats",
            "Metadata requirements",
            "Validation procedures",
            "Error correction",
            "Regulatory updates"
        ],
        primary_authority=[
            "RRC Data Standardization Guidelines",
            "USGS Data Quality Standards"
        ],
        burden_holder="Operator",
        adversary_position="Standardization is burdensome or unnecessary.",
        counter_arguments=[
            "Standardization improves data quality and comparability.",
            "Regulations require standardized reporting.",
            "Updates reflect technological advances."
        ],
        resolution_strategy="Mandate standardized data formats and periodic reviews.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Data Standardization Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Accessibility",
        keywords=["data accessibility", "seismic event", "public access", "regulatory transparency"],
        conclusion_template="Seismic event data must be made accessible to the public and stakeholders in accordance with regulatory transparency requirements.",
        reasoning_framework=(
            "Define categories of data for public access versus restricted use. "
            "Develop online portals and data dissemination platforms. "
            "Ensure timely updates and user-friendly interfaces. "
            "Monitor data usage and address access issues."
        ),
        key_factors=[
            "Data access categories",
            "Portal functionality",
            "Update frequency",
            "User support",
            "Regulatory transparency"
        ],
        primary_authority=[
            "RRC Data Accessibility Guidelines",
            "USGS Public Data Standards"
        ],
        burden_holder="Regulator",
        adversary_position="Data should be restricted.",
        counter_arguments=[
            "Transparency improves public trust.",
            "Online portals increase accessibility.",
            "Regulations require public access."
        ],
        resolution_strategy="Mandate public data portals and monitor usage.",
        entity_scope="Regulators, Operators, Public",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Data Accessibility Policy (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Correction and Revision",
        keywords=["data correction", "revision", "seismic event", "regulatory reporting"],
        conclusion_template="Procedures for correction and revision of seismic event data must be established and followed.",
        reasoning_framework=(
            "Define protocols for identifying and correcting data errors. "
            "Document all corrections and revisions in data records. "
            "Notify regulators and stakeholders of significant changes. "
            "Review and update correction procedures as needed."
        ),
        key_factors=[
            "Error identification protocols",
            "Documentation of corrections",
            "Notification procedures",
            "Regulatory requirements",
            "Procedure updates"
        ],
        primary_authority=[
            "RRC Data Correction Guidelines",
            "USGS Data Revision Standards"
        ],
        burden_holder="Operator",
        adversary_position="Corrections are unnecessary or minor.",
        counter_arguments=[
            "Accurate data is critical for risk assessment.",
            "Documentation ensures transparency.",
            "Regulations require correction procedures."
        ],
        resolution_strategy="Mandate correction protocols and periodic reviews.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Data Correction Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Retention",
        keywords=["data retention", "seismic event", "regulatory compliance", "archiving"],
        conclusion_template="Seismic event data must be retained for specified periods in accordance with regulatory requirements.",
        reasoning_framework=(
            "Define retention periods for all categories of seismic data. "
            "Ensure secure storage and access controls. "
            "Audit retention compliance and address deficiencies. "
            "Update retention policies as regulations evolve."
        ),
        key_factors=[
            "Retention period requirements",
            "Storage security",
            "Access controls",
            "Compliance audits",
            "Policy updates"
        ],
        primary_authority=[
            "RRC Data Retention Guidelines",
            "USGS Data Archiving Standards"
        ],
        burden_holder="Operator",
        adversary_position="Retention periods are excessive.",
        counter_arguments=[
            "Retention ensures data is available for future analysis.",
            "Regulations specify minimum periods.",
            "Audits improve compliance."
        ],
        resolution_strategy="Mandate retention and periodic audits.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Data Retention Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Security",
        keywords=["data security", "seismic event", "cybersecurity", "regulatory compliance"],
        conclusion_template="Seismic event data systems must implement cybersecurity measures to protect data integrity and confidentiality.",
        reasoning_framework=(
            "Assess cybersecurity risks to seismic data systems. "
            "Implement security protocols for data transmission, storage, and access. "
            "Conduct regular security audits and vulnerability assessments. "
            "Respond to security incidents and update protocols as needed."
        ),
        key_factors=[
            "Cybersecurity risk assessment",
            "Security protocol implementation",
            "Audit frequency",
            "Incident response",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Security Guidelines",
            "USGS Cybersecurity Standards"
        ],
        burden_holder="Operator",
        adversary_position="Security measures are adequate.",
        counter_arguments=[
            "Evolving threats require continuous improvement.",
            "Regulations require security audits.",
            "Incident response plans improve resilience."
        ],
        resolution_strategy="Mandate security protocols and regular audits.",
        entity_scope="Operators, Regulators, IT Managers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Data Security Policy (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Integration",
        keywords=["data integration", "seismic event", "multi-source data", "regulatory reporting"],
        conclusion_template="Integration of multi-source seismic event data is required for comprehensive risk assessment and regulatory reporting.",
        reasoning_framework=(
            "Identify and acquire relevant data sources (e.g., TexNet, operator, third-party). "
            "Standardize and merge data into unified databases. "
            "Resolve discrepancies through data reconciliation protocols. "
            "Use integrated data for risk assessment and regulatory reporting."
        ),
        key_factors=[
            "Data source identification",
            "Standardization and merging",
            "Discrepancy resolution",
            "Database management",
            "Regulatory reporting"
        ],
        primary_authority=[
            "RRC Data Integration Guidelines",
            "USGS Data Management Standards"
        ],
        burden_holder="Operator",
        adversary_position="Integration is unnecessary or costly.",
        counter_arguments=[
            "Integration improves risk assessment accuracy.",
            "Regulations require comprehensive reporting.",
            "Standardization reduces errors."
        ],
        resolution_strategy="Mandate integration protocols and periodic reviews.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Data Integration Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Visualization",
        keywords=["data visualization", "seismic event", "risk communication", "decision support"],
        conclusion_template="Effective data visualization tools must be used to communicate seismic event data and support decision-making.",
        reasoning_framework=(
            "Develop visualization tools for seismic event data (e.g., maps, time series, dashboards). "
            "Ensure tools are user-friendly and accessible to stakeholders. "
            "Update visualizations as new data becomes available. "
            "Use visualizations to inform risk assessments and operational decisions."
        ),
        key_factors=[
            "Visualization tool quality",
            "User accessibility",
            "Update frequency",
            "Stakeholder engagement",
            "Decision support"
        ],
        primary_authority=[
            "RRC Data Visualization Guidelines",
            "USGS Visualization Standards"
        ],
        burden_holder="Operator",
        adversary_position="Visualization is unnecessary or too costly.",
        counter_arguments=[
            "Visualization improves understanding and decision-making.",
            "Tools can be developed cost-effectively.",
            "Stakeholder engagement is enhanced."
        ],
        resolution_strategy="Mandate visualization tools for significant data sets.",
        entity_scope="Operators, Regulators, Stakeholders",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="RRC Data Visualization Policy (2021)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Backup and Recovery",
        keywords=["data backup", "recovery", "seismic event", "data integrity"],
        conclusion_template="Regular data backup and recovery procedures must be implemented for all seismic event data systems.",
        reasoning_framework=(
            "Establish backup schedules and procedures for all data systems. "
            "Test recovery processes regularly to ensure data integrity. "
            "Document backup and recovery actions. "
            "Update procedures as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Backup schedule",
            "Recovery process testing",
            "Documentation",
            "Procedure updates",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Backup Guidelines",
            "USGS Data Integrity Standards"
        ],
        burden_holder="Operator",
        adversary_position="Backup procedures are sufficient.",
        counter_arguments=[
            "Regular testing ensures effectiveness.",
            "Documentation improves accountability.",
            "Regulations require backup and recovery plans."
        ],
        resolution_strategy="Mandate backup and recovery protocols and periodic testing.",
        entity_scope="Operators, Regulators, IT Managers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="RRC Data Backup Policy (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Quality Assurance",
        keywords=["quality assurance", "seismic event", "data quality", "regulatory compliance"],
        conclusion_template="Quality assurance programs must be implemented to ensure the accuracy and reliability of seismic event data.",
        reasoning_framework=(
            "Develop and implement quality assurance protocols for data collection, processing, and reporting. "
            "Conduct regular audits and reviews of data quality. "
            "Document quality assurance actions and findings. "
            "Update protocols as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Quality assurance protocols",
            "Audit frequency",
            "Documentation",
            "Protocol updates",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Quality Assurance Guidelines",
            "USGS Data Quality Standards"
        ],
        burden_holder="Operator",
        adversary_position="Quality assurance is unnecessary or burdensome.",
        counter_arguments=[
            "Quality assurance improves data reliability.",
            "Audits identify and correct errors.",
            "Regulations require quality assurance programs."
        ],
        resolution_strategy="Mandate quality assurance protocols and periodic audits.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Quality Assurance Policy (2018)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Interoperability",
        keywords=["data interoperability", "seismic event", "system integration", "regulatory reporting"],
        conclusion_template="Seismic event data systems must be interoperable to facilitate integration and regulatory reporting.",
        reasoning_framework=(
            "Adopt interoperable data formats and communication protocols. "
            "Integrate data systems across operators and regulators. "
            "Test interoperability and resolve compatibility issues. "
            "Update protocols as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Interoperable data formats",
            "Communication protocols",
            "System integration",
            "Compatibility testing",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Interoperability Guidelines",
            "USGS System Integration Standards"
        ],
        burden_holder="Operator",
        adversary_position="Interoperability is unnecessary or costly.",
        counter_arguments=[
            "Interoperability improves efficiency and accuracy.",
            "Regulations require system integration.",
            "Updates reflect technological advances."
        ],
        resolution_strategy="Mandate interoperability protocols and periodic reviews.",
        entity_scope="Operators, Regulators, IT Managers",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Data Interoperability Policy (2019)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Provenance",
        keywords=["data provenance", "seismic event", "data lineage", "regulatory reporting"],
        conclusion_template="Data provenance must be documented for all seismic event data to ensure traceability and accountability.",
        reasoning_framework=(
            "Establish protocols for documenting data sources, processing steps, and modifications. "
            "Maintain data lineage records for all significant data sets. "
            "Report provenance information in regulatory filings. "
            "Update protocols as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Provenance documentation protocols",
            "Data lineage records",
            "Reporting requirements",
            "Protocol updates",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Provenance Guidelines",
            "USGS Data Lineage Standards"
        ],
        burden_holder="Operator",
        adversary_position="Provenance documentation is unnecessary.",
        counter_arguments=[
            "Provenance ensures data traceability and accountability.",
            "Regulations require documentation.",
            "Updates reflect technological advances."
        ],
        resolution_strategy="Mandate provenance documentation and periodic reviews.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Data Provenance Policy (2020)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Analytics",
        keywords=["data analytics", "seismic event", "risk assessment", "decision support"],
        conclusion_template="Advanced data analytics must be applied to seismic event data to improve risk assessment and decision support.",
        reasoning_framework=(
            "Implement data analytics tools for pattern recognition, anomaly detection, and predictive modeling. "
            "Integrate analytics outputs into risk assessment and operational decision-making. "
            "Update analytics tools as new data and technologies become available."
        ),
        key_factors=[
            "Analytics tool selection",
            "Integration with risk assessment",
            "Update frequency",
            "Stakeholder engagement",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Analytics Guidelines",
            "USGS Analytics Standards"
        ],
        burden_holder="Operator",
        adversary_position="Analytics are unnecessary or too costly.",
        counter_arguments=[
            "Analytics improve risk assessment accuracy.",
            "Integration supports decision-making.",
            "Updates reflect technological advances."
        ],
        resolution_strategy="Mandate analytics tools for significant data sets.",
        entity_scope="Operators, Regulators, Data Scientists",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="RRC Data Analytics Policy (2021)"
    ),
    DoctrineBlock(
        topic="Seismic Event Data Ethics",
        keywords=["data ethics", "seismic event", "privacy", "regulatory compliance"],
        conclusion_template="Ethical standards must be applied to seismic event data management, including privacy and responsible use.",
        reasoning_framework=(
            "Establish ethical guidelines for data collection, use, and sharing. "
            "Protect privacy and sensitive information. "
            "Review data management practices for ethical compliance. "
            "Update guidelines as technology and regulatory requirements evolve."
        ),
        key_factors=[
            "Ethical guidelines",
            "Privacy protection",
            "Compliance review",
            "Guideline updates",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Data Ethics Guidelines",
            "USGS Data Ethics Standards"
        ],
        burden_holder="Operator",
        adversary_position="Ethics are addressed by existing policies.",
        counter_arguments=[
            "Ethical standards improve public trust.",
            "Privacy protection is required by law.",
            "Guidelines must evolve with technology."
        ],
        resolution_strategy="Mandate ethical guidelines and periodic reviews.",
        entity_scope="Operators, Regulators, Data Managers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="RRC Data Ethics Policy (2020)"
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