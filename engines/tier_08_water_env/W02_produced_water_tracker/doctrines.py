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
        topic="Produced Water Volume Calculation",
        keywords=["volume", "produced water", "measurement", "production data", "allocation"],
        conclusion_template="The calculated produced water volume for the reporting period is {volume} bbl, determined in accordance with RRC and API standards.",
        reasoning_framework="""
        1. Collect daily production data from wellhead meters and tank gauges.
        2. Validate measurement devices are calibrated per API MPMS standards.
        3. Subtract base fluid and any injected volumes from gross liquid production to isolate produced water.
        4. Apply allocation factors if multiple wells share infrastructure.
        5. Cross-check with historical trends and anomaly detection.
        6. Document all calculation steps and retain supporting data for audit.
        7. Ensure compliance with RRC reporting requirements and operator-specific SOPs.
        """,
        key_factors=[
            "Meter calibration records",
            "Separation efficiency",
            "Allocation methodology",
            "Data integrity",
            "Regulatory reporting deadlines"
        ],
        primary_authority=[
            "Texas Railroad Commission (RRC) Rule 13",
            "API MPMS Chapter 4",
            "Operator SOP"
        ],
        burden_holder="Operator",
        adversary_position="Volumes may be overstated due to tank measurement errors or misallocation.",
        counter_arguments=[
            "Independent meter calibration records available",
            "Automated data logging reduces manual error",
            "Third-party verification conducted"
        ],
        resolution_strategy="Audit measurement records and perform field verification.",
        entity_scope="Well, Lease, Facility",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RRC Oil and Gas Division Guidance Letter 2018-05"
    ),
    DoctrineBlock(
        topic="Water-Oil Ratio Analysis",
        keywords=["WOR", "water-oil ratio", "production trend", "reservoir management"],
        conclusion_template="The water-oil ratio for {well} is {ratio}, indicating {interpretation} per reservoir engineering standards.",
        reasoning_framework="""
        1. Aggregate oil and water production data over the selected interval.
        2. Calculate WOR as produced water volume divided by oil volume.
        3. Analyze temporal trends to identify breakthrough or reservoir changes.
        4. Compare with offset wells and type curves.
        5. Assess operational impacts and potential interventions.
        6. Document findings and communicate with reservoir management team.
        """,
        key_factors=[
            "Production data accuracy",
            "Reservoir heterogeneity",
            "Lift method changes",
            "Water breakthrough timing"
        ],
        primary_authority=[
            "SPE Petroleum Engineering Handbook",
            "RRC Production Reporting Rules"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="WOR may be skewed by temporary operational upsets or measurement errors.",
        counter_arguments=[
            "Data smoothing and anomaly filtering applied",
            "Short-term upsets excluded from trend analysis"
        ],
        resolution_strategy="Use rolling averages and corroborate with field observations.",
        entity_scope="Well, Field",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 3, Water Control"
    ),
    DoctrineBlock(
        topic="Saltwater Disposal (SWD) Well Permitting",
        keywords=["SWD", "disposal well", "permitting", "UIC", "Class II"],
        conclusion_template="SWD well permit for {location} is {status} subject to RRC and EPA UIC Class II requirements.",
        reasoning_framework="""
        1. Submit Form H-1 and supporting documentation to RRC.
        2. Demonstrate mechanical integrity and suitable injection zone.
        3. Provide area of review (AOR) and evaluate potential for induced seismicity.
        4. Notify offset operators and landowners as required.
        5. Address public comments and regulatory queries.
        6. Await RRC and, if applicable, EPA approval.
        7. Maintain permit compliance through ongoing monitoring and reporting.
        """,
        key_factors=[
            "Well construction standards",
            "Injection zone suitability",
            "Seismic risk assessment",
            "Public notice compliance"
        ],
        primary_authority=[
            "RRC Statewide Rule 9",
            "EPA UIC Program",
            "40 CFR Part 146"
        ],
        burden_holder="Applicant (Operator)",
        adversary_position="Potential for groundwater contamination or seismicity not fully addressed.",
        counter_arguments=[
            "AOR and MIT results demonstrate containment",
            "Seismicity risk mitigated through operational controls"
        ],
        resolution_strategy="Regulatory review and public hearing if contested.",
        entity_scope="Facility, Field, Basin",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="RRC Docket No. 09-0256789"
    ),
    DoctrineBlock(
        topic="RRC Form H-1 Requirements",
        keywords=["Form H-1", "SWD", "permitting", "RRC", "application"],
        conclusion_template="Form H-1 for SWD well at {location} is {status} with all required attachments and certifications.",
        reasoning_framework="""
        1. Complete all sections of Form H-1, including well data, injection interval, and proposed rates.
        2. Attach well logs, casing diagrams, and area maps.
        3. Certify compliance with RRC construction and operation standards.
        4. Submit to RRC with applicable fees.
        5. Respond to RRC requests for additional information.
        6. Retain copies for operator records and potential audit.
        """,
        key_factors=[
            "Completeness of application",
            "Accuracy of technical data",
            "Timeliness of submission"
        ],
        primary_authority=[
            "RRC Statewide Rule 9",
            "RRC Form H-1 Instructions"
        ],
        burden_holder="Operator",
        adversary_position="Incomplete or inaccurate information may delay approval.",
        counter_arguments=[
            "Pre-submission review checklist used",
            "Third-party engineering review conducted"
        ],
        resolution_strategy="Resubmit with corrections as directed by RRC.",
        entity_scope="Facility",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RRC Form H-1 Guidance 2021"
    ),
    DoctrineBlock(
        topic="Disposal Well Capacity Determination",
        keywords=["capacity", "SWD", "disposal well", "injection rate", "formation"],
        conclusion_template="The maximum permitted disposal rate for {well} is {rate} bbl/day, based on formation injectivity and regulatory limits.",
        reasoning_framework="""
        1. Evaluate formation injectivity using step-rate and falloff tests.
        2. Review historical injection performance and pressure trends.
        3. Compare with RRC-permitted limits and area precedents.
        4. Consider mechanical integrity and wellbore constraints.
        5. Document supporting data and calculations.
        6. Submit findings to RRC for approval or modification of permit.
        """,
        key_factors=[
            "Injectivity test results",
            "Formation pressure",
            "Wellbore integrity",
            "Regulatory maximums"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Capacity may be overstated if formation damage or pressure buildup occurs.",
        counter_arguments=[
            "Recent injectivity tests confirm capacity",
            "Continuous pressure monitoring in place"
        ],
        resolution_strategy="Periodic retesting and regulatory review.",
        entity_scope="Well",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RRC Permit No. 08-123456"
    ),
    DoctrineBlock(
        topic="Injection Pressure Limits",
        keywords=["injection pressure", "SWD", "fracture gradient", "regulatory limit"],
        conclusion_template="The maximum allowable surface injection pressure for {well} is {pressure} psi, as determined by RRC and formation fracture gradient.",
        reasoning_framework="""
        1. Calculate fracture gradient for the injection zone using well logs and core data.
        2. Apply a safety margin per RRC and API guidelines.
        3. Set surface injection pressure limit accordingly.
        4. Install pressure monitoring devices with alarm thresholds.
        5. Review and update limits as formation data evolves.
        6. Report any exceedances to RRC per incident reporting rules.
        """,
        key_factors=[
            "Fracture gradient",
            "Wellbore pressure rating",
            "Regulatory safety factor"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Pressure limits may not account for local heterogeneity or operational upsets.",
        counter_arguments=[
            "Site-specific data used for limit determination",
            "Redundant pressure monitoring installed"
        ],
        resolution_strategy="Continuous monitoring and periodic limit reassessment.",
        entity_scope="Well",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="RRC Technical Memo 2019-02"
    ),
    DoctrineBlock(
        topic="Disposal Cost Modeling",
        keywords=["cost", "disposal", "SWD", "economics", "OPEX"],
        conclusion_template="The modeled disposal cost per barrel is ${cost}/bbl, incorporating transportation, injection, and regulatory compliance expenses.",
        reasoning_framework="""
        1. Itemize all cost components: transportation, injection, chemical treatment, monitoring, and reporting.
        2. Collect historical cost data and adjust for inflation.
        3. Model variable and fixed costs over projected disposal volumes.
        4. Include regulatory compliance and contingency allowances.
        5. Benchmark against regional SWD market rates.
        6. Document assumptions and sensitivity analysis.
        """,
        key_factors=[
            "Transportation distance",
            "SWD well fees",
            "Volume variability",
            "Regulatory changes"
        ],
        primary_authority=[
            "SEC Regulation S-X",
            "Operator Cost Accounting Policy"
        ],
        burden_holder="Operator Finance Team",
        adversary_position="Model may underestimate costs due to unanticipated regulatory changes or operational upsets.",
        counter_arguments=[
            "Sensitivity analysis covers regulatory scenarios",
            "Contingency reserves included"
        ],
        resolution_strategy="Periodic model updates and variance analysis.",
        entity_scope="Field, Asset",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="SEC Staff Accounting Bulletin No. 113"
    ),
    DoctrineBlock(
        topic="Produced Water Recycling Economics",
        keywords=["recycling", "economics", "produced water", "reuse", "cost-benefit"],
        conclusion_template="Produced water recycling is {feasibility} at a net cost of ${cost}/bbl, based on current technology and market conditions.",
        reasoning_framework="""
        1. Assess available recycling technologies and their treatment efficacy.
        2. Estimate capital and operating costs for recycling infrastructure.
        3. Compare recycled water cost to fresh water sourcing and disposal.
        4. Evaluate market demand for recycled water (e.g., for frac operations).
        5. Incorporate regulatory incentives or restrictions.
        6. Perform NPV and IRR analysis over project life.
        """,
        key_factors=[
            "Treatment technology cost",
            "Water quality requirements",
            "Market demand",
            "Regulatory incentives"
        ],
        primary_authority=[
            "SPE 184065",
            "Texas Water Code Chapter 27"
        ],
        burden_holder="Operator",
        adversary_position="Recycling may not be economic at low oil prices or in remote locations.",
        counter_arguments=[
            "Regulatory incentives improve economics",
            "Mobile treatment units reduce logistics cost"
        ],
        resolution_strategy="Pilot testing and phased implementation.",
        entity_scope="Field, Asset",
        confidence=0.84,
        confidence_zone="Moderate",
        controlling_precedent="SPE 184065"
    ),
    DoctrineBlock(
        topic="Water Transfer Pipeline Routing",
        keywords=["pipeline", "routing", "water transfer", "ROW", "permitting"],
        conclusion_template="The optimal water transfer pipeline route is selected based on {criteria}, minimizing cost and regulatory risk.",
        reasoning_framework="""
        1. Map all feasible routes using GIS and topographic data.
        2. Identify land ownership and secure rights-of-way (ROW).
        3. Assess environmental and regulatory constraints.
        4. Minimize crossings of sensitive areas (wetlands, streams, cultural sites).
        5. Optimize for construction cost, maintenance access, and hydraulic efficiency.
        6. Obtain all necessary permits before construction.
        """,
        key_factors=[
            "Landowner agreements",
            "Environmental impact",
            "Regulatory approvals",
            "Construction cost"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "US Army Corps of Engineers Section 404"
        ],
        burden_holder="Operator Project Team",
        adversary_position="Route selection may not adequately address environmental or community concerns.",
        counter_arguments=[
            "Stakeholder engagement conducted",
            "Alternative routes evaluated"
        ],
        resolution_strategy="Public consultation and environmental review.",
        entity_scope="Field, Asset",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="USACE Permit Guidance 2017"
    ),
    DoctrineBlock(
        topic="Disposal Well Network Optimization",
        keywords=["network", "optimization", "SWD", "logistics", "cost"],
        conclusion_template="The optimized disposal well network minimizes total cost and maximizes operational reliability for the asset.",
        reasoning_framework="""
        1. Model produced water flows from all wells to candidate SWD sites.
        2. Optimize for transportation cost, SWD capacity, and regulatory compliance.
        3. Incorporate constraints such as truck routing, pipeline availability, and injection limits.
        4. Use linear programming or heuristic algorithms to identify optimal network.
        5. Validate model with historical operations data.
        6. Update network as new SWD capacity or production comes online.
        """,
        key_factors=[
            "SWD well locations and capacity",
            "Produced water volumes",
            "Transportation logistics",
            "Regulatory injection limits"
        ],
        primary_authority=[
            "SPE 190965",
            "Operator Logistics Policy"
        ],
        burden_holder="Asset Manager",
        adversary_position="Model may not account for real-time operational disruptions or regulatory changes.",
        counter_arguments=[
            "Scenario analysis and contingency planning included",
            "Model updated quarterly"
        ],
        resolution_strategy="Continuous improvement and stakeholder review.",
        entity_scope="Asset, Basin",
        confidence=0.86,
        confidence_zone="Moderate",
        controlling_precedent="SPE 190965"
    ),
    DoctrineBlock(
        topic="Produced Water Chemistry: TDS and Chlorides",
        keywords=["chemistry", "TDS", "chlorides", "analysis", "water quality"],
        conclusion_template="Produced water from {well} has TDS of {tds} mg/L and chloride concentration of {chlorides} mg/L, within {compliance} limits.",
        reasoning_framework="""
        1. Collect representative produced water samples per API RP 45.
        2. Analyze for TDS and chlorides using EPA-approved methods.
        3. Compare results to disposal well and recycling facility acceptance criteria.
        4. Identify trends or anomalies that may indicate operational issues.
        5. Document and report results as required by RRC or EPA.
        """,
        key_factors=[
            "Sampling protocol",
            "Analytical method accuracy",
            "Acceptance criteria",
            "Data trending"
        ],
        primary_authority=[
            "API RP 45",
            "EPA Method 300.0"
        ],
        burden_holder="Operator Lab",
        adversary_position="Sample contamination or improper handling may skew results.",
        counter_arguments=[
            "Chain of custody maintained",
            "Duplicate and blank samples analyzed"
        ],
        resolution_strategy="Retest and review sampling procedures.",
        entity_scope="Well, Facility",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 45"
    ),
    DoctrineBlock(
        topic="Frac Water Reuse Standards",
        keywords=["frac water", "reuse", "standards", "treatment", "regulatory"],
        conclusion_template="Frac water reuse meets {standard} for TDS, bacteria, and oil content, enabling safe and effective hydraulic fracturing.",
        reasoning_framework="""
        1. Define target water quality parameters for frac operations.
        2. Select treatment technologies to achieve required standards.
        3. Test treated water for TDS, bacteria, oil, and other key parameters.
        4. Ensure compliance with operator and regulatory standards.
        5. Document treatment process and quality assurance results.
        """,
        key_factors=[
            "Treatment technology selection",
            "Water quality targets",
            "Regulatory requirements",
            "Quality assurance testing"
        ],
        primary_authority=[
            "API Guidance Document HF2",
            "Texas Water Development Board"
        ],
        burden_holder="Operator",
        adversary_position="Treated water may not consistently meet frac quality standards.",
        counter_arguments=[
            "Continuous monitoring and batch testing implemented",
            "Redundant treatment steps in place"
        ],
        resolution_strategy="Quality assurance program and corrective action procedures.",
        entity_scope="Facility, Field",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API HF2"
    ),
    DoctrineBlock(
        topic="Produced Water Hauling Logistics",
        keywords=["hauling", "logistics", "trucking", "dispatch", "cost"],
        conclusion_template="Produced water hauling schedule optimizes cost and minimizes risk of overflow or regulatory non-compliance.",
        reasoning_framework="""
        1. Forecast produced water volumes by location and time.
        2. Schedule truck dispatches to match production and SWD availability.
        3. Monitor real-time tank levels and adjust schedules as needed.
        4. Ensure compliance with DOT and RRC hauling regulations.
        5. Track costs and optimize routes for efficiency.
        """,
        key_factors=[
            "Volume forecasting accuracy",
            "Truck availability",
            "Regulatory compliance",
            "Cost per barrel hauled"
        ],
        primary_authority=[
            "DOT FMCSA Regulations",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Logistics Coordinator",
        adversary_position="Unplanned upsets may cause overflow or missed pickups.",
        counter_arguments=[
            "Real-time monitoring and dynamic scheduling",
            "Backup hauling contracts in place"
        ],
        resolution_strategy="Contingency planning and continuous improvement.",
        entity_scope="Field, Asset",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="DOT FMCSA Guidance 2018"
    ),
    DoctrineBlock(
        topic="RRC H-10 Reporting",
        keywords=["H-10", "reporting", "SWD", "compliance", "RRC"],
        conclusion_template="H-10 reporting for SWD well at {location} is {status}, with all required data submitted by the deadline.",
        reasoning_framework="""
        1. Compile monthly injection volumes, pressures, and well status data.
        2. Complete Form H-10 per RRC instructions.
        3. Submit electronically by the 15th of the following month.
        4. Retain supporting documentation for audit.
        5. Address any RRC queries or discrepancies promptly.
        """,
        key_factors=[
            "Data accuracy",
            "Timely submission",
            "Supporting documentation"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "RRC Form H-10 Instructions"
        ],
        burden_holder="Operator",
        adversary_position="Late or inaccurate reporting may result in penalties.",
        counter_arguments=[
            "Automated data collection and validation",
            "Internal compliance audits"
        ],
        resolution_strategy="Implement compliance calendar and periodic training.",
        entity_scope="Facility",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="RRC Compliance Bulletin 2020-01"
    ),
    DoctrineBlock(
        topic="Formation Compatibility Assessment",
        keywords=["formation", "compatibility", "SWD", "scaling", "souring"],
        conclusion_template="Produced water is {compatibility} with the injection formation, minimizing risk of scaling or souring.",
        reasoning_framework="""
        1. Analyze produced water and formation water chemistry.
        2. Model scaling and precipitation potential using geochemical software.
        3. Assess risk of microbial souring and corrosion.
        4. Recommend treatment or blending if compatibility issues are identified.
        5. Monitor injection performance and well integrity over time.
        """,
        key_factors=[
            "Water chemistry analysis",
            "Scaling indices",
            "Microbial activity",
            "Historical well performance"
        ],
        primary_authority=[
            "API RP 45",
            "SPE 169581"
        ],
        burden_holder="Operator",
        adversary_position="Incompatibility may cause formation damage and reduce injectivity.",
        counter_arguments=[
            "Pre-injection compatibility testing conducted",
            "Ongoing monitoring and mitigation in place"
        ],
        resolution_strategy="Adjust treatment program and retest as needed.",
        entity_scope="Well, Facility",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 169581"
    ),
    DoctrineBlock(
        topic="Injection Zone Pressure Monitoring",
        keywords=["pressure", "monitoring", "injection zone", "SWD", "compliance"],
        conclusion_template="Injection zone pressure is maintained within safe limits, with real-time monitoring and alerting in place.",
        reasoning_framework="""
        1. Install downhole and surface pressure sensors.
        2. Monitor injection pressure continuously and log data.
        3. Set alarm thresholds below regulatory and mechanical limits.
        4. Investigate and document any excursions.
        5. Report significant events to RRC as required.
        """,
        key_factors=[
            "Sensor calibration",
            "Alarm thresholds",
            "Data logging integrity",
            "Regulatory reporting"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Sensor failure or data gaps may mask unsafe conditions.",
        counter_arguments=[
            "Redundant sensors and periodic calibration",
            "Automated data validation"
        ],
        resolution_strategy="Regular maintenance and data review.",
        entity_scope="Well, Facility",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 51R"
    ),
    DoctrineBlock(
        topic="Water Cut Trending",
        keywords=["water cut", "trending", "production", "analysis"],
        conclusion_template="Water cut trend for {well} indicates {interpretation}, supporting {operational_decision}.",
        reasoning_framework="""
        1. Calculate water cut as percentage of produced water to total liquids.
        2. Analyze trends over time to detect breakthrough or coning.
        3. Compare with offset wells and reservoir models.
        4. Identify operational or reservoir interventions if needed.
        5. Communicate findings to production and reservoir teams.
        """,
        key_factors=[
            "Production data quality",
            "Reservoir heterogeneity",
            "Operational changes"
        ],
        primary_authority=[
            "SPE Petroleum Engineering Handbook",
            "Operator SOP"
        ],
        burden_holder="Production Engineer",
        adversary_position="Short-term fluctuations may obscure long-term trends.",
        counter_arguments=[
            "Statistical smoothing applied",
            "Cross-validation with field observations"
        ],
        resolution_strategy="Combine quantitative and qualitative analysis.",
        entity_scope="Well, Field",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 3"
    ),
    DoctrineBlock(
        topic="Disposal Well Interference",
        keywords=["interference", "SWD", "pressure communication", "offset wells"],
        conclusion_template="No significant interference detected between SWD wells, supporting continued operation at permitted rates.",
        reasoning_framework="""
        1. Monitor pressure in offset wells during injection operations.
        2. Analyze for correlated pressure responses indicating communication.
        3. Use step-rate and falloff tests to confirm findings.
        4. Adjust injection rates if interference is detected.
        5. Report significant interference to RRC as required.
        """,
        key_factors=[
            "Pressure monitoring data",
            "Well spacing",
            "Injection rates",
            "Formation continuity"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Subtle interference may go undetected without high-frequency monitoring.",
        counter_arguments=[
            "High-resolution pressure data collected",
            "Periodic interference testing scheduled"
        ],
        resolution_strategy="Enhance monitoring and reduce injection rates if needed.",
        entity_scope="Field, Asset",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="RRC Technical Memo 2018-04"
    ),
    DoctrineBlock(
        topic="Produced Water Treatment Technologies",
        keywords=["treatment", "technology", "produced water", "filtration", "desalination"],
        conclusion_template="Selected treatment technology achieves target water quality for {application}, with CAPEX and OPEX within budget.",
        reasoning_framework="""
        1. Identify water quality targets for intended use (disposal, reuse, discharge).
        2. Screen available treatment technologies (e.g., media filtration, chemical precipitation, reverse osmosis).
        3. Pilot test promising technologies on representative samples.
        4. Evaluate cost, reliability, and operational complexity.
        5. Select technology and design treatment train.
        6. Monitor performance and adjust as needed.
        """,
        key_factors=[
            "Water quality targets",
            "Technology efficacy",
            "Cost",
            "Operational complexity"
        ],
        primary_authority=[
            "SPE 184065",
            "API RP 45"
        ],
        burden_holder="Operator",
        adversary_position="Selected technology may not perform as expected at scale.",
        counter_arguments=[
            "Pilot testing conducted",
            "Performance guarantees in vendor contracts"
        ],
        resolution_strategy="Phased implementation and performance monitoring.",
        entity_scope="Facility, Field",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="SPE 184065"
    ),
    DoctrineBlock(
        topic="Produced Water Forecasting",
        keywords=["forecasting", "produced water", "volumes", "production planning"],
        conclusion_template="Produced water forecast for {asset} is {volume} bbl/day, supporting infrastructure and logistics planning.",
        reasoning_framework="""
        1. Analyze historical production and water cut trends.
        2. Model future water production using reservoir simulation and decline curves.
        3. Incorporate planned drilling, workovers, and EOR projects.
        4. Adjust for operational constraints and regulatory changes.
        5. Validate forecasts against actuals and update regularly.
        """,
        key_factors=[
            "Historical production data",
            "Reservoir model accuracy",
            "Operational plans",
            "Regulatory environment"
        ],
        primary_authority=[
            "SPE Petroleum Engineering Handbook",
            "Operator Planning SOP"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Forecasts may be inaccurate due to unforeseen operational or reservoir changes.",
        counter_arguments=[
            "Scenario planning and sensitivity analysis conducted",
            "Forecasts updated quarterly"
        ],
        resolution_strategy="Continuous improvement and stakeholder review.",
        entity_scope="Asset, Field",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="SPE Monograph Vol. 3"
    ),
    # Additional doctrines to reach 40+
    DoctrineBlock(
        topic="Mechanical Integrity Testing (MIT) for SWD Wells",
        keywords=["mechanical integrity", "MIT", "SWD", "testing", "compliance"],
        conclusion_template="SWD well at {location} passed MIT on {date}, confirming wellbore and casing integrity.",
        reasoning_framework="""
        1. Schedule MIT per RRC requirements (every 5 years or as directed).
        2. Perform pressure test or radioactive tracer survey.
        3. Document test parameters, results, and any anomalies.
        4. Submit results to RRC and retain for audit.
        5. Address any failures before resuming injection.
        """,
        key_factors=[
            "Test frequency",
            "Test method",
            "Documentation",
            "Regulatory submission"
        ],
        primary_authority=[
            "RRC Statewide Rule 46",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Test may not detect all integrity issues, especially in complex completions.",
        counter_arguments=[
            "Supplemental logs and monitoring used",
            "RRC review and oversight"
        ],
        resolution_strategy="Enhanced testing and periodic review.",
        entity_scope="Well",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="RRC Compliance Bulletin 2019-03"
    ),
    DoctrineBlock(
        topic="Area of Review (AOR) Evaluation",
        keywords=["AOR", "area of review", "SWD", "permitting", "well integrity"],
        conclusion_template="AOR evaluation for SWD well at {location} identified {number} wells within 1/4 mile, all with documented integrity.",
        reasoning_framework="""
        1. Map all wells within 1/4 mile of proposed SWD well.
        2. Review well construction and plugging status.
        3. Assess risk of fluid migration through legacy wells.
        4. Document findings and submit with permit application.
        5. Mitigate identified risks before commencing injection.
        """,
        key_factors=[
            "Well mapping accuracy",
            "Legacy well integrity",
            "Documentation",
            "Regulatory review"
        ],
        primary_authority=[
            "EPA UIC Guidance",
            "RRC Statewide Rule 9"
        ],
        burden_holder="Applicant (Operator)",
        adversary_position="Legacy wells may be undocumented or poorly plugged.",
        counter_arguments=[
            "Field verification and historical records review",
            "Contingency plans in place"
        ],
        resolution_strategy="Additional field investigation and regulatory coordination.",
        entity_scope="Facility, Field",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="EPA UIC Guidance"
    ),
    DoctrineBlock(
        topic="Induced Seismicity Risk Management",
        keywords=["seismicity", "induced", "SWD", "risk", "earthquake"],
        conclusion_template="Induced seismicity risk is {level}, with mitigation measures implemented per RRC and USGS guidance.",
        reasoning_framework="""
        1. Review regional seismicity data and fault mapping.
        2. Model potential for pressure transmission to basement faults.
        3. Limit injection rates and pressures as needed.
        4. Install seismic monitoring if required.
        5. Coordinate with RRC and USGS on risk mitigation.
        """,
        key_factors=[
            "Regional fault mapping",
            "Injection rates and pressures",
            "Seismic monitoring",
            "Regulatory guidance"
        ],
        primary_authority=[
            "RRC Seismicity Protocol",
            "USGS Induced Seismicity Guidance"
        ],
        burden_holder="Operator",
        adversary_position="Seismic risk may be underestimated due to limited subsurface data.",
        counter_arguments=[
            "Conservative operational limits set",
            "Ongoing seismic monitoring"
        ],
        resolution_strategy="Adjust operations and coordinate with regulators.",
        entity_scope="Field, Basin",
        confidence=0.83,
        confidence_zone="Moderate",
        controlling_precedent="RRC Seismicity Protocol 2015"
    ),
    DoctrineBlock(
        topic="NORM Management in Produced Water Operations",
        keywords=["NORM", "naturally occurring radioactive material", "produced water", "management"],
        conclusion_template="NORM in produced water is managed per TCEQ and RRC requirements, with worker and environmental safety ensured.",
        reasoning_framework="""
        1. Screen produced water and residuals for NORM using approved methods.
        2. Segregate and label NORM-containing materials.
        3. Dispose of NORM waste at licensed facilities.
        4. Train personnel in NORM handling and safety.
        5. Maintain records and report as required by TCEQ and RRC.
        """,
        key_factors=[
            "Screening protocol",
            "Waste disposal",
            "Worker safety",
            "Regulatory reporting"
        ],
        primary_authority=[
            "TCEQ 30 TAC 336",
            "RRC NORM Guidance"
        ],
        burden_holder="Operator",
        adversary_position="Improper NORM management may expose workers or environment to risk.",
        counter_arguments=[
            "Personnel trained and certified",
            "Licensed disposal facilities used"
        ],
        resolution_strategy="Periodic audits and regulatory inspection.",
        entity_scope="Facility, Asset",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="TCEQ 30 TAC 336"
    ),
    DoctrineBlock(
        topic="Spill Prevention and Response for Produced Water",
        keywords=["spill prevention", "response", "produced water", "contingency plan"],
        conclusion_template="Spill prevention and response plan is implemented, minimizing risk of environmental impact from produced water releases.",
        reasoning_framework="""
        1. Identify potential spill sources and failure modes.
        2. Install secondary containment and leak detection.
        3. Train personnel in spill response procedures.
        4. Maintain spill kits and response equipment onsite.
        5. Report and remediate spills per RRC and EPA requirements.
        """,
        key_factors=[
            "Containment systems",
            "Personnel training",
            "Response equipment",
            "Regulatory reporting"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "EPA SPCC Rule"
        ],
        burden_holder="Operator",
        adversary_position="Spill response may be delayed or inadequate, leading to environmental damage.",
        counter_arguments=[
            "Drills and training conducted regularly",
            "Automated leak detection systems in place"
        ],
        resolution_strategy="Continuous improvement and regulatory review.",
        entity_scope="Facility, Field",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Rule"
    ),
    DoctrineBlock(
        topic="Produced Water Trucking Safety Compliance",
        keywords=["trucking", "safety", "produced water", "DOT", "compliance"],
        conclusion_template="Produced water trucking operations comply with DOT and RRC safety regulations, minimizing risk of accidents.",
        reasoning_framework="""
        1. Ensure all trucks and drivers are DOT certified.
        2. Conduct regular vehicle inspections and maintenance.
        3. Train drivers in hazardous materials handling and emergency response.
        4. Monitor driver hours and fatigue.
        5. Investigate and report all incidents per regulatory requirements.
        """,
        key_factors=[
            "Driver certification",
            "Vehicle maintenance",
            "Safety training",
            "Incident reporting"
        ],
        primary_authority=[
            "DOT FMCSA Regulations",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Trucking Contractor",
        adversary_position="Non-compliance may result in accidents or regulatory penalties.",
        counter_arguments=[
            "Safety audits conducted",
            "Real-time GPS and ELD monitoring"
        ],
        resolution_strategy="Contractor management and periodic audits.",
        entity_scope="Field, Asset",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOT FMCSA Guidance"
    ),
    DoctrineBlock(
        topic="Disposal Well Plugging and Abandonment",
        keywords=["plugging", "abandonment", "SWD", "well closure", "regulatory"],
        conclusion_template="SWD well at {location} is plugged and abandoned per RRC requirements, with all records submitted.",
        reasoning_framework="""
        1. Submit plugging notice to RRC and obtain approval.
        2. Remove downhole equipment and clean wellbore.
        3. Set cement plugs at required intervals.
        4. Cut and cap casing at surface.
        5. File final plugging report and retain records.
        """,
        key_factors=[
            "Plugging procedure",
            "Regulatory approval",
            "Documentation",
            "Site restoration"
        ],
        primary_authority=[
            "RRC Statewide Rule 14",
            "API RP 51R"
        ],
        burden_holder="Operator",
        adversary_position="Improper plugging may allow fluid migration or environmental risk.",
        counter_arguments=[
            "Plugging witnessed by RRC inspector",
            "Post-plugging pressure test conducted"
        ],
        resolution_strategy="Regulatory oversight and post-plugging monitoring.",
        entity_scope="Well",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RRC Compliance Bulletin 2020-02"
    ),
    DoctrineBlock(
        topic="Disposal Well Surface Facility Design",
        keywords=["surface facility", "design", "SWD", "safety", "compliance"],
        conclusion_template="SWD surface facility is designed to meet RRC and API standards for safety, containment, and operational efficiency.",
        reasoning_framework="""
        1. Design facility layout for safe vehicle and personnel movement.
        2. Install secondary containment for tanks and equipment.
        3. Select materials and equipment rated for produced water service.
        4. Incorporate spill prevention and fire protection systems.
        5. Obtain necessary permits and conduct pre-startup safety review.
        """,
        key_factors=[
            "Facility layout",
            "Containment systems",
            "Equipment selection",
            "Regulatory permits"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "API RP 12R1"
        ],
        burden_holder="Facility Engineer",
        adversary_position="Design may not anticipate all operational hazards.",
        counter_arguments=[
            "HAZOP review conducted",
            "Design reviewed by third-party engineer"
        ],
        resolution_strategy="Periodic safety audits and design updates.",
        entity_scope="Facility",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 12R1"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Integrity Management",
        keywords=["pipeline", "integrity", "produced water", "corrosion", "inspection"],
        conclusion_template="Produced water pipelines are managed for integrity per API and DOT standards, minimizing risk of leaks or failures.",
        reasoning_framework="""
        1. Conduct regular pipeline inspections (ILI, hydrotest, visual).
        2. Monitor for internal and external corrosion.
        3. Implement cathodic protection and chemical inhibition.
        4. Maintain records of inspections, repairs, and incidents.
        5. Respond promptly to leaks or anomalies.
        """,
        key_factors=[
            "Inspection frequency",
            "Corrosion monitoring",
            "Repair documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 1110",
            "DOT PHMSA Regulations"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Corrosion or damage may go undetected between inspections.",
        counter_arguments=[
            "Real-time leak detection systems",
            "Increased inspection frequency in high-risk areas"
        ],
        resolution_strategy="Continuous improvement and technology adoption.",
        entity_scope="Asset, Field",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 1110"
    ),
    DoctrineBlock(
        topic="Water Transfer Pipeline Permitting",
        keywords=["pipeline", "permitting", "water transfer", "ROW", "regulatory"],
        conclusion_template="Water transfer pipeline at {location} is permitted per state and federal requirements, with all ROW secured.",
        reasoning_framework="""
        1. Identify permitting requirements at state, federal, and local levels.
        2. Prepare and submit permit applications with supporting documentation.
        3. Secure ROW agreements from landowners.
        4. Address agency and public comments.
        5. Receive permit approvals before commencing construction.
        """,
        key_factors=[
            "Permitting requirements",
            "ROW acquisition",
            "Public engagement",
            "Documentation"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "US Army Corps of Engineers Section 404"
        ],
        burden_holder="Project Manager",
        adversary_position="Permitting delays may impact project schedule.",
        counter_arguments=[
            "Early engagement with agencies",
            "Contingency planning for delays"
        ],
        resolution_strategy="Proactive stakeholder management.",
        entity_scope="Asset, Field",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="USACE Permit Guidance"
    ),
    DoctrineBlock(
        topic="Produced Water Storage Tank Compliance",
        keywords=["storage tank", "compliance", "produced water", "inspection", "RRC"],
        conclusion_template="Produced water storage tanks at {location} are compliant with RRC and EPA requirements, with inspection records current.",
        reasoning_framework="""
        1. Inspect tanks for integrity, leaks, and overfill protection.
        2. Maintain secondary containment and spill prevention measures.
        3. Document inspections and repairs.
        4. Comply with RRC and EPA SPCC rules.
        5. Train personnel in tank operation and emergency response.
        """,
        key_factors=[
            "Inspection frequency",
            "Containment systems",
            "Repair documentation",
            "Personnel training"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "EPA SPCC Rule"
        ],
        burden_holder="Operator",
        adversary_position="Tank failures may occur between inspections.",
        counter_arguments=[
            "Automated tank level and leak detection",
            "Increased inspection frequency"
        ],
        resolution_strategy="Technology adoption and continuous improvement.",
        entity_scope="Facility",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Rule"
    ),
    DoctrineBlock(
        topic="Produced Water Beneficial Reuse Permitting",
        keywords=["beneficial reuse", "permitting", "produced water", "regulatory"],
        conclusion_template="Produced water beneficial reuse project is permitted per TCEQ and RRC requirements, with all end uses documented.",
        reasoning_framework="""
        1. Identify proposed beneficial reuse applications (e.g., irrigation, dust control).
        2. Assess water quality and treatment needs.
        3. Prepare and submit permit applications to TCEQ and RRC.
        4. Document end users and ensure compliance with permit conditions.
        5. Monitor and report water quality as required.
        """,
        key_factors=[
            "End use documentation",
            "Water quality",
            "Permitting requirements",
            "Monitoring and reporting"
        ],
        primary_authority=[
            "TCEQ Chapter 210",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Project Developer",
        adversary_position="Reuse may not be permitted for all applications or locations.",
        counter_arguments=[
            "End use restrictions documented",
            "Water quality monitoring in place"
        ],
        resolution_strategy="Regulatory engagement and compliance monitoring.",
        entity_scope="Asset, Field",
        confidence=0.86,
        confidence_zone="Moderate",
        controlling_precedent="TCEQ Chapter 210"
    ),
    DoctrineBlock(
        topic="Produced Water Evaporation Pit Regulation",
        keywords=["evaporation pit", "regulation", "produced water", "RRC", "environmental"],
        conclusion_template="Produced water evaporation pit at {location} is permitted and operated per RRC environmental standards.",
        reasoning_framework="""
        1. Submit pit permit application to RRC with design and operational details.
        2. Install liners and leak detection systems.
        3. Monitor pit water levels and integrity.
        4. Prevent unauthorized discharges and wildlife exposure.
        5. Inspect and report per RRC schedule.
        """,
        key_factors=[
            "Pit design and liner integrity",
            "Leak detection",
            "Monitoring and reporting",
            "Wildlife protection"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "EPA NPDES"
        ],
        burden_holder="Operator",
        adversary_position="Evaporation pits may pose environmental risks if not properly managed.",
        counter_arguments=[
            "Liner integrity tested",
            "Regular inspections and reporting"
        ],
        resolution_strategy="Regulatory oversight and corrective action.",
        entity_scope="Facility",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="RRC Statewide Rule 8"
    ),
    DoctrineBlock(
        topic="Produced Water Discharge to Surface Water",
        keywords=["discharge", "surface water", "produced water", "NPDES", "permitting"],
        conclusion_template="Produced water discharge to surface water is permitted under NPDES, with all effluent limits met.",
        reasoning_framework="""
        1. Obtain NPDES permit from EPA or delegated state agency.
        2. Treat produced water to meet effluent limits for TDS, oil, and other parameters.
        3. Monitor discharge quality and flow.
        4. Report exceedances and take corrective action as required.
        5. Maintain records for inspection and audit.
        """,
        key_factors=[
            "Effluent limits",
            "Treatment technology",
            "Monitoring and reporting",
            "Permit conditions"
        ],
        primary_authority=[
            "EPA NPDES",
            "TCEQ Discharge Permitting"
        ],
        burden_holder="Operator",
        adversary_position="Discharge may impact surface water quality or aquatic life.",
        counter_arguments=[
            "Effluent monitoring and reporting in place",
            "Contingency plans for exceedances"
        ],
        resolution_strategy="Regulatory enforcement and adaptive management.",
        entity_scope="Facility, Field",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="EPA NPDES"
    ),
    DoctrineBlock(
        topic="Produced Water Data Management and Security",
        keywords=["data management", "security", "produced water", "compliance", "audit"],
        conclusion_template="Produced water data is managed and secured per company policy and regulatory requirements, ensuring auditability.",
        reasoning_framework="""
        1. Store all produced water data in secure, backed-up systems.
        2. Control access to sensitive data.
        3. Maintain audit trails for data changes.
        4. Comply with RRC electronic reporting requirements.
        5. Train personnel in data management and security best practices.
        """,
        key_factors=[
            "Data storage and backup",
            "Access control",
            "Audit trails",
            "Regulatory compliance"
        ],
        primary_authority=[
            "RRC Electronic Reporting Policy",
            "Operator Data Security Policy"
        ],
        burden_holder="IT/Data Manager",
        adversary_position="Data breaches or loss may compromise compliance or operations.",
        counter_arguments=[
            "Redundant backups and cybersecurity protocols",
            "Periodic data integrity audits"
        ],
        resolution_strategy="Continuous improvement and staff training.",
        entity_scope="Asset, Company",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="RRC Electronic Reporting Policy"
    ),
    DoctrineBlock(
        topic="Produced Water Sampling and Analysis Protocol",
        keywords=["sampling", "analysis", "protocol", "produced water", "QA/QC"],
        conclusion_template="Produced water sampling and analysis are conducted per API and EPA protocols, ensuring data reliability.",
        reasoning_framework="""
        1. Develop and implement a sampling plan covering all relevant locations and frequencies.
        2. Use clean, labeled containers and preserve samples as required.
        3. Analyze samples in accredited laboratories using EPA-approved methods.
        4. Include field blanks, duplicates, and spikes for QA/QC.
        5. Document and review results for anomalies.
        """,
        key_factors=[
            "Sampling plan",
            "Sample preservation",
            "Laboratory accreditation",
            "QA/QC procedures"
        ],
        primary_authority=[
            "API RP 45",
            "EPA Method 300.0"
        ],
        burden_holder="Lab Manager",
        adversary_position="Improper sampling or analysis may yield unreliable data.",
        counter_arguments=[
            "Personnel trained in protocol",
            "QA/QC results reviewed regularly"
        ],
        resolution_strategy="Ongoing training and method audits.",
        entity_scope="Facility, Field",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 45"
    ),
    DoctrineBlock(
        topic="Produced Water Regulatory Audit Preparedness",
        keywords=["regulatory audit", "preparedness", "produced water", "compliance"],
        conclusion_template="Produced water operations are audit-ready, with all records organized and compliance demonstrated.",
        reasoning_framework="""
        1. Maintain organized records for all produced water operations.
        2. Conduct periodic internal audits against RRC and EPA requirements.
        3. Address findings and implement corrective actions.
        4. Train staff in audit procedures and expectations.
        5. Cooperate fully with regulatory auditors.
        """,
        key_factors=[
            "Recordkeeping",
            "Internal audits",
            "Corrective actions",
            "Staff training"
        ],
        primary_authority=[
            "RRC Audit Policy",
            "EPA Audit Policy"
        ],
        burden_holder="Compliance Manager",
        adversary_position="Records may be incomplete or non-compliant, risking penalties.",
        counter_arguments=[
            "Audit checklists and periodic reviews",
            "Corrective actions tracked to closure"
        ],
        resolution_strategy="Continuous improvement and management oversight.",
        entity_scope="Asset, Company",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RRC Audit Policy"
    ),
    DoctrineBlock(
        topic="Produced Water Asset Retirement Obligation (ARO)",
        keywords=["ARO", "asset retirement obligation", "produced water", "financial", "compliance"],
        conclusion_template="ARO for produced water assets is estimated and reported per SEC and FASB requirements.",
        reasoning_framework="""
        1. Identify all produced water assets subject to retirement (SWD wells, pipelines, facilities).
        2. Estimate plugging, abandonment, and site restoration costs.
        3. Discount future costs to present value using appropriate rates.
        4. Record ARO liability in financial statements.
        5. Review and update estimates annually or as conditions change.
        """,
        key_factors=[
            "Asset inventory",
            "Cost estimation",
            "Discount rate",
            "Regulatory requirements"
        ],
        primary_authority=[
            "SEC Regulation S-X",
            "FASB ASC 410"
        ],
        burden_holder="Finance Department",
        adversary_position="ARO estimates may be understated, risking financial misstatement.",
        counter_arguments=[
            "Third-party cost benchmarking",
            "Annual review and update"
        ],
        resolution_strategy="Audit and management review.",
        entity_scope="Company, Asset",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FASB ASC 410"
    ),
    DoctrineBlock(
        topic="Produced Water Emissions Management",
        keywords=["emissions", "management", "produced water", "air quality", "compliance"],
        conclusion_template="Produced water emissions (VOC, H2S) are monitored and controlled per TCEQ and EPA requirements.",
        reasoning_framework="""
        1. Identify emission sources (tanks, treatment units, loading).
        2. Install emission controls (vapor recovery, flares, scrubbers).
        3. Monitor emissions and report as required.
        4. Maintain records and conduct periodic inspections.
        5. Respond to exceedances with corrective action.
        """,
        key_factors=[
            "Emission source identification",
            "Control technology",
            "Monitoring and reporting",
            "Regulatory compliance"
        ],
        primary_authority=[
            "TCEQ 30 TAC 106",
            "EPA Clean Air Act"
        ],
        burden_holder="Operator",
        adversary_position="Uncontrolled emissions may impact air quality and trigger enforcement.",
        counter_arguments=[
            "Vapor recovery and monitoring in place",
            "Periodic compliance audits"
        ],
        resolution_strategy="Continuous improvement and regulatory engagement.",
        entity_scope="Facility, Field",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="TCEQ 30 TAC 106"
    ),
    DoctrineBlock(
        topic="Produced Water Surface Discharge Spill Response",
        keywords=["surface discharge", "spill response", "produced water", "emergency", "environmental"],
        conclusion_template="Surface discharge spill response plan is implemented, minimizing environmental impact and regulatory risk.",
        reasoning_framework="""
        1. Identify potential surface discharge points and failure modes.
        2. Develop and train personnel in spill response procedures.
        3. Maintain spill response equipment and materials onsite.
        4. Notify regulatory agencies and affected stakeholders promptly.
        5. Remediate impacted areas and document response actions.
        """,
        key_factors=[
            "Spill response planning",
            "Personnel training",
            "Equipment readiness",
            "Regulatory notification"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "EPA SPCC Rule"
        ],
        burden_holder="Operator",
        adversary_position="Delayed or inadequate response may result in environmental damage.",
        counter_arguments=[
            "Drills and training conducted regularly",
            "Automated notification systems"
        ],
        resolution_strategy="Continuous improvement and regulatory review.",
        entity_scope="Facility, Field",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Rule"
    ),
    DoctrineBlock(
        topic="Produced Water Ownership and Royalty Allocation",
        keywords=["ownership", "royalty", "produced water", "allocation", "contract"],
        conclusion_template="Produced water ownership and royalty allocation are determined per lease agreements and Texas law.",
        reasoning_framework="""
        1. Review lease agreements for produced water ownership terms.
        2. Apply Texas Natural Resources Code provisions.
        3. Allocate royalties if lease specifies payment on water disposal or reuse.
        4. Document allocation methodology and communicate with royalty owners.
        5. Resolve disputes through negotiation or legal process.
        """,
        key_factors=[
            "Lease terms",
            "State law",
            "Royalty owner communication",
            "Documentation"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Lease Agreement"
        ],
        burden_holder="Land Department",
        adversary_position="Disputes may arise over allocation methodology or contract interpretation.",
        counter_arguments=[
            "Legal review of agreements",
            "Transparent documentation"
        ],
        resolution_strategy="Negotiation and, if necessary, legal resolution.",
        entity_scope="Asset, Company",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Texas Supreme Court, Hlavinka v. HSC Pipeline"
    ),
    DoctrineBlock(
        topic="Produced Water Blending for Injection",
        keywords=["blending", "injection", "produced water", "compatibility", "treatment"],
        conclusion_template="Produced water blending program achieves target compatibility for injection, minimizing scaling and souring risk.",
        reasoning_framework="""
        1. Analyze source water chemistries.
        2. Model blending ratios to achieve target compatibility.
        3. Conduct pilot blending tests and monitor for precipitation.
        4. Adjust treatment as needed and monitor injection performance.
        5. Document blending procedures and results.
        """,
        key_factors=[
            "Source water chemistry",
            "Blending ratios",
            "Scaling/souring indices",
            "Operational monitoring"
        ],
        primary_authority=[
            "API RP 45",
            "SPE 169581"
        ],
        burden_holder="Operations Team",
        adversary_position="Unexpected reactions may occur with changing source water quality.",
        counter_arguments=[
            "Continuous monitoring and adjustment",
            "Rapid response protocols"
        ],
        resolution_strategy="Ongoing testing and adaptive management.",
        entity_scope="Facility, Field",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 169581"
    ),
    DoctrineBlock(
        topic="Produced Water Trucking Contract Management",
        keywords=["trucking", "contract", "produced water", "management", "compliance"],
        conclusion_template="Produced water trucking contracts are managed for compliance, cost, and performance, minimizing operational risk.",
        reasoning_framework="""
        1. Develop contracts specifying safety, compliance, and performance standards.
        2. Monitor contractor performance and compliance with DOT and RRC rules.
        3. Review invoices and resolve discrepancies.
        4. Conduct periodic safety and compliance audits.
        5. Renew or terminate contracts based on performance.
        """,
        key_factors=[
            "Contract terms",
            "Performance monitoring",
            "Compliance audits",
            "Cost control"
        ],
        primary_authority=[
            "DOT FMCSA Regulations",
            "Operator Procurement Policy"
        ],
        burden_holder="Procurement Department",
        adversary_position="Contractors may fail to meet safety or compliance standards.",
        counter_arguments=[
            "Performance metrics and audits",
            "Contractor pre-qualification"
        ],
        resolution_strategy="Enforce contract provisions and replace non-compliant contractors.",
        entity_scope="Asset, Field",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOT FMCSA Guidance"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline ROW Acquisition",
        keywords=["pipeline", "ROW", "acquisition", "produced water", "landowner"],
        conclusion_template="ROW for produced water pipeline is acquired per Texas law, with all landowner agreements executed.",
        reasoning_framework="""
        1. Identify pipeline route and affected landowners.
        2. Negotiate ROW agreements and compensation.
        3. Record agreements and secure title.
        4. Address landowner concerns and regulatory requirements.
        5. Proceed with construction after all ROW secured.
        """,
        key_factors=[
            "Route selection",
            "Landowner negotiation",
            "Title documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Operator Land Policy"
        ],
        burden_holder="Land Department",
        adversary_position="ROW acquisition may be delayed by landowner disputes.",
        counter_arguments=[
            "Early engagement and fair compensation",
            "Legal remedies available"
        ],
        resolution_strategy="Negotiation and, if necessary, legal action.",
        entity_scope="Asset, Field",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Texas Natural Resources Code"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Leak Detection",
        keywords=["pipeline", "leak detection", "produced water", "monitoring", "compliance"],
        conclusion_template="Produced water pipeline leak detection system is operational, enabling rapid response to minimize environmental risk.",
        reasoning_framework="""
        1. Install leak detection systems (pressure, flow, acoustic).
        2. Monitor pipelines continuously and set alarm thresholds.
        3. Train personnel in leak response procedures.
        4. Investigate and document all alarms.
        5. Report leaks to RRC and remediate promptly.
        """,
        key_factors=[
            "Detection technology",
            "Alarm thresholds",
            "Response training",
            "Regulatory reporting"
        ],
        primary_authority=[
            "API RP 1130",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Small leaks may go undetected or response may be delayed.",
        counter_arguments=[
            "System tested regularly",
            "Rapid response protocols"
        ],
        resolution_strategy="Continuous improvement and periodic drills.",
        entity_scope="Asset, Field",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 1130"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Construction QA/QC",
        keywords=["pipeline", "construction", "QA/QC", "produced water", "inspection"],
        conclusion_template="Produced water pipeline construction meets QA/QC standards, ensuring integrity and regulatory compliance.",
        reasoning_framework="""
        1. Develop construction QA/QC plan covering materials, welding, and inspection.
        2. Inspect all welds and joints using NDE methods.
        3. Hydrotest pipeline before commissioning.
        4. Document all inspections and repairs.
        5. Submit records to RRC and retain for audit.
        """,
        key_factors=[
            "QA/QC plan",
            "Inspection methods",
            "Hydrotest results",
            "Documentation"
        ],
        primary_authority=[
            "API 1104",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Construction Manager",
        adversary_position="Construction defects may not be detected without rigorous QA/QC.",
        counter_arguments=[
            "Third-party inspection used",
            "Comprehensive documentation"
        ],
        resolution_strategy="Periodic audits and continuous improvement.",
        entity_scope="Asset, Field",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 1104"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Decommissioning",
        keywords=["pipeline", "decommissioning", "produced water", "abandonment", "regulatory"],
        conclusion_template="Produced water pipeline decommissioned per RRC and DOT requirements, with all records submitted.",
        reasoning_framework="""
        1. Notify RRC and DOT of intent to decommission.
        2. Clean and purge pipeline of all fluids.
        3. Remove or cap pipeline as required.
        4. Restore ROW and document site conditions.
        5. Submit decommissioning report and retain records.
        """,
        key_factors=[
            "Notification",
            "Cleaning and purging",
            "Site restoration",
            "Documentation"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "DOT PHMSA Regulations"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Residual contamination may persist if decommissioning is incomplete.",
        counter_arguments=[
            "Post-decommissioning inspection conducted",
            "Regulatory oversight"
        ],
        resolution_strategy="Regulatory review and corrective action.",
        entity_scope="Asset, Field",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOT PHMSA Guidance"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Operations Training",
        keywords=["pipeline", "operations", "training", "produced water", "compliance"],
        conclusion_template="Produced water pipeline operations personnel are trained per company and regulatory standards, ensuring safe and compliant operations.",
        reasoning_framework="""
        1. Develop training curriculum covering operations, safety, and emergency response.
        2. Conduct initial and periodic refresher training.
        3. Test personnel knowledge and document completion.
        4. Update training for regulatory or operational changes.
        5. Maintain training records for audit.
        """,
        key_factors=[
            "Training curriculum",
            "Frequency",
            "Documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "DOT PHMSA Regulations",
            "Operator Training Policy"
        ],
        burden_holder="Training Manager",
        adversary_position="Untrained personnel may cause operational errors or non-compliance.",
        counter_arguments=[
            "Training tracked and enforced",
            "Periodic knowledge assessments"
        ],
        resolution_strategy="Continuous improvement and management oversight.",
        entity_scope="Asset, Company",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="DOT PHMSA Guidance"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Emergency Response",
        keywords=["pipeline", "emergency response", "produced water", "spill", "safety"],
        conclusion_template="Produced water pipeline emergency response plan is implemented, minimizing risk to personnel and environment.",
        reasoning_framework="""
        1. Develop and maintain emergency response plan for pipeline incidents.
        2. Train personnel and conduct periodic drills.
        3. Coordinate with local emergency responders.
        4. Maintain emergency response equipment and materials.
        5. Review and update plan after incidents or drills.
        """,
        key_factors=[
            "Response plan",
            "Training and drills",
            "Equipment readiness",
            "Coordination with responders"
        ],
        primary_authority=[
            "DOT PHMSA Regulations",
            "RRC Statewide Rule 8"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Delayed or ineffective response may increase risk.",
        counter_arguments=[
            "Drills conducted regularly",
            "Automated notification systems"
        ],
        resolution_strategy="Continuous improvement and regulatory review.",
        entity_scope="Asset, Field",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOT PHMSA Guidance"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Corrosion Control",
        keywords=["pipeline", "corrosion control", "produced water", "cathodic protection", "inhibition"],
        conclusion_template="Produced water pipeline corrosion is controlled per API and DOT standards, minimizing risk of leaks or failures.",
        reasoning_framework="""
        1. Assess pipeline corrosion risk based on materials and environment.
        2. Install cathodic protection and chemical inhibition systems.
        3. Monitor corrosion rates and system performance.
        4. Inspect and maintain corrosion control equipment.
        5. Document all monitoring and maintenance activities.
        """,
        key_factors=[
            "Corrosion risk assessment",
            "Protection systems",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "API RP 651",
            "DOT PHMSA Regulations"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Corrosion may progress undetected between inspections.",
        counter_arguments=[
            "Continuous monitoring systems",
            "Increased inspection frequency"
        ],
        resolution_strategy="Technology adoption and periodic review.",
        entity_scope="Asset, Field",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 651"
    ),
    DoctrineBlock(
        topic="Produced Water Pipeline Regulatory Reporting",
        keywords=["pipeline", "regulatory reporting", "produced water", "compliance", "audit"],
        conclusion_template="Produced water pipeline regulatory reports are submitted accurately and on time, ensuring compliance.",
        reasoning_framework="""
        1. Identify all required reports (construction, operation, incidents).
        2. Collect and validate data for each reporting period.
        3. Submit reports to RRC, DOT, and other agencies as required.
        4. Retain supporting documentation for audit.
        5. Address agency queries or discrepancies promptly.
        """,
        key_factors=[
            "Reporting requirements",
            "Data accuracy",
            "Timely submission",
            "Documentation"
        ],
        primary_authority=[
            "RRC Statewide Rule 8",
            "DOT PHMSA Regulations"
        ],
        burden_holder="Compliance Manager",
        adversary_position="Late or inaccurate reporting may result in penalties.",
        counter_arguments=[
            "Automated data collection and validation",
            "Internal compliance audits"
        ],
        resolution_strategy="Compliance calendar and periodic training.",
        entity_scope="Asset, Company",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RRC Compliance Bulletin"
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