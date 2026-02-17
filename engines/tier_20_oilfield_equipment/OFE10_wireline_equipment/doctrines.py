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
        topic="Slickline Gauge Ring Run Procedure",
        keywords=["slickline", "gauge ring", "run procedure", "wellbore", "wireline", "intervention"],
        conclusion_template="The gauge ring run must be executed per API RP 5C5 to ensure wellbore clearance and tool string passage.",
        reasoning_framework="""
        The gauge ring run is a critical step to confirm wellbore clearance prior to deploying more complex or expensive tool strings. The procedure mandates the use of a gauge ring sized to the maximum outer diameter of the intended tool string, run to the target depth and retrieved without obstruction. The reasoning is based on minimizing the risk of tool sticking, ensuring operational efficiency, and preventing costly fishing operations. The process must be documented, with any restrictions or obstructions noted and addressed before proceeding. Deviations from the standard procedure must be justified and approved by the wellsite supervisor. The operator is responsible for ensuring that the gauge ring is free of burrs or damage that could misrepresent wellbore dimensions. The run must be performed under controlled tension, and any unexpected resistance should trigger an immediate halt and investigation. The procedure is governed by both operator policy and API recommended practices.
        """,
        key_factors=[
            "Gauge ring diameter matches tool string OD",
            "Wellbore cleanliness",
            "Documentation of run results",
            "Immediate response to resistance",
            "Supervisor approval for deviations"
        ],
        primary_authority=[
            "API RP 5C5",
            "Operator Wireline Operations Manual"
        ],
        burden_holder="Wireline Operator",
        adversary_position="Gauge ring runs are unnecessary if caliper logs are available.",
        counter_arguments=[
            "Caliper logs may not reflect real-time wellbore conditions.",
            "Physical gauge ring confirms actual passage.",
            "Caliper tools can miss debris or scale."
        ],
        resolution_strategy="Mandate physical gauge ring run unless a waiver is approved by the wellsite supervisor based on documented risk assessment.",
        entity_scope="Wireline Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Chevron North Sea Operations 2017"
    ),
    DoctrineBlock(
        topic="Wireline Pressure Control Equipment",
        keywords=["pressure control", "wireline", "BOP", "lubricator", "wellhead", "safety"],
        conclusion_template="Wireline pressure control equipment must be selected and rigged up per API 16A and operator standards to match the maximum anticipated surface pressure.",
        reasoning_framework="""
        The selection and deployment of wireline pressure control equipment is governed by the need to safely contain wellbore fluids and pressures during wireline operations. The reasoning follows a risk-based approach: equipment must be rated for the maximum anticipated surface pressure, including a safety margin as specified by API 16A. The stack-up typically includes a wireline BOP, lubricator, grease injection head (for slickline), and associated valves. Each component must be inspected and pressure-tested prior to use. The operator is responsible for verifying certification and test records. Pressure control equipment must be compatible with the deployed tool string and cable. The wellsite supervisor must approve any deviations from standard stack-ups. The procedure is designed to prevent uncontrolled hydrocarbon release and protect personnel and assets.
        """,
        key_factors=[
            "Maximum anticipated surface pressure",
            "Equipment certification and pressure test records",
            "Compatibility with tool string and cable",
            "Operator and supervisor approval",
            "Compliance with API and operator standards"
        ],
        primary_authority=[
            "API 16A",
            "Operator Pressure Control Standards"
        ],
        burden_holder="Wireline Service Provider",
        adversary_position="Older pressure control equipment is sufficient if it passes a basic leak test.",
        counter_arguments=[
            "Equipment must meet current certification and design standards.",
            "Basic leak tests do not substitute for full pressure rating compliance.",
            "Regulatory and operator requirements supersede field expediency."
        ],
        resolution_strategy="Require documented certification and pressure test results for all pressure control equipment; reject non-compliant components.",
        entity_scope="Wireline Pressure Control",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="BP Macondo Post-Incident Standards 2011"
    ),
    DoctrineBlock(
        topic="TCP Perforating Gun Systems",
        keywords=["TCP", "perforating", "gun system", "tubing conveyed perforating", "detonation"],
        conclusion_template="TCP perforating gun systems must be designed and deployed in accordance with API RP 67 and operator-specific risk assessments.",
        reasoning_framework="""
        Tubing Conveyed Perforating (TCP) systems are used for high-efficiency perforating operations, often in high-pressure or deviated wells. The doctrine mandates that TCP gun systems be designed to meet API RP 67 guidelines, including safe handling, arming, and deployment procedures. The reasoning is based on minimizing the risk of accidental detonation, ensuring proper depth control, and achieving the desired perforation performance. All explosives must be tracked and accounted for, with clear chain-of-custody documentation. The operator must conduct a risk assessment for each TCP run, considering well conditions, gun configuration, and detonation transfer systems. Only qualified personnel may handle or arm TCP guns. Post-job reviews are required to capture lessons learned and update procedures.
        """,
        key_factors=[
            "API RP 67 compliance",
            "Explosives tracking and documentation",
            "Qualified personnel",
            "Risk assessment for each run",
            "Post-job review and continuous improvement"
        ],
        primary_authority=[
            "API RP 67",
            "Operator Explosives Handling Policy"
        ],
        burden_holder="Wireline/TCP Supervisor",
        adversary_position="Standard wireline gun procedures are sufficient for TCP operations.",
        counter_arguments=[
            "TCP systems involve different deployment and arming mechanisms.",
            "Higher risk due to larger explosive loads and well pressures.",
            "API RP 67 specifically addresses TCP risks."
        ],
        resolution_strategy="Enforce TCP-specific procedures and require documented risk assessments for each operation.",
        entity_scope="TCP Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Shell Global TCP Safety Standard 2015"
    ),
    DoctrineBlock(
        topic="Wireline Logging Tool String Design",
        keywords=["wireline", "logging", "tool string", "design", "modularity", "telemetry"],
        conclusion_template="Wireline logging tool strings must be designed for modularity, compatibility, and telemetry integrity, following SPE 123456 best practices.",
        reasoning_framework="""
        The design of wireline logging tool strings must account for modularity, allowing for rapid reconfiguration and troubleshooting. Compatibility between tools, connectors, and telemetry systems is essential to ensure data integrity and operational efficiency. The doctrine emphasizes the use of standardized connectors, robust centralization, and redundancy in critical measurements. The reasoning is grounded in minimizing non-productive time due to tool failures or misruns, and maximizing data quality. The design must be reviewed by a qualified wireline engineer and tested in a simulated environment prior to field deployment. Documentation of tool string configuration and test results is mandatory.
        """,
        key_factors=[
            "Modularity of tool string components",
            "Connector and telemetry compatibility",
            "Centralization and mechanical integrity",
            "Redundancy in critical measurements",
            "Pre-job review and testing"
        ],
        primary_authority=[
            "SPE 123456",
            "Operator Wireline Logging Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Custom tool string designs are unnecessary if standard tool strings are available.",
        counter_arguments=[
            "Well conditions may require custom configurations.",
            "Standard tool strings may not provide required measurements.",
            "Custom design allows for risk mitigation and data quality assurance."
        ],
        resolution_strategy="Mandate engineering review and documentation for all non-standard tool string designs.",
        entity_scope="Wireline Logging",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ExxonMobil Wireline Logging Policy 2018"
    ),
    DoctrineBlock(
        topic="Bridge Plug Setting Procedures",
        keywords=["bridge plug", "setting", "wireline", "slickline", "mechanical", "hydraulic"],
        conclusion_template="Bridge plug setting must follow manufacturer's instructions and operator policy, with verification by depth correlation and post-set pressure test.",
        reasoning_framework="""
        The setting of bridge plugs is a critical well intervention step, often used for zonal isolation or well abandonment. The doctrine requires strict adherence to the manufacturer's setting procedures, including tool make-up, running speed, and set-down weight or hydraulic pressure. Depth correlation must be performed using gamma-ray or casing collar locator logs to ensure accurate placement. After setting, a post-set pressure test is mandatory to verify plug integrity. The operator must document all steps and obtain supervisor sign-off. Any anomalies during setting must be reported and investigated before proceeding with further operations.
        """,
        key_factors=[
            "Manufacturer's setting procedure",
            "Accurate depth correlation",
            "Post-set pressure test",
            "Documentation and supervisor sign-off",
            "Reporting of anomalies"
        ],
        primary_authority=[
            "Manufacturer's Instructions",
            "Operator Well Intervention Policy"
        ],
        burden_holder="Wireline/Slickline Crew",
        adversary_position="Visual confirmation of plug setting is sufficient without pressure testing.",
        counter_arguments=[
            "Visual confirmation does not guarantee pressure integrity.",
            "Pressure test is the industry standard for verification.",
            "Regulatory requirements mandate pressure testing."
        ],
        resolution_strategy="Require depth correlation and post-set pressure test for all bridge plug installations.",
        entity_scope="Well Intervention",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Halliburton Bridge Plug Setting Guidelines 2016"
    ),
    DoctrineBlock(
        topic="Wireline Fishing and Stuck Tool Recovery",
        keywords=["wireline", "fishing", "stuck tool", "recovery", "overshot", "jarring"],
        conclusion_template="Wireline fishing operations must follow a documented plan, including risk assessment, tool selection, and contingency procedures.",
        reasoning_framework="""
        Wireline fishing is inherently risky and can escalate well control hazards if not managed properly. The doctrine requires a pre-job risk assessment, selection of appropriate fishing tools (e.g., overshot, jars, spears), and definition of contingency procedures in case of escalation. The plan must be reviewed and approved by the wellsite supervisor. The operator must ensure all fishing tools are compatible with the stuck tool's dimensions and wellbore conditions. Real-time monitoring of tension and depth is required during fishing operations. If initial attempts fail, escalation to a higher authority and consideration of alternative recovery methods (e.g., milling, sidetracking) is mandatory.
        """,
        key_factors=[
            "Pre-job risk assessment",
            "Fishing tool selection",
            "Supervisor approval",
            "Real-time monitoring",
            "Escalation procedures"
        ],
        primary_authority=[
            "Operator Fishing Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Fishing Supervisor",
        adversary_position="Experienced crews can improvise fishing operations without formal plans.",
        counter_arguments=[
            "Improvisation increases risk of escalation and well control incidents.",
            "Formal plans ensure all contingencies are considered.",
            "Regulatory and insurance requirements mandate documentation."
        ],
        resolution_strategy="Enforce documented fishing plans and supervisor approval for all fishing operations.",
        entity_scope="Wireline Fishing",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Total E&P Fishing Operations Standard 2019"
    ),
    DoctrineBlock(
        topic="Wireline Cable Specifications and Weak Points",
        keywords=["wireline", "cable", "specifications", "weak point", "breaking strength"],
        conclusion_template="Wireline cable selection must be based on well conditions, tool string weight, and include an engineered weak point as per API 9A.",
        reasoning_framework="""
        The doctrine mandates that wireline cables be selected based on the maximum anticipated tool string weight, well depth, and environmental conditions (temperature, corrosivity). An engineered weak point must be incorporated to ensure that, in the event of a stuck tool, the cable will part at a predictable load, minimizing the risk of wellhead damage or uncontrolled release. The weak point must be rated below the minimum breaking strength of the cable but above the maximum expected operational load. All cable and weak point specifications must be documented and reviewed by the wireline supervisor.
        """,
        key_factors=[
            "Cable breaking strength",
            "Tool string weight",
            "Well conditions",
            "Weak point rating",
            "Documentation and supervisor review"
        ],
        primary_authority=[
            "API 9A",
            "Operator Wireline Cable Policy"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Weak points are unnecessary with modern cable technology.",
        counter_arguments=[
            "Weak points provide a controlled failure mode.",
            "Modern cables can still become stuck or overloaded.",
            "Industry standards require weak points for safety."
        ],
        resolution_strategy="Require engineered weak points in all wireline runs unless specifically waived by the operator.",
        entity_scope="Wireline Cable Management",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Schlumberger Wireline Cable Standards 2014"
    ),
    DoctrineBlock(
        topic="Wireline Truck and Unit Design",
        keywords=["wireline", "truck", "unit", "design", "safety", "ergonomics"],
        conclusion_template="Wireline trucks and units must be designed for safety, ergonomics, and compliance with DOT and operator requirements.",
        reasoning_framework="""
        The design of wireline trucks and units directly impacts operational safety and efficiency. The doctrine requires compliance with Department of Transportation (DOT) regulations, operator-specific requirements, and industry best practices. Safety features such as emergency shut-offs, fire suppression systems, and anti-slip surfaces must be incorporated. Ergonomic considerations include operator workspace layout, visibility, and access to controls. All modifications must be documented and approved by the fleet manager. Regular inspections and maintenance are mandatory to ensure continued compliance and performance.
        """,
        key_factors=[
            "DOT compliance",
            "Operator requirements",
            "Safety features",
            "Ergonomic design",
            "Documentation and maintenance"
        ],
        primary_authority=[
            "DOT Regulations",
            "Operator Fleet Policy"
        ],
        burden_holder="Wireline Fleet Manager",
        adversary_position="Standard truck designs are sufficient for all wireline operations.",
        counter_arguments=[
            "Wellsite conditions may require customizations.",
            "Operator requirements may exceed standard designs.",
            "Safety and ergonomics are critical for crew performance."
        ],
        resolution_strategy="Mandate fleet manager review and approval for all wireline unit designs and modifications.",
        entity_scope="Wireline Fleet Management",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Wireline Unit Design Standard 2017"
    ),
    DoctrineBlock(
        topic="Wellbore Deviation Effects on Wireline Operations",
        keywords=["wellbore deviation", "wireline", "operations", "drag", "helical buckling"],
        conclusion_template="Wireline operations in deviated wells require pre-job modeling and risk assessment to mitigate drag and buckling risks.",
        reasoning_framework="""
        Wellbore deviation introduces additional risks to wireline operations, including increased drag, helical buckling, and the potential for tool sticking. The doctrine requires pre-job modeling of the well trajectory and tool string behavior using industry-standard software. Risk mitigation strategies include the use of roller centralizers, modified tool strings, and adjusted running speeds. The operator must document the risk assessment and mitigation plan, with supervisor approval required for high-deviation wells (>60 degrees). Real-time monitoring of cable tension and depth is mandatory during operations.
        """,
        key_factors=[
            "Wellbore deviation angle",
            "Pre-job modeling",
            "Risk assessment and mitigation",
            "Supervisor approval",
            "Real-time monitoring"
        ],
        primary_authority=[
            "SPE 145678",
            "Operator Deviation Policy"
        ],
        burden_holder="Wireline Operations Engineer",
        adversary_position="Standard wireline procedures are sufficient regardless of deviation.",
        counter_arguments=[
            "Deviated wells present unique mechanical challenges.",
            "Standard procedures do not address increased drag and buckling.",
            "Pre-job modeling reduces risk of tool sticking."
        ],
        resolution_strategy="Require documented modeling and risk assessment for all wireline runs in wells with deviation >30 degrees.",
        entity_scope="Wireline Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ConocoPhillips Deviation Operations Standard 2015"
    ),
    DoctrineBlock(
        topic="E-Line Cable Head Design and Weak Point Integration",
        keywords=["e-line", "cable head", "weak point", "design", "integration"],
        conclusion_template="E-Line cable heads must be designed to integrate a certified weak point and ensure electrical continuity as per API 9A.",
        reasoning_framework="""
        The cable head is a critical interface between the wireline cable and the tool string. The doctrine mandates that E-Line cable heads incorporate a certified weak point, rated below the cable's minimum breaking strength but above operational loads. Electrical continuity must be verified through testing after assembly. The design must allow for rapid weak point replacement and minimize risk of electrical shorts or open circuits. All cable head assemblies must be inspected and tested prior to deployment, with results documented and reviewed by the wireline supervisor.
        """,
        key_factors=[
            "Certified weak point integration",
            "Electrical continuity verification",
            "Ease of weak point replacement",
            "Inspection and documentation",
            "Supervisor review"
        ],
        primary_authority=[
            "API 9A",
            "Operator E-Line Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Weak points can compromise electrical integrity and should be omitted.",
        counter_arguments=[
            "Proper design ensures both mechanical and electrical integrity.",
            "Weak points are required for controlled cable release.",
            "Industry standards mandate weak point integration."
        ],
        resolution_strategy="Mandate certified weak point integration and electrical testing for all E-Line cable heads.",
        entity_scope="E-Line Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Weatherford E-Line Cable Head Standard 2018"
    ),
    DoctrineBlock(
        topic="Memory Tool vs Real-Time Logging Trade-offs",
        keywords=["memory tool", "real-time logging", "wireline", "data acquisition", "telemetry"],
        conclusion_template="The choice between memory tool and real-time logging must be based on well conditions, data requirements, and risk assessment.",
        reasoning_framework="""
        Memory tools and real-time logging systems each offer distinct advantages and limitations. Memory tools are suitable for hostile environments or where real-time telemetry is not feasible, but they do not provide immediate data feedback. Real-time logging enables immediate decision-making but may be limited by telemetry bandwidth or well conditions. The doctrine requires a documented assessment of well conditions, data requirements, and operational risks to determine the appropriate logging mode. The decision must be reviewed and approved by the wireline supervisor, with contingency plans for tool failure or data loss.
        """,
        key_factors=[
            "Well conditions (temperature, pressure, deviation)",
            "Data requirements (real-time vs post-job)",
            "Telemetry limitations",
            "Operational risks",
            "Supervisor review and approval"
        ],
        primary_authority=[
            "SPE 234567",
            "Operator Logging Policy"
        ],
        burden_holder="Wireline Logging Engineer",
        adversary_position="Real-time logging should always be used for critical wells.",
        counter_arguments=[
            "Hostile environments may preclude real-time telemetry.",
            "Memory tools can provide higher data resolution.",
            "Risk assessment may favor memory tools in certain scenarios."
        ],
        resolution_strategy="Require documented assessment and supervisor approval for logging mode selection.",
        entity_scope="Wireline Logging",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Chevron Logging Operations Standard 2016"
    ),
    DoctrineBlock(
        topic="Perforating Gun Detonation Transfer Systems",
        keywords=["perforating gun", "detonation transfer", "TCP", "wireline", "explosives"],
        conclusion_template="Perforating gun detonation transfer systems must be designed and tested to ensure reliable initiation and prevent misfires as per API RP 67.",
        reasoning_framework="""
        The detonation transfer system is the mechanism by which the firing signal is transmitted through the perforating gun string. The doctrine requires that all components (detonators, boosters, transfer bars) be compatible and tested for reliable initiation. The system must be assembled in accordance with manufacturer instructions and API RP 67, with all joints and connections verified by a qualified explosives technician. Pre-job function testing and post-job inspection are mandatory. Documentation of assembly, testing, and any anomalies must be maintained for audit purposes. The operator must ensure that only certified components are used, and that all personnel handling explosives are trained and authorized.
        """,
        key_factors=[
            "Component compatibility",
            "Function testing",
            "Qualified personnel",
            "Documentation and traceability",
            "Certified components"
        ],
        primary_authority=[
            "API RP 67",
            "Manufacturer Instructions"
        ],
        burden_holder="Explosives Technician",
        adversary_position="Field-assembled transfer systems are sufficient if they work in practice.",
        counter_arguments=[
            "Improper assembly increases risk of misfires or accidental detonation.",
            "Certified components and procedures reduce risk.",
            "Documentation is required for regulatory compliance."
        ],
        resolution_strategy="Mandate certified components, documented assembly, and function testing for all detonation transfer systems.",
        entity_scope="Perforating Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Halliburton Perforating Safety Standard 2017"
    ),
    # --- Additional doctrines for comprehensive coverage ---
    DoctrineBlock(
        topic="Wireline Lubricator Length Determination",
        keywords=["wireline", "lubricator", "length", "pressure control", "tool string"],
        conclusion_template="Lubricator length must be calculated to fully accommodate the tool string above the closed wellhead valve, with a 10% contingency margin.",
        reasoning_framework="""
        The lubricator provides a pressure-tight chamber for deploying and retrieving tool strings under pressure. The doctrine requires precise measurement of the tool string, including all connectors and accessories, and adds a 10% contingency margin to account for measurement uncertainty and tool expansion. The lubricator must be pressure-rated for the well and inspected prior to use. The calculation and inspection must be documented and approved by the wireline supervisor. Failure to provide adequate lubricator length can result in tool sticking, pressure loss, or safety incidents.
        """,
        key_factors=[
            "Total tool string length",
            "Connector and accessory dimensions",
            "10% contingency margin",
            "Pressure rating and inspection",
            "Supervisor approval"
        ],
        primary_authority=[
            "API 16A",
            "Operator Pressure Control Manual"
        ],
        burden_holder="Wireline Operator",
        adversary_position="Standard lubricator lengths are sufficient for most jobs.",
        counter_arguments=[
            "Tool strings vary in length and configuration.",
            "Contingency margin accounts for measurement errors.",
            "Operator policy requires job-specific calculation."
        ],
        resolution_strategy="Require documented calculation and supervisor approval for lubricator length on every job.",
        entity_scope="Wireline Pressure Control",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Pressure Control Best Practices 2015"
    ),
    DoctrineBlock(
        topic="Grease Injection Head Operation for Slickline",
        keywords=["grease injection head", "slickline", "pressure control", "operation", "maintenance"],
        conclusion_template="Grease injection heads must be operated and maintained per manufacturer's instructions, with grease type and pressure matched to well conditions.",
        reasoning_framework="""
        The grease injection head is essential for maintaining pressure control during slickline operations. The doctrine mandates that only approved grease types be used, matched to well temperature and pressure. The operator must monitor grease pressure and flow rate, adjusting as necessary to maintain a seal. Regular maintenance, including cleaning and inspection of seals and bearings, is required. Any leaks or pressure anomalies must be reported and operations halted until resolved. Documentation of grease type, pressure settings, and maintenance actions is mandatory.
        """,
        key_factors=[
            "Approved grease type",
            "Pressure and flow rate monitoring",
            "Seal and bearing maintenance",
            "Leak reporting",
            "Documentation"
        ],
        primary_authority=[
            "Manufacturer Instructions",
            "Operator Pressure Control Policy"
        ],
        burden_holder="Slickline Operator",
        adversary_position="Any grease can be used as long as pressure is maintained.",
        counter_arguments=[
            "Incorrect grease can degrade seals and compromise pressure control.",
            "Manufacturer instructions specify compatible grease types.",
            "Operator policy mandates documentation and maintenance."
        ],
        resolution_strategy="Enforce use of approved grease and documented maintenance for all grease injection heads.",
        entity_scope="Slickline Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Slickline Pressure Control Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Depth Correlation Standards",
        keywords=["wireline", "depth correlation", "gamma ray", "CCL", "accuracy"],
        conclusion_template="Wireline depth correlation must be performed using gamma ray and/or casing collar locator logs, with accuracy verified to within 0.5 ft.",
        reasoning_framework="""
        Accurate depth correlation is essential for all wireline operations involving tool placement or intervention. The doctrine requires the use of gamma ray and/or casing collar locator (CCL) logs to correlate wireline depth with known well markers. The process must be documented, and the correlation accuracy verified to within 0.5 ft. Any discrepancies must be investigated and resolved before proceeding. The depth correlation log and calculations must be reviewed and approved by the wireline supervisor.
        """,
        key_factors=[
            "Use of gamma ray and/or CCL logs",
            "Correlation with well markers",
            "Verification to within 0.5 ft",
            "Documentation and supervisor review",
            "Resolution of discrepancies"
        ],
        primary_authority=[
            "SPE 345678",
            "Operator Wireline Logging Policy"
        ],
        burden_holder="Wireline Logging Engineer",
        adversary_position="Visual depth markers are sufficient for shallow wells.",
        counter_arguments=[
            "Visual markers are subject to human error.",
            "Accurate depth is critical for tool placement and intervention.",
            "Industry standards require log-based correlation."
        ],
        resolution_strategy="Mandate log-based depth correlation and supervisor review for all wireline operations.",
        entity_scope="Wireline Logging",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ExxonMobil Depth Correlation Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Centralization",
        keywords=["wireline", "tool string", "centralization", "deviation", "logging"],
        conclusion_template="Centralizers must be installed on wireline tool strings as required by well deviation and tool design to ensure data quality.",
        reasoning_framework="""
        Centralization of wireline tool strings is critical for accurate data acquisition, especially in deviated or horizontal wells. The doctrine requires assessment of well deviation and tool design to determine the number and placement of centralizers. Centralizers must be compatible with the tool string and not impede passage through restrictions. The operator must document centralizer selection and placement, with supervisor approval for high-deviation wells. Improper centralization can result in poor data quality or tool sticking.
        """,
        key_factors=[
            "Well deviation",
            "Tool string design",
            "Centralizer compatibility",
            "Documentation and supervisor approval",
            "Data quality impact"
        ],
        primary_authority=[
            "SPE 456789",
            "Operator Logging Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Centralizers are unnecessary in vertical wells.",
        counter_arguments=[
            "Even slight deviation can affect tool position.",
            "Centralizers improve data quality and reduce sticking risk.",
            "Operator policy requires assessment for every job."
        ],
        resolution_strategy="Require documented assessment and supervisor approval for centralizer use on all wireline runs.",
        entity_scope="Wireline Logging",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Halliburton Centralization Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Wireline Surface Pressure Testing",
        keywords=["wireline", "surface pressure test", "pressure control", "BOP", "lubricator"],
        conclusion_template="All wireline pressure control equipment must pass a documented surface pressure test to the maximum anticipated surface pressure before operations commence.",
        reasoning_framework="""
        Surface pressure testing verifies the integrity of pressure control equipment before exposure to well pressure. The doctrine requires that all components (BOP, lubricator, valves) be tested to the maximum anticipated surface pressure, with results documented and reviewed by the wireline supervisor. Any leaks or failures must be repaired and retested before proceeding. The test must be witnessed by the operator representative. Failure to perform or document the test is grounds for job suspension.
        """,
        key_factors=[
            "Maximum anticipated surface pressure",
            "Component integrity",
            "Documentation and supervisor review",
            "Operator witness",
            "Repair and retest of failures"
        ],
        primary_authority=[
            "API 16A",
            "Operator Pressure Control Policy"
        ],
        burden_holder="Wireline Crew",
        adversary_position="Pressure testing is unnecessary if equipment is new.",
        counter_arguments=[
            "Manufacturing defects or shipping damage can compromise new equipment.",
            "Testing verifies field readiness.",
            "Operator and regulatory requirements mandate testing."
        ],
        resolution_strategy="Enforce documented surface pressure testing for all pressure control equipment before every job.",
        entity_scope="Wireline Pressure Control",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="BP Global Pressure Control Standard 2016"
    ),
    DoctrineBlock(
        topic="Wireline Weak Point Load Verification",
        keywords=["wireline", "weak point", "load verification", "cable", "safety"],
        conclusion_template="All wireline weak points must be load-tested and certified prior to deployment, with documentation retained for audit.",
        reasoning_framework="""
        Weak points are designed to part the wireline at a controlled load in the event of a stuck tool. The doctrine requires that all weak points be load-tested to verify their breaking strength matches the design specification. Certification and test documentation must be retained for audit and reviewed by the wireline supervisor. Use of uncertified or untested weak points is strictly prohibited. The operator must ensure that weak points are compatible with the cable and tool string.
        """,
        key_factors=[
            "Load test results",
            "Certification documentation",
            "Supervisor review",
            "Compatibility with cable and tool string",
            "Audit retention"
        ],
        primary_authority=[
            "API 9A",
            "Operator Wireline Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Factory certification is sufficient without field testing.",
        counter_arguments=[
            "Field conditions may affect weak point performance.",
            "Load testing verifies actual breaking strength.",
            "Operator policy requires field verification."
        ],
        resolution_strategy="Mandate field load testing and documentation for all weak points prior to use.",
        entity_scope="Wireline Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Weak Point Verification Standard 2019"
    ),
    DoctrineBlock(
        topic="Wireline Emergency Disconnect Procedures",
        keywords=["wireline", "emergency disconnect", "safety", "well control", "procedure"],
        conclusion_template="Emergency disconnect procedures must be documented, rehearsed, and approved by the wellsite supervisor before wireline operations commence.",
        reasoning_framework="""
        Emergency disconnect procedures are critical for personnel safety and well control in the event of a surface or downhole emergency. The doctrine requires that all crew members be trained and rehearsed in disconnect procedures, with documentation of training and rehearsal maintained. The procedure must be reviewed and approved by the wellsite supervisor prior to each job. Emergency disconnect tools and equipment must be inspected and function-tested before use. Any deficiencies must be corrected before operations commence.
        """,
        key_factors=[
            "Documented procedures",
            "Crew training and rehearsal",
            "Supervisor approval",
            "Inspection and function testing",
            "Correction of deficiencies"
        ],
        primary_authority=[
            "Operator Safety Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Experienced crews do not need formal disconnect procedures.",
        counter_arguments=[
            "Emergencies require rapid, coordinated action.",
            "Formal procedures ensure consistency and safety.",
            "Operator policy mandates documentation and rehearsal."
        ],
        resolution_strategy="Require documented, rehearsed, and supervisor-approved emergency disconnect procedures for all wireline jobs.",
        entity_scope="Wireline Safety",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Total E&P Wireline Safety Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Cable Head Electrical Testing",
        keywords=["wireline", "cable head", "electrical testing", "continuity", "insulation"],
        conclusion_template="Cable head assemblies must pass electrical continuity and insulation resistance tests prior to deployment.",
        reasoning_framework="""
        Electrical integrity of the cable head is essential for reliable tool operation and data transmission. The doctrine requires continuity and insulation resistance tests be performed on every cable head assembly prior to deployment. Test results must be documented and reviewed by the wireline supervisor. Any failures must be corrected and retested. Use of untested or failed cable heads is prohibited. The operator must ensure that test equipment is calibrated and suitable for the cable type.
        """,
        key_factors=[
            "Continuity test results",
            "Insulation resistance test results",
            "Documentation and supervisor review",
            "Correction and retesting of failures",
            "Test equipment calibration"
        ],
        primary_authority=[
            "API 9A",
            "Operator E-Line Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Cable heads rarely fail and do not require testing before every run.",
        counter_arguments=[
            "Cable head failures can cause tool loss or data corruption.",
            "Testing is quick and prevents costly failures.",
            "Operator policy requires testing before every run."
        ],
        resolution_strategy="Mandate electrical testing and documentation for every cable head prior to deployment.",
        entity_scope="Wireline Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Weatherford Cable Head Testing Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Redress and Maintenance",
        keywords=["wireline", "tool string", "redress", "maintenance", "inspection"],
        conclusion_template="All wireline tool strings must be inspected, redressed, and maintained per manufacturer's schedule and operator policy.",
        reasoning_framework="""
        Regular inspection and maintenance of wireline tool strings are essential to ensure operational reliability and safety. The doctrine requires adherence to the manufacturer's maintenance schedule and operator policy for redressing and replacing wear components. All inspections and maintenance actions must be documented, with records retained for audit. Any damage or excessive wear must be reported and addressed before redeployment. The wireline supervisor is responsible for reviewing maintenance records and approving tool string readiness.
        """,
        key_factors=[
            "Manufacturer's maintenance schedule",
            "Operator policy",
            "Documentation and record retention",
            "Supervisor review and approval",
            "Reporting and correction of damage"
        ],
        primary_authority=[
            "Manufacturer Instructions",
            "Operator Maintenance Policy"
        ],
        burden_holder="Wireline Maintenance Technician",
        adversary_position="Tool strings can be reused without inspection if they appear undamaged.",
        counter_arguments=[
            "Hidden damage may not be visible.",
            "Regular maintenance prevents failures.",
            "Operator policy mandates inspection and documentation."
        ],
        resolution_strategy="Enforce documented inspection, maintenance, and supervisor approval before every tool string deployment.",
        entity_scope="Wireline Maintenance",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Tool String Maintenance Standard 2016"
    ),
    DoctrineBlock(
        topic="Wireline Explosives Handling and Storage",
        keywords=["wireline", "explosives", "handling", "storage", "safety"],
        conclusion_template="All explosives must be handled and stored per API RP 67, with chain-of-custody documentation and access control.",
        reasoning_framework="""
        Explosives used in wireline operations pose significant safety and security risks. The doctrine requires strict adherence to API RP 67 and operator policy for handling, storage, and transportation. All explosives must be tracked with chain-of-custody documentation, and access must be limited to authorized personnel. Storage facilities must meet regulatory requirements for security, ventilation, and fire protection. Any loss or discrepancy must be reported immediately to the operator and regulatory authorities. Training and certification of personnel are mandatory.
        """,
        key_factors=[
            "API RP 67 compliance",
            "Chain-of-custody documentation",
            "Access control",
            "Storage facility requirements",
            "Personnel training and certification"
        ],
        primary_authority=[
            "API RP 67",
            "Operator Explosives Policy"
        ],
        burden_holder="Explosives Custodian",
        adversary_position="Field expediency can override strict documentation in remote locations.",
        counter_arguments=[
            "Regulatory and operator requirements are mandatory.",
            "Field expediency does not justify safety or security lapses.",
            "Chain-of-custody prevents loss and misuse."
        ],
        resolution_strategy="Enforce strict documentation, access control, and regulatory compliance for all explosives handling and storage.",
        entity_scope="Wireline Explosives Management",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Halliburton Explosives Handling Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Wellsite Hazard Assessment",
        keywords=["wireline", "wellsite", "hazard assessment", "risk", "safety"],
        conclusion_template="A documented hazard assessment must be completed and reviewed by the supervisor prior to all wireline operations.",
        reasoning_framework="""
        Wellsite hazard assessment identifies and mitigates risks to personnel, equipment, and the environment. The doctrine requires completion of a hazard assessment checklist, including identification of well control, pressure, chemical, and mechanical hazards. The assessment must be reviewed and approved by the wellsite supervisor, with mitigation measures implemented before operations commence. All crew members must be briefed on identified hazards and controls. Documentation must be retained for audit.
        """,
        key_factors=[
            "Hazard assessment checklist",
            "Supervisor review and approval",
            "Implementation of mitigation measures",
            "Crew briefing",
            "Documentation and audit retention"
        ],
        primary_authority=[
            "Operator Safety Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Experienced crews can identify hazards without formal assessment.",
        counter_arguments=[
            "Formal assessment ensures consistency and thoroughness.",
            "Operator policy mandates documentation.",
            "Crew briefing improves hazard awareness."
        ],
        resolution_strategy="Mandate documented hazard assessment and supervisor review before all wireline operations.",
        entity_scope="Wireline Safety",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="BP Wellsite Hazard Assessment Standard 2019"
    ),
    DoctrineBlock(
        topic="Wireline Data Acquisition and Quality Control",
        keywords=["wireline", "data acquisition", "quality control", "logging", "QA/QC"],
        conclusion_template="All wireline data acquisition must follow documented QA/QC procedures, with real-time monitoring and post-job review.",
        reasoning_framework="""
        Data quality is critical for decision-making in wireline operations. The doctrine requires adherence to documented QA/QC procedures, including real-time monitoring of data quality, calibration of logging tools, and post-job review of acquired data. Any anomalies or data losses must be investigated and documented. The wireline supervisor is responsible for reviewing QA/QC documentation and approving data release to the client. Continuous improvement based on post-job reviews is encouraged.
        """,
        key_factors=[
            "QA/QC procedures",
            "Real-time data monitoring",
            "Tool calibration",
            "Post-job review and documentation",
            "Supervisor approval"
        ],
        primary_authority=[
            "SPE 567890",
            "Operator Data Quality Policy"
        ],
        burden_holder="Wireline Logging Engineer",
        adversary_position="QA/QC is unnecessary for routine logging jobs.",
        counter_arguments=[
            "Routine jobs can still encounter data quality issues.",
            "QA/QC ensures reliability and client confidence.",
            "Operator policy mandates QA/QC for all jobs."
        ],
        resolution_strategy="Enforce documented QA/QC procedures and supervisor approval for all wireline data acquisition.",
        entity_scope="Wireline Logging",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Chevron Wireline Data Quality Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Weight Calculation",
        keywords=["wireline", "tool string", "weight calculation", "cable selection", "weak point"],
        conclusion_template="Tool string weight must be calculated and documented prior to every run to ensure cable and weak point compatibility.",
        reasoning_framework="""
        Accurate calculation of tool string weight is essential for selecting the appropriate wireline cable and weak point. The doctrine requires that all components, including connectors and accessories, be weighed or their weights verified from manufacturer data sheets. The total weight must be documented and reviewed by the wireline supervisor. Any changes to the tool string require recalculation and documentation. The calculated weight is used to verify compatibility with the selected cable and weak point ratings.
        """,
        key_factors=[
            "Component weights",
            "Manufacturer data sheets",
            "Documentation and supervisor review",
            "Compatibility with cable and weak point",
            "Recalculation for changes"
        ],
        primary_authority=[
            "API 9A",
            "Operator Wireline Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Tool string weight can be estimated based on experience.",
        counter_arguments=[
            "Estimation increases risk of cable or weak point failure.",
            "Documentation ensures traceability and accountability.",
            "Operator policy mandates calculation and review."
        ],
        resolution_strategy="Require documented calculation and supervisor review for every tool string run.",
        entity_scope="Wireline Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Tool String Weight Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Cable Drum Tension Monitoring",
        keywords=["wireline", "cable drum", "tension monitoring", "safety", "operations"],
        conclusion_template="Cable drum tension must be monitored in real-time during all wireline operations, with alarms set for overload conditions.",
        reasoning_framework="""
        Real-time tension monitoring prevents cable overload, weak point failure, and tool loss. The doctrine requires installation of calibrated tension monitoring equipment on all wireline units. Alarms must be set to alert the crew of overload or underload conditions. Tension data must be logged and reviewed by the wireline supervisor. Any anomalies must be investigated and resolved before continuing operations. Documentation of tension monitoring and alarm settings is mandatory.
        """,
        key_factors=[
            "Calibrated tension monitoring equipment",
            "Real-time data logging",
            "Alarm settings",
            "Supervisor review",
            "Investigation of anomalies"
        ],
        primary_authority=[
            "Operator Wireline Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Operator",
        adversary_position="Experienced operators can judge tension by feel.",
        counter_arguments=[
            "Human judgment is subject to error.",
            "Real-time monitoring improves safety and reliability.",
            "Operator policy mandates monitoring and documentation."
        ],
        resolution_strategy="Mandate real-time tension monitoring and documentation for all wireline operations.",
        entity_scope="Wireline Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Tension Monitoring Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Cable Lubrication and Corrosion Prevention",
        keywords=["wireline", "cable", "lubrication", "corrosion prevention", "maintenance"],
        conclusion_template="Wireline cables must be lubricated and inspected for corrosion per manufacturer's recommendations and operator policy.",
        reasoning_framework="""
        Proper lubrication and corrosion prevention extend cable life and ensure operational reliability. The doctrine requires use of approved lubricants, application at specified intervals, and inspection for signs of corrosion or wear. Any damage or corrosion must be reported and addressed before further use. Lubrication and inspection actions must be documented, with records reviewed by the wireline supervisor. Operator policy may specify additional requirements for corrosive well environments.
        """,
        key_factors=[
            "Approved lubricant",
            "Application interval",
            "Inspection for corrosion and wear",
            "Documentation and supervisor review",
            "Reporting and correction of damage"
        ],
        primary_authority=[
            "Manufacturer Instructions",
            "Operator Maintenance Policy"
        ],
        burden_holder="Wireline Maintenance Technician",
        adversary_position="Lubrication is unnecessary for short-duration jobs.",
        counter_arguments=[
            "Corrosion can occur rapidly in some environments.",
            "Lubrication reduces friction and wear.",
            "Operator policy mandates lubrication and inspection."
        ],
        resolution_strategy="Enforce documented lubrication and inspection for all wireline cables.",
        entity_scope="Wireline Maintenance",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Baker Hughes Cable Maintenance Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Shock and Vibration Protection",
        keywords=["wireline", "tool string", "shock protection", "vibration", "logging"],
        conclusion_template="Shock and vibration protection must be incorporated in tool string design for all high-impact or high-deviation wireline operations.",
        reasoning_framework="""
        Shock and vibration can damage sensitive wireline tools and degrade data quality. The doctrine requires assessment of well conditions and operational risks to determine the need for shock absorbers, vibration dampers, or reinforced housings. The selection and placement of protection devices must be documented and reviewed by the wireline supervisor. Post-job inspection of tools for shock or vibration damage is mandatory. Continuous improvement based on incident review is encouraged.
        """,
        key_factors=[
            "Assessment of well conditions",
            "Selection of protection devices",
            "Documentation and supervisor review",
            "Post-job inspection",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 678901",
            "Operator Logging Standards"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Shock protection is only needed for explosive operations.",
        counter_arguments=[
            "High-deviation wells and rapid movement can cause shocks.",
            "Sensitive tools are vulnerable to vibration damage.",
            "Operator policy requires assessment for every job."
        ],
        resolution_strategy="Require documented assessment and supervisor review for shock and vibration protection on all wireline runs.",
        entity_scope="Wireline Logging",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Halliburton Shock Protection Guidelines 2018"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Pressure Equalization",
        keywords=["wireline", "tool string", "pressure equalization", "deployment", "retrieval"],
        conclusion_template="Pressure equalization procedures must be followed during tool string deployment and retrieval to prevent equipment damage and safety incidents.",
        reasoning_framework="""
        Pressure differentials across the tool string can cause rapid movement, equipment damage, or safety incidents during deployment and retrieval. The doctrine requires use of equalization valves or ports as specified by the manufacturer. The operator must follow documented procedures for opening and closing equalization devices, with verification by the wireline supervisor. Any anomalies must be reported and resolved before continuing operations. Documentation of equalization actions is mandatory.
        """,
        key_factors=[
            "Manufacturer's equalization procedure",
            "Use of equalization valves or ports",
            "Supervisor verification",
            "Reporting and resolution of anomalies",
            "Documentation"
        ],
        primary_authority=[
            "Manufacturer Instructions",
            "Operator Pressure Control Policy"
        ],
        burden_holder="Wireline Operator",
        adversary_position="Pressure equalization is unnecessary for shallow wells.",
        counter_arguments=[
            "Even small pressure differentials can cause rapid movement.",
            "Equipment damage and safety incidents have occurred in shallow wells.",
            "Operator policy mandates equalization procedures."
        ],
        resolution_strategy="Enforce documented equalization procedures and supervisor verification for all tool string deployments and retrievals.",
        entity_scope="Wireline Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Pressure Equalization Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Wellhead Connection Integrity",
        keywords=["wireline", "wellhead", "connection integrity", "pressure control", "leak testing"],
        conclusion_template="All wireline wellhead connections must be leak-tested and verified for integrity prior to pressurizing the stack.",
        reasoning_framework="""
        Wellhead connection integrity is critical for pressure control and safety. The doctrine requires that all connections be assembled per manufacturer instructions, torqued to specification, and leak-tested prior to pressurization. The test must be documented and reviewed by the wireline supervisor. Any leaks or deficiencies must be corrected and retested before proceeding. Use of damaged or incompatible connections is prohibited.
        """,
        key_factors=[
            "Manufacturer assembly instructions",
            "Torque specification",
            "Leak test results",
            "Supervisor review",
            "Correction and retesting of deficiencies"
        ],
        primary_authority=[
            "API 16A",
            "Operator Pressure Control Policy"
        ],
        burden_holder="Wireline Crew",
        adversary_position="Visual inspection is sufficient for wellhead connections.",
        counter_arguments=[
            "Visual inspection cannot detect small leaks.",
            "Leak testing is required for regulatory compliance.",
            "Operator policy mandates testing and documentation."
        ],
        resolution_strategy="Mandate leak testing and documentation for all wellhead connections prior to pressurization.",
        entity_scope="Wireline Pressure Control",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="BP Wellhead Connection Integrity Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Pre-Job Safety Meeting Requirements",
        keywords=["wireline", "pre-job safety meeting", "JSA", "crew briefing", "hazard communication"],
        conclusion_template="A documented pre-job safety meeting (JSA) must be held and attended by all crew members before wireline operations begin.",
        reasoning_framework="""
        Pre-job safety meetings (Job Safety Analysis, JSA) ensure that all crew members are aware of job hazards, procedures, and emergency actions. The doctrine requires that a JSA be conducted and documented before every wireline job. All crew members must attend and sign the attendance record. The meeting must cover job scope, hazards, controls, and emergency procedures. The wireline supervisor is responsible for leading the meeting and retaining documentation for audit.
        """,
        key_factors=[
            "JSA documentation",
            "Crew attendance and signatures",
            "Hazard and emergency procedure review",
            "Supervisor leadership",
            "Audit retention"
        ],
        primary_authority=[
            "Operator Safety Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Pre-job meetings are unnecessary for routine jobs.",
        counter_arguments=[
            "Routine jobs can still present hazards.",
            "JSA ensures all crew are informed and prepared.",
            "Operator policy mandates JSA for every job."
        ],
        resolution_strategy="Enforce documented JSA and crew attendance before all wireline operations.",
        entity_scope="Wireline Safety",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ExxonMobil Pre-Job Safety Meeting Standard 2019"
    ),
    DoctrineBlock(
        topic="Wireline Well Control Barrier Verification",
        keywords=["wireline", "well control", "barrier verification", "pressure control", "safety"],
        conclusion_template="All well control barriers must be verified and documented prior to commencing wireline operations.",
        reasoning_framework="""
        Well control barriers prevent uncontrolled flow of well fluids and ensure personnel safety. The doctrine requires verification of all primary and secondary barriers (e.g., BOP, valves, plugs) before starting wireline operations. The verification must be documented, and any deficiencies corrected before proceeding. The wireline supervisor is responsible for reviewing barrier status and documentation. Operator policy may require witness by a company representative.
        """,
        key_factors=[
            "Barrier verification checklist",
            "Documentation and supervisor review",
            "Correction of deficiencies",
            "Operator representative witness",
            "Compliance with operator policy"
        ],
        primary_authority=[
            "Operator Well Control Policy",
            "API RP 54"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Barriers can be assumed functional if recently tested.",
        counter_arguments=[
            "Barriers can fail between tests.",
            "Verification ensures current functionality.",
            "Operator policy mandates verification and documentation."
        ],
        resolution_strategy="Mandate documented barrier verification and supervisor review before all wireline operations.",
        entity_scope="Wireline Well Control",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Total E&P Well Control Barrier Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Tool String Compatibility Assessment",
        keywords=["wireline", "tool string", "compatibility", "connector", "telemetry"],
        conclusion_template="Compatibility of all tool string components must be assessed and documented prior to assembly and deployment.",
        reasoning_framework="""
        Tool string compatibility ensures mechanical integrity and reliable data transmission. The doctrine requires assessment of connector types, telemetry protocols, and physical dimensions for all components. Any incompatibilities must be resolved before assembly. The compatibility assessment must be documented and reviewed by the wireline supervisor. Use of incompatible components is prohibited. Operator policy may require simulation or bench testing for complex tool strings.
        """,
        key_factors=[
            "Connector type and fit",
            "Telemetry protocol compatibility",
            "Physical dimensions",
            "Documentation and supervisor review",
            "Simulation or bench testing"
        ],
        primary_authority=[
            "Operator Wireline Standards",
            "Manufacturer Instructions"
        ],
        burden_holder="Wireline Engineer",
        adversary_position="Experienced engineers can assemble tool strings without formal compatibility checks.",
        counter_arguments=[
            "Incompatibility can cause tool failure or data loss.",
            "Documentation ensures traceability and accountability.",
            "Operator policy mandates compatibility assessment."
        ],
        resolution_strategy="Require documented compatibility assessment and supervisor review for all tool string assemblies.",
        entity_scope="Wireline Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Schlumberger Tool String Compatibility Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Environmental Protection Measures",
        keywords=["wireline", "environmental protection", "spill prevention", "waste management", "compliance"],
        conclusion_template="Environmental protection measures, including spill prevention and waste management, must be implemented and documented for all wireline operations.",
        reasoning_framework="""
        Wireline operations can generate waste and pose risks of chemical or hydrocarbon spills. The doctrine requires implementation of environmental protection measures, including secondary containment for fluids, proper waste segregation, and immediate cleanup of spills. All measures must be documented and reviewed by the wireline supervisor. Compliance with regulatory and operator environmental policies is mandatory. Any incidents must be reported and investigated.
        """,
        key_factors=[
            "Secondary containment",
            "Waste segregation and disposal",
            "Spill prevention and cleanup",
            "Documentation and supervisor review",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Operator Environmental Policy",
            "Local Environmental Regulations"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Environmental measures can be relaxed for remote or low-risk locations.",
        counter_arguments=[
            "Environmental incidents can occur anywhere.",
            "Regulatory compliance is mandatory regardless of location.",
            "Operator policy mandates documentation and incident reporting."
        ],
        resolution_strategy="Enforce environmental protection measures and documentation for all wireline operations.",
        entity_scope="Wireline Environmental Management",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="BP Environmental Protection Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Crew Competency and Certification",
        keywords=["wireline", "crew competency", "certification", "training", "safety"],
        conclusion_template="All wireline crew members must hold current certification and competency records as required by operator and regulatory policy.",
        reasoning_framework="""
        Crew competency is essential for safe and efficient wireline operations. The doctrine requires that all crew members hold current certification for their roles, including safety, pressure control, and explosives handling as applicable. Training records must be maintained and reviewed by the wireline supervisor. Any gaps in competency or expired certifications must be addressed before crew members are assigned to jobs. Operator and regulatory requirements may specify additional training or certification.
        """,
        key_factors=[
            "Current certification records",
            "Training documentation",
            "Supervisor review",
            "Addressing competency gaps",
            "Compliance with operator and regulatory policy"
        ],
        primary_authority=[
            "Operator Training Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="On-the-job experience is sufficient for most crew roles.",
        counter_arguments=[
            "Certification ensures baseline competency and safety.",
            "Regulatory and operator requirements are mandatory.",
            "Documentation provides audit trail."
        ],
        resolution_strategy="Mandate current certification and supervisor review for all wireline crew members.",
        entity_scope="Wireline Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Chevron Crew Competency Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Incident Reporting and Investigation",
        keywords=["wireline", "incident reporting", "investigation", "safety", "compliance"],
        conclusion_template="All incidents, near-misses, and unsafe conditions must be reported and investigated per operator policy, with corrective actions documented.",
        reasoning_framework="""
        Incident reporting and investigation drive continuous improvement and regulatory compliance. The doctrine requires that all incidents, near-misses, and unsafe conditions be reported immediately to the supervisor. Investigations must be conducted to identify root causes and implement corrective actions. Documentation of reports, investigations, and actions must be retained for audit. Operator policy may require notification of regulatory authorities for certain incidents.
        """,
        key_factors=[
            "Immediate reporting",
            "Root cause investigation",
            "Corrective action implementation",
            "Documentation and audit retention",
            "Regulatory notification"
        ],
        primary_authority=[
            "Operator Safety Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Minor incidents do not require formal reporting or investigation.",
        counter_arguments=[
            "Minor incidents can indicate systemic issues.",
            "Formal reporting ensures corrective action.",
            "Operator and regulatory policy mandates reporting."
        ],
        resolution_strategy="Enforce immediate reporting, investigation, and documentation for all incidents and near-misses.",
        entity_scope="Wireline Safety",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="BP Incident Reporting Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Equipment Calibration and Certification",
        keywords=["wireline", "equipment calibration", "certification", "logging", "QA/QC"],
        conclusion_template="All wireline equipment must be calibrated and certified per manufacturer and operator schedules, with records maintained for audit.",
        reasoning_framework="""
        Calibration and certification ensure the accuracy and reliability of wireline equipment. The doctrine requires adherence to manufacturer and operator calibration schedules for all logging tools, pressure control equipment, and measurement devices. Calibration and certification records must be maintained and reviewed by the wireline supervisor. Use of uncalibrated or uncertified equipment is prohibited. Operator policy may require third-party calibration or certification for critical equipment.
        """,
        key_factors=[
            "Manufacturer calibration schedule",
            "Operator policy",
            "Certification records",
            "Supervisor review",
            "Third-party calibration"
        ],
        primary_authority=[
            "Manufacturer Instructions",
            "Operator QA/QC Policy"
        ],
        burden_holder="Wireline Maintenance Technician",
        adversary_position="Calibration is unnecessary for equipment that is rarely used.",
        counter_arguments=[
            "Uncalibrated equipment can produce inaccurate data.",
            "Operator policy mandates calibration and certification.",
            "Documentation provides audit trail."
        ],
        resolution_strategy="Mandate calibration, certification, and documentation for all wireline equipment.",
        entity_scope="Wireline QA/QC",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Equipment Calibration Standard 2017"
    ),
    DoctrineBlock(
        topic="Wireline Job Documentation and Record Keeping",
        keywords=["wireline", "job documentation", "record keeping", "compliance", "audit"],
        conclusion_template="Comprehensive job documentation and record keeping are required for all wireline operations, with records retained per operator and regulatory policy.",
        reasoning_framework="""
        Documentation provides traceability, supports audits, and ensures compliance with operator and regulatory requirements. The doctrine requires that all wireline job documentation, including procedures, checklists, test results, and crew certifications, be completed and retained for the specified period. The wireline supervisor is responsible for ensuring completeness and accuracy of records. Electronic or paper records must be protected from loss or tampering. Operator policy may specify additional documentation requirements.
        """,
        key_factors=[
            "Comprehensive documentation",
            "Record retention period",
            "Supervisor responsibility",
            "Protection from loss or tampering",
            "Compliance with operator and regulatory policy"
        ],
        primary_authority=[
            "Operator Documentation Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Minimal documentation is sufficient for routine jobs.",
        counter_arguments=[
            "Comprehensive records support audits and investigations.",
            "Operator and regulatory policy mandate documentation.",
            "Documentation ensures traceability and accountability."
        ],
        resolution_strategy="Enforce comprehensive documentation and supervisor review for all wireline jobs.",
        entity_scope="Wireline Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Chevron Job Documentation Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Equipment Decontamination Procedures",
        keywords=["wireline", "equipment decontamination", "H2S", "NORM", "hazardous materials"],
        conclusion_template="Wireline equipment exposed to hazardous materials (H2S, NORM, etc.) must be decontaminated per operator and regulatory procedures before maintenance or transport.",
        reasoning_framework="""
        Decontamination prevents exposure to hazardous materials and cross-contamination between sites. The doctrine requires that all equipment exposed to H2S, NORM, or other hazardous substances be decontaminated per operator and regulatory procedures before maintenance or transport. Documentation of decontamination actions must be retained for audit. The wireline supervisor is responsible for verifying decontamination and approving equipment release. Personnel performing decontamination must be trained and equipped with appropriate PPE.
        """,
        key_factors=[
            "Exposure to hazardous materials",
            "Decontamination procedures",
            "Documentation and supervisor approval",
            "Personnel training and PPE",
            "Audit retention"
        ],
        primary_authority=[
            "Operator HSE Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Decontamination is unnecessary if equipment appears clean.",
        counter_arguments=[
            "Hazardous residues may not be visible.",
            "Regulatory and operator policy mandate decontamination.",
            "Documentation supports compliance and audit."
        ],
        resolution_strategy="Mandate decontamination, documentation, and supervisor approval for all equipment exposed to hazardous materials.",
        entity_scope="Wireline HSE",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="BP Equipment Decontamination Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Remote Operations and Digital Monitoring",
        keywords=["wireline", "remote operations", "digital monitoring", "telemetry", "data security"],
        conclusion_template="Remote wireline operations and digital monitoring must comply with operator cybersecurity and data integrity policies.",
        reasoning_framework="""
        Remote operations and digital monitoring increase efficiency but introduce cybersecurity and data integrity risks. The doctrine requires compliance with operator cybersecurity policies, including secure data transmission, access control, and regular system audits. All remote operations must be monitored in real-time, with data backups and incident response plans in place. Documentation of system configuration, access logs, and incident reports must be retained for audit. The wireline supervisor is responsible for ensuring compliance and reviewing digital monitoring records.
        """,
        key_factors=[
            "Cybersecurity policy compliance",
            "Secure data transmission",
            "Access control and system audits",
            "Real-time monitoring and data backup",
            "Documentation and supervisor review"
        ],
        primary_authority=[
            "Operator Cybersecurity Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Cybersecurity is not a concern for remote wireline operations.",
        counter_arguments=[
            "Data breaches can compromise operational integrity.",
            "Operator and regulatory policy mandate cybersecurity controls.",
            "Documentation supports audit and incident response."
        ],
        resolution_strategy="Enforce cybersecurity compliance and documentation for all remote wireline operations.",
        entity_scope="Wireline Digital Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Chevron Digital Operations Standard 2019"
    ),
    DoctrineBlock(
        topic="Wireline Vendor and Third-Party Equipment Approval",
        keywords=["wireline", "vendor approval", "third-party equipment", "compliance", "QA/QC"],
        conclusion_template="All vendor and third-party equipment must be approved and documented per operator QA/QC policy before use in wireline operations.",
        reasoning_framework="""
        Use of vendor and third-party equipment introduces variability in quality and compliance. The doctrine requires that all such equipment be reviewed and approved per operator QA/QC policy before use. Documentation of approval, including certification and test results, must be retained for audit. The wireline supervisor is responsible for verifying approval and documentation. Use of unapproved equipment is prohibited. Operator policy may require additional testing or certification for critical equipment.
        """,
        key_factors=[
            "Operator QA/QC policy",
            "Certification and test results",
            "Supervisor verification",
            "Documentation and audit retention",
            "Additional testing or certification"
        ],
        primary_authority=[
            "Operator QA/QC Policy",
            "Regulatory Requirements"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Vendor equipment can be used if it appears to meet requirements.",
        counter_arguments=[
            "Apparent compliance does not guarantee quality or safety.",
            "Operator policy mandates approval and documentation.",
            "Documentation supports audit and accountability."
        ],
        resolution_strategy="Mandate approval, documentation, and supervisor verification for all vendor and third-party equipment.",
        entity_scope="Wireline Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Schlumberger Vendor Approval Standard 2018"
    ),
    DoctrineBlock(
        topic="Wireline Job Close-Out and Lessons Learned",
        keywords=["wireline", "job close-out", "lessons learned", "continuous improvement", "documentation"],
        conclusion_template="A documented job close-out and lessons learned review must be completed and submitted to operator management after every wireline job.",
        reasoning_framework="""
        Job close-out and lessons learned reviews drive continuous improvement and knowledge sharing. The doctrine requires completion of a close-out report, including job summary, performance metrics, incidents, and lessons learned. The report must be reviewed by the wireline supervisor and submitted to operator management. Documentation of corrective actions and improvement opportunities must be retained for audit. Operator policy may require periodic review of lessons learned across multiple jobs.
        """,
        key_factors=[
            "Close-out report completion",
            "Supervisor review and submission",
            "Documentation of incidents and lessons learned",
            "Corrective action tracking",
            "Periodic review"
        ],
        primary_authority=[
            "Operator Continuous Improvement Policy",
            "QA/QC Standards"
        ],
        burden_holder="Wireline Supervisor",
        adversary_position="Lessons learned reviews are unnecessary for routine jobs.",
        counter_arguments=[
            "Routine jobs can still yield improvement opportunities.",
            "Documentation supports continuous improvement.",
            "Operator policy mandates close-out and lessons learned."
        ],
        resolution_strategy="Enforce documented close-out and lessons learned review for all wireline jobs.",
        entity_scope="Wireline Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Chevron Lessons Learned Standard 2019"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]