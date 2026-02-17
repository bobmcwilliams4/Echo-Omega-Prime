from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="API_RP_53_BOP_MAINTENANCE",
        keywords=["BOP", "maintenance", "API RP 53", "preventive", "hydraulic", "pressure testing"],
        conclusion_template="BOP maintenance must adhere to API RP 53 guidelines, including regular pressure testing and hydraulic system inspection.",
        reasoning_framework="""
        The Blowout Preventer (BOP) is a critical safety device in drilling operations. API RP 53 outlines the minimum requirements for BOP maintenance, emphasizing the importance of regular inspections, pressure tests, and hydraulic system checks. Maintenance intervals should be determined based on operational risk, manufacturer recommendations, and historical performance data. The integrity of the BOP must be ensured through documented preventive maintenance procedures, including replacement of seals, testing of control systems, and verification of pressure ratings. Non-compliance increases the risk of catastrophic failure and regulatory penalties. Maintenance records must be retained and reviewed periodically to identify trends and potential improvements.
        """,
        key_factors=[
            "Frequency of maintenance",
            "Pressure testing intervals",
            "Hydraulic system integrity",
            "Documentation requirements",
            "Regulatory compliance"
        ],
        primary_authority=["API RP 53", "OSHA", "Manufacturer Guidelines"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Maintenance intervals can be extended based on operational experience.",
        counter_arguments=[
            "Operational experience does not supersede API RP 53 requirements.",
            "Extended intervals increase risk of undetected failures."
        ],
        resolution_strategy="Adhere strictly to API RP 53 intervals unless a risk-based justification is documented and approved.",
        entity_scope="All BOP systems on OFE07",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 53 Section 8"
    ),
    DoctrineBlock(
        topic="MUD_PUMP_FLUID_END_MAINTENANCE",
        keywords=["mud pump", "fluid end", "preventive maintenance", "valve replacement", "liner inspection"],
        conclusion_template="Mud pump fluid ends require scheduled liner and valve inspections, with replacements as per manufacturer and API recommendations.",
        reasoning_framework="""
        Mud pumps are essential for circulating drilling fluid. The fluid end is subject to high wear due to abrasive mud and pressure cycles. Preventive maintenance includes regular inspection of liners, valves, and piston assemblies. API and manufacturer guidelines specify inspection intervals and criteria for replacement. Maintenance should be scheduled based on pump hours, mud properties, and observed wear patterns. Failure to maintain fluid ends can result in loss of circulation, equipment damage, and safety incidents. Maintenance logs must be kept, and parts replaced with OEM-approved components.
        """,
        key_factors=[
            "Inspection frequency",
            "Liner wear",
            "Valve seat integrity",
            "Mud properties",
            "OEM parts usage"
        ],
        primary_authority=["API Spec 7K", "Manufacturer Guidelines"],
        burden_holder="Pump Maintenance Lead",
        adversary_position="Liners can be reused if wear is minimal.",
        counter_arguments=[
            "API and manufacturer specify minimum thickness for liners.",
            "Reusing worn liners increases risk of pump failure."
        ],
        resolution_strategy="Replace liners and valves at specified intervals or when wear exceeds limits.",
        entity_scope="Mud pumps on OFE07",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 5.3"
    ),
    DoctrineBlock(
        topic="DRAWWORKS_BRAKE_INSPECTION",
        keywords=["drawworks", "brake inspection", "preventive maintenance", "drilling rig", "safety"],
        conclusion_template="Drawworks brakes must be inspected and tested according to API and manufacturer standards to ensure operational safety.",
        reasoning_framework="""
        Drawworks brakes are critical for controlling hoisting operations. API and manufacturer standards require regular inspection of brake pads, discs, and hydraulic systems. Preventive maintenance includes checking for wear, contamination, and proper adjustment. Brake testing should be performed before each drilling operation and at scheduled intervals. Documentation of inspections and tests is mandatory. Failure to maintain brakes can result in uncontrolled hoisting, equipment damage, and personnel injury. Maintenance procedures should be reviewed and updated based on incident reports and performance data.
        """,
        key_factors=[
            "Inspection intervals",
            "Brake pad thickness",
            "Hydraulic system condition",
            "Test records",
            "Incident history"
        ],
        primary_authority=["API Spec 8C", "Manufacturer Guidelines"],
        burden_holder="Rig Maintenance Supervisor",
        adversary_position="Brake inspections can be reduced if no incidents are reported.",
        counter_arguments=[
            "Incident-free history does not eliminate risk.",
            "API requires minimum inspection intervals regardless of incident history."
        ],
        resolution_strategy="Maintain inspection schedule as per API and manufacturer; review after any incident.",
        entity_scope="Drawworks on OFE07",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 8C Section 6"
    ),
    DoctrineBlock(
        topic="CATERPILLAR_3512_3516_ENGINE_MAINTENANCE",
        keywords=["Caterpillar", "engine", "3512", "3516", "preventive maintenance", "oil change", "filter replacement"],
        conclusion_template="Caterpillar 3512/3516 engines require preventive maintenance including oil changes, filter replacements, and scheduled inspections.",
        reasoning_framework="""
        Caterpillar engines are widely used for power generation in drilling operations. Preventive maintenance is governed by manufacturer recommendations, including oil and filter changes, coolant checks, and valve adjustments. Maintenance intervals are based on engine hours, load profiles, and environmental conditions. Use of OEM parts and fluids is mandatory to maintain warranty and performance. Maintenance records must be kept and reviewed for compliance. Non-compliance can result in engine failure, downtime, and loss of warranty coverage.
        """,
        key_factors=[
            "Engine hours",
            "Oil and filter change intervals",
            "Coolant quality",
            "OEM parts usage",
            "Maintenance records"
        ],
        primary_authority=["Caterpillar Maintenance Manual", "OEM Guidelines"],
        burden_holder="Engine Maintenance Lead",
        adversary_position="Extended oil change intervals are acceptable with synthetic oils.",
        counter_arguments=[
            "Manufacturer specifies intervals regardless of oil type.",
            "Extended intervals may void warranty."
        ],
        resolution_strategy="Follow manufacturer intervals; document any deviations with risk assessment.",
        entity_scope="Caterpillar 3512/3516 engines on OFE07",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Caterpillar Maintenance Manual Section 3"
    ),
    DoctrineBlock(
        topic="API_2C_CRANE_INSPECTION",
        keywords=["crane", "API 2C", "inspection", "preventive maintenance", "lifting operations"],
        conclusion_template="Crane inspections must follow API 2C requirements, including structural, mechanical, and electrical checks.",
        reasoning_framework="""
        Cranes used in offshore operations are subject to API 2C requirements. Preventive maintenance includes structural inspection, mechanical and electrical system checks, and load testing. Inspections must be performed by qualified personnel at intervals specified by API 2C and manufacturer. Maintenance records must be kept and reviewed for compliance. Non-compliance can result in equipment failure, dropped loads, and regulatory penalties. Inspection findings must be documented and corrective actions taken before resuming operations.
        """,
        key_factors=[
            "Inspection intervals",
            "Structural integrity",
            "Mechanical and electrical system condition",
            "Load testing",
            "Qualified personnel"
        ],
        primary_authority=["API 2C", "OSHA", "Manufacturer Guidelines"],
        burden_holder="Crane Maintenance Supervisor",
        adversary_position="Visual inspections are sufficient for cranes with low utilization.",
        counter_arguments=[
            "API 2C requires comprehensive inspections regardless of utilization.",
            "Mechanical and electrical failures may not be visible."
        ],
        resolution_strategy="Perform full inspections as per API 2C; document utilization for risk assessment.",
        entity_scope="Cranes on OFE07",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 2C Section 7"
    ),
    DoctrineBlock(
        topic="PRESSURE_VESSEL_INSPECTION_NB23_API510",
        keywords=["pressure vessel", "inspection", "NB-23", "API 510", "preventive maintenance"],
        conclusion_template="Pressure vessels must be inspected as per NB-23 and API 510, including internal and external examinations.",
        reasoning_framework="""
        Pressure vessels are subject to periodic inspection under NB-23 and API 510. Inspections include internal and external examinations, thickness measurements, and pressure testing. Inspection intervals are determined by vessel type, operating conditions, and historical data. Qualified inspectors must perform examinations, and findings documented. Non-compliance can result in vessel failure, regulatory penalties, and safety incidents. Maintenance procedures should include corrective actions for any deficiencies found.
        """,
        key_factors=[
            "Inspection intervals",
            "Internal and external examination",
            "Thickness measurements",
            "Pressure testing",
            "Qualified inspectors"
        ],
        primary_authority=["NB-23", "API 510", "ASME"],
        burden_holder="Pressure Vessel Inspector",
        adversary_position="External inspections are sufficient unless internal corrosion is suspected.",
        counter_arguments=[
            "API 510 requires internal inspections at specified intervals.",
            "Internal corrosion may not be detected externally."
        ],
        resolution_strategy="Perform internal and external inspections as per API 510 and NB-23.",
        entity_scope="Pressure vessels on OFE07",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 510 Section 6"
    ),
    DoctrineBlock(
        topic="PIPING_INSPECTION_API570",
        keywords=["piping", "inspection", "API 570", "preventive maintenance", "corrosion"],
        conclusion_template="Piping systems must be inspected according to API 570, including thickness measurements and corrosion monitoring.",
        reasoning_framework="""
        API 570 governs the inspection and maintenance of piping systems. Preventive maintenance includes thickness measurements, corrosion monitoring, and leak detection. Inspection intervals are based on piping material, operating conditions, and historical data. Qualified inspectors must perform examinations, and findings documented. Non-compliance can result in leaks, environmental incidents, and regulatory penalties. Maintenance procedures should include corrective actions for any deficiencies found.
        """,
        key_factors=[
            "Inspection intervals",
            "Thickness measurements",
            "Corrosion monitoring",
            "Leak detection",
            "Qualified inspectors"
        ],
        primary_authority=["API 570", "OSHA", "ASME"],
        burden_holder="Piping Inspector",
        adversary_position="Visual inspections are sufficient for low-pressure piping.",
        counter_arguments=[
            "API 570 requires thickness measurements regardless of pressure.",
            "Corrosion may not be visible externally."
        ],
        resolution_strategy="Perform full inspections as per API 570; document risk assessment for low-pressure piping.",
        entity_scope="Piping systems on OFE07",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570 Section 5"
    ),
    DoctrineBlock(
        topic="STORAGE_TANK_INSPECTION_API653",
        keywords=["storage tank", "inspection", "API 653", "preventive maintenance", "corrosion"],
        conclusion_template="Storage tanks must be inspected as per API 653, including internal, external, and foundation checks.",
        reasoning_framework="""
        API 653 governs the inspection and maintenance of storage tanks. Preventive maintenance includes internal and external inspections, foundation checks, and corrosion monitoring. Inspection intervals are based on tank age, material, and operating conditions. Qualified inspectors must perform examinations, and findings documented. Non-compliance can result in leaks, environmental incidents, and regulatory penalties. Maintenance procedures should include corrective actions for any deficiencies found.
        """,
        key_factors=[
            "Inspection intervals",
            "Internal and external examination",
            "Foundation integrity",
            "Corrosion monitoring",
            "Qualified inspectors"
        ],
        primary_authority=["API 653", "OSHA", "ASME"],
        burden_holder="Tank Inspector",
        adversary_position="External inspections are sufficient unless leaks are detected.",
        counter_arguments=[
            "API 653 requires internal inspections at specified intervals.",
            "Leaks may not be visible externally."
        ],
        resolution_strategy="Perform internal and external inspections as per API 653.",
        entity_scope="Storage tanks on OFE07",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 653 Section 6"
    ),
    DoctrineBlock(
        topic="WIRE_ROPE_REPLACEMENT_CRITERIA",
        keywords=["wire rope", "replacement", "criteria", "inspection", "preventive maintenance"],
        conclusion_template="Wire ropes must be replaced based on API and manufacturer criteria, including broken wires, corrosion, and diameter reduction.",
        reasoning_framework="""
        Wire ropes are critical for lifting operations. API and manufacturer guidelines specify replacement criteria, including number of broken wires, corrosion, and reduction in diameter. Preventive maintenance includes regular inspection, lubrication, and tension checks. Replacement must occur when any criterion is met, regardless of operational history. Maintenance records must be kept, and only OEM-approved wire ropes used. Non-compliance can result in rope failure, dropped loads, and safety incidents.
        """,
        key_factors=[
            "Inspection intervals",
            "Broken wire count",
            "Corrosion",
            "Diameter reduction",
            "OEM parts usage"
        ],
        primary_authority=["API RP 9B", "Manufacturer Guidelines"],
        burden_holder="Lifting Equipment Supervisor",
        adversary_position="Wire ropes can be used until visible damage occurs.",
        counter_arguments=[
            "API specifies quantitative criteria for replacement.",
            "Failure to replace increases risk of rope failure."
        ],
        resolution_strategy="Replace wire ropes when any API or manufacturer criterion is met.",
        entity_scope="Wire ropes on OFE07",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 9B Section 4"
    ),
    DoctrineBlock(
        topic="TORQUE_WRENCH_CALIBRATION",
        keywords=["torque wrench", "calibration", "preventive maintenance", "accuracy", "inspection"],
        conclusion_template="Torque wrenches must be calibrated at intervals specified by manufacturer and API standards to ensure accuracy.",
        reasoning_framework="""
        Torque wrenches are used for critical bolting operations. API and manufacturer guidelines specify calibration intervals, typically every 6-12 months or after significant use. Preventive maintenance includes calibration, inspection for wear, and documentation of calibration certificates. Non-calibrated wrenches can result in inaccurate torque, leading to equipment failure or safety incidents. Maintenance records must be kept, and only calibrated wrenches used for critical operations.
        """,
        key_factors=[
            "Calibration intervals",
            "Calibration certificates",
            "Wear inspection",
            "Critical operations",
            "Documentation"
        ],
        primary_authority=["API Spec 7K", "Manufacturer Guidelines"],
        burden_holder="Tool Room Supervisor",
        adversary_position="Calibration can be skipped if wrench is used infrequently.",
        counter_arguments=[
            "API and manufacturer require calibration regardless of frequency.",
            "Infrequent use does not guarantee accuracy."
        ],
        resolution_strategy="Calibrate wrenches as per schedule; document any deviations.",
        entity_scope="Torque wrenches on OFE07",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 7"
    ),
    DoctrineBlock(
        topic="NDT_METHODS_SELECTION",
        keywords=["NDT", "non-destructive testing", "methods", "selection", "preventive maintenance"],
        conclusion_template="NDT methods must be selected based on API, ASME, and operational risk, including UT, MT, PT, and RT.",
        reasoning_framework="""
        Non-destructive testing (NDT) is used to detect flaws in critical equipment. API and ASME guidelines specify appropriate NDT methods based on material, flaw type, and operational risk. Common methods include ultrasonic testing (UT), magnetic particle testing (MT), penetrant testing (PT), and radiographic testing (RT). Selection should be based on equipment type, accessibility, and required sensitivity. Qualified personnel must perform NDT, and findings documented. Maintenance procedures should include corrective actions for any flaws detected.
        """,
        key_factors=[
            "Equipment material",
            "Flaw type",
            "Operational risk",
            "Accessibility",
            "Qualified personnel"
        ],
        primary_authority=["API RP 578", "ASME", "Manufacturer Guidelines"],
        burden_holder="NDT Supervisor",
        adversary_position="Visual inspection is sufficient for most equipment.",
        counter_arguments=[
            "API and ASME require NDT for critical equipment.",
            "Visual inspection cannot detect subsurface flaws."
        ],
        resolution_strategy="Select NDT methods based on risk and API/ASME guidelines.",
        entity_scope="Critical equipment on OFE07",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 578 Section 3"
    ),
    DoctrineBlock(
        topic="VIBRATION_ANALYSIS_ISO10816",
        keywords=["vibration analysis", "ISO 10816", "preventive maintenance", "rotating equipment", "condition monitoring"],
        conclusion_template="Vibration analysis must be performed on rotating equipment as per ISO 10816 to detect early signs of failure.",
        reasoning_framework="""
        Vibration analysis is a key tool for condition monitoring of rotating equipment. ISO 10816 specifies acceptable vibration levels and measurement techniques. Preventive maintenance includes periodic vibration measurements, trend analysis, and corrective actions for abnormal readings. Maintenance intervals are based on equipment criticality and historical data. Non-compliance can result in undetected failures, equipment damage, and safety incidents. Maintenance records must be kept, and corrective actions documented.
        """,
        key_factors=[
            "Measurement intervals",
            "Vibration levels",
            "Trend analysis",
            "Criticality",
            "Documentation"
        ],
        primary_authority=["ISO 10816", "Manufacturer Guidelines"],
        burden_holder="Condition Monitoring Lead",
        adversary_position="Vibration analysis is unnecessary for low-speed equipment.",
        counter_arguments=[
            "ISO 10816 applies to all rotating equipment.",
            "Low-speed equipment can still develop faults detectable by vibration."
        ],
        resolution_strategy="Perform vibration analysis as per ISO 10816; document exceptions.",
        entity_scope="Rotating equipment on OFE07",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10816 Section 4"
    ),
    DoctrineBlock(
        topic="OIL_ANALYSIS_PROGRAMS",
        keywords=["oil analysis", "preventive maintenance", "lubrication", "condition monitoring", "engine"],
        conclusion_template="Oil analysis programs must be implemented for engines and gearboxes to detect contamination and wear.",
        reasoning_framework="""
        Oil analysis is used to monitor the condition of lubricants and detect contamination, wear, and degradation. Preventive maintenance includes periodic sampling, laboratory analysis, and corrective actions for abnormal results. Maintenance intervals are based on equipment criticality and manufacturer recommendations. Non-compliance can result in undetected failures, equipment damage, and safety incidents. Maintenance records must be kept, and corrective actions documented.
        """,
        key_factors=[
            "Sampling intervals",
            "Contaminant detection",
            "Wear particle analysis",
            "Criticality",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "ISO 4406"],
        burden_holder="Lubrication Supervisor",
        adversary_position="Oil analysis is unnecessary if oil is changed regularly.",
        counter_arguments=[
            "Oil analysis detects issues before failure.",
            "Regular changes do not detect abnormal wear or contamination."
        ],
        resolution_strategy="Implement oil analysis programs for critical equipment.",
        entity_scope="Engines and gearboxes on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4406 Section 5"
    ),
    DoctrineBlock(
        topic="RCM_RELIABILITY_CENTERED_MAINTENANCE",
        keywords=["RCM", "reliability centered maintenance", "preventive maintenance", "risk assessment", "criticality"],
        conclusion_template="RCM principles must be applied to develop preventive maintenance programs based on risk and criticality.",
        reasoning_framework="""
        Reliability Centered Maintenance (RCM) is a systematic approach to preventive maintenance based on risk and equipment criticality. RCM principles include failure mode analysis, risk assessment, and optimization of maintenance intervals. Preventive maintenance programs should be developed using RCM to ensure resources are focused on critical equipment. Maintenance records must be kept, and programs reviewed periodically for effectiveness. Non-compliance can result in inefficient maintenance, increased downtime, and safety incidents.
        """,
        key_factors=[
            "Failure mode analysis",
            "Risk assessment",
            "Criticality ranking",
            "Maintenance interval optimization",
            "Program review"
        ],
        primary_authority=["RCM Handbook", "API RP 580"],
        burden_holder="Maintenance Manager",
        adversary_position="Traditional time-based maintenance is sufficient.",
        counter_arguments=[
            "RCM improves efficiency and reduces downtime.",
            "Time-based maintenance may not address critical risks."
        ],
        resolution_strategy="Apply RCM principles to all preventive maintenance programs.",
        entity_scope="All equipment on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 580 Section 2"
    ),
    DoctrineBlock(
        topic="HYDRAULIC_SYSTEM_FLUSHING",
        keywords=["hydraulic system", "flushing", "preventive maintenance", "contamination", "fluid replacement"],
        conclusion_template="Hydraulic systems must be flushed and fluid replaced at intervals specified by manufacturer and operational risk.",
        reasoning_framework="""
        Hydraulic systems are prone to contamination and degradation of fluids. Preventive maintenance includes periodic flushing, fluid replacement, and filter changes. Manufacturer guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and only approved fluids used. Non-compliance can result in system failure, equipment damage, and safety incidents. Maintenance procedures should include corrective actions for any contamination detected.
        """,
        key_factors=[
            "Flushing intervals",
            "Fluid quality",
            "Filter changes",
            "Contamination detection",
            "Approved fluids"
        ],
        primary_authority=["Manufacturer Guidelines", "ISO 4406"],
        burden_holder="Hydraulic System Supervisor",
        adversary_position="Flushing is unnecessary if fluid is clear.",
        counter_arguments=[
            "Contamination may not be visible.",
            "Manufacturer specifies intervals regardless of fluid appearance."
        ],
        resolution_strategy="Flush and replace fluids as per schedule; document any deviations.",
        entity_scope="Hydraulic systems on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4406 Section 6"
    ),
    DoctrineBlock(
        topic="ELECTRICAL_PANEL_INSPECTION",
        keywords=["electrical panel", "inspection", "preventive maintenance", "thermal imaging", "loose connections"],
        conclusion_template="Electrical panels must be inspected periodically, including thermal imaging and tightening of connections.",
        reasoning_framework="""
        Electrical panels are subject to preventive maintenance including visual inspection, thermal imaging, and tightening of connections. Manufacturer and NFPA guidelines specify inspection intervals and procedures. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in electrical faults, equipment damage, and safety incidents. Maintenance procedures should include documentation of thermal imaging results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Thermal imaging",
            "Connection integrity",
            "NFPA compliance",
            "Documentation"
        ],
        primary_authority=["NFPA 70B", "Manufacturer Guidelines"],
        burden_holder="Electrical Maintenance Lead",
        adversary_position="Visual inspection is sufficient unless faults are detected.",
        counter_arguments=[
            "Thermal imaging detects faults not visible externally.",
            "NFPA 70B requires periodic thermal imaging."
        ],
        resolution_strategy="Perform thermal imaging and tighten connections as per schedule.",
        entity_scope="Electrical panels on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70B Section 8"
    ),
    DoctrineBlock(
        topic="AIR_COMPRESSOR_MAINTENANCE",
        keywords=["air compressor", "preventive maintenance", "filter replacement", "oil change", "inspection"],
        conclusion_template="Air compressors require preventive maintenance including filter replacement, oil changes, and scheduled inspections.",
        reasoning_framework="""
        Air compressors are critical for pneumatic operations. Preventive maintenance includes filter replacement, oil changes, and inspection of belts and pressure relief valves. Manufacturer guidelines specify intervals based on compressor type and operational risk. Maintenance records must be kept, and only OEM-approved parts used. Non-compliance can result in compressor failure, downtime, and safety incidents. Maintenance procedures should include corrective actions for any deficiencies found.
        """,
        key_factors=[
            "Filter replacement intervals",
            "Oil change intervals",
            "Belt inspection",
            "Pressure relief valve testing",
            "OEM parts usage"
        ],
        primary_authority=["Manufacturer Guidelines", "OSHA"],
        burden_holder="Compressor Maintenance Lead",
        adversary_position="Filter replacement can be skipped if air quality is good.",
        counter_arguments=[
            "Manufacturer specifies intervals regardless of air quality.",
            "Skipping filter replacement increases risk of contamination."
        ],
        resolution_strategy="Replace filters and oil as per schedule; document any deviations.",
        entity_scope="Air compressors on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manufacturer Maintenance Manual Section 4"
    ),
    DoctrineBlock(
        topic="FIRE_SUPPRESSION_SYSTEM_INSPECTION",
        keywords=["fire suppression", "system", "inspection", "preventive maintenance", "NFPA"],
        conclusion_template="Fire suppression systems must be inspected and tested as per NFPA and manufacturer guidelines.",
        reasoning_framework="""
        Fire suppression systems are critical for safety. Preventive maintenance includes inspection, testing, and replacement of components as per NFPA and manufacturer guidelines. Maintenance intervals are based on system type and risk assessment. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, regulatory penalties, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Component testing",
            "NFPA compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["NFPA 25", "Manufacturer Guidelines"],
        burden_holder="Fire Protection Supervisor",
        adversary_position="Testing can be skipped if system is rarely activated.",
        counter_arguments=[
            "NFPA 25 requires periodic testing regardless of activation history.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test systems as per NFPA 25 and manufacturer.",
        entity_scope="Fire suppression systems on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 25 Section 5"
    ),
    DoctrineBlock(
        topic="EMERGENCY_GENERATOR_MAINTENANCE",
        keywords=["emergency generator", "preventive maintenance", "testing", "fuel system", "battery inspection"],
        conclusion_template="Emergency generators require preventive maintenance including testing, fuel system checks, and battery inspection.",
        reasoning_framework="""
        Emergency generators provide backup power during outages. Preventive maintenance includes periodic testing, inspection of fuel systems, battery checks, and oil changes. Manufacturer guidelines specify intervals based on generator type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in generator failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Testing intervals",
            "Fuel system integrity",
            "Battery inspection",
            "Oil change intervals",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "NFPA 110"],
        burden_holder="Generator Maintenance Lead",
        adversary_position="Testing can be reduced if generator is rarely used.",
        counter_arguments=[
            "NFPA 110 requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Test and maintain generators as per schedule.",
        entity_scope="Emergency generators on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 110 Section 8"
    ),
    DoctrineBlock(
        topic="COOLING_TOWER_MAINTENANCE",
        keywords=["cooling tower", "preventive maintenance", "water treatment", "inspection", "corrosion"],
        conclusion_template="Cooling towers require preventive maintenance including water treatment, inspection, and corrosion monitoring.",
        reasoning_framework="""
        Cooling towers are subject to preventive maintenance including water treatment, inspection for corrosion, and cleaning of components. Manufacturer and ASHRAE guidelines specify intervals based on tower type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in tower failure, downtime, and safety incidents. Maintenance procedures should include documentation of water treatment results and corrective actions.
        """,
        key_factors=[
            "Water treatment intervals",
            "Corrosion monitoring",
            "Component cleaning",
            "ASHRAE compliance",
            "Documentation"
        ],
        primary_authority=["ASHRAE", "Manufacturer Guidelines"],
        burden_holder="Cooling Tower Maintenance Lead",
        adversary_position="Water treatment can be skipped if water quality is good.",
        counter_arguments=[
            "ASHRAE requires periodic water treatment regardless of quality.",
            "Skipping treatment increases risk of corrosion and biological growth."
        ],
        resolution_strategy="Treat water and inspect towers as per schedule.",
        entity_scope="Cooling towers on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASHRAE Section 5"
    ),
    DoctrineBlock(
        topic="FUEL_SYSTEM_LEAK_DETECTION",
        keywords=["fuel system", "leak detection", "preventive maintenance", "inspection", "environmental"],
        conclusion_template="Fuel systems must be inspected for leaks and integrity as per API and manufacturer guidelines.",
        reasoning_framework="""
        Fuel systems are subject to preventive maintenance including leak detection, inspection of tanks and lines, and testing of containment systems. API and manufacturer guidelines specify intervals based on system type and environmental risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in environmental incidents, equipment damage, and regulatory penalties. Maintenance procedures should include documentation of inspection results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Leak detection methods",
            "Containment system integrity",
            "Environmental risk",
            "Documentation"
        ],
        primary_authority=["API RP 1631", "Manufacturer Guidelines"],
        burden_holder="Fuel System Supervisor",
        adversary_position="Leak detection can be skipped if no leaks are reported.",
        counter_arguments=[
            "API RP 1631 requires periodic leak detection.",
            "Leaks may not be detected without proper testing."
        ],
        resolution_strategy="Inspect and test fuel systems as per schedule.",
        entity_scope="Fuel systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 1631 Section 4"
    ),
    DoctrineBlock(
        topic="HEAT_EXCHANGER_TUBE_CLEANING",
        keywords=["heat exchanger", "tube cleaning", "preventive maintenance", "fouling", "inspection"],
        conclusion_template="Heat exchangers require periodic tube cleaning and inspection to prevent fouling and maintain efficiency.",
        reasoning_framework="""
        Heat exchangers are subject to preventive maintenance including tube cleaning, inspection for fouling, and pressure testing. Manufacturer and ASME guidelines specify intervals based on exchanger type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in reduced efficiency, equipment damage, and safety incidents. Maintenance procedures should include documentation of cleaning results and corrective actions.
        """,
        key_factors=[
            "Cleaning intervals",
            "Fouling detection",
            "Pressure testing",
            "ASME compliance",
            "Documentation"
        ],
        primary_authority=["ASME", "Manufacturer Guidelines"],
        burden_holder="Heat Exchanger Maintenance Lead",
        adversary_position="Cleaning can be skipped if pressure drop is minimal.",
        counter_arguments=[
            "Fouling may not cause immediate pressure drop.",
            "ASME requires periodic cleaning regardless of pressure drop."
        ],
        resolution_strategy="Clean and inspect tubes as per schedule.",
        entity_scope="Heat exchangers on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME Section 6"
    ),
    DoctrineBlock(
        topic="VALVE_ACTUATOR_MAINTENANCE",
        keywords=["valve actuator", "preventive maintenance", "inspection", "testing", "OEM"],
        conclusion_template="Valve actuators require preventive maintenance including inspection, testing, and lubrication as per OEM guidelines.",
        reasoning_framework="""
        Valve actuators are subject to preventive maintenance including inspection, testing, and lubrication. OEM guidelines specify intervals based on actuator type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in actuator failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of inspection and test results.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Lubrication",
            "OEM compliance",
            "Documentation"
        ],
        primary_authority=["OEM Guidelines", "API Spec 6A"],
        burden_holder="Valve Maintenance Lead",
        adversary_position="Testing can be skipped if actuator is rarely used.",
        counter_arguments=[
            "API Spec 6A requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test actuators as per schedule.",
        entity_scope="Valve actuators on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 6A Section 8"
    ),
    DoctrineBlock(
        topic="INSTRUMENTATION_CALIBRATION",
        keywords=["instrumentation", "calibration", "preventive maintenance", "accuracy", "inspection"],
        conclusion_template="Instrumentation must be calibrated at intervals specified by manufacturer and API standards to ensure accuracy.",
        reasoning_framework="""
        Instrumentation is used for critical measurements in drilling operations. API and manufacturer guidelines specify calibration intervals, typically every 6-12 months or after significant use. Preventive maintenance includes calibration, inspection for wear, and documentation of calibration certificates. Non-calibrated instruments can result in inaccurate measurements, leading to equipment failure or safety incidents. Maintenance records must be kept, and only calibrated instruments used for critical operations.
        """,
        key_factors=[
            "Calibration intervals",
            "Calibration certificates",
            "Wear inspection",
            "Critical operations",
            "Documentation"
        ],
        primary_authority=["API Spec 7K", "Manufacturer Guidelines"],
        burden_holder="Instrumentation Supervisor",
        adversary_position="Calibration can be skipped if instrument is used infrequently.",
        counter_arguments=[
            "API and manufacturer require calibration regardless of frequency.",
            "Infrequent use does not guarantee accuracy."
        ],
        resolution_strategy="Calibrate instruments as per schedule; document any deviations.",
        entity_scope="Instrumentation on OFE07",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 7"
    ),
    DoctrineBlock(
        topic="PNEUMATIC_SYSTEM_LEAK_TESTING",
        keywords=["pneumatic system", "leak testing", "preventive maintenance", "inspection", "pressure"],
        conclusion_template="Pneumatic systems must be leak tested and inspected at intervals specified by manufacturer and API standards.",
        reasoning_framework="""
        Pneumatic systems are subject to preventive maintenance including leak testing, inspection of lines and valves, and pressure testing. Manufacturer and API guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Leak testing intervals",
            "Pressure testing",
            "Line and valve inspection",
            "API compliance",
            "Documentation"
        ],
        primary_authority=["API Spec 7K", "Manufacturer Guidelines"],
        burden_holder="Pneumatic System Supervisor",
        adversary_position="Leak testing can be skipped if system is rarely used.",
        counter_arguments=[
            "API Spec 7K requires periodic leak testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Test and inspect pneumatic systems as per schedule.",
        entity_scope="Pneumatic systems on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 8"
    ),
    DoctrineBlock(
        topic="ROTATING_EQUIPMENT_ALIGNMENT",
        keywords=["rotating equipment", "alignment", "preventive maintenance", "inspection", "vibration"],
        conclusion_template="Rotating equipment must be aligned and inspected at intervals specified by manufacturer and ISO standards.",
        reasoning_framework="""
        Rotating equipment is subject to preventive maintenance including alignment checks, inspection for vibration, and correction of misalignment. Manufacturer and ISO guidelines specify intervals based on equipment type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in equipment failure, downtime, and safety incidents. Maintenance procedures should include documentation of alignment results and corrective actions.
        """,
        key_factors=[
            "Alignment intervals",
            "Vibration monitoring",
            "Correction of misalignment",
            "ISO compliance",
            "Documentation"
        ],
        primary_authority=["ISO 10816", "Manufacturer Guidelines"],
        burden_holder="Rotating Equipment Supervisor",
        adversary_position="Alignment can be skipped if vibration is low.",
        counter_arguments=[
            "ISO 10816 requires periodic alignment regardless of vibration.",
            "Misalignment may not cause immediate vibration."
        ],
        resolution_strategy="Align and inspect equipment as per schedule.",
        entity_scope="Rotating equipment on OFE07",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10816 Section 5"
    ),
    DoctrineBlock(
        topic="STEAM_BOILER_INSPECTION",
        keywords=["steam boiler", "inspection", "preventive maintenance", "ASME", "pressure testing"],
        conclusion_template="Steam boilers must be inspected and pressure tested at intervals specified by ASME and manufacturer guidelines.",
        reasoning_framework="""
        Steam boilers are subject to preventive maintenance including inspection, pressure testing, and cleaning. ASME and manufacturer guidelines specify intervals based on boiler type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in boiler failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Pressure testing",
            "Cleaning",
            "ASME compliance",
            "Documentation"
        ],
        primary_authority=["ASME", "Manufacturer Guidelines"],
        burden_holder="Boiler Maintenance Lead",
        adversary_position="Pressure testing can be skipped if boiler is rarely used.",
        counter_arguments=[
            "ASME requires periodic pressure testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test boilers as per schedule.",
        entity_scope="Steam boilers on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME Section 7"
    ),
    DoctrineBlock(
        topic="WATER_TREATMENT_SYSTEM_MAINTENANCE",
        keywords=["water treatment", "system", "maintenance", "preventive", "inspection"],
        conclusion_template="Water treatment systems require preventive maintenance including inspection, testing, and component replacement.",
        reasoning_framework="""
        Water treatment systems are subject to preventive maintenance including inspection, testing of water quality, and replacement of components. Manufacturer and EPA guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Water quality testing",
            "Component replacement",
            "EPA compliance",
            "Documentation"
        ],
        primary_authority=["EPA", "Manufacturer Guidelines"],
        burden_holder="Water Treatment Supervisor",
        adversary_position="Testing can be skipped if water quality is good.",
        counter_arguments=[
            "EPA requires periodic testing regardless of quality.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test water treatment systems as per schedule.",
        entity_scope="Water treatment systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Section 3"
    ),
    DoctrineBlock(
        topic="EMERGENCY_SHUTDOWN_SYSTEM_TESTING",
        keywords=["emergency shutdown", "system", "testing", "preventive maintenance", "API"],
        conclusion_template="Emergency shutdown systems must be tested at intervals specified by API and manufacturer guidelines.",
        reasoning_framework="""
        Emergency shutdown systems are critical for safety. Preventive maintenance includes periodic testing, inspection of components, and documentation of test results. API and manufacturer guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, regulatory penalties, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Testing intervals",
            "Component inspection",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API RP 14C", "Manufacturer Guidelines"],
        burden_holder="Shutdown System Supervisor",
        adversary_position="Testing can be skipped if system is rarely activated.",
        counter_arguments=[
            "API RP 14C requires periodic testing regardless of activation history.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Test and inspect shutdown systems as per schedule.",
        entity_scope="Emergency shutdown systems on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 14C Section 5"
    ),
    DoctrineBlock(
        topic="GAS_DETECTION_SYSTEM_CALIBRATION",
        keywords=["gas detection", "system", "calibration", "preventive maintenance", "testing"],
        conclusion_template="Gas detection systems must be calibrated and tested at intervals specified by manufacturer and API guidelines.",
        reasoning_framework="""
        Gas detection systems are critical for safety. Preventive maintenance includes calibration, testing, and inspection of sensors. Manufacturer and API guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, regulatory penalties, and safety incidents. Maintenance procedures should include documentation of calibration and test results.
        """,
        key_factors=[
            "Calibration intervals",
            "Sensor testing",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API RP 14E", "Manufacturer Guidelines"],
        burden_holder="Gas Detection Supervisor",
        adversary_position="Calibration can be skipped if system is rarely activated.",
        counter_arguments=[
            "API RP 14E requires periodic calibration regardless of activation history.",
            "Skipping calibration increases risk of undetected failures."
        ],
        resolution_strategy="Calibrate and test gas detection systems as per schedule.",
        entity_scope="Gas detection systems on OFE07",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 14E Section 6"
    ),
    DoctrineBlock(
        topic="LIGHTING_SYSTEM_INSPECTION",
        keywords=["lighting system", "inspection", "preventive maintenance", "testing", "safety"],
        conclusion_template="Lighting systems must be inspected and tested at intervals specified by manufacturer and OSHA guidelines.",
        reasoning_framework="""
        Lighting systems are critical for safety and operational visibility. Preventive maintenance includes inspection, testing, and replacement of components. Manufacturer and OSHA guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Component testing",
            "OSHA compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["OSHA", "Manufacturer Guidelines"],
        burden_holder="Lighting System Supervisor",
        adversary_position="Testing can be skipped if system is rarely used.",
        counter_arguments=[
            "OSHA requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test lighting systems as per schedule.",
        entity_scope="Lighting systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Section 4"
    ),
    DoctrineBlock(
        topic="SAFETY_VALVE_TESTING",
        keywords=["safety valve", "testing", "preventive maintenance", "inspection", "API"],
        conclusion_template="Safety valves must be tested and inspected at intervals specified by API and manufacturer guidelines.",
        reasoning_framework="""
        Safety valves are critical for pressure relief. Preventive maintenance includes testing, inspection, and replacement of components. API and manufacturer guidelines specify intervals based on valve type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in valve failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Testing intervals",
            "Component inspection",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API RP 576", "Manufacturer Guidelines"],
        burden_holder="Safety Valve Supervisor",
        adversary_position="Testing can be skipped if valve is rarely activated.",
        counter_arguments=[
            "API RP 576 requires periodic testing regardless of activation history.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Test and inspect safety valves as per schedule.",
        entity_scope="Safety valves on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 576 Section 5"
    ),
    DoctrineBlock(
        topic="HOIST_SYSTEM_MAINTENANCE",
        keywords=["hoist system", "maintenance", "preventive", "inspection", "testing"],
        conclusion_template="Hoist systems require preventive maintenance including inspection, testing, and lubrication as per API and manufacturer guidelines.",
        reasoning_framework="""
        Hoist systems are critical for lifting operations. Preventive maintenance includes inspection, testing, and lubrication. API and manufacturer guidelines specify intervals based on hoist type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in hoist failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Lubrication",
            "API compliance",
            "Documentation"
        ],
        primary_authority=["API Spec 8C", "Manufacturer Guidelines"],
        burden_holder="Hoist Maintenance Lead",
        adversary_position="Testing can be skipped if hoist is rarely used.",
        counter_arguments=[
            "API Spec 8C requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test hoist systems as per schedule.",
        entity_scope="Hoist systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 8C Section 7"
    ),
    DoctrineBlock(
        topic="INTEGRATED_CONTROL_SYSTEM_MAINTENANCE",
        keywords=["integrated control system", "maintenance", "preventive", "inspection", "testing"],
        conclusion_template="Integrated control systems require preventive maintenance including inspection, testing, and software updates as per manufacturer guidelines.",
        reasoning_framework="""
        Integrated control systems are critical for operational safety and efficiency. Preventive maintenance includes inspection, testing, and software updates. Manufacturer guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Software updates",
            "Manufacturer compliance",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "API RP 14C"],
        burden_holder="Control System Supervisor",
        adversary_position="Testing can be skipped if system is rarely used.",
        counter_arguments=[
            "API RP 14C requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test control systems as per schedule.",
        entity_scope="Integrated control systems on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 14C Section 7"
    ),
    DoctrineBlock(
        topic="PERSONNEL_PROTECTION_EQUIPMENT_INSPECTION",
        keywords=["personnel protection equipment", "inspection", "preventive maintenance", "testing", "OSHA"],
        conclusion_template="Personnel protection equipment must be inspected and tested at intervals specified by OSHA and manufacturer guidelines.",
        reasoning_framework="""
        Personnel protection equipment is critical for safety. Preventive maintenance includes inspection, testing, and replacement of components. OSHA and manufacturer guidelines specify intervals based on equipment type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in equipment failure, regulatory penalties, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "OSHA compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["OSHA", "Manufacturer Guidelines"],
        burden_holder="PPE Supervisor",
        adversary_position="Testing can be skipped if equipment is rarely used.",
        counter_arguments=[
            "OSHA requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test PPE as per schedule.",
        entity_scope="Personnel protection equipment on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Section 5"
    ),
    DoctrineBlock(
        topic="EMERGENCY_EGRESS_ROUTE_INSPECTION",
        keywords=["emergency egress", "route", "inspection", "preventive maintenance", "OSHA"],
        conclusion_template="Emergency egress routes must be inspected and maintained at intervals specified by OSHA and company policy.",
        reasoning_framework="""
        Emergency egress routes are critical for safety. Preventive maintenance includes inspection, maintenance of signage and lighting, and removal of obstructions. OSHA and company policy specify intervals based on operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in regulatory penalties and safety incidents. Maintenance procedures should include documentation of inspection results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Signage and lighting maintenance",
            "Obstruction removal",
            "OSHA compliance",
            "Documentation"
        ],
        primary_authority=["OSHA", "Company Policy"],
        burden_holder="Safety Supervisor",
        adversary_position="Inspection can be skipped if routes are rarely used.",
        counter_arguments=[
            "OSHA requires periodic inspection regardless of use.",
            "Skipping inspection increases risk of undetected deficiencies."
        ],
        resolution_strategy="Inspect and maintain egress routes as per schedule.",
        entity_scope="Emergency egress routes on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Section 6"
    ),
    DoctrineBlock(
        topic="LIFTING_GEAR_CERTIFICATION",
        keywords=["lifting gear", "certification", "inspection", "preventive maintenance", "API"],
        conclusion_template="Lifting gear must be certified and inspected at intervals specified by API and manufacturer guidelines.",
        reasoning_framework="""
        Lifting gear is critical for safe lifting operations. Preventive maintenance includes inspection, certification, and replacement of components. API and manufacturer guidelines specify intervals based on gear type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in equipment failure, regulatory penalties, and safety incidents. Maintenance procedures should include documentation of certification and inspection results.
        """,
        key_factors=[
            "Certification intervals",
            "Inspection procedures",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API Spec 8C", "Manufacturer Guidelines"],
        burden_holder="Lifting Gear Supervisor",
        adversary_position="Certification can be skipped if gear is rarely used.",
        counter_arguments=[
            "API Spec 8C requires periodic certification regardless of use.",
            "Skipping certification increases risk of undetected failures."
        ],
        resolution_strategy="Certify and inspect lifting gear as per schedule.",
        entity_scope="Lifting gear on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 8C Section 8"
    ),
    DoctrineBlock(
        topic="DRILL_PIPE_INSPECTION",
        keywords=["drill pipe", "inspection", "preventive maintenance", "API", "NDT"],
        conclusion_template="Drill pipes must be inspected and tested at intervals specified by API and manufacturer guidelines, including NDT methods.",
        reasoning_framework="""
        Drill pipes are subject to preventive maintenance including inspection, testing, and NDT methods. API and manufacturer guidelines specify intervals based on pipe type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in pipe failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "NDT methods",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API Spec 5DP", "Manufacturer Guidelines"],
        burden_holder="Drill Pipe Supervisor",
        adversary_position="Testing can be skipped if pipe is rarely used.",
        counter_arguments=[
            "API Spec 5DP requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test drill pipes as per schedule.",
        entity_scope="Drill pipes on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 5DP Section 6"
    ),
    DoctrineBlock(
        topic="MOTOR_CONTROL_CENTER_MAINTENANCE",
        keywords=["motor control center", "maintenance", "preventive", "inspection", "testing"],
        conclusion_template="Motor control centers require preventive maintenance including inspection, testing, and cleaning as per manufacturer guidelines.",
        reasoning_framework="""
        Motor control centers are critical for electrical distribution. Preventive maintenance includes inspection, testing, and cleaning. Manufacturer guidelines specify intervals based on center type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Cleaning",
            "Manufacturer compliance",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "NFPA 70B"],
        burden_holder="Electrical Maintenance Lead",
        adversary_position="Testing can be skipped if center is rarely used.",
        counter_arguments=[
            "NFPA 70B requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test motor control centers as per schedule.",
        entity_scope="Motor control centers on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70B Section 9"
    ),
    DoctrineBlock(
        topic="PIPE_SUPPORT_INSPECTION",
        keywords=["pipe support", "inspection", "preventive maintenance", "API", "corrosion"],
        conclusion_template="Pipe supports must be inspected and maintained at intervals specified by API and manufacturer guidelines.",
        reasoning_framework="""
        Pipe supports are critical for maintaining piping integrity. Preventive maintenance includes inspection, corrosion monitoring, and replacement of components. API and manufacturer guidelines specify intervals based on support type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in piping failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of inspection results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Corrosion monitoring",
            "Component replacement",
            "API compliance",
            "Documentation"
        ],
        primary_authority=["API 570", "Manufacturer Guidelines"],
        burden_holder="Piping Inspector",
        adversary_position="Inspection can be skipped if supports are rarely used.",
        counter_arguments=[
            "API 570 requires periodic inspection regardless of use.",
            "Skipping inspection increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and maintain pipe supports as per schedule.",
        entity_scope="Pipe supports on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570 Section 6"
    ),
    DoctrineBlock(
        topic="CORROSION_MONITORING_PROGRAMS",
        keywords=["corrosion monitoring", "program", "preventive maintenance", "inspection", "API"],
        conclusion_template="Corrosion monitoring programs must be implemented for critical equipment as per API and manufacturer guidelines.",
        reasoning_framework="""
        Corrosion monitoring is critical for equipment longevity. Preventive maintenance includes implementation of monitoring programs, inspection, and corrective actions. API and manufacturer guidelines specify intervals based on equipment type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in equipment failure, downtime, and safety incidents. Maintenance procedures should include documentation of monitoring results and corrective actions.
        """,
        key_factors=[
            "Monitoring intervals",
            "Inspection procedures",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API 570", "Manufacturer Guidelines"],
        burden_holder="Corrosion Monitoring Lead",
        adversary_position="Monitoring can be skipped if equipment is rarely used.",
        counter_arguments=[
            "API 570 requires periodic monitoring regardless of use.",
            "Skipping monitoring increases risk of undetected failures."
        ],
        resolution_strategy="Implement and maintain corrosion monitoring programs as per schedule.",
        entity_scope="Critical equipment on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570 Section 7"
    ),
    DoctrineBlock(
        topic="STRUCTURAL_INTEGRITY_INSPECTION",
        keywords=["structural integrity", "inspection", "preventive maintenance", "API", "NDT"],
        conclusion_template="Structural integrity inspections must be performed at intervals specified by API and manufacturer guidelines, including NDT methods.",
        reasoning_framework="""
        Structural integrity is critical for operational safety. Preventive maintenance includes inspection, NDT methods, and corrective actions. API and manufacturer guidelines specify intervals based on structure type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in structural failure, equipment damage, and safety incidents. Maintenance procedures should include documentation of inspection and NDT results.
        """,
        key_factors=[
            "Inspection intervals",
            "NDT methods",
            "API compliance",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["API RP 2A", "Manufacturer Guidelines"],
        burden_holder="Structural Inspector",
        adversary_position="NDT can be skipped if structure is rarely used.",
        counter_arguments=[
            "API RP 2A requires periodic NDT regardless of use.",
            "Skipping NDT increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test structures as per schedule.",
        entity_scope="Structures on OFE07",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 2A Section 8"
    ),
    DoctrineBlock(
        topic="AIR_HANDLING_UNIT_MAINTENANCE",
        keywords=["air handling unit", "maintenance", "preventive", "inspection", "filter replacement"],
        conclusion_template="Air handling units require preventive maintenance including filter replacement, inspection, and cleaning as per manufacturer guidelines.",
        reasoning_framework="""
        Air handling units are critical for HVAC operations. Preventive maintenance includes filter replacement, inspection, and cleaning. Manufacturer guidelines specify intervals based on unit type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in unit failure, downtime, and safety incidents. Maintenance procedures should include documentation of filter replacement and inspection results.
        """,
        key_factors=[
            "Filter replacement intervals",
            "Inspection procedures",
            "Cleaning",
            "Manufacturer compliance",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "ASHRAE"],
        burden_holder="HVAC Maintenance Lead",
        adversary_position="Filter replacement can be skipped if air quality is good.",
        counter_arguments=[
            "ASHRAE requires periodic filter replacement regardless of quality.",
            "Skipping replacement increases risk of contamination."
        ],
        resolution_strategy="Replace filters and inspect units as per schedule.",
        entity_scope="Air handling units on OFE07",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASHRAE Section 6"
    ),
    DoctrineBlock(
        topic="BATTERY_SYSTEM_MAINTENANCE",
        keywords=["battery system", "maintenance", "preventive", "inspection", "testing"],
        conclusion_template="Battery systems require preventive maintenance including inspection, testing, and replacement as per manufacturer guidelines.",
        reasoning_framework="""
        Battery systems are critical for backup power. Preventive maintenance includes inspection, testing, and replacement. Manufacturer guidelines specify intervals based on battery type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Replacement",
            "Manufacturer compliance",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "NFPA 70B"],
        burden_holder="Battery System Supervisor",
        adversary_position="Testing can be skipped if system is rarely used.",
        counter_arguments=[
            "NFPA 70B requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test battery systems as per schedule.",
        entity_scope="Battery systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 70B Section 10"
    ),
    DoctrineBlock(
        topic="EMERGENCY_COMMUNICATION_SYSTEM_MAINTENANCE",
        keywords=["emergency communication", "system", "maintenance", "preventive", "inspection"],
        conclusion_template="Emergency communication systems require preventive maintenance including inspection, testing, and software updates as per manufacturer guidelines.",
        reasoning_framework="""
        Emergency communication systems are critical for operational safety. Preventive maintenance includes inspection, testing, and software updates. Manufacturer guidelines specify intervals based on system type and operational risk. Maintenance records must be kept, and corrective actions taken for any deficiencies found. Non-compliance can result in system failure, downtime, and safety incidents. Maintenance procedures should include documentation of test results and corrective actions.
        """,
        key_factors=[
            "Inspection intervals",
            "Testing procedures",
            "Software updates",
            "Manufacturer compliance",
            "Documentation"
        ],
        primary_authority=["Manufacturer Guidelines", "NFPA 72"],
        burden_holder="Communication System Supervisor",
        adversary_position="Testing can be skipped if system is rarely used.",
        counter_arguments=[
            "NFPA 72 requires periodic testing regardless of use.",
            "Skipping tests increases risk of undetected failures."
        ],
        resolution_strategy="Inspect and test communication systems as per schedule.",
        entity_scope="Emergency communication systems on OFE07",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 72 Section 8"
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