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
        topic="Manual Transmission Synchronizer Design",
        keywords=["manual transmission", "synchronizer", "gear engagement", "cone clutch", "baulk ring"],
        conclusion_template="A synchronizer design is deemed effective if it ensures smooth gear engagement without gear clash under specified operational loads.",
        reasoning_framework=(
            "Evaluate the synchronizer's ability to match shaft speeds using frictional elements (cone clutch, baulk ring). "
            "Assess material selection for wear resistance and coefficient of friction. "
            "Analyze geometric tolerances and clearances to prevent gear clash. "
            "Review test data for shift effort, engagement time, and durability cycles. "
            "Consider failure modes such as baulk ring wear, cone scoring, and synchronizer spring fatigue. "
            "Compare with industry standards (SAE J945, J939) and OEM requirements. "
            "Balance shift quality, durability, and manufacturing cost. "
            "Document any field failures and warranty claims for continuous improvement."
        ),
        key_factors=[
            "Friction material properties",
            "Cone angle and geometry",
            "Baulk ring design",
            "Shift effort",
            "Durability test results",
            "Field failure data"
        ],
        primary_authority=[
            "SAE J945: Manual Transmission Synchronizer Test Procedure",
            "OEM Transmission Design Guidelines"
        ],
        burden_holder="Transmission Design Engineer",
        adversary_position="Synchronizer design is insufficient for high-torque applications and leads to premature wear.",
        counter_arguments=[
            "Test data demonstrates compliance with SAE J945 for all torque ranges.",
            "Material upgrades and geometric optimizations have been implemented."
        ],
        resolution_strategy="Conduct additional durability testing under high-torque cycles and review field data for validation.",
        entity_scope="Manual Transmission Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J945"
    ),
    DoctrineBlock(
        topic="Automatic Transmission Planetary Gear Set Design",
        keywords=["automatic transmission", "planetary gear set", "epicyclic", "gear ratios", "load distribution"],
        conclusion_template="A planetary gear set is validated if it provides required gear ratios, load capacity, and durability within package constraints.",
        reasoning_framework=(
            "Analyze the gear set configuration (simple, compound, Ravigneaux, Simpson). "
            "Calculate theoretical gear ratios and verify against transmission requirements. "
            "Assess load distribution among sun, planet, and ring gears. "
            "Evaluate bearing selection and lubrication strategy. "
            "Simulate torque paths for each gear range and identify stress concentrations. "
            "Review FEA results for gear tooth bending and contact stresses. "
            "Check for compliance with ISO 6336 and AGMA 2001 standards. "
            "Validate with dynamometer and vehicle-level endurance testing."
        ),
        key_factors=[
            "Gear ratio coverage",
            "Load sharing",
            "Gear tooth strength",
            "Lubrication effectiveness",
            "Package size constraints"
        ],
        primary_authority=[
            "ISO 6336: Calculation of load capacity of spur and helical gears",
            "AGMA 2001: Fundamental Rating Factors and Calculation Methods for Involute Spur and Helical Gear Teeth"
        ],
        burden_holder="Transmission Systems Engineer",
        adversary_position="The gear set design cannot withstand repeated high-torque shifts, leading to gear tooth failure.",
        counter_arguments=[
            "FEA and test data confirm gear tooth stresses are below allowable limits.",
            "Lubrication system ensures adequate film thickness under all conditions."
        ],
        resolution_strategy="Increase gear face width or improve material hardness as mitigation.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 6336"
    ),
    DoctrineBlock(
        topic="Torque Converter Operation and Diagnosis",
        keywords=["torque converter", "hydrodynamic", "stator", "lock-up clutch", "stall speed", "diagnosis"],
        conclusion_template="Torque converter operation is satisfactory if stall speed, torque multiplication, and lock-up function are within OEM specifications.",
        reasoning_framework=(
            "Review torque converter cutaway and flow diagrams to understand fluid coupling operation. "
            "Analyze stall speed and torque multiplication ratio using dynamometer data. "
            "Check lock-up clutch engagement timing and slip control. "
            "Diagnose common failures: stator one-way clutch malfunction, impeller blade deformation, lock-up shudder. "
            "Use transmission scan tool to monitor slip RPM and lock-up command. "
            "Correlate customer complaints (e.g., shudder, delayed engagement) with possible internal faults. "
            "Reference OEM diagnostic flowcharts and TSBs for systematic troubleshooting."
        ),
        key_factors=[
            "Stall speed",
            "Torque multiplication ratio",
            "Lock-up clutch function",
            "Fluid condition",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J643: Torque Converter Terminology"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Torque converter is the root cause of shudder and poor acceleration.",
        counter_arguments=[
            "Lock-up clutch control strategy and fluid condition must be verified before condemning the converter.",
            "Other transmission faults can mimic converter symptoms."
        ],
        resolution_strategy="Perform stall test, lock-up slip test, and fluid analysis before replacement.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="CVT Belt/Chain System Design and Failure",
        keywords=["CVT", "belt", "chain", "pulley", "slip", "failure analysis"],
        conclusion_template="A CVT belt/chain system is robust if it transmits rated torque without slip, excessive wear, or catastrophic failure over the service life.",
        reasoning_framework=(
            "Assess CVT architecture (push belt, pull chain, segmented, or banded). "
            "Evaluate belt/chain material composition and heat treatment. "
            "Analyze pulley surface finish and geometry for optimal friction and wear. "
            "Model torque transmission and slip using contact mechanics. "
            "Review failure modes: belt stretching, chain link fracture, pulley groove wear, delamination. "
            "Correlate field failures with duty cycles and maintenance practices. "
            "Reference JATCO, Bosch, and OEM technical bulletins for known issues and remedies."
        ),
        key_factors=[
            "Belt/chain material strength",
            "Pulley surface finish",
            "Lubrication quality",
            "Torque transmission efficiency",
            "Field failure rates"
        ],
        primary_authority=[
            "SAE J2311: CVT Terminology",
            "OEM CVT Design Standards"
        ],
        burden_holder="CVT Design Engineer",
        adversary_position="CVT belt/chain system is prone to premature failure under high torque or poor maintenance.",
        counter_arguments=[
            "Material upgrades and improved lubrication have reduced failure rates.",
            "Field data shows compliance with warranty targets."
        ],
        resolution_strategy="Implement periodic belt/chain inspection and fluid analysis in maintenance schedule.",
        entity_scope="Continuously Variable Transmission Systems",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2311"
    ),
    DoctrineBlock(
        topic="Dual Clutch Transmission (DCT) Operation",
        keywords=["DCT", "dual clutch", "wet clutch", "dry clutch", "shift quality", "mechatronics"],
        conclusion_template="DCT operation is considered optimal if shift times, torque capacity, and thermal management meet OEM and market benchmarks.",
        reasoning_framework=(
            "Examine DCT configuration (wet vs dry clutch, number of gears, actuator type). "
            "Evaluate clutch engagement strategy for minimal torque interruption. "
            "Analyze shift maps and mechatronic control algorithms. "
            "Assess thermal management for clutches during repeated launches and stop-go traffic. "
            "Review field data for complaints: judder, hesitation, overheating. "
            "Benchmark shift times and fuel economy against conventional AT and MT. "
            "Reference OEM TSBs and customer satisfaction indices."
        ),
        key_factors=[
            "Clutch type and cooling",
            "Shift time and quality",
            "Control algorithm robustness",
            "Thermal management",
            "Field reliability data"
        ],
        primary_authority=[
            "OEM DCT Technical Manuals",
            "SAE J2909: DCT Terminology"
        ],
        burden_holder="Transmission Systems Engineer",
        adversary_position="DCT suffers from poor shift quality and overheating in urban driving.",
        counter_arguments=[
            "Recent software updates have improved shift quality.",
            "Wet clutch variants offer superior thermal performance."
        ],
        resolution_strategy="Update control software and consider clutch type based on application.",
        entity_scope="Dual Clutch Transmission Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2909"
    ),
    DoctrineBlock(
        topic="Transfer Case Design - Part-Time vs Full-Time 4WD",
        keywords=["transfer case", "4WD", "AWD", "part-time", "full-time", "center differential"],
        conclusion_template="Transfer case selection is justified if it aligns with vehicle use case, durability targets, and customer expectations for traction.",
        reasoning_framework=(
            "Compare part-time and full-time 4WD transfer case architectures. "
            "Assess center differential (if present) for torque biasing and slip control. "
            "Evaluate engagement mechanisms (manual, electronic, automatic). "
            "Analyze NVH characteristics and parasitic losses. "
            "Review durability test results under off-road and on-road cycles. "
            "Consider customer feedback on usability and reliability. "
            "Reference OEM product planning and competitive benchmarking."
        ),
        key_factors=[
            "Engagement mechanism",
            "Torque distribution",
            "Durability test results",
            "NVH performance",
            "Customer feedback"
        ],
        primary_authority=[
            "OEM Transfer Case Design Standards",
            "SAE J1952: 4WD Terminology"
        ],
        burden_holder="Vehicle Systems Engineer",
        adversary_position="Part-time 4WD is less convenient and may lead to misuse on high-traction surfaces.",
        counter_arguments=[
            "Clear user instructions and electronic safeguards minimize misuse.",
            "Full-time 4WD adds cost and complexity."
        ],
        resolution_strategy="Select transfer case type based on target market and provide user education.",
        entity_scope="Drivetrain Systems",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1952"
    ),
    DoctrineBlock(
        topic="Differential Types and Limited-Slip Operation",
        keywords=["differential", "open", "limited-slip", "locking", "torque bias", "traction"],
        conclusion_template="Differential selection is appropriate if it provides required torque biasing and traction for intended vehicle application.",
        reasoning_framework=(
            "Identify differential type (open, clutch-type LSD, Torsen, electronic locking). "
            "Analyze torque bias ratio and response to slip events. "
            "Evaluate durability and maintenance requirements. "
            "Assess impact on vehicle handling and stability control integration. "
            "Review field data for noise, vibration, and harshness (NVH) issues. "
            "Benchmark against competitive vehicles in segment. "
            "Reference SAE J639 and OEM guidelines."
        ),
        key_factors=[
            "Torque bias ratio",
            "Slip response time",
            "Durability",
            "NVH characteristics",
            "Integration with stability control"
        ],
        primary_authority=[
            "SAE J639: Differential Terminology",
            "OEM Drivetrain Standards"
        ],
        burden_holder="Drivetrain Engineer",
        adversary_position="Limited-slip differentials add complexity and may increase NVH.",
        counter_arguments=[
            "Modern designs minimize NVH and require minimal maintenance.",
            "Traction benefits outweigh minor drawbacks."
        ],
        resolution_strategy="Select differential type based on vehicle mission profile and validate with customer clinics.",
        entity_scope="Axle and Drivetrain Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Analysis and Specification",
        keywords=["transmission fluid", "ATF", "viscosity", "additive package", "fluid analysis", "specification"],
        conclusion_template="Transmission fluid is specified correctly if it meets OEM viscosity, friction, and durability requirements for the transmission family.",
        reasoning_framework=(
            "Review OEM transmission fluid specification (viscosity, friction modifiers, additive package). "
            "Analyze fluid samples for wear metals, oxidation, and contamination. "
            "Compare laboratory results to baseline and condemnation limits. "
            "Assess impact of fluid condition on shift quality, clutch life, and seal compatibility. "
            "Reference SAE J300 and ASTM D445 for viscosity measurement. "
            "Document any field failures related to fluid degradation."
        ),
        key_factors=[
            "Viscosity index",
            "Friction characteristics",
            "Oxidation stability",
            "Wear metal content",
            "Seal compatibility"
        ],
        primary_authority=[
            "SAE J300: Engine Oil Viscosity Classification",
            "ASTM D445: Kinematic Viscosity"
        ],
        burden_holder="Transmission Fluids Engineer",
        adversary_position="Aftermarket fluids may not meet OEM requirements, leading to premature failure.",
        counter_arguments=[
            "OEM fluids are validated for specific friction and durability targets.",
            "Aftermarket fluids must demonstrate equivalent performance."
        ],
        resolution_strategy="Specify only validated fluids and monitor field performance.",
        entity_scope="Transmission Fluids",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="SAE J300"
    ),
    DoctrineBlock(
        topic="Clutch Hydraulic System Operation and Diagnosis",
        keywords=["clutch", "hydraulic system", "master cylinder", "slave cylinder", "bleeding", "diagnosis"],
        conclusion_template="Clutch hydraulic system is operating correctly if engagement/disengagement is smooth, with no leaks or pedal fade.",
        reasoning_framework=(
            "Inspect hydraulic circuit for leaks at master and slave cylinders, lines, and connections. "
            "Check fluid level and condition in reservoir. "
            "Assess pedal feel for sponginess or fade, indicating air in system. "
            "Perform bleeding procedure per OEM guidelines. "
            "Test for internal bypass in cylinders by holding pedal under pressure. "
            "Correlate customer complaints (hard pedal, incomplete disengagement) with hydraulic faults."
        ),
        key_factors=[
            "System integrity (no leaks)",
            "Fluid condition",
            "Pedal feel",
            "Bleeding procedure",
            "Cylinder function"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1703: Brake Fluid"
        ],
        burden_holder="Service Technician",
        adversary_position="Hydraulic system is prone to air ingress and premature seal failure.",
        counter_arguments=[
            "Proper bleeding and fluid maintenance prevent most issues.",
            "Seal materials are validated for service life."
        ],
        resolution_strategy="Enforce maintenance intervals and use only specified fluids.",
        entity_scope="Clutch Hydraulic Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Automatic Transmission Pressure Testing and Diagnosis",
        keywords=["automatic transmission", "pressure testing", "hydraulic circuit", "line pressure", "diagnosis"],
        conclusion_template="Transmission hydraulic system is validated if line and clutch pressures are within OEM specifications under all operating modes.",
        reasoning_framework=(
            "Connect pressure gauges to test ports as per OEM diagram. "
            "Measure line pressure in Park, Drive, Reverse, and during shifts. "
            "Compare readings to service manual specifications. "
            "Diagnose low/high pressure conditions: pump wear, valve body faults, leaks, or solenoid issues. "
            "Correlate with shift quality and DTCs. "
            "Document findings and recommend corrective action."
        ),
        key_factors=[
            "Line pressure readings",
            "Clutch pressure readings",
            "Pump condition",
            "Valve body function",
            "Solenoid operation"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Pressure testing is time-consuming and may not reveal intermittent faults.",
        counter_arguments=[
            "Pressure testing is essential for root cause analysis.",
            "Supplement with scan tool data for intermittent issues."
        ],
        resolution_strategy="Combine pressure testing with electronic diagnostics for comprehensive assessment.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Control Module (TCM) Adaptive Learning",
        keywords=["TCM", "adaptive learning", "shift quality", "clutch fill", "relearn", "transmission control"],
        conclusion_template="TCM adaptive learning is effective if it compensates for clutch wear and maintains shift quality over service life.",
        reasoning_framework=(
            "Review TCM adaptive learning algorithms for clutch fill, pressure control, and shift timing. "
            "Analyze relearn procedures after repair or fluid change. "
            "Monitor shift quality before and after adaptive reset. "
            "Assess long-term adaptation to wear and environmental changes. "
            "Reference OEM TSBs for known adaptation issues. "
            "Document customer complaints and field fixes."
        ),
        key_factors=[
            "Adaptive algorithm robustness",
            "Relearn procedure effectiveness",
            "Shift quality metrics",
            "Field adaptation data",
            "TCM software version"
        ],
        primary_authority=[
            "OEM Transmission Control Module Guidelines",
            "SAE J1939: CAN Communication"
        ],
        burden_holder="Transmission Calibration Engineer",
        adversary_position="TCM adaptation may mask underlying mechanical faults.",
        counter_arguments=[
            "Adaptive learning improves shift quality and extends service life.",
            "Mechanical faults must be addressed before adaptation."
        ],
        resolution_strategy="Perform mechanical repairs prior to adaptive relearn.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OEM TCM Guidelines"
    ),
    DoctrineBlock(
        topic="Toyota Hybrid Transaxle (eCVT) Operation",
        keywords=["Toyota", "hybrid", "transaxle", "eCVT", "planetary gear", "MG1", "MG2"],
        conclusion_template="Toyota eCVT operation is validated if power split, motor-generator coordination, and durability meet hybrid system targets.",
        reasoning_framework=(
            "Analyze eCVT architecture: single planetary gear set, MG1, MG2, and ICE integration. "
            "Evaluate power split device function and torque paths. "
            "Assess control strategy for seamless ICE/electric transitions. "
            "Review durability and field reliability data. "
            "Monitor energy flow using hybrid scan tool. "
            "Reference Toyota technical training and SAE papers."
        ),
        key_factors=[
            "Power split device function",
            "Motor-generator coordination",
            "Control strategy",
            "Durability",
            "Field reliability"
        ],
        primary_authority=[
            "Toyota Hybrid Technical Training",
            "SAE 2004-01-1007: Hybrid Synergy Drive"
        ],
        burden_holder="Hybrid Systems Engineer",
        adversary_position="eCVT is complex and may have higher repair costs.",
        counter_arguments=[
            "Field data shows high reliability and low maintenance.",
            "System simplicity reduces failure points compared to multi-gear AT."
        ],
        resolution_strategy="Educate service personnel and monitor field repair trends.",
        entity_scope="Hybrid Transmission Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Toyota Hybrid Technical Training"
    ),
    DoctrineBlock(
        topic="Transmission Rebuild Quality Gates and Inspection",
        keywords=["transmission rebuild", "quality gates", "inspection", "assembly", "end play", "cleanliness"],
        conclusion_template="A transmission rebuild is validated if all quality gates are passed and critical inspections are documented.",
        reasoning_framework=(
            "Define quality gates: teardown inspection, parts cleaning, subassembly checks, end play measurement, final test. "
            "Document all measurements and findings. "
            "Inspect for wear, scoring, and contamination. "
            "Verify assembly torque and clearances. "
            "Perform air and hydraulic tests before installation. "
            "Reference OEM rebuild manuals and ISO 9001 procedures."
        ),
        key_factors=[
            "Inspection documentation",
            "Critical dimension checks",
            "Cleanliness",
            "Assembly torque",
            "Final test results"
        ],
        primary_authority=[
            "OEM Rebuild Manual",
            "ISO 9001: Quality Management"
        ],
        burden_holder="Transmission Rebuilder",
        adversary_position="Missed inspection steps can lead to repeat failures.",
        counter_arguments=[
            "Quality gates ensure all critical steps are verified.",
            "Documentation supports warranty claims."
        ],
        resolution_strategy="Enforce checklist sign-off and periodic audits.",
        entity_scope="Transmission Service and Rebuild",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
    DoctrineBlock(
        topic="Drivetrain NVH (Noise, Vibration, Harshness) Diagnosis",
        keywords=["drivetrain", "NVH", "noise", "vibration", "harshness", "diagnosis", "FFT"],
        conclusion_template="Drivetrain NVH is diagnosed accurately if root cause is isolated using frequency analysis and road test data.",
        reasoning_framework=(
            "Conduct road test and record NVH events. "
            "Use FFT analysis to identify frequency and amplitude. "
            "Correlate with drivetrain component speeds (engine, driveshaft, axle). "
            "Inspect for worn U-joints, bearings, mounts, and gear sets. "
            "Review TSBs for known NVH issues. "
            "Document findings and recommend corrective action."
        ),
        key_factors=[
            "Frequency analysis",
            "Component speed correlation",
            "Physical inspection",
            "TSB review",
            "Customer complaint documentation"
        ],
        primary_authority=[
            "OEM NVH Diagnostic Manual",
            "SAE J2565: NVH Terminology"
        ],
        burden_holder="NVH Engineer",
        adversary_position="NVH complaints are subjective and difficult to resolve.",
        counter_arguments=[
            "Objective measurement tools isolate root causes.",
            "TSBs provide proven fixes for common issues."
        ],
        resolution_strategy="Combine objective data with customer feedback for resolution.",
        entity_scope="Drivetrain Systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2565"
    ),
    DoctrineBlock(
        topic="Performance Transmission Tuning and Modifications",
        keywords=["performance", "transmission tuning", "modifications", "shift kit", "clutch pack", "aftermarket"],
        conclusion_template="Performance tuning is justified if modifications improve shift quality, durability, and meet safety standards.",
        reasoning_framework=(
            "Identify target performance metrics (shift time, torque capacity, thermal limits). "
            "Select appropriate modifications: shift kits, upgraded clutch packs, valve body recalibration. "
            "Assess impact on durability and warranty. "
            "Verify compliance with safety and emissions regulations. "
            "Document all changes and test results. "
            "Reference SFI and NHRA guidelines for motorsports applications."
        ),
        key_factors=[
            "Performance metrics",
            "Modification type",
            "Durability impact",
            "Regulatory compliance",
            "Test documentation"
        ],
        primary_authority=[
            "SFI Foundation Specs",
            "OEM Performance Parts Catalog"
        ],
        burden_holder="Performance Transmission Builder",
        adversary_position="Modifications may void warranty and reduce reliability.",
        counter_arguments=[
            "Properly engineered upgrades can improve both performance and durability.",
            "Documentation supports compliance."
        ],
        resolution_strategy="Obtain customer sign-off and retain test records.",
        entity_scope="Performance Transmission Systems",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="SFI Foundation Specs"
    ),
    DoctrineBlock(
        topic="Final Drive Ratio Selection and Gear Ratio Calculations",
        keywords=["final drive", "gear ratio", "calculation", "acceleration", "fuel economy", "towing"],
        conclusion_template="Final drive ratio is selected appropriately if it balances acceleration, fuel economy, and towing requirements.",
        reasoning_framework=(
            "Calculate overall gear ratios for all transmission/axle combinations. "
            "Model vehicle performance: 0-60 mph, top speed, gradeability, fuel economy. "
            "Assess customer usage profile (urban, highway, towing). "
            "Benchmark against competitive vehicles. "
            "Reference OEM and SAE guidelines for ratio selection."
        ),
        key_factors=[
            "Overall gear ratio",
            "Vehicle performance targets",
            "Customer usage",
            "Competitive benchmarking",
            "Regulatory compliance"
        ],
        primary_authority=[
            "OEM Product Planning",
            "SAE J2261: Gear Ratio Terminology"
        ],
        burden_holder="Vehicle Integration Engineer",
        adversary_position="Final drive ratio may compromise either acceleration or fuel economy.",
        counter_arguments=[
            "Ratio selection is a compromise based on market research.",
            "Multiple axle ratios may be offered for different use cases."
        ],
        resolution_strategy="Offer ratio options and educate dealers/customers.",
        entity_scope="Drivetrain Systems",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2261"
    ),
    DoctrineBlock(
        topic="Fleet Transmission Maintenance and Predictive Monitoring",
        keywords=["fleet", "transmission maintenance", "predictive monitoring", "telematics", "fluid analysis"],
        conclusion_template="Fleet transmission maintenance is optimized if predictive monitoring reduces unplanned downtime and repair costs.",
        reasoning_framework=(
            "Implement telematics and IoT sensors for real-time transmission health monitoring. "
            "Analyze fluid samples for wear metals and degradation. "
            "Schedule maintenance based on predictive analytics rather than fixed intervals. "
            "Document reduction in breakdowns and repair costs. "
            "Reference OEM and fleet management best practices."
        ),
        key_factors=[
            "Telematics data",
            "Fluid analysis results",
            "Predictive analytics accuracy",
            "Downtime reduction",
            "Cost savings"
        ],
        primary_authority=[
            "OEM Fleet Maintenance Guidelines",
            "SAE J1939"
        ],
        burden_holder="Fleet Maintenance Manager",
        adversary_position="Predictive systems may generate false positives or require high initial investment.",
        counter_arguments=[
            "Long-term savings outweigh initial costs.",
            "Analytics algorithms are continuously improved."
        ],
        resolution_strategy="Pilot program and ROI analysis before full deployment.",
        entity_scope="Fleet Transmission Systems",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="OEM Fleet Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Transmission Temperature Management and Cooling Systems",
        keywords=["transmission", "temperature management", "cooling system", "heat exchanger", "thermal runaway"],
        conclusion_template="Transmission cooling system is validated if fluid temperature remains within safe limits under all duty cycles.",
        reasoning_framework=(
            "Model thermal loads for all driving scenarios (towing, mountain, track). "
            "Select appropriate heat exchanger (air-to-oil, water-to-oil, auxiliary cooler). "
            "Verify temperature sensor accuracy and control logic. "
            "Test for thermal runaway and overheat protection. "
            "Reference OEM and SAE guidelines for transmission cooling."
        ),
        key_factors=[
            "Thermal load modeling",
            "Heat exchanger selection",
            "Sensor accuracy",
            "Control logic",
            "Field test results"
        ],
        primary_authority=[
            "OEM Transmission Cooling Standards",
            "SAE J2311"
        ],
        burden_holder="Transmission Cooling Engineer",
        adversary_position="Standard cooling systems may be inadequate for severe service.",
        counter_arguments=[
            "Auxiliary coolers are available for severe duty.",
            "Sensor feedback enables overheat protection."
        ],
        resolution_strategy="Specify auxiliary cooling for severe applications.",
        entity_scope="Transmission Cooling Systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Transmission Cooling Standards"
    ),
    # Additional doctrines for comprehensive coverage (total 40+)
    DoctrineBlock(
        topic="Planetary Gear Set Noise and Vibration Control",
        keywords=["planetary gear", "noise", "vibration", "gear whine", "NVH"],
        conclusion_template="Planetary gear set NVH is controlled if gear whine and vibration are below customer perceptibility thresholds.",
        reasoning_framework=(
            "Perform modal and harmonic analysis of planetary gear set. "
            "Optimize tooth profile and microgeometry for minimal excitation. "
            "Use advanced materials and surface treatments to dampen vibration. "
            "Validate with vehicle-level NVH testing and customer clinics. "
            "Reference SAE and ISO NVH standards."
        ),
        key_factors=[
            "Modal analysis results",
            "Tooth profile optimization",
            "Material selection",
            "NVH test data",
            "Customer feedback"
        ],
        primary_authority=[
            "SAE J2565",
            "ISO 6336"
        ],
        burden_holder="Gear NVH Engineer",
        adversary_position="Planetary gear sets inherently generate objectionable noise.",
        counter_arguments=[
            "Profile modifications and materials reduce noise to acceptable levels.",
            "Customer clinics confirm NVH targets are met."
        ],
        resolution_strategy="Iterate design based on NVH test results.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2565"
    ),
    DoctrineBlock(
        topic="Mechatronic Valve Body Diagnostics",
        keywords=["mechatronic", "valve body", "solenoid", "hydraulic control", "diagnosis"],
        conclusion_template="Valve body is diagnosed correctly if solenoid function and hydraulic circuits are verified per OEM flowcharts.",
        reasoning_framework=(
            "Use scan tool to command solenoids and monitor response. "
            "Measure hydraulic pressures at key points. "
            "Inspect for valve sticking, wear, or contamination. "
            "Reference OEM diagnostic flowcharts and wiring diagrams. "
            "Document all findings and recommended repairs."
        ),
        key_factors=[
            "Solenoid response",
            "Hydraulic pressure readings",
            "Valve condition",
            "Diagnostic flowchart adherence",
            "Contamination inspection"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Valve body faults are difficult to isolate due to system complexity.",
        counter_arguments=[
            "OEM flowcharts provide systematic diagnosis.",
            "Scan tool data enables targeted repairs."
        ],
        resolution_strategy="Follow OEM diagnostic procedure step-by-step.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Overhaul Cleanliness Standards",
        keywords=["transmission", "overhaul", "cleanliness", "contamination", "assembly"],
        conclusion_template="Overhaul is validated if all components meet cleanliness standards prior to assembly.",
        reasoning_framework=(
            "Define cleanliness criteria for all transmission components. "
            "Implement cleaning and inspection steps at each stage. "
            "Use particle counters and white glove tests. "
            "Document compliance with ISO 16232 and OEM standards. "
            "Reject contaminated parts and re-clean as needed."
        ),
        key_factors=[
            "Particle count",
            "Inspection documentation",
            "Cleaning process validation",
            "Assembly environment control",
            "ISO 16232 compliance"
        ],
        primary_authority=[
            "ISO 16232: Cleanliness of Automotive Components",
            "OEM Assembly Standards"
        ],
        burden_holder="Transmission Assembly Technician",
        adversary_position="Contamination during rebuild leads to repeat failures.",
        counter_arguments=[
            "Strict cleanliness protocols reduce contamination risk.",
            "Documentation supports warranty claims."
        ],
        resolution_strategy="Audit cleaning process and retrain staff as needed.",
        entity_scope="Transmission Service and Rebuild",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 16232"
    ),
    DoctrineBlock(
        topic="Clutch Friction Material Selection",
        keywords=["clutch", "friction material", "organic", "ceramic", "carbon", "wear", "thermal"],
        conclusion_template="Friction material is selected appropriately if it balances wear resistance, thermal capacity, and shift quality.",
        reasoning_framework=(
            "Evaluate application requirements: torque, temperature, shift feel. "
            "Compare organic, ceramic, and carbon materials for wear and thermal properties. "
            "Test friction coefficient stability over temperature range. "
            "Assess compatibility with transmission fluid. "
            "Reference SAE and OEM material standards."
        ),
        key_factors=[
            "Wear resistance",
            "Thermal capacity",
            "Friction coefficient stability",
            "Fluid compatibility",
            "Cost"
        ],
        primary_authority=[
            "SAE J943: Friction Material Standards",
            "OEM Material Specs"
        ],
        burden_holder="Clutch Design Engineer",
        adversary_position="High-performance materials may increase cost and reduce shift comfort.",
        counter_arguments=[
            "Material selection is a trade-off based on application.",
            "OEMs validate shift quality with customer clinics."
        ],
        resolution_strategy="Select material based on use case and validate with durability testing.",
        entity_scope="Transmission Clutch Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J943"
    ),
    DoctrineBlock(
        topic="Transmission Solenoid Control Strategy",
        keywords=["transmission", "solenoid", "control strategy", "PWM", "shift timing"],
        conclusion_template="Solenoid control strategy is validated if it delivers precise shift timing and clutch pressure control.",
        reasoning_framework=(
            "Map solenoid activation sequence for all gears. "
            "Use PWM control for smooth pressure modulation. "
            "Monitor shift timing and pressure curves. "
            "Update TCM software as needed to address shift complaints. "
            "Reference OEM calibration guidelines."
        ),
        key_factors=[
            "Shift timing accuracy",
            "Pressure modulation",
            "TCM software version",
            "Field complaint rates",
            "Calibration documentation"
        ],
        primary_authority=[
            "OEM TCM Calibration Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Calibration Engineer",
        adversary_position="Software bugs or calibration errors can cause harsh or delayed shifts.",
        counter_arguments=[
            "Continuous software updates address field issues.",
            "Calibration is validated with test fleets."
        ],
        resolution_strategy="Monitor field data and update calibration as needed.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="OEM TCM Calibration Manual"
    ),
    DoctrineBlock(
        topic="Transmission Case Material Selection",
        keywords=["transmission case", "material selection", "aluminum", "magnesium", "cast iron", "NVH"],
        conclusion_template="Case material is selected appropriately if it meets strength, NVH, and weight targets.",
        reasoning_framework=(
            "Compare aluminum, magnesium, and cast iron for strength, weight, and NVH damping. "
            "Assess corrosion resistance and manufacturability. "
            "Validate with FEA and field durability tests. "
            "Reference OEM and SAE material standards."
        ),
        key_factors=[
            "Strength",
            "NVH damping",
            "Weight",
            "Corrosion resistance",
            "Manufacturability"
        ],
        primary_authority=[
            "SAE J431: Cast Iron",
            "OEM Material Standards"
        ],
        burden_holder="Transmission Design Engineer",
        adversary_position="Lightweight materials may compromise NVH or durability.",
        counter_arguments=[
            "Design optimizations and coatings address material limitations.",
            "Field data supports material selection."
        ],
        resolution_strategy="Balance material properties with design features.",
        entity_scope="Transmission Structural Components",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J431"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Exchange vs. Drain and Fill",
        keywords=["transmission fluid", "exchange", "drain and fill", "maintenance", "service interval"],
        conclusion_template="Fluid service method is selected appropriately if it maximizes fluid renewal and minimizes risk of damage.",
        reasoning_framework=(
            "Compare fluid exchange (machine-assisted) with drain and fill (gravity). "
            "Assess risk of dislodging debris and compatibility with transmission design. "
            "Reference OEM recommendations for service intervals and methods. "
            "Document field results and customer satisfaction."
        ),
        key_factors=[
            "Fluid renewal percentage",
            "Risk of debris mobilization",
            "OEM recommendation",
            "Service interval",
            "Customer satisfaction"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Service Manager",
        adversary_position="Fluid exchange may cause debris to clog valves or solenoids.",
        counter_arguments=[
            "Properly performed exchange is safe and effective.",
            "Drain and fill may leave significant old fluid."
        ],
        resolution_strategy="Follow OEM method and monitor field outcomes.",
        entity_scope="Transmission Maintenance",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Mount Design and NVH Isolation",
        keywords=["transmission mount", "NVH", "isolation", "elastomer", "hydraulic mount"],
        conclusion_template="Mount design is validated if it isolates NVH while maintaining drivetrain alignment.",
        reasoning_framework=(
            "Select elastomer or hydraulic mount based on NVH and durability targets. "
            "Model mount stiffness and damping. "
            "Test for resonance and vibration transmission. "
            "Validate with vehicle-level NVH and durability testing. "
            "Reference OEM and SAE mount standards."
        ),
        key_factors=[
            "Stiffness",
            "Damping",
            "Durability",
            "NVH test results",
            "Alignment retention"
        ],
        primary_authority=[
            "OEM Mount Design Standards",
            "SAE J2565"
        ],
        burden_holder="Drivetrain NVH Engineer",
        adversary_position="Soft mounts may compromise handling; stiff mounts may increase NVH.",
        counter_arguments=[
            "Mount tuning balances NVH and handling.",
            "Hydraulic mounts offer best compromise."
        ],
        resolution_strategy="Iterate mount design based on vehicle testing.",
        entity_scope="Drivetrain Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OEM Mount Design Standards"
    ),
    DoctrineBlock(
        topic="Transmission Range Sensor Calibration",
        keywords=["transmission range sensor", "calibration", "PRNDL", "shift position", "TCM input"],
        conclusion_template="Range sensor is calibrated correctly if TCM receives accurate gear position signals in all lever positions.",
        reasoning_framework=(
            "Align range sensor with shift lever per OEM procedure. "
            "Verify TCM input for all positions (P, R, N, D, L). "
            "Check for DTCs related to range sensor. "
            "Document calibration process and results."
        ),
        key_factors=[
            "Sensor alignment",
            "TCM input accuracy",
            "DTC absence",
            "Calibration documentation",
            "Field reliability"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Service Technician",
        adversary_position="Misaligned sensors cause shift errors and safety issues.",
        counter_arguments=[
            "Proper calibration eliminates errors.",
            "OEM procedures are robust."
        ],
        resolution_strategy="Enforce calibration after sensor replacement.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Parking Pawl Design and Safety",
        keywords=["parking pawl", "design", "safety", "engagement", "overload"],
        conclusion_template="Parking pawl is designed safely if it withstands specified loads and prevents vehicle rollaway.",
        reasoning_framework=(
            "Calculate engagement force and load capacity. "
            "Model stress in pawl and gear under worst-case slope. "
            "Test for engagement reliability and release under load. "
            "Reference OEM and SAE safety standards."
        ),
        key_factors=[
            "Load capacity",
            "Engagement reliability",
            "Release under load",
            "Safety test results",
            "Material strength"
        ],
        primary_authority=[
            "SAE J2208: Parking Mechanisms",
            "OEM Safety Standards"
        ],
        burden_holder="Transmission Design Engineer",
        adversary_position="Pawl failure can cause rollaway accidents.",
        counter_arguments=[
            "Design validation includes overload and abuse testing.",
            "Safety factors exceed regulatory minimums."
        ],
        resolution_strategy="Periodic review of field incidents and design updates.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2208"
    ),
    DoctrineBlock(
        topic="Transmission Output Shaft Spline Wear Diagnosis",
        keywords=["output shaft", "spline wear", "diagnosis", "backlash", "NVH"],
        conclusion_template="Spline wear is diagnosed accurately if excessive backlash or NVH is confirmed by measurement and inspection.",
        reasoning_framework=(
            "Measure output shaft backlash and compare to OEM limits. "
            "Inspect spline surfaces for wear, galling, or deformation. "
            "Correlate NVH complaints with measured wear. "
            "Reference OEM service bulletins for known issues."
        ),
        key_factors=[
            "Backlash measurement",
            "Spline surface inspection",
            "NVH correlation",
            "Service bulletin review",
            "Replacement criteria"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Service Technician",
        adversary_position="Spline wear is often missed until catastrophic failure.",
        counter_arguments=[
            "Routine inspection identifies wear early.",
            "OEM bulletins provide replacement guidelines."
        ],
        resolution_strategy="Include spline inspection in scheduled maintenance.",
        entity_scope="Drivetrain Systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Electronic Throttle Integration",
        keywords=["transmission", "electronic throttle", "integration", "shift quality", "torque management"],
        conclusion_template="Integration is validated if throttle and transmission coordinate for optimal shift quality and emissions.",
        reasoning_framework=(
            "Map throttle position to shift schedule and torque reduction events. "
            "Verify TCM and ECM communication via CAN. "
            "Test for shift quality and emissions compliance. "
            "Reference OEM calibration and integration guidelines."
        ),
        key_factors=[
            "Throttle-transmission coordination",
            "CAN communication integrity",
            "Shift quality metrics",
            "Emissions compliance",
            "Calibration documentation"
        ],
        primary_authority=[
            "OEM Calibration Manual",
            "SAE J1939"
        ],
        burden_holder="Powertrain Integration Engineer",
        adversary_position="Integration errors cause shift shock or emissions failures.",
        counter_arguments=[
            "OEM calibration process ensures robust integration.",
            "Continuous validation with test fleets."
        ],
        resolution_strategy="Monitor field data and update calibration as needed.",
        entity_scope="Powertrain Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Calibration Manual"
    ),
    DoctrineBlock(
        topic="Transmission Input Shaft Torsional Vibration Control",
        keywords=["input shaft", "torsional vibration", "damping", "NVH", "damper"],
        conclusion_template="Torsional vibration is controlled if damper system prevents resonance and NVH complaints.",
        reasoning_framework=(
            "Model input shaft torsional modes and resonance frequencies. "
            "Select damper (spring, rubber, dual-mass flywheel) based on application. "
            "Validate with NVH testing and customer clinics. "
            "Reference OEM and SAE NVH standards."
        ),
        key_factors=[
            "Resonance frequency",
            "Damper selection",
            "NVH test results",
            "Customer feedback",
            "Durability"
        ],
        primary_authority=[
            "SAE J2565",
            "OEM NVH Standards"
        ],
        burden_holder="NVH Engineer",
        adversary_position="Torsional vibration can cause gear rattle and customer dissatisfaction.",
        counter_arguments=[
            "Dampers are tuned for each application.",
            "Field data confirms NVH targets are met."
        ],
        resolution_strategy="Iterate damper design based on test results.",
        entity_scope="Drivetrain Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2565"
    ),
    DoctrineBlock(
        topic="Transmission Shift Interlock System Safety",
        keywords=["shift interlock", "safety", "brake pedal", "park", "TCM"],
        conclusion_template="Shift interlock is validated if it prevents unintended gear engagement per safety standards.",
        reasoning_framework=(
            "Test interlock function: gear lever movement only with brake pedal applied. "
            "Verify TCM and brake switch inputs. "
            "Reference FMVSS and OEM safety requirements. "
            "Document test results and field incident reports."
        ),
        key_factors=[
            "Interlock function test",
            "TCM input verification",
            "Safety standard compliance",
            "Incident report review",
            "Field reliability"
        ],
        primary_authority=[
            "FMVSS 114: Theft Protection",
            "OEM Safety Standards"
        ],
        burden_holder="Transmission Safety Engineer",
        adversary_position="Interlock failures can lead to rollaway or unintended movement.",
        counter_arguments=[
            "Redundant inputs and diagnostics minimize risk.",
            "Field reliability is high."
        ],
        resolution_strategy="Monitor incident reports and update design as needed.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 114"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Cooler Line Routing and Leak Prevention",
        keywords=["fluid cooler", "line routing", "leak prevention", "hose", "fitting"],
        conclusion_template="Cooler line routing is validated if it prevents leaks, abrasion, and thermal damage.",
        reasoning_framework=(
            "Route lines away from heat sources and moving parts. "
            "Use abrasion sleeves and secure with proper clips. "
            "Select hose and fitting materials for fluid compatibility and pressure rating. "
            "Pressure test after installation. "
            "Reference OEM routing diagrams and SAE standards."
        ),
        key_factors=[
            "Routing path",
            "Abrasion protection",
            "Material selection",
            "Pressure test results",
            "Installation documentation"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1532: Transmission Oil Cooler Hose"
        ],
        burden_holder="Service Technician",
        adversary_position="Improper routing leads to leaks and transmission failure.",
        counter_arguments=[
            "OEM diagrams and parts ensure proper routing.",
            "Pressure testing verifies integrity."
        ],
        resolution_strategy="Enforce routing checks during installation.",
        entity_scope="Transmission Cooling Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J1532"
    ),
    DoctrineBlock(
        topic="Transmission Output Speed Sensor Diagnosis",
        keywords=["output speed sensor", "diagnosis", "TCM", "DTC", "signal integrity"],
        conclusion_template="Output speed sensor is diagnosed correctly if signal matches shaft speed and DTCs are addressed.",
        reasoning_framework=(
            "Monitor output speed sensor signal with scan tool. "
            "Compare to expected shaft speed and check for dropouts. "
            "Inspect wiring and connector integrity. "
            "Reference DTCs and OEM diagnostic flowcharts."
        ),
        key_factors=[
            "Signal integrity",
            "Shaft speed correlation",
            "Wiring inspection",
            "DTC review",
            "OEM diagnostic procedure"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Sensor faults may be intermittent and hard to detect.",
        counter_arguments=[
            "Live data and DTCs pinpoint most faults.",
            "Wiring inspection addresses intermittent issues."
        ],
        resolution_strategy="Replace sensor and retest if faults persist.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Valve Body Remanufacturing Standards",
        keywords=["valve body", "remanufacturing", "standards", "solenoid", "hydraulic circuit"],
        conclusion_template="Valve body remanufacturing is validated if all bores, valves, and solenoids meet OEM specifications.",
        reasoning_framework=(
            "Disassemble and clean all valve body components. "
            "Measure bore diameters and check for wear. "
            "Replace or refurbish valves and solenoids as needed. "
            "Pressure test hydraulic circuits. "
            "Document all measurements and repairs."
        ),
        key_factors=[
            "Bore measurement",
            "Valve and solenoid condition",
            "Hydraulic circuit test",
            "Cleaning process",
            "Documentation"
        ],
        primary_authority=[
            "OEM Remanufacturing Manual",
            "ISO 9001"
        ],
        burden_holder="Remanufacturing Technician",
        adversary_position="Worn bores or valves may be missed, leading to repeat failures.",
        counter_arguments=[
            "Precision measurement and documentation ensure quality.",
            "ISO 9001 process audits verify compliance."
        ],
        resolution_strategy="Implement double-checks and periodic audits.",
        entity_scope="Transmission Service and Rebuild",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Thermal Degradation Analysis",
        keywords=["transmission fluid", "thermal degradation", "oxidation", "fluid analysis", "service interval"],
        conclusion_template="Thermal degradation is assessed if fluid oxidation and breakdown products are measured and compared to limits.",
        reasoning_framework=(
            "Collect fluid samples after severe duty cycles. "
            "Analyze for oxidation, TAN, and breakdown products. "
            "Compare to condemnation limits and OEM recommendations. "
            "Adjust service intervals based on results."
        ),
        key_factors=[
            "Oxidation level",
            "TAN measurement",
            "Breakdown products",
            "Service interval adjustment",
            "OEM limits"
        ],
        primary_authority=[
            "ASTM D664: Acid Number",
            "OEM Fluid Analysis Guidelines"
        ],
        burden_holder="Fluids Engineer",
        adversary_position="Thermal breakdown leads to clutch and valve failures.",
        counter_arguments=[
            "Analysis allows proactive fluid replacement.",
            "OEM fluids are validated for thermal stability."
        ],
        resolution_strategy="Monitor high-duty vehicles and adjust intervals.",
        entity_scope="Transmission Fluids",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D664"
    ),
    DoctrineBlock(
        topic="Transmission Clutch Pack Clearance Measurement",
        keywords=["clutch pack", "clearance", "measurement", "assembly", "shift quality"],
        conclusion_template="Clutch pack clearance is set correctly if it meets OEM specs for shift quality and durability.",
        reasoning_framework=(
            "Assemble clutch pack and measure clearance with feeler gauge or dial indicator. "
            "Compare to OEM specification. "
            "Adjust with selective steels as needed. "
            "Document all measurements."
        ),
        key_factors=[
            "Measured clearance",
            "OEM specification",
            "Adjustment method",
            "Documentation",
            "Shift quality"
        ],
        primary_authority=[
            "OEM Service Manual",
            "ISO 9001"
        ],
        burden_holder="Transmission Rebuilder",
        adversary_position="Incorrect clearance causes shift complaints and premature wear.",
        counter_arguments=[
            "Measurement and documentation prevent errors.",
            "ISO 9001 process ensures compliance."
        ],
        resolution_strategy="Double-check measurements and sign-off.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Line Pressure Modulator Valve Diagnosis",
        keywords=["line pressure", "modulator valve", "diagnosis", "hydraulic control", "shift quality"],
        conclusion_template="Modulator valve is diagnosed correctly if line pressure responds to control inputs per OEM specs.",
        reasoning_framework=(
            "Monitor line pressure with gauge during modulator valve actuation. "
            "Check for sticking, wear, or contamination. "
            "Reference OEM diagnostic flowcharts. "
            "Document findings and repairs."
        ),
        key_factors=[
            "Line pressure response",
            "Valve condition",
            "Contamination",
            "Diagnostic procedure",
            "Repair documentation"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Modulator valve faults are often intermittent.",
        counter_arguments=[
            "Systematic diagnosis and cleaning resolve most issues.",
            "Replacement available if needed."
        ],
        resolution_strategy="Follow OEM diagnostic steps and replace as needed.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Input Speed Sensor Diagnosis",
        keywords=["input speed sensor", "diagnosis", "TCM", "DTC", "signal integrity"],
        conclusion_template="Input speed sensor is diagnosed correctly if signal matches expected RPM and DTCs are addressed.",
        reasoning_framework=(
            "Monitor input speed sensor signal with scan tool. "
            "Compare to engine and transmission RPM. "
            "Inspect wiring and connectors. "
            "Reference DTCs and OEM diagnostic flowcharts."
        ),
        key_factors=[
            "Signal integrity",
            "RPM correlation",
            "Wiring inspection",
            "DTC review",
            "OEM diagnostic procedure"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Sensor faults may cause shift errors and are hard to detect.",
        counter_arguments=[
            "Live data and DTCs pinpoint most faults.",
            "Wiring inspection addresses intermittent issues."
        ],
        resolution_strategy="Replace sensor and retest if faults persist.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Clutch Apply and Release Timing",
        keywords=["clutch", "apply timing", "release timing", "shift quality", "TCM"],
        conclusion_template="Clutch timing is validated if apply and release events meet shift quality and durability targets.",
        reasoning_framework=(
            "Monitor clutch pressure and timing with scan tool and pressure gauges. "
            "Compare to OEM shift quality metrics. "
            "Adjust TCM calibration as needed. "
            "Document all changes and test results."
        ),
        key_factors=[
            "Apply/release timing",
            "Pressure curve",
            "Shift quality",
            "TCM calibration",
            "Test results"
        ],
        primary_authority=[
            "OEM Calibration Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Calibration Engineer",
        adversary_position="Incorrect timing causes harsh or delayed shifts.",
        counter_arguments=[
            "Calibration is validated with test fleets.",
            "Continuous updates address field issues."
        ],
        resolution_strategy="Monitor field data and update calibration as needed.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OEM Calibration Manual"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Contamination Diagnosis",
        keywords=["transmission fluid", "contamination", "diagnosis", "wear metals", "fluid analysis"],
        conclusion_template="Contamination is diagnosed if fluid analysis reveals abnormal wear metals or debris.",
        reasoning_framework=(
            "Collect fluid sample and send to lab for analysis. "
            "Check for wear metals, clutch material, and debris. "
            "Compare to baseline and condemnation limits. "
            "Correlate with transmission symptoms and DTCs."
        ),
        key_factors=[
            "Wear metal content",
            "Debris identification",
            "Baseline comparison",
            "Symptom correlation",
            "DTC review"
        ],
        primary_authority=[
            "ASTM D5185: Wear Metals",
            "OEM Fluid Analysis Guidelines"
        ],
        burden_holder="Fluids Engineer",
        adversary_position="Contamination may not be detected until major failure.",
        counter_arguments=[
            "Regular analysis identifies issues early.",
            "OEM guidelines specify limits."
        ],
        resolution_strategy="Implement periodic fluid analysis for high-value vehicles.",
        entity_scope="Transmission Fluids",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D5185"
    ),
    DoctrineBlock(
        topic="Transmission Clutch Return Spring Selection",
        keywords=["clutch", "return spring", "selection", "apply force", "release timing"],
        conclusion_template="Return spring is selected correctly if it ensures full clutch release and meets durability targets.",
        reasoning_framework=(
            "Calculate required spring force for full clutch release. "
            "Select material and design for fatigue life. "
            "Test for consistent release timing and force. "
            "Reference OEM and SAE spring standards."
        ),
        key_factors=[
            "Spring force",
            "Material selection",
            "Fatigue life",
            "Release timing",
            "Test results"
        ],
        primary_authority=[
            "SAE J157: Coil Springs",
            "OEM Spring Standards"
        ],
        burden_holder="Clutch Design Engineer",
        adversary_position="Weak springs cause incomplete release; strong springs increase apply effort.",
        counter_arguments=[
            "Design balances release and apply forces.",
            "Durability testing validates selection."
        ],
        resolution_strategy="Iterate design based on test results.",
        entity_scope="Transmission Clutch Systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J157"
    ),
    DoctrineBlock(
        topic="Transmission Fluid Pump Design and Efficiency",
        keywords=["fluid pump", "design", "efficiency", "gear pump", "vane pump"],
        conclusion_template="Pump design is validated if it delivers required flow and pressure with minimal parasitic loss.",
        reasoning_framework=(
            "Select pump type (gear, vane, variable displacement) based on application. "
            "Model flow and pressure curves. "
            "Test for efficiency and durability. "
            "Reference OEM and SAE pump standards."
        ),
        key_factors=[
            "Flow rate",
            "Pressure capability",
            "Efficiency",
            "Durability",
            "Test results"
        ],
        primary_authority=[
            "SAE J2311",
            "OEM Pump Standards"
        ],
        burden_holder="Transmission Design Engineer",
        adversary_position="Inefficient pumps increase fuel consumption.",
        counter_arguments=[
            "Variable displacement pumps reduce losses.",
            "Design is validated with test data."
        ],
        resolution_strategy="Monitor field data and update design as needed.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2311"
    ),
    DoctrineBlock(
        topic="Transmission Clutch Drum Crack Diagnosis",
        keywords=["clutch drum", "crack", "diagnosis", "hydraulic leak", "inspection"],
        conclusion_template="Drum is diagnosed correctly if cracks or leaks are confirmed by visual and pressure testing.",
        reasoning_framework=(
            "Inspect drum for cracks, scoring, or leaks. "
            "Pressure test drum for internal leaks. "
            "Reference OEM service bulletins for known issues. "
            "Replace drum if defects are found."
        ),
        key_factors=[
            "Visual inspection",
            "Pressure test",
            "Service bulletin review",
            "Replacement criteria",
            "Documentation"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J2311"
        ],
        burden_holder="Service Technician",
        adversary_position="Cracks may be missed during routine rebuild.",
        counter_arguments=[
            "Pressure testing identifies hidden leaks.",
            "OEM bulletins highlight common failure areas."
        ],
        resolution_strategy="Include drum inspection in rebuild checklist.",
        entity_scope="Automatic Transmission Systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Clutch Apply Piston Seal Selection",
        keywords=["clutch", "apply piston", "seal selection", "material", "leakage"],
        conclusion_template="Seal is selected correctly if it prevents leakage and is compatible with fluid and temperature range.",
        reasoning_framework=(
            "Select seal material for fluid compatibility and temperature range. "
            "Test for leakage and wear under cycling. "
            "Reference OEM and SAE seal standards."
        ),
        key_factors=[
            "Material compatibility",
            "Leakage rate",
            "Wear resistance",
            "Temperature range",
            "Test results"
        ],
        primary_authority=[
            "SAE J200: Rubber Materials",
            "OEM Seal Standards"
        ],
        burden_holder="Clutch Design Engineer",
        adversary_position="Incompatible seals cause leaks and failures.",
        counter_arguments=[
            "Material selection validated with lab and field tests.",
            "OEM standards specify requirements."
        ],
        resolution_strategy="Monitor field data and update material as needed.",
        entity_scope="Transmission Clutch Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J200"
    ),
    DoctrineBlock(
        topic="Transmission Case Ventilation and Pressure Control",
        keywords=["case ventilation", "pressure control", "breather", "seal", "leak prevention"],
        conclusion_template="Ventilation system is validated if it prevents pressure buildup and seal leaks.",
        reasoning_framework=(
            "Design breather system to vent excess pressure. "
            "Test for proper function under all operating conditions. "
            "Inspect for signs of seal leaks or contamination. "
            "Reference OEM and SAE ventilation standards."
        ),
        key_factors=[
            "Breather function",
            "Pressure measurement",
            "Seal condition",
            "Contamination inspection",
            "Test results"
        ],
        primary_authority=[
            "OEM Design Standards",
            "SAE J2311"
        ],
        burden_holder="Transmission Design Engineer",
        adversary_position="Poor ventilation causes seal leaks and contamination.",
        counter_arguments=[
            "Breather design validated with pressure testing.",
            "Field data supports effectiveness."
        ],
        resolution_strategy="Include breather inspection in maintenance schedule.",
        entity_scope="Transmission Structural Components",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OEM Design Standards"
    ),
    DoctrineBlock(
        topic="Transmission Output Flange Bolt Torque Specification",
        keywords=["output flange", "bolt torque", "specification", "assembly", "service"],
        conclusion_template="Bolt torque is specified correctly if it ensures joint integrity and prevents loosening.",
        reasoning_framework=(
            "Reference OEM torque specification for output flange bolts. "
            "Use calibrated torque wrench during assembly. "
            "Document torque applied and verify with torque audit. "
            "Replace bolts if specified by OEM."
        ),
        key_factors=[
            "OEM torque spec",
            "Tool calibration",
            "Documentation",
            "Bolt condition",
            "Audit results"
        ],
        primary_authority=[
            "OEM Service Manual",
            "ISO 6789: Torque Tools"
        ],
        burden_holder="Service Technician",
        adversary_position="Incorrect torque leads to flange loosening or failure.",
        counter_arguments=[
            "Documentation and audits prevent errors.",
            "OEM specs are robust."
        ],
        resolution_strategy="Enforce torque documentation and periodic audits.",
        entity_scope="Drivetrain Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
    ),
    DoctrineBlock(
        topic="Transmission Park/Neutral Safety Switch Diagnosis",
        keywords=["park/neutral safety switch", "diagnosis", "starter interlock", "TCM", "signal integrity"],
        conclusion_template="Switch is diagnosed correctly if TCM receives accurate park/neutral status and starter interlock functions.",
        reasoning_framework=(
            "Monitor switch signal with scan tool. "
            "Verify starter only operates in park/neutral. "
            "Inspect wiring and connectors. "
            "Reference OEM diagnostic flowcharts."
        ),
        key_factors=[
            "Signal integrity",
            "Starter interlock function",
            "Wiring inspection",
            "DTC review",
            "OEM diagnostic procedure"
        ],
        primary_authority=[
            "OEM Service Manual",
            "SAE J1939"
        ],
        burden_holder="Transmission Diagnostician",
        adversary_position="Switch faults can cause no-start or safety issues.",
        counter_arguments=[
            "Live data and DTCs pinpoint most faults.",
            "Wiring inspection addresses intermittent issues."
        ],
        resolution_strategy="Replace switch and retest if faults persist.",
        entity_scope="Transmission Electronic Controls",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Service Manual"
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