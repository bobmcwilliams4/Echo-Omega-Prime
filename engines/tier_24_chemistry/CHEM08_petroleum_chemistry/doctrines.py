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
        topic="Crude Oil Assay Interpretation",
        keywords=["crude oil", "assay", "petroleum analysis", "distillation curve"],
        conclusion_template="The interpretation of the crude oil assay indicates the suitability of the feedstock for specific refining processes.",
        reasoning_framework=(
            "1. Review the full crude oil assay, including TBP and ASTM distillation data.\n"
            "2. Evaluate key properties: API gravity, sulfur content, metals, nitrogen, and pour point.\n"
            "3. Assess the distillation curve to determine yields of naphtha, kerosene, diesel, and resid.\n"
            "4. Cross-reference with refinery configuration and product slate requirements.\n"
            "5. Consider compatibility with existing crude slate and operational constraints.\n"
            "6. Analyze the impact of contaminants on catalyst life and product quality.\n"
            "7. Synthesize findings to recommend optimal processing pathways or blending strategies."
        ),
        key_factors=[
            "API gravity",
            "Sulfur content",
            "Distillation yields",
            "Metals (Ni, V)",
            "Nitrogen content",
            "Pour point"
        ],
        primary_authority=[
            "ASTM D2892",
            "ASTM D5236",
            "UOP 375",
            "SPE Petroleum Engineering Handbook"
        ],
        burden_holder="Refinery Process Engineer",
        adversary_position="Crude oil supplier claims assay is representative and suitable for all refineries.",
        counter_arguments=[
            "Assay may not reflect operational realities of specific refinery units.",
            "Certain contaminants may be understated in supplier-provided assays."
        ],
        resolution_strategy="Conduct independent assay verification and pilot runs; compare with historical data from similar crudes.",
        entity_scope="Refinery technical and commercial teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API Technical Data Book, Section 2"
    ),
    DoctrineBlock(
        topic="Petroleum Product Specification Compliance",
        keywords=["product specification", "compliance", "diesel", "gasoline", "jet fuel"],
        conclusion_template="The petroleum product meets the required specification if all critical parameters are within regulatory and contractual limits.",
        reasoning_framework=(
            "1. Identify the relevant product specification (e.g., EN 590 for diesel, ASTM D4814 for gasoline).\n"
            "2. Collect laboratory analysis data for all critical parameters (e.g., sulfur, cetane/octane, distillation, aromatics).\n"
            "3. Compare measured values to specification limits.\n"
            "4. Assess margin of compliance and measurement uncertainty.\n"
            "5. Evaluate the impact of any deviations on downstream use and regulatory exposure.\n"
            "6. Document compliance status and communicate with stakeholders.\n"
            "7. Recommend corrective actions if non-compliance is detected."
        ),
        key_factors=[
            "Sulfur content",
            "Cetane/octane number",
            "Distillation profile",
            "Aromatics",
            "Flash point",
            "Density"
        ],
        primary_authority=[
            "EN 590",
            "ASTM D4814",
            "ASTM D1655",
            "API 1509"
        ],
        burden_holder="Quality Assurance Manager",
        adversary_position="Buyer alleges off-spec product delivery.",
        counter_arguments=[
            "Laboratory results may be within repeatability/reproducibility limits.",
            "Sampling method may have introduced bias."
        ],
        resolution_strategy="Review chain of custody, retest retained samples, and consult independent laboratory if needed.",
        entity_scope="Product quality and regulatory compliance teams",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 1509, Section 7"
    ),
    DoctrineBlock(
        topic="Hydrodesulfurization Catalyst Deactivation",
        keywords=["hydrodesulfurization", "catalyst", "deactivation", "sulfur removal"],
        conclusion_template="Catalyst deactivation in hydrodesulfurization units is primarily caused by metal deposition, coke formation, and poisoning by nitrogen compounds.",
        reasoning_framework=(
            "1. Analyze feedstock properties for metals (Ni, V), nitrogen, and asphaltenes.\n"
            "2. Review unit operating history and performance trends (ΔP, sulfur slip).\n"
            "3. Examine spent catalyst samples for metal and coke deposition.\n"
            "4. Correlate deactivation rate with feed contaminants and operating severity.\n"
            "5. Evaluate effectiveness of guard beds and pre-treatment steps.\n"
            "6. Recommend operational adjustments or catalyst change-out intervals.\n"
            "7. Document findings and update catalyst management plan."
        ),
        key_factors=[
            "Feed metal content",
            "Nitrogen compounds",
            "Operating temperature",
            "Hydrogen partial pressure",
            "Cycle length"
        ],
        primary_authority=[
            "UOP Hydroprocessing Handbook",
            "SPE 16905",
            "API Technical Data Book"
        ],
        burden_holder="Process Technology Specialist",
        adversary_position="Operations claims catalyst life is unaffected by feed variability.",
        counter_arguments=[
            "Short-term improvements may mask long-term deactivation.",
            "Feed blending can dilute but not eliminate contaminants."
        ],
        resolution_strategy="Implement feed monitoring, optimize operating conditions, and schedule catalyst regeneration or replacement.",
        entity_scope="Hydroprocessing units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="UOP Hydroprocessing Handbook, Ch. 4"
    ),
    DoctrineBlock(
        topic="Petroleum Storage Tank Corrosion Control",
        keywords=["storage tank", "corrosion", "inspection", "API 653"],
        conclusion_template="Effective corrosion control in petroleum storage tanks is achieved through regular inspection, protective coatings, and cathodic protection.",
        reasoning_framework=(
            "1. Review tank design, construction materials, and service history.\n"
            "2. Conduct periodic internal and external inspections per API 653.\n"
            "3. Assess condition of protective coatings and linings.\n"
            "4. Evaluate cathodic protection system performance.\n"
            "5. Identify areas of active corrosion or coating failure.\n"
            "6. Prioritize repairs based on risk assessment and regulatory requirements.\n"
            "7. Implement preventive maintenance and monitoring programs."
        ),
        key_factors=[
            "Tank material",
            "Coating integrity",
            "Cathodic protection",
            "Inspection frequency",
            "Stored product properties"
        ],
        primary_authority=[
            "API 653",
            "API 650",
            "NACE SP0193"
        ],
        burden_holder="Tank Integrity Engineer",
        adversary_position="Operations resists downtime for inspection and maintenance.",
        counter_arguments=[
            "Deferred maintenance increases long-term risk and cost.",
            "Regulatory penalties for non-compliance."
        ],
        resolution_strategy="Develop inspection schedule aligned with operations, justify downtime with risk-based analysis.",
        entity_scope="Storage and terminal facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 653, Section 6"
    ),
    DoctrineBlock(
        topic="Vapor Pressure Control in Gasoline Blending",
        keywords=["vapor pressure", "RVP", "gasoline blending", "volatility"],
        conclusion_template="Gasoline blends must meet regulatory and seasonal RVP limits to ensure safe and compliant distribution.",
        reasoning_framework=(
            "1. Determine applicable RVP limits (e.g., EPA, CARB, local regulations).\n"
            "2. Analyze blendstocks for individual vapor pressure contributions.\n"
            "3. Use blending equations or simulation tools to predict final RVP.\n"
            "4. Adjust blend ratios to achieve target RVP.\n"
            "5. Validate with laboratory testing (ASTM D323).\n"
            "6. Document blending operations and compliance status.\n"
            "7. Monitor for seasonal transitions and update blending recipes accordingly."
        ),
        key_factors=[
            "Blendstock RVP",
            "Ambient temperature",
            "Regulatory limits",
            "Blending sequence"
        ],
        primary_authority=[
            "ASTM D323",
            "EPA 40 CFR Part 80",
            "API 1509"
        ],
        burden_holder="Blending Operations Supervisor",
        adversary_position="Commercial team pressures for higher but non-compliant RVP blends to maximize volume.",
        counter_arguments=[
            "Non-compliance risks regulatory fines and product recalls.",
            "High RVP increases vapor lock and emissions."
        ],
        resolution_strategy="Strict adherence to regulatory limits and blending control systems.",
        entity_scope="Blending and distribution terminals",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR Part 80"
    ),
    DoctrineBlock(
        topic="Mercaptan Removal in LPG Streams",
        keywords=["mercaptan", "LPG", "sweetening", "Merox", "sulfur"],
        conclusion_template="Mercaptan removal from LPG is essential to meet odor, safety, and product quality standards.",
        reasoning_framework=(
            "1. Measure initial mercaptan sulfur content in LPG stream.\n"
            "2. Select appropriate sweetening process (e.g., Merox extraction, caustic wash).\n"
            "3. Optimize process parameters (temperature, caustic strength, contact time).\n"
            "4. Monitor effluent sulfur content and adjust operations as needed.\n"
            "5. Ensure compliance with product specifications (e.g., ASTM D1835).\n"
            "6. Maintain process equipment and chemical inventories.\n"
            "7. Document performance and troubleshoot any upsets."
        ),
        key_factors=[
            "Mercaptan sulfur content",
            "Process selection",
            "Operating conditions",
            "Product specification"
        ],
        primary_authority=[
            "ASTM D1835",
            "API Technical Data Book",
            "UOP Merox Process Manual"
        ],
        burden_holder="Process Engineer",
        adversary_position="Operations argues for reduced chemical usage to cut costs.",
        counter_arguments=[
            "Insufficient sweetening leads to off-spec product and safety hazards.",
            "Regulatory requirements mandate maximum sulfur levels."
        ],
        resolution_strategy="Balance chemical usage with product quality and regulatory compliance.",
        entity_scope="LPG processing and distribution",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D1835"
    ),
    DoctrineBlock(
        topic="Asphaltene Precipitation in Crude Oil Blending",
        keywords=["asphaltene", "precipitation", "crude blending", "stability"],
        conclusion_template="Asphaltene precipitation risk must be evaluated when blending crudes with differing solubility parameters.",
        reasoning_framework=(
            "1. Characterize asphaltene content and stability indices of candidate crudes.\n"
            "2. Use SARA analysis and colloidal instability index (CII) to predict precipitation risk.\n"
            "3. Conduct laboratory blending tests at relevant ratios.\n"
            "4. Monitor for visible precipitation, filterable solids, and changes in viscosity.\n"
            "5. Evaluate operational impacts (e.g., fouling, sludge formation).\n"
            "6. Adjust blending strategy to maintain stability.\n"
            "7. Document findings and update blending guidelines."
        ),
        key_factors=[
            "Asphaltene content",
            "Solubility parameter",
            "CII value",
            "Blend ratio"
        ],
        primary_authority=[
            "ASTM D6560",
            "SPE 16905",
            "API Technical Data Book"
        ],
        burden_holder="Blending Specialist",
        adversary_position="Commercial team pushes for aggressive blending to maximize margin.",
        counter_arguments=[
            "Precipitation leads to fouling and operational upsets.",
            "Short-term gains are offset by increased maintenance costs."
        ],
        resolution_strategy="Set conservative blending limits based on laboratory and historical data.",
        entity_scope="Crude blending operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D6560"
    ),
    DoctrineBlock(
        topic="Petroleum Coke Quality Assessment",
        keywords=["petroleum coke", "quality", "sulfur", "metals", "anode grade"],
        conclusion_template="Petroleum coke quality is determined by sulfur, metals, and volatile matter content relative to end-use requirements.",
        reasoning_framework=(
            "1. Analyze coke samples for sulfur, metals (Ni, V, Fe), and volatile matter.\n"
            "2. Compare results to specifications for fuel, anode, or needle coke grades.\n"
            "3. Assess impact of feedstock and coking process conditions on quality.\n"
            "4. Evaluate suitability for intended application (e.g., aluminum anodes, fuel).\n"
            "5. Document compliance and communicate with customers.\n"
            "6. Recommend process adjustments if off-spec coke is produced.\n"
            "7. Maintain traceability for regulatory and commercial purposes."
        ),
        key_factors=[
            "Sulfur content",
            "Metal content",
            "Volatile matter",
            "Coke structure"
        ],
        primary_authority=[
            "ASTM D6376",
            "ASTM D5004",
            "API Technical Data Book"
        ],
        burden_holder="Coking Unit Engineer",
        adversary_position="Buyer disputes coke quality based on isolated test results.",
        counter_arguments=[
            "Sampling and analysis must follow standardized methods.",
            "Process variability can affect batch-to-batch quality."
        ],
        resolution_strategy="Implement robust sampling and testing protocols, and communicate transparently with buyers.",
        entity_scope="Coking operations and product sales",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ASTM D6376"
    ),
    DoctrineBlock(
        topic="Petroleum Wastewater Treatment Standards",
        keywords=["wastewater", "treatment", "oil refinery", "discharge limits"],
        conclusion_template="Refinery wastewater must meet regulatory discharge limits for oil, solids, and priority pollutants.",
        reasoning_framework=(
            "1. Identify applicable discharge permits and regulatory standards (e.g., EPA NPDES, local limits).\n"
            "2. Characterize influent and effluent streams for oil, solids, metals, and organics.\n"
            "3. Evaluate treatment process performance (e.g., API separators, DAF, biological treatment).\n"
            "4. Monitor for excursions and investigate root causes.\n"
            "5. Implement corrective actions and process optimization as needed.\n"
            "6. Maintain records for regulatory reporting.\n"
            "7. Conduct periodic audits and training."
        ),
        key_factors=[
            "Oil and grease",
            "Total suspended solids",
            "Chemical oxygen demand",
            "Priority pollutants"
        ],
        primary_authority=[
            "EPA 40 CFR Part 419",
            "API 421",
            "ASTM D4281"
        ],
        burden_holder="Environmental Compliance Manager",
        adversary_position="Operations seeks to minimize treatment costs, risking non-compliance.",
        counter_arguments=[
            "Non-compliance leads to fines and reputational damage.",
            "Process upsets can be mitigated with proactive management."
        ],
        resolution_strategy="Invest in robust treatment systems and continuous monitoring.",
        entity_scope="Refinery wastewater treatment",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR Part 419"
    ),
    DoctrineBlock(
        topic="Catalytic Cracking Feed Quality Management",
        keywords=["FCC", "catalytic cracking", "feed quality", "contaminants"],
        conclusion_template="FCC feed quality must be managed to minimize contaminants that cause catalyst deactivation and emissions.",
        reasoning_framework=(
            "1. Characterize FCC feed for metals, nitrogen, Conradson carbon, and asphaltenes.\n"
            "2. Monitor trends in feed quality and correlate with unit performance.\n"
            "3. Implement feed pre-treatment or blending to control contaminants.\n"
            "4. Adjust operating conditions to mitigate adverse effects.\n"
            "5. Track catalyst activity and regeneration cycles.\n"
            "6. Communicate with upstream units to coordinate feed quality.\n"
            "7. Document actions and results for continuous improvement."
        ),
        key_factors=[
            "Metals content",
            "Nitrogen",
            "Conradson carbon",
            "Asphaltenes"
        ],
        primary_authority=[
            "API Technical Data Book",
            "UOP FCC Process Manual",
            "ASTM D189"
        ],
        burden_holder="FCC Unit Engineer",
        adversary_position="Feed supplier argues contaminants are within contractual limits.",
        counter_arguments=[
            "Even within limits, variability can impact unit performance.",
            "Long-term effects may not be immediately apparent."
        ],
        resolution_strategy="Set internal targets below contractual limits and monitor trends.",
        entity_scope="FCC operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API Technical Data Book, Section 7"
    ),
    DoctrineBlock(
        topic="Hydrogen Sulfide Management in Refinery Operations",
        keywords=["hydrogen sulfide", "H2S", "refinery", "safety", "emissions"],
        conclusion_template="Effective H2S management is critical for refinery safety, environmental compliance, and product quality.",
        reasoning_framework=(
            "1. Identify all sources of H2S generation and accumulation.\n"
            "2. Monitor H2S concentrations in process streams, tanks, and off-gas.\n"
            "3. Implement engineering controls (e.g., closed systems, scrubbers, scavengers).\n"
            "4. Train personnel in H2S hazard recognition and emergency response.\n"
            "5. Maintain and test detection and alarm systems.\n"
            "6. Ensure compliance with occupational and environmental regulations.\n"
            "7. Review incidents and update management plans."
        ),
        key_factors=[
            "H2S concentration",
            "Process containment",
            "Detection systems",
            "Personnel training"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.119",
            "API RP 49",
            "API RP 55"
        ],
        burden_holder="Health, Safety, and Environment Manager",
        adversary_position="Operations resists investment in additional controls.",
        counter_arguments=[
            "H2S incidents have severe consequences.",
            "Regulatory requirements are non-negotiable."
        ],
        resolution_strategy="Prioritize safety and compliance in all H2S management decisions.",
        entity_scope="All refinery units",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 55"
    ),
    DoctrineBlock(
        topic="Petroleum Product Traceability and Chain of Custody",
        keywords=["traceability", "chain of custody", "product movement", "quality"],
        conclusion_template="Maintaining chain of custody ensures product quality, regulatory compliance, and commercial integrity.",
        reasoning_framework=(
            "1. Document all product transfers, including source, destination, and batch identifiers.\n"
            "2. Implement robust sampling and testing protocols at custody transfer points.\n"
            "3. Maintain records of laboratory results and certificates of analysis.\n"
            "4. Use sealed and labeled containers to prevent tampering.\n"
            "5. Audit chain of custody records periodically.\n"
            "6. Investigate discrepancies and take corrective actions.\n"
            "7. Communicate transparently with all stakeholders."
        ),
        key_factors=[
            "Documentation",
            "Sampling protocols",
            "Tamper-evidence",
            "Audit trails"
        ],
        primary_authority=[
            "API 1169",
            "ASTM D5854",
            "API 1104"
        ],
        burden_holder="Logistics Manager",
        adversary_position="Buyer alleges contamination or off-spec product after transfer.",
        counter_arguments=[
            "Chain of custody records can demonstrate product integrity.",
            "Sampling errors can be identified and addressed."
        ],
        resolution_strategy="Enforce strict chain of custody procedures and independent verification.",
        entity_scope="Product movement and storage",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Petroleum Additive Compatibility",
        keywords=["additives", "compatibility", "blending", "product stability"],
        conclusion_template="Additive compatibility must be verified to prevent phase separation, precipitation, or loss of performance.",
        reasoning_framework=(
            "1. Review additive technical data sheets for compatibility information.\n"
            "2. Conduct laboratory blending tests at anticipated concentrations.\n"
            "3. Monitor for visible changes (e.g., haze, precipitation, color change).\n"
            "4. Evaluate impact on product performance (e.g., lubricity, detergency).\n"
            "5. Document test results and update blending guidelines.\n"
            "6. Communicate findings to operations and commercial teams.\n"
            "7. Reassess compatibility if feedstocks or additive suppliers change."
        ),
        key_factors=[
            "Additive chemistry",
            "Concentration",
            "Base oil properties",
            "Blending sequence"
        ],
        primary_authority=[
            "ASTM D4057",
            "API 1509",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Commercial team pushes for new additives without compatibility testing.",
        counter_arguments=[
            "Incompatible additives can cause off-spec product and warranty claims.",
            "Testing is essential for risk mitigation."
        ],
        resolution_strategy="Require compatibility testing before approving new additives.",
        entity_scope="Blending and product development",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D4057"
    ),
    DoctrineBlock(
        topic="Petroleum Laboratory Data Integrity",
        keywords=["laboratory", "data integrity", "quality control", "LIMS"],
        conclusion_template="Laboratory data integrity is maintained through robust quality control, documentation, and electronic data management.",
        reasoning_framework=(
            "1. Implement standardized test methods and calibration protocols.\n"
            "2. Use Laboratory Information Management Systems (LIMS) for data capture and traceability.\n"
            "3. Conduct regular audits and proficiency testing.\n"
            "4. Maintain detailed records of sample custody, preparation, and analysis.\n"
            "5. Investigate and resolve discrepancies promptly.\n"
            "6. Train personnel on data integrity principles.\n"
            "7. Review and update procedures as needed."
        ),
        key_factors=[
            "Standardized methods",
            "LIMS usage",
            "Quality control",
            "Personnel training"
        ],
        primary_authority=[
            "ASTM D6299",
            "ISO 17025",
            "API 1509"
        ],
        burden_holder="Laboratory Manager",
        adversary_position="Operations disputes lab results based on alleged data errors.",
        counter_arguments=[
            "LIMS and QC protocols ensure traceability and accuracy.",
            "Discrepancies can be resolved through retesting and audit."
        ],
        resolution_strategy="Enforce rigorous data integrity protocols and transparent communication.",
        entity_scope="Laboratory operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASTM D6299"
    ),
    DoctrineBlock(
        topic="Petroleum Pipeline Integrity Management",
        keywords=["pipeline", "integrity", "inspection", "API 1160"],
        conclusion_template="Pipeline integrity is managed through regular inspection, risk assessment, and maintenance per API 1160.",
        reasoning_framework=(
            "1. Develop and implement a Pipeline Integrity Management Program (IMP).\n"
            "2. Conduct baseline and periodic inspections (e.g., ILI, hydrotest).\n"
            "3. Assess risks based on pipeline age, material, and operating conditions.\n"
            "4. Prioritize repairs and mitigation based on risk ranking.\n"
            "5. Maintain detailed records of inspections and repairs.\n"
            "6. Train personnel in integrity management procedures.\n"
            "7. Review and update IMP regularly."
        ),
        key_factors=[
            "Inspection frequency",
            "Risk assessment",
            "Repair prioritization",
            "Recordkeeping"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA 49 CFR 195",
            "NACE SP0102"
        ],
        burden_holder="Pipeline Integrity Engineer",
        adversary_position="Operations resists downtime for inspection and repairs.",
        counter_arguments=[
            "Deferred maintenance increases risk of failure.",
            "Regulatory requirements mandate inspection intervals."
        ],
        resolution_strategy="Align inspection schedules with operations and regulatory deadlines.",
        entity_scope="Pipeline operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 1160"
    ),
    DoctrineBlock(
        topic="Petroleum Blending Economics",
        keywords=["blending", "economics", "optimization", "product value"],
        conclusion_template="Blending economics are optimized by maximizing product value within specification and operational constraints.",
        reasoning_framework=(
            "1. Identify available blendstocks and their properties.\n"
            "2. Define product specifications and market values.\n"
            "3. Use linear programming or blending models to optimize blends.\n"
            "4. Incorporate operational constraints (e.g., tankage, logistics, blend sequence).\n"
            "5. Validate model outputs with laboratory testing.\n"
            "6. Monitor market trends and adjust blending strategies.\n"
            "7. Document decisions and outcomes for continuous improvement."
        ),
        key_factors=[
            "Blendstock properties",
            "Product specifications",
            "Market prices",
            "Operational constraints"
        ],
        primary_authority=[
            "API 1509",
            "ASTM D323",
            "Blending software documentation"
        ],
        burden_holder="Blending Economist",
        adversary_position="Operations prioritizes throughput over optimal blend value.",
        counter_arguments=[
            "Value optimization increases profitability.",
            "Throughput constraints can be managed with planning."
        ],
        resolution_strategy="Balance economic optimization with operational realities.",
        entity_scope="Blending and commercial teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 1509"
    ),
    DoctrineBlock(
        topic="Petroleum Product Storage Compatibility",
        keywords=["storage", "compatibility", "product mixing", "tank"],
        conclusion_template="Product compatibility must be verified before commingling in storage tanks to prevent quality degradation.",
        reasoning_framework=(
            "1. Review product specifications and compatibility charts.\n"
            "2. Conduct laboratory mixing tests if compatibility is uncertain.\n"
            "3. Assess risk of phase separation, precipitation, or corrosion.\n"
            "4. Implement tank cleaning or segregation as needed.\n"
            "5. Document compatibility assessments and decisions.\n"
            "6. Communicate with logistics and commercial teams.\n"
            "7. Update compatibility guidelines based on experience."
        ),
        key_factors=[
            "Product specifications",
            "Mixing tests",
            "Tank history",
            "Corrosion risk"
        ],
        primary_authority=[
            "API 650",
            "ASTM D4057",
            "API 1509"
        ],
        burden_holder="Terminal Operations Manager",
        adversary_position="Commercial team pushes for commingling to maximize storage utilization.",
        counter_arguments=[
            "Incompatible mixing can cause off-spec product and tank cleaning costs.",
            "Segregation preserves product value."
        ],
        resolution_strategy="Require compatibility verification before commingling.",
        entity_scope="Storage and terminal operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 650"
    ),
    DoctrineBlock(
        topic="Petroleum Product Sampling Best Practices",
        keywords=["sampling", "best practices", "ASTM D4057", "quality control"],
        conclusion_template="Representative sampling is critical for accurate quality determination and dispute resolution.",
        reasoning_framework=(
            "1. Follow standardized sampling procedures (e.g., ASTM D4057).\n"
            "2. Use appropriate sampling equipment and containers.\n"
            "3. Label and seal samples to maintain chain of custody.\n"
            "4. Store and transport samples under controlled conditions.\n"
            "5. Document sampling details and any deviations.\n"
            "6. Train personnel in sampling techniques.\n"
            "7. Audit sampling practices periodically."
        ),
        key_factors=[
            "Sampling method",
            "Equipment cleanliness",
            "Chain of custody",
            "Personnel training"
        ],
        primary_authority=[
            "ASTM D4057",
            "API 1104",
            "API 1169"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer disputes results due to alleged sampling errors.",
        counter_arguments=[
            "Standardized methods ensure representativeness.",
            "Deviations can be identified and corrected."
        ],
        resolution_strategy="Enforce best practices and maintain detailed records.",
        entity_scope="Sampling and laboratory operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM D4057"
    ),
    DoctrineBlock(
        topic="Petroleum Product Additive Treat Rate Optimization",
        keywords=["additive", "treat rate", "optimization", "cost"],
        conclusion_template="Additive treat rates must be optimized to balance performance, cost, and compliance.",
        reasoning_framework=(
            "1. Review product specifications and additive performance curves.\n"
            "2. Conduct laboratory treat rate studies to determine minimum effective dose.\n"
            "3. Monitor product performance in the field.\n"
            "4. Adjust treat rates based on seasonal or feedstock changes.\n"
            "5. Document treat rate decisions and cost impact.\n"
            "6. Communicate with commercial and operations teams.\n"
            "7. Update treat rate guidelines as needed."
        ),
        key_factors=[
            "Additive performance",
            "Product specification",
            "Cost",
            "Seasonal variation"
        ],
        primary_authority=[
            "Additive supplier technical bulletins",
            "API 1509",
            "ASTM D4057"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Commercial team pushes for reduced treat rates to cut costs.",
        counter_arguments=[
            "Under-treating risks off-spec product and warranty claims.",
            "Optimization can reduce costs without compromising quality."
        ],
        resolution_strategy="Base treat rates on data and performance, not cost alone.",
        entity_scope="Blending and product development",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 1509"
    ),
    DoctrineBlock(
        topic="Petroleum Product Color and Appearance Control",
        keywords=["color", "appearance", "ASTM D1500", "product quality"],
        conclusion_template="Product color and appearance must meet specification to ensure market acceptance and regulatory compliance.",
        reasoning_framework=(
            "1. Analyze product samples for color using standardized methods (e.g., ASTM D1500).\n"
            "2. Investigate causes of off-color (e.g., feedstock, process upsets, contamination).\n"
            "3. Implement corrective actions (e.g., reprocessing, blending, additive use).\n"
            "4. Document color measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update process controls as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Color measurement",
            "Feedstock quality",
            "Process control",
            "Contamination risk"
        ],
        primary_authority=[
            "ASTM D1500",
            "API 1509",
            "Product specifications"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer rejects product based on color alone.",
        counter_arguments=[
            "Color does not always correlate with performance.",
            "Specification compliance is the primary criterion."
        ],
        resolution_strategy="Communicate specification compliance and investigate root causes of off-color.",
        entity_scope="Product quality management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D1500"
    ),
    DoctrineBlock(
        topic="Petroleum Product Sulfur Specification Management",
        keywords=["sulfur", "specification", "product", "compliance"],
        conclusion_template="Sulfur content must be controlled to meet product specifications and regulatory limits.",
        reasoning_framework=(
            "1. Monitor sulfur content in feedstocks and products.\n"
            "2. Use process controls (e.g., hydrodesulfurization) to reduce sulfur as needed.\n"
            "3. Validate results with laboratory testing (e.g., ASTM D4294).\n"
            "4. Document compliance and communicate with stakeholders.\n"
            "5. Investigate and resolve any non-compliance incidents.\n"
            "6. Update process and blending strategies as regulations evolve.\n"
            "7. Train personnel on sulfur management requirements."
        ),
        key_factors=[
            "Feedstock sulfur",
            "Process control",
            "Testing accuracy",
            "Regulatory limits"
        ],
        primary_authority=[
            "ASTM D4294",
            "EN 590",
            "EPA 40 CFR Part 80"
        ],
        burden_holder="Process Engineer",
        adversary_position="Operations argues for relaxed sulfur targets to increase throughput.",
        counter_arguments=[
            "Non-compliance risks fines and market exclusion.",
            "Sulfur reduction can be balanced with throughput."
        ],
        resolution_strategy="Set internal targets below regulatory limits and monitor trends.",
        entity_scope="Refining and blending operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D4294"
    ),
    DoctrineBlock(
        topic="Petroleum Product Flash Point Control",
        keywords=["flash point", "safety", "product specification", "ASTM D93"],
        conclusion_template="Flash point must meet specification to ensure safe handling, storage, and transport.",
        reasoning_framework=(
            "1. Test product samples for flash point using standardized methods (e.g., ASTM D93).\n"
            "2. Investigate causes of low flash point (e.g., light ends contamination, process upset).\n"
            "3. Implement corrective actions (e.g., reprocessing, blending, tank cleaning).\n"
            "4. Document flash point measurements and corrective actions.\n"
            "5. Communicate with logistics and safety teams.\n"
            "6. Update process controls as needed.\n"
            "7. Review incidents and update management plans."
        ),
        key_factors=[
            "Flash point measurement",
            "Contamination risk",
            "Process control",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D93",
            "API 1509",
            "Product specifications"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer rejects product based on flash point below specification.",
        counter_arguments=[
            "Flash point is a critical safety parameter.",
            "Specification compliance is non-negotiable."
        ],
        resolution_strategy="Enforce strict flash point control and investigate all non-compliance.",
        entity_scope="Product quality and logistics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM D93"
    ),
    DoctrineBlock(
        topic="Petroleum Product Water Content Control",
        keywords=["water content", "ASTM D6304", "product quality", "corrosion"],
        conclusion_template="Water content must be controlled to prevent corrosion, phase separation, and product degradation.",
        reasoning_framework=(
            "1. Test product samples for water content using standardized methods (e.g., ASTM D6304).\n"
            "2. Investigate sources of water (e.g., tank leaks, condensation, process upsets).\n"
            "3. Implement corrective actions (e.g., tank draining, drying, process adjustments).\n"
            "4. Document water content measurements and corrective actions.\n"
            "5. Communicate with operations and logistics teams.\n"
            "6. Update process controls as needed.\n"
            "7. Review incidents and update management plans."
        ),
        key_factors=[
            "Water content measurement",
            "Source identification",
            "Process control",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D6304",
            "API 1509",
            "Product specifications"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer rejects product based on water content above specification.",
        counter_arguments=[
            "High water content causes corrosion and operational issues.",
            "Specification compliance is essential for product quality."
        ],
        resolution_strategy="Enforce strict water content control and investigate all non-compliance.",
        entity_scope="Product quality and logistics",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D6304"
    ),
    DoctrineBlock(
        topic="Petroleum Product Density and Viscosity Control",
        keywords=["density", "viscosity", "ASTM D4052", "product quality"],
        conclusion_template="Density and viscosity must be controlled to meet product specifications and ensure proper performance.",
        reasoning_framework=(
            "1. Test product samples for density and viscosity using standardized methods (e.g., ASTM D4052, ASTM D445).\n"
            "2. Investigate causes of off-spec values (e.g., blending errors, contamination).\n"
            "3. Implement corrective actions (e.g., reblending, process adjustments).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with operations and logistics teams.\n"
            "6. Update process controls as needed.\n"
            "7. Review incidents and update management plans."
        ),
        key_factors=[
            "Density measurement",
            "Viscosity measurement",
            "Blending accuracy",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D4052",
            "ASTM D445",
            "Product specifications"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer rejects product based on density or viscosity outside specification.",
        counter_arguments=[
            "Density and viscosity affect product performance and handling.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and investigate all non-compliance.",
        entity_scope="Product quality and logistics",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM D4052"
    ),
    DoctrineBlock(
        topic="Petroleum Product Cloud and Pour Point Control",
        keywords=["cloud point", "pour point", "ASTM D2500", "ASTM D97", "cold flow"],
        conclusion_template="Cloud and pour points must be controlled to ensure product usability in cold climates.",
        reasoning_framework=(
            "1. Test product samples for cloud and pour points using standardized methods (e.g., ASTM D2500, ASTM D97).\n"
            "2. Investigate causes of high values (e.g., wax content, blending errors).\n"
            "3. Implement corrective actions (e.g., use of cold flow improvers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and logistics teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Cloud point",
            "Pour point",
            "Wax content",
            "Additive use"
        ],
        primary_authority=[
            "ASTM D2500",
            "ASTM D97",
            "Product specifications"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer rejects product based on poor cold flow properties.",
        counter_arguments=[
            "Cold flow properties are critical for certain markets.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product quality and commercial teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D2500"
    ),
    DoctrineBlock(
        topic="Petroleum Product Octane and Cetane Number Control",
        keywords=["octane", "cetane", "ASTM D2699", "ASTM D613", "engine performance"],
        conclusion_template="Octane and cetane numbers must meet specification to ensure engine performance and regulatory compliance.",
        reasoning_framework=(
            "1. Test gasoline for octane number (ASTM D2699/D2700) and diesel for cetane number (ASTM D613).\n"
            "2. Investigate causes of low values (e.g., blending errors, feedstock quality).\n"
            "3. Implement corrective actions (e.g., use of octane/cetane improvers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Octane number",
            "Cetane number",
            "Additive use",
            "Blending accuracy"
        ],
        primary_authority=[
            "ASTM D2699",
            "ASTM D613",
            "Product specifications"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer rejects product based on low octane or cetane.",
        counter_arguments=[
            "Engine performance and emissions depend on these parameters.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product quality and commercial teams",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D2699"
    ),
    DoctrineBlock(
        topic="Petroleum Product Aromatics and Olefins Control",
        keywords=["aromatics", "olefins", "ASTM D1319", "product specification"],
        conclusion_template="Aromatics and olefins content must be controlled to meet product specifications and regulatory limits.",
        reasoning_framework=(
            "1. Test product samples for aromatics and olefins using standardized methods (e.g., ASTM D1319).\n"
            "2. Investigate causes of high values (e.g., FCC operation, blending errors).\n"
            "3. Implement corrective actions (e.g., reblending, process adjustments).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and process strategies as needed.\n"
            "7. Review regulatory changes and adjust practices."
        ),
        key_factors=[
            "Aromatics content",
            "Olefins content",
            "Blending accuracy",
            "Process control"
        ],
        primary_authority=[
            "ASTM D1319",
            "EN 228",
            "EPA 40 CFR Part 80"
        ],
        burden_holder="Process Engineer",
        adversary_position="Operations argues for relaxed limits to increase yield.",
        counter_arguments=[
            "Aromatics and olefins affect emissions and product quality.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Set internal targets below regulatory limits and monitor trends.",
        entity_scope="Refining and blending operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM D1319"
    ),
    DoctrineBlock(
        topic="Petroleum Product Additive Shear Stability",
        keywords=["additive", "shear stability", "viscosity", "ASTM D6278"],
        conclusion_template="Additive shear stability must be verified to ensure viscosity retention in service.",
        reasoning_framework=(
            "1. Test additive-containing products for shear stability using standardized methods (e.g., ASTM D6278).\n"
            "2. Investigate causes of viscosity loss (e.g., additive selection, blending errors).\n"
            "3. Implement corrective actions (e.g., change additive, adjust treat rate).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with product development and quality teams.\n"
            "6. Update additive selection and blending guidelines as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Shear stability",
            "Viscosity retention",
            "Additive selection",
            "Blending accuracy"
        ],
        primary_authority=[
            "ASTM D6278",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports viscosity loss in service.",
        counter_arguments=[
            "Shear stability is critical for certain applications.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive selection.",
        entity_scope="Product development and quality teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D6278"
    ),
    DoctrineBlock(
        topic="Petroleum Product Oxidation Stability",
        keywords=["oxidation stability", "ASTM D2274", "product quality", "storage"],
        conclusion_template="Oxidation stability must be controlled to ensure product shelf life and performance.",
        reasoning_framework=(
            "1. Test product samples for oxidation stability using standardized methods (e.g., ASTM D2274).\n"
            "2. Investigate causes of poor stability (e.g., feedstock quality, additive depletion).\n"
            "3. Implement corrective actions (e.g., use of antioxidants, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Oxidation stability",
            "Feedstock quality",
            "Additive use",
            "Storage conditions"
        ],
        primary_authority=[
            "ASTM D2274",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports product degradation during storage.",
        counter_arguments=[
            "Oxidation stability is critical for certain markets.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product development and quality teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D2274"
    ),
    DoctrineBlock(
        topic="Petroleum Product Lubricity Control",
        keywords=["lubricity", "ASTM D6079", "diesel", "wear"],
        conclusion_template="Lubricity must be controlled to prevent excessive wear in diesel engine components.",
        reasoning_framework=(
            "1. Test diesel samples for lubricity using standardized methods (e.g., ASTM D6079).\n"
            "2. Investigate causes of poor lubricity (e.g., hydroprocessing severity, additive depletion).\n"
            "3. Implement corrective actions (e.g., use of lubricity improvers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Lubricity measurement",
            "Additive use",
            "Process severity",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D6079",
            "EN 590",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports excessive engine wear.",
        counter_arguments=[
            "Lubricity is critical for engine performance.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product development and quality teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM D6079"
    ),
    DoctrineBlock(
        topic="Petroleum Product Conductivity Control",
        keywords=["conductivity", "ASTM D2624", "static electricity", "additive"],
        conclusion_template="Conductivity must be controlled to prevent static discharge hazards during handling and transport.",
        reasoning_framework=(
            "1. Test product samples for conductivity using standardized methods (e.g., ASTM D2624).\n"
            "2. Investigate causes of low conductivity (e.g., additive depletion, blending errors).\n"
            "3. Implement corrective actions (e.g., use of conductivity improvers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with logistics and quality teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review incidents and update management plans."
        ),
        key_factors=[
            "Conductivity measurement",
            "Additive use",
            "Blending accuracy",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D2624",
            "API 1509",
            "Product specifications"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer reports static discharge incidents.",
        counter_arguments=[
            "Low conductivity increases static hazard.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product quality and logistics",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D2624"
    ),
    DoctrineBlock(
        topic="Petroleum Product Filterability and Particulate Control",
        keywords=["filterability", "particulate", "ASTM D5452", "cleanliness"],
        conclusion_template="Filterability and particulate content must be controlled to prevent filter plugging and equipment damage.",
        reasoning_framework=(
            "1. Test product samples for filterability and particulate content using standardized methods (e.g., ASTM D5452).\n"
            "2. Investigate sources of particulates (e.g., tank rust, process upsets, contamination).\n"
            "3. Implement corrective actions (e.g., filtration, tank cleaning, process adjustments).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with logistics and quality teams.\n"
            "6. Update process and maintenance strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Filterability",
            "Particulate content",
            "Source identification",
            "Process control"
        ],
        primary_authority=[
            "ASTM D5452",
            "Product specifications",
            "API 1509"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer reports filter plugging in service.",
        counter_arguments=[
            "Particulate control is critical for equipment reliability.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize process and maintenance.",
        entity_scope="Product quality and logistics",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D5452"
    ),
    DoctrineBlock(
        topic="Petroleum Product Acid Number Control",
        keywords=["acid number", "ASTM D664", "corrosion", "product quality"],
        conclusion_template="Acid number must be controlled to prevent corrosion and meet product specifications.",
        reasoning_framework=(
            "1. Test product samples for acid number using standardized methods (e.g., ASTM D664).\n"
            "2. Investigate causes of high acid number (e.g., feedstock quality, process upsets).\n"
            "3. Implement corrective actions (e.g., reprocessing, blending, additive use).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and process strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Acid number",
            "Feedstock quality",
            "Process control",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D664",
            "Product specifications",
            "API 1509"
        ],
        burden_holder="Process Engineer",
        adversary_position="Buyer reports corrosion in storage or use.",
        counter_arguments=[
            "Acid number is a key indicator of corrosivity.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize process and blending.",
        entity_scope="Product quality and commercial teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D664"
    ),
    DoctrineBlock(
        topic="Petroleum Product Stability During Storage",
        keywords=["stability", "storage", "degradation", "additive"],
        conclusion_template="Product stability during storage must be ensured to prevent degradation and maintain quality.",
        reasoning_framework=(
            "1. Assess product formulation for stability risks (e.g., oxidation, sediment formation).\n"
            "2. Use appropriate additives to enhance stability.\n"
            "3. Monitor storage conditions (temperature, tank cleanliness, exposure to air).\n"
            "4. Test stored product periodically for key quality parameters.\n"
            "5. Implement corrective actions if degradation is detected.\n"
            "6. Document storage and quality monitoring.\n"
            "7. Update storage and additive strategies as needed."
        ),
        key_factors=[
            "Product formulation",
            "Additive use",
            "Storage conditions",
            "Quality monitoring"
        ],
        primary_authority=[
            "Product specifications",
            "ASTM D2274",
            "API 1509"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer reports product degradation during storage.",
        counter_arguments=[
            "Stability is critical for product performance.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize storage and additive use.",
        entity_scope="Product quality and logistics",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D2274"
    ),
    DoctrineBlock(
        topic="Petroleum Product Compatibility with Elastomers and Metals",
        keywords=["compatibility", "elastomers", "metals", "product quality"],
        conclusion_template="Product compatibility with elastomers and metals must be verified to prevent equipment failure and warranty claims.",
        reasoning_framework=(
            "1. Review product formulation for known compatibility issues.\n"
            "2. Conduct laboratory compatibility tests with representative elastomers and metals.\n"
            "3. Monitor for swelling, cracking, corrosion, or other adverse effects.\n"
            "4. Document test results and update product data sheets.\n"
            "5. Communicate with customers and equipment suppliers.\n"
            "6. Update formulation or recommend material changes as needed.\n"
            "7. Review field performance and adjust practices."
        ),
        key_factors=[
            "Product formulation",
            "Elastomer type",
            "Metal type",
            "Test results"
        ],
        primary_authority=[
            "ASTM D471",
            "Product specifications",
            "Equipment supplier guidelines"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports equipment failure due to incompatibility.",
        counter_arguments=[
            "Compatibility testing is essential for risk mitigation.",
            "Specification compliance is required."
        ],
        resolution_strategy="Require compatibility testing and communicate results.",
        entity_scope="Product development and customer support",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D471"
    ),
    DoctrineBlock(
        topic="Petroleum Product Trace Metals Control",
        keywords=["trace metals", "ASTM D5708", "product quality", "catalyst poisoning"],
        conclusion_template="Trace metals must be controlled to prevent catalyst poisoning and meet product specifications.",
        reasoning_framework=(
            "1. Test product samples for trace metals using standardized methods (e.g., ASTM D5708).\n"
            "2. Investigate sources of metals (e.g., feedstock, corrosion, contamination).\n"
            "3. Implement corrective actions (e.g., feedstock selection, process adjustments, filtration).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with process and quality teams.\n"
            "6. Update process and blending strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Trace metals content",
            "Feedstock quality",
            "Process control",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D5708",
            "Product specifications",
            "API Technical Data Book"
        ],
        burden_holder="Process Engineer",
        adversary_position="Buyer reports catalyst poisoning or equipment damage.",
        counter_arguments=[
            "Trace metals control is critical for certain applications.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize process and blending.",
        entity_scope="Product quality and process teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D5708"
    ),
    DoctrineBlock(
        topic="Petroleum Product Ash Content Control",
        keywords=["ash content", "ASTM D482", "product quality", "combustion"],
        conclusion_template="Ash content must be controlled to prevent equipment fouling and meet product specifications.",
        reasoning_framework=(
            "1. Test product samples for ash content using standardized methods (e.g., ASTM D482).\n"
            "2. Investigate sources of ash (e.g., feedstock, contamination, additive use).\n"
            "3. Implement corrective actions (e.g., feedstock selection, process adjustments, filtration).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with process and quality teams.\n"
            "6. Update process and blending strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Ash content",
            "Feedstock quality",
            "Process control",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D482",
            "Product specifications",
            "API Technical Data Book"
        ],
        burden_holder="Process Engineer",
        adversary_position="Buyer reports equipment fouling or performance issues.",
        counter_arguments=[
            "Ash content control is critical for certain applications.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize process and blending.",
        entity_scope="Product quality and process teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D482"
    ),
    DoctrineBlock(
        topic="Petroleum Product Cold Soak Filtration Control",
        keywords=["cold soak filtration", "ASTM D7501", "biodiesel", "filter plugging"],
        conclusion_template="Cold soak filtration must be controlled to prevent filter plugging in biodiesel blends.",
        reasoning_framework=(
            "1. Test biodiesel blends for cold soak filtration time using standardized methods (e.g., ASTM D7501).\n"
            "2. Investigate causes of poor performance (e.g., feedstock quality, additive depletion).\n"
            "3. Implement corrective actions (e.g., use of cold flow improvers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with commercial and quality teams.\n"
            "6. Update blending and additive strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Cold soak filtration time",
            "Feedstock quality",
            "Additive use",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D7501",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports filter plugging in service.",
        counter_arguments=[
            "Cold soak filtration is critical for certain markets.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive use.",
        entity_scope="Product development and quality teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D7501"
    ),
    DoctrineBlock(
        topic="Petroleum Product Microbial Contamination Control",
        keywords=["microbial contamination", "bacteria", "fungi", "product quality"],
        conclusion_template="Microbial contamination must be controlled to prevent product degradation and operational issues.",
        reasoning_framework=(
            "1. Test product samples for microbial contamination using appropriate methods (e.g., ASTM D6469).\n"
            "2. Investigate sources of contamination (e.g., water ingress, tank cleanliness).\n"
            "3. Implement corrective actions (e.g., biocide treatment, tank cleaning, water removal).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with logistics and quality teams.\n"
            "6. Update storage and maintenance strategies as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Microbial contamination",
            "Water content",
            "Tank cleanliness",
            "Biocide use"
        ],
        primary_authority=[
            "ASTM D6469",
            "Product specifications",
            "API Technical Data Book"
        ],
        burden_holder="Quality Control Supervisor",
        adversary_position="Buyer reports product degradation or operational issues.",
        counter_arguments=[
            "Microbial contamination is a known risk in petroleum products.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize storage and biocide use.",
        entity_scope="Product quality and logistics",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D6469"
    ),
    DoctrineBlock(
        topic="Petroleum Product Antioxidant Additive Performance",
        keywords=["antioxidant", "additive", "performance", "ASTM D525"],
        conclusion_template="Antioxidant additive performance must be verified to ensure oxidation stability and product shelf life.",
        reasoning_framework=(
            "1. Test product samples for oxidation stability using standardized methods (e.g., ASTM D525).\n"
            "2. Investigate causes of poor performance (e.g., additive depletion, blending errors).\n"
            "3. Implement corrective actions (e.g., adjust treat rate, change additive supplier).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with product development and quality teams.\n"
            "6. Update additive selection and blending guidelines as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Oxidation stability",
            "Additive performance",
            "Blending accuracy",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D525",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports product degradation during storage.",
        counter_arguments=[
            "Antioxidant performance is critical for certain markets.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive selection.",
        entity_scope="Product development and quality teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D525"
    ),
    DoctrineBlock(
        topic="Petroleum Product Foam Tendency and Stability Control",
        keywords=["foam tendency", "foam stability", "ASTM D892", "product quality"],
        conclusion_template="Foam tendency and stability must be controlled to prevent operational issues in storage and use.",
        reasoning_framework=(
            "1. Test product samples for foam tendency and stability using standardized methods (e.g., ASTM D892).\n"
            "2. Investigate causes of excessive foaming (e.g., additive selection, contamination).\n"
            "3. Implement corrective actions (e.g., use of antifoam additives, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with product development and quality teams.\n"
            "6. Update additive selection and blending guidelines as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Foam tendency",
            "Foam stability",
            "Additive selection",
            "Contamination risk"
        ],
        primary_authority=[
            "ASTM D892",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports operational issues due to foaming.",
        counter_arguments=[
            "Foam control is critical for certain applications.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive selection.",
        entity_scope="Product development and quality teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D892"
    ),
    DoctrineBlock(
        topic="Petroleum Product Demulsibility Control",
        keywords=["demulsibility", "ASTM D1401", "water separation", "product quality"],
        conclusion_template="Demulsibility must be controlled to ensure water separation and prevent operational issues.",
        reasoning_framework=(
            "1. Test product samples for demulsibility using standardized methods (e.g., ASTM D1401).\n"
            "2. Investigate causes of poor demulsibility (e.g., additive selection, contamination).\n"
            "3. Implement corrective actions (e.g., use of demulsifiers, reblending).\n"
            "4. Document measurements and corrective actions.\n"
            "5. Communicate with product development and quality teams.\n"
            "6. Update additive selection and blending guidelines as needed.\n"
            "7. Review customer feedback and adjust practices."
        ),
        key_factors=[
            "Demulsibility",
            "Additive selection",
            "Contamination risk",
            "Specification limit"
        ],
        primary_authority=[
            "ASTM D1401",
            "Product specifications",
            "Additive supplier technical bulletins"
        ],
        burden_holder="Product Development Chemist",
        adversary_position="Buyer reports operational issues due to water separation.",
        counter_arguments=[
            "Demulsibility is critical for certain applications.",
            "Specification compliance is essential."
        ],
        resolution_strategy="Enforce strict control and optimize additive selection.",
        entity_scope="Product development and quality teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D1401"
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