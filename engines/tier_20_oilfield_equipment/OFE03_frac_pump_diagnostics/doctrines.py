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
        topic="Quintuplex Pump Plunger Wear Analysis",
        keywords=["plunger", "wear", "quintuplex", "pump", "diagnostics", "failure", "OFE03"],
        conclusion_template="Plunger wear is primarily attributed to abrasive proppant flow and inadequate lubrication, requiring scheduled inspection every 100 operational hours or upon detection of pressure irregularities.",
        reasoning_framework="""
1. Review operational logs for pressure fluctuations and abnormal pump noise.
2. Correlate plunger material grade with recorded fluid composition and proppant concentration.
3. Examine maintenance records for lubrication intervals and previous wear incidents.
4. Inspect plungers for scoring, pitting, or dimensional loss using NDT (ultrasonic or dye penetrant).
5. Compare observed wear patterns with manufacturer tolerances.
6. Assess correlation between high-rate jobs and accelerated wear.
7. Evaluate the effectiveness of implemented lubrication protocols.
8. Consider alternative plunger coatings or materials if wear exceeds expected rates.
9. Document findings and recommend replacement or reconditioning.
10. Update maintenance schedule and operator training accordingly.
""",
        key_factors=[
            "Proppant concentration",
            "Lubrication frequency and quality",
            "Plunger material and hardness",
            "Pump operating pressure",
            "Maintenance interval adherence",
            "Historical failure rates"
        ],
        primary_authority=[
            "API RP 11P",
            "OEM Maintenance Manual (Weir SPM, Gardner Denver)",
            "SPE 189-2021"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Plunger wear is within expected limits and does not require immediate action.",
        counter_arguments=[
            "Recent data shows accelerated wear beyond OEM projections.",
            "Lubrication logs indicate possible missed intervals.",
            "NDT reveals microcracks not previously documented."
        ],
        resolution_strategy="Conduct third-party NDT assessment and compare with OEM tolerances; escalate to engineering review if wear exceeds 10% of original diameter.",
        entity_scope="OFE03 frac pump fleet",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 6.2"
    ),
    DoctrineBlock(
        topic="Fluid End Crack Detection and NDT",
        keywords=["fluid end", "crack", "detection", "NDT", "ultrasonic", "dye penetrant", "OFE03"],
        conclusion_template="Routine NDT of fluid ends is required every 200 operational hours or after any overpressure event to detect incipient cracks and prevent catastrophic failure.",
        reasoning_framework="""
1. Review pressure logs for overpressure events or pressure spikes.
2. Schedule NDT (ultrasonic, magnetic particle, and dye penetrant) at recommended intervals.
3. Inspect high-stress regions: discharge bores, valve seats, and thread roots.
4. Document any crack indications, noting length, orientation, and location.
5. Compare findings to OEM and API allowable defect sizes.
6. Assess correlation between crack initiation and operational parameters (e.g., pressure cycling, temperature).
7. Evaluate previous repair history and metallurgical reports.
8. Determine if cracks are propagating or stable.
9. Decide on immediate fluid end replacement, repair, or continued operation with increased monitoring.
10. Update risk register and communicate findings to operations.
""",
        key_factors=[
            "Frequency of overpressure events",
            "NDT interval compliance",
            "Crack size and location",
            "Material heat treatment records",
            "Repair history"
        ],
        primary_authority=[
            "API 6A",
            "OEM Fluid End Inspection Guidelines",
            "SPE 204-2019"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Cracks detected are superficial and do not compromise integrity.",
        counter_arguments=[
            "Crack propagation rates are unpredictable under cyclic loading.",
            "API 6A requires removal at specific defect sizes.",
            "Previous failures have resulted from similar indications."
        ],
        resolution_strategy="Remove fluid end from service if cracks exceed 2mm in depth or are located in high-stress regions; confirm with third-party NDT.",
        entity_scope="OFE03 fluid ends",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 6A Section 10.3"
    ),
    DoctrineBlock(
        topic="Power End Bearing Failure Analysis",
        keywords=["power end", "bearing", "failure", "analysis", "vibration", "OFE03"],
        conclusion_template="Bearing failures are most often caused by lubrication breakdown, contamination, or misalignment; root cause analysis must precede any replacement.",
        reasoning_framework="""
1. Collect vibration and temperature data from power end sensors.
2. Review lubrication records for oil type, change intervals, and contamination reports.
3. Disassemble failed bearing and inspect for pitting, scoring, or discoloration.
4. Analyze oil samples for metal content and viscosity.
5. Check for shaft misalignment using dial indicators or laser alignment tools.
6. Compare failure mode with historical data and OEM failure analysis charts.
7. Identify any operational anomalies (e.g., overloading, high ambient temperature).
8. Document root cause and corrective actions.
9. Update maintenance procedures and training as needed.
10. Monitor replacement bearing for early warning signs.
""",
        key_factors=[
            "Lubrication quality and interval",
            "Vibration and temperature trends",
            "Bearing alignment",
            "Contamination levels",
            "Load history"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "ISO 15243:2017",
            "SPE 234-2020"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Bearing failure was a random event and not indicative of systemic issues.",
        counter_arguments=[
            "Contamination levels exceed ISO 4406 recommendations.",
            "Misalignment detected during post-failure inspection.",
            "Vibration data shows progressive deterioration."
        ],
        resolution_strategy="Implement enhanced oil filtration and alignment checks; schedule follow-up vibration analysis.",
        entity_scope="OFE03 power ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017 Section 4"
    ),
    DoctrineBlock(
        topic="Discharge Valve Inspection and Failure Modes",
        keywords=["discharge valve", "inspection", "failure", "seat", "spring", "OFE03"],
        conclusion_template="Discharge valve failures are primarily due to seat erosion, spring fatigue, or improper installation; regular inspection and component replacement are mandated.",
        reasoning_framework="""
1. Review operational hours since last valve inspection.
2. Disassemble discharge valve and inspect seat, spring, and poppet for wear or deformation.
3. Measure seat erosion using calibrated gauges.
4. Check spring for loss of free length and surface cracks.
5. Compare findings to OEM replacement criteria.
6. Analyze failure trends across fleet for systemic issues.
7. Document inspection results and replace components as needed.
8. Update inspection frequency based on observed wear rates.
9. Train personnel on proper valve installation techniques.
10. Maintain records for regulatory and warranty compliance.
""",
        key_factors=[
            "Seat erosion rate",
            "Spring fatigue life",
            "Installation practices",
            "Inspection interval",
            "Fleet-wide failure data"
        ],
        primary_authority=[
            "OEM Valve Manual",
            "API 7K",
            "SPE 145-2018"
        ],
        burden_holder="Valve Technician",
        adversary_position="Valve failures are within normal operational limits and do not require increased inspection frequency.",
        counter_arguments=[
            "Recent failures exceed historical averages.",
            "OEM recommends shorter intervals under high-rate conditions.",
            "Improper installation detected in multiple cases."
        ],
        resolution_strategy="Increase inspection frequency and implement installation training; replace all suspect components.",
        entity_scope="OFE03 discharge valves",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 7K Section 8.5"
    ),
    DoctrineBlock(
        topic="Treating Iron Integrity - Hammer Unions and Swivels",
        keywords=["treating iron", "hammer union", "swivel", "integrity", "inspection", "OFE03"],
        conclusion_template="All treating iron, including hammer unions and swivels, must be inspected for washout, thread damage, and material loss every 50 pumping hours or after any suspected overpressure event.",
        reasoning_framework="""
1. Review treating iron service logs for operational hours and pressure events.
2. Visually inspect hammer unions and swivels for washout, cracks, and thread deformation.
3. Measure wall thickness using ultrasonic gauges.
4. Compare measurements to OEM minimum wall thickness.
5. Check for proper make-up torque and alignment.
6. Document any findings and segregate components failing inspection.
7. Replace or repair damaged components per OEM and API guidelines.
8. Record all inspections for traceability.
9. Train personnel on proper handling and installation.
10. Update integrity management plan as needed.
""",
        key_factors=[
            "Wall thickness",
            "Thread condition",
            "Washout evidence",
            "Inspection interval",
            "Overpressure history"
        ],
        primary_authority=[
            "API 6A",
            "OEM Treating Iron Manual",
            "SPE 190-2017"
        ],
        burden_holder="Field Supervisor",
        adversary_position="Treating iron is robust and does not require such frequent inspection.",
        counter_arguments=[
            "API 6A mandates minimum wall thickness.",
            "Recent failures have occurred due to undetected washout.",
            "OEM recommends post-overpressure inspection."
        ],
        resolution_strategy="Enforce inspection intervals and replace all components below minimum wall thickness.",
        entity_scope="OFE03 treating iron",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 6A Section 9.2"
    ),
    DoctrineBlock(
        topic="Pump Rate Optimization and Efficiency",
        keywords=["pump rate", "optimization", "efficiency", "OFE03", "SCADA", "real-time"],
        conclusion_template="Pump rates should be dynamically optimized using real-time SCADA data to maximize efficiency while preventing cavitation and excessive wear.",
        reasoning_framework="""
1. Analyze SCADA data for pressure, flow rate, and pump efficiency trends.
2. Identify periods of suboptimal efficiency or cavitation risk.
3. Adjust pump rate setpoints to maintain optimal NPSH and minimize energy consumption.
4. Correlate rate changes with wear rates and maintenance incidents.
5. Implement closed-loop control algorithms for real-time optimization.
6. Review operator interventions and override frequency.
7. Document efficiency gains and reduced failure rates.
8. Update SOPs to reflect optimized rate protocols.
9. Train operators on new optimization procedures.
10. Continuously monitor and refine optimization algorithms.
""",
        key_factors=[
            "SCADA data accuracy",
            "NPSH margin",
            "Operator intervention frequency",
            "Wear and failure rates",
            "Energy consumption"
        ],
        primary_authority=[
            "OEM Control System Manual",
            "API RP 11P",
            "SPE 201-2022"
        ],
        burden_holder="Operations Manager",
        adversary_position="Manual pump rate control is sufficient and less complex.",
        counter_arguments=[
            "Manual control leads to increased wear and energy use.",
            "Real-time optimization reduces failures and costs.",
            "Industry trend favors automation."
        ],
        resolution_strategy="Pilot closed-loop optimization on select units and expand based on results.",
        entity_scope="OFE03 frac pump operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 201-2022"
    ),
    DoctrineBlock(
        topic="Suction Valve Inspection and Cavitation Damage",
        keywords=["suction valve", "inspection", "cavitation", "damage", "OFE03"],
        conclusion_template="Suction valves must be inspected for cavitation pitting and seat erosion every 75 operational hours, with immediate replacement if damage is detected.",
        reasoning_framework="""
1. Monitor suction pressure and flow for signs of cavitation (e.g., noise, vibration).
2. Disassemble suction valve and inspect for pitting, erosion, or cracking.
3. Measure seat and poppet dimensions against OEM specs.
4. Document any cavitation damage and correlate with operational data.
5. Replace damaged components and record findings.
6. Analyze root cause (e.g., low NPSH, high pump rate).
7. Adjust operational parameters to prevent recurrence.
8. Update inspection intervals based on observed damage rates.
9. Train personnel on cavitation detection and prevention.
10. Maintain records for warranty and regulatory compliance.
""",
        key_factors=[
            "Cavitation indicators",
            "Seat and poppet condition",
            "Inspection interval",
            "NPSH margin",
            "Root cause analysis"
        ],
        primary_authority=[
            "API 7K",
            "OEM Valve Manual",
            "SPE 155-2020"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Cavitation damage is rare and does not justify frequent inspection.",
        counter_arguments=[
            "Recent inspections show increased cavitation incidents.",
            "Low NPSH conditions are common in field operations.",
            "OEM recommends proactive inspection."
        ],
        resolution_strategy="Increase inspection frequency and adjust pump rates to maintain NPSH.",
        entity_scope="OFE03 suction valves",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API 7K Section 8.4"
    ),
    DoctrineBlock(
        topic="Cold Weather Pump Operations and Freeze Protection",
        keywords=["cold weather", "freeze protection", "pump", "operations", "OFE03"],
        conclusion_template="Freeze protection measures, including heat tracing and insulation, are mandatory for all OFE03 pumps operating below 0°C to prevent catastrophic damage.",
        reasoning_framework="""
1. Identify all pumps operating in sub-zero environments.
2. Review existing freeze protection measures (heat tracing, insulation, glycol systems).
3. Inspect for evidence of previous freeze damage (cracked housings, burst lines).
4. Test functionality of heat tracing and temperature sensors.
5. Document compliance with OEM and API recommendations.
6. Train operators on freeze protection protocols.
7. Schedule pre-winter inspections and system tests.
8. Record all incidents of freeze damage and root cause analysis.
9. Update procedures based on incident findings.
10. Communicate requirements to all field personnel.
""",
        key_factors=[
            "Ambient temperature",
            "Freeze protection system integrity",
            "Operator training",
            "Incident history",
            "Inspection frequency"
        ],
        primary_authority=[
            "OEM Freeze Protection Bulletin",
            "API RP 14J",
            "SPE 178-2019"
        ],
        burden_holder="Field Operations Supervisor",
        adversary_position="Freeze protection is unnecessary due to intermittent operation.",
        counter_arguments=[
            "Freeze events can occur during downtime.",
            "Repair costs far exceed prevention costs.",
            "API and OEM require freeze protection."
        ],
        resolution_strategy="Install and verify freeze protection on all units; enforce compliance audits.",
        entity_scope="OFE03 frac pump fleet",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API RP 14J Section 7.2"
    ),
    DoctrineBlock(
        topic="Proppant Erosion and Wear Mitigation",
        keywords=["proppant", "erosion", "wear", "mitigation", "OFE03", "fluid end"],
        conclusion_template="Erosion-resistant materials and flow path optimization are required to mitigate proppant-induced wear in OFE03 fluid ends.",
        reasoning_framework="""
1. Analyze proppant type, size, and concentration in operational fluids.
2. Review historical wear rates and failure incidents.
3. Evaluate current fluid end material and coatings.
4. Assess flow path geometry for high-velocity regions.
5. Implement erosion-resistant inserts or coatings as needed.
6. Monitor wear rates post-implementation.
7. Adjust proppant loading protocols to reduce peak concentrations.
8. Train personnel on erosion mitigation techniques.
9. Update material selection criteria for future purchases.
10. Document all mitigation measures and outcomes.
""",
        key_factors=[
            "Proppant concentration and type",
            "Material selection",
            "Flow path geometry",
            "Coating effectiveness",
            "Wear monitoring"
        ],
        primary_authority=[
            "SPE 189-2021",
            "OEM Material Specification",
            "API 6A"
        ],
        burden_holder="Engineering Manager",
        adversary_position="Current materials are sufficient and do not require upgrades.",
        counter_arguments=[
            "Wear rates exceed OEM projections.",
            "Erosion-resistant materials are industry standard.",
            "Upgrades reduce long-term costs."
        ],
        resolution_strategy="Pilot erosion-resistant upgrades and monitor results for fleet-wide adoption.",
        entity_scope="OFE03 fluid ends",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 189-2021"
    ),
    DoctrineBlock(
        topic="Chemical Compatibility and Fluid End Corrosion",
        keywords=["chemical compatibility", "corrosion", "fluid end", "OFE03", "acid", "brine"],
        conclusion_template="All fluids must be screened for chemical compatibility with fluid end metallurgy; incompatible fluids require mitigation or material upgrades.",
        reasoning_framework="""
1. Review job design for fluid chemistry (acid, brine, biocide, etc.).
2. Cross-reference fluid composition with fluid end material compatibility charts.
3. Identify any corrosive agents exceeding OEM or API limits.
4. Recommend inhibitors or alternative materials as needed.
5. Monitor corrosion rates via coupon testing or NDT.
6. Document all incidents of corrosion or material degradation.
7. Update fluid approval protocols.
8. Train personnel on chemical compatibility procedures.
9. Communicate findings to engineering and procurement.
10. Implement corrective actions for any corrosion incidents.
""",
        key_factors=[
            "Fluid chemistry",
            "Material compatibility",
            "Corrosion monitoring",
            "Inhibitor effectiveness",
            "Incident documentation"
        ],
        primary_authority=[
            "API 6A",
            "OEM Material Compatibility Chart",
            "SPE 210-2021"
        ],
        burden_holder="Frac Engineer",
        adversary_position="Current fluids are compatible with all OFE03 fluid ends.",
        counter_arguments=[
            "Recent corrosion incidents linked to unapproved fluids.",
            "Material upgrades prevent future failures.",
            "Inhibitor use is inconsistent."
        ],
        resolution_strategy="Implement mandatory fluid screening and upgrade materials as required.",
        entity_scope="OFE03 fluid ends",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API 6A Section 5.3"
    ),
    DoctrineBlock(
        topic="Pressure Relief Valve Sizing and Testing",
        keywords=["pressure relief valve", "sizing", "testing", "OFE03", "safety"],
        conclusion_template="All pressure relief valves must be sized per API 520 and tested every 6 months to ensure compliance and operational safety.",
        reasoning_framework="""
1. Calculate required relief capacity based on maximum allowable working pressure (MAWP) and system volume.
2. Select relief valve per API 520 sizing charts.
3. Install valve with proper orientation and support.
4. Test relief valve set pressure and reseat performance every 6 months.
5. Document all tests and calibrations.
6. Replace or recalibrate valves failing test criteria.
7. Maintain records for regulatory compliance.
8. Train personnel on relief valve operation and maintenance.
9. Review incident history for relief valve failures.
10. Update sizing and testing protocols as needed.
""",
        key_factors=[
            "MAWP",
            "System volume",
            "Test interval",
            "Calibration records",
            "Incident history"
        ],
        primary_authority=[
            "API 520",
            "OEM Relief Valve Manual",
            "ASME Section VIII"
        ],
        burden_holder="Safety Officer",
        adversary_position="Annual testing is sufficient and less disruptive.",
        counter_arguments=[
            "Semi-annual testing is industry standard.",
            "API 520 mandates test frequency.",
            "Recent failures linked to infrequent testing."
        ],
        resolution_strategy="Enforce 6-month testing and maintain audit trail.",
        entity_scope="OFE03 pressure relief valves",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 520 Section 7"
    ),
    DoctrineBlock(
        topic="Real-Time Pump Monitoring and SCADA Integration",
        keywords=["real-time", "monitoring", "SCADA", "integration", "OFE03", "diagnostics"],
        conclusion_template="All OFE03 pumps must be integrated with SCADA for real-time monitoring of pressure, flow, and vibration to enable predictive diagnostics.",
        reasoning_framework="""
1. Inventory all OFE03 pumps for SCADA connectivity.
2. Install or upgrade sensors for pressure, flow, and vibration.
3. Integrate sensor data into SCADA system with real-time alerts.
4. Develop diagnostic algorithms for anomaly detection.
5. Train operators and engineers on SCADA interface.
6. Document all integration steps and test results.
7. Monitor system performance and adjust thresholds as needed.
8. Review incident history for missed diagnostics.
9. Update SOPs to include SCADA-based monitoring.
10. Expand integration to all fleet units.
""",
        key_factors=[
            "Sensor coverage",
            "SCADA system reliability",
            "Operator training",
            "Diagnostic algorithm effectiveness",
            "Incident response time"
        ],
        primary_authority=[
            "OEM SCADA Integration Guide",
            "API RP 11P",
            "SPE 230-2022"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Manual monitoring is sufficient for current operations.",
        counter_arguments=[
            "Real-time monitoring enables early failure detection.",
            "Manual monitoring is prone to human error.",
            "SCADA integration is industry standard."
        ],
        resolution_strategy="Implement SCADA integration on all units and monitor outcomes.",
        entity_scope="OFE03 frac pump fleet",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 230-2022"
    ),
    DoctrineBlock(
        topic="Pump Fleet Management and Deployment Optimization",
        keywords=["fleet management", "deployment", "optimization", "OFE03", "utilization"],
        conclusion_template="Pump fleet deployment must be optimized based on utilization rates, maintenance history, and job requirements to maximize asset life and minimize downtime.",
        reasoning_framework="""
1. Analyze fleet utilization data and maintenance records.
2. Identify underutilized or high-failure units.
3. Match pump capabilities to job requirements.
4. Rotate units to balance wear and maximize asset life.
5. Schedule preventive maintenance based on usage, not just time.
6. Monitor downtime and failure rates.
7. Update deployment strategy quarterly.
8. Train dispatchers and supervisors on optimization protocols.
9. Document all deployment decisions and outcomes.
10. Review and refine strategy based on performance metrics.
""",
        key_factors=[
            "Utilization rates",
            "Maintenance history",
            "Job requirements",
            "Downtime statistics",
            "Asset life"
        ],
        primary_authority=[
            "OEM Fleet Management Guide",
            "API RP 11P",
            "SPE 240-2021"
        ],
        burden_holder="Fleet Manager",
        adversary_position="Current deployment practices are sufficient.",
        counter_arguments=[
            "Optimized deployment reduces downtime and costs.",
            "Data-driven decisions improve asset life.",
            "Industry trend favors optimization."
        ],
        resolution_strategy="Implement data-driven deployment and monitor KPIs.",
        entity_scope="OFE03 frac pump fleet",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 240-2021"
    ),
    DoctrineBlock(
        topic="Pump Packing Adjustment and Leakage Control",
        keywords=["packing", "adjustment", "leakage", "OFE03", "maintenance"],
        conclusion_template="Pump packing must be adjusted to minimize leakage while avoiding excessive friction and wear, with daily checks during operation.",
        reasoning_framework="""
1. Monitor leakage rates at packing glands during operation.
2. Adjust packing bolts incrementally to reduce leakage.
3. Avoid over-tightening to prevent excessive friction and heat.
4. Inspect packing for wear or extrusion during maintenance.
5. Replace packing if leakage cannot be controlled.
6. Document all adjustments and replacements.
7. Train operators on proper adjustment techniques.
8. Review packing material compatibility with pumped fluids.
9. Update SOPs to reflect best practices.
10. Track packing life and failure trends.
""",
        key_factors=[
            "Leakage rate",
            "Packing adjustment technique",
            "Material compatibility",
            "Operator training",
            "Packing life"
        ],
        primary_authority=[
            "OEM Packing Manual",
            "API 7K",
            "SPE 250-2022"
        ],
        burden_holder="Pump Operator",
        adversary_position="Leakage is unavoidable and does not require frequent adjustment.",
        counter_arguments=[
            "Proper adjustment minimizes leakage and extends packing life.",
            "Excessive leakage leads to environmental and safety issues.",
            "OEM recommends daily checks."
        ],
        resolution_strategy="Enforce daily checks and adjustment logs.",
        entity_scope="OFE03 frac pumps",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 7K Section 8.6"
    ),
    DoctrineBlock(
        topic="Pump Lubrication System Inspection",
        keywords=["lubrication", "system", "inspection", "OFE03", "oil", "maintenance"],
        conclusion_template="Lubrication systems must be inspected weekly for oil level, contamination, and delivery to all critical components.",
        reasoning_framework="""
1. Check oil level in all lubrication reservoirs.
2. Inspect for signs of contamination (water, metal, debris).
3. Test oil viscosity and additive levels.
4. Verify delivery to all bearings and gears.
5. Replace oil and filters as needed.
6. Document all inspections and corrective actions.
7. Train personnel on lubrication system maintenance.
8. Review failure history for lubrication-related incidents.
9. Update inspection protocols based on findings.
10. Maintain records for regulatory compliance.
""",
        key_factors=[
            "Oil level",
            "Contamination",
            "Delivery verification",
            "Inspection interval",
            "Failure history"
        ],
        primary_authority=[
            "OEM Lubrication Manual",
            "API RP 11P",
            "SPE 260-2020"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Monthly inspection is sufficient.",
        counter_arguments=[
            "Weekly inspection prevents failures.",
            "Contamination can occur rapidly.",
            "OEM recommends frequent checks."
        ],
        resolution_strategy="Enforce weekly inspections and maintain logs.",
        entity_scope="OFE03 frac pumps",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 8"
    ),
    DoctrineBlock(
        topic="Pump Foundation and Alignment Verification",
        keywords=["foundation", "alignment", "verification", "OFE03", "installation"],
        conclusion_template="Pump foundations and alignment must be verified at installation and annually to prevent vibration-induced failures.",
        reasoning_framework="""
1. Inspect foundation for cracks, settling, or loose anchors.
2. Use laser or dial indicator tools to verify shaft alignment.
3. Document all measurements and compare to OEM tolerances.
4. Correct any misalignment or foundation issues immediately.
5. Schedule annual re-verification.
6. Train installation crews on alignment procedures.
7. Review vibration data for signs of misalignment.
8. Update installation SOPs as needed.
9. Record all verification activities.
10. Analyze failure history for alignment-related incidents.
""",
        key_factors=[
            "Foundation integrity",
            "Alignment accuracy",
            "Verification interval",
            "Installation practices",
            "Vibration data"
        ],
        primary_authority=[
            "OEM Installation Manual",
            "API RP 686",
            "SPE 270-2021"
        ],
        burden_holder="Installation Supervisor",
        adversary_position="Alignment verification is unnecessary after initial installation.",
        counter_arguments=[
            "Settling and vibration can cause misalignment over time.",
            "Annual checks prevent failures.",
            "API RP 686 recommends periodic verification."
        ],
        resolution_strategy="Implement annual alignment checks and foundation inspections.",
        entity_scope="OFE03 frac pump installations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 686 Section 5"
    ),
    DoctrineBlock(
        topic="Pump Start-Up and Shut-Down Procedures",
        keywords=["start-up", "shut-down", "procedures", "OFE03", "operation"],
        conclusion_template="Standardized start-up and shut-down procedures must be followed to prevent water hammer, pressure surges, and component damage.",
        reasoning_framework="""
1. Review and standardize start-up and shut-down checklists.
2. Train operators on correct sequencing of valve and pump operations.
3. Monitor pressure and flow during transitions.
4. Document any incidents of water hammer or surges.
5. Update procedures based on incident analysis.
6. Implement interlocks or automation where possible.
7. Review OEM and API recommendations.
8. Audit compliance quarterly.
9. Record all deviations and corrective actions.
10. Communicate updates to all operators.
""",
        key_factors=[
            "Procedure compliance",
            "Operator training",
            "Incident history",
            "Automation/interlocks",
            "Checklist accuracy"
        ],
        primary_authority=[
            "OEM Operation Manual",
            "API RP 14C",
            "SPE 280-2020"
        ],
        burden_holder="Operations Supervisor",
        adversary_position="Operators can rely on experience rather than standardized procedures.",
        counter_arguments=[
            "Standardization reduces incidents.",
            "Checklists ensure consistency.",
            "API and OEM require documented procedures."
        ],
        resolution_strategy="Enforce procedure use and audit compliance.",
        entity_scope="OFE03 frac pump operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 14C Section 6"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Bolt Torque Verification",
        keywords=["fluid end", "bolt", "torque", "verification", "OFE03", "maintenance"],
        conclusion_template="Fluid end bolts must be torqued to OEM specifications and verified after any maintenance to prevent leaks and failures.",
        reasoning_framework="""
1. Use calibrated torque wrenches for all fluid end bolt tightening.
2. Verify torque values post-maintenance.
3. Document all torque readings.
4. Inspect for signs of bolt stretch or thread damage.
5. Replace bolts not meeting OEM criteria.
6. Train personnel on proper torque procedures.
7. Review failure history for bolt-related incidents.
8. Update maintenance SOPs as needed.
9. Audit compliance regularly.
10. Maintain records for warranty and regulatory purposes.
""",
        key_factors=[
            "Torque accuracy",
            "Bolt condition",
            "Maintenance compliance",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 6A",
            "SPE 290-2021"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Hand tightening is sufficient for experienced personnel.",
        counter_arguments=[
            "Incorrect torque leads to leaks and failures.",
            "OEM and API require torque verification.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate torque verification and documentation for all fluid end maintenance.",
        entity_scope="OFE03 fluid ends",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 6A Section 10.2"
    ),
    DoctrineBlock(
        topic="Pump Suction Manifold Integrity",
        keywords=["suction manifold", "integrity", "inspection", "OFE03", "NDT"],
        conclusion_template="Suction manifolds must be inspected for cracks, corrosion, and wall loss every 100 operational hours using NDT methods.",
        reasoning_framework="""
1. Review operational hours and pressure history.
2. Perform NDT (ultrasonic, magnetic particle) on all manifold sections.
3. Measure wall thickness and check for pitting or cracks.
4. Compare findings to OEM and API minimums.
5. Document all inspection results.
6. Replace or repair any compromised sections.
7. Update inspection intervals based on findings.
8. Train personnel on NDT techniques.
9. Maintain records for regulatory compliance.
10. Analyze failure history for trends.
""",
        key_factors=[
            "Wall thickness",
            "Crack/corrosion detection",
            "Inspection interval",
            "NDT technique",
            "Failure history"
        ],
        primary_authority=[
            "API 6A",
            "OEM Suction Manifold Manual",
            "SPE 300-2022"
        ],
        burden_holder="Field Inspector",
        adversary_position="Visual inspection is sufficient.",
        counter_arguments=[
            "NDT detects defects not visible to the naked eye.",
            "API and OEM recommend NDT.",
            "Recent failures linked to undetected cracks."
        ],
        resolution_strategy="Implement mandatory NDT and adjust intervals as needed.",
        entity_scope="OFE03 suction manifolds",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 6A Section 9.3"
    ),
    DoctrineBlock(
        topic="Pump Discharge Manifold Pressure Monitoring",
        keywords=["discharge manifold", "pressure monitoring", "OFE03", "SCADA"],
        conclusion_template="Continuous pressure monitoring of discharge manifolds is required to detect overpressure and prevent failures.",
        reasoning_framework="""
1. Install pressure sensors on all discharge manifolds.
2. Integrate sensor data with SCADA for real-time alerts.
3. Set alarm thresholds per OEM and API recommendations.
4. Train operators on response protocols.
5. Document all overpressure incidents.
6. Review sensor calibration records.
7. Update alarm setpoints based on incident analysis.
8. Audit system performance quarterly.
9. Maintain records for regulatory compliance.
10. Communicate updates to all stakeholders.
""",
        key_factors=[
            "Sensor coverage",
            "Alarm thresholds",
            "Operator response",
            "Calibration records",
            "Incident history"
        ],
        primary_authority=[
            "API 6A",
            "OEM Discharge Manifold Manual",
            "SPE 310-2021"
        ],
        burden_holder="Control Room Operator",
        adversary_position="Periodic manual checks are sufficient.",
        counter_arguments=[
            "Continuous monitoring enables rapid response.",
            "Manual checks miss transient events.",
            "API and OEM require continuous monitoring."
        ],
        resolution_strategy="Implement continuous monitoring and train operators on alarm response.",
        entity_scope="OFE03 discharge manifolds",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 6A Section 10.4"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Material Traceability",
        keywords=["fluid end", "material", "traceability", "OFE03", "compliance"],
        conclusion_template="All fluid ends must have full material traceability to heat and batch, documented and available for regulatory review.",
        reasoning_framework="""
1. Require MTRs (Material Test Reports) for all fluid end components.
2. Record heat and batch numbers in asset management system.
3. Audit traceability records quarterly.
4. Replace any components lacking documentation.
5. Train procurement and maintenance personnel on traceability requirements.
6. Review regulatory and OEM requirements.
7. Document all traceability actions.
8. Communicate requirements to suppliers.
9. Maintain records for regulatory and warranty purposes.
10. Update procedures based on audit findings.
""",
        key_factors=[
            "MTR availability",
            "Record accuracy",
            "Audit frequency",
            "Supplier compliance",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API 6A",
            "OEM Material Traceability Policy",
            "SPE 320-2020"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Traceability is not required for aftermarket components.",
        counter_arguments=[
            "API 6A mandates traceability.",
            "Lack of documentation voids warranty.",
            "Regulatory audits require traceability."
        ],
        resolution_strategy="Enforce traceability for all components and audit compliance.",
        entity_scope="OFE03 fluid ends",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 6A Section 5.4"
    ),
    DoctrineBlock(
        topic="Pump Vibration Monitoring and Analysis",
        keywords=["vibration", "monitoring", "analysis", "OFE03", "predictive maintenance"],
        conclusion_template="Continuous vibration monitoring is required for all OFE03 pumps to enable predictive maintenance and prevent catastrophic failures.",
        reasoning_framework="""
1. Install vibration sensors on all critical pump components.
2. Integrate data with SCADA or standalone monitoring systems.
3. Set alarm thresholds for abnormal vibration levels.
4. Analyze vibration trends for early failure indicators.
5. Schedule maintenance based on vibration analysis.
6. Document all findings and corrective actions.
7. Train personnel on vibration monitoring and response.
8. Review failure history for vibration-related incidents.
9. Update monitoring protocols as needed.
10. Audit system performance quarterly.
""",
        key_factors=[
            "Sensor coverage",
            "Alarm thresholds",
            "Trend analysis",
            "Maintenance scheduling",
            "Training"
        ],
        primary_authority=[
            "API RP 687",
            "OEM Vibration Analysis Guide",
            "SPE 330-2021"
        ],
        burden_holder="Predictive Maintenance Engineer",
        adversary_position="Periodic manual checks are sufficient.",
        counter_arguments=[
            "Continuous monitoring enables early intervention.",
            "Manual checks miss transient events.",
            "API and OEM recommend continuous monitoring."
        ],
        resolution_strategy="Implement continuous vibration monitoring and integrate with maintenance scheduling.",
        entity_scope="OFE03 frac pumps",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 687 Section 6"
    ),
    DoctrineBlock(
        topic="Pump Fluid End NDT Interval Optimization",
        keywords=["fluid end", "NDT", "interval", "optimization", "OFE03"],
        conclusion_template="NDT intervals for fluid ends must be optimized based on failure history, operational severity, and OEM recommendations.",
        reasoning_framework="""
1. Review historical NDT findings and failure incidents.
2. Analyze operational severity (pressure, proppant concentration, job frequency).
3. Compare current intervals to OEM and API guidelines.
4. Adjust intervals to balance risk and operational efficiency.
5. Document all interval changes and rationale.
6. Train personnel on updated inspection schedules.
7. Monitor outcomes and adjust as needed.
8. Maintain records for regulatory and warranty compliance.
9. Communicate changes to all stakeholders.
10. Review and refine intervals annually.
""",
        key_factors=[
            "Failure history",
            "Operational severity",
            "OEM/API guidelines",
            "Interval documentation",
            "Outcome monitoring"
        ],
        primary_authority=[
            "API 6A",
            "OEM Fluid End Manual",
            "SPE 340-2022"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Fixed intervals are sufficient regardless of operational changes.",
        counter_arguments=[
            "Optimized intervals reduce failures and costs.",
            "Operational severity impacts wear rates.",
            "OEM recommends interval adjustment."
        ],
        resolution_strategy="Implement data-driven interval optimization and monitor outcomes.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 340-2022"
    ),
    DoctrineBlock(
        topic="Pump Power End Oil Sampling and Analysis",
        keywords=["power end", "oil", "sampling", "analysis", "OFE03"],
        conclusion_template="Oil samples from power ends must be analyzed quarterly for contamination and degradation to prevent bearing and gear failures.",
        reasoning_framework="""
1. Collect oil samples from all power ends quarterly.
2. Analyze samples for metal content, water, and viscosity.
3. Compare results to OEM and ISO standards.
4. Replace oil and filters if contamination or degradation is detected.
5. Document all analysis results and corrective actions.
6. Train personnel on sampling and analysis procedures.
7. Review failure history for oil-related incidents.
8. Update sampling protocols as needed.
9. Maintain records for regulatory compliance.
10. Communicate findings to maintenance and engineering.
""",
        key_factors=[
            "Sampling interval",
            "Contamination levels",
            "Oil degradation",
            "Corrective actions",
            "Training"
        ],
        primary_authority=[
            "ISO 4406",
            "OEM Power End Manual",
            "SPE 350-2021"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Annual sampling is sufficient.",
        counter_arguments=[
            "Quarterly sampling detects issues early.",
            "Contamination can cause catastrophic failures.",
            "OEM and ISO recommend frequent analysis."
        ],
        resolution_strategy="Enforce quarterly sampling and maintain analysis records.",
        entity_scope="OFE03 power ends",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 4406 Section 5"
    ),
    DoctrineBlock(
        topic="Pump Gearbox Temperature Monitoring",
        keywords=["gearbox", "temperature", "monitoring", "OFE03", "overheating"],
        conclusion_template="Continuous temperature monitoring of pump gearboxes is required to prevent overheating and gear failure.",
        reasoning_framework="""
1. Install temperature sensors on all gearboxes.
2. Integrate data with SCADA for real-time monitoring.
3. Set alarm thresholds per OEM recommendations.
4. Train operators on response protocols.
5. Document all overheating incidents.
6. Review sensor calibration records.
7. Update alarm setpoints based on incident analysis.
8. Audit system performance quarterly.
9. Maintain records for regulatory compliance.
10. Communicate updates to all stakeholders.
""",
        key_factors=[
            "Sensor coverage",
            "Alarm thresholds",
            "Operator response",
            "Calibration records",
            "Incident history"
        ],
        primary_authority=[
            "OEM Gearbox Manual",
            "API RP 687",
            "SPE 360-2022"
        ],
        burden_holder="Control Room Operator",
        adversary_position="Manual temperature checks are sufficient.",
        counter_arguments=[
            "Continuous monitoring enables rapid response.",
            "Manual checks miss transient events.",
            "OEM recommends continuous monitoring."
        ],
        resolution_strategy="Implement continuous temperature monitoring and train operators on alarm response.",
        entity_scope="OFE03 gearboxes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 687 Section 7"
    ),
    DoctrineBlock(
        topic="Pump Discharge Piping Restraint and Support",
        keywords=["discharge piping", "restraint", "support", "OFE03", "installation"],
        conclusion_template="All discharge piping must be properly restrained and supported to prevent vibration, movement, and fatigue failures.",
        reasoning_framework="""
1. Inspect all discharge piping for adequate supports and restraints.
2. Compare installation to OEM and API guidelines.
3. Document any deficiencies and corrective actions.
4. Train installation crews on proper support techniques.
5. Review failure history for piping-related incidents.
6. Update installation SOPs as needed.
7. Audit installations quarterly.
8. Maintain records for regulatory compliance.
9. Communicate requirements to all stakeholders.
10. Analyze incidents for root cause and prevention.
""",
        key_factors=[
            "Support adequacy",
            "Restraint effectiveness",
            "Installation compliance",
            "Training",
            "Audit frequency"
        ],
        primary_authority=[
            "API 6A",
            "OEM Installation Manual",
            "SPE 370-2021"
        ],
        burden_holder="Installation Supervisor",
        adversary_position="Minimal supports are sufficient for short-term jobs.",
        counter_arguments=[
            "Inadequate support leads to failures.",
            "API and OEM require proper restraint.",
            "Incidents have occurred due to poor support."
        ],
        resolution_strategy="Enforce support requirements and audit all installations.",
        entity_scope="OFE03 discharge piping",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 6A Section 11"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Guide Wear Analysis",
        keywords=["fluid end", "valve guide", "wear", "analysis", "OFE03"],
        conclusion_template="Valve guides must be inspected for wear and replaced if clearance exceeds OEM limits to prevent valve misalignment and failure.",
        reasoning_framework="""
1. Disassemble fluid end and inspect valve guides for wear.
2. Measure guide-to-valve clearance with calibrated gauges.
3. Compare measurements to OEM limits.
4. Replace guides exceeding allowable clearance.
5. Document all findings and replacements.
6. Train personnel on inspection and measurement techniques.
7. Review failure history for valve misalignment incidents.
8. Update maintenance SOPs as needed.
9. Audit compliance quarterly.
10. Maintain records for warranty and regulatory purposes.
""",
        key_factors=[
            "Guide wear",
            "Clearance measurement",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 380-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Guide wear is not critical unless severe.",
        counter_arguments=[
            "Excessive clearance leads to valve failure.",
            "OEM and API require guide inspection.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate guide inspection and replacement per OEM limits.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.7"
    ),
    DoctrineBlock(
        topic="Pump Suction Strainer Inspection and Cleaning",
        keywords=["suction strainer", "inspection", "cleaning", "OFE03"],
        conclusion_template="Suction strainers must be inspected and cleaned every 24 operational hours to prevent debris ingress and pump damage.",
        reasoning_framework="""
1. Schedule strainer inspection and cleaning every 24 hours of operation.
2. Remove and inspect strainer for debris and damage.
3. Clean or replace as needed.
4. Document all inspections and maintenance.
5. Train personnel on proper cleaning procedures.
6. Review failure history for debris-related incidents.
7. Update SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for regulatory and warranty purposes.
10. Communicate requirements to all operators.
""",
        key_factors=[
            "Inspection interval",
            "Debris accumulation",
            "Cleaning effectiveness",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Suction Strainer Manual",
            "API RP 11P",
            "SPE 390-2021"
        ],
        burden_holder="Pump Operator",
        adversary_position="Longer intervals are sufficient if no issues are observed.",
        counter_arguments=[
            "Debris can accumulate rapidly.",
            "Frequent cleaning prevents failures.",
            "OEM recommends daily checks."
        ],
        resolution_strategy="Enforce 24-hour inspection and cleaning intervals.",
        entity_scope="OFE03 frac pumps",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 9"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Pressure Test Protocol",
        keywords=["fluid end", "pressure test", "protocol", "OFE03"],
        conclusion_template="Fluid ends must be pressure tested to 1.5x MAWP after any maintenance or repair before returning to service.",
        reasoning_framework="""
1. Perform pressure test to 1.5x MAWP after maintenance or repair.
2. Hold test pressure for minimum 15 minutes.
3. Inspect for leaks, deformation, or pressure loss.
4. Document all test results and corrective actions.
5. Replace or repair any components failing test.
6. Train personnel on pressure test procedures.
7. Review test records for trends.
8. Update protocols as needed.
9. Audit compliance quarterly.
10. Maintain records for regulatory and warranty purposes.
""",
        key_factors=[
            "Test pressure",
            "Hold time",
            "Leak detection",
            "Documentation",
            "Training"
        ],
        primary_authority=[
            "API 6A",
            "OEM Fluid End Manual",
            "SPE 400-2022"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Lower test pressures are sufficient.",
        counter_arguments=[
            "API and OEM require 1.5x MAWP.",
            "Higher pressure ensures integrity.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate 1.5x MAWP testing and documentation for all fluid end repairs.",
        entity_scope="OFE03 fluid ends",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 6A Section 10.5"
    ),
    DoctrineBlock(
        topic="Pump Power End Crankshaft Inspection",
        keywords=["power end", "crankshaft", "inspection", "OFE03"],
        conclusion_template="Crankshafts must be inspected for cracks, wear, and alignment every 1,000 operational hours or during major overhauls.",
        reasoning_framework="""
1. Schedule crankshaft inspection every 1,000 hours or during overhauls.
2. Use NDT (magnetic particle, ultrasonic) to detect cracks.
3. Measure journals for wear and out-of-round.
4. Verify alignment using dial indicators.
5. Document all findings and corrective actions.
6. Replace or repair crankshafts as needed.
7. Train personnel on inspection techniques.
8. Review failure history for crankshaft-related incidents.
9. Update inspection protocols as needed.
10. Maintain records for regulatory and warranty purposes.
""",
        key_factors=[
            "Inspection interval",
            "Crack/wear detection",
            "Alignment verification",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 11P",
            "SPE 410-2021"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Visual inspection is sufficient.",
        counter_arguments=[
            "NDT detects defects not visible to the naked eye.",
            "OEM and API recommend periodic NDT.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate NDT and alignment checks at specified intervals.",
        entity_scope="OFE03 power ends",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 10"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Spring Fatigue Analysis",
        keywords=["fluid end", "valve spring", "fatigue", "analysis", "OFE03"],
        conclusion_template="Valve springs must be inspected for fatigue and replaced at intervals recommended by the OEM or upon detection of loss of free length.",
        reasoning_framework="""
1. Disassemble fluid end and inspect valve springs for cracks, corrosion, and loss of free length.
2. Measure free length and compare to OEM specifications.
3. Replace springs not meeting criteria.
4. Document all inspections and replacements.
5. Train personnel on fatigue detection techniques.
6. Review failure history for spring-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance quarterly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Spring fatigue",
            "Free length measurement",
            "Replacement interval",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 420-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Springs only need replacement upon failure.",
        counter_arguments=[
            "Fatigue can lead to sudden failure.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate spring inspection and replacement per OEM intervals.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.8"
    ),
    DoctrineBlock(
        topic="Pump Crosshead and Guide Wear Inspection",
        keywords=["crosshead", "guide", "wear", "inspection", "OFE03"],
        conclusion_template="Crossheads and guides must be inspected for wear and alignment every 500 operational hours to prevent power end failures.",
        reasoning_framework="""
1. Schedule crosshead and guide inspection every 500 hours.
2. Measure wear and alignment with calibrated tools.
3. Replace components exceeding OEM wear limits.
4. Document all inspections and replacements.
5. Train personnel on measurement techniques.
6. Review failure history for crosshead-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance quarterly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Wear measurement",
            "Alignment verification",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 11P",
            "SPE 430-2021"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Inspection interval can be extended if no issues are found.",
        counter_arguments=[
            "Wear can accelerate unexpectedly.",
            "OEM and API recommend fixed intervals.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate inspection at specified intervals and adjust as needed.",
        entity_scope="OFE03 power ends",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 11"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Retainer Torque Verification",
        keywords=["fluid end", "valve retainer", "torque", "verification", "OFE03"],
        conclusion_template="Valve retainers must be torqued to OEM specifications and verified after any maintenance to prevent valve ejection and failure.",
        reasoning_framework="""
1. Use calibrated torque wrenches for all valve retainer tightening.
2. Verify torque values post-maintenance.
3. Document all torque readings.
4. Replace retainers not meeting OEM criteria.
5. Train personnel on proper torque procedures.
6. Review failure history for retainer-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Torque accuracy",
            "Retainer condition",
            "Maintenance compliance",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 440-2022"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Hand tightening is sufficient for experienced personnel.",
        counter_arguments=[
            "Incorrect torque leads to failures.",
            "OEM and API require torque verification.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate torque verification and documentation for all valve retainer maintenance.",
        entity_scope="OFE03 fluid ends",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.9"
    ),
    DoctrineBlock(
        topic="Pump Power End Connecting Rod Bolt Inspection",
        keywords=["power end", "connecting rod", "bolt", "inspection", "OFE03"],
        conclusion_template="Connecting rod bolts must be inspected for stretch and replaced at intervals recommended by the OEM or upon detection of elongation.",
        reasoning_framework="""
1. Disassemble power end and inspect connecting rod bolts for stretch.
2. Measure bolt length and compare to OEM specifications.
3. Replace bolts exceeding allowable elongation.
4. Document all inspections and replacements.
5. Train personnel on measurement techniques.
6. Review failure history for bolt-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance quarterly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Bolt elongation",
            "Replacement interval",
            "Measurement accuracy",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 11P",
            "SPE 450-2021"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Bolts only need replacement upon failure.",
        counter_arguments=[
            "Stretch can lead to sudden failure.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate bolt inspection and replacement per OEM intervals.",
        entity_scope="OFE03 power ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 12"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Seat Installation Procedure",
        keywords=["fluid end", "valve seat", "installation", "procedure", "OFE03"],
        conclusion_template="Valve seats must be installed using OEM-approved tools and procedures to ensure proper fit and sealing.",
        reasoning_framework="""
1. Use OEM-approved tools for valve seat installation.
2. Clean all mating surfaces prior to installation.
3. Apply recommended lubricant or sealant as specified.
4. Press seat into place using proper force and alignment.
5. Inspect for proper seating and sealing.
6. Document all installations.
7. Train personnel on installation procedures.
8. Review failure history for seat-related incidents.
9. Update SOPs as needed.
10. Audit compliance regularly.
""",
        key_factors=[
            "Tool selection",
            "Surface preparation",
            "Alignment",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 460-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Alternative tools and methods are sufficient.",
        counter_arguments=[
            "Improper installation leads to leaks and failures.",
            "OEM and API require approved procedures.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate use of OEM tools and procedures for all seat installations.",
        entity_scope="OFE03 fluid ends",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.10"
    ),
    DoctrineBlock(
        topic="Pump Power End Oil Heater Operation in Cold Weather",
        keywords=["power end", "oil heater", "operation", "cold weather", "OFE03"],
        conclusion_template="Oil heaters must be operational and tested prior to cold weather to ensure proper lubrication and prevent power end failures.",
        reasoning_framework="""
1. Inspect and test oil heaters prior to onset of cold weather.
2. Verify heater operation and temperature control.
3. Document all tests and corrective actions.
4. Train personnel on heater operation and troubleshooting.
5. Review failure history for cold weather incidents.
6. Update SOPs as needed.
7. Audit compliance regularly.
8. Maintain records for warranty and regulatory purposes.
9. Communicate requirements to all maintenance personnel.
10. Analyze incidents for root cause and prevention.
""",
        key_factors=[
            "Heater operation",
            "Temperature control",
            "Testing interval",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 14J",
            "SPE 470-2022"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Heaters are unnecessary if pumps are kept running.",
        counter_arguments=[
            "Downtime can lead to oil thickening.",
            "OEM and API recommend heaters in cold weather.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate heater testing and operation prior to cold weather.",
        entity_scope="OFE03 power ends",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 14J Section 8"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Locking Device Inspection",
        keywords=["fluid end", "valve", "locking device", "inspection", "OFE03"],
        conclusion_template="Valve locking devices must be inspected for integrity and proper engagement every 100 operational hours.",
        reasoning_framework="""
1. Schedule inspection of valve locking devices every 100 hours.
2. Check for wear, deformation, or disengagement.
3. Replace any defective devices.
4. Document all inspections and replacements.
5. Train personnel on inspection techniques.
6. Review failure history for locking device-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance quarterly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Inspection interval",
            "Device integrity",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 480-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Locking devices only need inspection upon failure.",
        counter_arguments=[
            "Failure can lead to catastrophic incidents.",
            "OEM and API recommend proactive inspection.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate inspection and replacement per OEM intervals.",
        entity_scope="OFE03 fluid ends",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.11"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Cage Wear Analysis",
        keywords=["fluid end", "valve cage", "wear", "analysis", "OFE03"],
        conclusion_template="Valve cages must be inspected for wear and replaced if clearance or damage exceeds OEM limits.",
        reasoning_framework="""
1. Disassemble fluid end and inspect valve cages for wear and damage.
2. Measure clearance and compare to OEM specifications.
3. Replace cages exceeding allowable limits.
4. Document all inspections and replacements.
5. Train personnel on measurement techniques.
6. Review failure history for cage-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance quarterly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Wear measurement",
            "Clearance limits",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 490-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Cages only need replacement upon failure.",
        counter_arguments=[
            "Excessive wear leads to valve misalignment.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate cage inspection and replacement per OEM limits.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.12"
    ),
    DoctrineBlock(
        topic="Pump Power End Main Bearing Cap Bolt Torque Verification",
        keywords=["power end", "main bearing cap", "bolt", "torque", "verification", "OFE03"],
        conclusion_template="Main bearing cap bolts must be torqued to OEM specifications and verified after any maintenance to prevent bearing movement and failure.",
        reasoning_framework="""
1. Use calibrated torque wrenches for all main bearing cap bolt tightening.
2. Verify torque values post-maintenance.
3. Document all torque readings.
4. Replace bolts not meeting OEM criteria.
5. Train personnel on proper torque procedures.
6. Review failure history for bearing cap-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Torque accuracy",
            "Bolt condition",
            "Maintenance compliance",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 11P",
            "SPE 500-2022"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Hand tightening is sufficient for experienced personnel.",
        counter_arguments=[
            "Incorrect torque leads to failures.",
            "OEM and API require torque verification.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate torque verification and documentation for all main bearing cap maintenance.",
        entity_scope="OFE03 power ends",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 13"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Stop Installation Procedure",
        keywords=["fluid end", "valve stop", "installation", "procedure", "OFE03"],
        conclusion_template="Valve stops must be installed per OEM procedures to ensure proper valve movement and prevent impact damage.",
        reasoning_framework="""
1. Use OEM procedures for valve stop installation.
2. Verify correct orientation and engagement.
3. Inspect for proper movement and clearance.
4. Document all installations.
5. Train personnel on installation techniques.
6. Review failure history for valve stop-related incidents.
7. Update SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Installation procedure",
            "Orientation",
            "Movement verification",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 510-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Alternative installation methods are sufficient.",
        counter_arguments=[
            "Improper installation leads to valve damage.",
            "OEM and API require approved procedures.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate use of OEM procedures for all valve stop installations.",
        entity_scope="OFE03 fluid ends",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.13"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Key Installation and Inspection",
        keywords=["fluid end", "valve key", "installation", "inspection", "OFE03"],
        conclusion_template="Valve keys must be installed and inspected per OEM procedures to ensure proper valve retention and prevent failures.",
        reasoning_framework="""
1. Use OEM procedures for valve key installation.
2. Inspect for proper engagement and wear.
3. Replace keys showing signs of damage or wear.
4. Document all installations and inspections.
5. Train personnel on installation and inspection techniques.
6. Review failure history for valve key-related incidents.
7. Update SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Installation procedure",
            "Engagement verification",
            "Wear detection",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 520-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Keys only need replacement upon failure.",
        counter_arguments=[
            "Improper installation leads to valve failures.",
            "OEM and API require proactive inspection.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate installation and inspection per OEM procedures.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.14"
    ),
    DoctrineBlock(
        topic="Pump Power End Oil Filter Inspection and Replacement",
        keywords=["power end", "oil filter", "inspection", "replacement", "OFE03"],
        conclusion_template="Oil filters must be inspected and replaced at intervals recommended by the OEM or upon detection of contamination.",
        reasoning_framework="""
1. Inspect oil filters at OEM-recommended intervals.
2. Replace filters showing signs of contamination or clogging.
3. Document all inspections and replacements.
4. Train personnel on filter inspection and replacement procedures.
5. Review failure history for oil-related incidents.
6. Update SOPs as needed.
7. Audit compliance regularly.
8. Maintain records for warranty and regulatory purposes.
9. Communicate requirements to all maintenance personnel.
10. Analyze incidents for root cause and prevention.
""",
        key_factors=[
            "Inspection interval",
            "Contamination detection",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Power End Manual",
            "API RP 11P",
            "SPE 530-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Filters only need replacement upon failure.",
        counter_arguments=[
            "Contaminated filters lead to failures.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate filter inspection and replacement per OEM intervals.",
        entity_scope="OFE03 power ends",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 11P Section 14"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Spring Retainer Inspection",
        keywords=["fluid end", "valve spring retainer", "inspection", "OFE03"],
        conclusion_template="Valve spring retainers must be inspected for wear and replaced if deformation or cracks are detected.",
        reasoning_framework="""
1. Inspect valve spring retainers during each maintenance cycle.
2. Check for wear, deformation, or cracks.
3. Replace retainers not meeting OEM criteria.
4. Document all inspections and replacements.
5. Train personnel on inspection techniques.
6. Review failure history for retainer-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Inspection frequency",
            "Wear detection",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 540-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Retainers only need replacement upon failure.",
        counter_arguments=[
            "Deformation leads to spring failure.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate retainer inspection and replacement per OEM criteria.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.15"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Insert Inspection and Replacement",
        keywords=["fluid end", "valve insert", "inspection", "replacement", "OFE03"],
        conclusion_template="Valve inserts must be inspected for wear and replaced if damage or loss of material is detected.",
        reasoning_framework="""
1. Inspect valve inserts during each maintenance cycle.
2. Check for wear, cracks, or loss of material.
3. Replace inserts not meeting OEM criteria.
4. Document all inspections and replacements.
5. Train personnel on inspection techniques.
6. Review failure history for insert-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Inspection frequency",
            "Wear detection",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 550-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Inserts only need replacement upon failure.",
        counter_arguments=[
            "Wear leads to valve failure.",
            "OEM and API recommend proactive replacement.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate insert inspection and replacement per OEM criteria.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.16"
    ),
    DoctrineBlock(
        topic="Pump Fluid End Valve Guide Retention Inspection",
        keywords=["fluid end", "valve guide", "retention", "inspection", "OFE03"],
        conclusion_template="Valve guide retention must be inspected for integrity and proper engagement during each maintenance cycle.",
        reasoning_framework="""
1. Inspect valve guide retention during each maintenance cycle.
2. Check for wear, deformation, or disengagement.
3. Replace any defective retention devices.
4. Document all inspections and replacements.
5. Train personnel on inspection techniques.
6. Review failure history for retention-related incidents.
7. Update maintenance SOPs as needed.
8. Audit compliance regularly.
9. Maintain records for warranty and regulatory purposes.
10. Communicate requirements to all maintenance personnel.
""",
        key_factors=[
            "Inspection frequency",
            "Retention integrity",
            "Replacement criteria",
            "Training",
            "Documentation"
        ],
        primary_authority=[
            "OEM Fluid End Manual",
            "API 7K",
            "SPE 560-2022"
        ],
        burden_holder="Maintenance Technician",
        adversary_position="Retention only needs inspection upon failure.",
        counter_arguments=[
            "Failure leads to valve misalignment.",
            "OEM and API recommend proactive inspection.",
            "Documentation is necessary for warranty."
        ],
        resolution_strategy="Mandate retention inspection and replacement per OEM criteria.",
        entity_scope="OFE03 fluid ends",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 7K Section 8.17"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]