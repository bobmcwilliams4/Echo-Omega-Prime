from dataclasses import dataclass
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
        topic="API 6A Pressure Rating Selection",
        keywords=["API 6A", "pressure rating", "wellhead", "OFE08", "9008", "design pressure", "working pressure"],
        conclusion_template="The selected pressure rating for OFE08 wellhead equipment must comply with API 6A standards and be validated against maximum anticipated well pressures.",
        reasoning_framework=(
            "Pressure rating selection is governed by API 6A, which stipulates that wellhead equipment must be rated "
            "for the maximum expected well pressure plus a safety margin. The process involves evaluating reservoir data, "
            "anticipated shut-in pressures, and transient events. The engineer must cross-reference the design pressure "
            "with API 6A pressure rating tables (e.g., 2,000 psi to 20,000 psi). Material selection, temperature derating, "
            "and compatibility with downstream equipment must be considered. Pressure testing protocols and historical "
            "failure modes are reviewed. The final rating is documented and justified in the engineering dossier, "
            "with sign-off from technical authorities."
        ),
        key_factors=[
            "Maximum anticipated well pressure",
            "API 6A pressure rating tables",
            "Material compatibility",
            "Temperature derating",
            "Safety margin",
            "Pressure testing requirements"
        ],
        primary_authority=["API 6A", "Company Engineering Standards", "Local Regulatory Authority"],
        burden_holder="Design Engineer",
        adversary_position="Pressure rating is excessive and increases cost; lower rating is sufficient.",
        counter_arguments=[
            "Lower ratings may compromise safety during abnormal pressure events.",
            "API 6A mandates pressure ratings based on maximum anticipated pressure, not average.",
            "Historical incidents show failures due to under-rated equipment."
        ],
        resolution_strategy="Pressure rating is selected based on highest credible well pressure, validated by reservoir engineering and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 4.1.2"
    ),
    DoctrineBlock(
        topic="Material Class Selection (API 6A)",
        keywords=["API 6A", "material class", "wellhead", "corrosion", "H2S", "CO2", "OFE08"],
        conclusion_template="Material class for OFE08 wellhead must be selected per API 6A based on fluid composition and environmental conditions.",
        reasoning_framework=(
            "API 6A defines material classes (AA, BB, CC, DD, EE, FF) based on resistance to corrosion, sour service, "
            "and mechanical properties. Selection requires analysis of produced fluids (H2S, CO2, chlorides), temperature, "
            "and pressure. NACE MR0175/ISO 15156 is referenced for sour service. Material traceability, certification, "
            "and compatibility with seals and coatings are reviewed. The engineer documents the rationale, including "
            "test data and supplier certifications. Final selection is approved by materials engineering and verified "
            "against API 6A Annex A."
        ),
        key_factors=[
            "Fluid composition (H2S, CO2, chlorides)",
            "API 6A material class definitions",
            "NACE MR0175/ISO 15156 compliance",
            "Temperature and pressure",
            "Supplier certification"
        ],
        primary_authority=["API 6A", "NACE MR0175/ISO 15156", "Company Materials Standard"],
        burden_holder="Materials Engineer",
        adversary_position="Material class is over-specified; lower grade is acceptable.",
        counter_arguments=[
            "Sour service requires higher material class per API 6A and NACE.",
            "Lower grade increases risk of corrosion and catastrophic failure.",
            "Regulatory authorities mandate compliance for sour wells."
        ],
        resolution_strategy="Material class is selected based on worst-case fluid composition and API 6A/NACE requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Annex A"
    ),
    DoctrineBlock(
        topic="PSL (Product Specification Level) Requirements",
        keywords=["API 6A", "PSL", "product specification level", "wellhead", "OFE08", "9008", "quality"],
        conclusion_template="OFE08 wellhead equipment must meet PSL requirements as defined by API 6A based on well criticality and regulatory mandates.",
        reasoning_framework=(
            "Product Specification Level (PSL) is defined in API 6A to specify the level of quality, testing, and documentation required. "
            "PSL 1 is basic; PSL 2 and PSL 3 require enhanced testing, traceability, and documentation. Selection is based on well criticality, "
            "service environment, and regulatory requirements. PSL 3 is mandated for high-pressure, sour service, or critical wells. "
            "The engineer reviews project specifications, regulatory guidance, and risk assessments. Documentation includes test reports, "
            "material certificates, and inspection records. Final PSL is approved by QA/QC and documented in the project dossier."
        ),
        key_factors=[
            "Well criticality",
            "Service environment",
            "Regulatory requirements",
            "API 6A PSL definitions",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards", "Local Regulatory Authority"],
        burden_holder="QA/QC Engineer",
        adversary_position="PSL 3 is unnecessary; PSL 2 is sufficient for this well.",
        counter_arguments=[
            "Critical wells require PSL 3 for enhanced safety and reliability.",
            "Regulatory authorities may mandate PSL 3 for sour or high-pressure wells.",
            "PSL 2 lacks traceability and testing required for critical applications."
        ],
        resolution_strategy="PSL is selected based on risk assessment, regulatory mandates, and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 5"
    ),
    DoctrineBlock(
        topic="Casing Head (Braden Head) Configuration",
        keywords=["casing head", "Braden head", "wellhead", "OFE08", "configuration", "API 6A"],
        conclusion_template="Casing head configuration for OFE08 must be selected based on casing program, pressure rating, and API 6A compliance.",
        reasoning_framework=(
            "Casing head (Braden head) configuration is determined by the casing program, anticipated pressures, and API 6A requirements. "
            "The engineer reviews well design, casing sizes, and load conditions. Selection includes consideration of slip vs mandrel hangers, "
            "seal technology, and connection type (flanged vs studded). Pressure rating and material class are validated. "
            "Installation procedures, test protocols, and compatibility with downstream equipment are documented. Final configuration is "
            "approved by well engineering and verified against API 6A Section 6."
        ),
        key_factors=[
            "Casing program",
            "Pressure rating",
            "API 6A compliance",
            "Seal technology",
            "Connection type"
        ],
        primary_authority=["API 6A", "Company Well Design Standard"],
        burden_holder="Well Engineer",
        adversary_position="Alternative configuration is more cost-effective and meets minimum requirements.",
        counter_arguments=[
            "Cost-effective alternatives may compromise seal integrity and pressure containment.",
            "API 6A mandates specific configurations for certain casing sizes and pressures.",
            "Historical failures linked to improper configuration."
        ],
        resolution_strategy="Configuration is selected based on casing program, API 6A requirements, and risk assessment.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 6"
    ),
    DoctrineBlock(
        topic="Tubing Head Spool and Hanger",
        keywords=["tubing head", "spool", "hanger", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Tubing head spool and hanger selection for OFE08 must comply with API 6A and be compatible with tubing program and well conditions.",
        reasoning_framework=(
            "Tubing head spool and hanger selection is governed by API 6A, requiring compatibility with tubing size, load, and pressure rating. "
            "The engineer evaluates tubing program, anticipated loads, seal requirements, and hanger type (slip vs mandrel). "
            "Material class and PSL are validated. Installation and retrieval procedures are reviewed. Documentation includes "
            "test reports and supplier certifications. Final selection is approved by well engineering and QA/QC."
        ),
        key_factors=[
            "Tubing size and program",
            "Pressure rating",
            "Hanger type",
            "Seal requirements",
            "Material class"
        ],
        primary_authority=["API 6A", "Company Tubing Standards"],
        burden_holder="Well Engineer",
        adversary_position="Mandrel hangers are unnecessary; slip hangers suffice.",
        counter_arguments=[
            "Mandrel hangers provide superior sealing and load capacity.",
            "API 6A mandates hanger selection based on well conditions.",
            "Slip hangers may compromise seal integrity in high-pressure wells."
        ],
        resolution_strategy="Hanger type is selected based on tubing program, API 6A requirements, and risk assessment.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 7"
    ),
    DoctrineBlock(
        topic="Christmas Tree Selection (Vertical vs Horizontal)",
        keywords=["Christmas tree", "vertical", "horizontal", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Christmas tree configuration for OFE08 must be selected based on well type, intervention requirements, and API 6A compliance.",
        reasoning_framework=(
            "Christmas tree selection (vertical vs horizontal) depends on well type (surface vs subsea), intervention requirements, and API 6A standards. "
            "Vertical trees are preferred for surface wells due to ease of access and maintenance. Horizontal trees are used for subsea wells to facilitate "
            "intervention and flow control. The engineer evaluates well geometry, intervention frequency, and compatibility with completion equipment. "
            "Pressure rating, material class, and PSL are validated. Documentation includes risk assessment and operational procedures."
        ),
        key_factors=[
            "Well type (surface vs subsea)",
            "Intervention requirements",
            "API 6A compliance",
            "Pressure rating",
            "Material class"
        ],
        primary_authority=["API 6A", "Company Completion Standards"],
        burden_holder="Completion Engineer",
        adversary_position="Vertical tree is sufficient for all wells; horizontal tree adds unnecessary complexity.",
        counter_arguments=[
            "Horizontal trees are required for subsea wells to facilitate intervention.",
            "API 6A mandates tree selection based on well type and intervention needs.",
            "Vertical trees may limit access in subsea environments."
        ],
        resolution_strategy="Tree configuration is selected based on well type, intervention requirements, and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 8"
    ),
    DoctrineBlock(
        topic="Choke Valve Selection (Positive vs Adjustable)",
        keywords=["choke valve", "positive", "adjustable", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Choke valve type for OFE08 must be selected based on flow control requirements, operational flexibility, and API 6A compliance.",
        reasoning_framework=(
            "Choke valve selection (positive vs adjustable) is governed by API 6A and operational requirements. Positive chokes provide fixed flow rates "
            "and are used for stable wells. Adjustable chokes offer flexibility for variable flow and intervention. The engineer evaluates well flow profile, "
            "pressure rating, material class, and maintenance requirements. Documentation includes risk assessment and operational procedures. Final selection "
            "is approved by production engineering and QA/QC."
        ),
        key_factors=[
            "Flow control requirements",
            "Operational flexibility",
            "API 6A compliance",
            "Pressure rating",
            "Maintenance requirements"
        ],
        primary_authority=["API 6A", "Company Production Standards"],
        burden_holder="Production Engineer",
        adversary_position="Positive chokes are sufficient; adjustable chokes increase complexity and cost.",
        counter_arguments=[
            "Adjustable chokes provide operational flexibility for variable flow.",
            "API 6A mandates choke selection based on flow control requirements.",
            "Positive chokes may limit intervention and flow optimization."
        ],
        resolution_strategy="Choke type is selected based on flow control requirements, operational flexibility, and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 9"
    ),
    DoctrineBlock(
        topic="Wellhead Seal Technology (Metal vs Elastomeric)",
        keywords=["seal technology", "metal", "elastomeric", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Seal technology for OFE08 wellhead must be selected based on pressure, temperature, and compatibility with fluids per API 6A.",
        reasoning_framework=(
            "Seal technology selection (metal vs elastomeric) is governed by API 6A and well conditions. Metal seals provide superior pressure and temperature "
            "resistance, suitable for high-pressure, high-temperature wells. Elastomeric seals offer flexibility and ease of installation but may degrade in "
            "sour or high-temperature environments. The engineer evaluates pressure, temperature, fluid composition, and compatibility with materials. "
            "Documentation includes test data, supplier certifications, and operational procedures."
        ),
        key_factors=[
            "Pressure and temperature",
            "Fluid composition",
            "API 6A seal requirements",
            "Material compatibility",
            "Supplier certification"
        ],
        primary_authority=["API 6A", "Company Materials Standard"],
        burden_holder="Materials Engineer",
        adversary_position="Elastomeric seals are sufficient; metal seals are over-specified.",
        counter_arguments=[
            "Metal seals are required for high-pressure, high-temperature wells.",
            "API 6A mandates seal selection based on well conditions.",
            "Elastomeric seals may degrade in sour environments."
        ],
        resolution_strategy="Seal technology is selected based on pressure, temperature, and API 6A requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 10"
    ),
    DoctrineBlock(
        topic="Flanged vs Studded Connections",
        keywords=["flanged", "studded", "connections", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Connection type for OFE08 wellhead must be selected based on load, pressure, and installation requirements per API 6A.",
        reasoning_framework=(
            "Connection type (flanged vs studded) is governed by API 6A and operational requirements. Flanged connections offer ease of installation and "
            "maintenance, suitable for surface wells. Studded connections provide superior load capacity and are preferred for high-pressure or subsea wells. "
            "The engineer evaluates load conditions, pressure rating, installation procedures, and compatibility with downstream equipment. Documentation "
            "includes risk assessment and operational procedures."
        ),
        key_factors=[
            "Load conditions",
            "Pressure rating",
            "Installation requirements",
            "API 6A connection requirements",
            "Compatibility with equipment"
        ],
        primary_authority=["API 6A", "Company Installation Standards"],
        burden_holder="Installation Engineer",
        adversary_position="Flanged connections are sufficient; studded connections add unnecessary complexity.",
        counter_arguments=[
            "Studded connections provide superior load capacity for high-pressure wells.",
            "API 6A mandates connection selection based on load and pressure.",
            "Flanged connections may compromise integrity in subsea environments."
        ],
        resolution_strategy="Connection type is selected based on load, pressure, and API 6A requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 11"
    ),
    DoctrineBlock(
        topic="Pressure Testing and Verification (API 6A)",
        keywords=["pressure testing", "verification", "API 6A", "wellhead", "OFE08"],
        conclusion_template="Pressure testing for OFE08 wellhead must comply with API 6A protocols and be documented for regulatory verification.",
        reasoning_framework=(
            "Pressure testing and verification are governed by API 6A, requiring hydrostatic and gas tests at specified pressures and durations. "
            "The engineer reviews test protocols, equipment calibration, and documentation requirements. Test results are recorded, witnessed by QA/QC, "
            "and submitted to regulatory authorities. Failure modes and corrective actions are documented. Final verification is approved by technical authorities."
        ),
        key_factors=[
            "Test pressure and duration",
            "API 6A test protocols",
            "Equipment calibration",
            "QA/QC documentation",
            "Regulatory verification"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards", "Local Regulatory Authority"],
        burden_holder="QA/QC Engineer",
        adversary_position="Testing protocols are excessive; lower test pressures are sufficient.",
        counter_arguments=[
            "API 6A mandates test pressures and durations for safety.",
            "Lower test pressures may compromise verification.",
            "Regulatory authorities require documented compliance."
        ],
        resolution_strategy="Testing is conducted per API 6A protocols and documented for regulatory verification.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 12"
    ),
    DoctrineBlock(
        topic="Surface Safety Valve (SSV) Requirements",
        keywords=["surface safety valve", "SSV", "wellhead", "OFE08", "API 6A", "safety"],
        conclusion_template="SSV requirements for OFE08 wellhead must comply with API 6A and local regulatory mandates for emergency shut-in.",
        reasoning_framework=(
            "Surface Safety Valve (SSV) requirements are governed by API 6A and local regulations, mandating installation for emergency shut-in. "
            "The engineer reviews well risk profile, pressure rating, and operational procedures. SSV selection includes evaluation of valve type, "
            "actuation mechanism, and fail-safe features. Documentation includes risk assessment, supplier certifications, and operational procedures. "
            "Final selection is approved by safety engineering and regulatory authorities."
        ),
        key_factors=[
            "Well risk profile",
            "API 6A SSV requirements",
            "Pressure rating",
            "Actuation mechanism",
            "Regulatory mandates"
        ],
        primary_authority=["API 6A", "Local Regulatory Authority", "Company Safety Standards"],
        burden_holder="Safety Engineer",
        adversary_position="SSV is unnecessary for low-risk wells.",
        counter_arguments=[
            "API 6A and regulatory authorities mandate SSV for emergency shut-in.",
            "Low-risk wells may still experience abnormal events requiring SSV.",
            "Historical incidents show failures due to lack of SSV."
        ],
        resolution_strategy="SSV is installed per API 6A and regulatory requirements, regardless of risk profile.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 13"
    ),
    DoctrineBlock(
        topic="Cameron vs FMC vs Dril-Quip Systems",
        keywords=["Cameron", "FMC", "Dril-Quip", "wellhead", "OFE08", "API 6A", "system selection"],
        conclusion_template="System selection for OFE08 wellhead must be based on API 6A compliance, operational requirements, and supplier performance.",
        reasoning_framework=(
            "System selection (Cameron vs FMC vs Dril-Quip) is governed by API 6A compliance, operational requirements, and supplier performance. "
            "The engineer evaluates technical specifications, compatibility with wellhead equipment, supplier track record, and support infrastructure. "
            "Material class, PSL, and pressure rating are validated. Documentation includes supplier certifications, risk assessment, and operational procedures. "
            "Final selection is approved by procurement and technical authorities."
        ),
        key_factors=[
            "API 6A compliance",
            "Operational requirements",
            "Supplier performance",
            "Material class",
            "PSL"
        ],
        primary_authority=["API 6A", "Company Procurement Standards"],
        burden_holder="Procurement Engineer",
        adversary_position="Alternative supplier offers lower cost and meets minimum requirements.",
        counter_arguments=[
            "Supplier performance and support infrastructure are critical for reliability.",
            "API 6A compliance must be verified for all suppliers.",
            "Historical failures linked to poor supplier performance."
        ],
        resolution_strategy="System is selected based on API 6A compliance, operational requirements, and supplier performance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 14"
    ),
    DoctrineBlock(
        topic="Subsea Wellhead vs Surface Wellhead",
        keywords=["subsea wellhead", "surface wellhead", "OFE08", "API 6A", "configuration"],
        conclusion_template="Wellhead configuration for OFE08 must be selected based on well location, intervention requirements, and API 6A compliance.",
        reasoning_framework=(
            "Wellhead configuration (subsea vs surface) is governed by well location, intervention requirements, and API 6A standards. Subsea wellheads require "
            "enhanced pressure rating, corrosion resistance, and intervention capability. Surface wellheads offer ease of access and maintenance. The engineer "
            "evaluates well location, operational requirements, and compatibility with completion equipment. Documentation includes risk assessment and operational procedures."
        ),
        key_factors=[
            "Well location",
            "Intervention requirements",
            "API 6A compliance",
            "Pressure rating",
            "Corrosion resistance"
        ],
        primary_authority=["API 6A", "Company Completion Standards"],
        burden_holder="Completion Engineer",
        adversary_position="Surface wellhead is sufficient; subsea wellhead adds unnecessary complexity.",
        counter_arguments=[
            "Subsea wells require enhanced pressure rating and corrosion resistance.",
            "API 6A mandates configuration selection based on well location.",
            "Surface wellheads may limit intervention in subsea environments."
        ],
        resolution_strategy="Configuration is selected based on well location, intervention requirements, and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 15"
    ),
    DoctrineBlock(
        topic="Casing Hanger Selection (Slip vs Mandrel)",
        keywords=["casing hanger", "slip", "mandrel", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Casing hanger type for OFE08 must be selected based on load, seal integrity, and API 6A compliance.",
        reasoning_framework=(
            "Casing hanger selection (slip vs mandrel) is governed by API 6A and well conditions. Mandrel hangers provide superior seal integrity and load capacity, "
            "suitable for high-pressure wells. Slip hangers offer flexibility and ease of installation. The engineer evaluates load conditions, seal requirements, "
            "and compatibility with casing program. Documentation includes risk assessment and operational procedures."
        ),
        key_factors=[
            "Load conditions",
            "Seal integrity",
            "API 6A hanger requirements",
            "Casing program",
            "Installation requirements"
        ],
        primary_authority=["API 6A", "Company Well Design Standard"],
        burden_holder="Well Engineer",
        adversary_position="Slip hangers are sufficient; mandrel hangers are over-specified.",
        counter_arguments=[
            "Mandrel hangers provide superior seal integrity for high-pressure wells.",
            "API 6A mandates hanger selection based on load and seal requirements.",
            "Slip hangers may compromise seal integrity in critical wells."
        ],
        resolution_strategy="Hanger type is selected based on load, seal integrity, and API 6A requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 16"
    ),
    DoctrineBlock(
        topic="Temperature Class and Derating",
        keywords=["temperature class", "derating", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Temperature class for OFE08 wellhead must be selected per API 6A and derated for high-temperature wells.",
        reasoning_framework=(
            "Temperature class selection and derating are governed by API 6A, requiring evaluation of well temperature and material performance. High-temperature "
            "wells require derating of pressure ratings and material properties. The engineer reviews reservoir temperature, material class, and API 6A temperature "
            "class definitions. Documentation includes test data, supplier certifications, and operational procedures."
        ),
        key_factors=[
            "Well temperature",
            "API 6A temperature class definitions",
            "Material performance",
            "Pressure derating",
            "Supplier certification"
        ],
        primary_authority=["API 6A", "Company Materials Standard"],
        burden_holder="Materials Engineer",
        adversary_position="Derating is unnecessary; material performance is sufficient.",
        counter_arguments=[
            "API 6A mandates derating for high-temperature wells.",
            "Material performance may degrade at elevated temperatures.",
            "Historical failures linked to lack of derating."
        ],
        resolution_strategy="Temperature class is selected and derated per API 6A requirements and material performance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 17"
    ),
    DoctrineBlock(
        topic="PR1 vs PR2 Performance Requirements",
        keywords=["PR1", "PR2", "performance requirements", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Performance requirement for OFE08 wellhead must be selected per API 6A based on criticality and regulatory mandates.",
        reasoning_framework=(
            "PR1 and PR2 performance requirements are defined in API 6A. PR1 is basic; PR2 requires enhanced testing and documentation. Selection is based on well "
            "criticality, service environment, and regulatory requirements. PR2 is mandated for critical or high-pressure wells. The engineer reviews project "
            "specifications, regulatory guidance, and risk assessments. Documentation includes test reports, material certificates, and inspection records."
        ),
        key_factors=[
            "Well criticality",
            "Service environment",
            "API 6A PR definitions",
            "Regulatory requirements",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards", "Local Regulatory Authority"],
        burden_holder="QA/QC Engineer",
        adversary_position="PR2 is unnecessary; PR1 is sufficient for this well.",
        counter_arguments=[
            "Critical wells require PR2 for enhanced safety and reliability.",
            "Regulatory authorities may mandate PR2 for sour or high-pressure wells.",
            "PR1 lacks testing and documentation required for critical applications."
        ],
        resolution_strategy="Performance requirement is selected based on risk assessment, regulatory mandates, and API 6A compliance.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 18"
    ),
    DoctrineBlock(
        topic="Wellhead Valve Types (Gate vs Ball)",
        keywords=["valve types", "gate valve", "ball valve", "wellhead", "OFE08", "API 6A"],
        conclusion_template="Valve type for OFE08 wellhead must be selected based on flow control, pressure rating, and API 6A compliance.",
        reasoning_framework=(
            "Valve type selection (gate vs ball) is governed by API 6A and operational requirements. Gate valves provide superior sealing and are preferred for "
            "high-pressure wells. Ball valves offer quick operation and are suitable for low-pressure applications. The engineer evaluates flow control requirements, "
            "pressure rating, material class, and maintenance procedures. Documentation includes risk assessment and operational procedures."
        ),
        key_factors=[
            "Flow control requirements",
            "Pressure rating",
            "API 6A valve requirements",
            "Material class",
            "Maintenance procedures"
        ],
        primary_authority=["API 6A", "Company Production Standards"],
        burden_holder="Production Engineer",
        adversary_position="Ball valves are sufficient; gate valves add unnecessary complexity.",
        counter_arguments=[
            "Gate valves provide superior sealing for high-pressure wells.",
            "API 6A mandates valve selection based on flow control and pressure rating.",
            "Ball valves may compromise seal integrity in critical wells."
        ],
        resolution_strategy="Valve type is selected based on flow control, pressure rating, and API 6A requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 19"
    ),
    DoctrineBlock(
        topic="API Monogram Licensing and Verification",
        keywords=["API monogram", "licensing", "verification", "wellhead", "OFE08", "API 6A"],
        conclusion_template="API monogram licensing and verification for OFE08 wellhead must comply with API 6A and be documented for regulatory approval.",
        reasoning_framework=(
            "API monogram licensing and verification are governed by API 6A, requiring supplier certification, traceability, and documentation. The engineer reviews "
            "supplier certifications, material traceability, and QA/QC documentation. Verification includes inspection records, test reports, and regulatory submissions. "
            "Final approval is granted by QA/QC and regulatory authorities."
        ),
        key_factors=[
            "Supplier certification",
            "Material traceability",
            "API 6A monogram requirements",
            "QA/QC documentation",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards", "Local Regulatory Authority"],
        burden_holder="QA/QC Engineer",
        adversary_position="API monogram is unnecessary; supplier certification is sufficient.",
        counter_arguments=[
            "API monogram is required for regulatory approval and traceability.",
            "Supplier certification alone may lack traceability and documentation.",
            "Regulatory authorities mandate API monogram for critical equipment."
        ],
        resolution_strategy="API monogram licensing and verification are conducted per API 6A and regulatory requirements.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 20"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Traceability",
        keywords=["traceability", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Traceability for OFE08 wellhead equipment must be maintained per API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Traceability is a core requirement under API 6A and company QA/QC standards. All wellhead equipment must be uniquely identified, "
            "with full documentation of material origin, manufacturing processes, and testing. The engineer ensures traceability records are "
            "maintained from procurement through installation and operation. Any non-conformance is documented and resolved. Regulatory authorities "
            "may audit traceability records during inspections."
        ),
        key_factors=[
            "Unique identification",
            "Material origin",
            "Manufacturing processes",
            "Testing records",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Traceability adds unnecessary administrative burden.",
        counter_arguments=[
            "Traceability is required for regulatory compliance and safety.",
            "Lack of traceability can lead to unaddressed non-conformance.",
            "Historical failures linked to poor traceability."
        ],
        resolution_strategy="Traceability is maintained per API 6A and QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 21"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Non-Conformance Management",
        keywords=["non-conformance", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Non-conformance for OFE08 wellhead equipment must be managed per API 6A and company QA/QC procedures.",
        reasoning_framework=(
            "Non-conformance management is governed by API 6A and company QA/QC procedures. Any deviation from specifications, material class, or testing "
            "is documented, investigated, and resolved. The engineer ensures corrective actions are implemented and documented. Regulatory authorities "
            "may require notification and approval of corrective actions. Non-conforming equipment is quarantined until resolution."
        ),
        key_factors=[
            "Deviation from specifications",
            "Material class",
            "Testing records",
            "Corrective actions",
            "Regulatory notification"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Non-conformance management is excessive; minor deviations can be ignored.",
        counter_arguments=[
            "Ignoring non-conformance can compromise safety and reliability.",
            "API 6A mandates documentation and resolution of all non-conformance.",
            "Regulatory authorities require notification and approval."
        ],
        resolution_strategy="Non-conformance is managed per API 6A and QA/QC procedures, with full documentation and corrective actions.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 22"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Maintenance and Inspection",
        keywords=["maintenance", "inspection", "wellhead equipment", "OFE08", "API 6A"],
        conclusion_template="Maintenance and inspection for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Maintenance and inspection are governed by API 6A and company operational standards. The engineer develops maintenance schedules, inspection protocols, "
            "and documentation requirements. Equipment is inspected for wear, corrosion, and non-conformance. Maintenance actions are documented and reviewed by QA/QC. "
            "Regulatory authorities may require periodic inspection reports."
        ),
        key_factors=[
            "Maintenance schedules",
            "Inspection protocols",
            "Wear and corrosion",
            "Documentation requirements",
            "Regulatory inspection"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Maintenance Engineer",
        adversary_position="Maintenance schedules are excessive; inspection intervals can be extended.",
        counter_arguments=[
            "API 6A mandates maintenance and inspection intervals for safety.",
            "Extended intervals may compromise equipment reliability.",
            "Regulatory authorities require periodic inspection reports."
        ],
        resolution_strategy="Maintenance and inspection are conducted per API 6A and company standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 23"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Installation Procedures",
        keywords=["installation", "procedures", "wellhead equipment", "OFE08", "API 6A"],
        conclusion_template="Installation procedures for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Installation procedures are governed by API 6A and company operational standards. The engineer develops detailed installation protocols, "
            "including equipment handling, alignment, and torque requirements. Installation is witnessed by QA/QC and documented. Any deviation is "
            "investigated and resolved. Regulatory authorities may require installation records for verification."
        ),
        key_factors=[
            "Installation protocols",
            "Equipment handling",
            "Alignment and torque",
            "QA/QC documentation",
            "Regulatory verification"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Installation Engineer",
        adversary_position="Installation protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates detailed installation procedures for safety.",
            "Simplified procedures may compromise equipment integrity.",
            "Regulatory authorities require installation records."
        ],
        resolution_strategy="Installation procedures are developed per API 6A and company standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 24"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Decommissioning",
        keywords=["decommissioning", "wellhead equipment", "OFE08", "API 6A", "regulatory"],
        conclusion_template="Decommissioning for OFE08 wellhead equipment must comply with API 6A and local regulatory requirements.",
        reasoning_framework=(
            "Decommissioning procedures are governed by API 6A and local regulatory requirements. The engineer develops decommissioning protocols, including "
            "equipment removal, environmental protection, and documentation. Decommissioning actions are witnessed by QA/QC and regulatory authorities. "
            "Any deviation is documented and resolved. Final approval is granted by regulatory authorities."
        ),
        key_factors=[
            "Decommissioning protocols",
            "Equipment removal",
            "Environmental protection",
            "QA/QC documentation",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Local Regulatory Authority", "Company Decommissioning Standards"],
        burden_holder="Decommissioning Engineer",
        adversary_position="Decommissioning protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A and regulatory authorities mandate decommissioning protocols for environmental protection.",
            "Simplified procedures may compromise environmental safety.",
            "Regulatory authorities require decommissioning records."
        ],
        resolution_strategy="Decommissioning is conducted per API 6A and regulatory requirements, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 25"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Emergency Response",
        keywords=["emergency response", "wellhead equipment", "OFE08", "API 6A", "safety"],
        conclusion_template="Emergency response for OFE08 wellhead equipment must comply with API 6A and company safety standards.",
        reasoning_framework=(
            "Emergency response procedures are governed by API 6A and company safety standards. The engineer develops emergency protocols, including equipment shut-in, "
            "evacuation, and communication. Emergency actions are documented and reviewed by safety engineering and regulatory authorities. Any deviation is investigated "
            "and resolved. Final approval is granted by safety engineering and regulatory authorities."
        ),
        key_factors=[
            "Emergency protocols",
            "Equipment shut-in",
            "Evacuation procedures",
            "Documentation requirements",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company Safety Standards", "Local Regulatory Authority"],
        burden_holder="Safety Engineer",
        adversary_position="Emergency response protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A and company standards mandate emergency response protocols for safety.",
            "Simplified procedures may compromise emergency response effectiveness.",
            "Regulatory authorities require emergency response records."
        ],
        resolution_strategy="Emergency response is conducted per API 6A and company standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 26"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Environmental Protection",
        keywords=["environmental protection", "wellhead equipment", "OFE08", "API 6A", "regulatory"],
        conclusion_template="Environmental protection for OFE08 wellhead equipment must comply with API 6A and local regulatory requirements.",
        reasoning_framework=(
            "Environmental protection procedures are governed by API 6A and local regulatory requirements. The engineer develops protocols for equipment handling, "
            "spill prevention, and waste management. Environmental actions are documented and reviewed by environmental engineering and regulatory authorities. "
            "Any deviation is investigated and resolved. Final approval is granted by environmental engineering and regulatory authorities."
        ),
        key_factors=[
            "Equipment handling",
            "Spill prevention",
            "Waste management",
            "Documentation requirements",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Local Regulatory Authority", "Company Environmental Standards"],
        burden_holder="Environmental Engineer",
        adversary_position="Environmental protection protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A and regulatory authorities mandate environmental protection protocols.",
            "Simplified procedures may compromise environmental safety.",
            "Regulatory authorities require environmental protection records."
        ],
        resolution_strategy="Environmental protection is conducted per API 6A and regulatory requirements, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 27"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Supplier Qualification",
        keywords=["supplier qualification", "wellhead equipment", "OFE08", "API 6A", "procurement"],
        conclusion_template="Supplier qualification for OFE08 wellhead equipment must comply with API 6A and company procurement standards.",
        reasoning_framework=(
            "Supplier qualification is governed by API 6A and company procurement standards. The engineer reviews supplier certifications, track record, and support infrastructure. "
            "Qualification includes evaluation of material class, PSL, and pressure rating. Documentation includes supplier certifications, risk assessment, and operational procedures. "
            "Final qualification is approved by procurement and technical authorities."
        ),
        key_factors=[
            "Supplier certifications",
            "Track record",
            "Support infrastructure",
            "Material class",
            "PSL"
        ],
        primary_authority=["API 6A", "Company Procurement Standards"],
        burden_holder="Procurement Engineer",
        adversary_position="Supplier qualification is unnecessary; lowest cost supplier is sufficient.",
        counter_arguments=[
            "Supplier qualification is required for reliability and safety.",
            "API 6A mandates supplier qualification for critical equipment.",
            "Historical failures linked to poor supplier qualification."
        ],
        resolution_strategy="Supplier qualification is conducted per API 6A and company procurement standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 28"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Documentation Requirements",
        keywords=["documentation", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Documentation for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Documentation requirements are governed by API 6A and company QA/QC standards. The engineer ensures all equipment is documented, including material certificates, "
            "test reports, installation records, and maintenance logs. Documentation is reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Material certificates",
            "Test reports",
            "Installation records",
            "Maintenance logs",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Documentation requirements are excessive; simplified records are sufficient.",
        counter_arguments=[
            "API 6A mandates full documentation for traceability and safety.",
            "Simplified records may compromise regulatory compliance.",
            "Regulatory authorities require full documentation."
        ],
        resolution_strategy="Documentation is maintained per API 6A and company QA/QC standards, with full records.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 29"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Risk Assessment",
        keywords=["risk assessment", "wellhead equipment", "OFE08", "API 6A", "safety"],
        conclusion_template="Risk assessment for OFE08 wellhead equipment must comply with API 6A and company safety standards.",
        reasoning_framework=(
            "Risk assessment is governed by API 6A and company safety standards. The engineer conducts risk assessments for equipment selection, installation, operation, "
            "and decommissioning. Risk mitigation measures are documented and reviewed by safety engineering and regulatory authorities. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Equipment selection",
            "Installation",
            "Operation",
            "Decommissioning",
            "Risk mitigation"
        ],
        primary_authority=["API 6A", "Company Safety Standards"],
        burden_holder="Safety Engineer",
        adversary_position="Risk assessment is unnecessary; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates risk assessment for safety and reliability.",
            "Standard procedures may not address all risks.",
            "Regulatory authorities require risk assessment records."
        ],
        resolution_strategy="Risk assessment is conducted per API 6A and company safety standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 30"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Change Management",
        keywords=["change management", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Change management for OFE08 wellhead equipment must comply with API 6A and company QA/QC procedures.",
        reasoning_framework=(
            "Change management is governed by API 6A and company QA/QC procedures. The engineer documents any changes to equipment specifications, materials, or installation procedures. "
            "Changes are reviewed and approved by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment specifications",
            "Materials",
            "Installation procedures",
            "QA/QC documentation",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Change management is unnecessary; minor changes can be ignored.",
        counter_arguments=[
            "API 6A mandates documentation and approval of all changes.",
            "Ignoring changes can compromise safety and reliability.",
            "Regulatory authorities require change management records."
        ],
        resolution_strategy="Change management is conducted per API 6A and company QA/QC procedures, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 31"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Training Requirements",
        keywords=["training", "wellhead equipment", "OFE08", "API 6A", "operational"],
        conclusion_template="Training requirements for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Training requirements are governed by API 6A and company operational standards. The engineer ensures all personnel are trained in equipment handling, installation, "
            "maintenance, and emergency response. Training records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment handling",
            "Installation",
            "Maintenance",
            "Emergency response",
            "Training records"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Training Coordinator",
        adversary_position="Training requirements are excessive; on-the-job training is sufficient.",
        counter_arguments=[
            "API 6A mandates training for safety and reliability.",
            "On-the-job training may lack documentation and consistency.",
            "Regulatory authorities require training records."
        ],
        resolution_strategy="Training is conducted per API 6A and company operational standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 32"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Procurement Procedures",
        keywords=["procurement", "procedures", "wellhead equipment", "OFE08", "API 6A"],
        conclusion_template="Procurement procedures for OFE08 wellhead equipment must comply with API 6A and company procurement standards.",
        reasoning_framework=(
            "Procurement procedures are governed by API 6A and company procurement standards. The engineer ensures all equipment is procured from qualified suppliers, "
            "with full documentation of material class, PSL, and pressure rating. Procurement records are maintained and reviewed by QA/QC and regulatory authorities. "
            "Any deviation is documented and resolved."
        ),
        key_factors=[
            "Qualified suppliers",
            "Material class",
            "PSL",
            "Pressure rating",
            "Procurement records"
        ],
        primary_authority=["API 6A", "Company Procurement Standards"],
        burden_holder="Procurement Engineer",
        adversary_position="Procurement procedures are excessive; lowest cost supplier is sufficient.",
        counter_arguments=[
            "API 6A mandates procurement from qualified suppliers.",
            "Lowest cost supplier may lack qualifications and documentation.",
            "Regulatory authorities require procurement records."
        ],
        resolution_strategy="Procurement is conducted per API 6A and company procurement standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 33"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Quality Control",
        keywords=["quality control", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Quality control for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Quality control is governed by API 6A and company QA/QC standards. The engineer develops quality control protocols, including inspection, testing, and documentation. "
            "Quality control actions are documented and reviewed by QA/QC and regulatory authorities. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Inspection protocols",
            "Testing requirements",
            "Documentation",
            "QA/QC review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Quality control protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates quality control for safety and reliability.",
            "Simplified procedures may compromise equipment quality.",
            "Regulatory authorities require quality control records."
        ],
        resolution_strategy="Quality control is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 34"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Regulatory Compliance",
        keywords=["regulatory compliance", "wellhead equipment", "OFE08", "API 6A", "regulatory"],
        conclusion_template="Regulatory compliance for OFE08 wellhead equipment must be maintained per API 6A and local regulatory requirements.",
        reasoning_framework=(
            "Regulatory compliance is governed by API 6A and local regulatory requirements. The engineer ensures all equipment complies with regulatory mandates, including "
            "material class, PSL, pressure rating, and documentation. Regulatory compliance records are maintained and reviewed by QA/QC and regulatory authorities. "
            "Any deviation is documented and resolved."
        ),
        key_factors=[
            "Regulatory mandates",
            "Material class",
            "PSL",
            "Pressure rating",
            "Compliance records"
        ],
        primary_authority=["API 6A", "Local Regulatory Authority"],
        burden_holder="Regulatory Compliance Engineer",
        adversary_position="Regulatory compliance is unnecessary; company standards are sufficient.",
        counter_arguments=[
            "API 6A and regulatory authorities mandate compliance for safety and reliability.",
            "Company standards may not address all regulatory requirements.",
            "Regulatory authorities require compliance records."
        ],
        resolution_strategy="Regulatory compliance is maintained per API 6A and local regulatory requirements, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 35"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Safety Management",
        keywords=["safety management", "wellhead equipment", "OFE08", "API 6A", "safety"],
        conclusion_template="Safety management for OFE08 wellhead equipment must comply with API 6A and company safety standards.",
        reasoning_framework=(
            "Safety management is governed by API 6A and company safety standards. The engineer develops safety management protocols, including risk assessment, emergency response, "
            "and documentation. Safety management actions are documented and reviewed by safety engineering and regulatory authorities. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Risk assessment",
            "Emergency response",
            "Documentation",
            "Safety engineering review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company Safety Standards"],
        burden_holder="Safety Engineer",
        adversary_position="Safety management protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates safety management for reliability and emergency response.",
            "Simplified procedures may compromise safety.",
            "Regulatory authorities require safety management records."
        ],
        resolution_strategy="Safety management is conducted per API 6A and company safety standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 36"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Performance Monitoring",
        keywords=["performance monitoring", "wellhead equipment", "OFE08", "API 6A", "operational"],
        conclusion_template="Performance monitoring for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Performance monitoring is governed by API 6A and company operational standards. The engineer develops performance monitoring protocols, including data collection, "
            "analysis, and documentation. Performance monitoring actions are documented and reviewed by operational engineering and regulatory authorities. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Data collection",
            "Analysis",
            "Documentation",
            "Operational engineering review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Operational Engineer",
        adversary_position="Performance monitoring protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates performance monitoring for reliability and safety.",
            "Simplified procedures may compromise performance monitoring effectiveness.",
            "Regulatory authorities require performance monitoring records."
        ],
        resolution_strategy="Performance monitoring is conducted per API 6A and company operational standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 37"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Incident Investigation",
        keywords=["incident investigation", "wellhead equipment", "OFE08", "API 6A", "safety"],
        conclusion_template="Incident investigation for OFE08 wellhead equipment must comply with API 6A and company safety standards.",
        reasoning_framework=(
            "Incident investigation is governed by API 6A and company safety standards. The engineer documents all incidents, conducts root cause analysis, and implements corrective actions. "
            "Incident investigation records are reviewed by safety engineering and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Incident documentation",
            "Root cause analysis",
            "Corrective actions",
            "Safety engineering review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company Safety Standards"],
        burden_holder="Safety Engineer",
        adversary_position="Incident investigation protocols are excessive; minor incidents can be ignored.",
        counter_arguments=[
            "API 6A mandates incident investigation for safety and reliability.",
            "Ignoring incidents can compromise safety and reliability.",
            "Regulatory authorities require incident investigation records."
        ],
        resolution_strategy="Incident investigation is conducted per API 6A and company safety standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 38"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Data Management",
        keywords=["data management", "wellhead equipment", "OFE08", "API 6A", "operational"],
        conclusion_template="Data management for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Data management is governed by API 6A and company operational standards. The engineer ensures all equipment data is collected, stored, and documented. Data management records "
            "are reviewed by operational engineering and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Data collection",
            "Data storage",
            "Documentation",
            "Operational engineering review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Data Management Engineer",
        adversary_position="Data management protocols are excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates data management for traceability and reliability.",
            "Simplified procedures may compromise data integrity.",
            "Regulatory authorities require data management records."
        ],
        resolution_strategy="Data management is conducted per API 6A and company operational standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 39"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Continuous Improvement",
        keywords=["continuous improvement", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Continuous improvement for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Continuous improvement is governed by API 6A and company QA/QC standards. The engineer develops protocols for continuous improvement, including review of performance data, "
            "implementation of corrective actions, and documentation. Continuous improvement records are reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Performance data review",
            "Corrective actions",
            "Documentation",
            "QA/QC review",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Continuous improvement protocols are excessive; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates continuous improvement for reliability and safety.",
            "Standard procedures may not address all improvement opportunities.",
            "Regulatory authorities require continuous improvement records."
        ],
        resolution_strategy="Continuous improvement is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 40"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Audit Procedures",
        keywords=["audit procedures", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Audit procedures for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Audit procedures are governed by API 6A and company QA/QC standards. The engineer develops audit protocols, including review of documentation, inspection records, and compliance. "
            "Audit actions are documented and reviewed by QA/QC and regulatory authorities. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Audit protocols",
            "Documentation review",
            "Inspection records",
            "Compliance review",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Audit procedures are excessive; simplified audits are sufficient.",
        counter_arguments=[
            "API 6A mandates audit procedures for traceability and reliability.",
            "Simplified audits may compromise compliance.",
            "Regulatory authorities require audit records."
        ],
        resolution_strategy="Audit procedures are conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 41"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Supplier Performance Monitoring",
        keywords=["supplier performance", "monitoring", "wellhead equipment", "OFE08", "API 6A", "procurement"],
        conclusion_template="Supplier performance monitoring for OFE08 wellhead equipment must comply with API 6A and company procurement standards.",
        reasoning_framework=(
            "Supplier performance monitoring is governed by API 6A and company procurement standards. The engineer develops protocols for monitoring supplier performance, including review of delivery, "
            "quality, and support. Supplier performance records are documented and reviewed by procurement and QA/QC. Any deviation is investigated and resolved."
        ),
        key_factors=[
            "Delivery performance",
            "Quality",
            "Support",
            "Documentation",
            "Procurement review"
        ],
        primary_authority=["API 6A", "Company Procurement Standards"],
        burden_holder="Procurement Engineer",
        adversary_position="Supplier performance monitoring is unnecessary; lowest cost supplier is sufficient.",
        counter_arguments=[
            "Supplier performance monitoring is required for reliability and safety.",
            "API 6A mandates supplier performance monitoring for critical equipment.",
            "Historical failures linked to poor supplier performance."
        ],
        resolution_strategy="Supplier performance monitoring is conducted per API 6A and company procurement standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 42"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Spare Parts Management",
        keywords=["spare parts", "management", "wellhead equipment", "OFE08", "API 6A", "operational"],
        conclusion_template="Spare parts management for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Spare parts management is governed by API 6A and company operational standards. The engineer develops protocols for spare parts identification, storage, and documentation. "
            "Spare parts records are maintained and reviewed by operational engineering and QA/QC. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Spare parts identification",
            "Storage",
            "Documentation",
            "Operational engineering review",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Operational Engineer",
        adversary_position="Spare parts management is excessive; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates spare parts management for reliability and safety.",
            "Simplified procedures may compromise spare parts availability.",
            "Regulatory authorities require spare parts management records."
        ],
        resolution_strategy="Spare parts management is conducted per API 6A and company operational standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 43"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Lifecycle Management",
        keywords=["lifecycle management", "wellhead equipment", "OFE08", "API 6A", "operational"],
        conclusion_template="Lifecycle management for OFE08 wellhead equipment must comply with API 6A and company operational standards.",
        reasoning_framework=(
            "Lifecycle management is governed by API 6A and company operational standards. The engineer develops protocols for equipment lifecycle management, including procurement, installation, operation, "
            "maintenance, and decommissioning. Lifecycle management records are maintained and reviewed by operational engineering and QA/QC. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Procurement",
            "Installation",
            "Operation",
            "Maintenance",
            "Decommissioning"
        ],
        primary_authority=["API 6A", "Company Operational Standards"],
        burden_holder="Lifecycle Management Engineer",
        adversary_position="Lifecycle management protocols are excessive; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates lifecycle management for reliability and safety.",
            "Standard procedures may not address all lifecycle stages.",
            "Regulatory authorities require lifecycle management records."
        ],
        resolution_strategy="Lifecycle management is conducted per API 6A and company operational standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 44"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Reliability Analysis",
        keywords=["reliability analysis", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Reliability analysis for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Reliability analysis is governed by API 6A and company QA/QC standards. The engineer conducts reliability analysis for equipment selection, operation, and maintenance. "
            "Reliability analysis records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment selection",
            "Operation",
            "Maintenance",
            "Reliability analysis",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Reliability analysis is unnecessary; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates reliability analysis for safety and performance.",
            "Standard procedures may not address all reliability concerns.",
            "Regulatory authorities require reliability analysis records."
        ],
        resolution_strategy="Reliability analysis is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 45"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Failure Mode and Effects Analysis (FMEA)",
        keywords=["failure mode", "effects analysis", "FMEA", "wellhead equipment", "OFE08", "API 6A"],
        conclusion_template="FMEA for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Failure Mode and Effects Analysis (FMEA) is governed by API 6A and company QA/QC standards. The engineer conducts FMEA for equipment selection, operation, and maintenance. "
            "FMEA records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment selection",
            "Operation",
            "Maintenance",
            "FMEA",
            "QA/QC documentation"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="FMEA is unnecessary; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates FMEA for safety and reliability.",
            "Standard procedures may not address all failure modes.",
            "Regulatory authorities require FMEA records."
        ],
        resolution_strategy="FMEA is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 46"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Root Cause Analysis",
        keywords=["root cause analysis", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Root cause analysis for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Root cause analysis is governed by API 6A and company QA/QC standards. The engineer conducts root cause analysis for equipment failures and incidents. "
            "Root cause analysis records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment failures",
            "Incidents",
            "Root cause analysis",
            "QA/QC documentation",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Root cause analysis is unnecessary; minor failures can be ignored.",
        counter_arguments=[
            "API 6A mandates root cause analysis for safety and reliability.",
            "Ignoring failures can compromise safety and reliability.",
            "Regulatory authorities require root cause analysis records."
        ],
        resolution_strategy="Root cause analysis is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 47"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Corrective and Preventive Actions (CAPA)",
        keywords=["corrective actions", "preventive actions", "CAPA", "wellhead equipment", "OFE08", "API 6A"],
        conclusion_template="CAPA for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Corrective and Preventive Actions (CAPA) are governed by API 6A and company QA/QC standards. The engineer documents CAPA for equipment failures and incidents. "
            "CAPA records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment failures",
            "Incidents",
            "CAPA",
            "QA/QC documentation",
            "Regulatory approval"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="CAPA is unnecessary; standard procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates CAPA for safety and reliability.",
            "Standard procedures may not address all corrective and preventive actions.",
            "Regulatory authorities require CAPA records."
        ],
        resolution_strategy="CAPA is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 48"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Documentation Control",
        keywords=["documentation control", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Documentation control for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Documentation control is governed by API 6A and company QA/QC standards. The engineer ensures all documentation is controlled, updated, and reviewed. "
            "Documentation control records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Documentation control",
            "Updates",
            "QA/QC review",
            "Regulatory approval",
            "Compliance records"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Documentation control is unnecessary; simplified procedures are sufficient.",
        counter_arguments=[
            "API 6A mandates documentation control for traceability and reliability.",
            "Simplified procedures may compromise documentation integrity.",
            "Regulatory authorities require documentation control records."
        ],
        resolution_strategy="Documentation control is conducted per API 6A and company QA/QC standards, with full documentation.",
        entity_scope="OFE08 wellhead equipment",
        confidence=0.70,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 49"
    ),
    DoctrineBlock(
        topic="Wellhead Equipment Configuration Management",
        keywords=["configuration management", "wellhead equipment", "OFE08", "API 6A", "QA/QC"],
        conclusion_template="Configuration management for OFE08 wellhead equipment must comply with API 6A and company QA/QC standards.",
        reasoning_framework=(
            "Configuration management is governed by API 6A and company QA/QC standards. The engineer ensures all equipment configurations are documented, controlled, and reviewed. "
            "Configuration management records are maintained and reviewed by QA/QC and regulatory authorities. Any deviation is documented and resolved."
        ),
        key_factors=[
            "Equipment configurations",
            "Documentation",
            "QA/QC review",
            "Regulatory approval",
            "Compliance records"
        ],
        primary_authority=["API 6A", "Company QA/QC Standards"],
        burden_holder="QA/QC Engineer",
        adversary_position="Configuration management is unnecessary; simplified procedures are sufficient.",
        counter_arguments=[
            "