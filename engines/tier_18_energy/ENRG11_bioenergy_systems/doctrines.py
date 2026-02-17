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
        topic="Biomass Feedstock Energy Density Analysis",
        keywords=["biomass", "feedstock", "energy density", "calorific value", "moisture content"],
        conclusion_template="The energy density of {feedstock} is primarily determined by its moisture content and inherent calorific value, impacting logistics and conversion efficiency.",
        reasoning_framework="""
        1. Identify the type of biomass feedstock (woody, herbaceous, agricultural residue, etc.).
        2. Measure or reference the typical moisture content for the feedstock.
        3. Obtain the higher heating value (HHV) and lower heating value (LHV) from authoritative databases (e.g., NREL, EIA).
        4. Calculate energy density on a dry and as-received basis.
        5. Assess the impact of preprocessing (drying, pelletizing, torrefaction) on energy density.
        6. Compare energy density to fossil fuel benchmarks (e.g., coal, natural gas).
        7. Evaluate implications for transportation, storage, and conversion technology selection.
        8. Consider regional variations and supply chain logistics.
        9. Synthesize findings to inform feedstock selection and system design.
        """,
        key_factors=["Moisture content", "HHV/LHV", "Preprocessing", "Feedstock type", "Logistics"],
        primary_authority=["NREL Biomass Energy Data Book", "IEA Bioenergy Task 32", "US DOE"],
        burden_holder="Feedstock supplier",
        adversary_position="Moisture reduction is not cost-effective and does not significantly improve system efficiency.",
        counter_arguments=[
            "High moisture increases transport and handling costs.",
            "Low energy density reduces conversion system efficiency.",
            "Preprocessing can improve overall economics despite upfront costs."
        ],
        resolution_strategy="Quantify cost-benefit of preprocessing and select feedstock with optimal energy density for the application.",
        entity_scope="Biomass supply chain operators, project developers",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NREL Biomass Energy Data Book, Section 2.3"
    ),
    DoctrineBlock(
        topic="Anaerobic Digestion Kinetics and Reactor Design",
        keywords=["anaerobic digestion", "kinetics", "reactor design", "biogas", "retention time"],
        conclusion_template="Anaerobic digestion system design must match substrate kinetics with appropriate reactor type and hydraulic retention time to optimize biogas yield.",
        reasoning_framework="""
        1. Characterize the substrate (C/N ratio, biodegradability, particle size).
        2. Select kinetic model (first-order, Monod, ADM1) based on substrate complexity.
        3. Determine optimal temperature regime (mesophilic vs thermophilic).
        4. Calculate required hydraulic retention time (HRT) and solids retention time (SRT).
        5. Match reactor type (CSTR, plug-flow, UASB, batch) to substrate and operational needs.
        6. Model biogas yield using substrate-specific parameters.
        7. Evaluate mixing, heating, and loading strategies.
        8. Consider scale-up and operational stability.
        9. Validate design with pilot data or literature benchmarks.
        """,
        key_factors=["Substrate characteristics", "Kinetic model", "HRT/SRT", "Reactor selection", "Temperature"],
        primary_authority=["IEA Bioenergy Task 37", "VFA/Alkali guidelines", "US EPA AgSTAR"],
        burden_holder="System designer",
        adversary_position="Shorter retention times can be used without compromising yield.",
        counter_arguments=[
            "Insufficient retention reduces methane yield and process stability.",
            "Complex substrates require longer retention for complete digestion.",
            "Empirical data supports longer HRT for high-solids feedstocks."
        ],
        resolution_strategy="Base design on substrate-specific kinetic data and validated models.",
        entity_scope="AD system designers, EPC contractors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 37 Technical Brochure 2019"
    ),
    DoctrineBlock(
        topic="Biogas Upgrading and Purification Technologies",
        keywords=["biogas", "upgrading", "purification", "CO2 removal", "H2S removal", "membrane", "PSA"],
        conclusion_template="Selection of biogas upgrading technology should be based on feed gas composition, required biomethane quality, and lifecycle cost analysis.",
        reasoning_framework="""
        1. Analyze raw biogas composition (CH4, CO2, H2S, siloxanes, water vapor).
        2. Define biomethane quality requirements (pipeline, CNG, LNG, grid injection).
        3. Evaluate available upgrading technologies: water scrubbing, PSA, membrane separation, chemical scrubbing, cryogenic.
        4. Assess removal efficiency for CO2, H2S, and trace contaminants.
        5. Compare capital and operating costs, energy consumption, and footprint.
        6. Consider operational complexity and maintenance requirements.
        7. Factor in local regulations and incentives.
        8. Model lifecycle emissions and methane slip.
        9. Select technology with best fit for project scale and economics.
        """,
        key_factors=["Feed gas composition", "Product quality", "Technology fit", "Cost", "Regulatory"],
        primary_authority=["IEA Bioenergy Task 37", "US EPA", "DVGW G262"],
        burden_holder="Project developer",
        adversary_position="Cheapest technology should always be selected regardless of long-term performance.",
        counter_arguments=[
            "Low-cost options may have higher OPEX or lower product quality.",
            "Regulatory compliance may require advanced purification.",
            "Lifecycle analysis often favors higher CAPEX for lower emissions."
        ],
        resolution_strategy="Conduct multi-criteria analysis including lifecycle cost and regulatory compliance.",
        entity_scope="Biogas plant operators, technology vendors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 37 Upgrading Report 2021"
    ),
    DoctrineBlock(
        topic="Biodiesel Transesterification Chemistry and Process Control",
        keywords=["biodiesel", "transesterification", "process control", "catalyst", "FFA", "glycerol"],
        conclusion_template="Effective biodiesel production requires precise control of transesterification parameters and feedstock quality to maximize yield and meet ASTM D6751/EN 14214 standards.",
        reasoning_framework="""
        1. Analyze feedstock for free fatty acid (FFA) and water content.
        2. Select appropriate catalyst (alkaline, acid, enzymatic) based on FFA level.
        3. Control reaction temperature, molar ratio (alcohol:oil), and mixing intensity.
        4. Monitor reaction progress and endpoint using titration or spectroscopy.
        5. Separate biodiesel and glycerol phases efficiently.
        6. Wash and dry biodiesel to remove residual catalyst and methanol.
        7. Test product against ASTM D6751/EN 14214 specifications.
        8. Implement process automation for consistent quality.
        9. Optimize for minimal by-product and waste generation.
        """,
        key_factors=["Feedstock quality", "Catalyst selection", "Process parameters", "Product specs", "Separation"],
        primary_authority=["ASTM D6751", "EN 14214", "NREL Biodiesel Handbook"],
        burden_holder="Plant operator",
        adversary_position="Feedstock pretreatment is unnecessary for most oils.",
        counter_arguments=[
            "High FFA leads to soap formation and low yield.",
            "Water inhibits catalyst activity.",
            "Pretreatment ensures compliance with fuel standards."
        ],
        resolution_strategy="Implement feedstock testing and pretreatment protocols as standard practice.",
        entity_scope="Biodiesel producers, QA/QC labs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM D6751 Section 4, EN 14214"
    ),
    DoctrineBlock(
        topic="Cellulosic Ethanol Production via Enzymatic Hydrolysis",
        keywords=["cellulosic ethanol", "enzymatic hydrolysis", "pretreatment", "fermentation", "lignocellulose"],
        conclusion_template="Efficient cellulosic ethanol production relies on optimized pretreatment and enzyme cocktails to maximize sugar release for fermentation.",
        reasoning_framework="""
        1. Select lignocellulosic feedstock (corn stover, switchgrass, bagasse, etc.).
        2. Apply pretreatment (steam explosion, dilute acid, ammonia fiber expansion) to increase cellulose accessibility.
        3. Characterize pretreated biomass for cellulose, hemicellulose, lignin content.
        4. Choose enzyme blend (cellulase, hemicellulase, β-glucosidase) tailored to substrate.
        5. Optimize hydrolysis conditions (pH, temperature, solids loading).
        6. Monitor sugar release kinetics and conversion efficiency.
        7. Integrate hydrolysis with fermentation (SHF, SSF, CBP).
        8. Address inhibitor formation and removal.
        9. Scale up with pilot data and techno-economic analysis.
        """,
        key_factors=["Pretreatment efficacy", "Enzyme selection", "Hydrolysis conditions", "Inhibitor management", "Integration"],
        primary_authority=["NREL Cellulosic Ethanol Reports", "IEA Bioenergy Task 39"],
        burden_holder="Process developer",
        adversary_position="Enzyme cost outweighs benefits of higher conversion.",
        counter_arguments=[
            "Enzyme recycling and improved cocktails reduce cost.",
            "Higher conversion increases ethanol yield and plant economics.",
            "Pretreatment optimization can lower enzyme dose."
        ],
        resolution_strategy="Iteratively optimize pretreatment and enzyme use for lowest cost per liter ethanol.",
        entity_scope="Cellulosic ethanol plants, R&D labs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NREL Cellulosic Ethanol Process Design Report 2020"
    ),
    DoctrineBlock(
        topic="Feedstock Logistics and Supply Chain Optimization",
        keywords=["feedstock logistics", "supply chain", "biomass collection", "transport", "storage"],
        conclusion_template="A robust feedstock logistics strategy minimizes delivered cost and supply risk through regional aggregation, densification, and just-in-time delivery.",
        reasoning_framework="""
        1. Map regional biomass availability and seasonality.
        2. Model collection, aggregation, and preprocessing (chipping, baling, pelletizing).
        3. Optimize transport routes and modes (truck, rail, barge).
        4. Design storage systems to minimize dry matter loss and fire risk.
        5. Implement inventory management and just-in-time delivery.
        6. Evaluate supply contracts and risk mitigation strategies.
        7. Use GIS and simulation tools for scenario analysis.
        8. Integrate logistics with plant demand and conversion technology.
        9. Monitor market trends and adapt procurement strategy.
        """,
        key_factors=["Regional supply", "Aggregation", "Transport", "Storage", "Risk management"],
        primary_authority=["US DOE Billion-Ton Report", "IEA Bioenergy Task 40"],
        burden_holder="Supply chain manager",
        adversary_position="On-site storage is always preferable to regional depots.",
        counter_arguments=[
            "Centralized depots reduce transport cost and supply risk.",
            "On-site storage increases fire and spoilage risk.",
            "Just-in-time delivery improves cash flow and logistics."
        ],
        resolution_strategy="Adopt hybrid logistics with regional aggregation and flexible storage.",
        entity_scope="Biomass supply chain operators, project developers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="US DOE Billion-Ton Report 2016"
    ),
    DoctrineBlock(
        topic="Thermochemical Biomass Conversion: Gasification vs Pyrolysis",
        keywords=["thermochemical", "biomass", "gasification", "pyrolysis", "syngas", "bio-oil"],
        conclusion_template="Selection between gasification and pyrolysis should be based on desired product slate, feedstock characteristics, and integration with downstream processes.",
        reasoning_framework="""
        1. Characterize feedstock (ash content, moisture, particle size).
        2. Define desired products (syngas, bio-oil, biochar, heat).
        3. Compare process conditions: gasification (800-1000°C, air/oxygen/steam), pyrolysis (350-600°C, inert atmosphere).
        4. Assess conversion efficiency and product yields.
        5. Evaluate tar and contaminant management strategies.
        6. Consider integration with CHP, Fischer-Tropsch, or soil amendment.
        7. Model process economics and emissions.
        8. Factor in technology readiness and scalability.
        9. Select process with best fit for project goals and constraints.
        """,
        key_factors=["Feedstock", "Product slate", "Process conditions", "Integration", "Economics"],
        primary_authority=["IEA Bioenergy Task 33", "NREL Thermochemical Platform"],
        burden_holder="Process designer",
        adversary_position="Pyrolysis is universally superior due to bio-oil value.",
        counter_arguments=[
            "Gasification offers higher efficiency for power/fuel synthesis.",
            "Bio-oil markets are limited and require upgrading.",
            "Feedstock and scale often favor gasification."
        ],
        resolution_strategy="Conduct techno-economic and market analysis for site-specific selection.",
        entity_scope="Biomass conversion project developers, engineers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 33 Gasification vs Pyrolysis Review"
    ),
    DoctrineBlock(
        topic="Bioenergy Environmental Life Cycle and Carbon Accounting",
        keywords=["life cycle analysis", "carbon accounting", "GHG", "bioenergy", "sustainability"],
        conclusion_template="Bioenergy systems must demonstrate net GHG reductions via comprehensive life cycle analysis, accounting for direct and indirect emissions.",
        reasoning_framework="""
        1. Define system boundaries (cradle-to-gate, cradle-to-grave).
        2. Inventory all material and energy flows.
        3. Quantify direct emissions (combustion, process).
        4. Include indirect emissions (fertilizer, transport, land use change).
        5. Apply recognized LCA methodologies (ISO 14040/44, GREET).
        6. Compare GHG intensity to fossil reference systems.
        7. Assess co-product allocation and carbon sequestration.
        8. Evaluate uncertainty and sensitivity.
        9. Report results transparently for regulatory and market use.
        """,
        key_factors=["System boundaries", "Direct/indirect emissions", "LCA methodology", "Co-products", "Uncertainty"],
        primary_authority=["ISO 14040/44", "GREET Model", "EU RED II"],
        burden_holder="Project proponent",
        adversary_position="Bioenergy is always carbon neutral by definition.",
        counter_arguments=[
            "Land use change and supply chain emissions can offset benefits.",
            "LCA is required for regulatory compliance.",
            "Best practices ensure robust GHG reductions."
        ],
        resolution_strategy="Conduct third-party verified LCA and disclose methodology.",
        entity_scope="Bioenergy project developers, regulators",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 14044, EU RED II Annex V"
    ),
    DoctrineBlock(
        topic="Algae Cultivation for Biofuel Production",
        keywords=["algae", "cultivation", "biofuel", "photobioreactor", "open pond", "lipid content"],
        conclusion_template="Algae biofuel production is viable with high-lipid strains, optimized cultivation systems, and integrated co-product valorization.",
        reasoning_framework="""
        1. Select algal strain with high lipid productivity and robustness.
        2. Choose cultivation system (open pond, raceway, closed photobioreactor).
        3. Optimize nutrient supply, light, CO2 delivery, and mixing.
        4. Monitor growth kinetics and lipid accumulation.
        5. Harvest and dewater biomass efficiently.
        6. Extract lipids and process into biodiesel or renewable diesel.
        7. Valorize co-products (proteins, pigments, fertilizers).
        8. Assess water and energy use, and recycle where possible.
        9. Model techno-economics and environmental impacts.
        """,
        key_factors=["Strain selection", "Cultivation system", "Nutrient/light/CO2", "Harvesting", "Co-products"],
        primary_authority=["NREL Algae Biofuels Program", "IEA Bioenergy Task 39"],
        burden_holder="Algae project developer",
        adversary_position="Open ponds are always more cost-effective than closed systems.",
        counter_arguments=[
            "Closed photobioreactors offer higher productivity and contamination control.",
            "Site-specific factors may favor different systems.",
            "Hybrid approaches can optimize cost and yield."
        ],
        resolution_strategy="Pilot both systems and select based on site-specific performance and economics.",
        entity_scope="Algae biofuel developers, R&D labs",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="NREL Algae Program Reports 2018-2022"
    ),
    DoctrineBlock(
        topic="Biomass Co-firing in Coal Power Plants",
        keywords=["biomass", "co-firing", "coal", "power plant", "retrofit", "ash"],
        conclusion_template="Biomass co-firing in coal plants reduces GHG emissions but requires careful management of fuel handling, boiler performance, and ash quality.",
        reasoning_framework="""
        1. Assess plant suitability for co-firing (boiler type, fuel handling).
        2. Determine optimal biomass fraction (typically 5-20% thermal input).
        3. Evaluate impacts on combustion, emissions, and boiler efficiency.
        4. Address fuel feeding, storage, and milling modifications.
        5. Monitor ash quality for disposal or reuse.
        6. Ensure compliance with air quality and waste regulations.
        7. Model GHG reductions and economic impacts.
        8. Pilot test and monitor operational performance.
        9. Scale up co-firing based on results and regulatory incentives.
        """,
        key_factors=["Plant suitability", "Biomass fraction", "Boiler impacts", "Ash quality", "Regulatory"],
        primary_authority=["IEA Clean Coal Centre", "US DOE NETL", "EPRI"],
        burden_holder="Plant operator",
        adversary_position="Co-firing always reduces plant efficiency and increases maintenance.",
        counter_arguments=[
            "Properly managed co-firing can maintain efficiency.",
            "Fuel selection and handling are key to minimizing issues.",
            "Long-term pilots show manageable impacts."
        ],
        resolution_strategy="Implement phased co-firing with monitoring and adaptive management.",
        entity_scope="Coal power plant operators, utilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IEA Clean Coal Centre Co-firing Report 2017"
    ),
    DoctrineBlock(
        topic="Renewable Diesel via Hydrotreating (HVO/HEFA)",
        keywords=["renewable diesel", "hydrotreating", "HVO", "HEFA", "feedstock", "catalyst"],
        conclusion_template="Renewable diesel production via hydrotreating requires low-impurity feedstocks and robust catalyst management to ensure fuel quality and process economics.",
        reasoning_framework="""
        1. Select feedstock with low metals, sulfur, and phosphorus.
        2. Pre-treat feedstock to remove contaminants.
        3. Choose appropriate catalyst (NiMo, CoMo, noble metals).
        4. Control process conditions (temperature, pressure, H2/feed ratio).
        5. Monitor catalyst activity and manage regeneration/replacement.
        6. Test product for compliance with ASTM D975/EN 15940.
        7. Integrate with refinery or stand-alone operation.
        8. Evaluate co-product streams (propane, naphtha).
        9. Model process economics and lifecycle GHG impacts.
        """,
        key_factors=["Feedstock quality", "Catalyst", "Process control", "Product specs", "Integration"],
        primary_authority=["NREL Renewable Diesel Reports", "IEA Bioenergy Task 39"],
        burden_holder="Refinery operator",
        adversary_position="Any feedstock can be used without significant impact on catalyst life.",
        counter_arguments=[
            "Impurities poison catalysts and reduce yield.",
            "Feedstock pre-treatment extends catalyst life.",
            "Product quality depends on feedstock and process control."
        ],
        resolution_strategy="Implement rigorous feedstock screening and catalyst management protocols.",
        entity_scope="Renewable diesel producers, refineries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NREL Renewable Diesel Process Design Report 2021"
    ),
    DoctrineBlock(
        topic="Biogas CHP Sizing and Economics",
        keywords=["biogas", "CHP", "sizing", "economics", "capacity factor", "heat recovery"],
        conclusion_template="Biogas CHP systems should be sized to match average biogas production and site heat/power demand for optimal efficiency and project economics.",
        reasoning_framework="""
        1. Characterize biogas production profile (daily, seasonal).
        2. Assess site heat and power demand patterns.
        3. Select CHP technology (reciprocating engine, microturbine, fuel cell).
        4. Size system for average, not peak, biogas flow to maximize capacity factor.
        5. Optimize heat recovery and integration with site processes.
        6. Model system efficiency, OPEX, and revenue streams.
        7. Evaluate grid interconnection and export options.
        8. Analyze incentives, tariffs, and regulatory requirements.
        9. Conduct sensitivity analysis on key economic drivers.
        """,
        key_factors=["Biogas profile", "Site demand", "CHP technology", "Heat integration", "Economics"],
        primary_authority=["US EPA AgSTAR", "IEA Bioenergy Task 37", "NREL"],
        burden_holder="Project developer",
        adversary_position="Oversizing ensures future flexibility and is always preferable.",
        counter_arguments=[
            "Oversizing reduces capacity factor and increases cost.",
            "Right-sizing maximizes efficiency and ROI.",
            "Modular expansion is preferable to chronic underutilization."
        ],
        resolution_strategy="Size CHP for average load and plan for modular expansion.",
        entity_scope="Biogas project developers, engineers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="US EPA AgSTAR CHP Sizing Guide"
    ),
    DoctrineBlock(
        topic="Enzyme Production for Cellulosic Hydrolysis",
        keywords=["enzyme production", "cellulosic hydrolysis", "fermentation", "downstream processing"],
        conclusion_template="On-site enzyme production can reduce cellulosic ethanol costs if integrated with process energy and substrate streams.",
        reasoning_framework="""
        1. Select host organism (Trichoderma, Aspergillus, engineered yeast).
        2. Optimize fermentation conditions for high enzyme yield.
        3. Integrate enzyme production with ethanol process energy and substrate flows.
        4. Minimize downstream processing (concentration, purification) for cost savings.
        5. Evaluate enzyme activity and stability on target substrate.
        6. Compare on-site vs. commercial enzyme cost and logistics.
        7. Model impact on overall process economics.
        8. Address IP/licensing for engineered strains.
        9. Scale up with pilot data and risk assessment.
        """,
        key_factors=["Host organism", "Fermentation", "Integration", "Cost", "IP/licensing"],
        primary_authority=["NREL Enzyme Cost Reports", "IEA Bioenergy Task 39"],
        burden_holder="Process developer",
        adversary_position="Commercial enzymes are always more cost-effective.",
        counter_arguments=[
            "On-site production reduces logistics and can use process side-streams.",
            "Integration with process energy lowers cost.",
            "IP/licensing can be managed with partnerships."
        ],
        resolution_strategy="Conduct techno-economic analysis and pilot on-site production.",
        entity_scope="Cellulosic ethanol producers, R&D labs",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="NREL Enzyme Cost Reduction Reports"
    ),
    # Additional doctrine blocks for coverage and depth
    DoctrineBlock(
        topic="Biomass Ash Management and Utilization",
        keywords=["biomass", "ash", "management", "utilization", "disposal", "soil amendment"],
        conclusion_template="Biomass ash should be characterized and, where possible, valorized as a soil amendment or construction material, minimizing landfill disposal.",
        reasoning_framework="""
        1. Analyze ash composition for nutrients and contaminants.
        2. Assess suitability for land application (pH, heavy metals, nutrients).
        3. Evaluate regulatory limits for ash reuse.
        4. Consider use in construction materials (cement, bricks).
        5. Monitor ash handling and storage to prevent environmental release.
        6. Quantify economic and environmental benefits of valorization.
        7. Develop partnerships with end-users (farmers, construction firms).
        8. Track changes in ash quality with feedstock and process changes.
        9. Ensure compliance with local and national regulations.
        """,
        key_factors=["Ash composition", "Reuse options", "Regulatory limits", "End-user partnerships", "Environmental risk"],
        primary_authority=["IEA Bioenergy Task 36", "US EPA", "EU Waste Framework Directive"],
        burden_holder="Plant operator",
        adversary_position="Landfilling is the only safe option for all biomass ash.",
        counter_arguments=[
            "Many ashes are suitable for beneficial use.",
            "Landfilling increases costs and environmental impact.",
            "Valorization can generate revenue and reduce waste."
        ],
        resolution_strategy="Characterize ash and pursue reuse pathways where feasible.",
        entity_scope="Biomass plant operators, waste managers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 36 Ash Management Reports"
    ),
    DoctrineBlock(
        topic="Biomethane Grid Injection Standards",
        keywords=["biomethane", "grid injection", "standards", "pipeline", "quality"],
        conclusion_template="Biomethane must meet stringent pipeline quality standards for grid injection, requiring comprehensive upgrading and monitoring.",
        reasoning_framework="""
        1. Identify applicable pipeline quality standards (e.g., DVGW G262, CEN EN 16723).
        2. Analyze biomethane for CH4, CO2, H2S, O2, siloxanes, and water.
        3. Select upgrading and polishing technologies to meet all specifications.
        4. Implement continuous monitoring and control systems.
        5. Coordinate with grid operator for interconnection and metering.
        6. Address odorization and pressure requirements.
        7. Ensure traceability and documentation for regulatory compliance.
        8. Plan for contingency in case of off-spec gas.
        9. Review and update procedures as standards evolve.
        """,
        key_factors=["Quality standards", "Upgrading technology", "Monitoring", "Grid operator coordination", "Compliance"],
        primary_authority=["DVGW G262", "CEN EN 16723", "US EPA"],
        burden_holder="Biogas plant operator",
        adversary_position="Partial upgrading is sufficient for most grid injection applications.",
        counter_arguments=[
            "Non-compliance can result in grid access denial and penalties.",
            "Trace contaminants can damage pipeline infrastructure.",
            "Continuous monitoring is required by most operators."
        ],
        resolution_strategy="Design upgrading and QA/QC to exceed minimum standards.",
        entity_scope="Biomethane producers, pipeline operators",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CEN EN 16723-1:2016"
    ),
    DoctrineBlock(
        topic="Sustainable Biomass Certification Schemes",
        keywords=["sustainability", "biomass", "certification", "ISCC", "RSB", "traceability"],
        conclusion_template="Sustainable biomass supply chains require third-party certification and traceability to meet regulatory and market requirements.",
        reasoning_framework="""
        1. Identify applicable certification schemes (ISCC, RSB, FSC, SBP).
        2. Map supply chain actors and traceability requirements.
        3. Implement chain-of-custody and mass balance systems.
        4. Conduct risk assessment for land use change and social impacts.
        5. Audit suppliers and maintain documentation.
        6. Integrate certification with procurement and logistics.
        7. Address non-conformities and continuous improvement.
        8. Communicate certification status to stakeholders.
        9. Monitor evolving regulatory requirements.
        """,
        key_factors=["Certification scheme", "Traceability", "Risk assessment", "Auditing", "Stakeholder communication"],
        primary_authority=["ISCC", "RSB", "EU RED II"],
        burden_holder="Feedstock supplier",
        adversary_position="Self-declaration is sufficient for sustainability claims.",
        counter_arguments=[
            "Third-party certification is required by most regulators and buyers.",
            "Traceability prevents fraud and ensures compliance.",
            "Certification improves market access and reputation."
        ],
        resolution_strategy="Adopt recognized certification and integrate with supply chain management.",
        entity_scope="Biomass suppliers, project developers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EU RED II, ISCC System Documents"
    ),
    DoctrineBlock(
        topic="Digestate Management and Valorization",
        keywords=["digestate", "anaerobic digestion", "valorization", "nutrients", "fertilizer"],
        conclusion_template="Digestate should be managed as a valuable co-product, with nutrient recovery and application guided by agronomic and regulatory best practices.",
        reasoning_framework="""
        1. Characterize digestate for nutrient content and contaminants.
        2. Assess local agronomic needs and land application regulations.
        3. Implement separation (solid/liquid) and treatment as needed.
        4. Monitor application rates to prevent nutrient runoff.
        5. Explore advanced valorization (composting, drying, pelletizing).
        6. Develop partnerships with farmers and land managers.
        7. Track regulatory changes and market opportunities.
        8. Quantify environmental and economic benefits.
        9. Ensure documentation and traceability.
        """,
        key_factors=["Nutrient content", "Regulatory limits", "Application rates", "Valorization options", "Stakeholder engagement"],
        primary_authority=["IEA Bioenergy Task 37", "US EPA", "EU Nitrates Directive"],
        burden_holder="AD plant operator",
        adversary_position="Digestate is a waste and should be disposed of in landfill.",
        counter_arguments=[
            "Digestate contains valuable nutrients for agriculture.",
            "Land application is regulated and widely practiced.",
            "Advanced valorization creates additional revenue streams."
        ],
        resolution_strategy="Develop digestate management plan aligned with best practices and local needs.",
        entity_scope="AD plant operators, farmers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 37 Digestate Reports"
    ),
    DoctrineBlock(
        topic="Biomass Torrefaction and Densification",
        keywords=["torrefaction", "biomass", "densification", "pellets", "energy density"],
        conclusion_template="Torrefaction and densification improve biomass energy density and handling, enabling cost-effective long-distance transport and co-firing.",
        reasoning_framework="""
        1. Select suitable feedstock for torrefaction.
        2. Optimize torrefaction parameters (temperature, residence time).
        3. Densify torrefied biomass (pelletizing, briquetting).
        4. Measure energy density, hydrophobicity, and grindability.
        5. Assess logistics and storage benefits.
        6. Evaluate process economics and market demand.
        7. Compare with untreated biomass and fossil fuel benchmarks.
        8. Address emissions and process integration.
        9. Pilot and scale up based on performance data.
        """,
        key_factors=["Feedstock", "Process parameters", "Product quality", "Logistics", "Economics"],
        primary_authority=["IEA Bioenergy Task 32", "NREL"],
        burden_holder="Biomass processor",
        adversary_position="Torrefaction adds unnecessary cost and complexity.",
        counter_arguments=[
            "Improved energy density reduces transport cost.",
            "Hydrophobicity improves storage and handling.",
            "Market demand for high-quality pellets is growing."
        ],
        resolution_strategy="Conduct techno-economic analysis and market assessment.",
        entity_scope="Biomass processors, pellet producers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 32 Torrefaction Reports"
    ),
    DoctrineBlock(
        topic="Biogas Desulfurization Best Practices",
        keywords=["biogas", "desulfurization", "H2S removal", "iron sponge", "biological filter"],
        conclusion_template="H2S removal from biogas is essential for equipment protection and emissions compliance, with technology selection based on gas composition and scale.",
        reasoning_framework="""
        1. Measure H2S concentration in raw biogas.
        2. Select removal technology: iron sponge, activated carbon, biological filter, chemical scrubbing.
        3. Assess removal efficiency, OPEX, and maintenance.
        4. Monitor H2S breakthrough and replace/renew media as needed.
        5. Integrate with upstream and downstream processes.
        6. Ensure compliance with emissions and safety regulations.
        7. Quantify impact on biogas utilization equipment.
        8. Train operators on safe handling and disposal of spent media.
        9. Review and update practices as technology evolves.
        """,
        key_factors=["H2S concentration", "Removal technology", "OPEX", "Maintenance", "Compliance"],
        primary_authority=["IEA Bioenergy Task 37", "US EPA", "DVGW"],
        burden_holder="Biogas plant operator",
        adversary_position="H2S removal is unnecessary for small-scale systems.",
        counter_arguments=[
            "Even low H2S damages engines and catalysts.",
            "Emissions regulations apply to all scales.",
            "Low-cost options are available for small plants."
        ],
        resolution_strategy="Implement H2S removal as standard practice for all biogas systems.",
        entity_scope="Biogas plant operators, equipment vendors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 37 Desulfurization Reports"
    ),
    DoctrineBlock(
        topic="Biomass Gasification Tar Management",
        keywords=["gasification", "tar", "management", "catalytic reforming", "scrubbing"],
        conclusion_template="Effective tar management in biomass gasification is critical for syngas utilization, requiring integrated thermal, catalytic, and mechanical strategies.",
        reasoning_framework="""
        1. Characterize tar composition and loading in raw syngas.
        2. Optimize gasifier operating conditions to minimize tar formation.
        3. Implement primary measures (temperature, residence time, feedstock selection).
        4. Apply secondary measures: cyclones, scrubbers, catalytic reformers.
        5. Monitor tar levels and system performance.
        6. Evaluate impact on downstream equipment (engines, turbines, synthesis).
        7. Quantify OPEX and maintenance requirements.
        8. Train operators in tar management protocols.
        9. Update strategies as technology advances.
        """,
        key_factors=["Tar loading", "Gasifier operation", "Removal technologies", "OPEX", "Downstream impact"],
        primary_authority=["IEA Bioenergy Task 33", "NREL"],
        burden_holder="Gasification plant operator",
        adversary_position="Tar management is only necessary for large-scale gasifiers.",
        counter_arguments=[
            "Tar fouling affects all scales.",
            "Small-scale systems are more sensitive to tar.",
            "Integrated strategies improve reliability and economics."
        ],
        resolution_strategy="Adopt best practices for tar management at all scales.",
        entity_scope="Gasification plant operators, technology vendors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 33 Tar Management Reports"
    ),
    DoctrineBlock(
        topic="Biomass Harvesting and Field Drying",
        keywords=["biomass", "harvesting", "field drying", "moisture reduction", "logistics"],
        conclusion_template="Optimizing biomass harvesting and field drying reduces moisture content and logistics costs, improving conversion efficiency.",
        reasoning_framework="""
        1. Schedule harvesting for optimal weather and crop maturity.
        2. Implement field drying protocols (windrowing, turning).
        3. Monitor moisture content and target <20% for most applications.
        4. Minimize soil contamination during collection.
        5. Coordinate with logistics for timely transport.
        6. Quantify impact on energy density and storage stability.
        7. Evaluate trade-offs with nutrient removal and soil health.
        8. Train operators in best practices.
        9. Adapt protocols for regional climate and crop type.
        """,
        key_factors=["Harvest timing", "Field drying", "Moisture content", "Logistics", "Soil health"],
        primary_authority=["US DOE", "IEA Bioenergy Task 43"],
        burden_holder="Feedstock supplier",
        adversary_position="Field drying is unnecessary with modern conversion technologies.",
        counter_arguments=[
            "High moisture increases transport and conversion costs.",
            "Field drying is low-cost and effective.",
            "Moisture reduction improves storage and process efficiency."
        ],
        resolution_strategy="Incorporate field drying into standard harvesting protocols.",
        entity_scope="Biomass suppliers, logistics operators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 43 Harvesting Reports"
    ),
    DoctrineBlock(
        topic="Biomass Pellet Quality Standards",
        keywords=["biomass", "pellets", "quality standards", "ENplus", "ISO 17225"],
        conclusion_template="Biomass pellets must meet recognized quality standards for durability, ash, and energy content to ensure market acceptance and performance.",
        reasoning_framework="""
        1. Produce pellets from clean, homogeneous feedstock.
        2. Test for moisture, ash, durability, fines, and energy content.
        3. Certify product to ENplus, ISO 17225, or equivalent standards.
        4. Monitor process control and adjust as needed.
        5. Document quality control and traceability.
        6. Address customer feedback and complaints.
        7. Update procedures as standards evolve.
        8. Train staff in QA/QC protocols.
        9. Communicate certification to buyers.
        """,
        key_factors=["Feedstock quality", "Testing", "Certification", "Process control", "Customer communication"],
        primary_authority=["ENplus", "ISO 17225", "IEA Bioenergy Task 32"],
        burden_holder="Pellet producer",
        adversary_position="Quality certification is unnecessary for domestic markets.",
        counter_arguments=[
            "Certification is required for many export markets.",
            "Quality standards ensure consistent performance.",
            "Certification improves reputation and reduces complaints."
        ],
        resolution_strategy="Certify all pellets to recognized standards.",
        entity_scope="Pellet producers, traders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ENplus Handbook, ISO 17225"
    ),
    DoctrineBlock(
        topic="Biogas Leak Detection and Mitigation",
        keywords=["biogas", "leak detection", "methane emissions", "fugitive emissions", "infrared camera"],
        conclusion_template="Routine leak detection and repair is essential to minimize fugitive methane emissions and regulatory risk at biogas facilities.",
        reasoning_framework="""
        1. Survey facility with infrared camera or portable gas detector.
        2. Identify and quantify leaks at all process stages.
        3. Prioritize repairs based on leak size and location.
        4. Implement regular inspection and maintenance schedule.
        5. Train staff in leak detection and repair protocols.
        6. Document findings and corrective actions.
        7. Report emissions as required by regulators.
        8. Evaluate technology upgrades for leak prevention.
        9. Review and update protocols as best practices evolve.
        """,
        key_factors=["Detection technology", "Repair protocols", "Training", "Documentation", "Regulatory reporting"],
        primary_authority=["US EPA", "IEA Bioenergy Task 37", "GHG Protocol"],
        burden_holder="Facility operator",
        adversary_position="Leak detection is only necessary for large facilities.",
        counter_arguments=[
            "Small leaks can have large cumulative impact.",
            "Regulations increasingly require leak detection at all scales.",
            "Routine LDAR reduces emissions and improves safety."
        ],
        resolution_strategy="Implement LDAR program for all biogas facilities.",
        entity_scope="Biogas plant operators, maintenance staff",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="US EPA Methane Challenge Program"
    ),
    DoctrineBlock(
        topic="Biomass Preprocessing for Thermochemical Conversion",
        keywords=["biomass", "preprocessing", "thermochemical", "size reduction", "drying"],
        conclusion_template="Preprocessing (size reduction, drying) is critical for efficient thermochemical conversion, impacting reactor performance and product quality.",
        reasoning_framework="""
        1. Analyze feedstock particle size and moisture.
        2. Select preprocessing steps: chipping, milling, drying.
        3. Target particle size and moisture for specific reactor type.
        4. Monitor energy use and cost of preprocessing.
        5. Assess impact on conversion efficiency and product yield.
        6. Integrate preprocessing with logistics and storage.
        7. Evaluate trade-offs with feedstock cost and availability.
        8. Pilot and optimize preprocessing line.
        9. Update protocols as technology advances.
        """,
        key_factors=["Particle size", "Moisture", "Preprocessing cost", "Reactor requirements", "Integration"],
        primary_authority=["NREL", "IEA Bioenergy Task 33"],
        burden_holder="Feedstock processor",
        adversary_position="Preprocessing is unnecessary for most thermochemical systems.",
        counter_arguments=[
            "Uniform feedstock improves reactor operation and yield.",
            "Drying reduces tar and increases energy density.",
            "Preprocessing can be integrated with logistics."
        ],
        resolution_strategy="Design preprocessing to match reactor and feedstock needs.",
        entity_scope="Feedstock processors, plant operators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL Thermochemical Preprocessing Reports"
    ),
    DoctrineBlock(
        topic="Biogas Digestate Pathogen Reduction",
        keywords=["digestate", "pathogen reduction", "hygienization", "pasteurization", "regulation"],
        conclusion_template="Digestate must undergo pathogen reduction (e.g., pasteurization) before land application to meet health and regulatory standards.",
        reasoning_framework="""
        1. Test digestate for pathogen indicators (E. coli, Salmonella).
        2. Select pathogen reduction method (pasteurization, composting, ammonia treatment).
        3. Monitor process parameters (temperature, time, pH).
        4. Validate reduction with post-treatment testing.
        5. Document compliance with local and national regulations.
        6. Train staff in hygienization protocols.
        7. Communicate safety to end-users (farmers, regulators).
        8. Update procedures as standards evolve.
        9. Track emerging research on pathogen risks.
        """,
        key_factors=["Pathogen testing", "Reduction method", "Process control", "Documentation", "Regulatory"],
        primary_authority=["EU Animal By-Products Regulation", "US EPA", "IEA Bioenergy Task 37"],
        burden_holder="AD plant operator",
        adversary_position="Pathogen reduction is unnecessary if digestate is land-applied locally.",
        counter_arguments=[
            "Pathogen risks exist regardless of application distance.",
            "Regulations require pathogen reduction for most uses.",
            "Best practices protect public health and market access."
        ],
        resolution_strategy="Implement and document pathogen reduction for all digestate.",
        entity_scope="AD plant operators, farmers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EU Regulation (EC) No 1069/2009"
    ),
    DoctrineBlock(
        topic="Biomass Co-product Valorization",
        keywords=["biomass", "co-products", "valorization", "biochar", "lignin", "market"],
        conclusion_template="Maximizing co-product valorization (biochar, lignin, nutrients) improves project economics and sustainability.",
        reasoning_framework="""
        1. Identify potential co-products from conversion process.
        2. Characterize quality and market demand for each co-product.
        3. Develop separation and upgrading processes.
        4. Quantify economic contribution and environmental benefits.
        5. Engage with end-users and develop offtake agreements.
        6. Monitor regulatory requirements and incentives.
        7. Integrate co-product streams with main process.
        8. Pilot and scale up based on market feedback.
        9. Update strategy as markets and technologies evolve.
        """,
        key_factors=["Co-product identification", "Market demand", "Separation/upgrading", "Economics", "Regulatory"],
        primary_authority=["NREL", "IEA Bioenergy Task 42"],
        burden_holder="Project developer",
        adversary_position="Co-product valorization distracts from main product focus.",
        counter_arguments=[
            "Co-products can provide significant revenue.",
            "Valorization improves sustainability and reduces waste.",
            "Integrated approach enhances project resilience."
        ],
        resolution_strategy="Develop co-product valorization plan as part of project design.",
        entity_scope="Bioenergy project developers, technology vendors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 42 Biorefining Reports"
    ),
    DoctrineBlock(
        topic="Biomass Storage Fire Risk Management",
        keywords=["biomass", "storage", "fire risk", "self-heating", "monitoring"],
        conclusion_template="Biomass storage systems must be designed and monitored to minimize fire risk from self-heating and microbial activity.",
        reasoning_framework="""
        1. Select storage method (pile, bunker, silo) appropriate for feedstock and climate.
        2. Monitor temperature and moisture in storage.
        3. Implement pile size and shape guidelines to prevent hotspots.
        4. Control moisture to <20% where possible.
        5. Train staff in fire prevention and emergency response.
        6. Install fire detection and suppression systems.
        7. Document incidents and corrective actions.
        8. Review and update protocols as best practices evolve.
        9. Engage with insurers and regulators for compliance.
        """,
        key_factors=["Storage method", "Temperature/moisture monitoring", "Pile management", "Training", "Fire systems"],
        primary_authority=["NFPA", "IEA Bioenergy Task 32", "US DOE"],
        burden_holder="Storage operator",
        adversary_position="Fire risk is negligible with modern storage systems.",
        counter_arguments=[
            "Self-heating fires are a documented risk.",
            "Monitoring and management reduce incidents.",
            "Insurance and regulatory compliance require best practices."
        ],
        resolution_strategy="Implement fire risk management as standard operating procedure.",
        entity_scope="Biomass storage operators, insurers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NFPA 850, IEA Bioenergy Task 32 Storage Reports"
    ),
    DoctrineBlock(
        topic="Biomass Feedstock Blending Strategies",
        keywords=["biomass", "feedstock blending", "multi-feedstock", "process optimization"],
        conclusion_template="Blending multiple biomass feedstocks can optimize process performance and economics, but requires careful characterization and control.",
        reasoning_framework="""
        1. Characterize each feedstock for energy, ash, moisture, and contaminants.
        2. Model blend ratios for target process performance.
        3. Monitor feedstock variability and adjust blends as needed.
        4. Evaluate impact on conversion efficiency, emissions, and product quality.
        5. Integrate blending with logistics and storage.
        6. Document blend recipes and performance data.
        7. Train staff in blending protocols.
        8. Pilot and scale up blending strategies.
        9. Update approach as feedstock supply and process needs change.
        """,
        key_factors=["Feedstock characterization", "Blend modeling", "Process performance", "Documentation", "Training"],
        primary_authority=["NREL", "IEA Bioenergy Task 32"],
        burden_holder="Feedstock manager",
        adversary_position="Blending increases complexity without significant benefit.",
        counter_arguments=[
            "Blending can reduce cost and improve reliability.",
            "Optimized blends improve process stability.",
            "Documentation and control mitigate complexity."
        ],
        resolution_strategy="Develop blending protocols and monitor performance.",
        entity_scope="Feedstock managers, plant operators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NREL Biomass Blending Reports"
    ),
    DoctrineBlock(
        topic="Biomass Moisture Measurement and Control",
        keywords=["biomass", "moisture measurement", "control", "process efficiency"],
        conclusion_template="Accurate moisture measurement and control are essential for efficient biomass conversion and logistics.",
        reasoning_framework="""
        1. Select appropriate moisture measurement technology (oven-drying, NIR, capacitance).
        2. Implement routine sampling and testing protocols.
        3. Integrate moisture data with process control systems.
        4. Adjust drying and storage protocols based on measurements.
        5. Quantify impact on energy density, transport, and conversion.
        6. Train staff in measurement and control procedures.
        7. Document results and corrective actions.
        8. Update protocols as technology advances.
        9. Communicate importance of moisture control to all stakeholders.
        """,
        key_factors=["Measurement technology", "Sampling protocols", "Process control", "Training", "Documentation"],
        primary_authority=["NREL", "IEA Bioenergy Task 32"],
        burden_holder="Feedstock supplier",
        adversary_position="Moisture measurement is unnecessary with modern conversion systems.",
        counter_arguments=[
            "Moisture affects energy density and process efficiency.",
            "Measurement enables process optimization.",
            "Best practices require routine moisture control."
        ],
        resolution_strategy="Implement moisture measurement and control as standard practice.",
        entity_scope="Feedstock suppliers, process operators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL Biomass Moisture Reports"
    ),
    DoctrineBlock(
        topic="Biogas Plant Odor Management",
        keywords=["biogas", "odor management", "emissions", "community relations"],
        conclusion_template="Odor management is critical for biogas plant acceptance, requiring source control, capture, and treatment technologies.",
        reasoning_framework="""
        1. Identify odor sources (feedstock handling, digestate, leaks).
        2. Implement source control (enclosed handling, rapid processing).
        3. Capture odorous air and treat with biofilters, scrubbers, or thermal oxidation.
        4. Monitor odor emissions and community feedback.
        5. Train staff in odor management protocols.
        6. Document complaints and corrective actions.
        7. Engage with community and regulators proactively.
        8. Update odor management plan as needed.
        9. Integrate odor management with overall plant operations.
        """,
        key_factors=["Source control", "Capture/treatment", "Monitoring", "Community engagement", "Documentation"],
        primary_authority=["US EPA", "IEA Bioenergy Task 37"],
        burden_holder="Plant operator",
        adversary_position="Odor management is unnecessary in rural areas.",
        counter_arguments=[
            "Odor complaints can lead to shutdowns.",
            "Best practices improve community relations.",
            "Odor management is required by many permits."
        ],
        resolution_strategy="Implement odor management as part of standard operations.",
        entity_scope="Biogas plant operators, community relations staff",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IEA Bioenergy Task 37 Odor Management Reports"
    ),
    DoctrineBlock(
        topic="Biomass Conversion Plant Water Management",
        keywords=["biomass", "water management", "conversion plant", "wastewater"],
        conclusion_template="Water management in biomass conversion plants must minimize consumption, recycle streams, and ensure compliant wastewater discharge.",
        reasoning_framework="""
        1. Map water use and discharge points in the plant.
        2. Implement water-saving and recycling technologies.
        3. Monitor water quality and quantity.
        4. Treat wastewater to meet discharge standards.
        5. Quantify water footprint and report as required.
        6. Train staff in water management protocols.
        7. Document water use, recycling, and discharge data.
        8. Engage with regulators and community on water issues.
        9. Update water management plan as technology and regulations evolve.
        """,
        key_factors=["Water mapping", "Recycling", "Wastewater treatment", "Monitoring", "Reporting"],
        primary_authority=["US EPA", "NREL", "IEA Bioenergy Task 42"],
        burden_holder="Plant operator",
        adversary_position="Water management is a minor issue for most biomass plants.",
        counter_arguments=[
            "Water use can be significant and regulated.",
            "Recycling reduces cost and environmental impact.",
            "Non-compliance can halt operations."
        ],
        resolution_strategy="Develop and implement comprehensive water management plan.",
        entity_scope="Biomass plant operators, environmental managers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL Water Management Reports"
    ),
    DoctrineBlock(
        topic="Biomass Conversion Plant Safety Management",
        keywords=["biomass", "safety management", "conversion plant", "hazard analysis"],
        conclusion_template="Comprehensive safety management systems are essential for biomass conversion plants to prevent accidents and ensure regulatory compliance.",
        reasoning_framework="""
        1. Conduct hazard identification and risk assessment (HAZOP, FMEA).
        2. Implement engineering and administrative controls.
        3. Train staff in safety protocols and emergency response.
        4. Monitor and report incidents and near-misses.
        5. Maintain safety documentation and records.
        6. Engage with regulators and insurers.
        7. Update safety management plan as processes and regulations change.
        8. Foster a safety culture through leadership and incentives.
        9. Review and audit safety performance regularly.
        """,
        key_factors=["Hazard analysis", "Controls", "Training", "Documentation", "Culture"],
        primary_authority=["OSHA", "NFPA", "NREL"],
        burden_holder="Plant operator",
        adversary_position="Safety management adds unnecessary cost and bureaucracy.",
        counter_arguments=[
            "Accidents can have severe human and financial consequences.",
            "Safety management is required by law.",
            "Best practices improve performance and reputation."
        ],
        resolution_strategy="Implement and maintain robust safety management system.",
        entity_scope="Biomass plant operators, safety managers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA PSM, NFPA 850"
    ),
    DoctrineBlock(
        topic="Biomass Conversion Plant Air Emissions Control",
        keywords=["biomass", "air emissions", "control", "regulation", "particulate"],
        conclusion_template="Air emissions from biomass conversion plants must be controlled and monitored to meet regulatory and community standards.",
        reasoning_framework="""
        1. Identify all emission sources (combustion, process vents, storage).
        2. Select appropriate control technologies (cyclones, ESP, baghouse, scrubbers).
        3. Monitor emissions continuously or periodically as required.
        4. Maintain records and report to regulators.
        5. Engage with community on air quality concerns.
        6. Train staff in emissions control and monitoring.
        7. Update control systems as regulations and technology evolve.
        8. Quantify emissions for GHG and air quality reporting.
        9. Integrate emissions control with overall plant operations.
        """,
        key_factors=["Emission sources", "Control technology", "Monitoring", "Reporting", "Community engagement"],
        primary_authority=["US EPA", "NREL", "IEA Bioenergy Task 32"],
        burden_holder="Plant operator",
        adversary_position="Air emissions from biomass are negligible and unregulated.",
        counter_arguments=[
            "Emissions are regulated and monitored.",
            "Control technologies are effective and required.",
            "Community concerns must be addressed."
        ],
        resolution_strategy="Implement emissions control and monitoring as standard practice.",
        entity_scope="Biomass plant operators, environmental managers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="US EPA MACT, NREL Air Emissions Reports"
    ),
    DoctrineBlock(
        topic="Biomass Plant Noise Management",
        keywords=["biomass", "noise management", "community", "regulation"],
        conclusion_template="Noise management is essential for community acceptance of biomass plants, requiring monitoring, mitigation, and stakeholder engagement.",
        reasoning_framework="""
        1. Identify noise sources (equipment, transport, operations).
        2. Measure baseline and operational noise levels.
        3. Implement mitigation (enclosures, barriers, scheduling).
        4. Monitor noise and respond to complaints.
        5. Train staff in noise management protocols.
        6. Document noise levels and corrective actions.
        7. Engage with community and regulators.
        8. Update noise management plan as needed.
        9. Integrate noise management with overall plant operations.
        """,
        key_factors=["Noise sources", "Measurement", "Mitigation", "Community engagement", "Documentation"],
        primary_authority=["US EPA", "NREL"],
        burden_holder="Plant operator",
        adversary_position="Noise is not a significant issue for biomass plants.",
        counter_arguments=[
            "Noise complaints can lead to operational restrictions.",
            "Mitigation is often low-cost and effective.",
            "Community engagement improves acceptance."
        ],
        resolution_strategy="Implement noise management as part of standard operations.",
        entity_scope="Biomass plant operators, community relations staff",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NREL Noise Management Reports"
    ),
    DoctrineBlock(
        topic="Biomass Conversion Plant Data Management",
        keywords=["biomass", "data management", "plant operations", "monitoring"],
        conclusion_template="Robust data management systems are required for process optimization, regulatory compliance, and continuous improvement in biomass plants.",
        reasoning_framework="""
        1. Identify key process and compliance data streams.
        2. Implement automated data collection and storage.
        3. Ensure data integrity, security, and accessibility.
        4. Analyze data for process optimization and troubleshooting.
        5. Report data as required by regulators and stakeholders.
        6. Train staff in data management protocols.
        7. Update data management systems as technology evolves.
        8. Integrate data management with plant control systems.
        9. Foster a culture of data-driven decision making.
        """,
        key_factors=["Data collection", "Integrity", "Analysis", "Reporting", "Training"],
        primary_authority=["NREL", "US DOE"],
        burden_holder="Plant operator",
        adversary_position="Data management is only necessary for large-scale plants.",
        counter_arguments=[
            "Data is essential for all scales of operation.",
            "Automated systems are increasingly affordable.",
            "Data-driven management improves performance."
        ],
        resolution_strategy="Implement data management for all plant operations.",
        entity_scope="Biomass plant operators, IT staff",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL Data Management Reports"
    ),
    DoctrineBlock(
        topic="Biomass Plant Staff Training and Certification",
        keywords=["biomass", "staff training", "certification", "operations"],
        conclusion_template="Ongoing staff training and certification are essential for safe, efficient, and compliant biomass plant operations.",
        reasoning_framework="""
        1. Identify required competencies for all staff roles.
        2. Develop and implement training programs.
        3. Certify staff as required by regulation and best practice.
        4. Monitor training effectiveness and update as needed.
        5. Document training and certification records.
        6. Foster a culture of continuous learning.
        7. Engage with external training providers as appropriate.
        8. Integrate training with safety and quality management systems.
        9. Review and update training programs regularly.
        """,
        key_factors=["Competency identification", "Training programs", "Certification", "Documentation", "Continuous improvement"],
        primary_authority=["OSHA", "NREL"],
        burden_holder="Plant operator",
        adversary_position="Training is only necessary for new staff.",
        counter_arguments=[
            "Ongoing training is required for safety and compliance.",
            "Continuous improvement improves performance.",
            "Certification is required by many regulators and insurers."
        ],
        resolution_strategy="Implement ongoing training and certification for all staff.",
        entity_scope="Biomass plant operators, HR managers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Training Requirements"
    ),
    DoctrineBlock(
        topic="Biomass Plant Emergency Response Planning",
        keywords=["biomass", "emergency response", "planning", "safety"],
        conclusion_template="Comprehensive emergency response planning is required for all biomass plants to protect staff, community, and assets.",
        reasoning_framework="""
        1. Identify potential emergency scenarios (fire, spill, explosion, weather).
        2. Develop and document response plans for each scenario.
        3. Train staff in emergency response protocols.
        4. Coordinate with local emergency services.
        5. Conduct regular drills and exercises.
        6. Maintain emergency equipment and supplies.
        7. Review and update plans as risks and regulations change.
        8. Communicate plans to all stakeholders.
        9. Document incidents and lessons learned.
        """,
        key_factors=["Scenario identification", "Response planning", "Training", "Coordination", "Documentation"],
        primary_authority=["NFPA", "OSHA", "NREL"],
        burden_holder="Plant operator",
        adversary_position="Emergency planning is unnecessary for modern plants.",
        counter_arguments=[
            "Emergencies can occur at any plant.",
            "Planning reduces risk and improves response.",
            "Regulations require emergency planning."
        ],
        resolution_strategy="Develop, implement, and update emergency response plans.",
        entity_scope="Biomass plant operators, safety managers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NFPA 850, OSHA Emergency Action Plans"
    ),
    DoctrineBlock(
        topic="Biomass Conversion Plant Community Engagement",
        keywords=["biomass", "community engagement", "stakeholder", "acceptance"],
        conclusion_template="Proactive community engagement is essential for biomass plant acceptance and long-term success.",
        reasoning_framework="""
        1. Identify community stakeholders and concerns.
        2. Develop and implement engagement plan (meetings, tours, information).
        3. Monitor and respond to feedback and complaints.
        4. Communicate plant benefits and performance transparently.
        5. Involve community in monitoring and improvement initiatives.
        6. Document engagement activities and outcomes.
        7. Update engagement plan as community needs evolve.
        8. Integrate engagement with regulatory and permitting processes.
        9. Foster long-term relationships and trust.
        """,
        key_factors=["Stakeholder identification", "Engagement plan", "Feedback", "Communication", "Documentation"],
        primary_authority=["NREL", "US DOE"],
        burden_holder="Plant operator",
        adversary_position="Community engagement is unnecessary if plant is compliant.",
        counter_arguments=[
            "Community acceptance is critical for project success.",
            "Engagement reduces risk of opposition and delays.",
            "Transparency builds trust and reputation."
        ],
        resolution_strategy="Implement and maintain proactive community engagement.",
        entity_scope="Biomass plant operators, community relations staff",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL Community Engagement Reports"
    ),
    DoctrineBlock(
        topic="Biomass Plant Permitting and Regulatory Compliance",
        keywords=["biomass", "permitting", "regulatory compliance", "environmental"],
        conclusion_template="Comprehensive permitting and regulatory compliance are prerequisites for biomass plant construction and operation.",
        reasoning_framework="""
        1. Identify all applicable permits and regulations (air, water, waste, safety).
        2. Develop permitting plan and timeline.
        3. Prepare and submit permit applications with supporting documentation.
        4. Engage with regulators and respond to information requests.
        5. Monitor compliance and maintain records.
        6. Train staff in compliance protocols.
        7. Update permits and plans as regulations change.
        8. Document compliance activities and audits.
        9. Integrate compliance with overall plant management.
        """,
        key_factors=["Permit identification", "Application", "Regulator engagement", "Monitoring", "Documentation"],
        primary_authority=["US EPA", "NREL", "State/Local Agencies"],
        burden_holder="Plant developer/operator",
        adversary_position="Permitting is a one-time activity and not an ongoing concern.",
        counter_arguments=[
            "Regulations and permits change over time.",
            "Ongoing compliance is required for continued operation.",
            "Non-compliance can halt operations and incur penalties."
        ],
        resolution_strategy="Develop and maintain comprehensive compliance management system.",
        entity_scope="Biomass plant developers, operators",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="US EPA, NREL Permitting Guides"
    ),
    DoctrineBlock(
        topic="Biomass Plant Financial Modeling and Project Finance",
        keywords=["biomass", "financial modeling", "project finance", "CAPEX", "OPEX"],
        conclusion_template="Robust financial modeling and access to project finance are essential for successful biomass plant development.",
        reasoning_framework="""
        1. Develop detailed CAPEX and OPEX estimates.
        2. Model revenue streams (energy, co-products, incentives).
        3. Conduct sensitivity analysis on key variables.
        4. Structure project finance (debt, equity, grants).
        5. Engage with lenders and investors.
        6. Document financial assumptions and risks.
        7. Update model as project details evolve.
        8. Monitor financial performance post-commissioning.
        9. Integrate financial modeling with overall project management.
        """,
        key_factors=["CAPEX/OPEX", "Revenue", "Sensitivity analysis", "Finance structure", "Risk documentation"],
        primary_authority=["NREL", "US DOE", "IEA Bioenergy Task 42"],
        burden_holder="Project developer",
        adversary_position="Simple payback is sufficient for financial analysis.",
        counter_arguments=[
            "Project finance requires detailed modeling.",
            "Sensitivity analysis identifies key risks.",
            "Lenders and investors require robust documentation."
        ],
        resolution_strategy="Develop and maintain robust financial model for all projects.",
        entity_scope="Project developers, finance teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NREL Project Finance Guides"
    ),
    DoctrineBlock(
        topic="Biomass Plant Technology Selection and Due Diligence",
        keywords=["biomass", "technology selection", "due diligence", "proven technology"],
        conclusion_template="Technology selection and due diligence are critical to minimize technical risk and ensure project bankability.",
        reasoning_framework="""
        1. Identify proven technologies with commercial track record.
        2. Evaluate technology fit for feedstock, scale, and products.
        3. Conduct technical and financial due diligence.
        4. Engage independent experts for validation.
        5. Review vendor references and performance data.
        6. Quantify technical risks and mitigation strategies.
        7. Document due diligence findings.
        8. Update selection as project details evolve.
        9. Integrate technology selection with project finance and permitting.
        """,
        key_factors=["Proven technology", "Fit for purpose", "Due diligence", "Risk mitigation", "Documentation"],
        primary_authority=["NREL", "US DOE", "IEA Bioenergy Task 42"],
        burden_holder="Project developer",
        adversary_position="Novel technologies should be prioritized for higher returns.",
        counter_arguments=[
            "Proven technologies reduce risk and improve financeability.",
            "Due diligence identifies and mitigates risks.",
            "Lenders and insurers require validation."
        ],
        resolution_strategy="Prioritize proven technologies and conduct thorough due diligence.",
        entity_scope="Project developers, lenders, insurers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NREL Technology Validation Guides"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (query_lower in doctrine.topic.lower() or
            any(query_lower in kw.lower() for kw in doctrine.keywords) or
            query_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]