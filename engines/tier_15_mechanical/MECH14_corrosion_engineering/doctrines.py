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
        topic="Electrochemical Corrosion Fundamentals",
        keywords=["electrochemical", "corrosion", "redox", "potential", "anode", "cathode", "passivity"],
        conclusion_template="Corrosion occurs when a metal undergoes oxidation at the anode, facilitated by electron flow to the cathode, governed by the electrochemical potential difference.",
        reasoning_framework="""
        Corrosion is fundamentally an electrochemical process involving the transfer of electrons from the metal (anode) to an oxidizing agent (often oxygen or ions in solution) at the cathode. The rate and extent of corrosion are determined by the potential difference between the anodic and cathodic sites, the conductivity of the electrolyte, and the availability of reactants. Passivity, the formation of a protective oxide film, can inhibit corrosion, but breakdown of this film leads to localized attack. The Nernst equation and Pourbaix diagrams are used to predict corrosion behavior under varying conditions. The process is governed by thermodynamics (feasibility) and kinetics (rate), with the mixed potential theory explaining the balance of anodic and cathodic reactions.
        """,
        key_factors=["Electrochemical potential", "Anode/cathode identification", "Electrolyte conductivity", "Passivity", "Thermodynamics", "Kinetics"],
        primary_authority=["Fontana & Greene", "Uhlig's Corrosion Handbook", "ASM Handbook Vol. 13"],
        burden_holder="Corrosion engineer",
        adversary_position="Corrosion is not primarily electrochemical; mechanical factors dominate.",
        counter_arguments=[
            "Electrochemical measurements consistently predict corrosion rates.",
            "Corrosion products and cell potentials are explained only by electrochemical theory.",
            "Mechanical factors may accelerate corrosion but do not initiate it."
        ],
        resolution_strategy="Demonstrate via laboratory electrochemical tests and theoretical modeling.",
        entity_scope="All metallic materials exposed to electrolytes",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fontana & Greene, Electrochemical Principles"
    ),
    DoctrineBlock(
        topic="Galvanic Corrosion between Dissimilar Metals",
        keywords=["galvanic", "dissimilar metals", "couple", "anode", "cathode", "potential", "electrolyte"],
        conclusion_template="Galvanic corrosion occurs when two dissimilar metals are electrically connected in the presence of an electrolyte, resulting in accelerated corrosion of the more anodic metal.",
        reasoning_framework="""
        When metals with different electrochemical potentials are coupled in an electrolyte, the metal with the lower potential acts as the anode and corrodes preferentially. The galvanic series ranks metals by their tendency to corrode when coupled. The severity of galvanic corrosion depends on the potential difference, area ratio (anode/cathode), conductivity of the electrolyte, and environmental conditions. Mitigation strategies include material selection, insulation, and application of protective coatings. The phenomenon is well documented in marine, pipeline, and infrastructure applications.
        """,
        key_factors=["Electrochemical potential difference", "Area ratio", "Electrolyte conductivity", "Material compatibility"],
        primary_authority=["NACE SP0170", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Design engineer",
        adversary_position="Galvanic corrosion is negligible with modern alloys.",
        counter_arguments=[
            "Field failures in pipelines and marine structures confirm galvanic corrosion.",
            "Galvanic series remains valid for modern alloys.",
            "Insufficient mitigation leads to rapid deterioration."
        ],
        resolution_strategy="Material selection and electrical isolation; verify via galvanic series.",
        entity_scope="Dissimilar metal assemblies in electrolytes",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0170, Galvanic Series"
    ),
    DoctrineBlock(
        topic="Pitting Corrosion due to Chloride-Induced Passivity Breakdown",
        keywords=["pitting", "chloride", "passivity", "localized corrosion", "stainless steel"],
        conclusion_template="Pitting corrosion is initiated when chloride ions penetrate and locally disrupt the passive film on susceptible alloys, leading to rapid, localized metal dissolution.",
        reasoning_framework="""
        Pitting corrosion is a highly localized form of attack that occurs when aggressive anions, particularly chlorides, breach the passive oxide film on metals such as stainless steel. The breakdown potential (Epit) defines the threshold above which pitting initiates. Once a pit forms, autocatalytic processes accelerate its growth due to localized acidification and chloride concentration. The severity is influenced by alloy composition, chloride concentration, temperature, and surface condition. Pitting resistance equivalent number (PREN) is used to assess alloy susceptibility. Prevention includes alloy selection, environmental control, and regular inspection.
        """,
        key_factors=["Chloride concentration", "Passive film integrity", "Breakdown potential", "Alloy composition", "Surface condition"],
        primary_authority=["ASTM G48", "NACE MR0175", "Uhlig's Corrosion Handbook"],
        burden_holder="Materials engineer",
        adversary_position="Pitting is rare in modern stainless steels.",
        counter_arguments=[
            "Field experience shows frequent pitting in chloride environments.",
            "PREN values correlate with pitting resistance.",
            "Surface contamination and weld defects increase susceptibility."
        ],
        resolution_strategy="Select alloys with high PREN; control chloride exposure.",
        entity_scope="Stainless steels and passive alloys in chloride environments",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM G48, PREN methodology"
    ),
    DoctrineBlock(
        topic="Crevice Corrosion due to Differential Aeration",
        keywords=["crevice corrosion", "differential aeration", "localized corrosion", "oxygen concentration", "stagnant zones"],
        conclusion_template="Crevice corrosion occurs in shielded areas where oxygen concentration is depleted, leading to localized anodic dissolution.",
        reasoning_framework="""
        Crevice corrosion is initiated in regions where the oxygen supply is restricted, such as under gaskets, deposits, or lap joints. The differential aeration creates a potential gradient, with the oxygen-depleted zone acting as the anode. The resulting acidification and chloride accumulation within the crevice accelerate metal dissolution. Factors influencing crevice corrosion include geometry, material, environmental conditions, and presence of deposits. Prevention strategies involve design modification, material selection, and regular cleaning.
        """,
        key_factors=["Oxygen concentration gradient", "Crevice geometry", "Material susceptibility", "Deposit presence"],
        primary_authority=["ASTM G78", "Fontana & Greene", "ASM Handbook Vol. 13"],
        burden_holder="Design engineer",
        adversary_position="Crevice corrosion is insignificant in well-designed systems.",
        counter_arguments=[
            "Crevice corrosion is observed in field failures despite good design.",
            "Deposits and biofilms can create unintentional crevices.",
            "Regular cleaning is often impractical."
        ],
        resolution_strategy="Minimize crevice formation; use resistant alloys; implement cleaning protocols.",
        entity_scope="Assemblies with crevice-prone geometries",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM G78, Differential Aeration Principle"
    ),
    DoctrineBlock(
        topic="Stress Corrosion Cracking (SCC) in Chloride and Caustic Environments",
        keywords=["SCC", "stress corrosion cracking", "chloride", "caustic", "cracking", "failure"],
        conclusion_template="SCC occurs when susceptible alloys are exposed to tensile stress and aggressive environments, leading to brittle fracture.",
        reasoning_framework="""
        Stress corrosion cracking is a synergistic phenomenon requiring three conditions: susceptible material, tensile stress, and a specific corrosive environment (chloride or caustic). The process initiates at microstructural defects or stress concentrators and propagates rapidly, often without significant general corrosion. Mechanisms include anodic dissolution and hydrogen embrittlement. SCC is particularly problematic in stainless steels (chloride SCC) and carbon steels (caustic SCC). Prevention involves stress relief, alloy selection, and environmental control.
        """,
        key_factors=["Material susceptibility", "Tensile stress", "Environment (chloride/caustic)", "Microstructural defects"],
        primary_authority=["NACE MR0175", "ASTM G36", "Uhlig's Corrosion Handbook"],
        burden_holder="Integrity engineer",
        adversary_position="SCC is rare and only occurs under extreme conditions.",
        counter_arguments=[
            "Field failures in pipelines and pressure vessels confirm SCC occurrence.",
            "Microstructural analysis reveals SCC features.",
            "Stress and environment thresholds are well documented."
        ],
        resolution_strategy="Apply stress relief, select resistant alloys, monitor environments.",
        entity_scope="Susceptible alloys under tensile stress",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175, SCC Criteria"
    ),
    DoctrineBlock(
        topic="Hydrogen Embrittlement, HIC, SOHIC, and SSC",
        keywords=["hydrogen embrittlement", "HIC", "SOHIC", "SSC", "sour service", "cracking"],
        conclusion_template="Hydrogen-induced cracking mechanisms occur when atomic hydrogen diffuses into steel, leading to embrittlement and cracking, especially in sour environments.",
        reasoning_framework="""
        Hydrogen embrittlement encompasses several cracking mechanisms: hydrogen-induced cracking (HIC), stepwise HIC (SOHIC), and sulfide stress cracking (SSC). In sour environments (H2S presence), hydrogen atoms generated by corrosion reactions diffuse into steel, accumulating at inclusions or stress concentrators. This leads to loss of ductility and brittle fracture. The severity depends on material microstructure, hardness, stress, and H2S concentration. NACE MR0175/ISO 15156 provides material selection criteria to mitigate these risks. Prevention includes using low-hardness steels, controlling stress, and environmental monitoring.
        """,
        key_factors=["Hydrogen generation", "Material microstructure", "Hardness", "Stress", "H2S concentration"],
        primary_authority=["NACE MR0175/ISO 15156", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Materials engineer",
        adversary_position="Modern steels are immune to hydrogen-induced cracking.",
        counter_arguments=[
            "Cracking is observed in low-hardness steels under sour service.",
            "NACE MR0175 criteria remain essential for material selection.",
            "Microstructural analysis confirms hydrogen-induced mechanisms."
        ],
        resolution_strategy="Select materials per NACE MR0175; monitor H2S and stress levels.",
        entity_scope="Steels in sour environments",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175/ISO 15156, Hydrogen Embrittlement Criteria"
    ),
    DoctrineBlock(
        topic="Erosion Corrosion due to Flow Velocity and Impingement",
        keywords=["erosion corrosion", "flow velocity", "impingement", "mechanical", "metal loss"],
        conclusion_template="Erosion corrosion is accelerated metal loss due to combined mechanical wear and electrochemical attack in high-velocity or impinging flows.",
        reasoning_framework="""
        Erosion corrosion occurs when high-velocity fluids or particles impinge on metal surfaces, removing protective films and exposing fresh metal to electrochemical attack. The rate of metal loss increases with flow velocity, turbulence, and presence of solid particles. Materials with high hardness and toughness resist erosion corrosion. Design modifications, such as reducing flow velocity and avoiding sharp bends, help mitigate the risk. Monitoring involves inspection for localized thinning and pitting.
        """,
        key_factors=["Flow velocity", "Impingement angle", "Material hardness", "Particle presence", "Design geometry"],
        primary_authority=["API RP 571", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Process engineer",
        adversary_position="Erosion corrosion is solely mechanical and not influenced by electrochemical factors.",
        counter_arguments=[
            "Electrochemical attack accelerates metal loss after film removal.",
            "Material selection influences erosion corrosion rate.",
            "Design changes reduce both mechanical and electrochemical contributions."
        ],
        resolution_strategy="Optimize flow conditions; select resistant materials; inspect regularly.",
        entity_scope="Pipelines, process equipment with high-velocity flows",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, Erosion Corrosion Mechanisms"
    ),
    DoctrineBlock(
        topic="Microbiologically Influenced Corrosion (MIC) by SRB and APB",
        keywords=["MIC", "microbiologically influenced corrosion", "SRB", "APB", "biofilm", "pipeline"],
        conclusion_template="MIC occurs when microbial activity, particularly by sulfate-reducing and acid-producing bacteria, accelerates corrosion through biofilm formation and metabolic byproducts.",
        reasoning_framework="""
        Microbiologically influenced corrosion is driven by the metabolic activity of bacteria such as sulfate-reducing (SRB) and acid-producing (APB) species. These microbes form biofilms on metal surfaces, creating localized environments that promote corrosion. SRB generate hydrogen sulfide, which reacts with steel, while APB produce organic acids. MIC is characterized by localized pitting and rapid metal loss. Detection involves microbiological sampling and corrosion monitoring. Mitigation includes biocide application, cleaning, and environmental control.
        """,
        key_factors=["Microbial activity", "Biofilm formation", "SRB/APB presence", "Environmental conditions", "Detection methods"],
        primary_authority=["NACE TM0194", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Corrosion engineer",
        adversary_position="MIC is rare and insignificant in pipelines.",
        counter_arguments=[
            "Field evidence shows MIC as a major cause of pipeline failures.",
            "Microbiological sampling confirms SRB/APB presence.",
            "Biocide treatment reduces corrosion rates."
        ],
        resolution_strategy="Implement biocide programs; monitor microbial activity; clean regularly.",
        entity_scope="Pipelines and process equipment exposed to water",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0194, MIC Detection"
    ),
    DoctrineBlock(
        topic="CO2 Corrosion (Sweet Corrosion) and de Waard-Milliams Model",
        keywords=["CO2 corrosion", "sweet corrosion", "de Waard-Milliams", "carbon steel", "pipeline"],
        conclusion_template="CO2 corrosion is a major threat to carbon steel pipelines, with rate predictions governed by the de Waard-Milliams model.",
        reasoning_framework="""
        CO2 corrosion, also known as sweet corrosion, occurs when carbon dioxide dissolves in water to form carbonic acid, which attacks carbon steel. The de Waard-Milliams model is used to predict corrosion rates based on CO2 partial pressure, temperature, flow velocity, and water chemistry. Protective iron carbonate films may form, but their stability is influenced by environmental conditions. Mitigation includes material selection, corrosion inhibitors, and environmental control. Monitoring involves coupon testing and real-time probes.
        """,
        key_factors=["CO2 partial pressure", "Water chemistry", "Temperature", "Flow velocity", "Film stability"],
        primary_authority=["de Waard-Milliams Model", "NACE TM0185", "API RP 571"],
        burden_holder="Corrosion engineer",
        adversary_position="CO2 corrosion is negligible in modern pipeline operations.",
        counter_arguments=[
            "Field failures confirm CO2 corrosion as a major threat.",
            "Model predictions align with observed corrosion rates.",
            "Inhibitor effectiveness is well documented."
        ],
        resolution_strategy="Apply inhibitors; monitor corrosion rates; select resistant materials.",
        entity_scope="Carbon steel pipelines transporting CO2-containing fluids",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="de Waard-Milliams Model, NACE TM0185"
    ),
    DoctrineBlock(
        topic="H2S Corrosion (Sour Service) and NACE MR0175/ISO 15156",
        keywords=["H2S corrosion", "sour service", "NACE MR0175", "ISO 15156", "pipeline", "steel"],
        conclusion_template="H2S corrosion in sour service environments is governed by NACE MR0175/ISO 15156, which defines material selection and operational limits.",
        reasoning_framework="""
        Hydrogen sulfide (H2S) in oil and gas environments causes severe corrosion and cracking in steels. NACE MR0175/ISO 15156 provides guidelines for material selection, hardness limits, and environmental thresholds to prevent sulfide stress cracking (SSC) and other sour service failures. The severity of H2S corrosion depends on concentration, temperature, pressure, and material microstructure. Monitoring and mitigation involve environmental control, material selection, and regular inspection.
        """,
        key_factors=["H2S concentration", "Material hardness", "Temperature", "Pressure", "Microstructure"],
        primary_authority=["NACE MR0175/ISO 15156", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Materials engineer",
        adversary_position="NACE MR0175 is overly conservative for modern steels.",
        counter_arguments=[
            "Field failures confirm the necessity of MR0175 criteria.",
            "Microstructural analysis reveals SSC in steels exceeding hardness limits.",
            "Environmental thresholds are based on empirical data."
        ],
        resolution_strategy="Select materials per MR0175; monitor H2S and hardness.",
        entity_scope="Steels in sour oil and gas environments",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175/ISO 15156, Sour Service Material Selection"
    ),
    DoctrineBlock(
        topic="Cathodic Protection: Impressed Current and Sacrificial Anode Systems",
        keywords=["cathodic protection", "impressed current", "sacrificial anode", "pipeline", "electrochemical"],
        conclusion_template="Cathodic protection prevents corrosion by shifting the metal potential to a non-corrosive state using impressed current or sacrificial anodes.",
        reasoning_framework="""
        Cathodic protection is an electrochemical technique that reduces corrosion by making the protected metal the cathode of a galvanic cell. Impressed current systems use external power sources to supply electrons, while sacrificial anode systems rely on more active metals (e.g., zinc, magnesium) to corrode preferentially. The effectiveness depends on current distribution, system design, and environmental conditions. Monitoring involves potential measurements and system maintenance. Standards such as NACE SP0169 define criteria for protection.
        """,
        key_factors=["System design", "Current distribution", "Anode material", "Environmental conditions", "Monitoring"],
        primary_authority=["NACE SP0169", "API RP 571", "Fontana & Greene"],
        burden_holder="Corrosion engineer",
        adversary_position="Cathodic protection is unnecessary with modern coatings.",
        counter_arguments=[
            "Coatings may fail, exposing metal to corrosion.",
            "Cathodic protection is essential for buried and submerged pipelines.",
            "Field data confirms effectiveness."
        ],
        resolution_strategy="Combine cathodic protection with coatings; monitor system performance.",
        entity_scope="Buried and submerged metallic structures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169, Cathodic Protection Criteria"
    ),
    DoctrineBlock(
        topic="Coating Systems: Epoxy, Polyurethane, FBE, and Three-Layer",
        keywords=["coating", "epoxy", "polyurethane", "FBE", "three-layer", "pipeline", "protection"],
        conclusion_template="Coating systems provide a physical barrier against corrosion, with selection based on environment, mechanical properties, and application method.",
        reasoning_framework="""
        Protective coatings such as epoxy, polyurethane, fusion-bonded epoxy (FBE), and three-layer systems are applied to pipelines and equipment to prevent corrosion. The effectiveness depends on adhesion, mechanical strength, chemical resistance, and application quality. Three-layer systems combine FBE, adhesive, and polyethylene for enhanced protection. Inspection and maintenance are critical to ensure long-term performance. Standards such as ISO 21809 and NACE SP0394 provide guidelines for selection and application.
        """,
        key_factors=["Coating type", "Adhesion", "Mechanical properties", "Chemical resistance", "Application quality"],
        primary_authority=["ISO 21809", "NACE SP0394", "API RP 571"],
        burden_holder="Coating engineer",
        adversary_position="Coatings are unnecessary with cathodic protection.",
        counter_arguments=[
            "Coatings reduce current demand for cathodic protection.",
            "Combined systems offer superior protection.",
            "Field experience confirms coating effectiveness."
        ],
        resolution_strategy="Select appropriate coatings; combine with cathodic protection; inspect regularly.",
        entity_scope="Pipelines and process equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 21809, NACE SP0394"
    ),
    DoctrineBlock(
        topic="Corrosion Inhibitors: Film-Forming and Neutralizing Types",
        keywords=["corrosion inhibitor", "film-forming", "neutralizing", "pipeline", "protection"],
        conclusion_template="Corrosion inhibitors reduce corrosion rates by forming protective films or neutralizing corrosive agents in the environment.",
        reasoning_framework="""
        Corrosion inhibitors are chemicals added to process fluids to reduce corrosion. Film-forming inhibitors adsorb onto metal surfaces, creating a barrier, while neutralizing inhibitors adjust pH to reduce acidity. The effectiveness depends on inhibitor type, concentration, fluid composition, and flow conditions. Monitoring involves chemical analysis and corrosion rate measurement. Standards such as NACE TM0193 provide guidelines for selection and application.
        """,
        key_factors=["Inhibitor type", "Concentration", "Fluid composition", "Flow conditions", "Monitoring"],
        primary_authority=["NACE TM0193", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Inhibitors are ineffective in turbulent flows.",
        counter_arguments=[
            "Inhibitor effectiveness is proven in field and laboratory tests.",
            "Proper dosing and monitoring ensure performance.",
            "Combined strategies enhance protection."
        ],
        resolution_strategy="Select appropriate inhibitors; monitor dosing and effectiveness.",
        entity_scope="Pipelines and process equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0193, Inhibitor Selection"
    ),
    DoctrineBlock(
        topic="Material Selection: CRA, Duplex, and Super Duplex",
        keywords=["material selection", "CRA", "duplex", "super duplex", "pipeline", "corrosion resistance"],
        conclusion_template="Material selection for corrosion resistance involves evaluating environmental conditions and selecting alloys such as CRA, duplex, or super duplex based on performance and cost.",
        reasoning_framework="""
        Corrosion-resistant alloys (CRA), duplex, and super duplex stainless steels are selected for environments where carbon steel is inadequate. Selection criteria include corrosion resistance, mechanical properties, weldability, and cost. PREN values are used to assess pitting resistance. Standards such as NACE MR0175 and API 5LD provide guidelines. Material selection must consider environmental conditions, expected life, and maintenance requirements. Failure to select appropriate materials leads to premature failures.
        """,
        key_factors=["Corrosion resistance", "Mechanical properties", "Weldability", "Cost", "Environmental conditions"],
        primary_authority=["NACE MR0175", "API 5LD", "ASM Handbook Vol. 13"],
        burden_holder="Materials engineer",
        adversary_position="Carbon steel is sufficient for most environments.",
        counter_arguments=[
            "Field failures demonstrate need for CRA and duplex alloys.",
            "PREN values correlate with performance.",
            "Cost-benefit analysis supports advanced alloys."
        ],
        resolution_strategy="Evaluate environmental conditions; select materials per standards.",
        entity_scope="Pipelines and process equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE MR0175, API 5LD"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring: Coupons, ER, LPR, and FSM",
        keywords=["corrosion monitoring", "coupon", "ER", "LPR", "FSM", "pipeline"],
        conclusion_template="Corrosion monitoring employs techniques such as coupons, electrical resistance (ER), linear polarization resistance (LPR), and field signature method (FSM) to assess corrosion rates and mechanisms.",
        reasoning_framework="""
        Monitoring corrosion involves deploying coupons, ER probes, LPR sensors, and FSM devices to measure metal loss and corrosion rates. Coupons provide direct measurement, ER probes assess cumulative loss, LPR sensors estimate instantaneous rates, and FSM detects localized corrosion. Data interpretation requires understanding environmental conditions and probe placement. Standards such as NACE TM0497 and API RP 571 guide monitoring programs. Effective monitoring enables proactive maintenance and integrity management.
        """,
        key_factors=["Monitoring technique", "Probe placement", "Data interpretation", "Environmental conditions", "Maintenance"],
        primary_authority=["NACE TM0497", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Integrity engineer",
        adversary_position="Monitoring is unnecessary with proper design.",
        counter_arguments=[
            "Monitoring detects unexpected corrosion mechanisms.",
            "Data supports maintenance decisions.",
            "Field experience confirms value of monitoring."
        ],
        resolution_strategy="Implement comprehensive monitoring; interpret data for proactive management.",
        entity_scope="Pipelines and process equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE TM0497, Corrosion Monitoring"
    ),
    DoctrineBlock(
        topic="Internal Corrosion Direct Assessment (ICDA)",
        keywords=["ICDA", "internal corrosion", "direct assessment", "pipeline", "integrity"],
        conclusion_template="ICDA is a structured methodology for assessing internal corrosion threats in pipelines using data integration and targeted inspections.",
        reasoning_framework="""
        Internal Corrosion Direct Assessment (ICDA) involves collecting operational, environmental, and inspection data to identify areas at risk for internal corrosion. The process includes pre-assessment, indirect inspection, direct examination, and post-assessment. Data integration from flow modeling, corrosion monitoring, and chemical analysis enables targeted inspections. Standards such as NACE SP0208 define ICDA methodology. ICDA supports integrity management and risk reduction.
        """,
        key_factors=["Data integration", "Inspection targeting", "Flow modeling", "Corrosion monitoring", "Chemical analysis"],
        primary_authority=["NACE SP0208", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Integrity engineer",
        adversary_position="ICDA is unnecessary with pigging and cleaning.",
        counter_arguments=[
            "ICDA identifies hidden corrosion threats.",
            "Pigging may miss localized corrosion.",
            "Data-driven assessment improves reliability."
        ],
        resolution_strategy="Implement ICDA per standards; integrate data for targeted inspections.",
        entity_scope="Pipelines with internal corrosion risk",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0208, ICDA Methodology"
    ),
    DoctrineBlock(
        topic="External Corrosion Direct Assessment (ECDA)",
        keywords=["ECDA", "external corrosion", "direct assessment", "pipeline", "integrity"],
        conclusion_template="ECDA is a structured methodology for assessing external corrosion threats in pipelines using data integration and targeted inspections.",
        reasoning_framework="""
        External Corrosion Direct Assessment (ECDA) involves collecting environmental, operational, and inspection data to identify areas at risk for external corrosion. The process includes pre-assessment, indirect inspection (e.g., soil resistivity, CP surveys), direct examination, and post-assessment. Standards such as NACE SP0502 define ECDA methodology. ECDA supports integrity management and risk reduction by focusing resources on high-risk areas.
        """,
        key_factors=["Environmental data", "CP surveys", "Soil resistivity", "Inspection targeting", "Data integration"],
        primary_authority=["NACE SP0502", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Integrity engineer",
        adversary_position="ECDA is redundant with coating and CP systems.",
        counter_arguments=[
            "ECDA identifies areas where coatings and CP are compromised.",
            "Data-driven assessment improves reliability.",
            "Field experience confirms ECDA effectiveness."
        ],
        resolution_strategy="Implement ECDA per standards; integrate data for targeted inspections.",
        entity_scope="Pipelines with external corrosion risk",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0502, ECDA Methodology"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management: ASME B31G and RSTRENG",
        keywords=["pipeline integrity", "ASME B31G", "RSTRENG", "assessment", "corrosion"],
        conclusion_template="Pipeline integrity management employs ASME B31G and RSTRENG methods to assess corrosion defects and determine safe operating limits.",
        reasoning_framework="""
        ASME B31G and RSTRENG are industry-standard methods for evaluating the severity of corrosion defects in pipelines. B31G provides a conservative approach based on defect length and depth, while RSTRENG offers a more detailed assessment using profile data. These methods determine maximum allowable operating pressure (MAOP) and support risk-based maintenance. Data from inspections, monitoring, and historical records inform integrity decisions. Standards ensure consistency and safety.
        """,
        key_factors=["Defect assessment", "MAOP calculation", "Inspection data", "Profile analysis", "Risk management"],
        primary_authority=["ASME B31G", "RSTRENG", "API RP 571"],
        burden_holder="Integrity engineer",
        adversary_position="B31G and RSTRENG are overly conservative and limit pipeline utilization.",
        counter_arguments=[
            "Conservatism ensures safety and regulatory compliance.",
            "Profile data enables accurate assessment.",
            "Field experience supports methodology."
        ],
        resolution_strategy="Apply B31G/RSTRENG; use profile data for accurate assessment.",
        entity_scope="Pipelines with corrosion defects",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31G, RSTRENG"
    ),
    DoctrineBlock(
        topic="Corrosion Allowance and Remaining Life Assessment",
        keywords=["corrosion allowance", "remaining life", "assessment", "pipeline", "integrity"],
        conclusion_template="Corrosion allowance and remaining life assessment determine the safe operating period of equipment based on corrosion rates and design margins.",
        reasoning_framework="""
        Corrosion allowance is the extra thickness added to equipment to account for expected metal loss over its service life. Remaining life assessment involves calculating the time until minimum allowable thickness is reached, using measured corrosion rates and design margins. Data from inspections, monitoring, and historical records inform decisions. Standards such as API 570 and ASME B31.3 provide guidelines. Accurate assessment supports proactive maintenance and risk reduction.
        """,
        key_factors=["Corrosion rate", "Design margin", "Inspection data", "Minimum allowable thickness", "Maintenance planning"],
        primary_authority=["API 570", "ASME B31.3", "API RP 571"],
        burden_holder="Integrity engineer",
        adversary_position="Corrosion allowance is unnecessary with modern materials.",
        counter_arguments=[
            "Field failures confirm need for corrosion allowance.",
            "Remaining life assessment prevents unexpected failures.",
            "Standards mandate assessment."
        ],
        resolution_strategy="Calculate corrosion allowance; assess remaining life per standards.",
        entity_scope="Pipelines and process equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 570, ASME B31.3"
    ),
    DoctrineBlock(
        topic="High Temperature Corrosion: Oxidation, Sulfidation, Carburization",
        keywords=["high temperature corrosion", "oxidation", "sulfidation", "carburization", "alloy", "process equipment"],
        conclusion_template="High temperature corrosion mechanisms include oxidation, sulfidation, and carburization, requiring alloy selection and environmental control for mitigation.",
        reasoning_framework="""
        High temperature corrosion occurs in process equipment exposed to elevated temperatures. Oxidation involves reaction with oxygen, forming protective or non-protective oxides. Sulfidation occurs in sulfur-containing environments, leading to rapid metal loss. Carburization involves absorption of carbon, altering material properties. Alloy selection, environmental control, and protective coatings are essential for mitigation. Standards such as API RP 571 and ASM Handbook Vol. 13 provide guidance.
        """,
        key_factors=["Temperature", "Environment (oxygen, sulfur, carbon)", "Alloy selection", "Coating", "Inspection"],
        primary_authority=["API RP 571", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Process engineer",
        adversary_position="High temperature corrosion is negligible in modern alloys.",
        counter_arguments=[
            "Field failures demonstrate high temperature corrosion.",
            "Alloy selection influences resistance.",
            "Environmental control reduces risk."
        ],
        resolution_strategy="Select appropriate alloys; control environment; inspect regularly.",
        entity_scope="Process equipment at elevated temperatures",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, High Temperature Corrosion"
    ),
    DoctrineBlock(
        topic="Localized Corrosion: Filiform, Intergranular, and Exfoliation",
        keywords=["localized corrosion", "filiform", "intergranular", "exfoliation", "aluminum", "stainless steel"],
        conclusion_template="Localized corrosion mechanisms such as filiform, intergranular, and exfoliation require specific alloy and environmental controls for mitigation.",
        reasoning_framework="""
        Filiform corrosion occurs under thin coatings, driven by moisture and oxygen. Intergranular corrosion affects grain boundaries in susceptible alloys, often due to improper heat treatment. Exfoliation is a form of intergranular corrosion in aluminum alloys, leading to layer separation. Prevention involves proper alloy selection, heat treatment, and environmental control. Inspection and maintenance are critical for early detection.
        """,
        key_factors=["Alloy susceptibility", "Heat treatment", "Coating quality", "Environmental conditions", "Inspection"],
        primary_authority=["ASM Handbook Vol. 13", "API RP 571", "Fontana & Greene"],
        burden_holder="Materials engineer",
        adversary_position="Localized corrosion is rare in modern alloys.",
        counter_arguments=[
            "Field experience confirms occurrence.",
            "Heat treatment and alloy selection are critical.",
            "Inspection detects early signs."
        ],
        resolution_strategy="Select appropriate alloys; apply proper heat treatment; inspect regularly.",
        entity_scope="Aluminum and stainless steel alloys",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASM Handbook Vol. 13, Localized Corrosion"
    ),
    DoctrineBlock(
        topic="Atmospheric Corrosion: Humidity, Pollutants, and Protective Measures",
        keywords=["atmospheric corrosion", "humidity", "pollutants", "coating", "steel"],
        conclusion_template="Atmospheric corrosion is driven by humidity and pollutants, requiring protective coatings and environmental control for mitigation.",
        reasoning_framework="""
        Atmospheric corrosion occurs when metals are exposed to humid air and pollutants such as SO2, NOx, and chlorides. The rate depends on relative humidity, pollutant concentration, and material susceptibility. Protective coatings, environmental control, and regular maintenance are essential for mitigation. Standards such as ISO 9223 and API RP 571 provide guidelines for assessment and protection.
        """,
        key_factors=["Humidity", "Pollutant concentration", "Coating quality", "Material susceptibility", "Maintenance"],
        primary_authority=["ISO 9223", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Maintenance engineer",
        adversary_position="Atmospheric corrosion is negligible in urban environments.",
        counter_arguments=[
            "Field data confirms significant corrosion in urban and industrial areas.",
            "Coating effectiveness depends on maintenance.",
            "Environmental monitoring supports assessment."
        ],
        resolution_strategy="Apply protective coatings; monitor environment; maintain regularly.",
        entity_scope="Steel structures exposed to atmosphere",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9223, Atmospheric Corrosion Assessment"
    ),
    DoctrineBlock(
        topic="Corrosion Under Insulation (CUI)",
        keywords=["CUI", "corrosion under insulation", "moisture", "insulation", "process equipment"],
        conclusion_template="Corrosion under insulation occurs when moisture penetrates insulation, leading to accelerated corrosion of underlying metal surfaces.",
        reasoning_framework="""
        CUI is a major threat to process equipment, particularly in humid environments. Moisture ingress through damaged or improperly installed insulation creates a corrosive environment. The rate depends on insulation type, environmental conditions, and maintenance. Prevention involves proper insulation installation, regular inspection, and use of resistant alloys. Standards such as API RP 571 and NACE SP0198 provide guidelines for mitigation.
        """,
        key_factors=["Insulation quality", "Moisture ingress", "Environmental conditions", "Inspection", "Alloy selection"],
        primary_authority=["API RP 571", "NACE SP0198", "ASM Handbook Vol. 13"],
        burden_holder="Maintenance engineer",
        adversary_position="CUI is rare with modern insulation materials.",
        counter_arguments=[
            "Field failures demonstrate CUI occurrence.",
            "Inspection and maintenance are critical.",
            "Alloy selection influences resistance."
        ],
        resolution_strategy="Install insulation properly; inspect regularly; select resistant alloys.",
        entity_scope="Process equipment with insulation",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE SP0198"
    ),
    DoctrineBlock(
        topic="Corrosion Fatigue",
        keywords=["corrosion fatigue", "cyclic loading", "cracking", "pipeline", "process equipment"],
        conclusion_template="Corrosion fatigue occurs when cyclic loading and corrosive environments combine to accelerate crack initiation and growth.",
        reasoning_framework="""
        Corrosion fatigue is a synergistic mechanism where cyclic mechanical loading and corrosive environments accelerate crack initiation and propagation. The rate depends on stress amplitude, frequency, environmental conditions, and material properties. Prevention involves reducing cyclic loads, selecting resistant materials, and controlling environment. Inspection and monitoring are essential for early detection.
        """,
        key_factors=["Cyclic loading", "Stress amplitude", "Environmental conditions", "Material properties", "Inspection"],
        primary_authority=["API RP 571", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Integrity engineer",
        adversary_position="Corrosion fatigue is insignificant in pipelines.",
        counter_arguments=[
            "Field failures confirm corrosion fatigue.",
            "Stress and environment thresholds are well documented.",
            "Inspection detects early signs."
        ],
        resolution_strategy="Reduce cyclic loads; select resistant materials; inspect regularly.",
        entity_scope="Pipelines and process equipment",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, Corrosion Fatigue"
    ),
    DoctrineBlock(
        topic="Selective Leaching: Dezincification, Graphitization",
        keywords=["selective leaching", "dezincification", "graphitization", "brass", "cast iron"],
        conclusion_template="Selective leaching mechanisms such as dezincification and graphitization require material selection and environmental control for mitigation.",
        reasoning_framework="""
        Dezincification occurs in brass alloys exposed to water, where zinc is selectively removed, leaving porous copper. Graphitization occurs in cast iron exposed to acidic environments, where iron is removed, leaving graphite. Prevention involves material selection, environmental control, and regular inspection. Standards such as API RP 571 and ASM Handbook Vol. 13 provide guidance.
        """,
        key_factors=["Material susceptibility", "Environmental conditions", "Inspection", "Alloy selection", "Mitigation"],
        primary_authority=["API RP 571", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Materials engineer",
        adversary_position="Selective leaching is rare in modern alloys.",
        counter_arguments=[
            "Field experience confirms occurrence.",
            "Material selection influences resistance.",
            "Inspection detects early signs."
        ],
        resolution_strategy="Select appropriate alloys; control environment; inspect regularly.",
        entity_scope="Brass and cast iron alloys",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, Selective Leaching"
    ),
    DoctrineBlock(
        topic="Corrosion in Concrete: Reinforcement and Carbonation",
        keywords=["corrosion in concrete", "reinforcement", "carbonation", "chloride", "passivity"],
        conclusion_template="Corrosion in concrete occurs when carbonation or chloride ingress disrupts the passive film on reinforcement, leading to metal loss and structural damage.",
        reasoning_framework="""
        Concrete provides alkaline protection to steel reinforcement, maintaining passivity. Carbonation reduces pH, while chloride ingress breaks down the passive film, leading to corrosion. The rate depends on environmental conditions, concrete quality, and maintenance. Prevention involves proper mix design, use of resistant alloys, and environmental control. Inspection and monitoring are essential for early detection.
        """,
        key_factors=["Concrete quality", "Environmental conditions", "Chloride ingress", "Carbonation", "Inspection"],
        primary_authority=["ACI 222R", "API RP 571", "ASM Handbook Vol. 13"],
        burden_holder="Structural engineer",
        adversary_position="Corrosion in concrete is negligible with modern mix designs.",
        counter_arguments=[
            "Field failures demonstrate corrosion in concrete.",
            "Mix design and maintenance influence resistance.",
            "Inspection detects early signs."
        ],
        resolution_strategy="Design concrete properly; inspect regularly; control environment.",
        entity_scope="Reinforced concrete structures",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ACI 222R, Corrosion in Concrete"
    ),
    DoctrineBlock(
        topic="Corrosion in Fire Water Systems",
        keywords=["corrosion", "fire water system", "pipeline", "MIC", "coating"],
        conclusion_template="Corrosion in fire water systems is driven by stagnant conditions, microbial activity, and coating failures, requiring regular inspection and maintenance.",
        reasoning_framework="""
        Fire water systems are prone to corrosion due to stagnant water, microbial activity (MIC), and coating failures. The rate depends on water quality, system design, and maintenance. Prevention involves regular inspection, biocide application, and coating maintenance. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Stagnant conditions", "MIC", "Coating quality", "Inspection", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Maintenance engineer",
        adversary_position="Corrosion is negligible in fire water systems.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC is a major threat.",
            "Inspection and maintenance are critical."
        ],
        resolution_strategy="Inspect regularly; apply biocides; maintain coatings.",
        entity_scope="Fire water systems",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Cooling Water Systems",
        keywords=["corrosion", "cooling water system", "pipeline", "MIC", "inhibitor"],
        conclusion_template="Corrosion in cooling water systems is driven by water chemistry, microbial activity, and inhibitor effectiveness, requiring monitoring and maintenance.",
        reasoning_framework="""
        Cooling water systems are prone to corrosion due to water chemistry, microbial activity (MIC), and inhibitor effectiveness. The rate depends on water quality, system design, and maintenance. Prevention involves regular monitoring, biocide application, and inhibitor dosing. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Water chemistry", "MIC", "Inhibitor effectiveness", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in cooling water systems.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC is a major threat.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; dose inhibitors.",
        entity_scope="Cooling water systems",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Produced Water Systems",
        keywords=["corrosion", "produced water system", "pipeline", "CO2", "H2S", "inhibitor"],
        conclusion_template="Corrosion in produced water systems is driven by CO2, H2S, and water chemistry, requiring inhibitor application and monitoring.",
        reasoning_framework="""
        Produced water systems are prone to corrosion due to CO2, H2S, and water chemistry. The rate depends on fluid composition, system design, and inhibitor effectiveness. Prevention involves regular monitoring, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["CO2", "H2S", "Water chemistry", "Inhibitor effectiveness", "Monitoring"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in produced water systems.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "CO2 and H2S are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; dose inhibitors; select resistant materials.",
        entity_scope="Produced water systems",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Injection Water Systems",
        keywords=["corrosion", "injection water system", "pipeline", "MIC", "inhibitor"],
        conclusion_template="Corrosion in injection water systems is driven by water chemistry, microbial activity, and inhibitor effectiveness, requiring monitoring and maintenance.",
        reasoning_framework="""
        Injection water systems are prone to corrosion due to water chemistry, microbial activity (MIC), and inhibitor effectiveness. The rate depends on water quality, system design, and maintenance. Prevention involves regular monitoring, biocide application, and inhibitor dosing. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Water chemistry", "MIC", "Inhibitor effectiveness", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in injection water systems.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC is a major threat.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; dose inhibitors.",
        entity_scope="Injection water systems",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Sea Water Systems",
        keywords=["corrosion", "sea water system", "pipeline", "chloride", "MIC"],
        conclusion_template="Corrosion in sea water systems is driven by chloride, microbial activity, and material selection, requiring monitoring and maintenance.",
        reasoning_framework="""
        Sea water systems are prone to corrosion due to high chloride concentration, microbial activity (MIC), and material selection. The rate depends on water quality, system design, and maintenance. Prevention involves regular monitoring, biocide application, and selection of resistant alloys. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Chloride concentration", "MIC", "Material selection", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in sea water systems.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "Chloride and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; select resistant alloys.",
        entity_scope="Sea water systems",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Oil and Gas Production Facilities",
        keywords=["corrosion", "oil and gas production", "facility", "CO2", "H2S", "MIC"],
        conclusion_template="Corrosion in oil and gas production facilities is driven by CO2, H2S, MIC, and water chemistry, requiring inhibitor application and monitoring.",
        reasoning_framework="""
        Oil and gas production facilities are prone to corrosion due to CO2, H2S, MIC, and water chemistry. The rate depends on fluid composition, system design, and inhibitor effectiveness. Prevention involves regular monitoring, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["CO2", "H2S", "MIC", "Water chemistry", "Inhibitor effectiveness"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in oil and gas production facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "CO2, H2S, and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; dose inhibitors; select resistant materials.",
        entity_scope="Oil and gas production facilities",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Gas Processing Facilities",
        keywords=["corrosion", "gas processing facility", "CO2", "H2S", "inhibitor"],
        conclusion_template="Corrosion in gas processing facilities is driven by CO2, H2S, and water chemistry, requiring inhibitor application and monitoring.",
        reasoning_framework="""
        Gas processing facilities are prone to corrosion due to CO2, H2S, and water chemistry. The rate depends on fluid composition, system design, and inhibitor effectiveness. Prevention involves regular monitoring, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["CO2", "H2S", "Water chemistry", "Inhibitor effectiveness", "Monitoring"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in gas processing facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "CO2 and H2S are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; dose inhibitors; select resistant materials.",
        entity_scope="Gas processing facilities",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Refinery Facilities",
        keywords=["corrosion", "refinery facility", "high temperature", "sulfidation", "carburization"],
        conclusion_template="Corrosion in refinery facilities is driven by high temperature, sulfidation, carburization, and water chemistry, requiring alloy selection and monitoring.",
        reasoning_framework="""
        Refinery facilities are prone to corrosion due to high temperature, sulfidation, carburization, and water chemistry. The rate depends on fluid composition, system design, and alloy selection. Prevention involves regular monitoring, selection of resistant alloys, and environmental control. Standards such as API RP 571 and ASM Handbook Vol. 13 provide guidance.
        """,
        key_factors=["High temperature", "Sulfidation", "Carburization", "Alloy selection", "Monitoring"],
        primary_authority=["API RP 571", "ASM Handbook Vol. 13", "Fontana & Greene"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in refinery facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "High temperature, sulfidation, and carburization are major threats.",
            "Monitoring and alloy selection are critical."
        ],
        resolution_strategy="Monitor regularly; select resistant alloys; control environment.",
        entity_scope="Refinery facilities",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, ASM Handbook Vol. 13"
    ),
    DoctrineBlock(
        topic="Corrosion in Petrochemical Facilities",
        keywords=["corrosion", "petrochemical facility", "CO2", "H2S", "MIC"],
        conclusion_template="Corrosion in petrochemical facilities is driven by CO2, H2S, MIC, and water chemistry, requiring inhibitor application and monitoring.",
        reasoning_framework="""
        Petrochemical facilities are prone to corrosion due to CO2, H2S, MIC, and water chemistry. The rate depends on fluid composition, system design, and inhibitor effectiveness. Prevention involves regular monitoring, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["CO2", "H2S", "MIC", "Water chemistry", "Inhibitor effectiveness"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in petrochemical facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "CO2, H2S, and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; dose inhibitors; select resistant materials.",
        entity_scope="Petrochemical facilities",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Offshore Facilities",
        keywords=["corrosion", "offshore facility", "sea water", "chloride", "MIC"],
        conclusion_template="Corrosion in offshore facilities is driven by sea water, chloride, MIC, and material selection, requiring monitoring and maintenance.",
        reasoning_framework="""
        Offshore facilities are prone to corrosion due to sea water, chloride, MIC, and material selection. The rate depends on water quality, system design, and maintenance. Prevention involves regular monitoring, biocide application, and selection of resistant alloys. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Sea water", "Chloride", "MIC", "Material selection", "Monitoring"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in offshore facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "Sea water, chloride, and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; select resistant alloys.",
        entity_scope="Offshore facilities",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Subsea Pipelines",
        keywords=["corrosion", "subsea pipeline", "sea water", "chloride", "MIC"],
        conclusion_template="Corrosion in subsea pipelines is driven by sea water, chloride, MIC, and material selection, requiring monitoring and maintenance.",
        reasoning_framework="""
        Subsea pipelines are prone to corrosion due to sea water, chloride, MIC, and material selection. The rate depends on water quality, system design, and maintenance. Prevention involves regular monitoring, biocide application, and selection of resistant alloys. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Sea water", "Chloride", "MIC", "Material selection", "Monitoring"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in subsea pipelines.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "Sea water, chloride, and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; select resistant alloys.",
        entity_scope="Subsea pipelines",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Storage Tanks",
        keywords=["corrosion", "storage tank", "MIC", "coating", "inspection"],
        conclusion_template="Corrosion in storage tanks is driven by water chemistry, MIC, coating quality, and inspection frequency, requiring monitoring and maintenance.",
        reasoning_framework="""
        Storage tanks are prone to corrosion due to water chemistry, MIC, coating quality, and inspection frequency. The rate depends on fluid composition, tank design, and maintenance. Prevention involves regular monitoring, biocide application, coating maintenance, and inspection. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Water chemistry", "MIC", "Coating quality", "Inspection", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Maintenance engineer",
        adversary_position="Corrosion is negligible in storage tanks.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC and coating quality are major threats.",
            "Inspection and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; maintain coatings; inspect frequently.",
        entity_scope="Storage tanks",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
    ),
    DoctrineBlock(
        topic="Corrosion in Heat Exchangers",
        keywords=["corrosion", "heat exchanger", "water chemistry", "MIC", "inhibitor"],
        conclusion_template="Corrosion in heat exchangers is driven by water chemistry, MIC, and inhibitor effectiveness, requiring monitoring and maintenance.",
        reasoning_framework="""
        Heat exchangers are prone to corrosion due to water chemistry, MIC, and inhibitor effectiveness. The rate depends on fluid composition, exchanger design, and maintenance. Prevention involves regular monitoring, biocide application, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["Water chemistry", "MIC", "Inhibitor effectiveness", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in heat exchangers.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC and inhibitor effectiveness are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; dose inhibitors; select resistant materials.",
        entity_scope="Heat exchangers",
        confidence=0.70,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Boilers",
        keywords=["corrosion", "boiler", "water chemistry", "oxygen", "inhibitor"],
        conclusion_template="Corrosion in boilers is driven by water chemistry, oxygen ingress, and inhibitor effectiveness, requiring monitoring and maintenance.",
        reasoning_framework="""
        Boilers are prone to corrosion due to water chemistry, oxygen ingress, and inhibitor effectiveness. The rate depends on fluid composition, boiler design, and maintenance. Prevention involves regular monitoring, oxygen removal, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["Water chemistry", "Oxygen ingress", "Inhibitor effectiveness", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in boilers.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "Oxygen ingress and inhibitor effectiveness are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; remove oxygen; dose inhibitors; select resistant materials.",
        entity_scope="Boilers",
        confidence=0.69,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Water Treatment Facilities",
        keywords=["corrosion", "water treatment facility", "water chemistry", "MIC", "inhibitor"],
        conclusion_template="Corrosion in water treatment facilities is driven by water chemistry, MIC, and inhibitor effectiveness, requiring monitoring and maintenance.",
        reasoning_framework="""
        Water treatment facilities are prone to corrosion due to water chemistry, MIC, and inhibitor effectiveness. The rate depends on fluid composition, facility design, and maintenance. Prevention involves regular monitoring, biocide application, inhibitor dosing, and material selection. Standards such as API RP 571 and NACE TM0193 provide guidance.
        """,
        key_factors=["Water chemistry", "MIC", "Inhibitor effectiveness", "Monitoring", "Maintenance"],
        primary_authority=["API RP 571", "NACE TM0193", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in water treatment facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "MIC and inhibitor effectiveness are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; dose inhibitors; select resistant materials.",
        entity_scope="Water treatment facilities",
        confidence=0.68,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0193"
    ),
    DoctrineBlock(
        topic="Corrosion in Desalination Facilities",
        keywords=["corrosion", "desalination facility", "sea water", "chloride", "MIC"],
        conclusion_template="Corrosion in desalination facilities is driven by sea water, chloride, MIC, and material selection, requiring monitoring and maintenance.",
        reasoning_framework="""
        Desalination facilities are prone to corrosion due to sea water, chloride, MIC, and material selection. The rate depends on water quality, facility design, and maintenance. Prevention involves regular monitoring, biocide application, and selection of resistant alloys. Standards such as API RP 571 and NACE TM0194 provide guidance.
        """,
        key_factors=["Sea water", "Chloride", "MIC", "Material selection", "Monitoring"],
        primary_authority=["API RP 571", "NACE TM0194", "ASM Handbook Vol. 13"],
        burden_holder="Process engineer",
        adversary_position="Corrosion is negligible in desalination facilities.",
        counter_arguments=[
            "Field failures demonstrate corrosion occurrence.",
            "Sea water, chloride, and MIC are major threats.",
            "Monitoring and maintenance are critical."
        ],
        resolution_strategy="Monitor regularly; apply biocides; select resistant alloys.",
        entity_scope="Desalination facilities",
        confidence=0.67,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 571, NACE TM0194"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]