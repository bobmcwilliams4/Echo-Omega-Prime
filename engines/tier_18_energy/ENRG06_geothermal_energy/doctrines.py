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
        topic="USGS Geothermal Resource Classification System",
        keywords=[
            "resource classification", "USGS", "geothermal reserves", "resource assessment",
            "inferred resource", "indicated resource", "measured resource", "contingent resource"
        ],
        conclusion_template="Geothermal resources must be classified according to USGS standards to ensure consistency in reporting and project evaluation.",
        reasoning_framework="""
            The USGS Geothermal Resource Classification System provides a standardized approach to categorize geothermal resources based on geological confidence and economic viability. The classification distinguishes between inferred, indicated, and measured resources, as well as contingent and prospective resources. This framework ensures that resource estimates are transparent and comparable across projects. The classification process involves integrating geological, geophysical, and engineering data to assign confidence levels. Economic factors, such as proximity to infrastructure and market conditions, are also considered. The system is widely recognized by regulatory bodies and financial institutions, making it essential for project financing and permitting. Adherence to this system reduces the risk of overestimating resource potential and supports responsible development.
        """,
        key_factors=[
            "Geological confidence", "Data quality", "Economic viability", "Regulatory requirements", "Project stage"
        ],
        primary_authority=["USGS Circular 790", "SPE PRMS", "DOE Geothermal Technologies Office"],
        burden_holder="Project developer",
        adversary_position="Resource classification can be subjective and may overstate reserves.",
        counter_arguments=[
            "USGS system is internationally recognized and peer-reviewed.",
            "Independent audits can validate classifications.",
            "Transparency in reporting mitigates subjectivity."
        ],
        resolution_strategy="Require third-party review and adherence to USGS definitions in all resource reporting.",
        entity_scope="All geothermal resource assessments in the US and projects seeking international financing.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="USGS Circular 790 (1978); SPE PRMS (2018)"
    ),
    DoctrineBlock(
        topic="Geothermal Gradient and Heat Flow Assessment",
        keywords=[
            "heat flow", "geothermal gradient", "temperature-depth profile", "thermal conductivity",
            "resource potential", "exploration"
        ],
        conclusion_template="Accurate geothermal gradient and heat flow assessments are fundamental for resource evaluation and well targeting.",
        reasoning_framework="""
            Geothermal gradient and heat flow measurements are critical for estimating subsurface temperatures and identifying viable geothermal reservoirs. The assessment involves collecting temperature logs from exploration wells and integrating thermal conductivity data from core samples. Regional geological context, such as tectonic setting and lithology, must be considered to interpret anomalies. High-quality data reduce uncertainty in resource estimates and guide well placement. The methodology should follow ASTM and ISO standards for temperature logging and heat flow calculation. Data should be corrected for drilling disturbances and validated through repeat measurements. The results inform both resource classification and reservoir modeling, impacting project economics and feasibility.
        """,
        key_factors=[
            "Temperature log accuracy", "Thermal conductivity data", "Geological context", "Data correction methods"
        ],
        primary_authority=["ASTM D5334", "ISO 17660", "USGS Open-File Reports"],
        burden_holder="Exploration geologist",
        adversary_position="Heat flow data are often sparse and may not represent the entire field.",
        counter_arguments=[
            "Multiple wells and surface heat flow surveys can improve spatial coverage.",
            "Geostatistical methods can interpolate between data points.",
            "Uncertainty quantification is standard practice."
        ],
        resolution_strategy="Mandate minimum data density and uncertainty reporting in all assessments.",
        entity_scope="All geothermal exploration projects and resource assessments.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM D5334-14; USGS OFR 2013-1240"
    ),
    DoctrineBlock(
        topic="Flash Steam vs Binary Cycle Technology Selection",
        keywords=[
            "flash steam", "binary cycle", "technology selection", "enthalpy", "power plant design",
            "resource temperature"
        ],
        conclusion_template="Selection between flash steam and binary cycle technology must be based on reservoir temperature, fluid chemistry, and project economics.",
        reasoning_framework="""
            Flash steam plants are optimal for high-enthalpy resources (typically >180°C), where geothermal fluids can be flashed to steam for direct turbine drive. Binary cycle plants, using Organic Rankine Cycle (ORC) or Kalina Cycle, are suited for moderate- to low-enthalpy resources (typically 90–180°C), transferring heat to a secondary working fluid. The decision framework involves evaluating reservoir temperature, non-condensable gas content, scaling potential, and environmental constraints. Flash plants offer higher efficiency at high temperatures but require robust scaling and corrosion management. Binary plants have lower environmental impact and can utilize a broader range of resources but at higher capital cost per MW. Lifecycle cost analysis and regulatory compliance are essential in technology selection.
        """,
        key_factors=[
            "Reservoir temperature", "Fluid chemistry", "Non-condensable gas content", "Capital and O&M costs"
        ],
        primary_authority=["DOE Geothermal Technologies Office", "IEA Geothermal Handbook"],
        burden_holder="Project engineer",
        adversary_position="Binary cycle plants are more expensive and less efficient than flash plants.",
        counter_arguments=[
            "Binary plants enable utilization of lower-temperature resources.",
            "Environmental permitting is often easier for binary plants.",
            "Advances in ORC technology are improving efficiency."
        ],
        resolution_strategy="Conduct comparative techno-economic and environmental analysis for all candidate technologies.",
        entity_scope="All geothermal power plant developments.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="DOE GTO Technology Pathways (2020); IEA Geothermal Handbook (2010)"
    ),
    DoctrineBlock(
        topic="Enhanced Geothermal Systems (EGS) Hydraulic Stimulation",
        keywords=[
            "EGS", "hydraulic stimulation", "reservoir enhancement", "fracturing", "microseismic monitoring"
        ],
        conclusion_template="Hydraulic stimulation in EGS must follow best practices for induced seismicity mitigation and reservoir sustainability.",
        reasoning_framework="""
            Enhanced Geothermal Systems (EGS) rely on hydraulic stimulation to increase permeability in low-porosity rocks. The process involves injecting fluid at high pressure to create or enhance fracture networks, monitored by microseismic arrays. The framework requires pre-stimulation risk assessment, real-time seismic monitoring, and adaptive traffic light protocols to manage induced seismicity. Stimulation parameters (rate, pressure, volume) must be optimized to maximize reservoir connectivity while minimizing seismic risk. Regulatory compliance with local and national seismicity guidelines is mandatory. Post-stimulation evaluation includes tracer testing and flow logging to assess reservoir response. Long-term monitoring ensures sustainability and public acceptance.
        """,
        key_factors=[
            "Seismic risk", "Stimulation parameters", "Regulatory compliance", "Reservoir response"
        ],
        primary_authority=["DOE EGS Best Practices", "ISRM Guidelines", "USGS Induced Seismicity Protocols"],
        burden_holder="EGS operator",
        adversary_position="Hydraulic stimulation can cause damaging earthquakes and public opposition.",
        counter_arguments=[
            "Traffic light protocols and real-time monitoring can mitigate seismic risk.",
            "Public engagement and transparency improve acceptance.",
            "Site selection avoids known fault zones."
        ],
        resolution_strategy="Implement adaptive traffic light protocols and require public disclosure of monitoring data.",
        entity_scope="All EGS projects and pilot demonstrations.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="DOE EGS Protocols (2015); ISRM Guidelines (2018)"
    ),
    DoctrineBlock(
        topic="Geothermal Well Design for High Temperature Environments",
        keywords=[
            "well design", "high temperature", "casing", "cementing", "thermal stress", "well integrity"
        ],
        conclusion_template="High-temperature geothermal wells require specialized design to ensure long-term integrity and operational safety.",
        reasoning_framework="""
            Geothermal wells in high-temperature environments (>200°C) are subject to unique challenges, including thermal expansion, casing deformation, and aggressive fluid chemistry. Well design must incorporate high-grade casing materials (e.g., chrome alloys), thermal expansion joints, and cement formulations resistant to high temperatures and chemical attack. The design process involves thermal and mechanical modeling to predict stress regimes during production and shut-in cycles. Wellhead equipment must be rated for high temperatures and pressures. Regular integrity testing (pressure, temperature, and cement bond logs) is required throughout the well's lifecycle. Compliance with API and ISO standards is mandatory for safety and regulatory approval.
        """,
        key_factors=[
            "Casing material selection", "Thermal expansion modeling", "Cement integrity", "Wellhead rating"
        ],
        primary_authority=["API Spec 5CT", "ISO 10423", "DOE Geothermal Well Best Practices"],
        burden_holder="Well design engineer",
        adversary_position="High-grade materials and complex designs increase capital costs.",
        counter_arguments=[
            "Failure to address high-temperature challenges leads to costly well failures.",
            "Long-term integrity reduces O&M costs.",
            "Regulatory compliance is non-negotiable."
        ],
        resolution_strategy="Adopt lifecycle cost analysis and require third-party design review for all high-temperature wells.",
        entity_scope="All geothermal wells in high-temperature fields.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Spec 5CT (2018); ISO 10423 (2015)"
    ),
    DoctrineBlock(
        topic="Silica and Calcite Scaling Management",
        keywords=[
            "scaling", "silica", "calcite", "inhibitors", "wellbore maintenance", "plant efficiency"
        ],
        conclusion_template="Silica and calcite scaling must be proactively managed to maintain well and plant performance.",
        reasoning_framework="""
            Silica and calcite scaling are common issues in geothermal operations, leading to reduced well productivity and plant efficiency. Management strategies include chemical inhibition, pH adjustment, controlled pressure drops, and periodic mechanical cleaning. The selection of inhibitors must consider compatibility with reservoir fluids and environmental regulations. Real-time monitoring of scaling indices and fluid chemistry enables early intervention. Plant design should minimize conditions that promote scaling, such as rapid pressure and temperature changes. Regular maintenance schedules and data-driven scaling prediction models are essential for long-term reliability. Regulatory compliance for chemical use and waste disposal must be maintained.
        """,
        key_factors=[
            "Scaling indices", "Inhibitor selection", "Fluid chemistry monitoring", "Maintenance protocols"
        ],
        primary_authority=["DOE Geothermal Scaling Guidelines", "NACE International", "Geothermal Resources Council"],
        burden_holder="Plant operator",
        adversary_position="Scaling management increases O&M costs and chemical use.",
        counter_arguments=[
            "Proactive management reduces unplanned downtime.",
            "Advanced inhibitors minimize environmental impact.",
            "Predictive maintenance optimizes cost."
        ],
        resolution_strategy="Implement real-time monitoring and predictive scaling management in all geothermal operations.",
        entity_scope="All geothermal wells and power plants.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOE Scaling Guidelines (2017); NACE SP0472"
    ),
    DoctrineBlock(
        topic="Induced Seismicity Traffic Light Protocol",
        keywords=[
            "induced seismicity", "traffic light protocol", "seismic monitoring", "EGS", "public safety"
        ],
        conclusion_template="All geothermal operations with induced seismicity risk must implement a traffic light protocol (TLP) for real-time risk management.",
        reasoning_framework="""
            The traffic light protocol (TLP) is a risk management tool for geothermal projects where hydraulic stimulation or reinjection may induce seismic events. TLP involves continuous seismic monitoring and predefined response actions based on observed seismicity levels: green (continue), amber (proceed with caution), and red (suspend operations). Thresholds are set based on local seismicity, regulatory requirements, and public risk tolerance. Real-time data integration and communication with stakeholders are essential. The protocol must be adaptive, allowing for threshold adjustments based on observed outcomes. Public transparency and regulatory reporting are mandatory components. TLP implementation is a condition for permitting in many jurisdictions.
        """,
        key_factors=[
            "Seismic monitoring network", "Threshold determination", "Regulatory compliance", "Stakeholder engagement"
        ],
        primary_authority=["USGS Induced Seismicity Protocols", "DOE EGS Best Practices", "ISRM Guidelines"],
        burden_holder="Project operator",
        adversary_position="TLPs may be overly conservative and limit project productivity.",
        counter_arguments=[
            "TLPs protect public safety and project reputation.",
            "Adaptive thresholds allow for operational flexibility.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Mandate TLP implementation and periodic review for all geothermal projects with induced seismicity risk.",
        entity_scope="All geothermal projects with hydraulic stimulation or significant reinjection.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="USGS Induced Seismicity Protocols (2016); DOE EGS Protocols (2015)"
    ),
    DoctrineBlock(
        topic="Ground-Source Heat Pump Coefficient of Performance (COP)",
        keywords=[
            "ground-source heat pump", "COP", "efficiency", "heat exchange", "system design"
        ],
        conclusion_template="COP must be calculated and optimized for all ground-source heat pump (GSHP) systems to ensure energy efficiency and regulatory compliance.",
        reasoning_framework="""
            The coefficient of performance (COP) is a key metric for evaluating the efficiency of ground-source heat pump (GSHP) systems. COP is defined as the ratio of useful heating or cooling provided to the energy consumed. Accurate COP calculation requires measurement of heat exchange rates, input power, and system losses. System design should maximize COP by optimizing ground loop configuration, fluid flow rates, and heat exchanger sizing. Regulatory standards (e.g., ASHRAE, ISO 13256) specify minimum COP requirements for different climates and applications. Monitoring and periodic performance verification are necessary to maintain efficiency over the system's lifecycle. Incentive programs may require documented COP values.
        """,
        key_factors=[
            "Heat exchange rate", "System losses", "Ground loop design", "Regulatory standards"
        ],
        primary_authority=["ASHRAE 90.1", "ISO 13256", "DOE GSHP Guidelines"],
        burden_holder="System designer",
        adversary_position="COP values can be overstated in marketing and may not reflect real-world performance.",
        counter_arguments=[
            "Third-party testing and certification ensure accuracy.",
            "Performance monitoring can detect deviations.",
            "Regulatory oversight enforces compliance."
        ],
        resolution_strategy="Require third-party COP certification and ongoing performance monitoring for all GSHP installations.",
        entity_scope="All ground-source heat pump projects.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASHRAE 90.1 (2019); ISO 13256 (1998)"
    ),
    DoctrineBlock(
        topic="Geothermal Reservoir Modeling with TOUGH2",
        keywords=[
            "reservoir modeling", "TOUGH2", "numerical simulation", "multiphase flow", "history matching"
        ],
        conclusion_template="Numerical reservoir modeling using TOUGH2 or equivalent is required for all major geothermal developments.",
        reasoning_framework="""
            TOUGH2 is a widely used numerical simulator for geothermal reservoir modeling, capable of handling multiphase, multicomponent flow in porous and fractured media. The modeling process integrates geological, geophysical, and production data to predict reservoir behavior under various development scenarios. History matching with observed production and pressure data is essential for model calibration. Sensitivity analysis identifies key uncertainties and guides data acquisition. Model results inform well placement, production strategy, and resource management. Regulatory agencies and financiers often require independent model review. Model documentation must include assumptions, input data, calibration results, and uncertainty quantification.
        """,
        key_factors=[
            "Data integration", "Model calibration", "Uncertainty analysis", "Regulatory review"
        ],
        primary_authority=["Lawrence Berkeley National Laboratory", "DOE Geothermal Technologies Office", "IEA Geothermal"],
        burden_holder="Reservoir engineer",
        adversary_position="Numerical models are only as good as the input data and may misrepresent reality.",
        counter_arguments=[
            "History matching and sensitivity analysis improve reliability.",
            "Independent review ensures model quality.",
            "Continuous data integration reduces uncertainty."
        ],
        resolution_strategy="Mandate independent model review and regular updates with new data.",
        entity_scope="All geothermal fields under development or expansion.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="LBNL TOUGH2 User's Guide; DOE GTO Modeling Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Levelized Cost of Energy (LCOE) Analysis",
        keywords=[
            "LCOE", "cost analysis", "project finance", "economic assessment", "power purchase agreement"
        ],
        conclusion_template="LCOE analysis is mandatory for all geothermal projects seeking financing or regulatory approval.",
        reasoning_framework="""
            Levelized Cost of Energy (LCOE) is a standard metric for comparing the cost-effectiveness of energy projects. LCOE analysis for geothermal projects includes capital costs, O&M costs, fuel (if any), financing terms, project lifetime, and capacity factor. The analysis must follow recognized methodologies (e.g., NREL, IEA) and include sensitivity to key variables. LCOE results inform investment decisions, power purchase agreements, and policy incentives. Transparent assumptions and documentation are required for regulatory and financial review. LCOE should be updated as project parameters change during development.
        """,
        key_factors=[
            "Capital cost", "O&M cost", "Capacity factor", "Financing terms", "Project lifetime"
        ],
        primary_authority=["NREL LCOE Calculator", "IEA Geothermal Handbook", "DOE GTO"],
        burden_holder="Project developer",
        adversary_position="LCOE does not capture all project risks and may underestimate costs.",
        counter_arguments=[
            "Sensitivity analysis can address uncertainties.",
            "LCOE is an industry standard for comparability.",
            "Supplementary risk assessment can be included."
        ],
        resolution_strategy="Require LCOE analysis with sensitivity and risk assessment for all major projects.",
        entity_scope="All geothermal projects seeking external financing or regulatory approval.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NREL LCOE Methodology (2020); IEA Geothermal Handbook (2010)"
    ),
    DoctrineBlock(
        topic="Non-Condensable Gas (NCG) Extraction and H2S Abatement",
        keywords=[
            "NCG", "hydrogen sulfide", "gas extraction", "environmental compliance", "air emissions"
        ],
        conclusion_template="Effective NCG extraction and H2S abatement are required to meet environmental and health standards.",
        reasoning_framework="""
            Non-condensable gases (NCGs), including CO2 and H2S, are commonly produced in geothermal operations. NCG extraction systems (e.g., vacuum pumps, ejectors) are required to maintain condenser vacuum and plant efficiency. H2S abatement technologies (e.g., Stretford, LO-CAT, thermal oxidation) must be selected based on gas concentration, plant scale, and regulatory limits. Continuous emissions monitoring is required for compliance with air quality standards (e.g., EPA, local agencies). Plant design should minimize fugitive emissions and provide for safe handling and disposal of abatement byproducts. Community engagement and transparent reporting are essential for public acceptance.
        """,
        key_factors=[
            "NCG concentration", "Abatement technology selection", "Emissions monitoring", "Regulatory limits"
        ],
        primary_authority=["EPA Clean Air Act", "DOE Geothermal Emissions Guidelines", "Geothermal Resources Council"],
        burden_holder="Plant operator",
        adversary_position="Abatement systems increase capital and O&M costs.",
        counter_arguments=[
            "Non-compliance leads to fines and operational shutdown.",
            "Modern abatement systems are cost-effective and reliable.",
            "Public health and environmental protection are priorities."
        ],
        resolution_strategy="Mandate continuous emissions monitoring and best available abatement technology for all plants.",
        entity_scope="All geothermal power plants with NCG emissions.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Clean Air Act (2018); DOE Emissions Guidelines (2017)"
    ),
    DoctrineBlock(
        topic="Geothermal Reinjection Strategy and Pressure Maintenance",
        keywords=[
            "reinjection", "pressure maintenance", "reservoir sustainability", "thermal breakthrough", "well placement"
        ],
        conclusion_template="Reinjection strategies must be optimized for pressure maintenance and long-term reservoir sustainability.",
        reasoning_framework="""
            Reinjection of spent geothermal fluids is essential for pressure maintenance, reservoir sustainability, and environmental compliance. Reinjection well placement and rate must be optimized to avoid thermal breakthrough and maintain reservoir pressure. Numerical modeling and tracer testing inform reinjection strategy. Monitoring of reservoir pressure, temperature, and chemistry is required to detect adverse impacts. Reinjection design must comply with regulatory requirements for groundwater protection and induced seismicity. Adaptive management allows for adjustment of reinjection parameters based on monitoring data. Reinjection also supports environmental goals by minimizing surface discharge.
        """,
        key_factors=[
            "Well placement", "Reinjection rate", "Thermal breakthrough risk", "Regulatory compliance"
        ],
        primary_authority=["DOE Geothermal Reinjection Guidelines", "USGS", "IEA Geothermal"],
        burden_holder="Reservoir engineer",
        adversary_position="Reinjection can cause induced seismicity and reduce resource temperature.",
        counter_arguments=[
            "Careful modeling and monitoring mitigate risks.",
            "Adaptive management allows for real-time adjustments.",
            "Reinjection is required for environmental compliance."
        ],
        resolution_strategy="Mandate integrated modeling and monitoring for all reinjection operations.",
        entity_scope="All geothermal fields with reinjection requirements.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOE Reinjection Guidelines (2016); USGS Circular 790"
    ),
    DoctrineBlock(
        topic="Geothermal Exploration Risk and Drilling Success Rates",
        keywords=[
            "exploration risk", "drilling success", "resource uncertainty", "risk mitigation", "insurance"
        ],
        conclusion_template="Exploration risk must be quantified and mitigated through phased drilling, insurance, and data integration.",
        reasoning_framework="""
            Geothermal exploration involves significant risk due to subsurface uncertainty and high drilling costs. Risk quantification includes probabilistic resource assessment, geological risk mapping, and analysis of historical drilling success rates. Phased exploration, starting with slim holes and progressing to full-diameter wells, reduces exposure. Risk mitigation tools include exploration insurance and government-backed risk-sharing programs. Integration of geophysical, geological, and geochemical data improves targeting. Transparent risk disclosure is required for financing and regulatory approval. Lessons learned from unsuccessful wells should inform future exploration strategy.
        """,
        key_factors=[
            "Resource uncertainty", "Historical success rates", "Risk mitigation tools", "Data integration"
        ],
        primary_authority=["World Bank ESMAP", "DOE Geothermal Technologies Office", "IEA Geothermal"],
        burden_holder="Project developer",
        adversary_position="Exploration risk is too high for private investment.",
        counter_arguments=[
            "Risk-sharing mechanisms and insurance reduce financial exposure.",
            "Improved data integration increases drilling success.",
            "Government incentives are available."
        ],
        resolution_strategy="Require risk assessment, phased drilling, and disclosure for all exploration projects.",
        entity_scope="All geothermal exploration and early-stage development projects.",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="World Bank ESMAP Geothermal Handbook (2012); DOE GTO"
    ),
    DoctrineBlock(
        topic="Binary Cycle Organic Rankine Cycle (ORC) Working Fluid Selection",
        keywords=[
            "binary cycle", "ORC", "working fluid", "thermodynamics", "environmental impact"
        ],
        conclusion_template="Working fluid selection for ORC plants must balance thermodynamic efficiency, environmental impact, and regulatory compliance.",
        reasoning_framework="""
            The choice of working fluid in binary cycle (ORC) geothermal plants affects plant efficiency, environmental impact, and safety. Thermodynamic properties (boiling point, heat capacity, vapor pressure) must match resource temperature and plant design. Environmental considerations include global warming potential (GWP), ozone depletion potential (ODP), and toxicity. Regulatory frameworks (e.g., EPA SNAP, EU F-Gas Regulation) restrict the use of certain fluids. Safety protocols require assessment of flammability and compatibility with plant materials. Lifecycle analysis should inform fluid selection. Documentation of fluid selection criteria and regulatory compliance is required for permitting.
        """,
        key_factors=[
            "Thermodynamic properties", "Environmental impact", "Regulatory compliance", "Safety"
        ],
        primary_authority=["EPA SNAP", "EU F-Gas Regulation", "DOE ORC Guidelines"],
        burden_holder="Plant designer",
        adversary_position="Environmentally benign fluids may reduce efficiency or increase costs.",
        counter_arguments=[
            "Advances in fluid technology are improving both efficiency and environmental performance.",
            "Regulatory compliance is mandatory.",
            "Lifecycle cost analysis can justify selection."
        ],
        resolution_strategy="Mandate lifecycle and regulatory review for all working fluid selections.",
        entity_scope="All binary cycle geothermal plants.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA SNAP (2020); EU F-Gas Regulation (2014)"
    ),
    DoctrineBlock(
        topic="Geothermal Power Plant Capacity Factor and Availability",
        keywords=[
            "capacity factor", "availability", "plant reliability", "O&M", "performance monitoring"
        ],
        conclusion_template="Capacity factor and availability must be tracked and reported for all geothermal power plants.",
        reasoning_framework="""
            Capacity factor measures the actual output of a plant relative to its maximum possible output, while availability reflects the percentage of time the plant is operational. High capacity factors (>85%) are a key advantage of geothermal power. Accurate tracking requires automated performance monitoring and regular reporting. O&M practices, equipment reliability, and resource management directly impact these metrics. Regulatory agencies and financiers require documented capacity factor and availability for project evaluation. Performance deviations should trigger root cause analysis and corrective action. Transparent reporting supports market credibility and policy incentives.
        """,
        key_factors=[
            "Performance monitoring", "O&M practices", "Equipment reliability", "Reporting standards"
        ],
        primary_authority=["NERC GADS", "DOE Geothermal Technologies Office", "IEA Geothermal"],
        burden_holder="Plant operator",
        adversary_position="Reported capacity factors may not reflect long-term performance.",
        counter_arguments=[
            "Long-term data collection and independent audits ensure accuracy.",
            "Performance guarantees can be included in contracts.",
            "Regulatory oversight enforces reporting."
        ],
        resolution_strategy="Require automated monitoring and independent verification for all plants.",
        entity_scope="All geothermal power plants.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NERC GADS (2019); DOE GTO Reporting Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Direct Use Applications",
        keywords=[
            "direct use", "district heating", "greenhouse heating", "aquaculture", "balneology"
        ],
        conclusion_template="Direct use applications must be evaluated for technical, economic, and environmental feasibility.",
        reasoning_framework="""
            Geothermal direct use involves utilizing moderate-temperature resources for heating, agriculture, aquaculture, and recreational purposes. Feasibility assessment includes resource temperature, flow rate, proximity to end users, and infrastructure requirements. Economic analysis considers capital and O&M costs, market demand, and potential revenue streams. Environmental review addresses fluid disposal, land use, and emissions. Regulatory compliance with health, safety, and environmental standards is required. Community engagement and stakeholder analysis support project acceptance. Successful direct use projects diversify revenue and increase resource utilization efficiency.
        """,
        key_factors=[
            "Resource temperature", "Market demand", "Infrastructure", "Environmental compliance"
        ],
        primary_authority=["DOE Direct Use Handbook", "IEA Geothermal", "Geothermal Resources Council"],
        burden_holder="Project developer",
        adversary_position="Direct use projects may have limited market and low returns.",
        counter_arguments=[
            "Co-location with existing infrastructure reduces costs.",
            "District heating and agriculture offer stable demand.",
            "Environmental benefits can attract incentives."
        ],
        resolution_strategy="Require comprehensive feasibility and market studies for all direct use proposals.",
        entity_scope="All geothermal direct use projects.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Direct Use Handbook (2004); IEA Geothermal"
    ),
    DoctrineBlock(
        topic="Geothermal Environmental Impact Assessment",
        keywords=[
            "environmental impact", "EIA", "permitting", "biodiversity", "emissions", "land use"
        ],
        conclusion_template="Comprehensive environmental impact assessment is mandatory for all geothermal projects prior to permitting.",
        reasoning_framework="""
            Environmental Impact Assessment (EIA) is a legal requirement for geothermal projects in most jurisdictions. The EIA process evaluates potential impacts on air, water, soil, biodiversity, and local communities. Baseline studies establish pre-project conditions. Impact mitigation measures address emissions, noise, land use, and waste management. Stakeholder consultation and public disclosure are integral components. Cumulative impacts and alternatives analysis must be included. Regulatory agencies review EIA documentation as part of the permitting process. Ongoing monitoring and adaptive management are required to address unforeseen impacts during operations.
        """,
        key_factors=[
            "Baseline studies", "Impact mitigation", "Stakeholder consultation", "Regulatory compliance"
        ],
        primary_authority=["EPA NEPA", "DOE EIA Guidelines", "World Bank ESMAP"],
        burden_holder="Project developer",
        adversary_position="EIA process is lengthy and costly, delaying project development.",
        counter_arguments=[
            "Early planning and stakeholder engagement streamline the process.",
            "EIA reduces long-term environmental and social risks.",
            "Regulatory compliance is non-negotiable."
        ],
        resolution_strategy="Mandate early initiation of EIA and integration with project planning.",
        entity_scope="All geothermal projects requiring permits.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NEPA (1969); DOE EIA Guidelines (2017)"
    ),
    # Additional doctrine blocks for coverage (to reach 40+)
    DoctrineBlock(
        topic="Geothermal Brine Handling and Disposal",
        keywords=[
            "brine handling", "disposal", "environmental compliance", "waste management", "reinjection"
        ],
        conclusion_template="Brine handling and disposal must comply with environmental regulations and minimize surface discharge.",
        reasoning_framework="""
            Geothermal brine often contains dissolved minerals and trace contaminants. Handling and disposal strategies include reinjection, evaporation ponds, and zero-liquid discharge systems. Reinjection is preferred for environmental compliance and reservoir sustainability. Brine chemistry must be analyzed to assess scaling, corrosion, and environmental risk. Regulatory permits specify allowable disposal methods and monitoring requirements. Treatment technologies (e.g., filtration, chemical precipitation) may be required for surface discharge. Community engagement is necessary for projects near sensitive areas. Documentation of brine management practices is required for regulatory review.
        """,
        key_factors=[
            "Brine chemistry", "Disposal method", "Regulatory compliance", "Monitoring"
        ],
        primary_authority=["EPA Underground Injection Control", "DOE Brine Management Guidelines"],
        burden_holder="Plant operator",
        adversary_position="Brine disposal increases operational complexity and cost.",
        counter_arguments=[
            "Reinjection supports reservoir sustainability.",
            "Treatment technologies reduce environmental impact.",
            "Non-compliance leads to penalties."
        ],
        resolution_strategy="Mandate reinjection where feasible and require monitoring of all disposal methods.",
        entity_scope="All geothermal projects producing brine.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA UIC Program (2018); DOE Brine Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Fluid Chemistry Monitoring",
        keywords=[
            "fluid chemistry", "monitoring", "scaling", "corrosion", "sampling", "analytical methods"
        ],
        conclusion_template="Regular fluid chemistry monitoring is required to manage scaling, corrosion, and environmental compliance.",
        reasoning_framework="""
            Geothermal fluid chemistry changes over time due to reservoir processes and production activities. Regular sampling and analysis detect trends in scaling and corrosion potential, as well as environmental contaminants. Analytical methods must follow ASTM and EPA standards for accuracy and comparability. Data inform inhibitor selection, maintenance schedules, and regulatory reporting. Automated sensors and remote monitoring improve data frequency and reliability. Documentation of sampling protocols and results is required for audits and compliance.
        """,
        key_factors=[
            "Sampling frequency", "Analytical accuracy", "Data integration", "Regulatory reporting"
        ],
        primary_authority=["ASTM D4519", "EPA Water Quality Standards", "DOE Geothermal Guidelines"],
        burden_holder="Plant chemist",
        adversary_position="Frequent monitoring increases O&M costs.",
        counter_arguments=[
            "Early detection prevents costly equipment failures.",
            "Automated systems reduce labor costs.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Implement automated monitoring and require quarterly reporting.",
        entity_scope="All geothermal wells and plants.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D4519 (2016); EPA Water Quality Standards"
    ),
    DoctrineBlock(
        topic="Geothermal Well Logging and Testing Standards",
        keywords=[
            "well logging", "testing", "temperature logs", "pressure logs", "flow testing", "data quality"
        ],
        conclusion_template="All geothermal wells must undergo standardized logging and testing to ensure data quality and regulatory compliance.",
        reasoning_framework="""
            Well logging and testing provide critical data for reservoir characterization and well integrity assessment. Standard logs include temperature, pressure, caliper, and flow tests. Testing protocols must follow API, ASTM, and ISO standards. Data quality control includes calibration, repeat measurements, and independent review. Results inform resource assessment, well design, and production strategy. Regulatory agencies require submission of logging and testing data for permitting and monitoring. Data archiving ensures long-term accessibility for future analysis.
        """,
        key_factors=[
            "Logging protocols", "Data calibration", "Regulatory submission", "Data archiving"
        ],
        primary_authority=["API RP 10B", "ASTM D5753", "ISO 10414"],
        burden_holder="Wellsite geologist",
        adversary_position="Standardized testing increases drilling time and costs.",
        counter_arguments=[
            "High-quality data reduce long-term project risk.",
            "Regulatory compliance is mandatory.",
            "Data archiving supports future optimization."
        ],
        resolution_strategy="Mandate standardized logging and testing for all geothermal wells.",
        entity_scope="All geothermal drilling operations.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 10B (2015); ASTM D5753 (2017)"
    ),
    DoctrineBlock(
        topic="Geothermal Project Financing and Risk Allocation",
        keywords=[
            "project finance", "risk allocation", "PPAs", "insurance", "government incentives"
        ],
        conclusion_template="Project financing structures must allocate risks appropriately and comply with lender and regulatory requirements.",
        reasoning_framework="""
            Geothermal projects require significant upfront capital and face unique risks (resource, construction, market). Financing structures include equity, debt, and public-private partnerships. Risk allocation is achieved through power purchase agreements (PPAs), insurance (exploration, construction, operational), and government incentives (tax credits, grants). Lenders require due diligence on resource assessment, permitting, and offtake agreements. Transparent risk disclosure and mitigation plans are essential for securing financing. Regulatory compliance with securities and environmental laws is mandatory. Financial close requires all major risks to be addressed and allocated to parties best able to manage them.
        """,
        key_factors=[
            "Risk allocation", "Financing structure", "Due diligence", "Regulatory compliance"
        ],
        primary_authority=["World Bank ESMAP", "DOE Geothermal Financing Handbook", "IEA Geothermal"],
        burden_holder="Project developer",
        adversary_position="Complex financing structures increase transaction costs.",
        counter_arguments=[
            "Proper risk allocation attracts investment.",
            "Government incentives reduce financing costs.",
            "Due diligence protects all parties."
        ],
        resolution_strategy="Require risk allocation documentation and third-party review for all financed projects.",
        entity_scope="All geothermal projects seeking external financing.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="World Bank ESMAP Financing Handbook (2014); DOE GTO"
    ),
    DoctrineBlock(
        topic="Geothermal Surface Facility Siting and Land Use",
        keywords=[
            "facility siting", "land use", "permitting", "zoning", "community engagement"
        ],
        conclusion_template="Surface facility siting must consider land use, environmental, and community factors in accordance with permitting requirements.",
        reasoning_framework="""
            Siting of geothermal surface facilities (plants, pipelines, roads) requires assessment of land use compatibility, environmental sensitivity, and community impacts. Permitting processes involve zoning review, environmental impact assessment, and stakeholder consultation. Site selection should avoid protected areas, minimize land disturbance, and consider access to infrastructure. Community engagement is essential to address concerns and secure social license. Regulatory compliance with local, state, and federal land use laws is mandatory. Documentation of siting criteria and alternatives analysis is required for permitting.
        """,
        key_factors=[
            "Land use compatibility", "Environmental sensitivity", "Community engagement", "Regulatory compliance"
        ],
        primary_authority=["EPA NEPA", "DOE Facility Siting Guidelines", "Local zoning laws"],
        burden_holder="Project developer",
        adversary_position="Siting restrictions can delay projects and increase costs.",
        counter_arguments=[
            "Early engagement and alternatives analysis streamline permitting.",
            "Proper siting reduces long-term risk.",
            "Community support is critical for project success."
        ],
        resolution_strategy="Mandate alternatives analysis and early community consultation for all siting decisions.",
        entity_scope="All geothermal surface facility projects.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NEPA (1969); DOE Siting Guidelines (2015)"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Temperature Classification",
        keywords=[
            "resource temperature", "classification", "high-enthalpy", "low-enthalpy", "technology selection"
        ],
        conclusion_template="Resource temperature classification guides technology selection and project design.",
        reasoning_framework="""
            Geothermal resources are classified by temperature: low (<90°C), moderate (90–150°C), and high (>150°C). This classification informs technology selection (direct use, binary cycle, flash steam) and project economics. Resource temperature is determined by well logging and reservoir modeling. Regulatory agencies and financiers require temperature classification in resource reporting. Documentation must include data sources, measurement methods, and uncertainty analysis. Temperature classification also informs environmental and permitting requirements.
        """,
        key_factors=[
            "Temperature measurement", "Classification criteria", "Technology compatibility", "Regulatory reporting"
        ],
        primary_authority=["USGS Circular 790", "DOE GTO", "IEA Geothermal"],
        burden_holder="Resource assessor",
        adversary_position="Temperature classification may oversimplify resource potential.",
        counter_arguments=[
            "Detailed reporting can supplement classification.",
            "Classification is required for comparability.",
            "Uncertainty analysis addresses limitations."
        ],
        resolution_strategy="Require temperature classification and supporting data in all resource reports.",
        entity_scope="All geothermal resource assessments.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="USGS Circular 790 (1978); DOE GTO"
    ),
    DoctrineBlock(
        topic="Geothermal Reservoir Pressure Management",
        keywords=[
            "reservoir pressure", "management", "monitoring", "sustainability", "production strategy"
        ],
        conclusion_template="Reservoir pressure must be monitored and managed to ensure sustainable production.",
        reasoning_framework="""
            Reservoir pressure declines with production and can lead to reduced output, subsidence, and induced seismicity. Pressure management involves monitoring with downhole gauges, modeling pressure response, and adjusting production and reinjection rates. Regulatory agencies require pressure monitoring and reporting. Adaptive management allows for real-time adjustments to maintain reservoir sustainability. Pressure management strategies should be documented and reviewed periodically. Failure to manage pressure can lead to regulatory penalties and resource depletion.
        """,
        key_factors=[
            "Pressure monitoring", "Production rate", "Reinjection strategy", "Regulatory compliance"
        ],
        primary_authority=["DOE Reservoir Management Guidelines", "USGS", "IEA Geothermal"],
        burden_holder="Reservoir engineer",
        adversary_position="Pressure management adds operational complexity.",
        counter_arguments=[
            "Sustainable production maximizes long-term value.",
            "Automated monitoring reduces labor.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate pressure monitoring and adaptive management for all geothermal fields.",
        entity_scope="All geothermal production fields.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOE Reservoir Management Guidelines (2016); USGS"
    ),
    DoctrineBlock(
        topic="Geothermal Well Abandonment and Site Restoration",
        keywords=[
            "well abandonment", "site restoration", "plugging", "regulatory compliance", "environmental protection"
        ],
        conclusion_template="All geothermal wells must be properly abandoned and sites restored in accordance with regulatory requirements.",
        reasoning_framework="""
            Well abandonment involves plugging the well with cement and removing surface equipment to prevent fluid migration and environmental contamination. Site restoration includes regrading, revegetation, and removal of infrastructure. Regulatory agencies specify abandonment procedures and require documentation and inspection. Environmental monitoring may be required post-abandonment. Financial assurance (bonds) is often required to ensure proper closure. Failure to comply can result in penalties and long-term liability.
        """,
        key_factors=[
            "Plugging procedures", "Site restoration", "Regulatory inspection", "Financial assurance"
        ],
        primary_authority=["API RP 1004", "DOE Well Abandonment Guidelines", "State regulatory agencies"],
        burden_holder="Well operator",
        adversary_position="Abandonment and restoration increase project costs.",
        counter_arguments=[
            "Proper closure prevents future liabilities.",
            "Regulatory compliance is mandatory.",
            "Financial assurance protects public interest."
        ],
        resolution_strategy="Mandate regulatory-approved abandonment and restoration for all wells.",
        entity_scope="All geothermal wells at end of life.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 1004 (2014); DOE Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Leasing and Royalty Compliance",
        keywords=[
            "resource leasing", "royalties", "compliance", "BLM", "state lands", "revenue reporting"
        ],
        conclusion_template="Leasing and royalty compliance is required for all geothermal projects on public and private lands.",
        reasoning_framework="""
            Geothermal resource development on public and private lands requires leases and payment of royalties. Federal (BLM), state, and private leases specify terms for exploration, development, and production. Royalty rates and reporting requirements vary by jurisdiction. Compliance includes timely payment, accurate production reporting, and adherence to lease terms. Audits and inspections may be conducted by authorities. Non-compliance can result in lease termination and penalties. Transparent documentation and regular training support compliance.
        """,
        key_factors=[
            "Lease terms", "Royalty rates", "Reporting requirements", "Audit procedures"
        ],
        primary_authority=["BLM Geothermal Regulations", "State land agencies", "DOE GTO"],
        burden_holder="Leaseholder",
        adversary_position="Royalty compliance increases administrative burden.",
        counter_arguments=[
            "Non-compliance risks loss of lease.",
            "Clear procedures streamline compliance.",
            "Revenue supports public interest."
        ],
        resolution_strategy="Mandate compliance training and regular audits for all leaseholders.",
        entity_scope="All geothermal projects on leased lands.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="BLM Geothermal Regulations (2016); State agencies"
    ),
    DoctrineBlock(
        topic="Geothermal Induced Subsidence Monitoring",
        keywords=[
            "subsidence", "monitoring", "land deformation", "InSAR", "reservoir management"
        ],
        conclusion_template="Subsidence monitoring is required for all geothermal fields to detect and mitigate land deformation.",
        reasoning_framework="""
            Fluid extraction from geothermal reservoirs can cause land subsidence, affecting infrastructure and ecosystems. Monitoring methods include leveling surveys, GPS, and InSAR remote sensing. Data are integrated with reservoir models to assess causes and predict future deformation. Regulatory agencies may require subsidence monitoring and reporting as a permit condition. Mitigation measures include adjusting production and reinjection rates. Community engagement is essential if subsidence affects populated areas. Documentation of monitoring protocols and results is required for regulatory review.
        """,
        key_factors=[
            "Monitoring methods", "Data integration", "Mitigation measures", "Regulatory reporting"
        ],
        primary_authority=["USGS", "DOE Geothermal Guidelines", "State regulatory agencies"],
        burden_holder="Field operator",
        adversary_position="Subsidence monitoring adds cost and complexity.",
        counter_arguments=[
            "Early detection prevents infrastructure damage.",
            "Mitigation reduces long-term risk.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate annual subsidence monitoring and reporting for all fields.",
        entity_scope="All geothermal production fields.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="USGS Subsidence Monitoring (2015); DOE Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Unitization and Joint Development",
        keywords=[
            "unitization", "joint development", "resource management", "stakeholder agreement", "regulatory approval"
        ],
        conclusion_template="Unitization and joint development agreements are required for shared geothermal resources to optimize recovery and minimize conflict.",
        reasoning_framework="""
            Geothermal reservoirs may extend across multiple leases or ownerships. Unitization involves combining interests for joint development, optimizing resource recovery, and reducing duplication. Agreements specify allocation of costs, revenues, and operational responsibilities. Regulatory approval is required to ensure fair and efficient development. Stakeholder engagement and transparent negotiation are essential. Documentation of unitization agreements and regulatory filings is required. Failure to unitize can lead to legal disputes and suboptimal recovery.
        """,
        key_factors=[
            "Resource boundaries", "Stakeholder agreement", "Cost/revenue allocation", "Regulatory approval"
        ],
        primary_authority=["BLM Unitization Guidelines", "State regulatory agencies", "DOE GTO"],
        burden_holder="Resource owners",
        adversary_position="Unitization negotiations can be lengthy and contentious.",
        counter_arguments=[
            "Joint development maximizes resource value.",
            "Regulatory frameworks facilitate agreement.",
            "Transparent negotiation reduces conflict."
        ],
        resolution_strategy="Mandate unitization for all shared reservoirs and require regulatory approval.",
        entity_scope="All shared geothermal resources.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="BLM Unitization Guidelines (2016); State agencies"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Sustainability Certification",
        keywords=[
            "sustainability", "certification", "resource management", "third-party audit", "environmental standards"
        ],
        conclusion_template="Sustainability certification is recommended for geothermal projects to demonstrate responsible resource management.",
        reasoning_framework="""
            Sustainability certification programs (e.g., IGA, GRC) assess geothermal projects for responsible resource management, environmental protection, and community engagement. Certification involves third-party audit of resource management, emissions, reinjection, and social practices. Certified projects may access premium markets and incentives. Documentation of sustainability practices and audit results is required. Certification supports public acceptance and regulatory compliance. Periodic recertification ensures ongoing compliance.
        """,
        key_factors=[
            "Certification criteria", "Third-party audit", "Documentation", "Recertification"
        ],
        primary_authority=["International Geothermal Association", "Geothermal Resources Council"],
        burden_holder="Project developer",
        adversary_position="Certification adds cost and administrative burden.",
        counter_arguments=[
            "Certification improves market access and reputation.",
            "Third-party audit increases transparency.",
            "Incentives may offset costs."
        ],
        resolution_strategy="Encourage certification and provide incentives for certified projects.",
        entity_scope="All geothermal projects seeking sustainability recognition.",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="IGA Sustainability Protocol (2015); GRC"
    ),
    DoctrineBlock(
        topic="Geothermal Data Management and Reporting",
        keywords=[
            "data management", "reporting", "data archiving", "regulatory compliance", "transparency"
        ],
        conclusion_template="Robust data management and reporting systems are required for all geothermal projects.",
        reasoning_framework="""
            Geothermal projects generate large volumes of data (exploration, drilling, production, environmental). Data management systems must ensure data quality, security, and accessibility. Regulatory agencies require regular reporting and data submission. Data archiving supports future analysis and regulatory review. Transparency in data reporting builds stakeholder trust and supports project financing. Data standards (e.g., XML, WITSML) facilitate interoperability. Documentation of data management protocols and regular audits are required.
        """,
        key_factors=[
            "Data quality", "Reporting standards", "Archiving", "Regulatory submission"
        ],
        primary_authority=["DOE Data Management Guidelines", "USGS", "State regulatory agencies"],
        burden_holder="Project operator",
        adversary_position="Data management systems are expensive and complex.",
        counter_arguments=[
            "Efficient data management reduces long-term costs.",
            "Regulatory compliance is mandatory.",
            "Transparency supports financing."
        ],
        resolution_strategy="Mandate data management plans and regular audits for all projects.",
        entity_scope="All geothermal projects.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOE Data Guidelines (2018); USGS"
    ),
    DoctrineBlock(
        topic="Geothermal Workforce Health and Safety Standards",
        keywords=[
            "workforce safety", "health standards", "OSHA", "training", "PPE", "incident reporting"
        ],
        conclusion_template="All geothermal operations must comply with workforce health and safety standards.",
        reasoning_framework="""
            Geothermal operations involve high temperatures, high pressures, and hazardous chemicals. Health and safety standards (OSHA, ISO) require risk assessment, training, use of personal protective equipment (PPE), and incident reporting. Safety management systems must be documented and regularly audited. Emergency response plans and regular drills are required. Regulatory agencies may conduct inspections and enforce compliance. Worker engagement and safety culture are critical for incident prevention. Non-compliance can result in fines, shutdowns, and reputational damage.
        """,
        key_factors=[
            "Risk assessment", "Training", "PPE", "Incident reporting", "Emergency response"
        ],
        primary_authority=["OSHA", "ISO 45001", "DOE Safety Guidelines"],
        burden_holder="Site operator",
        adversary_position="Safety compliance increases operational costs.",
        counter_arguments=[
            "Safety reduces incident costs and liability.",
            "Worker engagement improves productivity.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate safety management systems and regular audits for all sites.",
        entity_scope="All geothermal operations.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHA 29 CFR 1910; ISO 45001 (2018)"
    ),
    DoctrineBlock(
        topic="Geothermal Community Engagement and Social License",
        keywords=[
            "community engagement", "social license", "stakeholder consultation", "public acceptance", "transparency"
        ],
        conclusion_template="Community engagement is required to secure social license for geothermal projects.",
        reasoning_framework="""
            Social license refers to ongoing community acceptance of a project. Engagement involves early and transparent consultation, addressing concerns, and sharing project benefits. Regulatory processes may require public hearings and comment periods. Community benefit agreements can formalize commitments. Ongoing communication and grievance mechanisms support long-term acceptance. Failure to secure social license can delay or halt projects. Documentation of engagement activities and outcomes is required for permitting and financing.
        """,
        key_factors=[
            "Stakeholder identification", "Consultation process", "Benefit sharing", "Documentation"
        ],
        primary_authority=["World Bank ESMAP", "DOE Community Engagement Guidelines", "IEA Geothermal"],
        burden_holder="Project developer",
        adversary_position="Community engagement increases project complexity and may raise expectations.",
        counter_arguments=[
            "Early engagement reduces risk of opposition.",
            "Benefit sharing builds support.",
            "Transparency supports regulatory compliance."
        ],
        resolution_strategy="Mandate engagement plans and documentation for all projects.",
        entity_scope="All geothermal projects.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="World Bank ESMAP Community Engagement (2017); DOE GTO"
    ),
    DoctrineBlock(
        topic="Geothermal Greenhouse Gas (GHG) Emissions Reporting",
        keywords=[
            "GHG emissions", "reporting", "CO2", "H2S", "regulatory compliance", "monitoring"
        ],
        conclusion_template="GHG emissions reporting is required for all geothermal power plants.",
        reasoning_framework="""
            Geothermal plants emit greenhouse gases (CO2, H2S, CH4) at lower rates than fossil plants but must comply with reporting requirements. Continuous emissions monitoring systems (CEMS) are used for real-time data collection. Regulatory frameworks (EPA, EU ETS) specify reporting thresholds and methods. Accurate reporting supports compliance, market participation, and public transparency. Emissions reduction strategies (e.g., abatement, reinjection) should be documented. Non-compliance can result in penalties and loss of incentives.
        """,
        key_factors=[
            "Monitoring systems", "Reporting standards", "Regulatory thresholds", "Reduction strategies"
        ],
        primary_authority=["EPA GHG Reporting Program", "EU ETS", "DOE Emissions Guidelines"],
        burden_holder="Plant operator",
        adversary_position="Reporting requirements add administrative burden.",
        counter_arguments=[
            "Accurate reporting supports incentives and market access.",
            "Automated systems reduce labor.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Mandate CEMS and regular reporting for all plants.",
        entity_scope="All geothermal power plants.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA GHG Reporting (2018); EU ETS"
    ),
    DoctrineBlock(
        topic="Geothermal Technology Innovation and Intellectual Property",
        keywords=[
            "technology innovation", "intellectual property", "patents", "R&D", "licensing"
        ],
        conclusion_template="Intellectual property protection is essential for geothermal technology innovation and commercialization.",
        reasoning_framework="""
            Innovation in geothermal technology (drilling, power conversion, monitoring) drives efficiency and cost reduction. Intellectual property (IP) protection (patents, trade secrets) incentivizes R&D investment and enables commercialization. IP management includes patent filing, licensing agreements, and freedom-to-operate analysis. Regulatory compliance with patent laws is required. Collaboration with research institutions and industry partners can accelerate innovation. Documentation of IP strategy and portfolio is required for investors and partners.
        """,
        key_factors=[
            "Patent filing", "Licensing", "Freedom-to-operate", "Collaboration"
        ],
        primary_authority=["USPTO", "WIPO", "DOE Technology Transfer Office"],
        burden_holder="Technology developer",
        adversary_position="IP protection increases costs and may limit technology diffusion.",
        counter_arguments=[
            "Licensing enables broader adoption.",
            "IP protection incentivizes innovation.",
            "Collaboration can balance access and protection."
        ],
        resolution_strategy="Mandate IP strategy documentation for all funded R&D projects.",
        entity_scope="All geothermal technology development projects.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="USPTO Patent Law; DOE Technology Transfer"
    ),
    DoctrineBlock(
        topic="Geothermal Drilling Fluid Selection and Management",
        keywords=[
            "drilling fluid", "mud selection", "fluid management", "wellbore stability", "environmental compliance"
        ],
        conclusion_template="Drilling fluid selection and management must ensure wellbore stability and environmental compliance.",
        reasoning_framework="""
            Drilling fluids maintain wellbore stability, cool the bit, and transport cuttings. Fluid selection depends on formation properties, temperature, and environmental regulations. Water-based, oil-based, and synthetic fluids have different performance and environmental profiles. Fluid management includes solids control, loss circulation prevention, and waste disposal. Regulatory agencies require documentation of fluid composition and disposal methods. Monitoring of fluid properties is required throughout drilling. Non-compliance can result in penalties and well failure.
        """,
        key_factors=[
            "Fluid selection", "Wellbore stability", "Environmental compliance", "Waste management"
        ],
        primary_authority=["API RP 13B", "DOE Drilling Guidelines", "State regulatory agencies"],
        burden_holder="Drilling engineer",
        adversary_position="Strict fluid management increases drilling costs.",
        counter_arguments=[
            "Proper fluid management prevents costly well failures.",
            "Environmental compliance is required.",
            "Advances in fluid technology reduce costs."
        ],
        resolution_strategy="Mandate fluid management plans and regulatory reporting for all drilling operations.",
        entity_scope="All geothermal drilling projects.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B (2017); DOE Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Reservoir Stimulation Chemical Use and Disclosure",
        keywords=[
            "stimulation chemicals", "disclosure", "EGS", "regulatory compliance", "environmental impact"
        ],
        conclusion_template="Full disclosure of stimulation chemicals is required for all EGS operations.",
        reasoning_framework="""
            Chemical additives are used in hydraulic stimulation for EGS to enhance fracture creation and fluid flow. Regulatory agencies require disclosure of chemical composition, concentration, and potential environmental impacts. Disclosure supports public transparency and risk assessment. Alternatives analysis should minimize hazardous chemical use. Monitoring of groundwater and surface water is required to detect contamination. Non-compliance can result in permit revocation and public opposition.
        """,
        key_factors=[
            "Chemical composition", "Disclosure requirements", "Alternatives analysis", "Environmental monitoring"
        ],
        primary_authority=["EPA", "DOE EGS Guidelines", "State regulatory agencies"],
        burden_holder="EGS operator",
        adversary_position="Disclosure may reveal proprietary information.",
        counter_arguments=[
            "Public transparency builds trust.",
            "Alternatives analysis protects proprietary interests.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Mandate full disclosure and alternatives analysis for all stimulation operations.",
        entity_scope="All EGS projects.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Disclosure Rules (2017); DOE EGS Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Project Decommissioning Planning",
        keywords=[
            "decommissioning", "planning", "cost estimation", "regulatory compliance", "financial assurance"
        ],
        conclusion_template="Decommissioning plans and financial assurance are required for all geothermal projects.",
        reasoning_framework="""
            Decommissioning involves removal of facilities, well plugging, and site restoration at project end-of-life. Regulatory agencies require decommissioning plans and cost estimates as a permit condition. Financial assurance (bonds, escrow) ensures funds are available for closure. Plans must address environmental protection, waste disposal, and community impacts. Periodic review and update of decommissioning plans are required. Non-compliance can result in penalties and long-term liability.
        """,
        key_factors=[
            "Plan documentation", "Cost estimation", "Financial assurance", "Regulatory review"
        ],
        primary_authority=["DOE Decommissioning Guidelines", "State regulatory agencies", "EPA"],
        burden_holder="Project operator",
        adversary_position="Decommissioning planning increases upfront costs.",
        counter_arguments=[
            "Financial assurance protects public interest.",
            "Proper planning reduces long-term risk.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate decommissioning plans and financial assurance for all projects.",
        entity_scope="All geothermal projects.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOE Guidelines (2016); State agencies"
    ),
    DoctrineBlock(
        topic="Geothermal Well Blowout Prevention and Emergency Response",
        keywords=[
            "blowout prevention", "emergency response", "well control", "BOP", "training"
        ],
        conclusion_template="Blowout prevention and emergency response plans are required for all geothermal drilling operations.",
        reasoning_framework="""
            Blowouts are uncontrolled releases of geothermal fluids and pose safety and environmental risks. Blowout prevention equipment (BOPs) must be installed and tested according to API and ISO standards. Emergency response plans include training, drills, and coordination with local authorities. Incident reporting and root cause analysis are required after any event. Regulatory agencies may inspect BOPs and review emergency plans. Non-compliance can result in fines and permit revocation.
        """,
        key_factors=[
            "BOP installation", "Training", "Emergency response plan", "Incident reporting"
        ],
        primary_authority=["API RP 53", "ISO 13535", "DOE Safety Guidelines"],
        burden_holder="Drilling contractor",
        adversary_position="BOP requirements increase drilling costs.",
        counter_arguments=[
            "Blowout prevention protects lives and environment.",
            "Regulatory compliance is mandatory.",
            "Training reduces incident risk."
        ],
        resolution_strategy="Mandate BOP installation and emergency response plans for all drilling operations.",
        entity_scope="All geothermal drilling projects.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 53 (2015); ISO 13535 (2000)"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Exploration Permitting",
        keywords=[
            "exploration permitting", "regulatory compliance", "environmental review", "stakeholder consultation"
        ],
        conclusion_template="Exploration permits and environmental review are required before any geothermal drilling.",
        reasoning_framework="""
            Exploration activities (drilling, geophysics) require permits from federal, state, or local agencies. Permitting includes environmental review, stakeholder consultation, and documentation of planned activities. Agencies may require baseline studies and mitigation plans. Public notice and comment periods are common. Non-compliance can delay or halt exploration. Documentation of permit conditions and compliance is required for future development.
        """,
        key_factors=[
            "Permit application", "Environmental review", "Stakeholder consultation", "Compliance documentation"
        ],
        primary_authority=["BLM", "State regulatory agencies", "DOE GTO"],
        burden_holder="Project developer",
        adversary_position="Permitting delays increase project risk.",
        counter_arguments=[
            "Early planning streamlines permitting.",
            "Compliance is required for project advancement.",
            "Stakeholder engagement reduces opposition."
        ],
        resolution_strategy="Mandate permit acquisition and compliance documentation for all exploration activities.",
        entity_scope="All geothermal exploration projects.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="BLM Exploration Permitting (2016); State agencies"
    ),
    DoctrineBlock(
        topic="Geothermal Reservoir Tracer Testing",
        keywords=[
            "tracer testing", "reservoir characterization", "fluid flow", "breakthrough", "monitoring"
        ],
        conclusion_template="Tracer testing is required for reservoir characterization and reinjection optimization.",
        reasoning_framework="""
            Tracer testing involves injecting chemical or isotopic tracers into the reservoir and monitoring their return in production wells. Results provide data on fluid flow paths, breakthrough times, and reservoir connectivity. Tracer selection must consider environmental safety and detection limits. Regulatory agencies may require tracer testing for reinjection permitting. Data inform reservoir models and reinjection strategy. Documentation of tracer protocols and results is required for regulatory review.
        """,
        key_factors=[
            "Tracer selection", "Sampling protocol", "Data analysis", "Regulatory compliance"
        ],
        primary_authority=["DOE Tracer Testing Guidelines", "USGS", "State regulatory agencies"],
        burden_holder="Reservoir engineer",
        adversary_position="Tracer testing adds cost and operational complexity.",
        counter_arguments=[
            "Improved reservoir understanding optimizes production.",
            "Regulatory compliance is required.",
            "Environmental safety is ensured by tracer selection."
        ],
        resolution_strategy="Mandate tracer testing for all reinjection operations and major reservoir studies.",
        entity_scope="All geothermal fields with reinjection.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOE Guidelines (2016); USGS"
    ),
    DoctrineBlock(
        topic="Geothermal Power Purchase Agreement (PPA) Structuring",
        keywords=[
            "PPA", "contract structuring", "offtake agreement", "pricing", "risk allocation"
        ],
        conclusion_template="PPAs must be structured to allocate risks and ensure project bankability.",
        reasoning_framework="""
            Power Purchase Agreements (PPAs) define the terms for sale of geothermal electricity. Key elements include pricing, term, delivery obligations, and risk allocation (resource, curtailment, force majeure). Lenders require PPAs to be bankable, with clear remedies for non-performance. Regulatory compliance with market and environmental rules is required. Negotiation should consider project economics, market conditions, and stakeholder interests. Documentation of PPA terms and compliance is required for financing and permitting.
        """,
        key_factors=[
            "Pricing structure", "Risk allocation", "Term length", "Regulatory compliance"
        ],
        primary_authority=["DOE PPA Guidelines", "World Bank ESMAP", "IEA Geothermal"],
        burden_holder="Project developer",
        adversary_position="Rigid PPAs may limit project flexibility.",
        counter_arguments=[
            "Bankable PPAs are required for financing.",
            "Risk allocation protects all parties.",
            "Negotiation can address flexibility."
        ],
        resolution_strategy="Mandate PPA review and risk allocation analysis for all financed projects.",
        entity_scope="All geothermal power projects.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="DOE PPA Guidelines (2017); World Bank ESMAP"
    ),
    DoctrineBlock(
        topic="Geothermal Field Development Planning",
        keywords=[
            "field development", "planning", "phased development", "infrastructure", "resource management"
        ],
        conclusion_template="Comprehensive field development planning is required for all geothermal projects.",
        reasoning_framework="""
            Field development planning integrates resource assessment, drilling, infrastructure, and environmental management. Phased development reduces risk and optimizes investment. Plans must address well placement, production strategy, reinjection, and infrastructure needs (roads, pipelines, power lines). Regulatory agencies require submission and approval of development plans. Adaptive management allows for plan updates as new data become available. Documentation of planning process and stakeholder input is required.
        """,
        key_factors=[
            "Resource assessment", "Phased development", "Infrastructure planning", "Regulatory approval"
        ],
        primary_authority=["DOE Field Development Guidelines", "USGS", "IEA Geothermal"],
        burden_holder="Project developer",
        adversary_position="Comprehensive planning increases upfront costs.",
        counter_arguments=[
            "Phased development reduces risk.",
            "Regulatory compliance is required.",
            "Adaptive management optimizes outcomes."
        ],
        resolution_strategy="Mandate submission and periodic review of development plans for all projects.",
        entity_scope="All geothermal field developments.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOE Guidelines (2016); USGS"
    ),
    DoctrineBlock(
        topic="Geothermal Project Insurance Requirements",
        keywords=[
            "insurance", "risk management", "exploration insurance", "construction insurance", "operational insurance"
        ],
        conclusion_template="Insurance coverage is required for all major project phases to manage risk.",
        reasoning_framework="""
            Insurance products (exploration, construction, operational) protect against financial loss from unforeseen events. Exploration insurance covers drilling failure; construction insurance covers accidents and delays; operational insurance covers equipment failure and business interruption. Lenders and regulators require proof of insurance for project approval. Documentation of coverage, claims history, and risk management practices is required. Periodic review ensures adequate coverage as project risks evolve.
        """,
        key_factors=[
            "Coverage type", "Claims history", "Risk management", "Regulatory requirements"
        ],
        primary_authority=["World Bank ESMAP", "DOE Insurance Guidelines", "Private insurers"],
        burden_holder="Project developer",
        adversary_position="Insurance premiums increase project costs.",
        counter_arguments=[
            "Insurance protects against catastrophic loss.",
            "Coverage is required for financing.",
            "Risk management may reduce premiums."
        ],
        resolution_strategy="Mandate insurance coverage and documentation for all major project phases.",
        entity_scope="All geothermal projects.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="World Bank ESMAP (2014); DOE Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Resource Exploration Geophysics Standards",
        keywords=[
            "geophysics", "exploration", "magnetotellurics", "seismic surveys", "gravity", "data integration"
        ],
        conclusion_template="Geophysical surveys must follow recognized standards and be integrated with other exploration data.",
        reasoning_framework="""
            Geophysical methods (magnetotellurics, seismic, gravity, resistivity) provide critical data for geothermal exploration. Survey design must consider target depth, resolution, and environmental impact. Data processing and interpretation follow SEG and EAGE standards. Integration with geological and geochemical data improves targeting. Regulatory agencies may require survey permits and environmental review. Documentation of survey protocols, data quality, and results is required for reporting and permitting.
        """,
        key_factors=[
            "Survey design", "Data processing", "Integration", "Regulatory compliance"
        ],
        primary_authority=["SEG", "EAGE", "DOE Geophysics Guidelines"],
        burden_holder="Exploration geophysicist",
        adversary_position="Geophysical surveys are expensive and may not guarantee success.",
        counter_arguments=[
            "Integrated data improves drilling success.",
            "Standards ensure data quality.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate standards-based surveys and data integration for all exploration projects.",
        entity_scope="All geothermal exploration projects.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SEG Standards (2017); DOE Guidelines"
    ),
    DoctrineBlock(
        topic="Geothermal Well Cementing Practices",
        keywords=[
            "cementing", "well integrity", "thermal stability", "API standards", "cement bond log"
        ],
        conclusion_template="Well cementing must follow API and ISO standards to ensure long-term integrity.",
        reasoning_framework="""
            Cementing secures casing and prevents fluid migration. High-temperature geothermal wells require thermally stable cement blends and additives. Cementing practices follow API and ISO standards for mixing, placement, and testing. Cement bond logs verify integrity. Regulatory agencies require documentation of cementing procedures and test results. Poor cementing can lead to well failure and environmental contamination. Periodic integrity testing is required during well life.
        """,
        key_factors=[
            "Cement blend", "Placement technique", "Integrity testing", "Regulatory documentation"
        ],
        primary_authority=["API Spec 10A", "ISO 10426", "DOE Well Integrity Guidelines"],
        burden_holder="Well engineer",
        adversary_position="Specialized cement blends increase costs.",
        counter_arguments=[
            "Integrity failures are more costly.",
            "Regulatory compliance is required.",
            "Testing ensures quality."
        ],
        resolution_strategy="Mandate standards-based cementing and integrity testing for all wells.",
        entity_scope="All geothermal wells.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API Spec 10A (2019); ISO 10426"
    ),
    DoctrineBlock(
        topic="Geothermal Well Testing for Production Allocation",
        keywords=[
            "well testing", "production allocation", "flow testing", "regulatory compliance", "data reporting"
        ],
        conclusion_template="Well testing is required to allocate production and comply with regulatory reporting.",
        reasoning_framework="""
            Flow testing determines well productivity and supports allocation of production among wells and stakeholders. Testing protocols follow API and ASTM standards. Results inform reservoir management, royalty calculation, and regulatory reporting. Data quality control includes calibration and repeat testing. Regulatory agencies require submission of test data. Documentation of testing procedures and results is required for audits and compliance.
        """,
        key_factors=[
            "Testing protocol", "Data quality", "Allocation method", "Regulatory reporting"
        ],
        primary_authority=["API RP 53", "ASTM D5753", "DOE Guidelines"],
        burden_holder="Production engineer",
        adversary_position="Testing increases operational costs.",
        counter_arguments=[
            "Accurate allocation supports fair revenue sharing.",
            "Testing informs reservoir management.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate regular well testing and data submission for all production wells.",
        entity_scope="All geothermal production wells.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 53 (2015); ASTM D5753"
    ),
    DoctrineBlock(
        topic="Geothermal Power Plant Water Use and Conservation",
        keywords=[
            "water use", "conservation", "cooling", "makeup water", "regulatory compliance"
        ],
        conclusion_template="Water use must be minimized and managed for all geothermal power plants.",
        reasoning_framework="""
            Geothermal plants use water for cooling, steam generation, and reinjection. Water conservation strategies include air-cooled condensers, closed-loop systems, and recycling. Regulatory agencies may limit water withdrawals and require conservation plans. Monitoring of water use and reporting are required for compliance. Community engagement is important in water-scarce regions. Documentation of water management practices is required for permitting and audits.
        """,
        key_factors=[
            "Water conservation", "Cooling technology", "Monitoring", "Regulatory compliance"
        ],
        primary_authority=["DOE Water Use Guidelines", "EPA", "State water agencies"],
        burden_holder="Plant operator",
        adversary_position="Water conservation technologies may increase capital costs.",
        counter_arguments=[
            "Water scarcity increases long-term risk.",
            "Conservation supports community acceptance.",
            "Regulatory compliance is required."
        ],
        resolution_strategy="Mandate water conservation plans and monitoring for all plants.",
        entity_scope="All geothermal power plants.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DOE Guidelines (2017); EPA"
    ),
    DoctrineBlock(
        topic="Geothermal Wellhead Equipment Standards",
        keywords=[
            "wellhead equipment", "API standards", "thermal rating", "pressure rating", "maintenance"
        ],
        conclusion_template="Wellhead equipment must meet API and ISO standards for temperature and pressure.",
        reasoning_framework="""
            Geothermal wellheads operate at high temperatures and pressures. Equipment selection must meet API and ISO standards for ratings and materials. Regular inspection and maintenance are required to ensure safety and reliability. Regulatory agencies may require documentation of equipment specifications and maintenance records. Non-compliance can result in equipment failure and regulatory penalties.
        """,
        key_factors=[
            "Equipment rating", "Material selection", "Inspection", "Regulatory documentation"
        ],
        primary_authority=["API Spec 6A", "ISO 10423", "DOE Guidelines"],
        burden_holder="Well operator",
        adversary_position="High-spec equipment increases costs.",
        counter_arguments=[
            "Equipment failure risks safety and production.",
            "Regulatory compliance is required.",
            "Maintenance extends equipment life."
        ],
        resolution_strategy="Mandate standards-based equipment and maintenance for all wellheads.",
        entity_scope="All geothermal wells.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API Spec 6A (2018); ISO 10423"
    ),
    DoctrineBlock(
        topic="Geothermal Field Environmental Monitoring",
        keywords=[
            "environmental monitoring", "baseline studies", "air quality", "water quality", "biodiversity"
        ],
        conclusion_template="Environmental monitoring is required throughout the project lifecycle.",
        reasoning_framework="""
            Baseline and ongoing environmental monitoring track project impacts on air, water, soil, and biodiversity. Monitoring protocols follow EPA and state standards. Data inform adaptive management and regulatory compliance. Community engagement and transparent reporting build trust. Documentation of monitoring protocols and results