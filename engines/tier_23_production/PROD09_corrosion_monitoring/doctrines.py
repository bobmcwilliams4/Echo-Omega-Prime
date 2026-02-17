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
        topic="CO2 Corrosion Mechanism and de Waard-Milliams Model",
        keywords=["CO2", "carbon dioxide", "corrosion", "de Waard-Milliams", "predictive model", "pipeline"],
        conclusion_template="CO2 corrosion rate is predicted using the de Waard-Milliams model, considering partial pressure, temperature, and flow velocity.",
        reasoning_framework=(
            "The de Waard-Milliams model is a semi-empirical approach used to estimate corrosion rates in carbon steel pipelines exposed to CO2-containing environments. "
            "The model incorporates key parameters such as CO2 partial pressure, temperature, steel composition, and flow velocity. "
            "Corrosion occurs due to the formation of carbonic acid, which accelerates steel dissolution. "
            "The model is validated against field data and laboratory experiments, with adjustments for localized conditions. "
            "Limitations include underestimation in high-velocity or turbulent flow, and lack of consideration for inhibitor presence. "
            "Risk assessment is performed by comparing predicted rates with acceptable thresholds for pipeline integrity. "
            "Mitigation strategies include material selection, inhibitor dosing, and operational controls. "
            "The model is referenced in NACE standards and is widely used in the oil and gas industry for pipeline design and maintenance planning. "
            "Uncertainties are addressed by periodic coupon monitoring and recalibration of model parameters."
        ),
        key_factors=[
            "CO2 partial pressure",
            "Temperature",
            "Steel composition",
            "Flow velocity",
            "Presence of inhibitors",
            "Water chemistry"
        ],
        primary_authority=[
            "NACE SP0775",
            "de Waard-Milliams (1975, 1984)",
            "API 571"
        ],
        burden_holder="Pipeline operator",
        adversary_position="Corrosion rates are underestimated; model does not account for all variables.",
        counter_arguments=[
            "Model validated against extensive field data.",
            "Periodic recalibration addresses uncertainties.",
            "Supplemented by coupon and ER probe monitoring."
        ],
        resolution_strategy="Combine model predictions with field monitoring and adjust mitigation strategies accordingly.",
        entity_scope="Carbon steel pipelines exposed to CO2 environments",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="de Waard-Milliams Model; NACE SP0775"
    ),
    DoctrineBlock(
        topic="H2S Corrosion and Sulfide Stress Cracking (SSC)",
        keywords=["H2S", "hydrogen sulfide", "corrosion", "SSC", "sulfide stress cracking", "pipeline", "sour service"],
        conclusion_template="H2S corrosion and SSC risk are managed by material selection, environmental control, and adherence to NACE MR0175.",
        reasoning_framework=(
            "Hydrogen sulfide (H2S) induces both general corrosion and localized cracking, particularly sulfide stress cracking (SSC), in susceptible steels. "
            "SSC is a form of hydrogen embrittlement exacerbated by tensile stress and sour environments. "
            "Risk assessment involves evaluating H2S partial pressure, pH, temperature, and steel hardness. "
            "NACE MR0175/ISO 15156 provides material selection guidelines for sour service, specifying maximum hardness and alloy composition. "
            "Mitigation includes environmental control (decreasing H2S concentration), stress reduction, and use of corrosion-resistant alloys. "
            "Monitoring is performed via periodic inspection and coupon testing. "
            "Failure to comply with standards can result in catastrophic pipeline failure. "
            "Countermeasures are validated through laboratory testing and field experience."
        ),
        key_factors=[
            "H2S partial pressure",
            "Steel hardness",
            "Tensile stress",
            "pH",
            "Temperature",
            "Material composition"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "API 571",
            "API 5L"
        ],
        burden_holder="Pipeline designer/operator",
        adversary_position="Material selection is overly conservative; operational controls suffice.",
        counter_arguments=[
            "SSC risk is unpredictable; conservative material selection prevents catastrophic failure.",
            "Operational controls may not eliminate all risk.",
            "Industry standards mandate compliance."
        ],
        resolution_strategy="Strict adherence to NACE MR0175/ISO 15156 and periodic review of material performance.",
        entity_scope="Pipelines and equipment in sour service environments",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175/ISO 15156"
    ),
    DoctrineBlock(
        topic="Microbiologically Influenced Corrosion (MIC)",
        keywords=["MIC", "microbiologically influenced corrosion", "SRB", "bacteria", "pipeline", "biofilm"],
        conclusion_template="MIC is managed by biocide dosing, monitoring of microbial activity, and regular inspection.",
        reasoning_framework=(
            "MIC occurs when microbial activity, particularly sulfate-reducing bacteria (SRB), accelerates corrosion in pipelines and equipment. "
            "Biofilm formation creates localized environments conducive to corrosion, often resulting in pitting. "
            "Risk assessment involves microbial enumeration, ATP testing, and coupon monitoring. "
            "Biocide dosing is tailored to microbial population and environmental conditions. "
            "Inspection techniques include ultrasonic thickness measurement and visual inspection for pitting. "
            "Industry standards recommend periodic monitoring and adjustment of biocide programs. "
            "Uncertainties arise from microbial adaptation and resistance; biocide rotation mitigates resistance development."
        ),
        key_factors=[
            "Microbial population",
            "SRB activity",
            "Biofilm formation",
            "Water chemistry",
            "Biocide effectiveness"
        ],
        primary_authority=[
            "NACE TM0212",
            "API 571",
            "ASTM G4"
        ],
        burden_holder="Pipeline operator",
        adversary_position="MIC is overstated; corrosion is primarily abiotic.",
        counter_arguments=[
            "Field evidence demonstrates MIC-induced pitting.",
            "Microbial enumeration correlates with corrosion rates.",
            "Biocide programs reduce MIC incidents."
        ],
        resolution_strategy="Implement robust monitoring and biocide dosing, with periodic review of effectiveness.",
        entity_scope="Pipelines and equipment exposed to water and microbial activity",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0212"
    ),
    DoctrineBlock(
        topic="Corrosion Coupon Monitoring",
        keywords=["corrosion coupon", "monitoring", "pipeline", "corrosion rate", "inspection"],
        conclusion_template="Corrosion coupon monitoring provides direct measurement of corrosion rates and informs mitigation strategies.",
        reasoning_framework=(
            "Corrosion coupons are exposed to process environments for a defined period, then retrieved and analyzed for weight loss and pitting. "
            "Coupon data provides empirical corrosion rates, supplementing predictive models. "
            "Placement is critical to ensure representative exposure; multiple locations may be required. "
            "Analysis includes weight loss, pit depth measurement, and metallographic examination. "
            "Coupon monitoring is referenced in NACE and API standards as a primary method for corrosion assessment. "
            "Limitations include non-continuous data and potential for non-representative exposure. "
            "Results are used to calibrate models and adjust inhibitor dosing."
        ),
        key_factors=[
            "Exposure duration",
            "Coupon placement",
            "Weight loss",
            "Pit depth",
            "Process conditions"
        ],
        primary_authority=[
            "NACE TM0497",
            "API 571",
            "ASTM G1"
        ],
        burden_holder="Corrosion engineer",
        adversary_position="Coupons do not represent all locations; data is limited.",
        counter_arguments=[
            "Multiple coupons improve representativeness.",
            "Supplemented by ER and LPR probes.",
            "Periodic retrieval ensures timely data."
        ],
        resolution_strategy="Deploy coupons at critical locations and integrate data with other monitoring methods.",
        entity_scope="Process pipelines and vessels",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0497"
    ),
    DoctrineBlock(
        topic="Electrical Resistance (ER) Probes",
        keywords=["ER probe", "electrical resistance", "corrosion monitoring", "pipeline", "continuous monitoring"],
        conclusion_template="ER probes provide continuous corrosion rate monitoring and early detection of changes in process conditions.",
        reasoning_framework=(
            "ER probes measure the change in electrical resistance of a sensing element exposed to the process environment. "
            "Continuous data allows for real-time detection of corrosion rate changes, enabling rapid response to process upsets. "
            "Probe placement is critical for representative data; calibration against coupon data is recommended. "
            "ER probe data is used to optimize inhibitor dosing and validate predictive models. "
            "Limitations include sensitivity to temperature fluctuations and potential for probe fouling. "
            "Industry standards recommend regular calibration and maintenance."
        ),
        key_factors=[
            "Probe placement",
            "Calibration",
            "Process conditions",
            "Temperature",
            "Data interpretation"
        ],
        primary_authority=[
            "NACE TM0185",
            "API 571",
            "ASTM G96"
        ],
        burden_holder="Corrosion monitoring team",
        adversary_position="ER probes are unreliable due to fouling and temperature effects.",
        counter_arguments=[
            "Regular maintenance mitigates fouling.",
            "Calibration addresses temperature sensitivity.",
            "Continuous data enables rapid response."
        ],
        resolution_strategy="Integrate ER probe data with coupon and LPR monitoring; maintain regular calibration schedule.",
        entity_scope="Process pipelines and vessels",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0185"
    ),
    DoctrineBlock(
        topic="Linear Polarization Resistance (LPR) Probes",
        keywords=["LPR probe", "linear polarization resistance", "corrosion monitoring", "pipeline", "electrochemical"],
        conclusion_template="LPR probes provide electrochemical measurement of corrosion rates, particularly in aqueous environments.",
        reasoning_framework=(
            "LPR probes measure the polarization resistance of a metal electrode, which correlates with corrosion rate in aqueous environments. "
            "Technique is sensitive to changes in water chemistry and inhibitor presence. "
            "LPR data is used to validate coupon and ER probe results and optimize inhibitor dosing. "
            "Limitations include requirement for conductive environments and sensitivity to flow conditions. "
            "Industry standards recommend periodic calibration and integration with other monitoring methods."
        ),
        key_factors=[
            "Electrolyte conductivity",
            "Probe calibration",
            "Water chemistry",
            "Flow conditions",
            "Data interpretation"
        ],
        primary_authority=[
            "NACE TM0186",
            "API 571",
            "ASTM G59"
        ],
        burden_holder="Corrosion monitoring team",
        adversary_position="LPR probes are limited to conductive environments; not universally applicable.",
        counter_arguments=[
            "LPR probes supplement other monitoring techniques.",
            "Calibration ensures data reliability.",
            "Used in conjunction with coupon and ER monitoring."
        ],
        resolution_strategy="Deploy LPR probes in suitable environments and integrate data with other monitoring methods.",
        entity_scope="Aqueous process environments",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0186"
    ),
    DoctrineBlock(
        topic="Ultrasonic Thickness Measurement (UTM) and Inspection",
        keywords=["UTM", "ultrasonic thickness", "inspection", "pipeline", "wall loss", "NDT"],
        conclusion_template="UTM provides non-destructive measurement of wall thickness and detection of localized corrosion.",
        reasoning_framework=(
            "UTM uses ultrasonic pulses to measure wall thickness in pipelines and vessels. "
            "Technique is non-destructive and capable of detecting localized corrosion, pitting, and general wall loss. "
            "Periodic UTM surveys are mandated by industry standards for integrity management. "
            "Data is used to assess remaining life, prioritize repairs, and validate corrosion models. "
            "Limitations include access requirements and potential for measurement error in rough surfaces. "
            "Resolution includes use of advanced techniques (phased array, TOFD) and periodic calibration."
        ),
        key_factors=[
            "Measurement accuracy",
            "Access to inspection locations",
            "Calibration",
            "Surface condition",
            "Frequency of inspection"
        ],
        primary_authority=[
            "API 570",
            "ASME B31.3",
            "ASTM E797"
        ],
        burden_holder="Inspection team",
        adversary_position="UTM is limited by access and surface condition; may miss localized corrosion.",
        counter_arguments=[
            "Advanced techniques improve detection.",
            "Multiple inspection points increase coverage.",
            "Periodic calibration ensures accuracy."
        ],
        resolution_strategy="Combine UTM with other NDT methods and prioritize inspection at high-risk locations.",
        entity_scope="Pipelines and vessels",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Corrosion Inhibitor Selection - Film-Forming Amines",
        keywords=["corrosion inhibitor", "film-forming amine", "pipeline", "selection", "chemical treatment"],
        conclusion_template="Film-forming amines are selected based on compatibility, effectiveness, and environmental impact.",
        reasoning_framework=(
            "Film-forming amines create a protective layer on steel surfaces, reducing corrosion rates in pipelines and process equipment. "
            "Selection criteria include compatibility with process fluids, effectiveness in target environments, and environmental impact. "
            "Performance is validated through laboratory testing, field trials, and monitoring of corrosion rates. "
            "Industry standards recommend periodic review of inhibitor performance and adjustment of dosing. "
            "Limitations include potential for emulsion formation and environmental regulations on discharge."
        ),
        key_factors=[
            "Compatibility with process fluids",
            "Effectiveness in target environment",
            "Environmental impact",
            "Dosing rate",
            "Monitoring of performance"
        ],
        primary_authority=[
            "NACE SP0108",
            "API 571",
            "ASTM G210"
        ],
        burden_holder="Corrosion engineer",
        adversary_position="Film-forming amines are ineffective in turbulent flow; alternatives are required.",
        counter_arguments=[
            "Field trials demonstrate effectiveness.",
            "Dosing adjustments address turbulence.",
            "Environmental impact assessed prior to selection."
        ],
        resolution_strategy="Select inhibitors based on comprehensive testing and regulatory compliance.",
        entity_scope="Pipelines and process equipment",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0108"
    ),
    DoctrineBlock(
        topic="Corrosion-Resistant Alloy (CRA) Material Selection",
        keywords=["CRA", "corrosion-resistant alloy", "material selection", "pipeline", "sour service", "alloy"],
        conclusion_template="CRA selection is based on environmental compatibility, mechanical properties, and cost-benefit analysis.",
        reasoning_framework=(
            "Corrosion-resistant alloys (CRAs) are selected for pipelines and equipment exposed to aggressive environments, including sour service. "
            "Selection criteria include environmental compatibility (H2S, CO2, chloride), mechanical properties, and cost-benefit analysis. "
            "Industry standards (NACE MR0175/ISO 15156) specify allowable alloys for sour service. "
            "Performance is validated through laboratory testing and field experience. "
            "Limitations include higher cost and potential for galvanic corrosion when used with carbon steel."
        ),
        key_factors=[
            "Environmental compatibility",
            "Mechanical properties",
            "Cost-benefit analysis",
            "Industry standards",
            "Field performance"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "API 571",
            "ASTM G48"
        ],
        burden_holder="Design engineer",
        adversary_position="CRAs are cost-prohibitive; carbon steel with inhibitors suffices.",
        counter_arguments=[
            "CRAs prevent catastrophic failure in aggressive environments.",
            "Long-term cost savings from reduced maintenance.",
            "Industry standards mandate CRA use in certain conditions."
        ],
        resolution_strategy="Perform detailed cost-benefit analysis and select materials per industry standards.",
        entity_scope="Pipelines and equipment in aggressive environments",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175/ISO 15156"
    ),
    DoctrineBlock(
        topic="Cathodic Protection (CP) for Pipelines and Structures",
        keywords=["cathodic protection", "CP", "pipeline", "structure", "corrosion control", "impressed current", "sacrificial anode"],
        conclusion_template="CP is implemented using impressed current or sacrificial anodes, monitored per NACE standards.",
        reasoning_framework=(
            "Cathodic protection (CP) reduces corrosion by shifting the electrochemical potential of steel below the corrosion threshold. "
            "CP systems use either impressed current or sacrificial anodes, selected based on pipeline length, environment, and operational requirements. "
            "Design and monitoring are governed by NACE standards, with periodic potential measurements and system maintenance. "
            "Limitations include interference from stray currents and coating degradation. "
            "Resolution includes regular system audits and integration with coating maintenance programs."
        ),
        key_factors=[
            "System design",
            "Potential measurements",
            "Anode selection",
            "Coating condition",
            "Interference management"
        ],
        primary_authority=[
            "NACE SP0169",
            "API 571",
            "ASTM G57"
        ],
        burden_holder="CP engineer",
        adversary_position="CP is unnecessary with high-quality coatings.",
        counter_arguments=[
            "Coating defects are inevitable; CP provides backup protection.",
            "Industry standards mandate CP for buried pipelines.",
            "CP effectiveness validated by potential measurements."
        ],
        resolution_strategy="Integrate CP with coating maintenance and monitor system performance.",
        entity_scope="Buried and submerged pipelines and structures",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management (IIM) and Inline Inspection (ILI)",
        keywords=["pipeline integrity", "IIM", "ILI", "inline inspection", "corrosion", "management", "pigging"],
        conclusion_template="IIM combines periodic ILI, risk assessment, and mitigation to ensure pipeline safety and reliability.",
        reasoning_framework=(
            "Pipeline integrity management (IIM) is a systematic approach to maintaining pipeline safety and reliability. "
            "Inline inspection (ILI) tools (smart pigs) detect wall loss, pitting, and other defects. "
            "Risk assessment incorporates inspection data, corrosion models, and operational history. "
            "Mitigation includes repair, replacement, and operational controls. "
            "Industry standards mandate periodic ILI and documentation of integrity management activities. "
            "Limitations include tool accuracy and access constraints. "
            "Resolution includes integration of multiple inspection techniques and continuous improvement."
        ),
        key_factors=[
            "Inspection frequency",
            "Tool accuracy",
            "Risk assessment",
            "Mitigation strategies",
            "Documentation"
        ],
        primary_authority=[
            "API 1169",
            "API 570",
            "NACE SP0102"
        ],
        burden_holder="Integrity management team",
        adversary_position="ILI tools miss small defects; risk is underestimated.",
        counter_arguments=[
            "Multiple inspection methods improve detection.",
            "Risk assessment incorporates tool limitations.",
            "Continuous improvement addresses gaps."
        ],
        resolution_strategy="Integrate ILI with other inspection and monitoring methods; update risk models regularly.",
        entity_scope="Transmission pipelines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Erosion-Corrosion in High-Velocity Systems",
        keywords=["erosion-corrosion", "high-velocity", "pipeline", "corrosion", "flow", "velocity"],
        conclusion_template="Erosion-corrosion is mitigated by controlling flow velocity, material selection, and protective coatings.",
        reasoning_framework=(
            "Erosion-corrosion occurs when high flow velocities accelerate wall loss through combined mechanical and chemical effects. "
            "Risk assessment involves evaluating flow velocity, particle content, and material susceptibility. "
            "Mitigation includes controlling flow rates, selecting erosion-resistant materials, and applying protective coatings. "
            "Industry standards recommend periodic inspection and monitoring of high-risk locations. "
            "Limitations include operational constraints and cost of material upgrades."
        ),
        key_factors=[
            "Flow velocity",
            "Particle content",
            "Material susceptibility",
            "Coating effectiveness",
            "Inspection frequency"
        ],
        primary_authority=[
            "API 571",
            "ASME B31.3",
            "ASTM G76"
        ],
        burden_holder="Operations team",
        adversary_position="Flow control is impractical; material upgrades are cost-prohibitive.",
        counter_arguments=[
            "Targeted flow control reduces risk.",
            "Cost-benefit analysis supports material upgrades.",
            "Coatings provide additional protection."
        ],
        resolution_strategy="Combine flow control, material selection, and coatings; prioritize mitigation at high-risk locations.",
        entity_scope="High-velocity process pipelines",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Galvanic Corrosion in Mixed-Metallurgy Systems",
        keywords=["galvanic corrosion", "mixed-metallurgy", "pipeline", "corrosion", "alloy", "electrochemical"],
        conclusion_template="Galvanic corrosion is managed by material compatibility, electrical isolation, and monitoring.",
        reasoning_framework=(
            "Galvanic corrosion occurs when dissimilar metals are electrically connected in a conductive environment, resulting in accelerated corrosion of the less noble metal. "
            "Risk assessment involves identifying material combinations, evaluating environmental conductivity, and assessing electrical connections. "
            "Mitigation includes material compatibility, electrical isolation (dielectric flanges), and monitoring for potential differences. "
            "Industry standards recommend periodic inspection and documentation of material transitions. "
            "Limitations include operational constraints and potential for isolation failure."
        ),
        key_factors=[
            "Material combinations",
            "Electrical isolation",
            "Environmental conductivity",
            "Inspection",
            "Monitoring"
        ],
        primary_authority=[
            "NACE SP0188",
            "API 571",
            "ASTM G71"
        ],
        burden_holder="Design engineer",
        adversary_position="Electrical isolation is unnecessary; corrosion is minimal.",
        counter_arguments=[
            "Field evidence demonstrates accelerated corrosion at material transitions.",
            "Industry standards mandate isolation.",
            "Monitoring detects early signs of galvanic corrosion."
        ],
        resolution_strategy="Ensure material compatibility and electrical isolation; monitor and inspect regularly.",
        entity_scope="Mixed-metallurgy process systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0188"
    ),
    DoctrineBlock(
        topic="Pitting Corrosion and Pitting Resistance Equivalent (PRE)",
        keywords=["pitting corrosion", "PRE", "pitting resistance", "pipeline", "alloy", "localized corrosion"],
        conclusion_template="Pitting corrosion risk is managed by alloy selection based on PRE, environmental control, and monitoring.",
        reasoning_framework=(
            "Pitting corrosion is a localized form of attack, often occurring in environments containing chlorides. "
            "Pitting Resistance Equivalent (PRE) is used to evaluate alloy susceptibility, with higher PRE indicating greater resistance. "
            "Risk assessment involves environmental analysis (chloride concentration, pH), alloy composition, and operational history. "
            "Mitigation includes selection of high-PRE alloys, environmental control, and periodic monitoring. "
            "Industry standards recommend documentation of alloy selection and monitoring of high-risk environments. "
            "Limitations include cost of high-PRE alloys and potential for unexpected environmental changes."
        ),
        key_factors=[
            "Chloride concentration",
            "Alloy composition",
            "PRE value",
            "Environmental control",
            "Monitoring"
        ],
        primary_authority=[
            "ASTM G48",
            "API 571",
            "NACE MR0175"
        ],
        burden_holder="Design engineer",
        adversary_position="High-PRE alloys are cost-prohibitive; monitoring suffices.",
        counter_arguments=[
            "Localized corrosion can result in rapid failure.",
            "PRE-based selection prevents pitting.",
            "Monitoring supplements alloy selection."
        ],
        resolution_strategy="Select alloys based on PRE and environmental risk; monitor and adjust as needed.",
        entity_scope="Pipelines and equipment in chloride environments",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM G48"
    ),
    DoctrineBlock(
        topic="Localized Corrosion Monitoring with Smart Sensors",
        keywords=["localized corrosion", "smart sensors", "monitoring", "pipeline", "real-time", "IoT"],
        conclusion_template="Smart sensor networks provide real-time detection of localized corrosion and enable rapid mitigation.",
        reasoning_framework=(
            "Smart sensors deployed in pipelines offer real-time monitoring of localized corrosion, including pitting and crevice corrosion. "
            "Sensors use electrochemical, ultrasonic, or optical techniques to detect corrosion events. "
            "Data is transmitted via IoT networks for analysis and response. "
            "Integration with integrity management systems enables rapid mitigation and reduces downtime. "
            "Limitations include sensor reliability, data interpretation, and network security."
        ),
        key_factors=[
            "Sensor reliability",
            "Data transmission",
            "Detection sensitivity",
            "Integration with management systems",
            "Network security"
        ],
        primary_authority=[
            "API 1169",
            "NACE TM0212",
            "IEEE 1451"
        ],
        burden_holder="Integrity management team",
        adversary_position="Sensor networks are costly and prone to failure.",
        counter_arguments=[
            "Cost offset by reduced downtime and rapid mitigation.",
            "Redundancy improves reliability.",
            "Industry adoption increasing."
        ],
        resolution_strategy="Deploy sensors in critical locations; ensure redundancy and robust data analysis.",
        entity_scope="Transmission pipelines and high-risk assets",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Crevice Corrosion in Flanged Connections",
        keywords=["crevice corrosion", "flanged connection", "pipeline", "localized corrosion", "seal"],
        conclusion_template="Crevice corrosion is mitigated by proper flange design, seal selection, and periodic inspection.",
        reasoning_framework=(
            "Crevice corrosion occurs in confined spaces, such as flanged connections, where stagnant conditions promote localized attack. "
            "Risk assessment involves evaluating flange design, seal material, and environmental exposure. "
            "Mitigation includes proper flange design, selection of corrosion-resistant seals, and periodic inspection. "
            "Industry standards recommend documentation of flange and seal selection and monitoring for early signs of corrosion."
        ),
        key_factors=[
            "Flange design",
            "Seal material",
            "Environmental exposure",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "ASME B16.5",
            "API 570",
            "ASTM G48"
        ],
        burden_holder="Design engineer",
        adversary_position="Crevice corrosion is rare; inspection suffices.",
        counter_arguments=[
            "Field evidence demonstrates frequent crevice corrosion in flanged connections.",
            "Seal selection reduces risk.",
            "Periodic inspection detects early signs."
        ],
        resolution_strategy="Optimize flange design and seal selection; implement regular inspection program.",
        entity_scope="Flanged connections in pipelines and vessels",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B16.5"
    ),
    DoctrineBlock(
        topic="Stress Corrosion Cracking (SCC) in Pipelines",
        keywords=["SCC", "stress corrosion cracking", "pipeline", "cracking", "corrosion", "stress"],
        conclusion_template="SCC risk is managed by material selection, stress reduction, and environmental control.",
        reasoning_framework=(
            "Stress corrosion cracking (SCC) occurs when susceptible materials are exposed to tensile stress and corrosive environments. "
            "Risk assessment involves evaluating material susceptibility, stress levels, and environmental factors (e.g., pH, chloride, temperature). "
            "Mitigation includes selection of SCC-resistant materials, reduction of residual and operational stresses, and environmental control. "
            "Industry standards recommend periodic inspection and documentation of mitigation measures."
        ),
        key_factors=[
            "Material susceptibility",
            "Stress levels",
            "Environmental factors",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE MR0175",
            "ASTM G123"
        ],
        burden_holder="Design engineer",
        adversary_position="SCC is rare; mitigation measures are unnecessary.",
        counter_arguments=[
            "SCC incidents have resulted in catastrophic failures.",
            "Industry standards mandate mitigation.",
            "Periodic inspection detects early signs."
        ],
        resolution_strategy="Select SCC-resistant materials and implement stress reduction measures; monitor and inspect regularly.",
        entity_scope="Transmission pipelines and high-stress assets",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Under Insulation (CUI)",
        keywords=["CUI", "corrosion under insulation", "pipeline", "insulation", "moisture", "inspection"],
        conclusion_template="CUI is managed by insulation selection, moisture control, and targeted inspection.",
        reasoning_framework=(
            "Corrosion under insulation (CUI) occurs when moisture penetrates insulation, creating conditions for accelerated corrosion. "
            "Risk assessment involves evaluating insulation material, environmental exposure, and moisture ingress. "
            "Mitigation includes selection of water-resistant insulation, moisture barriers, and targeted inspection at high-risk locations. "
            "Industry standards recommend periodic inspection and documentation of insulation and mitigation measures."
        ),
        key_factors=[
            "Insulation material",
            "Moisture ingress",
            "Environmental exposure",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 570",
            "ASTM C795",
            "NACE SP0198"
        ],
        burden_holder="Maintenance team",
        adversary_position="CUI is overstated; insulation prevents corrosion.",
        counter_arguments=[
            "Field evidence demonstrates frequent CUI incidents.",
            "Moisture barriers reduce risk.",
            "Targeted inspection detects early signs."
        ],
        resolution_strategy="Select appropriate insulation and implement moisture control; inspect at high-risk locations.",
        entity_scope="Insulated pipelines and vessels",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Atmospheric Corrosion of Above-Ground Pipelines",
        keywords=["atmospheric corrosion", "above-ground", "pipeline", "corrosion", "coating", "inspection"],
        conclusion_template="Atmospheric corrosion is managed by protective coatings, environmental control, and periodic inspection.",
        reasoning_framework=(
            "Atmospheric corrosion occurs in above-ground pipelines exposed to moisture, pollutants, and temperature fluctuations. "
            "Risk assessment involves evaluating environmental exposure, coating condition, and inspection frequency. "
            "Mitigation includes application of protective coatings, environmental control (e.g., shelters), and periodic inspection. "
            "Industry standards recommend documentation of coating application and maintenance."
        ),
        key_factors=[
            "Environmental exposure",
            "Coating condition",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 570",
            "NACE SP0394",
            "ASTM D3276"
        ],
        burden_holder="Maintenance team",
        adversary_position="Coatings are sufficient; inspection is unnecessary.",
        counter_arguments=[
            "Coating defects are inevitable; inspection detects early signs.",
            "Environmental control supplements coatings.",
            "Industry standards mandate inspection."
        ],
        resolution_strategy="Apply and maintain protective coatings; implement regular inspection program.",
        entity_scope="Above-ground pipelines",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Internal Corrosion Monitoring with Fiber Optic Sensors",
        keywords=["internal corrosion", "fiber optic sensors", "monitoring", "pipeline", "real-time", "distributed sensing"],
        conclusion_template="Fiber optic sensors provide distributed, real-time monitoring of internal corrosion and enable rapid response.",
        reasoning_framework=(
            "Fiber optic sensors deployed inside pipelines offer distributed, real-time monitoring of internal corrosion. "
            "Sensors detect changes in wall thickness, temperature, and strain, enabling early detection of corrosion events. "
            "Data is integrated with integrity management systems for rapid response. "
            "Limitations include sensor installation complexity and data interpretation challenges."
        ),
        key_factors=[
            "Sensor installation",
            "Detection sensitivity",
            "Data integration",
            "Response time",
            "Maintenance"
        ],
        primary_authority=[
            "API 1169",
            "NACE TM0212",
            "IEEE 1451"
        ],
        burden_holder="Integrity management team",
        adversary_position="Fiber optic sensors are costly and complex to install.",
        counter_arguments=[
            "Distributed sensing improves detection.",
            "Cost offset by reduced downtime.",
            "Industry adoption increasing."
        ],
        resolution_strategy="Deploy sensors in critical locations; ensure robust data integration and maintenance.",
        entity_scope="Transmission pipelines and high-risk assets",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Hydrogen-Induced Cracking (HIC) in Sour Environments",
        keywords=["HIC", "hydrogen-induced cracking", "sour environment", "pipeline", "corrosion", "cracking"],
        conclusion_template="HIC risk is managed by material selection, environmental control, and periodic inspection.",
        reasoning_framework=(
            "Hydrogen-induced cracking (HIC) occurs in steels exposed to sour environments, where hydrogen generated by corrosion accumulates and causes cracking. "
            "Risk assessment involves evaluating material susceptibility, environmental factors (H2S concentration, pH), and operational history. "
            "Mitigation includes selection of HIC-resistant materials, environmental control, and periodic inspection. "
            "Industry standards recommend documentation of material selection and inspection results."
        ),
        key_factors=[
            "Material susceptibility",
            "Environmental factors",
            "Inspection frequency",
            "Documentation",
            "Operational history"
        ],
        primary_authority=[
            "NACE TM0284",
            "API 571",
            "ASTM G35"
        ],
        burden_holder="Design engineer",
        adversary_position="HIC is rare; mitigation measures are unnecessary.",
        counter_arguments=[
            "HIC incidents have resulted in catastrophic failures.",
            "Industry standards mandate mitigation.",
            "Periodic inspection detects early signs."
        ],
        resolution_strategy="Select HIC-resistant materials and implement environmental control; monitor and inspect regularly.",
        entity_scope="Pipelines in sour environments",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0284"
    ),
    DoctrineBlock(
        topic="Corrosion Fatigue in Cyclically Loaded Pipelines",
        keywords=["corrosion fatigue", "cyclic loading", "pipeline", "corrosion", "fatigue", "inspection"],
        conclusion_template="Corrosion fatigue is managed by material selection, stress reduction, and periodic inspection.",
        reasoning_framework=(
            "Corrosion fatigue occurs when pipelines are subjected to cyclic loading in corrosive environments, resulting in accelerated crack growth. "
            "Risk assessment involves evaluating material susceptibility, loading history, and environmental factors. "
            "Mitigation includes selection of fatigue-resistant materials, reduction of cyclic stresses, and periodic inspection. "
            "Industry standards recommend documentation of mitigation measures and inspection results."
        ),
        key_factors=[
            "Material susceptibility",
            "Cyclic loading",
            "Environmental factors",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "ASTM E647",
            "NACE TM0212"
        ],
        burden_holder="Design engineer",
        adversary_position="Corrosion fatigue is rare; mitigation measures are unnecessary.",
        counter_arguments=[
            "Corrosion fatigue incidents have resulted in failures.",
            "Industry standards mandate mitigation.",
            "Periodic inspection detects early signs."
        ],
        resolution_strategy="Select fatigue-resistant materials and implement stress reduction; monitor and inspect regularly.",
        entity_scope="Cyclically loaded pipelines",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Chloride-Induced Corrosion in Cooling Water Systems",
        keywords=["chloride-induced corrosion", "cooling water", "pipeline", "corrosion", "chloride", "monitoring"],
        conclusion_template="Chloride-induced corrosion is managed by water chemistry control, material selection, and periodic monitoring.",
        reasoning_framework=(
            "Chloride-induced corrosion occurs in cooling water systems, particularly in carbon steel and low-alloy materials. "
            "Risk assessment involves evaluating chloride concentration, material susceptibility, and water chemistry. "
            "Mitigation includes water chemistry control (chloride reduction), selection of corrosion-resistant materials, and periodic monitoring. "
            "Industry standards recommend documentation of water chemistry and monitoring results."
        ),
        key_factors=[
            "Chloride concentration",
            "Material susceptibility",
            "Water chemistry",
            "Monitoring frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "ASTM G48",
            "NACE MR0175"
        ],
        burden_holder="Operations team",
        adversary_position="Chloride control is unnecessary; materials are sufficient.",
        counter_arguments=[
            "High chloride levels accelerate corrosion.",
            "Water chemistry control reduces risk.",
            "Monitoring detects early signs."
        ],
        resolution_strategy="Control water chemistry and select appropriate materials; monitor and document results.",
        entity_scope="Cooling water systems",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring Data Integration and Analytics",
        keywords=["corrosion monitoring", "data integration", "analytics", "pipeline", "management", "AI"],
        conclusion_template="Integrated analytics improve corrosion management by consolidating monitoring data and enabling predictive maintenance.",
        reasoning_framework=(
            "Corrosion monitoring generates large volumes of data from coupons, probes, sensors, and inspections. "
            "Integrated analytics consolidate data, enabling predictive maintenance and rapid response to corrosion events. "
            "Data integration involves standardization, validation, and correlation with operational history. "
            "AI and machine learning techniques are increasingly used for anomaly detection and risk assessment. "
            "Limitations include data quality, integration complexity, and interpretation challenges."
        ),
        key_factors=[
            "Data quality",
            "Integration complexity",
            "Analytics capability",
            "Predictive maintenance",
            "Interpretation"
        ],
        primary_authority=[
            "API 1169",
            "NACE TM0212",
            "IEEE 1451"
        ],
        burden_holder="Integrity management team",
        adversary_position="Data integration is unnecessary; manual analysis suffices.",
        counter_arguments=[
            "Integrated analytics improve detection and response.",
            "Predictive maintenance reduces downtime.",
            "Industry adoption increasing."
        ],
        resolution_strategy="Implement integrated analytics and validate data quality; use AI for anomaly detection.",
        entity_scope="Transmission pipelines and high-risk assets",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Corrosion Risk Assessment and Prioritization",
        keywords=["corrosion risk", "assessment", "prioritization", "pipeline", "management", "risk matrix"],
        conclusion_template="Corrosion risk is assessed using risk matrices and prioritized for mitigation based on likelihood and consequence.",
        reasoning_framework=(
            "Corrosion risk assessment involves evaluating likelihood and consequence of corrosion events using risk matrices. "
            "Assessment incorporates monitoring data, inspection results, and operational history. "
            "Prioritization enables targeted mitigation and resource allocation. "
            "Industry standards recommend documentation of risk assessment and mitigation strategies."
        ),
        key_factors=[
            "Likelihood",
            "Consequence",
            "Monitoring data",
            "Inspection results",
            "Resource allocation"
        ],
        primary_authority=[
            "API 1169",
            "NACE SP0102",
            "ISO 31000"
        ],
        burden_holder="Integrity management team",
        adversary_position="Risk assessment is subjective; prioritization is arbitrary.",
        counter_arguments=[
            "Risk matrices provide structured assessment.",
            "Data-driven prioritization improves outcomes.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Use structured risk matrices and data-driven prioritization; document mitigation strategies.",
        entity_scope="Transmission pipelines and high-risk assets",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1169"
    ),
    DoctrineBlock(
        topic="Corrosion Management in Aging Pipelines",
        keywords=["corrosion management", "aging pipeline", "pipeline", "inspection", "maintenance", "integrity"],
        conclusion_template="Corrosion management in aging pipelines requires enhanced inspection, maintenance, and risk assessment.",
        reasoning_framework=(
            "Aging pipelines are at increased risk of corrosion due to coating degradation, material fatigue, and operational history. "
            "Management includes enhanced inspection frequency, targeted maintenance, and updated risk assessment. "
            "Industry standards recommend documentation of inspection and maintenance activities and periodic review of integrity management plans."
        ),
        key_factors=[
            "Inspection frequency",
            "Maintenance",
            "Coating condition",
            "Operational history",
            "Risk assessment"
        ],
        primary_authority=[
            "API 570",
            "API 1169",
            "NACE SP0102"
        ],
        burden_holder="Integrity management team",
        adversary_position="Enhanced inspection is unnecessary; maintenance suffices.",
        counter_arguments=[
            "Aging pipelines are at increased risk.",
            "Enhanced inspection detects early signs.",
            "Industry standards mandate periodic review."
        ],
        resolution_strategy="Increase inspection frequency and update maintenance plans; review risk assessment regularly.",
        entity_scope="Aging transmission pipelines",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Corrosion Control in Water Injection Pipelines",
        keywords=["corrosion control", "water injection", "pipeline", "corrosion", "monitoring", "inhibitor"],
        conclusion_template="Corrosion control in water injection pipelines is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Water injection pipelines are susceptible to corrosion due to water chemistry and microbial activity. "
            "Control measures include inhibitor dosing, monitoring of corrosion rates, and periodic inspection. "
            "Industry standards recommend documentation of inhibitor programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Inhibitor dosing",
            "Monitoring",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Inhibitor dosing is unnecessary; monitoring suffices.",
        counter_arguments=[
            "Inhibitor dosing reduces corrosion rates.",
            "Monitoring detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement inhibitor dosing and monitor effectiveness; inspect and document results.",
        entity_scope="Water injection pipelines",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Multiphase Flow Pipelines",
        keywords=["corrosion monitoring", "multiphase flow", "pipeline", "oil", "gas", "water", "corrosion"],
        conclusion_template="Corrosion monitoring in multiphase flow pipelines requires integrated techniques and frequent data analysis.",
        reasoning_framework=(
            "Multiphase flow pipelines transport oil, gas, and water, creating complex corrosion environments. "
            "Monitoring requires integrated techniques (coupons, ER, LPR, sensors) and frequent data analysis. "
            "Industry standards recommend documentation of monitoring programs and periodic review of data."
        ),
        key_factors=[
            "Flow composition",
            "Monitoring techniques",
            "Data analysis",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Frequent data analysis enables rapid response.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and analyze data frequently; document and review results.",
        entity_scope="Multiphase flow pipelines",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Prevention in Offshore Pipelines",
        keywords=["corrosion prevention", "offshore pipeline", "pipeline", "coating", "CP", "inspection"],
        conclusion_template="Corrosion prevention in offshore pipelines is achieved by coatings, CP, and periodic inspection.",
        reasoning_framework=(
            "Offshore pipelines are exposed to aggressive environments, requiring robust corrosion prevention measures. "
            "Prevention includes application of protective coatings, cathodic protection, and periodic inspection. "
            "Industry standards recommend documentation of prevention measures and inspection results."
        ),
        key_factors=[
            "Coating application",
            "CP system",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 570",
            "NACE SP0169",
            "ASTM D3276"
        ],
        burden_holder="Maintenance team",
        adversary_position="Coatings and CP are unnecessary; inspection suffices.",
        counter_arguments=[
            "Aggressive environments require robust prevention.",
            "Coatings and CP reduce risk.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Apply coatings and CP; inspect and document results regularly.",
        entity_scope="Offshore pipelines",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Gas Gathering Systems",
        keywords=["corrosion monitoring", "gas gathering", "pipeline", "corrosion", "monitoring", "inspection"],
        conclusion_template="Corrosion monitoring in gas gathering systems is achieved by integrated techniques and periodic inspection.",
        reasoning_framework=(
            "Gas gathering systems are susceptible to corrosion due to water, CO2, and H2S content. "
            "Monitoring includes coupons, ER, LPR, and periodic inspection. "
            "Industry standards recommend documentation of monitoring programs and inspection results."
        ),
        key_factors=[
            "Gas composition",
            "Monitoring techniques",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Periodic inspection detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and inspect regularly; document and review results.",
        entity_scope="Gas gathering pipelines",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Control in Produced Water Pipelines",
        keywords=["corrosion control", "produced water", "pipeline", "corrosion", "monitoring", "inhibitor"],
        conclusion_template="Corrosion control in produced water pipelines is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Produced water pipelines are susceptible to corrosion due to water chemistry and microbial activity. "
            "Control measures include inhibitor dosing, monitoring of corrosion rates, and periodic inspection. "
            "Industry standards recommend documentation of inhibitor programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Inhibitor dosing",
            "Monitoring",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Inhibitor dosing is unnecessary; monitoring suffices.",
        counter_arguments=[
            "Inhibitor dosing reduces corrosion rates.",
            "Monitoring detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement inhibitor dosing and monitor effectiveness; inspect and document results.",
        entity_scope="Produced water pipelines",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Downhole Tubing",
        keywords=["corrosion monitoring", "downhole tubing", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion monitoring in downhole tubing is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Downhole tubing is susceptible to corrosion due to water, CO2, and H2S content. "
            "Monitoring includes coupons, ER, LPR, and periodic inspection. "
            "Industry standards recommend documentation of monitoring programs and inspection results."
        ),
        key_factors=[
            "Fluid composition",
            "Monitoring techniques",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Periodic inspection detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and inspect regularly; document and review results.",
        entity_scope="Downhole tubing",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Control in Injection Wells",
        keywords=["corrosion control", "injection well", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion control in injection wells is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Injection wells are susceptible to corrosion due to water chemistry and microbial activity. "
            "Control measures include inhibitor dosing, monitoring of corrosion rates, and periodic inspection. "
            "Industry standards recommend documentation of inhibitor programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Inhibitor dosing",
            "Monitoring",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Inhibitor dosing is unnecessary; monitoring suffices.",
        counter_arguments=[
            "Inhibitor dosing reduces corrosion rates.",
            "Monitoring detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement inhibitor dosing and monitor effectiveness; inspect and document results.",
        entity_scope="Injection wells",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Storage Tanks",
        keywords=["corrosion monitoring", "storage tank", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion monitoring in storage tanks is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Storage tanks are susceptible to corrosion due to water, CO2, and H2S content. "
            "Monitoring includes coupons, ER, LPR, and periodic inspection. "
            "Industry standards recommend documentation of monitoring programs and inspection results."
        ),
        key_factors=[
            "Fluid composition",
            "Monitoring techniques",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 653",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Periodic inspection detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and inspect regularly; document and review results.",
        entity_scope="Storage tanks",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 653"
    ),
    DoctrineBlock(
        topic="Corrosion Control in Water Treatment Plants",
        keywords=["corrosion control", "water treatment plant", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion control in water treatment plants is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Water treatment plants are susceptible to corrosion due to water chemistry and microbial activity. "
            "Control measures include inhibitor dosing, monitoring of corrosion rates, and periodic inspection. "
            "Industry standards recommend documentation of inhibitor programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Inhibitor dosing",
            "Monitoring",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Inhibitor dosing is unnecessary; monitoring suffices.",
        counter_arguments=[
            "Inhibitor dosing reduces corrosion rates.",
            "Monitoring detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement inhibitor dosing and monitor effectiveness; inspect and document results.",
        entity_scope="Water treatment plants",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Fire Water Systems",
        keywords=["corrosion monitoring", "fire water system", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion monitoring in fire water systems is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Fire water systems are susceptible to corrosion due to water chemistry and microbial activity. "
            "Monitoring includes coupons, ER, LPR, and periodic inspection. "
            "Industry standards recommend documentation of monitoring programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Monitoring techniques",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Periodic inspection detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and inspect regularly; document and review results.",
        entity_scope="Fire water systems",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Control in Utility Water Systems",
        keywords=["corrosion control", "utility water system", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion control in utility water systems is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Utility water systems are susceptible to corrosion due to water chemistry and microbial activity. "
            "Control measures include inhibitor dosing, monitoring of corrosion rates, and periodic inspection. "
            "Industry standards recommend documentation of inhibitor programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Inhibitor dosing",
            "Monitoring",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Inhibitor dosing is unnecessary; monitoring suffices.",
        counter_arguments=[
            "Inhibitor dosing reduces corrosion rates.",
            "Monitoring detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement inhibitor dosing and monitor effectiveness; inspect and document results.",
        entity_scope="Utility water systems",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Process Water Systems",
        keywords=["corrosion monitoring", "process water system", "corrosion", "monitoring", "inspection", "inhibitor"],
        conclusion_template="Corrosion monitoring in process water systems is achieved by inhibitor dosing, monitoring, and periodic inspection.",
        reasoning_framework=(
            "Process water systems are susceptible to corrosion due to water chemistry and microbial activity. "
            "Monitoring includes coupons, ER, LPR, and periodic inspection. "
            "Industry standards recommend documentation of monitoring programs and inspection results."
        ),
        key_factors=[
            "Water chemistry",
            "Monitoring techniques",
            "Inspection frequency",
            "Documentation",
            "Maintenance"
        ],
        primary_authority=[
            "API 571",
            "NACE TM0212",
            "ASTM G4"
        ],
        burden_holder="Operations team",
        adversary_position="Integrated monitoring is unnecessary; coupons suffice.",
        counter_arguments=[
            "Integrated techniques improve detection.",
            "Periodic inspection detects early signs.",
            "Industry standards mandate documentation."
        ],
        resolution_strategy="Implement integrated monitoring and inspect regularly; document and review results.",
        entity_scope="Process water systems",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 571"
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