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
        topic="Flowback Equipment Configuration",
        keywords=["flowback", "equipment", "configuration", "separator", "choke", "tank", "pressure"],
        conclusion_template="Optimal flowback equipment configuration is determined by reservoir pressure, expected sand production, and target flow rates.",
        reasoning_framework=(
            "The selection and arrangement of flowback equipment must consider the anticipated wellhead pressure, "
            "the likelihood and volume of proppant flowback, and the operational objectives such as maximizing load recovery "
            "while minimizing formation damage. Separator sizing is dictated by expected liquid and gas volumes, "
            "while choke selection balances pressure control and sand handling. Tanks must be sized for surge capacity, "
            "and sand traps or desanders are included based on proppant risk. The configuration is validated against "
            "industry standards (API RP 13B, SPE guidelines) and historical analogs. Safety and environmental controls "
            "are integrated, including pressure relief and containment. Equipment redundancy is considered for critical operations. "
            "Final configuration is reviewed by the production engineering team and approved by the site supervisor."
        ),
        key_factors=[
            "Reservoir pressure",
            "Expected sand production",
            "Target flow rates",
            "Separator sizing",
            "Choke selection",
            "Tank capacity",
            "Safety controls",
            "Environmental containment"
        ],
        primary_authority=[
            "API RP 13B",
            "SPE Flowback Guidelines",
            "Company Engineering Standards"
        ],
        burden_holder="Production Engineering Team",
        adversary_position="Cost minimization may lead to undersized equipment and operational risks.",
        counter_arguments=[
            "Oversizing increases capital costs and footprint.",
            "Undersizing risks operational bottlenecks and safety incidents."
        ],
        resolution_strategy="Risk-based sizing with cost-benefit analysis and peer review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B Section 4.2"
    ),
    DoctrineBlock(
        topic="Choke Management Strategy - Aggressive vs Conservative",
        keywords=["choke", "management", "strategy", "aggressive", "conservative", "pressure", "flow rate"],
        conclusion_template="Choke management should begin conservatively and transition to aggressive as sand production stabilizes.",
        reasoning_framework=(
            "Choke management during flowback is a critical determinant of both load recovery efficiency and formation integrity. "
            "An aggressive choke strategy accelerates load recovery and potentially increases early production rates, "
            "but risks excessive proppant flowback and formation damage. A conservative approach reduces these risks but may delay cleanup. "
            "The optimal strategy is to start with conservative choke settings, monitoring sand production and pressure response, "
            "and incrementally open the choke as sand rates decline. Decision points are based on real-time sand trap readings, "
            "pressure transients, and fluid composition. The strategy is documented in the flowback plan and reviewed daily. "
            "Exceptions are made for wells with low proppant risk or urgent production targets, subject to supervisor approval."
        ),
        key_factors=[
            "Sand production rate",
            "Pressure response",
            "Load recovery targets",
            "Formation sensitivity",
            "Operational urgency"
        ],
        primary_authority=[
            "SPE 162808",
            "Company Flowback Procedures"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Aggressive choke opening maximizes early production but increases sand risk.",
        counter_arguments=[
            "Conservative approach delays production and increases operational costs.",
            "Aggressive approach may cause irreversible formation damage."
        ],
        resolution_strategy="Incremental choke adjustments based on real-time monitoring and risk assessment.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 162808"
    ),
    DoctrineBlock(
        topic="Flowback Data Acquisition and Monitoring",
        keywords=["data", "acquisition", "monitoring", "flowback", "real-time", "pressure", "sand", "water", "gas"],
        conclusion_template="Continuous, real-time data acquisition is mandatory for flowback operations to enable proactive management.",
        reasoning_framework=(
            "Effective flowback management relies on comprehensive data acquisition, including real-time measurements of pressure, "
            "temperature, sand production, fluid rates, and gas composition. Data is collected via digital sensors and manual readings, "
            "transmitted to the central control system, and archived for analysis. Data integrity is ensured through calibration and redundancy. "
            "Monitoring protocols require hourly reviews and immediate action on anomalies. Data is used to adjust choke settings, "
            "optimize load recovery, and prevent equipment overload. Historical data informs future operations and regulatory reporting. "
            "Data acquisition standards follow API RP 13B and company digitalization policies. Data privacy and cybersecurity are maintained."
        ),
        key_factors=[
            "Sensor calibration",
            "Data integrity",
            "Real-time transmission",
            "Anomaly detection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 13B",
            "Company Digitalization Policy"
        ],
        burden_holder="Flowback Data Technician",
        adversary_position="Manual data acquisition is sufficient and less costly.",
        counter_arguments=[
            "Manual readings are prone to error and delay.",
            "Real-time data enables proactive risk mitigation."
        ],
        resolution_strategy="Mandatory real-time digital acquisition with manual backup and regular audits.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API RP 13B Section 6.1"
    ),
    DoctrineBlock(
        topic="Load Recovery Calculations and Optimization",
        keywords=["load recovery", "calculation", "optimization", "flowback", "water", "frac fluid", "efficiency"],
        conclusion_template="Load recovery is calculated as the ratio of recovered fluid to injected frac fluid and optimized for speed and completeness.",
        reasoning_framework=(
            "Load recovery is a key metric in flowback operations, representing the percentage of injected fracturing fluid recovered. "
            "Calculation involves accurate measurement of injected volumes and recovered fluids, adjusted for formation water and gas. "
            "Optimization targets rapid recovery without inducing formation damage or excessive proppant flowback. "
            "Recovery curves are plotted daily, and deviations trigger operational reviews. Optimization strategies include choke adjustments, "
            "chemical additives, and temperature management. Load recovery targets are set based on reservoir characteristics and historical analogs. "
            "Results are benchmarked against industry standards and regulatory requirements."
        ),
        key_factors=[
            "Injected frac fluid volume",
            "Recovered fluid volume",
            "Formation water contribution",
            "Recovery rate",
            "Operational adjustments"
        ],
        primary_authority=[
            "SPE 187159",
            "Company Flowback Optimization Guidelines"
        ],
        burden_holder="Flowback Engineer",
        adversary_position="Maximizing load recovery speed increases risk of formation damage.",
        counter_arguments=[
            "Slower recovery reduces operational efficiency.",
            "Rapid recovery may compromise well integrity."
        ],
        resolution_strategy="Balanced optimization using real-time data and risk assessment.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 187159"
    ),
    DoctrineBlock(
        topic="Proppant Flowback Prevention and Management",
        keywords=["proppant", "flowback", "prevention", "management", "sand", "trap", "screen", "choke"],
        conclusion_template="Proppant flowback is prevented by conservative choke management, sand traps, and chemical stabilizers.",
        reasoning_framework=(
            "Proppant flowback poses operational and environmental risks, including equipment damage and formation impairment. "
            "Prevention strategies include conservative choke management, installation of sand traps and screens, and use of chemical stabilizers. "
            "Sand production is monitored in real-time, and thresholds trigger operational adjustments. Sand trap efficiency is validated weekly. "
            "Chemical stabilizers are selected based on reservoir mineralogy and injected during flowback. Equipment is inspected daily for sand accumulation. "
            "Proppant flowback incidents are documented and root cause analysis performed. Management protocols follow SPE 162808 and company standards."
        ),
        key_factors=[
            "Choke settings",
            "Sand trap efficiency",
            "Chemical stabilizer selection",
            "Real-time monitoring",
            "Incident documentation"
        ],
        primary_authority=[
            "SPE 162808",
            "Company Sand Management Policy"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Aggressive flowback increases early production but risks sand overload.",
        counter_arguments=[
            "Conservative approach delays production.",
            "Chemical stabilizers increase operational costs."
        ],
        resolution_strategy="Integrated prevention using equipment, operational controls, and chemical additives.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 162808 Section 5.3"
    ),
    DoctrineBlock(
        topic="Flowback Water Quality and Chemistry",
        keywords=["water quality", "chemistry", "flowback", "analysis", "salinity", "TDS", "scaling", "corrosion"],
        conclusion_template="Flowback water quality is monitored for salinity, TDS, scaling, and corrosion risk, guiding disposal and recycling.",
        reasoning_framework=(
            "Flowback water quality is assessed via regular laboratory analysis, measuring salinity, total dissolved solids (TDS), "
            "scaling potential, and corrosion risk. Results inform water disposal, recycling, and treatment strategies. "
            "Scaling and corrosion inhibitors are dosed based on water chemistry. Water samples are collected daily and analyzed per EPA and company standards. "
            "Water quality trends are tracked to identify formation changes and operational impacts. Disposal and recycling plans are adjusted based on quality. "
            "Compliance with environmental regulations is mandatory. Data is archived for regulatory reporting and future planning."
        ),
        key_factors=[
            "Salinity",
            "TDS",
            "Scaling potential",
            "Corrosion risk",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EPA Water Quality Standards",
            "Company Water Management Policy"
        ],
        burden_holder="Water Quality Technician",
        adversary_position="Water quality monitoring increases operational costs.",
        counter_arguments=[
            "Poor water quality risks environmental violations.",
            "Inadequate monitoring leads to scaling and corrosion incidents."
        ],
        resolution_strategy="Mandatory daily sampling and analysis with automated dosing controls.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="EPA Water Quality Standards Section 3"
    ),
    DoctrineBlock(
        topic="Flare Operations and EPA Methane Regulations",
        keywords=["flare", "operations", "methane", "EPA", "regulations", "emissions", "compliance"],
        conclusion_template="Flare operations must comply with EPA methane regulations, minimizing emissions and documenting all events.",
        reasoning_framework=(
            "Flare operations during flowback are governed by EPA methane regulations, requiring minimization of emissions and thorough documentation. "
            "Flare efficiency is monitored via combustion analysis and infrared cameras. All flare events are logged with time, duration, and emission estimates. "
            "Operational adjustments are made to maximize combustion efficiency and minimize methane release. Flare stack inspections are conducted weekly. "
            "Non-compliance incidents are reported immediately and corrective actions implemented. Flare operations are reviewed monthly for regulatory compliance. "
            "Training is provided to all personnel on EPA requirements and company environmental policies."
        ),
        key_factors=[
            "Flare efficiency",
            "Emission monitoring",
            "Documentation",
            "Regulatory compliance",
            "Personnel training"
        ],
        primary_authority=[
            "EPA Methane Regulations",
            "Company Environmental Policy"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Flare minimization increases operational complexity and costs.",
        counter_arguments=[
            "Non-compliance risks regulatory penalties.",
            "Efficient flare operations reduce environmental impact."
        ],
        resolution_strategy="Automated emission monitoring and documentation with regular compliance audits.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Methane Regulations Section 7"
    ),
    DoctrineBlock(
        topic="Water Disposal and Recycling Planning",
        keywords=["water", "disposal", "recycling", "planning", "flowback", "environmental", "EPA", "permits"],
        conclusion_template="Water disposal and recycling plans must comply with EPA permits and maximize recycling opportunities.",
        reasoning_framework=(
            "Water disposal and recycling are planned based on flowback water quality, regulatory permits, and operational needs. "
            "Disposal routes include injection wells, surface discharge, and third-party treatment, each requiring EPA permits and documentation. "
            "Recycling is prioritized where feasible, using on-site or off-site treatment facilities. Water volumes and quality are tracked daily. "
            "Plans are reviewed quarterly and adjusted for operational changes and regulatory updates. Environmental impact assessments are conducted annually. "
            "All disposal and recycling activities are documented for regulatory reporting."
        ),
        key_factors=[
            "Water quality",
            "Disposal routes",
            "Recycling capacity",
            "EPA permits",
            "Documentation"
        ],
        primary_authority=[
            "EPA Disposal Permits",
            "Company Water Management Policy"
        ],
        burden_holder="Water Management Coordinator",
        adversary_position="Disposal is simpler and less costly than recycling.",
        counter_arguments=[
            "Recycling reduces environmental impact and water sourcing costs.",
            "Disposal risks regulatory violations and public scrutiny."
        ],
        resolution_strategy="Maximize recycling within permit limits and document all disposal activities.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA Disposal Permits Section 2"
    ),
    DoctrineBlock(
        topic="Initial Production (IP) Rate Determination",
        keywords=["initial production", "IP rate", "determination", "flowback", "measurement", "forecast", "reservoir"],
        conclusion_template="IP rate is determined from stabilized flowback rates, adjusted for water and gas, and validated against reservoir forecasts.",
        reasoning_framework=(
            "Initial Production (IP) rate is a critical metric for well performance, determined from stabilized flowback rates. "
            "Measurement includes oil, water, and gas rates, adjusted for water cut and gas-oil ratio. IP rate is compared to reservoir forecasts and analog wells. "
            "Data is collected over a minimum of 48 hours post-stabilization. Deviations from forecast trigger technical review. "
            "IP rate is documented in the well completion report and used for production planning. Measurement protocols follow API standards and company guidelines."
        ),
        key_factors=[
            "Stabilized flowback rate",
            "Water cut",
            "Gas-oil ratio",
            "Reservoir forecast",
            "Measurement protocol"
        ],
        primary_authority=[
            "API Production Measurement Standards",
            "Company Production Planning Policy"
        ],
        burden_holder="Production Engineer",
        adversary_position="Shorter measurement periods increase reporting speed but reduce accuracy.",
        counter_arguments=[
            "Longer measurement periods delay production planning.",
            "Shorter periods risk inaccurate IP rate determination."
        ],
        resolution_strategy="Minimum 48-hour stabilized measurement with technical review of deviations.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API Production Measurement Standards Section 5"
    ),
    DoctrineBlock(
        topic="Surfactant-Assisted Flowback",
        keywords=["surfactant", "flowback", "assisted", "chemical", "load recovery", "formation damage"],
        conclusion_template="Surfactant-assisted flowback is used to enhance load recovery and minimize formation damage, subject to reservoir compatibility.",
        reasoning_framework=(
            "Surfactant-assisted flowback involves injecting surfactants during flowback to reduce interfacial tension, enhance load recovery, and minimize formation damage. "
            "Surfactant selection is based on reservoir mineralogy and compatibility testing. Dosage is optimized for effectiveness and cost. "
            "Results are monitored via recovery curves and water chemistry analysis. Surfactant use is documented in the flowback plan and reviewed post-operation. "
            "Risks include chemical incompatibility and environmental impact. Surfactant-assisted flowback follows SPE 187159 and company chemical management policy."
        ),
        key_factors=[
            "Surfactant selection",
            "Dosage optimization",
            "Reservoir compatibility",
            "Recovery curve analysis",
            "Environmental impact"
        ],
        primary_authority=[
            "SPE 187159",
            "Company Chemical Management Policy"
        ],
        burden_holder="Flowback Engineer",
        adversary_position="Surfactant use increases operational costs and environmental risks.",
        counter_arguments=[
            "Surfactant enhances recovery and reduces formation damage.",
            "Chemical risks are mitigated by compatibility testing."
        ],
        resolution_strategy="Surfactant use subject to compatibility testing and environmental review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 187159 Section 4"
    ),
    DoctrineBlock(
        topic="Nitrogen-Assisted Flowback",
        keywords=["nitrogen", "assisted", "flowback", "gas", "load recovery", "pressure", "formation damage"],
        conclusion_template="Nitrogen-assisted flowback is used to accelerate load recovery in low-pressure wells, with careful monitoring for formation damage.",
        reasoning_framework=(
            "Nitrogen-assisted flowback involves injecting nitrogen gas to increase wellbore pressure and accelerate load recovery, particularly in low-pressure reservoirs. "
            "Nitrogen injection rates are calculated based on reservoir pressure and fluid volumes. Risks include formation damage, gas breakthrough, and operational complexity. "
            "Nitrogen use is monitored via pressure transients and recovery curves. Safety protocols are enforced for gas handling. "
            "Nitrogen-assisted flowback is documented in the flowback plan and reviewed post-operation. Use follows SPE 187159 and company gas management policy."
        ),
        key_factors=[
            "Reservoir pressure",
            "Nitrogen injection rate",
            "Load recovery acceleration",
            "Formation damage risk",
            "Safety protocols"
        ],
        primary_authority=[
            "SPE 187159",
            "Company Gas Management Policy"
        ],
        burden_holder="Flowback Engineer",
        adversary_position="Nitrogen use increases operational complexity and formation damage risk.",
        counter_arguments=[
            "Nitrogen accelerates recovery in low-pressure wells.",
            "Risks are mitigated by careful monitoring and safety protocols."
        ],
        resolution_strategy="Nitrogen use subject to reservoir evaluation and safety review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 187159 Section 5"
    ),
    DoctrineBlock(
        topic="Formation Damage Prevention During Flowback",
        keywords=["formation damage", "prevention", "flowback", "pressure", "choke", "chemical", "proppant"],
        conclusion_template="Formation damage is prevented by conservative choke management, chemical additives, and real-time monitoring.",
        reasoning_framework=(
            "Formation damage during flowback is minimized by maintaining conservative choke settings, using chemical additives, and monitoring pressure transients. "
            "Damage mechanisms include proppant flowback, water invasion, and scaling. Prevention strategies are documented in the flowback plan and reviewed daily. "
            "Chemical additives are selected based on reservoir mineralogy and injected as needed. Real-time monitoring enables rapid response to anomalies. "
            "Formation damage incidents are documented and root cause analysis performed. Prevention protocols follow SPE 162808 and company standards."
        ),
        key_factors=[
            "Choke management",
            "Chemical additive selection",
            "Pressure monitoring",
            "Incident documentation",
            "Root cause analysis"
        ],
        primary_authority=[
            "SPE 162808",
            "Company Formation Damage Prevention Policy"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Aggressive flowback increases production but risks formation damage.",
        counter_arguments=[
            "Conservative approach delays production.",
            "Chemical additives increase operational costs."
        ],
        resolution_strategy="Integrated prevention using operational controls and chemical additives.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 162808 Section 6"
    ),
    DoctrineBlock(
        topic="Separator Sizing for Flowback Operations",
        keywords=["separator", "sizing", "flowback", "equipment", "liquid", "gas", "capacity"],
        conclusion_template="Separator sizing is based on expected liquid and gas volumes, with safety margins for surge events.",
        reasoning_framework=(
            "Separator sizing is determined by expected liquid and gas volumes during flowback, with safety margins for surge events. "
            "Sizing calculations follow API RP 13B and company engineering standards. Separator performance is validated via historical analogs and simulation. "
            "Oversized separators increase capital costs, while undersized units risk operational bottlenecks and safety incidents. "
            "Sizing decisions are documented and reviewed by the engineering team. Separator inspections are conducted weekly during flowback."
        ),
        key_factors=[
            "Expected liquid volume",
            "Expected gas volume",
            "Safety margin",
            "Historical analogs",
            "Engineering standards"
        ],
        primary_authority=[
            "API RP 13B",
            "Company Engineering Standards"
        ],
        burden_holder="Production Engineering Team",
        adversary_position="Oversizing increases costs; undersizing risks operational failures.",
        counter_arguments=[
            "Safety margins are essential for surge events.",
            "Cost optimization must not compromise safety."
        ],
        resolution_strategy="Risk-based sizing with peer review and historical validation.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 13B Section 4.2"
    ),
    DoctrineBlock(
        topic="Sand Trap Efficiency Validation",
        keywords=["sand trap", "efficiency", "validation", "flowback", "proppant", "equipment"],
        conclusion_template="Sand trap efficiency is validated weekly via sand volume measurement and operational review.",
        reasoning_framework=(
            "Sand trap efficiency is critical for proppant management during flowback. Weekly validation involves measuring trapped sand volumes, "
            "comparing to expected production, and reviewing operational performance. Inefficiencies trigger maintenance or equipment upgrades. "
            "Validation protocols follow SPE 162808 and company sand management policy. Results are documented for regulatory and operational review."
        ),
        key_factors=[
            "Sand volume measurement",
            "Expected proppant production",
            "Operational review",
            "Maintenance triggers",
            "Documentation"
        ],
        primary_authority=[
            "SPE 162808",
            "Company Sand Management Policy"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Weekly validation increases operational workload.",
        counter_arguments=[
            "Efficient sand traps prevent equipment damage.",
            "Validation ensures regulatory compliance."
        ],
        resolution_strategy="Mandatory weekly validation with maintenance triggers for inefficiency.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 162808 Section 5.4"
    ),
    DoctrineBlock(
        topic="Real-Time Pressure Monitoring Protocol",
        keywords=["pressure", "monitoring", "real-time", "protocol", "flowback", "safety"],
        conclusion_template="Real-time pressure monitoring is mandatory during flowback, with automated alarms for threshold breaches.",
        reasoning_framework=(
            "Real-time pressure monitoring is essential for flowback safety and operational control. Automated sensors transmit data to the central control system, "
            "with alarms set for threshold breaches. Manual readings are taken hourly for validation. Pressure anomalies trigger immediate operational review and corrective action. "
            "Monitoring protocols follow API RP 13B and company safety standards. Data is archived for regulatory and operational review."
        ),
        key_factors=[
            "Sensor calibration",
            "Automated alarms",
            "Manual validation",
            "Threshold setting",
            "Corrective action"
        ],
        primary_authority=[
            "API RP 13B",
            "Company Safety Standards"
        ],
        burden_holder="Flowback Data Technician",
        adversary_position="Manual monitoring is sufficient and less costly.",
        counter_arguments=[
            "Automated monitoring enables rapid response.",
            "Manual readings are prone to error."
        ],
        resolution_strategy="Mandatory real-time monitoring with manual backup and regular audits.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API RP 13B Section 6.1"
    ),
    DoctrineBlock(
        topic="Flowback Water Sampling Frequency",
        keywords=["water", "sampling", "frequency", "flowback", "quality", "chemistry"],
        conclusion_template="Flowback water sampling is conducted daily, with additional sampling after operational changes.",
        reasoning_framework=(
            "Daily flowback water sampling ensures accurate assessment of water quality and chemistry. Additional samples are taken after operational changes, "
            "such as choke adjustments or chemical injections. Sampling protocols follow EPA standards and company water management policy. "
            "Results inform disposal and recycling decisions. Sampling frequency is documented and reviewed monthly."
        ),
        key_factors=[
            "Daily sampling",
            "Operational change triggers",
            "EPA standards",
            "Documentation",
            "Review frequency"
        ],
        primary_authority=[
            "EPA Water Quality Standards",
            "Company Water Management Policy"
        ],
        burden_holder="Water Quality Technician",
        adversary_position="Daily sampling increases operational costs.",
        counter_arguments=[
            "Frequent sampling ensures accurate water quality assessment.",
            "Inadequate sampling risks environmental violations."
        ],
        resolution_strategy="Mandatory daily sampling with additional samples after operational changes.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="EPA Water Quality Standards Section 3.2"
    ),
    DoctrineBlock(
        topic="Flowback Data Archival and Security",
        keywords=["data", "archival", "security", "flowback", "monitoring", "cybersecurity"],
        conclusion_template="Flowback data is archived digitally with cybersecurity controls and regular audits.",
        reasoning_framework=(
            "Flowback data is archived digitally, with cybersecurity controls to prevent unauthorized access and data loss. "
            "Data is backed up daily and stored in secure company servers. Access is restricted to authorized personnel. "
            "Regular audits are conducted to ensure data integrity and compliance with company digitalization policy. "
            "Data archival protocols follow API RP 13B and company cybersecurity standards."
        ),
        key_factors=[
            "Digital archival",
            "Cybersecurity controls",
            "Daily backup",
            "Access restriction",
            "Audit frequency"
        ],
        primary_authority=[
            "API RP 13B",
            "Company Cybersecurity Standards"
        ],
        burden_holder="Flowback Data Technician",
        adversary_position="Manual archival is simpler and less costly.",
        counter_arguments=[
            "Digital archival ensures data integrity and security.",
            "Manual methods risk data loss and unauthorized access."
        ],
        resolution_strategy="Mandatory digital archival with cybersecurity controls and regular audits.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Company Cybersecurity Standards Section 2"
    ),
    DoctrineBlock(
        topic="Choke Adjustment Decision Criteria",
        keywords=["choke", "adjustment", "decision", "criteria", "flowback", "sand", "pressure"],
        conclusion_template="Choke adjustments are made based on sand production, pressure response, and load recovery targets.",
        reasoning_framework=(
            "Choke adjustments during flowback are guided by sand production rates, pressure response, and load recovery targets. "
            "Real-time monitoring informs decision points, with incremental adjustments to balance recovery and formation integrity. "
            "Criteria are documented in the flowback plan and reviewed daily. Exceptions are made for urgent operational needs, subject to supervisor approval."
        ),
        key_factors=[
            "Sand production rate",
            "Pressure response",
            "Load recovery targets",
            "Operational urgency",
            "Documentation"
        ],
        primary_authority=[
            "SPE 162808",
            "Company Flowback Procedures"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Aggressive adjustments maximize production but risk sand overload.",
        counter_arguments=[
            "Conservative adjustments delay recovery.",
            "Aggressive adjustments risk formation damage."
        ],
        resolution_strategy="Incremental adjustments based on real-time monitoring and risk assessment.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 162808 Section 4"
    ),
    DoctrineBlock(
        topic="Flowback Incident Documentation Protocol",
        keywords=["incident", "documentation", "protocol", "flowback", "safety", "regulatory"],
        conclusion_template="All flowback incidents are documented within 24 hours, including root cause analysis and corrective actions.",
        reasoning_framework=(
            "Flowback incidents, including equipment failures, sand overload, and environmental releases, are documented within 24 hours. "
            "Documentation includes incident description, root cause analysis, corrective actions, and regulatory reporting. "
            "Protocols follow company safety standards and regulatory requirements. Incident logs are reviewed monthly for trend analysis and prevention planning."
        ),
        key_factors=[
            "Incident description",
            "Root cause analysis",
            "Corrective actions",
            "Regulatory reporting",
            "Review frequency"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Reporting Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Incident documentation increases operational workload.",
        counter_arguments=[
            "Documentation enables trend analysis and prevention.",
            "Regulatory compliance requires timely reporting."
        ],
        resolution_strategy="Mandatory incident documentation within 24 hours and monthly review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 8"
    ),
    DoctrineBlock(
        topic="Chemical Additive Selection for Flowback",
        keywords=["chemical", "additive", "selection", "flowback", "compatibility", "formation", "environmental"],
        conclusion_template="Chemical additives are selected based on reservoir compatibility, effectiveness, and environmental impact.",
        reasoning_framework=(
            "Chemical additive selection for flowback is based on reservoir mineralogy, compatibility testing, effectiveness, and environmental impact. "
            "Additives are reviewed by the engineering team and approved by the environmental compliance officer. "
            "Selection protocols follow SPE 187159 and company chemical management policy. Additive use is documented in the flowback plan and reviewed post-operation."
        ),
        key_factors=[
            "Reservoir mineralogy",
            "Compatibility testing",
            "Effectiveness",
            "Environmental impact",
            "Approval process"
        ],
        primary_authority=[
            "SPE 187159",
            "Company Chemical Management Policy"
        ],
        burden_holder="Flowback Engineer",
        adversary_position="Additive selection increases operational complexity and costs.",
        counter_arguments=[
            "Effective additives enhance recovery and prevent damage.",
            "Environmental risks are mitigated by compatibility testing."
        ],
        resolution_strategy="Additive selection subject to compatibility testing and environmental review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 187159 Section 3"
    ),
    DoctrineBlock(
        topic="Flowback Equipment Inspection Frequency",
        keywords=["equipment", "inspection", "frequency", "flowback", "maintenance", "safety"],
        conclusion_template="Flowback equipment is inspected daily, with additional inspections after operational incidents.",
        reasoning_framework=(
            "Daily inspection of flowback equipment ensures operational integrity and safety. Additional inspections are conducted after operational incidents, "
            "such as sand overload or pressure anomalies. Inspection protocols follow company safety standards and regulatory requirements. "
            "Results are documented and reviewed weekly for maintenance planning."
        ),
        key_factors=[
            "Daily inspection",
            "Incident-triggered inspection",
            "Safety standards",
            "Documentation",
            "Review frequency"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Daily inspection increases operational workload.",
        counter_arguments=[
            "Frequent inspection prevents equipment failures.",
            "Regulatory compliance requires documentation."
        ],
        resolution_strategy="Mandatory daily inspection with additional checks after incidents.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 6"
    ),
    DoctrineBlock(
        topic="Flowback Operational Review Frequency",
        keywords=["operational", "review", "frequency", "flowback", "performance", "planning"],
        conclusion_template="Flowback operations are reviewed daily, with monthly performance analysis and planning updates.",
        reasoning_framework=(
            "Daily operational review ensures proactive management of flowback operations. Monthly performance analysis informs planning updates and optimization. "
            "Review protocols follow company operational standards. Results are documented and used for trend analysis and future planning."
        ),
        key_factors=[
            "Daily review",
            "Monthly performance analysis",
            "Documentation",
            "Planning updates",
            "Trend analysis"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Frequent reviews increase operational workload.",
        counter_arguments=[
            "Regular review enables proactive management.",
            "Performance analysis informs optimization."
        ],
        resolution_strategy="Mandatory daily review with monthly performance analysis.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Operational Standards Section 4"
    ),
    DoctrineBlock(
        topic="Flowback Safety Training Requirements",
        keywords=["safety", "training", "requirements", "flowback", "personnel", "compliance"],
        conclusion_template="All flowback personnel must complete safety training annually, with refresher courses after incidents.",
        reasoning_framework=(
            "Annual safety training is mandatory for all flowback personnel, covering operational hazards, emergency response, and regulatory compliance. "
            "Refresher courses are required after incidents or regulatory updates. Training protocols follow company safety standards and regulatory requirements. "
            "Training completion is documented and reviewed quarterly."
        ),
        key_factors=[
            "Annual training",
            "Refresher courses",
            "Operational hazards",
            "Emergency response",
            "Documentation"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Training increases operational costs and downtime.",
        counter_arguments=[
            "Training prevents incidents and ensures compliance.",
            "Regulatory requirements mandate training."
        ],
        resolution_strategy="Mandatory annual training with refresher courses after incidents.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 2"
    ),
    DoctrineBlock(
        topic="Flowback Regulatory Compliance Documentation",
        keywords=["regulatory", "compliance", "documentation", "flowback", "EPA", "reporting"],
        conclusion_template="Regulatory compliance documentation is maintained daily, with monthly reporting to EPA and company management.",
        reasoning_framework=(
            "Daily documentation of regulatory compliance ensures accurate reporting and audit readiness. Monthly reports are submitted to EPA and company management. "
            "Documentation protocols follow EPA requirements and company standards. Compliance logs are reviewed quarterly for audit preparation."
        ),
        key_factors=[
            "Daily documentation",
            "Monthly reporting",
            "EPA requirements",
            "Audit preparation",
            "Review frequency"
        ],
        primary_authority=[
            "EPA Reporting Requirements",
            "Company Compliance Standards"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Daily documentation increases operational workload.",
        counter_arguments=[
            "Accurate documentation ensures audit readiness.",
            "Regulatory requirements mandate reporting."
        ],
        resolution_strategy="Mandatory daily documentation with monthly reporting.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="EPA Reporting Requirements Section 5"
    ),
    DoctrineBlock(
        topic="Flowback Emergency Response Planning",
        keywords=["emergency", "response", "planning", "flowback", "safety", "incident"],
        conclusion_template="Emergency response plans are maintained for all flowback operations, with annual drills and incident reviews.",
        reasoning_framework=(
            "Emergency response plans are developed for all flowback operations, covering equipment failures, environmental releases, and personnel injuries. "
            "Annual drills are conducted to ensure readiness. Incident reviews inform plan updates. Plans follow company safety standards and regulatory requirements. "
            "Documentation is maintained for regulatory and operational review."
        ),
        key_factors=[
            "Emergency response plan",
            "Annual drills",
            "Incident review",
            "Plan updates",
            "Documentation"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Emergency planning increases operational workload.",
        counter_arguments=[
            "Planning ensures readiness and compliance.",
            "Drills prevent incident escalation."
        ],
        resolution_strategy="Mandatory emergency response planning with annual drills.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 10"
    ),
    DoctrineBlock(
        topic="Flowback Environmental Impact Assessment",
        keywords=["environmental", "impact", "assessment", "flowback", "EPA", "review"],
        conclusion_template="Annual environmental impact assessments are conducted for flowback operations, with quarterly reviews for compliance.",
        reasoning_framework=(
            "Annual environmental impact assessments evaluate flowback operations for regulatory compliance and operational impact. "
            "Quarterly reviews ensure ongoing compliance and inform operational adjustments. Assessment protocols follow EPA requirements and company environmental policy. "
            "Results are documented and used for planning and regulatory reporting."
        ),
        key_factors=[
            "Annual assessment",
            "Quarterly review",
            "EPA requirements",
            "Operational adjustments",
            "Documentation"
        ],
        primary_authority=[
            "EPA Environmental Policy",
            "Company Environmental Standards"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Assessment increases operational workload and costs.",
        counter_arguments=[
            "Assessment ensures compliance and informs planning.",
            "Regulatory requirements mandate assessment."
        ],
        resolution_strategy="Mandatory annual assessment with quarterly reviews.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA Environmental Policy Section 4"
    ),
    DoctrineBlock(
        topic="Flowback Equipment Redundancy Planning",
        keywords=["equipment", "redundancy", "planning", "flowback", "safety", "operational"],
        conclusion_template="Critical flowback equipment is duplicated for redundancy, with operational protocols for failure scenarios.",
        reasoning_framework=(
            "Redundancy planning ensures operational continuity during flowback. Critical equipment, including separators, sand traps, and pumps, are duplicated. "
            "Operational protocols are developed for failure scenarios. Redundancy planning follows company engineering standards and safety requirements. "
            "Plans are documented and reviewed quarterly for operational readiness."
        ),
        key_factors=[
            "Critical equipment identification",
            "Duplication",
            "Failure scenario protocols",
            "Documentation",
            "Review frequency"
        ],
        primary_authority=[
            "Company Engineering Standards",
            "Company Safety Requirements"
        ],
        burden_holder="Production Engineering Team",
        adversary_position="Redundancy increases capital costs.",
        counter_arguments=[
            "Redundancy ensures operational continuity and safety.",
            "Failure scenarios risk operational shutdown."
        ],
        resolution_strategy="Mandatory redundancy for critical equipment with quarterly review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Engineering Standards Section 7"
    ),
    DoctrineBlock(
        topic="Flowback Operational Cost Optimization",
        keywords=["operational", "cost", "optimization", "flowback", "efficiency", "planning"],
        conclusion_template="Operational costs are optimized by balancing equipment sizing, chemical use, and personnel allocation.",
        reasoning_framework=(
            "Cost optimization in flowback operations involves balancing equipment sizing, chemical use, and personnel allocation. "
            "Operational efficiency is prioritized without compromising safety or regulatory compliance. Cost reviews are conducted monthly and inform planning updates. "
            "Optimization protocols follow company operational standards and financial guidelines."
        ),
        key_factors=[
            "Equipment sizing",
            "Chemical use",
            "Personnel allocation",
            "Operational efficiency",
            "Cost review"
        ],
        primary_authority=[
            "Company Operational Standards",
            "Company Financial Guidelines"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Cost minimization risks operational integrity.",
        counter_arguments=[
            "Optimization ensures efficiency and compliance.",
            "Cost minimization must not compromise safety."
        ],
        resolution_strategy="Monthly cost review with planning updates.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Company Financial Guidelines Section 3"
    ),
    DoctrineBlock(
        topic="Flowback Operational Communication Protocol",
        keywords=["operational", "communication", "protocol", "flowback", "team", "reporting"],
        conclusion_template="Operational communication protocols require daily team meetings and incident reporting within 24 hours.",
        reasoning_framework=(
            "Daily team meetings ensure proactive communication during flowback operations. Incident reporting is required within 24 hours. "
            "Communication protocols follow company operational standards. Meeting minutes and incident reports are documented and reviewed weekly."
        ),
        key_factors=[
            "Daily team meetings",
            "Incident reporting",
            "Documentation",
            "Review frequency",
            "Operational standards"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Frequent communication increases operational workload.",
        counter_arguments=[
            "Communication prevents incidents and ensures proactive management.",
            "Documentation enables trend analysis."
        ],
        resolution_strategy="Mandatory daily meetings and incident reporting within 24 hours.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Operational Standards Section 5"
    ),
    DoctrineBlock(
        topic="Flowback Personnel Allocation Optimization",
        keywords=["personnel", "allocation", "optimization", "flowback", "efficiency", "planning"],
        conclusion_template="Personnel allocation is optimized based on operational needs, safety requirements, and cost efficiency.",
        reasoning_framework=(
            "Personnel allocation during flowback is optimized based on operational needs, safety requirements, and cost efficiency. "
            "Allocation protocols follow company operational standards and safety requirements. Reviews are conducted monthly and inform planning updates."
        ),
        key_factors=[
            "Operational needs",
            "Safety requirements",
            "Cost efficiency",
            "Review frequency",
            "Documentation"
        ],
        primary_authority=[
            "Company Operational Standards",
            "Company Safety Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Personnel minimization increases efficiency but risks operational integrity.",
        counter_arguments=[
            "Optimization ensures efficiency and compliance.",
            "Personnel minimization must not compromise safety."
        ],
        resolution_strategy="Monthly review with planning updates.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Operational Standards Section 6"
    ),
    DoctrineBlock(
        topic="Flowback Equipment Maintenance Planning",
        keywords=["equipment", "maintenance", "planning", "flowback", "safety", "operational"],
        conclusion_template="Equipment maintenance plans are developed for all flowback operations, with weekly reviews and incident-triggered updates.",
        reasoning_framework=(
            "Maintenance planning ensures operational integrity and safety during flowback. Plans are developed for all equipment, with weekly reviews and updates after incidents. "
            "Maintenance protocols follow company engineering standards and safety requirements. Results are documented and reviewed monthly."
        ),
        key_factors=[
            "Maintenance plan development",
            "Weekly review",
            "Incident-triggered updates",
            "Documentation",
            "Safety requirements"
        ],
        primary_authority=[
            "Company Engineering Standards",
            "Company Safety Requirements"
        ],
        burden_holder="Production Engineering Team",
        adversary_position="Maintenance planning increases operational workload and costs.",
        counter_arguments=[
            "Planning prevents equipment failures and ensures safety.",
            "Regulatory requirements mandate maintenance documentation."
        ],
        resolution_strategy="Mandatory maintenance planning with weekly review and incident-triggered updates.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Engineering Standards Section 8"
    ),
    DoctrineBlock(
        topic="Flowback Operational Risk Assessment",
        keywords=["operational", "risk", "assessment", "flowback", "safety", "planning"],
        conclusion_template="Operational risk assessments are conducted monthly for flowback operations, with updates after incidents.",
        reasoning_framework=(
            "Monthly operational risk assessments identify hazards and inform mitigation strategies for flowback operations. "
            "Assessments are updated after incidents. Protocols follow company safety standards and regulatory requirements. "
            "Results are documented and used for planning and regulatory reporting."
        ),
        key_factors=[
            "Monthly assessment",
            "Incident-triggered updates",
            "Hazard identification",
            "Mitigation strategies",
            "Documentation"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Risk assessment increases operational workload.",
        counter_arguments=[
            "Assessment prevents incidents and ensures compliance.",
            "Regulatory requirements mandate assessment."
        ],
        resolution_strategy="Mandatory monthly assessment with updates after incidents.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 9"
    ),
    DoctrineBlock(
        topic="Flowback Operational Performance Benchmarking",
        keywords=["operational", "performance", "benchmarking", "flowback", "optimization", "planning"],
        conclusion_template="Operational performance is benchmarked monthly against industry standards and historical analogs.",
        reasoning_framework=(
            "Monthly benchmarking of flowback operational performance informs optimization and planning. Benchmarks are set against industry standards and historical analogs. "
            "Results are documented and used for planning updates and regulatory reporting. Benchmarking protocols follow company operational standards."
        ),
        key_factors=[
            "Monthly benchmarking",
            "Industry standards",
            "Historical analogs",
            "Documentation",
            "Planning updates"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Benchmarking increases operational workload.",
        counter_arguments=[
            "Benchmarking informs optimization and compliance.",
            "Industry standards require performance review."
        ],
        resolution_strategy="Mandatory monthly benchmarking with planning updates.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Operational Standards Section 7"
    ),
    DoctrineBlock(
        topic="Flowback Operational Optimization Protocol",
        keywords=["operational", "optimization", "protocol", "flowback", "efficiency", "planning"],
        conclusion_template="Operational optimization protocols are reviewed monthly, with updates based on performance benchmarking and incident analysis.",
        reasoning_framework=(
            "Operational optimization protocols are reviewed monthly, with updates based on performance benchmarking and incident analysis. "
            "Protocols follow company operational standards and inform planning updates. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Monthly review",
            "Performance benchmarking",
            "Incident analysis",
            "Documentation",
            "Planning updates"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Optimization protocols increase operational workload.",
        counter_arguments=[
            "Protocols inform efficiency and compliance.",
            "Incident analysis prevents future incidents."
        ],
        resolution_strategy="Mandatory monthly review with updates based on benchmarking and incident analysis.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Operational Standards Section 8"
    ),
    DoctrineBlock(
        topic="Flowback Regulatory Audit Preparation",
        keywords=["regulatory", "audit", "preparation", "flowback", "EPA", "documentation"],
        conclusion_template="Regulatory audit preparation includes daily documentation, monthly review, and quarterly audit readiness checks.",
        reasoning_framework=(
            "Regulatory audit preparation for flowback operations includes daily documentation, monthly review, and quarterly audit readiness checks. "
            "Protocols follow EPA requirements and company compliance standards. Results are documented and used for audit preparation and regulatory reporting."
        ),
        key_factors=[
            "Daily documentation",
            "Monthly review",
            "Quarterly audit readiness",
            "EPA requirements",
            "Compliance standards"
        ],
        primary_authority=[
            "EPA Requirements",
            "Company Compliance Standards"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Audit preparation increases operational workload.",
        counter_arguments=[
            "Preparation ensures audit readiness and compliance.",
            "Regulatory requirements mandate audit preparation."
        ],
        resolution_strategy="Mandatory daily documentation with quarterly audit readiness checks.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="EPA Requirements Section 6"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Prevention Planning",
        keywords=["operational", "incident", "prevention", "planning", "flowback", "safety"],
        conclusion_template="Incident prevention planning is reviewed monthly, with updates after incidents and performance benchmarking.",
        reasoning_framework=(
            "Incident prevention planning is reviewed monthly, with updates after incidents and performance benchmarking. "
            "Planning protocols follow company safety standards and inform operational updates. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Monthly review",
            "Incident updates",
            "Performance benchmarking",
            "Documentation",
            "Operational updates"
        ],
        primary_authority=[
            "Company Safety Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Prevention planning increases operational workload.",
        counter_arguments=[
            "Planning prevents incidents and ensures compliance.",
            "Benchmarking informs prevention strategies."
        ],
        resolution_strategy="Mandatory monthly review with updates after incidents and benchmarking.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 11"
    ),
    DoctrineBlock(
        topic="Flowback Operational Documentation Protocol",
        keywords=["operational", "documentation", "protocol", "flowback", "reporting", "compliance"],
        conclusion_template="Operational documentation protocols require daily logs, incident reports, and monthly performance summaries.",
        reasoning_framework=(
            "Operational documentation protocols require daily logs, incident reports, and monthly performance summaries. "
            "Protocols follow company operational standards and regulatory requirements. Documentation is reviewed monthly for compliance and planning updates."
        ),
        key_factors=[
            "Daily logs",
            "Incident reports",
            "Monthly summaries",
            "Compliance review",
            "Planning updates"
        ],
        primary_authority=[
            "Company Operational Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Documentation increases operational workload.",
        counter_arguments=[
            "Documentation ensures compliance and informs planning.",
            "Regulatory requirements mandate documentation."
        ],
        resolution_strategy="Mandatory daily logs, incident reports, and monthly summaries.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Operational Standards Section 9"
    ),
    DoctrineBlock(
        topic="Flowback Operational Planning Update Frequency",
        keywords=["operational", "planning", "update", "frequency", "flowback", "optimization"],
        conclusion_template="Operational planning is updated monthly, with additional updates after incidents and performance benchmarking.",
        reasoning_framework=(
            "Operational planning is updated monthly, with additional updates after incidents and performance benchmarking. "
            "Planning protocols follow company operational standards and inform optimization strategies. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Monthly updates",
            "Incident-triggered updates",
            "Performance benchmarking",
            "Documentation",
            "Optimization strategies"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Frequent updates increase operational workload.",
        counter_arguments=[
            "Updates inform optimization and compliance.",
            "Incident analysis prevents future incidents."
        ],
        resolution_strategy="Mandatory monthly updates with additional updates after incidents and benchmarking.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Operational Standards Section 10"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Analysis Protocol",
        keywords=["operational", "incident", "analysis", "protocol", "flowback", "safety"],
        conclusion_template="Incident analysis protocols require root cause analysis within 48 hours and monthly trend review.",
        reasoning_framework=(
            "Incident analysis protocols require root cause analysis within 48 hours and monthly trend review. "
            "Protocols follow company safety standards and inform operational updates. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Root cause analysis",
            "48-hour timeline",
            "Monthly trend review",
            "Documentation",
            "Operational updates"
        ],
        primary_authority=[
            "Company Safety Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Incident analysis increases operational workload.",
        counter_arguments=[
            "Analysis prevents future incidents and ensures compliance.",
            "Trend review informs prevention strategies."
        ],
        resolution_strategy="Mandatory root cause analysis within 48 hours and monthly trend review.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 12"
    ),
    DoctrineBlock(
        topic="Flowback Operational Regulatory Update Protocol",
        keywords=["operational", "regulatory", "update", "protocol", "flowback", "compliance"],
        conclusion_template="Regulatory update protocols require quarterly review of EPA and company standards, with operational updates as needed.",
        reasoning_framework=(
            "Regulatory update protocols require quarterly review of EPA and company standards, with operational updates as needed. "
            "Protocols follow company compliance standards and inform operational planning. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Quarterly review",
            "EPA standards",
            "Company standards",
            "Operational updates",
            "Documentation"
        ],
        primary_authority=[
            "EPA Standards",
            "Company Compliance Standards"
        ],
        burden_holder="Environmental Compliance Officer",
        adversary_position="Regulatory updates increase operational workload.",
        counter_arguments=[
            "Updates ensure compliance and inform planning.",
            "Regulatory requirements mandate review."
        ],
        resolution_strategy="Mandatory quarterly review with operational updates as needed.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA Standards Section 7"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Communication Protocol",
        keywords=["operational", "incident", "communication", "protocol", "flowback", "reporting"],
        conclusion_template="Incident communication protocols require immediate reporting to supervisor and documentation within 24 hours.",
        reasoning_framework=(
            "Incident communication protocols require immediate reporting to supervisor and documentation within 24 hours. "
            "Protocols follow company operational standards and inform incident analysis and prevention planning. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Immediate reporting",
            "24-hour documentation",
            "Operational standards",
            "Incident analysis",
            "Prevention planning"
        ],
        primary_authority=[
            "Company Operational Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Communication protocols increase operational workload.",
        counter_arguments=[
            "Immediate reporting enables rapid response and prevention.",
            "Documentation ensures compliance."
        ],
        resolution_strategy="Mandatory immediate reporting and documentation within 24 hours.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Operational Standards Section 11"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Recovery Planning",
        keywords=["operational", "incident", "recovery", "planning", "flowback", "safety"],
        conclusion_template="Incident recovery planning is reviewed monthly, with updates after incidents and performance benchmarking.",
        reasoning_framework=(
            "Incident recovery planning is reviewed monthly, with updates after incidents and performance benchmarking. "
            "Planning protocols follow company safety standards and inform operational updates. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Monthly review",
            "Incident updates",
            "Performance benchmarking",
            "Documentation",
            "Operational updates"
        ],
        primary_authority=[
            "Company Safety Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Recovery planning increases operational workload.",
        counter_arguments=[
            "Planning ensures rapid recovery and compliance.",
            "Benchmarking informs recovery strategies."
        ],
        resolution_strategy="Mandatory monthly review with updates after incidents and benchmarking.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 13"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Prevention Training",
        keywords=["operational", "incident", "prevention", "training", "flowback", "safety"],
        conclusion_template="Incident prevention training is conducted annually, with refresher courses after incidents.",
        reasoning_framework=(
            "Incident prevention training is conducted annually, with refresher courses after incidents. Training protocols follow company safety standards and regulatory requirements. "
            "Training completion is documented and reviewed quarterly."
        ),
        key_factors=[
            "Annual training",
            "Refresher courses",
            "Safety standards",
            "Regulatory requirements",
            "Documentation"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Training increases operational costs and downtime.",
        counter_arguments=[
            "Training prevents incidents and ensures compliance.",
            "Regulatory requirements mandate training."
        ],
        resolution_strategy="Mandatory annual training with refresher courses after incidents.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 14"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Prevention Documentation",
        keywords=["operational", "incident", "prevention", "documentation", "flowback", "reporting"],
        conclusion_template="Incident prevention documentation protocols require daily logs, incident reports, and monthly trend analysis.",
        reasoning_framework=(
            "Incident prevention documentation protocols require daily logs, incident reports, and monthly trend analysis. "
            "Protocols follow company safety standards and regulatory requirements. Documentation is reviewed monthly for compliance and planning updates."
        ),
        key_factors=[
            "Daily logs",
            "Incident reports",
            "Monthly trend analysis",
            "Compliance review",
            "Planning updates"
        ],
        primary_authority=[
            "Company Safety Standards",
            "Regulatory Requirements"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Documentation increases operational workload.",
        counter_arguments=[
            "Documentation ensures compliance and informs planning.",
            "Regulatory requirements mandate documentation."
        ],
        resolution_strategy="Mandatory daily logs, incident reports, and monthly trend analysis.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 15"
    ),
    DoctrineBlock(
        topic="Flowback Operational Incident Prevention Review Frequency",
        keywords=["operational", "incident", "prevention", "review", "frequency", "flowback"],
        conclusion_template="Incident prevention reviews are conducted monthly, with additional reviews after incidents and performance benchmarking.",
        reasoning_framework=(
            "Incident prevention reviews are conducted monthly, with additional reviews after incidents and performance benchmarking. "
            "Review protocols follow company safety standards and inform operational updates. Results are documented and used for regulatory reporting."
        ),
        key_factors=[
            "Monthly review",
            "Incident updates",
            "Performance benchmarking",
            "Documentation",
            "Operational updates"
        ],
        primary_authority=[
            "Company Safety Standards"
        ],
        burden_holder="Flowback Supervisor",
        adversary_position="Review frequency increases operational workload.",
        counter_arguments=[
            "Reviews prevent incidents and ensure compliance.",
            "Benchmarking informs prevention strategies."
        ],
        resolution_strategy="Mandatory monthly review with additional reviews after incidents and benchmarking.",
        entity_scope="FRAC07 flowback operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Company Safety Standards Section 16"
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