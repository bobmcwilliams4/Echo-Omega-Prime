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
        topic="Post-Combustion CO2 Capture with Amine Scrubbing",
        keywords=[
            "post-combustion", "CO2 capture", "amine scrubbing", "chemical absorption", "flue gas", "retrofit", "solvent regeneration"
        ],
        conclusion_template="Post-combustion amine scrubbing is a mature and widely applicable technology for CO2 capture from flue gas streams, suitable for retrofitting existing fossil-fuel power plants.",
        reasoning_framework="""
        1. Assess the chemical compatibility of the flue gas with amine solvents, focusing on SOx/NOx levels and particulate matter.
        2. Evaluate the energy penalty associated with solvent regeneration and its impact on plant efficiency.
        3. Consider the scalability and retrofit potential for existing infrastructure.
        4. Analyze solvent degradation rates and emissions of amine degradation products.
        5. Review regulatory requirements for emissions and solvent management.
        6. Compare cost-effectiveness against alternative capture methods.
        7. Examine operational experience and track record in commercial settings.
        8. Weigh environmental and health impacts of solvent use and emissions.
        9. Determine integration feasibility with downstream CO2 compression and transport.
        10. Synthesize findings to conclude suitability and best practices for deployment.
        """,
        key_factors=[
            "Flue gas composition", "Solvent selection", "Energy penalty", "Retrofit feasibility", "Emissions control", "Operational experience"
        ],
        primary_authority=[
            "IEA Greenhouse Gas R&D Programme", "US Department of Energy (DOE)", "IPCC Special Report on Carbon Dioxide Capture and Storage"
        ],
        burden_holder="Project developer",
        adversary_position="Amine scrubbing is too costly and environmentally risky for large-scale deployment.",
        counter_arguments=[
            "Recent advances have reduced energy penalties and solvent losses.",
            "Commercial-scale plants have demonstrated reliability and performance.",
            "Regulatory frameworks exist to manage emissions and solvent handling."
        ],
        resolution_strategy="Conduct site-specific techno-economic and environmental assessments, referencing best available data and regulatory guidance.",
        entity_scope="Power utilities, industrial emitters",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Boundary Dam CCS Project (Canada), Petra Nova Project (USA)"
    ),
    DoctrineBlock(
        topic="Pre-Combustion Capture in IGCC with Shift Reactor",
        keywords=[
            "pre-combustion", "IGCC", "integrated gasification combined cycle", "shift reactor", "syngas", "hydrogen", "CO2 separation"
        ],
        conclusion_template="Pre-combustion CO2 capture in IGCC plants with shift reactors is technically feasible and offers high capture rates, but is best suited for new builds rather than retrofits.",
        reasoning_framework="""
        1. Evaluate the gasification process and syngas composition.
        2. Analyze the water-gas shift reaction efficiency and hydrogen yield.
        3. Assess the performance of physical or chemical CO2 separation units (e.g., Selexol, Rectisol).
        4. Consider integration with hydrogen production and utilization.
        5. Examine capital and operating costs relative to post-combustion options.
        6. Review operational complexity and reliability of IGCC systems.
        7. Assess regulatory drivers for hydrogen and CO2 markets.
        8. Evaluate environmental impacts and lifecycle emissions.
        9. Synthesize findings to determine project viability and risk profile.
        """,
        key_factors=[
            "Gasifier technology", "Shift reactor efficiency", "CO2 separation process", "Hydrogen market", "Capital cost", "Operational complexity"
        ],
        primary_authority=[
            "US DOE National Energy Technology Laboratory (NETL)", "IEA Clean Coal Centre"
        ],
        burden_holder="Plant developer",
        adversary_position="IGCC with pre-combustion capture is prohibitively expensive and operationally complex.",
        counter_arguments=[
            "High capture rates (>90%) are achievable with proven technology.",
            "Integration with hydrogen production can improve economics.",
            "New-build plants can be optimized for capture from the outset."
        ],
        resolution_strategy="Conduct comparative techno-economic analysis and risk assessment for new-build projects.",
        entity_scope="New IGCC power plants, hydrogen producers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Duke Energy Edwardsport IGCC Plant, Kemper County Energy Facility (pre-cancellation)"
    ),
    DoctrineBlock(
        topic="Direct Air Capture with Solid Sorbent Technology",
        keywords=[
            "direct air capture", "DAC", "solid sorbent", "low-concentration CO2", "modular", "temperature swing adsorption"
        ],
        conclusion_template="Solid sorbent DAC is a promising modular approach for atmospheric CO2 removal, but is currently limited by high energy requirements and cost.",
        reasoning_framework="""
        1. Assess the adsorption/desorption cycle efficiency for solid sorbents.
        2. Evaluate energy requirements for regeneration (typically low-grade heat).
        3. Analyze scalability and modular deployment potential.
        4. Review lifecycle emissions and net carbon removal.
        5. Examine cost trajectories and learning curve effects.
        6. Consider siting requirements and land use.
        7. Assess supply chain and material sustainability for sorbents.
        8. Review regulatory and voluntary carbon removal market frameworks.
        9. Synthesize findings to determine near-term and long-term viability.
        """,
        key_factors=[
            "Sorbent performance", "Energy source for regeneration", "Cost per ton CO2", "Scalability", "Lifecycle emissions"
        ],
        primary_authority=[
            "National Academies of Sciences, Engineering, and Medicine (NASEM)", "IEA Direct Air Capture Reports"
        ],
        burden_holder="DAC project proponent",
        adversary_position="Solid sorbent DAC is too expensive and energy-intensive for meaningful climate impact.",
        counter_arguments=[
            "Technology costs are projected to decline with scale.",
            "Modular design enables distributed deployment.",
            "Low-carbon energy sources can minimize lifecycle emissions."
        ],
        resolution_strategy="Support pilot and demonstration projects, monitor cost and performance data, and align with emerging carbon removal standards.",
        entity_scope="Carbon removal developers, policy makers",
        confidence=0.81,
        confidence_zone="Medium-High",
        controlling_precedent="Climeworks Orca Plant (Iceland)"
    ),
    DoctrineBlock(
        topic="Direct Air Capture with Liquid Solvent (Alkaline Solution)",
        keywords=[
            "direct air capture", "liquid solvent", "alkaline solution", "CO2 absorption", "regeneration", "carbon removal"
        ],
        conclusion_template="Liquid solvent DAC using alkaline solutions is technically viable for atmospheric CO2 removal, but faces challenges in solvent management and energy use.",
        reasoning_framework="""
        1. Analyze the CO2 absorption efficiency of the alkaline solution.
        2. Evaluate energy requirements for solvent regeneration and CO2 release.
        3. Assess solvent degradation rates and management of byproducts.
        4. Consider water consumption and environmental impacts.
        5. Examine scalability and land use constraints.
        6. Review cost estimates and learning curve potential.
        7. Assess regulatory and market frameworks for carbon removal.
        8. Synthesize findings to determine deployment potential and risks.
        """,
        key_factors=[
            "Absorption efficiency", "Solvent regeneration energy", "Water use", "Byproduct management", "Cost per ton CO2"
        ],
        primary_authority=[
            "Carbon Engineering Ltd.", "NASEM Negative Emissions Technologies Report"
        ],
        burden_holder="DAC project developer",
        adversary_position="Liquid solvent DAC is unsustainable due to high water and energy use.",
        counter_arguments=[
            "Process optimization can reduce water and energy demands.",
            "Large-scale pilots have demonstrated technical feasibility.",
            "Solvent recycling and byproduct management strategies are improving."
        ],
        resolution_strategy="Conduct site-specific environmental and techno-economic assessments, and monitor pilot project outcomes.",
        entity_scope="Carbon removal developers, investors",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="Carbon Engineering Squamish Pilot Plant (Canada)"
    ),
    DoctrineBlock(
        topic="CO2 Pipeline Transport in Dense Phase",
        keywords=[
            "CO2 pipeline", "dense phase", "supercritical", "transport", "compression", "pipeline integrity"
        ],
        conclusion_template="Dense phase (supercritical) CO2 pipeline transport is the industry standard for large-scale, long-distance movement of captured CO2, subject to rigorous safety and material requirements.",
        reasoning_framework="""
        1. Determine the required pressure and temperature for dense phase transport (typically >7.38 MPa, >31°C).
        2. Assess pipeline material compatibility with CO2 and impurities (e.g., water, H2S).
        3. Evaluate design codes and safety standards (e.g., ASME B31.4, DOT PHMSA).
        4. Review permitting and right-of-way acquisition processes.
        5. Analyze operational risks, including fracture propagation and corrosion.
        6. Consider monitoring and leak detection requirements.
        7. Examine integration with compression and injection infrastructure.
        8. Synthesize findings to ensure safe and cost-effective pipeline deployment.
        """,
        key_factors=[
            "Pressure and temperature control", "Material selection", "Safety standards", "Permitting", "Impurity management"
        ],
        primary_authority=[
            "US Department of Transportation (DOT) PHMSA", "ASME B31.4 Pipeline Code", "IEA CO2 Transport Report"
        ],
        burden_holder="Pipeline operator",
        adversary_position="CO2 pipelines pose unacceptable safety and environmental risks.",
        counter_arguments=[
            "CO2 pipelines have a strong safety record in the US and globally.",
            "Modern monitoring and emergency response protocols mitigate risks.",
            "Regulatory oversight ensures adherence to safety standards."
        ],
        resolution_strategy="Adhere to established codes, conduct risk assessments, and engage stakeholders throughout project development.",
        entity_scope="Pipeline operators, project developers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Denbury CO2 Pipeline Network (USA), Cortez Pipeline"
    ),
    DoctrineBlock(
        topic="Geological CO2 Storage in Deep Saline Aquifers",
        keywords=[
            "geological storage", "saline aquifer", "deep injection", "CO2 sequestration", "caprock integrity", "trapping mechanisms"
        ],
        conclusion_template="Deep saline aquifers provide the largest and most widely distributed storage capacity for CO2, with demonstrated long-term security when properly characterized and managed.",
        reasoning_framework="""
        1. Characterize the target aquifer's porosity, permeability, and depth.
        2. Assess caprock integrity and sealing capacity.
        3. Evaluate trapping mechanisms: structural, residual, solubility, and mineral.
        4. Review site-specific geomechanical and geochemical risks.
        5. Model plume migration and pressure buildup.
        6. Consider monitoring, verification, and accounting (MVA) requirements.
        7. Examine regulatory frameworks (e.g., EPA Class VI).
        8. Synthesize findings to determine site suitability and risk profile.
        """,
        key_factors=[
            "Aquifer properties", "Caprock integrity", "Trapping mechanisms", "Site characterization", "MVA plan"
        ],
        primary_authority=[
            "US EPA", "IEA Greenhouse Gas R&D Programme", "IPCC Special Report on CCS"
        ],
        burden_holder="Storage operator",
        adversary_position="Long-term CO2 leakage from saline aquifers is inevitable and poses environmental risks.",
        counter_arguments=[
            "Decades of field experience show minimal leakage risk with proper site selection.",
            "Multiple trapping mechanisms provide redundancy.",
            "Rigorous monitoring and regulatory oversight ensure safety."
        ],
        resolution_strategy="Follow best practices in site selection, characterization, and MVA, and comply with regulatory requirements.",
        entity_scope="Storage operators, regulators",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Sleipner CO2 Storage Project (Norway), Illinois Basin Decatur Project (USA)"
    ),
    DoctrineBlock(
        topic="CO2 Enhanced Oil Recovery (EOR) and Incidental Storage",
        keywords=[
            "CO2 EOR", "enhanced oil recovery", "incidental storage", "tertiary recovery", "oil field", "MMV"
        ],
        conclusion_template="CO2-EOR is a commercially proven method for increasing oil recovery while providing incidental CO2 storage, subject to robust monitoring and accounting.",
        reasoning_framework="""
        1. Assess the suitability of the oil reservoir for CO2 injection.
        2. Evaluate incremental oil recovery and CO2 storage potential.
        3. Review MMV (monitoring, measurement, and verification) protocols.
        4. Analyze regulatory requirements for CO2 accounting and reporting.
        5. Consider lifecycle emissions and net climate benefit.
        6. Examine economic incentives, including Section 45Q tax credits.
        7. Synthesize findings to determine project viability and climate impact.
        """,
        key_factors=[
            "Reservoir characteristics", "CO2 injection rates", "MMV protocols", "Regulatory compliance", "Economic incentives"
        ],
        primary_authority=[
            "US EPA", "US DOE", "IEA EOR Reports"
        ],
        burden_holder="EOR operator",
        adversary_position="CO2-EOR increases net emissions by enabling additional oil production.",
        counter_arguments=[
            "Incidental CO2 storage can be significant and verifiable.",
            "Lifecycle analysis can demonstrate net climate benefit.",
            "Regulatory frameworks require robust accounting."
        ],
        resolution_strategy="Implement rigorous MMV and lifecycle analysis, and comply with reporting requirements.",
        entity_scope="Oil producers, regulators",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Permian Basin CO2-EOR Operations (USA)"
    ),
    DoctrineBlock(
        topic="Section 45Q Tax Credit for Carbon Capture and Sequestration",
        keywords=[
            "Section 45Q", "tax credit", "carbon capture", "sequestration", "IRS", "incentives"
        ],
        conclusion_template="Section 45Q provides a federal tax credit for qualified carbon capture and sequestration activities, subject to strict eligibility and reporting requirements.",
        reasoning_framework="""
        1. Determine project eligibility based on capture volume and facility type.
        2. Assess requirements for secure geological storage or EOR.
        3. Review IRS guidance on credit calculation and transferability.
        4. Evaluate documentation and reporting obligations.
        5. Consider interaction with other federal and state incentives.
        6. Examine recapture provisions in case of CO2 leakage.
        7. Synthesize findings to ensure compliance and maximize credit value.
        """,
        key_factors=[
            "Capture volume", "Storage method", "IRS compliance", "Reporting", "Recapture risk"
        ],
        primary_authority=[
            "US Internal Revenue Service (IRS)", "US Department of Treasury", "US DOE"
        ],
        burden_holder="Project owner",
        adversary_position="Section 45Q is too restrictive and administratively burdensome for project developers.",
        counter_arguments=[
            "Recent IRS guidance has clarified eligibility and streamlined processes.",
            "Credit transferability increases project finance options.",
            "Robust documentation ensures long-term compliance."
        ],
        resolution_strategy="Engage tax and legal advisors early, maintain thorough documentation, and monitor regulatory updates.",
        entity_scope="Project developers, investors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2020-12, IRS Revenue Procedure 2020-12"
    ),
    DoctrineBlock(
        topic="Oxy-Combustion CO2 Capture Technology",
        keywords=[
            "oxy-combustion", "CO2 capture", "pure oxygen", "flue gas", "cryogenic air separation", "retrofit"
        ],
        conclusion_template="Oxy-combustion enables high-purity CO2 capture by combusting fuel in pure oxygen, but is limited by the cost and energy demand of oxygen production.",
        reasoning_framework="""
        1. Evaluate the technical feasibility of retrofitting or designing oxy-combustion systems.
        2. Assess the performance and cost of cryogenic air separation units.
        3. Analyze flue gas composition and CO2 purity.
        4. Consider integration with downstream CO2 compression and transport.
        5. Review operational complexity and safety considerations.
        6. Compare cost-effectiveness with alternative capture technologies.
        7. Synthesize findings to determine deployment potential and barriers.
        """,
        key_factors=[
            "Oxygen production cost", "CO2 purity", "Retrofit feasibility", "Operational complexity", "Safety"
        ],
        primary_authority=[
            "IEA Greenhouse Gas R&D Programme", "US DOE NETL"
        ],
        burden_holder="Plant owner",
        adversary_position="Oxy-combustion is economically uncompetitive due to oxygen production costs.",
        counter_arguments=[
            "Advances in air separation technology are reducing costs.",
            "High CO2 purity simplifies downstream processing.",
            "Oxy-combustion is suitable for new builds and some retrofits."
        ],
        resolution_strategy="Conduct comparative techno-economic analysis and pilot testing.",
        entity_scope="Power generators, technology providers",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="Callide Oxyfuel Project (Australia)"
    ),
    DoctrineBlock(
        topic="CO2 Compression for Pipeline Transport and Storage",
        keywords=[
            "CO2 compression", "pipeline transport", "storage", "multistage compressor", "dehydration", "energy use"
        ],
        conclusion_template="CO2 must be compressed to supercritical pressures for efficient pipeline transport and storage, requiring robust multistage compression and dehydration systems.",
        reasoning_framework="""
        1. Determine target pressure for pipeline entry (typically 8-15 MPa).
        2. Assess compressor selection and configuration (centrifugal, reciprocating, integrally geared).
        3. Evaluate energy consumption and integration with plant operations.
        4. Analyze dehydration requirements to prevent corrosion and hydrate formation.
        5. Review maintenance and reliability considerations.
        6. Examine safety and emergency shutdown protocols.
        7. Synthesize findings to optimize compression system design.
        """,
        key_factors=[
            "Target pressure", "Compressor type", "Energy use", "Dehydration", "Reliability"
        ],
        primary_authority=[
            "US DOE NETL", "API Recommended Practice 521"
        ],
        burden_holder="Plant operator",
        adversary_position="CO2 compression is a major cost and reliability bottleneck for CCS projects.",
        counter_arguments=[
            "Advances in compressor technology are improving efficiency.",
            "Integrated designs can reduce energy use.",
            "Proper dehydration and maintenance mitigate reliability risks."
        ],
        resolution_strategy="Optimize compressor selection and integration, and implement robust maintenance protocols.",
        entity_scope="CCS project operators, pipeline companies",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="Sleipner CO2 Compression System (Norway)"
    ),
    DoctrineBlock(
        topic="CCUS Lifecycle Carbon Accounting and Net Climate Benefit",
        keywords=[
            "CCUS", "lifecycle analysis", "carbon accounting", "net climate benefit", "GHG inventory", "ISO 14064"
        ],
        conclusion_template="Comprehensive lifecycle carbon accounting is essential to demonstrate the net climate benefit of CCUS projects, requiring adherence to recognized standards and transparent reporting.",
        reasoning_framework="""
        1. Define system boundaries for the CCUS project.
        2. Identify all relevant GHG emissions sources and sinks.
        3. Apply recognized standards (e.g., ISO 14064, GHG Protocol).
        4. Quantify direct and indirect emissions, including capture, transport, storage, and energy use.
        5. Account for leakage risks and monitoring results.
        6. Review third-party verification and reporting requirements.
        7. Synthesize findings to demonstrate net climate benefit and eligibility for incentives.
        """,
        key_factors=[
            "System boundaries", "Emissions quantification", "Standards compliance", "Leakage accounting", "Verification"
        ],
        primary_authority=[
            "ISO 14064", "GHG Protocol", "US EPA"
        ],
        burden_holder="Project developer",
        adversary_position="CCUS projects overstate climate benefits by ignoring indirect emissions and leakage.",
        counter_arguments=[
            "Lifecycle analysis standards require comprehensive accounting.",
            "Third-party verification ensures transparency.",
            "Monitoring and reporting frameworks address leakage risks."
        ],
        resolution_strategy="Adopt best-practice lifecycle analysis and engage independent verifiers.",
        entity_scope="Project developers, regulators, investors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 14064-2:2019, California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="EPA Class VI Injection Well Permitting Process",
        keywords=[
            "EPA", "Class VI", "injection well", "permitting", "CO2 storage", "UIC program"
        ],
        conclusion_template="Class VI wells are subject to stringent EPA permitting requirements to ensure the safe and permanent storage of CO2 in deep geologic formations.",
        reasoning_framework="""
        1. Review EPA Class VI well application requirements under the UIC program.
        2. Assess site characterization, including geology, hydrology, and risk assessment.
        3. Evaluate well construction, operation, and monitoring plans.
        4. Analyze public participation and stakeholder engagement processes.
        5. Review post-injection site care and closure requirements.
        6. Consider state primacy and coordination with federal agencies.
        7. Synthesize findings to ensure permit compliance and project approval.
        """,
        key_factors=[
            "Site characterization", "Well construction", "Monitoring plan", "Public engagement", "Closure requirements"
        ],
        primary_authority=[
            "US EPA", "Safe Drinking Water Act", "UIC Program Guidance"
        ],
        burden_holder="Storage operator",
        adversary_position="Class VI permitting is too slow and unpredictable for timely CCS deployment.",
        counter_arguments=[
            "EPA has streamlined permitting guidance and timelines.",
            "State primacy can expedite permitting in some jurisdictions.",
            "Robust permitting ensures long-term safety and public trust."
        ],
        resolution_strategy="Engage with regulators early, prepare comprehensive applications, and maintain transparent stakeholder communication.",
        entity_scope="Storage operators, regulators",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA Class VI Permitting Guidance, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="Monitoring, Verification, and Accounting (MVA) for CO2 Storage",
        keywords=[
            "monitoring", "verification", "accounting", "MVA", "CO2 storage", "plume tracking", "leak detection"
        ],
        conclusion_template="Robust MVA programs are essential for ensuring the integrity and permanence of CO2 storage, supporting regulatory compliance and public confidence.",
        reasoning_framework="""
        1. Define monitoring objectives and regulatory requirements.
        2. Select appropriate technologies for plume tracking and leak detection (e.g., seismic, pressure, geochemical).
        3. Develop baseline and ongoing data collection protocols.
        4. Establish verification and reporting procedures.
        5. Analyze data to detect anomalies and assess storage performance.
        6. Engage stakeholders and communicate results transparently.
        7. Synthesize findings to support regulatory compliance and credit eligibility.
        """,
        key_factors=[
            "Monitoring technology", "Baseline data", "Leak detection", "Reporting", "Stakeholder engagement"
        ],
        primary_authority=[
            "US EPA", "IEA Greenhouse Gas R&D Programme", "California Air Resources Board"
        ],
        burden_holder="Storage operator",
        adversary_position="MVA programs are costly and cannot guarantee leakage detection.",
        counter_arguments=[
            "Multiple, redundant monitoring methods increase reliability.",
            "Continuous improvement and technology advances enhance detection.",
            "Transparent reporting builds public trust."
        ],
        resolution_strategy="Implement multi-layered MVA plans and adapt to new technologies and regulatory requirements.",
        entity_scope="Storage operators, regulators, verifiers",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Sleipner MVA Program, California LCFS CCS Protocol"
    ),
    # -- Additional DoctrineBlocks for comprehensive coverage (examples below) --
    DoctrineBlock(
        topic="CO2 Capture from Cement Plants",
        keywords=[
            "cement", "industrial capture", "calcium looping", "amine scrubbing", "process integration"
        ],
        conclusion_template="CO2 capture from cement plants is technically feasible using amine scrubbing or calcium looping, but requires careful integration with plant operations.",
        reasoning_framework="""
        1. Assess the CO2 concentration and flow in cement plant flue gas.
        2. Evaluate the suitability of amine scrubbing versus calcium looping.
        3. Analyze integration with kiln and heat recovery systems.
        4. Review operational impacts and maintenance requirements.
        5. Consider cost and emissions reduction potential.
        6. Examine regulatory drivers and incentives.
        7. Synthesize findings for technology selection and deployment.
        """,
        key_factors=[
            "Flue gas composition", "Technology selection", "Integration", "Cost", "Regulatory drivers"
        ],
        primary_authority=[
            "Global CCS Institute", "IEA Technology Roadmap: Low-Carbon Transition in the Cement Industry"
        ],
        burden_holder="Cement plant operator",
        adversary_position="CCS is too costly and disruptive for cement production.",
        counter_arguments=[
            "Demonstration projects have shown technical feasibility.",
            "Integration can be optimized to minimize operational impact.",
            "Incentives and carbon pricing improve project economics."
        ],
        resolution_strategy="Conduct detailed feasibility studies and leverage demonstration project learnings.",
        entity_scope="Cement producers, technology providers",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="Norcem Brevik CCS Project (Norway)"
    ),
    DoctrineBlock(
        topic="CO2 Capture from Steel Plants",
        keywords=[
            "steel", "blast furnace", "basic oxygen furnace", "amine scrubbing", "top gas recycling"
        ],
        conclusion_template="CO2 capture from steel plants is achievable with amine scrubbing or top gas recycling, but economic and operational challenges remain.",
        reasoning_framework="""
        1. Assess CO2 concentration and flow in steel plant off-gases.
        2. Evaluate capture technology options and integration.
        3. Analyze impact on plant operations and product quality.
        4. Review cost and emissions reduction potential.
        5. Examine regulatory and market drivers.
        6. Synthesize findings for project development and risk management.
        """,
        key_factors=[
            "Off-gas composition", "Technology integration", "Cost", "Operational impact", "Regulatory drivers"
        ],
        primary_authority=[
            "Global CCS Institute", "IEA Iron and Steel Technology Roadmap"
        ],
        burden_holder="Steel plant operator",
        adversary_position="CCS is not viable for steel due to high cost and process complexity.",
        counter_arguments=[
            "Pilot projects have demonstrated technical feasibility.",
            "Integration strategies can minimize operational disruption.",
            "Policy support can improve project economics."
        ],
        resolution_strategy="Leverage pilot project experience and engage with policy makers for support.",
        entity_scope="Steel producers, technology providers",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="ArcelorMittal Steelanol Project (Belgium)"
    ),
    DoctrineBlock(
        topic="CO2 Capture from Natural Gas Processing",
        keywords=[
            "natural gas", "acid gas removal", "amine scrubbing", "membrane separation", "dehydration"
        ],
        conclusion_template="CO2 capture from natural gas processing is a mature and widely deployed technology, essential for pipeline specification and emissions reduction.",
        reasoning_framework="""
        1. Assess CO2 and H2S concentrations in raw natural gas.
        2. Evaluate amine scrubbing and membrane separation options.
        3. Analyze dehydration and downstream processing requirements.
        4. Review operational experience and reliability.
        5. Consider regulatory requirements for pipeline gas quality.
        6. Synthesize findings for technology selection and deployment.
        """,
        key_factors=[
            "Feed gas composition", "Technology selection", "Reliability", "Regulatory compliance", "Cost"
        ],
        primary_authority=[
            "US DOE", "API Standards", "IEA Natural Gas Information"
        ],
        burden_holder="Gas processor",
        adversary_position="CO2 capture adds unnecessary cost to gas processing.",
        counter_arguments=[
            "CO2 removal is required for pipeline specification.",
            "Mature technologies ensure reliability.",
            "Emissions reduction aligns with regulatory and market trends."
        ],
        resolution_strategy="Adopt best-available technologies and maintain compliance with gas quality standards.",
        entity_scope="Gas processors, pipeline operators",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Val Verde Gas Plant (USA)"
    ),
    DoctrineBlock(
        topic="CO2 Utilization in Building Materials",
        keywords=[
            "CO2 utilization", "concrete", "mineralization", "building materials", "carbon cure"
        ],
        conclusion_template="CO2 utilization in building materials, such as concrete mineralization, offers permanent storage and product enhancement, but market adoption is still emerging.",
        reasoning_framework="""
        1. Assess the technical feasibility of CO2 mineralization in concrete.
        2. Evaluate product performance and durability.
        3. Analyze lifecycle emissions and net storage.
        4. Review regulatory and certification pathways.
        5. Consider market acceptance and scalability.
        6. Synthesize findings for commercialization strategy.
        """,
        key_factors=[
            "Mineralization process", "Product performance", "Lifecycle emissions", "Certification", "Market acceptance"
        ],
        primary_authority=[
            "CarbonCure Technologies", "NASEM Negative Emissions Technologies Report"
        ],
        burden_holder="Material producer",
        adversary_position="CO2 mineralization is too costly and unproven for widespread use.",
        counter_arguments=[
            "Pilot projects demonstrate technical and commercial feasibility.",
            "Product performance can exceed conventional materials.",
            "Certification and standards are evolving to support adoption."
        ],
        resolution_strategy="Engage with certification bodies and conduct market trials.",
        entity_scope="Building material producers, construction firms",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="CarbonCure Commercial Deployments"
    ),
    DoctrineBlock(
        topic="CO2 Mineralization for Permanent Storage",
        keywords=[
            "CO2 mineralization", "permanent storage", "basalt", "ultramafic rock", "in situ carbonation"
        ],
        conclusion_template="In situ CO2 mineralization in reactive rock formations offers permanent storage with minimal leakage risk, but is limited by site availability and injection rates.",
        reasoning_framework="""
        1. Characterize target rock formations for reactivity and permeability.
        2. Assess injection and carbonation rates.
        3. Evaluate monitoring and verification protocols.
        4. Review environmental and seismic risks.
        5. Analyze scalability and cost.
        6. Synthesize findings for project development.
        """,
        key_factors=[
            "Rock reactivity", "Injection rate", "Monitoring", "Environmental risk", "Cost"
        ],
        primary_authority=[
            "CarbFix Project", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Mineralization is too slow and site-limited for large-scale deployment.",
        counter_arguments=[
            "Field projects have demonstrated rapid mineralization in suitable formations.",
            "Permanent storage eliminates long-term leakage risk.",
            "Site screening can identify optimal locations."
        ],
        resolution_strategy="Conduct site-specific feasibility studies and leverage field project data.",
        entity_scope="Storage developers, regulators",
        confidence=0.82,
        confidence_zone="Medium-High",
        controlling_precedent="CarbFix Project (Iceland)"
    ),
    DoctrineBlock(
        topic="CO2 Storage Liability and Long-Term Stewardship",
        keywords=[
            "liability", "long-term stewardship", "CO2 storage", "post-closure", "financial assurance"
        ],
        conclusion_template="Long-term liability for CO2 storage must be addressed through regulatory frameworks, financial assurance, and post-closure stewardship plans.",
        reasoning_framework="""
        1. Review regulatory requirements for post-closure care and liability transfer.
        2. Assess financial assurance mechanisms (trust funds, insurance).
        3. Evaluate monitoring and reporting obligations post-injection.
        4. Analyze stakeholder concerns and public trust.
        5. Synthesize findings for risk management and compliance.
        """,
        key_factors=[
            "Regulatory framework", "Financial assurance", "Monitoring", "Liability transfer", "Stakeholder trust"
        ],
        primary_authority=[
            "US EPA", "California Air Resources Board", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Long-term liability is a barrier to investment in CO2 storage.",
        counter_arguments=[
            "Regulatory frameworks provide for liability transfer after post-closure care.",
            "Financial assurance mechanisms mitigate risk.",
            "Transparent stewardship builds public trust."
        ],
        resolution_strategy="Comply with regulatory requirements and maintain robust financial assurance.",
        entity_scope="Storage operators, regulators, insurers",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="California LCFS CCS Protocol, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Site Selection and Characterization",
        keywords=[
            "site selection", "characterization", "CO2 storage", "geology", "risk assessment"
        ],
        conclusion_template="Thorough site selection and characterization are critical to ensure safe, permanent CO2 storage and regulatory compliance.",
        reasoning_framework="""
        1. Identify candidate formations based on geology and storage capacity.
        2. Conduct seismic surveys and core sampling.
        3. Assess caprock integrity and faulting.
        4. Evaluate hydrological and geochemical conditions.
        5. Model CO2 plume migration and pressure.
        6. Synthesize findings for site selection and permitting.
        """,
        key_factors=[
            "Geology", "Caprock integrity", "Hydrology", "Plume modeling", "Risk assessment"
        ],
        primary_authority=[
            "US DOE", "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage developer",
        adversary_position="Site selection is uncertain and prone to error, risking leakage.",
        counter_arguments=[
            "Advances in geophysical techniques improve site characterization.",
            "Multiple lines of evidence reduce uncertainty.",
            "Rigorous regulatory review ensures safety."
        ],
        resolution_strategy="Follow best practices and regulatory guidance for site characterization.",
        entity_scope="Storage developers, regulators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sleipner Project, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Well Integrity Management",
        keywords=[
            "well integrity", "CO2 storage", "cementing", "corrosion", "well monitoring"
        ],
        conclusion_template="Well integrity management is essential for safe CO2 storage, requiring robust construction, monitoring, and maintenance practices.",
        reasoning_framework="""
        1. Design wells with materials compatible with CO2-rich environments.
        2. Implement best practices for cementing and zonal isolation.
        3. Monitor well integrity throughout injection and post-closure.
        4. Assess corrosion risks and mitigation strategies.
        5. Synthesize findings for risk management and regulatory compliance.
        """,
        key_factors=[
            "Material selection", "Cementing", "Monitoring", "Corrosion control", "Regulatory compliance"
        ],
        primary_authority=[
            "API Standards", "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Well failures will lead to CO2 leakage and environmental harm.",
        counter_arguments=[
            "Modern well construction standards minimize leakage risk.",
            "Continuous monitoring enables early detection and remediation.",
            "Regulatory oversight enforces best practices."
        ],
        resolution_strategy="Adopt industry standards and maintain rigorous monitoring and maintenance.",
        entity_scope="Storage operators, regulators",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 1110, Sleipner Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Induced Seismicity Risk Management",
        keywords=[
            "induced seismicity", "CO2 storage", "pressure management", "faults", "monitoring"
        ],
        conclusion_template="Induced seismicity risk in CO2 storage can be managed through careful site selection, pressure management, and real-time monitoring.",
        reasoning_framework="""
        1. Assess seismic history and faulting in candidate storage sites.
        2. Model pressure buildup and fault slip potential.
        3. Implement real-time seismic monitoring networks.
        4. Develop operational protocols for pressure management.
        5. Synthesize findings for risk mitigation and regulatory compliance.
        """,
        key_factors=[
            "Seismic history", "Fault mapping", "Pressure management", "Monitoring", "Operational protocols"
        ],
        primary_authority=[
            "USGS", "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="CO2 injection will trigger damaging earthquakes.",
        counter_arguments=[
            "Site screening excludes high-risk faulted areas.",
            "Pressure management protocols reduce seismic risk.",
            "Real-time monitoring enables rapid response."
        ],
        resolution_strategy="Implement comprehensive risk assessment and adaptive management protocols.",
        entity_scope="Storage operators, regulators",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Plume Migration Modeling",
        keywords=[
            "plume migration", "CO2 storage", "reservoir modeling", "simulation", "risk assessment"
        ],
        conclusion_template="Accurate modeling of CO2 plume migration is essential for predicting storage performance and ensuring regulatory compliance.",
        reasoning_framework="""
        1. Collect site-specific geological and hydrological data.
        2. Develop reservoir models using industry-standard simulation tools.
        3. Calibrate models with field data and monitoring results.
        4. Predict plume migration and pressure evolution.
        5. Synthesize findings for risk assessment and regulatory reporting.
        """,
        key_factors=[
            "Geological data", "Simulation tools", "Model calibration", "Monitoring data", "Regulatory reporting"
        ],
        primary_authority=[
            "US DOE", "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Modeling is too uncertain to ensure safe storage.",
        counter_arguments=[
            "Model calibration with field data improves predictive accuracy.",
            "Multiple modeling approaches can be used for cross-validation.",
            "Regulatory review ensures robustness."
        ],
        resolution_strategy="Use best-available modeling tools and validate with monitoring data.",
        entity_scope="Storage operators, regulators",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Sleipner Project, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Pressure Management and Brine Displacement",
        keywords=[
            "pressure management", "brine displacement", "CO2 storage", "reservoir engineering", "risk mitigation"
        ],
        conclusion_template="Pressure management and brine displacement strategies are critical to prevent caprock breach and induced seismicity during CO2 injection.",
        reasoning_framework="""
        1. Model reservoir pressure evolution during injection.
        2. Assess brine displacement pathways and risks.
        3. Develop operational protocols for injection rate control.
        4. Monitor pressure and fluid movement in real time.
        5. Synthesize findings for risk mitigation and regulatory compliance.
        """,
        key_factors=[
            "Reservoir modeling", "Injection protocols", "Pressure monitoring", "Brine displacement", "Regulatory compliance"
        ],
        primary_authority=[
            "US DOE", "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Pressure buildup will cause caprock failure and leakage.",
        counter_arguments=[
            "Pressure management protocols are standard practice.",
            "Real-time monitoring enables rapid response.",
            "Regulatory oversight enforces safe injection rates."
        ],
        resolution_strategy="Implement adaptive pressure management and monitoring protocols.",
        entity_scope="Storage operators, regulators",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Environmental Justice and Community Engagement",
        keywords=[
            "environmental justice", "community engagement", "CO2 storage", "public participation", "stakeholder trust"
        ],
        conclusion_template="Meaningful community engagement and attention to environmental justice are essential for the successful siting and operation of CO2 storage projects.",
        reasoning_framework="""
        1. Identify impacted communities and stakeholders.
        2. Conduct outreach and solicit input on project design and siting.
        3. Assess potential disproportionate impacts and mitigation strategies.
        4. Ensure transparency in risk communication and decision-making.
        5. Synthesize findings for project planning and regulatory compliance.
        """,
        key_factors=[
            "Stakeholder identification", "Outreach", "Impact assessment", "Transparency", "Mitigation strategies"
        ],
        primary_authority=[
            "US EPA", "US DOE", "California Air Resources Board"
        ],
        burden_holder="Project developer",
        adversary_position="CO2 storage projects impose risks on vulnerable communities.",
        counter_arguments=[
            "Early and ongoing engagement builds trust.",
            "Impact assessments identify and mitigate risks.",
            "Regulatory frameworks require public participation."
        ],
        resolution_strategy="Implement robust community engagement and impact mitigation plans.",
        entity_scope="Project developers, regulators, communities",
        confidence=0.83,
        confidence_zone="Medium-High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Public Perception and Acceptance",
        keywords=[
            "public perception", "acceptance", "CO2 storage", "risk communication", "outreach"
        ],
        conclusion_template="Public perception and acceptance are critical to the success of CO2 storage projects, requiring transparent communication and stakeholder engagement.",
        reasoning_framework="""
        1. Assess public awareness and concerns regarding CO2 storage.
        2. Develop risk communication strategies tailored to local context.
        3. Engage stakeholders through outreach and education.
        4. Monitor public sentiment and adapt engagement as needed.
        5. Synthesize findings for project planning and risk management.
        """,
        key_factors=[
            "Public awareness", "Risk communication", "Stakeholder engagement", "Sentiment monitoring", "Adaptability"
        ],
        primary_authority=[
            "Global CCS Institute", "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Public opposition will block CO2 storage projects.",
        counter_arguments=[
            "Transparent communication builds understanding and trust.",
            "Engagement can address concerns and misconceptions.",
            "Successful projects have demonstrated public acceptance."
        ],
        resolution_strategy="Prioritize transparent, ongoing public engagement and education.",
        entity_scope="Project developers, communities",
        confidence=0.81,
        confidence_zone="Medium-High",
        controlling_precedent="Sleipner Project, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Regulatory Harmonization and Policy Alignment",
        keywords=[
            "regulatory harmonization", "policy alignment", "CO2 storage", "federal", "state", "international"
        ],
        conclusion_template="Regulatory harmonization and policy alignment are necessary to enable efficient, large-scale CO2 storage deployment.",
        reasoning_framework="""
        1. Review federal, state, and international regulatory frameworks.
        2. Identify inconsistencies and gaps in permitting and oversight.
        3. Engage with policymakers and stakeholders to align requirements.
        4. Develop recommendations for harmonization and best practices.
        5. Synthesize findings for policy advocacy and project planning.
        """,
        key_factors=[
            "Regulatory review", "Gap analysis", "Stakeholder engagement", "Best practices", "Policy advocacy"
        ],
        primary_authority=[
            "US EPA", "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Policy makers",
        adversary_position="Fragmented regulations will delay or prevent CCS deployment.",
        counter_arguments=[
            "Ongoing efforts are aligning state and federal requirements.",
            "International best practices inform policy development.",
            "Stakeholder engagement supports harmonization."
        ],
        resolution_strategy="Participate in policy forums and advocate for harmonization.",
        entity_scope="Policy makers, project developers",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="California LCFS CCS Protocol, EPA Class VI Guidance"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Financing and Risk Allocation",
        keywords=[
            "project finance", "risk allocation", "CO2 storage", "insurance", "public-private partnership"
        ],
        conclusion_template="Innovative financing mechanisms and clear risk allocation are essential for bankable CO2 storage projects.",
        reasoning_framework="""
        1. Assess project capital and operating cost structure.
        2. Identify and allocate key risks (technical, regulatory, market).
        3. Evaluate insurance and risk mitigation instruments.
        4. Consider public-private partnership models.
        5. Synthesize findings for project finance structuring.
        """,
        key_factors=[
            "Cost structure", "Risk allocation", "Insurance", "Partnership models", "Bankability"
        ],
        primary_authority=[
            "World Bank", "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Uncertain risks make CO2 storage projects unbankable.",
        counter_arguments=[
            "Risk allocation frameworks are maturing.",
            "Insurance products are emerging for CCS projects.",
            "Public-private partnerships can share risk."
        ],
        resolution_strategy="Engage with financiers and insurers early, and structure risk allocation transparently.",
        entity_scope="Project developers, investors, insurers",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="World Bank CCS Finance Reports"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Insurance and Financial Assurance",
        keywords=[
            "insurance", "financial assurance", "CO2 storage", "liability", "risk management"
        ],
        conclusion_template="Insurance and financial assurance instruments are increasingly available to manage long-term CO2 storage risks and support regulatory compliance.",
        reasoning_framework="""
        1. Review regulatory requirements for financial assurance.
        2. Assess available insurance products for CO2 storage risks.
        3. Evaluate cost and coverage of financial instruments.
        4. Engage with insurers and regulators to tailor solutions.
        5. Synthesize findings for project risk management.
        """,
        key_factors=[
            "Regulatory requirements", "Insurance products", "Cost and coverage", "Stakeholder engagement", "Risk management"
        ],
        primary_authority=[
            "US EPA", "World Bank", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Insurance is unavailable or unaffordable for CO2 storage risks.",
        counter_arguments=[
            "Insurance markets are evolving to cover CCS risks.",
            "Financial assurance is required by regulators.",
            "Early engagement with insurers can tailor solutions."
        ],
        resolution_strategy="Work with insurers and regulators to secure appropriate coverage.",
        entity_scope="Storage operators, insurers, regulators",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Data Management and Transparency",
        keywords=[
            "data management", "transparency", "CO2 storage", "monitoring data", "public reporting"
        ],
        conclusion_template="Robust data management and transparency are essential for regulatory compliance, public trust, and project optimization in CO2 storage.",
        reasoning_framework="""
        1. Develop data management systems for monitoring and operational data.
        2. Ensure data integrity and security.
        3. Establish protocols for public reporting and transparency.
        4. Engage with regulators and stakeholders on data sharing.
        5. Synthesize findings for continuous improvement and compliance.
        """,
        key_factors=[
            "Data integrity", "Security", "Public reporting", "Stakeholder engagement", "Continuous improvement"
        ],
        primary_authority=[
            "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="Data secrecy undermines public trust in CO2 storage.",
        counter_arguments=[
            "Transparent data sharing builds trust.",
            "Regulatory frameworks require public reporting.",
            "Robust data management supports project optimization."
        ],
        resolution_strategy="Implement transparent data management and reporting protocols.",
        entity_scope="Storage operators, regulators, public",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Performance Verification and Third-Party Certification",
        keywords=[
            "performance verification", "third-party certification", "CO2 storage", "monitoring", "carbon credits"
        ],
        conclusion_template="Third-party performance verification and certification are critical for credit issuance and public confidence in CO2 storage projects.",
        reasoning_framework="""
        1. Identify certification standards and protocols (e.g., ISO, LCFS).
        2. Engage accredited third-party verifiers.
        3. Develop monitoring and reporting plans to meet certification requirements.
        4. Conduct periodic audits and performance reviews.
        5. Synthesize findings for credit issuance and public reporting.
        """,
        key_factors=[
            "Certification standards", "Third-party verification", "Monitoring plan", "Audit protocols", "Public reporting"
        ],
        primary_authority=[
            "ISO 14064", "California Air Resources Board", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Certification is costly and adds administrative burden.",
        counter_arguments=[
            "Certification is required for credit issuance and market access.",
            "Third-party verification ensures credibility.",
            "Standardized protocols streamline the process."
        ],
        resolution_strategy="Engage with certifiers early and integrate certification into project planning.",
        entity_scope="Project developers, verifiers, regulators",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Integration with Renewable Energy",
        keywords=[
            "integration", "renewable energy", "CO2 storage", "hybrid systems", "grid balancing"
        ],
        conclusion_template="Integrating CO2 storage projects with renewable energy can enhance grid flexibility and reduce lifecycle emissions.",
        reasoning_framework="""
        1. Assess renewable energy availability for CO2 capture and compression.
        2. Evaluate hybrid system design and operational flexibility.
        3. Analyze lifecycle emissions and net climate benefit.
        4. Consider grid integration and balancing services.
        5. Synthesize findings for project optimization and emissions reduction.
        """,
        key_factors=[
            "Renewable energy availability", "Hybrid system design", "Lifecycle emissions", "Grid integration", "Operational flexibility"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Integration with renewables is technically complex and costly.",
        counter_arguments=[
            "Hybrid systems can optimize energy use and emissions.",
            "Grid services can provide additional revenue streams.",
            "Technology advances are reducing integration costs."
        ],
        resolution_strategy="Conduct system integration studies and leverage renewable energy incentives.",
        entity_scope="Project developers, utilities",
        confidence=0.83,
        confidence_zone="Medium-High",
        controlling_precedent="IEA Reports on CCUS and Renewables"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Water Resource Management",
        keywords=[
            "water resource management", "CO2 storage", "brine production", "water use", "environmental impact"
        ],
        conclusion_template="Effective water resource management is essential to minimize environmental impacts of CO2 storage, particularly in water-stressed regions.",
        reasoning_framework="""
        1. Assess water use and brine production associated with CO2 injection.
        2. Evaluate potential impacts on local water resources.
        3. Develop water management and treatment strategies.
        4. Engage with regulators and stakeholders on water issues.
        5. Synthesize findings for project planning and compliance.
        """,
        key_factors=[
            "Water use", "Brine production", "Impact assessment", "Management strategies", "Regulatory compliance"
        ],
        primary_authority=[
            "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="CO2 storage will deplete or contaminate local water resources.",
        counter_arguments=[
            "Water management strategies can minimize impacts.",
            "Regulatory frameworks require impact assessment and mitigation.",
            "Stakeholder engagement addresses local concerns."
        ],
        resolution_strategy="Implement robust water management and monitoring protocols.",
        entity_scope="Project developers, regulators, communities",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Air Quality and Health Impact Assessment",
        keywords=[
            "air quality", "health impact", "CO2 storage", "risk assessment", "monitoring"
        ],
        conclusion_template="Air quality and health impact assessments are required to ensure safe operation and regulatory compliance for CO2 storage projects.",
        reasoning_framework="""
        1. Identify potential air emissions from CO2 storage operations.
        2. Conduct health risk assessments for workers and nearby communities.
        3. Develop air monitoring and mitigation plans.
        4. Engage with regulators and public health agencies.
        5. Synthesize findings for project planning and compliance.
        """,
        key_factors=[
            "Emissions identification", "Health risk assessment", "Monitoring", "Mitigation", "Regulatory compliance"
        ],
        primary_authority=[
            "US EPA", "CDC", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="CO2 storage operations will harm air quality and public health.",
        counter_arguments=[
            "Air emissions from storage are minimal and manageable.",
            "Monitoring and mitigation plans address risks.",
            "Regulatory oversight ensures public safety."
        ],
        resolution_strategy="Conduct thorough impact assessments and implement mitigation measures.",
        entity_scope="Project developers, regulators, communities",
        confidence=0.82,
        confidence_zone="Medium-High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Emergency Response Planning",
        keywords=[
            "emergency response", "CO2 storage", "contingency planning", "incident management", "public safety"
        ],
        conclusion_template="Comprehensive emergency response planning is essential to ensure public safety and regulatory compliance for CO2 storage projects.",
        reasoning_framework="""
        1. Identify potential emergency scenarios (e.g., well blowout, leak).
        2. Develop incident response and communication protocols.
        3. Coordinate with local emergency services and regulators.
        4. Conduct training and emergency drills.
        5. Synthesize findings for continuous improvement and compliance.
        """,
        key_factors=[
            "Scenario identification", "Response protocols", "Coordination", "Training", "Continuous improvement"
        ],
        primary_authority=[
            "US EPA", "FEMA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Storage operator",
        adversary_position="CO2 storage emergencies will endanger public safety.",
        counter_arguments=[
            "Comprehensive planning and training minimize risk.",
            "Coordination with emergency services ensures readiness.",
            "Regulatory frameworks require emergency response plans."
        ],
        resolution_strategy="Maintain and regularly update emergency response plans and conduct drills.",
        entity_scope="Storage operators, emergency services, regulators",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Stakeholder Benefit Sharing",
        keywords=[
            "stakeholder benefit", "community benefit", "CO2 storage", "local economic development", "public trust"
        ],
        conclusion_template="Benefit sharing with local stakeholders enhances public trust and supports the long-term success of CO2 storage projects.",
        reasoning_framework="""
        1. Identify local stakeholders and potential benefits.
        2. Develop benefit-sharing mechanisms (e.g., jobs, infrastructure, revenue sharing).
        3. Engage stakeholders in project planning and decision-making.
        4. Monitor and report on benefit delivery.
        5. Synthesize findings for continuous improvement and public trust.
        """,
        key_factors=[
            "Stakeholder identification", "Benefit mechanisms", "Engagement", "Monitoring", "Transparency"
        ],
        primary_authority=[
            "World Bank", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="CO2 storage projects provide little or no benefit to local communities.",
        counter_arguments=[
            "Benefit-sharing enhances local support and trust.",
            "Engagement ensures benefits align with community needs.",
            "Monitoring and reporting increase transparency."
        ],
        resolution_strategy="Develop and implement tailored benefit-sharing plans.",
        entity_scope="Project developers, communities",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="World Bank CCS Community Engagement Reports"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project International Collaboration and Knowledge Sharing",
        keywords=[
            "international collaboration", "knowledge sharing", "CO2 storage", "best practices", "capacity building"
        ],
        conclusion_template="International collaboration and knowledge sharing accelerate CO2 storage deployment and improve project outcomes.",
        reasoning_framework="""
        1. Identify relevant international initiatives and networks.
        2. Participate in knowledge sharing and best practice forums.
        3. Engage in joint research and demonstration projects.
        4. Leverage international experience for domestic project development.
        5. Synthesize findings for continuous improvement and capacity building.
        """,
        key_factors=[
            "International initiatives", "Knowledge sharing", "Joint projects", "Best practices", "Capacity building"
        ],
        primary_authority=[
            "IEA Greenhouse Gas R&D Programme", "Global CCS Institute", "US DOE"
        ],
        burden_holder="Project developer",
        adversary_position="International collaboration is slow and yields little practical benefit.",
        counter_arguments=[
            "Collaboration accelerates learning and risk reduction.",
            "Best practice sharing improves project outcomes.",
            "Joint projects leverage resources and expertise."
        ],
        resolution_strategy="Actively participate in international networks and apply lessons learned.",
        entity_scope="Project developers, policy makers, researchers",
        confidence=0.83,
        confidence_zone="Medium-High",
        controlling_precedent="IEA Greenhouse Gas R&D Programme"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Technology Innovation and Continuous Improvement",
        keywords=[
            "technology innovation", "continuous improvement", "CO2 storage", "R&D", "best practices"
        ],
        conclusion_template="Ongoing technology innovation and continuous improvement are essential to reduce costs and risks in CO2 storage.",
        reasoning_framework="""
        1. Monitor emerging technologies and R&D developments.
        2. Implement pilot and demonstration projects to test innovations.
        3. Integrate successful innovations into commercial projects.
        4. Share lessons learned and best practices across the industry.
        5. Synthesize findings for continuous improvement and cost reduction.
        """,
        key_factors=[
            "R&D monitoring", "Pilot projects", "Integration", "Best practice sharing", "Cost reduction"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme", "Global CCS Institute"
        ],
        burden_holder="Project developer",
        adversary_position="Innovation is too slow to make CO2 storage cost-competitive.",
        counter_arguments=[
            "R&D investment is accelerating technology progress.",
            "Pilots are demonstrating rapid learning and cost reduction.",
            "Industry collaboration spreads best practices."
        ],
        resolution_strategy="Invest in R&D and foster industry collaboration for innovation.",
        entity_scope="Project developers, technology providers",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="US DOE CarbonSAFE Initiative"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Supply Chain and Workforce Development",
        keywords=[
            "supply chain", "workforce development", "CO2 storage", "local content", "capacity building"
        ],
        conclusion_template="Robust supply chain and workforce development are critical for timely, cost-effective CO2 storage project delivery.",
        reasoning_framework="""
        1. Assess supply chain readiness and local content opportunities.
        2. Identify workforce skills gaps and training needs.
        3. Develop partnerships with educational and training institutions.
        4. Monitor supply chain performance and adapt as needed.
        5. Synthesize findings for project planning and capacity building.
        """,
        key_factors=[
            "Supply chain readiness", "Workforce skills", "Training", "Local content", "Performance monitoring"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Supply chain and workforce constraints will delay projects.",
        counter_arguments=[
            "Early planning and partnerships mitigate constraints.",
            "Training programs build local capacity.",
            "Supply chain monitoring enables rapid response."
        ],
        resolution_strategy="Invest in workforce training and supply chain development.",
        entity_scope="Project developers, educational institutions",
        confidence=0.82,
        confidence_zone="Medium-High",
        controlling_precedent="US DOE Workforce Development Initiatives"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Environmental Impact Assessment (EIA)",
        keywords=[
            "environmental impact assessment", "EIA", "CO2 storage", "regulatory compliance", "public participation"
        ],
        conclusion_template="Comprehensive EIA is required for CO2 storage projects to identify, assess, and mitigate environmental impacts and ensure regulatory compliance.",
        reasoning_framework="""
        1. Identify potential environmental impacts of the project.
        2. Conduct baseline studies and stakeholder consultations.
        3. Develop mitigation and monitoring plans.
        4. Submit EIA for regulatory review and public comment.
        5. Synthesize findings for project approval and continuous improvement.
        """,
        key_factors=[
            "Impact identification", "Baseline studies", "Mitigation plans", "Stakeholder consultation", "Regulatory review"
        ],
        primary_authority=[
            "US EPA", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="EIA is a bureaucratic hurdle that delays projects.",
        counter_arguments=[
            "EIA ensures environmental protection and public trust.",
            "Early engagement streamlines the process.",
            "Mitigation plans reduce project risks."
        ],
        resolution_strategy="Conduct thorough EIA and engage stakeholders early.",
        entity_scope="Project developers, regulators, communities",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Social License to Operate",
        keywords=[
            "social license", "public trust", "CO2 storage", "community engagement", "transparency"
        ],
        conclusion_template="Securing a social license to operate is essential for the long-term success of CO2 storage projects, requiring ongoing engagement and transparency.",
        reasoning_framework="""
        1. Engage communities and stakeholders early and often.
        2. Maintain transparency in project planning and operations.
        3. Address concerns and adapt plans as needed.
        4. Monitor public sentiment and respond proactively.
        5. Synthesize findings for continuous improvement and trust building.
        """,
        key_factors=[
            "Community engagement", "Transparency", "Responsiveness", "Monitoring", "Continuous improvement"
        ],
        primary_authority=[
            "Global CCS Institute", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Lack of public trust will prevent project success.",
        counter_arguments=[
            "Ongoing engagement builds trust and acceptance.",
            "Transparency addresses concerns and misinformation.",
            "Successful projects maintain strong community relationships."
        ],
        resolution_strategy="Prioritize social license considerations in all project phases.",
        entity_scope="Project developers, communities",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="Sleipner Project, Illinois Basin Decatur Project"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Climate Policy Alignment",
        keywords=[
            "climate policy", "Paris Agreement", "CO2 storage", "net zero", "compliance"
        ],
        conclusion_template="CO2 storage projects must align with national and international climate policies to ensure long-term viability and access to incentives.",
        reasoning_framework="""
        1. Review relevant climate policies and targets (e.g., Paris Agreement, net zero).
        2. Assess project alignment with policy objectives and timelines.
        3. Evaluate eligibility for incentives and compliance mechanisms.
        4. Monitor policy developments and adapt project plans as needed.
        5. Synthesize findings for long-term project viability.
        """,
        key_factors=[
            "Policy review", "Alignment assessment", "Incentive eligibility", "Monitoring", "Adaptability"
        ],
        primary_authority=[
            "UNFCCC", "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Policy uncertainty undermines investment in CO2 storage.",
        counter_arguments=[
            "Policy alignment increases project certainty and access to incentives.",
            "Monitoring and adaptability reduce risk.",
            "International frameworks support long-term viability."
        ],
        resolution_strategy="Align project planning with evolving policy frameworks.",
        entity_scope="Project developers, policy makers",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Paris Agreement, US 45Q Guidance"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Market Development and Carbon Credit Trading",
        keywords=[
            "market development", "carbon credits", "CO2 storage", "trading", "offsets"
        ],
        conclusion_template="Robust carbon credit markets are essential to incentivize investment in CO2 storage and enable trading of verified emissions reductions.",
        reasoning_framework="""
        1. Review carbon credit standards and market frameworks.
        2. Assess project eligibility for credit issuance.
        3. Engage with market registries and trading platforms.
        4. Monitor market developments and price signals.
        5. Synthesize findings for project finance and risk management.
        """,
        key_factors=[
            "Credit standards", "Market frameworks", "Eligibility", "Market engagement", "Price monitoring"
        ],
        primary_authority=[
            "Verra", "Gold Standard", "California Air Resources Board"
        ],
        burden_holder="Project developer",
        adversary_position="Carbon credit markets are too volatile and uncertain.",
        counter_arguments=[
            "Market frameworks are maturing and stabilizing.",
            "Verified credits provide revenue and risk management.",
            "Engagement with registries ensures compliance."
        ],
        resolution_strategy="Participate in market development and monitor price trends.",
        entity_scope="Project developers, investors, registries",
        confidence=0.82,
        confidence_zone="Medium-High",
        controlling_precedent="California LCFS CCS Protocol"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Cross-Sectoral Integration",
        keywords=[
            "cross-sectoral integration", "CO2 storage", "industrial clusters", "hydrogen", "energy transition"
        ],
        conclusion_template="Cross-sectoral integration of CO2 storage with industrial clusters and hydrogen production enhances efficiency and accelerates decarbonization.",
        reasoning_framework="""
        1. Identify opportunities for integration with industrial clusters and hydrogen hubs.
        2. Assess shared infrastructure and cost savings.
        3. Evaluate emissions reduction potential and policy alignment.
        4. Engage stakeholders across sectors for coordinated planning.
        5. Synthesize findings for project optimization and risk reduction.
        """,
        key_factors=[
            "Integration opportunities", "Shared infrastructure", "Cost savings", "Emissions reduction", "Stakeholder coordination"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Cross-sectoral integration is too complex and slow.",
        counter_arguments=[
            "Shared infrastructure reduces costs and accelerates deployment.",
            "Policy support is increasing for industrial decarbonization.",
            "Stakeholder coordination enables efficient planning."
        ],
        resolution_strategy="Pursue integration opportunities and leverage policy incentives.",
        entity_scope="Project developers, industrial operators",
        confidence=0.83,
        confidence_zone="Medium-High",
        controlling_precedent="UK Industrial Clusters Mission"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Digitalization and Automation",
        keywords=[
            "digitalization", "automation", "CO2 storage", "monitoring", "data analytics"
        ],
        conclusion_template="Digitalization and automation enhance monitoring, operational efficiency, and risk management in CO2 storage projects.",
        reasoning_framework="""
        1. Assess digital technologies for monitoring and data analytics.
        2. Evaluate automation opportunities for operations and maintenance.
        3. Integrate digital systems with regulatory reporting requirements.
        4. Monitor performance and adapt systems as needed.
        5. Synthesize findings for continuous improvement and risk reduction.
        """,
        key_factors=[
            "Digital technology", "Automation", "Integration", "Performance monitoring", "Adaptability"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Digitalization adds cost and complexity without clear benefit.",
        counter_arguments=[
            "Digital systems improve efficiency and reduce risk.",
            "Automation streamlines operations and reporting.",
            "Continuous improvement increases project value."
        ],
        resolution_strategy="Invest in digital technologies and integrate with project planning.",
        entity_scope="Project developers, technology providers",
        confidence=0.81,
        confidence_zone="Medium-High",
        controlling_precedent="US DOE Digitalization Initiatives"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Supply Chain Resilience",
        keywords=[
            "supply chain resilience", "CO2 storage", "risk management", "local sourcing", "disruption"
        ],
        conclusion_template="Building resilient supply chains is essential to mitigate risks and ensure timely delivery of CO2 storage projects.",
        reasoning_framework="""
        1. Assess supply chain vulnerabilities and critical components.
        2. Develop local sourcing and diversification strategies.
        3. Monitor supply chain performance and adapt as needed.
        4. Engage with suppliers and stakeholders for risk management.
        5. Synthesize findings for project planning and resilience.
        """,
        key_factors=[
            "Vulnerability assessment", "Local sourcing", "Diversification", "Performance monitoring", "Stakeholder engagement"
        ],
        primary_authority=[
            "US DOE", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Supply chain disruptions will delay or derail projects.",
        counter_arguments=[
            "Resilience planning mitigates disruption risk.",
            "Local sourcing reduces dependency on global supply chains.",
            "Continuous monitoring enables rapid response."
        ],
        resolution_strategy="Implement supply chain resilience planning and monitoring.",
        entity_scope="Project developers, suppliers",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="US DOE Supply Chain Reports"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Gender and Diversity Inclusion",
        keywords=[
            "gender inclusion", "diversity", "CO2 storage", "workforce", "equity"
        ],
        conclusion_template="Promoting gender and diversity inclusion in CO2 storage projects strengthens workforce capacity and social license.",
        reasoning_framework="""
        1. Assess current workforce diversity and inclusion practices.
        2. Develop recruitment and retention strategies for underrepresented groups.
        3. Monitor diversity metrics and adapt programs as needed.
        4. Engage with stakeholders on equity and inclusion.
        5. Synthesize findings for continuous improvement and social license.
        """,
        key_factors=[
            "Workforce diversity", "Inclusion strategies", "Monitoring", "Stakeholder engagement", "Continuous improvement"
        ],
        primary_authority=[
            "World Bank", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="Diversity initiatives are irrelevant to project success.",
        counter_arguments=[
            "Diverse teams improve innovation and performance.",
            "Inclusion strengthens social license and public trust.",
            "Monitoring and adaptation ensure progress."
        ],
        resolution_strategy="Implement diversity and inclusion programs and monitor outcomes.",
        entity_scope="Project developers, workforce",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="World Bank Gender and CCS Reports"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Indigenous Peoples Engagement",
        keywords=[
            "indigenous engagement", "CO2 storage", "free, prior and informed consent", "cultural heritage", "stakeholder engagement"
        ],
        conclusion_template="Respectful engagement with Indigenous Peoples, including free, prior and informed consent, is essential for CO2 storage projects on or near traditional lands.",
        reasoning_framework="""
        1. Identify Indigenous communities potentially impacted by the project.
        2. Engage early and seek free, prior and informed consent.
        3. Assess and mitigate impacts on cultural heritage and rights.
        4. Develop benefit-sharing and partnership agreements.
        5. Synthesize findings for project planning and compliance.
        """,
        key_factors=[
            "Community identification", "Consent", "Cultural heritage", "Benefit sharing", "Compliance"
        ],
        primary_authority=[
            "UNDRIP", "World Bank", "IEA Greenhouse Gas R&D Programme"
        ],
        burden_holder="Project developer",
        adversary_position="CO2 storage projects violate Indigenous rights.",
        counter_arguments=[
            "Early and respectful engagement builds trust.",
            "Benefit-sharing agreements support mutual benefit.",
            "International frameworks guide best practices."
        ],
        resolution_strategy="Follow international best practices for Indigenous engagement.",
        entity_scope="Project developers, Indigenous communities",
        confidence=0.81,
        confidence_zone="Medium-High",
        controlling_precedent="World Bank Indigenous Peoples Policy"
    ),
    DoctrineBlock(
        topic="CO2 Storage Project Transparency and Anti-Corruption",
        keywords=[
            "transparency", "anti-corruption", "CO2 storage", "governance", "compliance"
        ],
        conclusion_template="Transparency and anti-corruption measures are essential for good governance and public trust in CO2 storage projects.",
        reasoning_framework="""
        1. Implement transparent reporting and disclosure practices.
        2. Develop anti-corruption policies and training.
        3. Monitor compliance and investigate irregularities.
        4. Engage