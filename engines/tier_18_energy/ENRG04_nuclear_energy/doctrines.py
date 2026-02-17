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
        topic="nuclear_fission_chain_reaction",
        keywords=["fission", "chain reaction", "criticality", "neutron population", "uranium-235", "plutonium-239"],
        conclusion_template="A sustained nuclear fission chain reaction is achieved when each fission event causes, on average, one subsequent fission, maintaining a stable neutron population.",
        reasoning_framework=(
            "The chain reaction is governed by the neutron multiplication factor (k_eff). "
            "For a self-sustained reaction, k_eff must be exactly 1 (critical). "
            "If k_eff < 1, the reaction is subcritical and will die out; if k_eff > 1, it is supercritical and will increase exponentially. "
            "The process relies on fissile material (e.g., U-235, Pu-239) and a moderator to slow neutrons. "
            "Neutron leakage, non-fission captures, and the geometry of the core all affect criticality. "
            "Reactor design ensures that the arrangement of fuel, moderator, and control materials maintains k_eff at or near unity. "
            "Reactivity control is essential for safe operation, requiring precise management of neutron economy."
        ),
        key_factors=[
            "Neutron multiplication factor (k_eff)",
            "Fuel enrichment",
            "Moderator effectiveness",
            "Core geometry",
            "Neutron leakage",
            "Control material insertion"
        ],
        primary_authority=["IAEA", "NRC", "DOE"],
        burden_holder="Reactor operator/designer",
        adversary_position="Chain reactions are inherently unstable and cannot be reliably controlled.",
        counter_arguments=[
            "Modern reactors employ multiple redundant control systems.",
            "Negative temperature and void coefficients provide inherent safety.",
            "Extensive operational history demonstrates reliable control."
        ],
        resolution_strategy="Adopt defense-in-depth with engineered safety features and regulatory oversight.",
        entity_scope="All nuclear fission reactors",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50; IAEA Safety Standards Series No. SSR-2/1"
    ),
    DoctrineBlock(
        topic="neutron_moderation_thermalization",
        keywords=["neutron moderation", "thermal neutrons", "moderator", "hydrogen", "light water", "graphite"],
        conclusion_template="Neutron moderation is essential for converting fast neutrons to thermal energies, increasing the probability of fission in thermal reactors.",
        reasoning_framework=(
            "Moderators slow down fast neutrons through elastic scattering, reducing their kinetic energy to thermal levels (~0.025 eV). "
            "Materials with low atomic mass (e.g., hydrogen in light water, deuterium in heavy water, carbon in graphite) are most effective. "
            "The choice of moderator impacts reactor design, fuel requirements, and neutron economy. "
            "Thermal neutrons have a much higher cross-section for fission in U-235, enabling sustained chain reactions at lower enrichment. "
            "Moderator purity and temperature affect moderation efficiency and reactor reactivity."
        ),
        key_factors=[
            "Moderator material",
            "Moderator purity",
            "Moderator-to-fuel ratio",
            "Temperature effects",
            "Neutron absorption cross-section"
        ],
        primary_authority=["IAEA", "NRC"],
        burden_holder="Reactor designer",
        adversary_position="Fast reactors do not require moderation; moderation introduces complexity and safety concerns.",
        counter_arguments=[
            "Thermal reactors dominate commercial power production due to fuel cycle advantages.",
            "Moderator selection allows for inherent safety features.",
            "Fast reactors serve different purposes and are not a replacement for all applications."
        ],
        resolution_strategy="Select moderator based on reactor type, safety, and fuel cycle considerations.",
        entity_scope="Thermal nuclear reactors",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IAEA TECDOC-1198; NRC Regulatory Guide 1.42"
    ),
    DoctrineBlock(
        topic="pwr_primary_secondary_loop",
        keywords=["pressurized water reactor", "PWR", "primary loop", "secondary loop", "heat exchanger", "steam generator"],
        conclusion_template="PWRs utilize separate primary and secondary coolant loops to prevent radioactive contamination of the turbine and enhance safety.",
        reasoning_framework=(
            "In PWRs, the primary loop circulates pressurized water through the reactor core, removing heat generated by fission. "
            "This water transfers heat via steam generators to a secondary loop, where steam is produced to drive turbines. "
            "The separation of loops ensures that radioactive materials remain confined within the primary system, reducing the risk of contamination in the turbine hall. "
            "Pressure in the primary loop is maintained above the boiling point to prevent phase change, while the secondary loop operates at lower pressure. "
            "This design enhances operational safety and simplifies maintenance of non-nuclear components."
        ),
        key_factors=[
            "Primary loop pressure",
            "Steam generator integrity",
            "Coolant chemistry",
            "Heat exchanger efficiency",
            "Leak detection systems"
        ],
        primary_authority=["NRC", "EPRI"],
        burden_holder="Plant designer/operator",
        adversary_position="The dual-loop system increases complexity and cost without significant safety benefit.",
        counter_arguments=[
            "Physical separation of loops is a proven method to contain radioactivity.",
            "Operational experience shows reduced turbine contamination incidents.",
            "Maintenance and regulatory compliance are simplified for secondary systems."
        ],
        resolution_strategy="Maintain rigorous inspection and testing of loop boundaries and steam generators.",
        entity_scope="Pressurized water reactors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC Standard Review Plan 9.2.2; IEEE Std 497"
    ),
    DoctrineBlock(
        topic="pwr_reactivity_control_boron_rods",
        keywords=["PWR", "reactivity control", "boron", "control rods", "chemical shim", "boric acid"],
        conclusion_template="PWRs employ both boron in solution (chemical shim) and control rods to precisely manage core reactivity throughout the fuel cycle.",
        reasoning_framework=(
            "Soluble boron (as boric acid) is added to the primary coolant to provide uniform reactivity control. "
            "Control rods containing neutron-absorbing materials (e.g., boron, silver-indium-cadmium) are inserted or withdrawn for rapid reactivity adjustments. "
            "Boron concentration is gradually reduced as fuel burns up, maintaining criticality. "
            "This dual approach allows for both fine and coarse reactivity management, accommodating changes in fuel composition and operational demands. "
            "Careful monitoring of boron chemistry is essential to prevent corrosion and maintain system integrity."
        ),
        key_factors=[
            "Boron concentration",
            "Control rod worth",
            "Fuel burnup",
            "Coolant chemistry",
            "Reactivity feedbacks"
        ],
        primary_authority=["NRC", "EPRI"],
        burden_holder="Reactor operator",
        adversary_position="Chemical shim introduces complexity and risk of boron dilution accidents.",
        counter_arguments=[
            "Redundant systems monitor and control boron concentration.",
            "Procedures and training mitigate dilution risks.",
            "Boron chemistry is well-understood and managed."
        ],
        resolution_strategy="Implement robust boron monitoring and emergency procedures.",
        entity_scope="Pressurized water reactors",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NRC Information Notice 97-03; ANSI/ANS-8.1"
    ),
    DoctrineBlock(
        topic="bwr_direct_cycle_design",
        keywords=["boiling water reactor", "BWR", "direct cycle", "steam generation", "turbine", "reactor vessel"],
        conclusion_template="BWRs utilize a direct cycle design in which steam generated in the reactor vessel is sent directly to the turbine, simplifying plant layout but requiring careful radiological controls.",
        reasoning_framework=(
            "In BWRs, water boils within the reactor vessel, and the resulting steam is routed directly to the turbine generator. "
            "This eliminates the need for steam generators and a secondary loop, reducing system complexity and cost. "
            "However, radioactive isotopes (e.g., N-16) can be carried with the steam, necessitating shielding and remote operation of turbine components. "
            "Moisture separators and reheaters improve steam quality and turbine efficiency. "
            "The direct cycle design is optimized for operational simplicity and rapid load-following capability."
        ),
        key_factors=[
            "Steam quality",
            "Radiological controls",
            "Turbine shielding",
            "Moisture separator performance",
            "Coolant chemistry"
        ],
        primary_authority=["NRC", "EPRI"],
        burden_holder="Plant designer/operator",
        adversary_position="Direct cycle increases turbine contamination and maintenance costs.",
        counter_arguments=[
            "Design features minimize contamination risk.",
            "Operational protocols ensure worker safety.",
            "Economic benefits offset increased shielding requirements."
        ],
        resolution_strategy="Enhance shielding and remote handling in turbine areas.",
        entity_scope="Boiling water reactors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.70; GE BWR Design Manual"
    ),
    DoctrineBlock(
        topic="bwr_control_rods_cruciform",
        keywords=["BWR", "control rods", "cruciform", "neutron absorber", "reactivity control", "hafnium"],
        conclusion_template="BWRs use cruciform-shaped control rods inserted between fuel assemblies to provide rapid and effective reactivity control.",
        reasoning_framework=(
            "BWR control rods are typically cruciform in cross-section, allowing them to be inserted between four adjacent fuel assemblies. "
            "They are constructed from neutron-absorbing materials such as hafnium or boron carbide. "
            "The design maximizes neutron absorption efficiency and enables rapid shutdown (scram) in emergency situations. "
            "Control rod drive mechanisms are located below the reactor vessel, facilitating insertion against core pressure. "
            "Regular testing and maintenance ensure reliable operation throughout the fuel cycle."
        ),
        key_factors=[
            "Control rod material",
            "Insertion speed",
            "Drive mechanism reliability",
            "Neutron absorption cross-section",
            "Core geometry"
        ],
        primary_authority=["NRC", "GE"],
        burden_holder="Reactor operator",
        adversary_position="Cruciform rods are prone to mechanical failure and uneven wear.",
        counter_arguments=[
            "Material selection and design improvements address wear issues.",
            "Redundant drive systems enhance reliability.",
            "Extensive operational experience supports safety claims."
        ],
        resolution_strategy="Implement rigorous inspection and preventive maintenance programs.",
        entity_scope="Boiling water reactors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GE BWR/6 Technical Specifications; NRC Information Notice 85-58"
    ),
    DoctrineBlock(
        topic="nuclear_fuel_uo2_zircaloy",
        keywords=["nuclear fuel", "UO2", "zircaloy", "fuel pellet", "cladding", "oxidation"],
        conclusion_template="Uranium dioxide (UO2) fuel pellets clad in zircaloy tubes are the industry standard for light water reactors, offering high stability and corrosion resistance.",
        reasoning_framework=(
            "UO2 is chosen for its high melting point, chemical stability, and favorable neutronic properties. "
            "Zircaloy cladding provides mechanical strength and resists corrosion in high-temperature water environments. "
            "The combination minimizes the release of fission products and maintains fuel integrity during normal and transient conditions. "
            "Cladding oxidation and hydrogen uptake are managed through strict coolant chemistry control and material specifications. "
            "Fuel fabrication and quality assurance are governed by international standards."
        ),
        key_factors=[
            "Fuel enrichment",
            "Cladding integrity",
            "Coolant chemistry",
            "Fabrication quality",
            "Burnup limits"
        ],
        primary_authority=["IAEA", "ASTM", "NRC"],
        burden_holder="Fuel manufacturer/operator",
        adversary_position="Zircaloy is susceptible to high-temperature oxidation and hydrogen embrittlement.",
        counter_arguments=[
            "Operational limits prevent excessive temperatures.",
            "Advanced alloys and coatings mitigate embrittlement.",
            "Fuel performance is closely monitored."
        ],
        resolution_strategy="Adopt advanced cladding materials and maintain strict chemistry controls.",
        entity_scope="Light water reactors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASTM C996; NRC Regulatory Guide 1.126"
    ),
    DoctrineBlock(
        topic="fuel_burnup_depletion",
        keywords=["fuel burnup", "depletion", "fission products", "actinides", "fuel cycle", "reactivity loss"],
        conclusion_template="Fuel burnup and depletion are managed to optimize energy extraction while maintaining core reactivity and safety margins.",
        reasoning_framework=(
            "Burnup measures the amount of energy extracted from nuclear fuel, typically in MWd/kgU. "
            "As burnup increases, fissile material is consumed and fission products accumulate, reducing reactivity. "
            "Depletion calculations inform fuel management strategies, including shuffling and replacement schedules. "
            "High burnup improves fuel utilization but increases the challenge of managing fission gas release and cladding integrity. "
            "Regulatory limits ensure that safety margins are maintained throughout the fuel cycle."
        ),
        key_factors=[
            "Initial enrichment",
            "Burnup limits",
            "Fission product accumulation",
            "Cladding performance",
            "Fuel management strategy"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Reactor operator",
        adversary_position="High burnup increases the risk of fuel failure and complicates waste management.",
        counter_arguments=[
            "Operational experience supports safe high-burnup operation.",
            "Advanced fuel designs mitigate failure risks.",
            "Waste handling protocols are adapted for high-burnup fuel."
        ],
        resolution_strategy="Monitor fuel performance and adhere to regulatory burnup limits.",
        entity_scope="All nuclear reactors",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NRC NUREG/CR-6703; IAEA TECDOC-1299"
    ),
    DoctrineBlock(
        topic="delayed_neutrons_reactor_period",
        keywords=["delayed neutrons", "reactor period", "reactivity", "core kinetics", "control", "prompt criticality"],
        conclusion_template="Delayed neutrons are essential for controlling reactor kinetics, enabling safe and manageable changes in power level.",
        reasoning_framework=(
            "A small fraction of neutrons (~0.65% in U-235) are emitted by fission product precursors seconds after fission. "
            "These delayed neutrons extend the reactor period, allowing operators to control power changes safely. "
            "Prompt criticality (reactor controlled only by prompt neutrons) is avoided due to rapid, uncontrollable power increases. "
            "Reactivity insertions are managed to remain within delayed criticality, ensuring operational safety. "
            "Reactor protection systems are designed to respond within the delayed neutron time frame."
        ),
        key_factors=[
            "Delayed neutron fraction",
            "Reactivity insertion rate",
            "Core kinetics",
            "Operator response time",
            "Protection system speed"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Reactor operator",
        adversary_position="Delayed neutrons are too few to provide meaningful control in accident scenarios.",
        counter_arguments=[
            "Protection systems are designed for worst-case reactivity events.",
            "Training and procedures emphasize delayed neutron importance.",
            "Accident analyses incorporate delayed neutron behavior."
        ],
        resolution_strategy="Maintain conservative reactivity management and fast-acting protection systems.",
        entity_scope="All nuclear reactors",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.53; IAEA Safety Series No. 50-C-D"
    ),
    DoctrineBlock(
        topic="xenon_poisoning_iodine_dynamics",
        keywords=["xenon poisoning", "iodine-135", "xenon-135", "reactivity", "power maneuvering", "shutdown"],
        conclusion_template="Xenon-135 and iodine-135 dynamics significantly affect reactor reactivity, especially during power changes and after shutdown.",
        reasoning_framework=(
            "Iodine-135 decays to xenon-135, a potent neutron absorber (poison). "
            "During steady-state operation, xenon concentration reaches equilibrium, but power changes disrupt this balance. "
            "After shutdown, xenon concentration peaks ('xenon precluded startup'), temporarily inhibiting restart. "
            "Operators must anticipate xenon transients during load-following and refueling. "
            "Core design and operational procedures account for xenon and iodine behavior to maintain safe reactivity margins."
        ),
        key_factors=[
            "Fission product yield",
            "Neutron flux",
            "Decay rates",
            "Power history",
            "Reactivity margin"
        ],
        primary_authority=["NRC", "EPRI"],
        burden_holder="Reactor operator",
        adversary_position="Xenon transients can cause unexpected shutdowns and power oscillations.",
        counter_arguments=[
            "Operational planning accounts for xenon dynamics.",
            "Automated monitoring systems provide real-time feedback.",
            "Training ensures operator proficiency in managing xenon effects."
        ],
        resolution_strategy="Integrate xenon monitoring and predictive modeling into reactor control systems.",
        entity_scope="All thermal reactors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NRC NUREG-800, Section 4.3; IAEA TECDOC-1162"
    ),
    DoctrineBlock(
        topic="defense_in_depth_safety_philosophy",
        keywords=["defense-in-depth", "safety", "redundancy", "diversity", "barriers", "nuclear regulation"],
        conclusion_template="Defense-in-depth is the foundational safety philosophy for nuclear facilities, employing multiple layers of protection to prevent and mitigate accidents.",
        reasoning_framework=(
            "Defense-in-depth requires multiple, independent, and redundant safety systems and barriers. "
            "Physical barriers (fuel cladding, reactor vessel, containment) prevent release of radioactive materials. "
            "Engineered safety features and administrative controls provide additional protection. "
            "Diversity in safety systems ensures that common-cause failures do not compromise protection. "
            "Regulatory frameworks mandate defense-in-depth as a licensing requirement for all nuclear plants."
        ),
        key_factors=[
            "Physical barriers",
            "Redundant safety systems",
            "Diversity of design",
            "Administrative controls",
            "Regulatory compliance"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Licensee/plant operator",
        adversary_position="Defense-in-depth is costly and leads to over-engineering.",
        counter_arguments=[
            "Historical accidents demonstrate the necessity of multiple barriers.",
            "Cost is justified by risk reduction.",
            "International consensus supports defense-in-depth."
        ],
        resolution_strategy="Balance safety and cost through risk-informed, performance-based regulation.",
        entity_scope="All nuclear facilities",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix A; IAEA INSAG-10"
    ),
    DoctrineBlock(
        topic="eccs_emergency_core_cooling",
        keywords=["ECCS", "emergency core cooling", "LOCA", "safety injection", "core protection", "redundancy"],
        conclusion_template="Emergency Core Cooling Systems (ECCS) are required to rapidly restore core cooling during loss-of-coolant accidents, preventing fuel damage.",
        reasoning_framework=(
            "ECCS consists of multiple, redundant systems (e.g., high-pressure injection, low-pressure injection, accumulators) designed to supply coolant to the core during a LOCA. "
            "Systems are engineered to operate automatically and withstand single failures. "
            "Performance criteria are established to ensure that fuel cladding temperature and oxidation remain within safety limits. "
            "Periodic testing and maintenance verify ECCS readiness. "
            "Regulatory requirements specify ECCS capacity, reliability, and response time."
        ),
        key_factors=[
            "System redundancy",
            "Injection flow rates",
            "Automatic actuation",
            "Testing and maintenance",
            "Single-failure criterion"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Licensee/plant operator",
        adversary_position="ECCS complexity increases the risk of common-cause failures.",
        counter_arguments=[
            "System diversity and physical separation mitigate common-cause risks.",
            "Rigorous testing ensures reliability.",
            "Operational experience supports ECCS effectiveness."
        ],
        resolution_strategy="Maintain strict ECCS testing and incorporate lessons learned from operational events.",
        entity_scope="All power reactors",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50.46; IAEA Safety Standards SSR-2/1"
    ),
    DoctrineBlock(
        topic="containment_structure_function",
        keywords=["containment", "structure", "leak-tight", "pressure boundary", "accident mitigation", "concrete", "steel liner"],
        conclusion_template="Containment structures provide a robust, leak-tight barrier to prevent the release of radioactive materials during accidents.",
        reasoning_framework=(
            "Containment is the final physical barrier in the defense-in-depth strategy. "
            "Structures are designed to withstand internal pressures from design-basis accidents, including LOCA and steam line breaks. "
            "Materials include reinforced concrete and steel liners for leak-tightness. "
            "Penetrations are minimized and equipped with isolation valves. "
            "Periodic leak rate testing ensures containment integrity throughout plant life."
        ),
        key_factors=[
            "Structural design",
            "Material selection",
            "Leak rate testing",
            "Penetration isolation",
            "Pressure and temperature limits"
        ],
        primary_authority=["NRC", "ASME", "IAEA"],
        burden_holder="Plant designer/operator",
        adversary_position="Containment structures are expensive and may not prevent all releases.",
        counter_arguments=[
            "Containment has proven effective in major accidents.",
            "Design improvements enhance performance.",
            "Cost is justified by public safety benefits."
        ],
        resolution_strategy="Adopt robust containment designs and maintain rigorous inspection/testing programs.",
        entity_scope="All nuclear power plants",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix J; ASME Section III, Division 2"
    ),
    DoctrineBlock(
        topic="alara_dose_limits",
        keywords=["ALARA", "dose limits", "radiation protection", "optimization", "regulation", "occupational exposure"],
        conclusion_template="Radiation exposures must be kept As Low As Reasonably Achievable (ALARA), consistent with regulatory dose limits and operational needs.",
        reasoning_framework=(
            "The ALARA principle requires that all exposures be minimized, taking into account economic and social factors. "
            "Regulatory dose limits are established for occupational workers and the public. "
            "Optimization involves engineering controls, administrative procedures, and personal protective equipment. "
            "Continuous review and improvement of radiation protection programs are mandated. "
            "ALARA is a cornerstone of nuclear safety culture and regulatory compliance."
        ),
        key_factors=[
            "Regulatory dose limits",
            "Engineering controls",
            "Administrative procedures",
            "Personal protective equipment",
            "Program review"
        ],
        primary_authority=["NRC", "ICRP", "IAEA"],
        burden_holder="Licensee/radiation protection officer",
        adversary_position="ALARA is subjective and can be used to justify excessive costs.",
        counter_arguments=[
            "Cost-benefit analysis is integral to ALARA decisions.",
            "Regulatory oversight ensures reasonable application.",
            "Continuous improvement balances safety and practicality."
        ],
        resolution_strategy="Implement risk-informed, graded approach to ALARA optimization.",
        entity_scope="All nuclear facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 20; ICRP Publication 103"
    ),
    DoctrineBlock(
        topic="spent_fuel_pool_storage",
        keywords=["spent fuel", "pool storage", "decay heat", "criticality control", "radiation shielding", "storage racks"],
        conclusion_template="Spent fuel pools provide underwater storage for irradiated fuel assemblies, ensuring decay heat removal, criticality safety, and radiation shielding.",
        reasoning_framework=(
            "After removal from the reactor, spent fuel generates significant decay heat and requires cooling. "
            "Pools are designed with sufficient water depth to provide radiation shielding and accommodate thermal loads. "
            "Storage racks incorporate neutron absorbers to maintain subcriticality. "
            "Water chemistry is controlled to prevent corrosion and maintain clarity. "
            "Redundant cooling and level monitoring systems ensure pool safety."
        ),
        key_factors=[
            "Pool cooling capacity",
            "Water chemistry",
            "Criticality control",
            "Structural integrity",
            "Redundancy of safety systems"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Plant operator",
        adversary_position="Spent fuel pools are vulnerable to loss-of-cooling accidents and seismic events.",
        counter_arguments=[
            "Redundant cooling and backup power mitigate accident risks.",
            "Seismic qualification and robust design enhance safety.",
            "Transition to dry storage reduces long-term risk."
        ],
        resolution_strategy="Maintain robust pool safety systems and plan for timely transfer to dry storage.",
        entity_scope="All nuclear power plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC NUREG-1738; IAEA SSG-15"
    ),
    DoctrineBlock(
        topic="dry_cask_storage_isfsi",
        keywords=["dry cask storage", "ISFSI", "spent fuel", "passive cooling", "concrete cask", "transportability"],
        conclusion_template="Dry cask storage at Independent Spent Fuel Storage Installations (ISFSIs) provides safe, passive, and secure long-term storage for spent nuclear fuel.",
        reasoning_framework=(
            "After sufficient cooling in pools, spent fuel is transferred to dry casks for long-term storage. "
            "Casks use thick steel and concrete for radiation shielding and are designed for passive heat removal. "
            "ISFSIs are licensed facilities with robust security and monitoring. "
            "Dry storage reduces reliance on active cooling systems and is seismically qualified. "
            "Casks are designed for eventual transport to permanent disposal or reprocessing sites."
        ),
        key_factors=[
            "Cask design and integrity",
            "Passive cooling",
            "Security and monitoring",
            "Transportability",
            "Regulatory compliance"
        ],
        primary_authority=["NRC", "DOE", "IAEA"],
        burden_holder="ISFSI licensee",
        adversary_position="Dry cask storage is a temporary solution and does not address permanent disposal.",
        counter_arguments=[
            "Dry storage provides safe interim management for decades.",
            "Casks are designed for retrievability and transport.",
            "Permanent disposal solutions are under development."
        ],
        resolution_strategy="Continue research on permanent disposal and maintain robust ISFSI safety programs.",
        entity_scope="All ISFSIs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 72; IAEA SSG-15"
    ),
    DoctrineBlock(
        topic="nuclear_waste_classification_hlw_llw",
        keywords=["nuclear waste", "classification", "high-level waste", "low-level waste", "HLW", "LLW", "regulation"],
        conclusion_template="Nuclear waste is classified by origin, radioactivity, and longevity, guiding its management and disposal requirements.",
        reasoning_framework=(
            "High-level waste (HLW) primarily consists of spent fuel and reprocessing residues, requiring deep geological disposal. "
            "Low-level waste (LLW) includes contaminated materials from plant operation and maintenance, disposed of in near-surface facilities. "
            "Classification determines packaging, transport, and disposal methods. "
            "Regulatory frameworks specify waste forms, activity limits, and site licensing. "
            "Proper classification ensures long-term protection of human health and the environment."
        ),
        key_factors=[
            "Waste origin",
            "Radioactivity level",
            "Decay characteristics",
            "Disposal facility type",
            "Regulatory limits"
        ],
        primary_authority=["NRC", "DOE", "IAEA"],
        burden_holder="Waste generator",
        adversary_position="Classification is arbitrary and leads to inconsistent disposal practices.",
        counter_arguments=[
            "International standards harmonize classification schemes.",
            "Site-specific safety assessments guide disposal decisions.",
            "Continuous review improves classification systems."
        ],
        resolution_strategy="Align national regulations with international best practices and update as needed.",
        entity_scope="All nuclear waste generators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 61; IAEA GSG-1"
    ),
    DoctrineBlock(
        topic="nrc_10cfr50_licensing",
        keywords=["NRC", "10 CFR 50", "licensing", "construction permit", "operating license", "regulation"],
        conclusion_template="NRC 10 CFR 50 establishes the regulatory framework for licensing the construction and operation of nuclear power plants in the United States.",
        reasoning_framework=(
            "Applicants must submit detailed safety analyses, design information, and environmental reports. "
            "The licensing process includes public hearings, technical reviews, and inspections. "
            "Compliance with general design criteria and technical specifications is mandatory. "
            "Amendments and renewals are subject to ongoing regulatory oversight. "
            "The framework ensures that only qualified entities operate nuclear plants, maintaining public health and safety."
        ),
        key_factors=[
            "Safety analysis",
            "Design criteria",
            "Environmental impact",
            "Public participation",
            "Regulatory compliance"
        ],
        primary_authority=["NRC"],
        burden_holder="License applicant",
        adversary_position="The licensing process is overly burdensome and delays innovation.",
        counter_arguments=[
            "Rigorous review ensures safety and public trust.",
            "Processes are evolving to support advanced reactors.",
            "Stakeholder engagement is essential for transparency."
        ],
        resolution_strategy="Streamline licensing for new technologies while maintaining safety standards.",
        entity_scope="U.S. nuclear power plants",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50; NRC NUREG-0800"
    ),
    DoctrineBlock(
        topic="small_modular_reactors_smr",
        keywords=["SMR", "small modular reactor", "factory fabrication", "modularity", "deployment", "advanced reactor"],
        conclusion_template="Small Modular Reactors (SMRs) offer enhanced safety, scalability, and deployment flexibility through modular design and factory fabrication.",
        reasoning_framework=(
            "SMRs are designed for factory construction and site assembly, reducing construction time and cost. "
            "Their smaller size allows for enhanced passive safety features and siting flexibility. "
            "Modularity enables phased capacity additions and easier integration with renewable energy sources. "
            "Regulatory frameworks are adapting to accommodate SMR licensing and deployment. "
            "SMRs are positioned to expand nuclear energy access in remote or smaller markets."
        ),
        key_factors=[
            "Factory fabrication",
            "Passive safety",
            "Modular deployment",
            "Licensing adaptability",
            "Market suitability"
        ],
        primary_authority=["NRC", "DOE", "IAEA"],
        burden_holder="SMR developer",
        adversary_position="SMRs lack operational experience and may not achieve projected cost savings.",
        counter_arguments=[
            "Demonstration projects are underway globally.",
            "Design innovations address cost and safety concerns.",
            "International collaboration accelerates learning."
        ],
        resolution_strategy="Support pilot deployments and regulatory innovation for SMRs.",
        entity_scope="All SMR projects",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="NRC 10 CFR 52; IAEA NP-T-2.9"
    ),
    DoctrineBlock(
        topic="fusion_energy_tokamak_basics",
        keywords=["fusion", "tokamak", "plasma", "magnetic confinement", "ITER", "deuterium-tritium"],
        conclusion_template="Tokamak reactors use strong magnetic fields to confine high-temperature plasma, enabling controlled thermonuclear fusion.",
        reasoning_framework=(
            "Tokamaks employ toroidal and poloidal magnetic fields to confine plasma at temperatures exceeding 100 million degrees Celsius. "
            "Deuterium-tritium fuel is heated to initiate fusion reactions, releasing energy primarily as neutrons. "
            "Plasma stability and confinement time are critical for net energy gain. "
            "ITER is the leading international tokamak project, aiming to demonstrate sustained fusion power. "
            "Material challenges, tritium breeding, and power extraction remain key research areas."
        ),
        key_factors=[
            "Magnetic field strength",
            "Plasma stability",
            "Fuel purity",
            "First wall materials",
            "Tritium handling"
        ],
        primary_authority=["ITER Organization", "IAEA", "DOE"],
        burden_holder="Fusion researcher/operator",
        adversary_position="Tokamaks are too complex and costly for commercial energy production.",
        counter_arguments=[
            "Technological advances are reducing costs.",
            "Alternative fusion concepts are being explored.",
            "International collaboration accelerates progress."
        ],
        resolution_strategy="Continue research and development with international support and technology transfer.",
        entity_scope="Fusion research facilities",
        confidence=0.90,
        confidence_zone="Medium",
        controlling_precedent="ITER Project Agreement; IAEA TECDOC-1234"
    ),
    # Additional doctrine blocks for comprehensive coverage
    DoctrineBlock(
        topic="reactor_coolant_chemistry_control",
        keywords=["coolant chemistry", "corrosion", "water chemistry", "hydrazine", "lithium", "boron", "pH control"],
        conclusion_template="Strict control of reactor coolant chemistry minimizes corrosion, maintains fuel integrity, and ensures safe plant operation.",
        reasoning_framework=(
            "Coolant chemistry programs manage parameters such as pH, dissolved oxygen, and impurity concentrations. "
            "Additives like lithium and boron are used for pH and reactivity control, respectively. "
            "Hydrazine is employed to scavenge oxygen and prevent corrosion. "
            "Regular sampling and analysis detect deviations early. "
            "Chemistry excursions are managed through corrective actions to prevent fuel and component degradation."
        ),
        key_factors=[
            "pH control",
            "Oxygen removal",
            "Impurity monitoring",
            "Additive management",
            "Corrosion product control"
        ],
        primary_authority=["EPRI", "NRC"],
        burden_holder="Chemistry manager/operator",
        adversary_position="Chemistry control is costly and may not prevent all corrosion issues.",
        counter_arguments=[
            "Cost of chemistry control is offset by reduced component failures.",
            "Continuous improvement in monitoring technology enhances effectiveness.",
            "Regulatory requirements mandate chemistry programs."
        ],
        resolution_strategy="Adopt best practices and invest in advanced monitoring systems.",
        entity_scope="All water-cooled reactors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPRI PWR Water Chemistry Guidelines; NRC Regulatory Guide 1.56"
    ),
    DoctrineBlock(
        topic="reactor_shutdown_margin",
        keywords=["shutdown margin", "reactivity", "control rods", "safety", "subcriticality"],
        conclusion_template="Adequate shutdown margin ensures the reactor remains safely subcritical under all design-basis conditions.",
        reasoning_framework=(
            "Shutdown margin is the amount of negative reactivity available with all control rods inserted except the most reactive one. "
            "It guarantees that the core can be made and kept subcritical during normal and accident conditions. "
            "Shutdown margin calculations account for fuel burnup, temperature, and xenon effects. "
            "Regulatory requirements specify minimum shutdown margin values for each reactor type. "
            "Testing and surveillance confirm control rod performance and shutdown capability."
        ),
        key_factors=[
            "Control rod worth",
            "Core reactivity",
            "Fuel burnup",
            "Xenon poisoning",
            "Temperature feedback"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Reactor operator",
        adversary_position="Shutdown margin calculations are overly conservative and reduce operational flexibility.",
        counter_arguments=[
            "Conservatism ensures safety in all scenarios.",
            "Operational experience supports current requirements.",
            "Shutdown margin is periodically reviewed and updated."
        ],
        resolution_strategy="Maintain conservative shutdown margin and update as new data becomes available.",
        entity_scope="All nuclear reactors",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.77; IAEA Safety Series No. 50-SG-D3"
    ),
    DoctrineBlock(
        topic="reactor_trip_systems",
        keywords=["reactor trip", "scram", "protection system", "automatic shutdown", "safety"],
        conclusion_template="Reactor trip systems provide rapid, automatic shutdown of the reactor in response to abnormal or unsafe conditions.",
        reasoning_framework=(
            "Trip systems monitor key parameters such as power, temperature, and pressure. "
            "Upon detection of unsafe conditions, control rods are rapidly inserted (scram) to terminate the chain reaction. "
            "Redundant and diverse instrumentation ensures reliability. "
            "Periodic testing and maintenance verify system readiness. "
            "Trip setpoints are established based on safety analyses and regulatory requirements."
        ),
        key_factors=[
            "Instrumentation reliability",
            "Trip setpoints",
            "Redundancy",
            "Diversity",
            "Testing frequency"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Plant operator",
        adversary_position="Frequent trips reduce plant availability and can stress equipment.",
        counter_arguments=[
            "Safety takes precedence over availability.",
            "Trip frequency is monitored and analyzed for root causes.",
            "Design improvements reduce unnecessary trips."
        ],
        resolution_strategy="Balance safety and reliability through root cause analysis and system upgrades.",
        entity_scope="All nuclear reactors",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix A; IAEA Safety Guide NS-G-1.11"
    ),
    DoctrineBlock(
        topic="containment_leak_rate_testing",
        keywords=["containment", "leak rate", "integrity", "pressure testing", "regulatory compliance"],
        conclusion_template="Periodic containment leak rate testing verifies the integrity of the containment boundary and compliance with regulatory limits.",
        reasoning_framework=(
            "Leak rate tests (Type A, B, and C) are conducted to measure the containment's ability to maintain its pressure boundary. "
            "Type A tests assess overall leak tightness, while Type B and C focus on penetrations and isolation valves. "
            "Test results are compared to allowable leakage rates specified in plant technical specifications. "
            "Failures prompt corrective actions and retesting. "
            "Testing frequency and methods are established by regulation and industry standards."
        ),
        key_factors=[
            "Test method",
            "Allowable leakage rate",
            "Penetration integrity",
            "Isolation valve performance",
            "Testing frequency"
        ],
        primary_authority=["NRC", "ASME"],
        burden_holder="Plant operator",
        adversary_position="Leak rate testing is disruptive and may not detect all defects.",
        counter_arguments=[
            "Testing is essential for early detection of degradation.",
            "Non-destructive methods minimize disruption.",
            "Continuous improvement in test technology enhances detection."
        ],
        resolution_strategy="Optimize testing intervals and adopt advanced diagnostic techniques.",
        entity_scope="All nuclear power plants",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix J; ASME N511"
    ),
    DoctrineBlock(
        topic="seismic_design_basis",
        keywords=["seismic", "design basis", "earthquake", "structural qualification", "safety-related systems"],
        conclusion_template="Nuclear facilities must be designed to withstand site-specific seismic events without loss of safety function.",
        reasoning_framework=(
            "Seismic design basis is established through site characterization and probabilistic seismic hazard analysis. "
            "Structures, systems, and components important to safety are qualified to withstand the Safe Shutdown Earthquake (SSE). "
            "Designs incorporate seismic isolation, reinforcement, and anchoring. "
            "Periodic seismic walkdowns verify continued compliance. "
            "Regulatory requirements specify analysis methods and acceptance criteria."
        ),
        key_factors=[
            "Site seismic hazard",
            "SSE definition",
            "Structural qualification",
            "Component anchoring",
            "Periodic walkdowns"
        ],
        primary_authority=["NRC", "IAEA", "ASCE"],
        burden_holder="Plant designer",
        adversary_position="Seismic requirements increase construction cost and complexity.",
        counter_arguments=[
            "Safety of the public justifies additional cost.",
            "Design innovations reduce cost impact.",
            "Seismic events are low-probability, high-consequence risks."
        ],
        resolution_strategy="Apply risk-informed, performance-based seismic design.",
        entity_scope="All nuclear facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.60; IAEA NS-G-1.6"
    ),
    DoctrineBlock(
        topic="fire_protection_programs",
        keywords=["fire protection", "program", "defense-in-depth", "detection", "suppression", "safe shutdown"],
        conclusion_template="Comprehensive fire protection programs are required to prevent, detect, and suppress fires, ensuring safe reactor shutdown.",
        reasoning_framework=(
            "Fire protection employs defense-in-depth: prevention, detection, suppression, and safe shutdown capability. "
            "Fire barriers, detection systems, and automatic suppression are installed in critical areas. "
            "Administrative controls and training support physical measures. "
            "Periodic drills and inspections maintain program effectiveness. "
            "Regulations require fire protection as a condition of plant licensing."
        ),
        key_factors=[
            "Fire barriers",
            "Detection systems",
            "Suppression systems",
            "Administrative controls",
            "Training and drills"
        ],
        primary_authority=["NRC", "NFPA", "IAEA"],
        burden_holder="Plant operator",
        adversary_position="Fire protection measures are costly and may not prevent all fires.",
        counter_arguments=[
            "Fire is a credible risk to nuclear safety.",
            "Integrated programs minimize risk.",
            "Cost is justified by risk reduction."
        ],
        resolution_strategy="Continuously improve fire protection based on operating experience.",
        entity_scope="All nuclear facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix R; NFPA 805"
    ),
    DoctrineBlock(
        topic="environmental_qualification_eq",
        keywords=["environmental qualification", "EQ", "equipment", "harsh environment", "accident conditions"],
        conclusion_template="Safety-related equipment must be environmentally qualified to perform its function under accident conditions.",
        reasoning_framework=(
            "EQ ensures that equipment exposed to harsh environments (temperature, humidity, radiation) will operate reliably during and after design-basis accidents. "
            "Qualification is achieved through testing, analysis, and aging simulations. "
            "Documentation and traceability are required for all EQ components. "
            "Periodic reviews and replacement programs maintain EQ status. "
            "Regulatory requirements specify EQ scope and methods."
        ),
        key_factors=[
            "Environmental conditions",
            "Qualification testing",
            "Aging management",
            "Documentation",
            "Replacement intervals"
        ],
        primary_authority=["NRC", "IEEE", "IAEA"],
        burden_holder="Plant operator",
        adversary_position="EQ adds cost and complexity to equipment procurement.",
        counter_arguments=[
            "EQ is essential for accident mitigation.",
            "Standardization reduces cost and complexity.",
            "Regulatory oversight ensures compliance."
        ],
        resolution_strategy="Standardize EQ processes and maintain robust documentation.",
        entity_scope="All safety-related equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50.49; IEEE Std 323"
    ),
    DoctrineBlock(
        topic="quality_assurance_nuclear",
        keywords=["quality assurance", "QA", "nuclear", "program", "regulation", "safety"],
        conclusion_template="Comprehensive quality assurance programs are mandatory to ensure the safety and reliability of nuclear facilities.",
        reasoning_framework=(
            "QA programs cover design, procurement, construction, operation, and decommissioning. "
            "Documented procedures, audits, and corrective actions ensure compliance with regulatory and industry standards. "
            "Personnel training and qualification are integral to QA. "
            "Continuous improvement and lessons learned are incorporated into QA processes. "
            "Regulatory agencies require QA as a licensing condition."
        ),
        key_factors=[
            "Documented procedures",
            "Audits and inspections",
            "Corrective actions",
            "Personnel qualification",
            "Continuous improvement"
        ],
        primary_authority=["NRC", "IAEA", "ANSI"],
        burden_holder="Licensee/QA manager",
        adversary_position="QA programs are bureaucratic and hinder innovation.",
        counter_arguments=[
            "QA ensures safety and reliability.",
            "Programs are periodically reviewed for efficiency.",
            "Innovation is supported within QA frameworks."
        ],
        resolution_strategy="Streamline QA processes and integrate risk-informed approaches.",
        entity_scope="All nuclear facilities",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix B; IAEA GS-G-3.1"
    ),
    DoctrineBlock(
        topic="nuclear_security_design_basis_threat",
        keywords=["nuclear security", "design basis threat", "DBT", "physical protection", "regulation"],
        conclusion_template="Nuclear facilities must be protected against the Design Basis Threat (DBT) through robust physical and cyber security programs.",
        reasoning_framework=(
            "DBT defines the characteristics of potential adversaries that facilities must be protected against. "
            "Physical protection systems include barriers, detection, delay, and response measures. "
            "Cyber security is integrated to protect digital assets. "
            "Security programs are regularly tested through force-on-force exercises. "
            "Regulatory agencies periodically update DBT based on threat assessments."
        ),
        key_factors=[
            "Threat assessment",
            "Physical barriers",
            "Detection systems",
            "Response force",
            "Cyber security"
        ],
        primary_authority=["NRC", "IAEA", "DHS"],
        burden_holder="Facility security officer",
        adversary_position="DBT is classified and may not reflect real-world threats.",
        counter_arguments=[
            "DBT is regularly reviewed and updated.",
            "Security programs are tested and improved.",
            "International cooperation enhances threat assessment."
        ],
        resolution_strategy="Maintain adaptive security programs and incorporate intelligence updates.",
        entity_scope="All nuclear facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 73; IAEA NSS No. 13"
    ),
    DoctrineBlock(
        topic="nuclear_material_accounting_control",
        keywords=["material control", "accounting", "nuclear material", "safeguards", "diversion prevention"],
        conclusion_template="Strict material control and accounting (MC&A) programs prevent diversion and ensure the peaceful use of nuclear materials.",
        reasoning_framework=(
            "MC&A systems track nuclear material from receipt to disposal. "
            "Inventory records, measurements, and audits detect discrepancies. "
            "International safeguards (e.g., IAEA) verify compliance with nonproliferation commitments. "
            "Physical protection and administrative controls complement MC&A. "
            "Regulatory agencies require periodic reporting and inspections."
        ),
        key_factors=[
            "Inventory tracking",
            "Measurement accuracy",
            "Audit frequency",
            "Safeguards compliance",
            "Physical protection"
        ],
        primary_authority=["NRC", "IAEA", "DOE"],
        burden_holder="Material custodian",
        adversary_position="MC&A is resource-intensive and may not detect sophisticated diversion.",
        counter_arguments=[
            "Layered safeguards increase detection probability.",
            "Technology improvements enhance MC&A effectiveness.",
            "International cooperation strengthens oversight."
        ],
        resolution_strategy="Invest in advanced measurement and data analytics for MC&A.",
        entity_scope="All nuclear material holders",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 74; IAEA INFCIRC/153"
    ),
    DoctrineBlock(
        topic="reactor_operator_licensing_training",
        keywords=["operator licensing", "training", "reactor operator", "certification", "simulator"],
        conclusion_template="Reactor operators must complete rigorous training and licensing programs, including simulator exercises and periodic requalification.",
        reasoning_framework=(
            "Operator training includes classroom instruction, on-the-job experience, and simulator scenarios. "
            "Licensing exams test knowledge of plant systems, procedures, and emergency response. "
            "Requalification is required at regular intervals to maintain proficiency. "
            "Training programs are accredited and subject to regulatory audit. "
            "Continuous improvement incorporates operating experience and lessons learned."
        ),
        key_factors=[
            "Training curriculum",
            "Simulator exercises",
            "Licensing exams",
            "Requalification frequency",
            "Accreditation"
        ],
        primary_authority=["NRC", "INPO", "IAEA"],
        burden_holder="License applicant",
        adversary_position="Training requirements are excessive and limit workforce availability.",
        counter_arguments=[
            "Rigorous training ensures safety and reliability.",
            "Training programs are periodically reviewed for efficiency.",
            "Alternative pathways are being developed for workforce expansion."
        ],
        resolution_strategy="Modernize training methods and support workforce development.",
        entity_scope="All reactor operators",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 55; INPO ACAD 16-001"
    ),
    DoctrineBlock(
        topic="probabilistic_risk_assessment_pra",
        keywords=["PRA", "probabilistic risk assessment", "risk-informed", "safety analysis", "decision making"],
        conclusion_template="Probabilistic Risk Assessment (PRA) is used to quantify and manage nuclear plant risks, supporting risk-informed decision making.",
        reasoning_framework=(
            "PRA evaluates the likelihood and consequences of accident scenarios, identifying dominant risk contributors. "
            "Results inform safety improvements, regulatory decisions, and resource allocation. "
            "PRA complements deterministic safety analysis, providing a more complete risk picture. "
            "Quality and scope of PRA are defined by regulatory guidance. "
            "Continuous update and validation are required as plant configuration and operating experience evolve."
        ),
        key_factors=[
            "Accident scenario identification",
            "Frequency estimation",
            "Consequence analysis",
            "Data quality",
            "Model validation"
        ],
        primary_authority=["NRC", "IAEA", "ASME"],
        burden_holder="Licensee/risk manager",
        adversary_position="PRA is subject to modeling uncertainties and may underestimate risk.",
        counter_arguments=[
            "Uncertainty is addressed through sensitivity analysis.",
            "PRA is used alongside deterministic analysis.",
            "Regulatory review ensures PRA quality."
        ],
        resolution_strategy="Integrate PRA with deterministic analysis for balanced decision making.",
        entity_scope="All nuclear power plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.174; ASME/ANS RA-S"
    ),
    DoctrineBlock(
        topic="plant_modifications_configuration_control",
        keywords=["plant modification", "configuration control", "design change", "safety review", "documentation"],
        conclusion_template="Configuration control ensures that plant modifications are properly reviewed, documented, and implemented without compromising safety.",
        reasoning_framework=(
            "All design changes are subject to safety review, impact assessment, and regulatory notification if required. "
            "Configuration management systems track modifications and maintain up-to-date documentation. "
            "Change control prevents unauthorized alterations and ensures traceability. "
            "Periodic audits verify compliance with configuration control procedures. "
            "Regulatory requirements specify processes for safety-related modifications."
        ),
        key_factors=[
            "Change review process",
            "Documentation accuracy",
            "Impact assessment",
            "Audit frequency",
            "Regulatory notification"
        ],
        primary_authority=["NRC", "IAEA"],
        burden_holder="Plant engineering manager",
        adversary_position="Configuration control slows down innovation and plant upgrades.",
        counter_arguments=[
            "Safety is paramount in nuclear operations.",
            "Efficient processes balance safety and innovation.",
            "Digital tools streamline configuration management."
        ],
        resolution_strategy="Adopt digital configuration management and continuous process improvement.",
        entity_scope="All nuclear facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50.59; IAEA NS-G-2.3"
    ),
    DoctrineBlock(
        topic="reactor_pressure_boundary_integrity",
        keywords=["pressure boundary", "integrity", "leakage", "inspection", "ASME code"],
        conclusion_template="Reactor pressure boundaries must be maintained leak-tight and structurally sound through periodic inspection and testing.",
        reasoning_framework=(
            "Pressure boundary components are designed and fabricated to ASME Boiler and Pressure Vessel Code standards. "
            "In-service inspection programs detect degradation, cracking, or leakage. "
            "Non-destructive examination methods (ultrasonic, radiographic) are employed. "
            "Repair and replacement are performed under strict quality assurance. "
            "Regulatory requirements specify inspection intervals and acceptance criteria."
        ),
        key_factors=[
            "ASME code compliance",
            "Inspection method",
            "Repair procedures",
            "Quality assurance",
            "Testing frequency"
        ],
        primary_authority=["NRC", "ASME"],
        burden_holder="Plant operator",
        adversary_position="Inspection programs are costly and may not detect all flaws.",
        counter_arguments=[
            "Early detection prevents catastrophic failure.",
            "Continuous improvement in inspection technology increases effectiveness.",
            "Cost is justified by safety benefits."
        ],
        resolution_strategy="Adopt risk-informed inspection and advanced NDE techniques.",
        entity_scope="All nuclear power plants",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50.55a; ASME Section XI"
    ),
    DoctrineBlock(
        topic="reactor_core_design_optimization",
        keywords=["core design", "optimization", "fuel loading", "power distribution", "reactivity management"],
        conclusion_template="Core design optimization balances fuel utilization, power distribution, and safety margins for efficient and safe reactor operation.",
        reasoning_framework=(
            "Core loading patterns are developed to maximize fuel burnup and minimize power peaking. "
            "Reactivity management ensures shutdown margin and control rod effectiveness. "
            "Thermal-hydraulic analysis verifies that temperature and flow limits are not exceeded. "
            "Safety analyses confirm that design meets regulatory requirements. "
            "Periodic core redesign incorporates operational experience and new technology."
        ),
        key_factors=[
            "Fuel assembly arrangement",
            "Power peaking factors",
            "Reactivity control",
            "Thermal-hydraulic limits",
            "Safety analysis"
        ],
        primary_authority=["NRC", "EPRI", "IAEA"],
        burden_holder="Core designer",
        adversary_position="Optimization increases complexity and risk of design errors.",
        counter_arguments=[
            "Computer modeling reduces error probability.",
            "Designs are independently reviewed and verified.",
            "Operational feedback informs continuous improvement."
        ],
        resolution_strategy="Maintain robust design review and validation processes.",
        entity_scope="All nuclear reactors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.70; IAEA TECDOC-1162"
    ),
    DoctrineBlock(
        topic="reactor_thermal_limits_protection",
        keywords=["thermal limits", "DNBR", "fuel temperature", "safety", "protection systems"],
        conclusion_template="Reactor protection systems enforce thermal limits to prevent fuel damage and maintain core integrity.",
        reasoning_framework=(
            "Thermal limits such as Departure from Nucleate Boiling Ratio (DNBR) and maximum fuel temperature are established by safety analysis. "
            "Instrumentation monitors key parameters and initiates protective actions if limits are approached. "
            "Operating procedures ensure that margins to thermal limits are maintained during all conditions. "
            "Periodic calibration and testing of protection systems verify performance. "
            "Regulatory requirements specify thermal limits and protection setpoints."
        ),
        key_factors=[
            "DNBR",
            "Fuel temperature",
            "Instrumentation accuracy",
            "Protection setpoints",
            "Operating procedures"
        ],
        primary_authority=["NRC", "EPRI"],
        burden_holder="Plant operator",
        adversary_position="Thermal limits are overly conservative and reduce plant efficiency.",
        counter_arguments=[
            "Conservatism ensures safety under all scenarios.",
            "Limits are periodically reviewed and updated.",
            "Efficiency improvements are pursued within safety margins."
        ],
        resolution_strategy="Balance safety and efficiency through periodic review of thermal limits.",
        entity_scope="All nuclear reactors",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.105; EPRI NP-5652"
    ),
    DoctrineBlock(
        topic="reactor_ventilation_and_filtration",
        keywords=["ventilation", "filtration", "HEPA", "containment", "radioactive release", "HVAC"],
        conclusion_template="Ventilation and filtration systems are essential for controlling airborne radioactive releases and maintaining safe working environments.",
        reasoning_framework=(
            "HVAC systems maintain pressure differentials to prevent the spread of contamination. "
            "HEPA and charcoal filters remove particulates and radioactive iodine. "
            "System redundancy and monitoring ensure continuous operation during accidents. "
            "Periodic testing and filter replacement maintain system effectiveness. "
            "Regulatory requirements specify design and performance criteria for ventilation and filtration."
        ),
        key_factors=[
            "Filter efficiency",
            "Pressure differentials",
            "System redundancy",
            "Testing and maintenance",
            "Release monitoring"
        ],
        primary_authority=["NRC", "ASME", "IAEA"],
        burden_holder="Facility operator",
        adversary_position="Filtration systems add cost and complexity to plant HVAC.",
        counter_arguments=[
            "Filtration is essential for worker and public safety.",
            "Design improvements reduce cost and maintenance.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Adopt advanced filtration technology and optimize maintenance intervals.",
        entity_scope="All nuclear facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC Regulatory Guide 1.52; ASME AG-1"
    ),
    DoctrineBlock(
        topic="nuclear_emergency_preparedness",
        keywords=["emergency preparedness", "EP", "drills", "response plan", "offsite response"],
        conclusion_template="Comprehensive emergency preparedness programs ensure effective response to nuclear incidents, protecting workers and the public.",
        reasoning_framework=(
            "EP programs include emergency planning zones, notification systems, and coordinated response with local, state, and federal agencies. "
            "Regular drills and exercises test readiness and identify improvement areas. "
            "Public education and communication plans support effective response. "
            "Regulatory requirements specify EP program content and performance objectives. "
            "Continuous improvement incorporates lessons learned from exercises and real events."
        ),
        key_factors=[
            "Emergency planning zones",
            "Notification systems",
            "Drills and exercises",
            "Agency coordination",
            "Public communication"
        ],
        primary_authority=["NRC", "FEMA", "IAEA"],
        burden_holder="Licensee/emergency manager",
        adversary_position="EP programs are resource-intensive and may not cover all scenarios.",
        counter_arguments=[
            "EP is essential for public safety.",
            "Programs are regularly reviewed and improved.",
            "International best practices inform program updates."
        ],
        resolution_strategy="Integrate EP with risk assessment and continuous improvement.",
        entity_scope="All nuclear facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NRC 10 CFR 50 Appendix E; IAEA GS-G-2.1"
    ),
    DoctrineBlock(
        topic="human_factors_engineering_nuclear",
        keywords=["human factors", "HFE", "ergonomics", "control room", "operator interface"],
        conclusion_template="Human Factors Engineering (HFE) optimizes the interface between operators and plant systems, reducing human error and enhancing safety.",
        reasoning_framework=(
            "HFE principles are applied to control room design, procedure development, and alarm management. "
            "Operator workload, situational awareness, and decision support are key considerations. "
            "Simulator-based validation and user feedback inform design improvements. "
            "Regulatory guidance specifies HFE program requirements for new and modified facilities. "
            "Continuous improvement incorporates lessons learned from operating experience."
        ),
        key_factors=[
            "Control room layout",
            "Alarm management",
            "Procedure usability",
            "Operator workload",
            "Simulator validation"
        ],
        primary_authority=["NRC", "IAEA", "EPRI"],
        burden_holder="Plant designer/operator",
        adversary_position="HFE adds cost and may not eliminate all human errors.",
        counter_arguments=[
            "HFE reduces error probability and improves response.",
            "Cost is offset by safety and efficiency gains.",
            "HFE programs are periodically reviewed for effectiveness."
        ],
        resolution_strategy="Integrate HFE into all phases of plant design and operation.",
        entity_scope="All nuclear facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NRC NUREG-0711; IAEA TECDOC-1140"
    ),
    DoctrineBlock(
        topic="nuclear_safety_culture",
        keywords=["safety culture", "nuclear", "leadership", "accountability", "continuous improvement"],
        conclusion_template="A strong nuclear safety culture is essential for safe, reliable plant operation and regulatory compliance.",
        reasoning_framework=(
            "Safety culture encompasses leadership commitment, individual accountability, and a questioning attitude. "
            "Open communication and reporting of safety concerns are encouraged. "
            "Continuous learning and improvement are core values. "
            "Regulatory agencies assess safety culture as part of oversight. "
            "Events and near-misses are analyzed for lessons learned."
        ),
        key_factors=[
            "Leadership commitment",
            "Accountability",
            "Open communication",
            "Learning environment",
            "Regulatory oversight"
        ],
        primary_authority=["NRC", "IAEA", "INPO"],
        burden_holder="All plant personnel",
        adversary_position="Safety culture is intangible and difficult to measure.",
        counter_arguments=[
            "Assessment tools and surveys provide insight.",
            "Strong safety culture correlates with better performance.",
            "Continuous improvement is achievable."
        ],
        resolution_strategy="Promote safety culture through leadership, training, and feedback.",
        entity_scope="All nuclear facilities",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NRC Policy Statement on Safety Culture; IAEA GS-G-3.5"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
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