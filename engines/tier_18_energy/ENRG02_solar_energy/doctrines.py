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
        topic="Photovoltaic Cell Physics - p-n Junction Operation",
        keywords=["p-n junction", "photovoltaic", "cell physics", "charge separation", "semiconductor"],
        conclusion_template="The efficient operation of a photovoltaic cell relies on the creation and maintenance of a p-n junction, enabling charge separation and current generation under illumination.",
        reasoning_framework="""
        The p-n junction forms the fundamental basis for photovoltaic cell operation. When photons strike the semiconductor material, electron-hole pairs are generated. The built-in electric field at the junction separates these carriers, allowing electrons to flow toward the n-type region and holes toward the p-type region. This separation prevents recombination and enables an external circuit to collect the generated current. The efficiency of this process depends on junction quality, doping concentrations, and material purity. Defects or improper doping can increase recombination rates, reducing cell efficiency. The photovoltaic effect is maximized by optimizing junction depth, surface passivation, and minimizing series resistance.
        """,
        key_factors=["junction quality", "doping concentration", "material purity", "surface passivation", "series resistance"],
        primary_authority=["IEEE Photovoltaic Standards", "IEC 61215"],
        burden_holder="Cell Manufacturer",
        adversary_position="The junction may not be optimal, leading to reduced efficiency.",
        counter_arguments=["Advanced manufacturing techniques ensure junction quality.", "Quality control protocols minimize defects."],
        resolution_strategy="Require certification to IEC 61215 and third-party testing.",
        entity_scope="Photovoltaic cell manufacturers and system integrators",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IEC 61215 Section 4.2"
    ),
    DoctrineBlock(
        topic="Monocrystalline vs Polycrystalline Silicon Technology",
        keywords=["monocrystalline", "polycrystalline", "silicon", "cell efficiency", "manufacturing"],
        conclusion_template="Monocrystalline silicon cells offer higher efficiency and longer lifespan compared to polycrystalline, but at increased manufacturing cost.",
        reasoning_framework="""
        Monocrystalline silicon cells are produced from a single crystal structure, resulting in fewer grain boundaries and higher carrier mobility. This leads to higher conversion efficiencies (typically 19-22%) and improved longevity due to reduced recombination. Polycrystalline cells, made from multiple crystal fragments, are less expensive to produce but suffer from lower efficiency (15-17%) due to grain boundary recombination. The choice between technologies depends on project economics, available space, and performance requirements. Recent advances in polycrystalline manufacturing have narrowed the efficiency gap, but monocrystalline remains preferred for space-constrained or premium applications.
        """,
        key_factors=["cell efficiency", "cost", "longevity", "grain boundaries", "project economics"],
        primary_authority=["NREL Silicon PV Reports", "IEC 61215"],
        burden_holder="System Designer",
        adversary_position="Polycrystalline offers sufficient performance at lower cost.",
        counter_arguments=["Monocrystalline's higher efficiency justifies cost in many applications.", "Space constraints favor monocrystalline."],
        resolution_strategy="Perform cost-benefit analysis and site-specific evaluation.",
        entity_scope="PV system designers and procurement teams",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NREL Silicon PV Efficiency Chart"
    ),
    DoctrineBlock(
        topic="Thin-Film Technologies - CdTe and CIGS",
        keywords=["thin-film", "CdTe", "CIGS", "photovoltaic", "module"],
        conclusion_template="CdTe and CIGS thin-film modules provide competitive efficiency and lower manufacturing costs, but face challenges in scalability and material availability.",
        reasoning_framework="""
        Thin-film photovoltaic technologies, including Cadmium Telluride (CdTe) and Copper Indium Gallium Selenide (CIGS), offer advantages in lower material usage and flexible substrates. CdTe modules have achieved efficiencies up to 18%, with cost-effective manufacturing and strong performance in low-light conditions. CIGS modules reach similar efficiencies but require rare materials, impacting scalability. Both technologies are less susceptible to temperature-induced losses compared to silicon. However, concerns over cadmium toxicity and indium scarcity limit widespread adoption. Regulatory compliance and recycling programs mitigate environmental risks. Thin-film modules are ideal for large-scale utility projects and applications requiring lightweight or flexible panels.
        """,
        key_factors=["efficiency", "material availability", "toxicity", "temperature performance", "manufacturing cost"],
        primary_authority=["First Solar Technical Reports", "IEC 61646"],
        burden_holder="Module Manufacturer",
        adversary_position="Thin-film modules are less efficient and pose environmental risks.",
        counter_arguments=["Modern recycling programs address toxicity.", "Thin-film modules excel in specific applications."],
        resolution_strategy="Mandate compliance with IEC 61646 and environmental regulations.",
        entity_scope="Thin-film module manufacturers and project developers",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="IEC 61646 Section 5.3"
    ),
    DoctrineBlock(
        topic="Perovskite Solar Cells - Emerging Technology",
        keywords=["perovskite", "emerging technology", "solar cell", "efficiency", "stability"],
        conclusion_template="Perovskite solar cells demonstrate high efficiency potential but require further development to address stability and scalability challenges.",
        reasoning_framework="""
        Perovskite solar cells have rapidly advanced, achieving laboratory efficiencies exceeding 25%. Their tunable bandgap and low-cost fabrication make them attractive for future PV applications. However, issues with long-term stability, moisture sensitivity, and lead content hinder commercial viability. Research focuses on encapsulation techniques, lead-free perovskites, and tandem cell integration. While perovskites may revolutionize the PV industry, current deployments are limited to pilot projects and research settings. Regulatory approval and lifecycle analysis are necessary before widespread adoption.
        """,
        key_factors=["efficiency", "stability", "scalability", "lead content", "regulatory approval"],
        primary_authority=["Nature Energy Perovskite Reviews", "DOE SunShot Initiative"],
        burden_holder="Research Consortium",
        adversary_position="Perovskite cells are not commercially viable due to instability.",
        counter_arguments=["Encapsulation improves stability.", "Lead-free perovskites are under development."],
        resolution_strategy="Support pilot projects and monitor regulatory progress.",
        entity_scope="PV researchers and technology developers",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="DOE SunShot Perovskite Roadmap"
    ),
    DoctrineBlock(
        topic="Solar Module Design - Cell Stringing and Bypass Diodes",
        keywords=["module design", "cell stringing", "bypass diodes", "shading", "reliability"],
        conclusion_template="Proper cell stringing and integration of bypass diodes are essential for minimizing shading losses and ensuring module reliability.",
        reasoning_framework="""
        Solar modules are constructed by stringing individual cells in series and parallel configurations. Bypass diodes are installed across cell strings to prevent hot-spot formation and reduce power loss under partial shading. Without bypass diodes, shaded cells can cause reverse bias, leading to overheating and permanent damage. The number and placement of diodes depend on module architecture and expected shading patterns. Quality assurance protocols require diode testing and thermal imaging to verify performance. Module reliability is enhanced by robust interconnections and encapsulation.
        """,
        key_factors=["cell stringing", "bypass diode placement", "shading", "hot-spot prevention", "reliability"],
        primary_authority=["IEC 61215", "UL 1703"],
        burden_holder="Module Designer",
        adversary_position="Bypass diodes increase complexity and cost.",
        counter_arguments=["Bypass diodes prevent costly failures.", "Industry standards require their use."],
        resolution_strategy="Enforce compliance with IEC 61215 and UL 1703.",
        entity_scope="Module designers and manufacturers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61215 Section 6.4"
    ),
    DoctrineBlock(
        topic="Inverter Technologies - String vs Micro vs Central",
        keywords=["inverter", "string inverter", "micro inverter", "central inverter", "system design"],
        conclusion_template="The choice of inverter technology impacts system performance, reliability, and maintenance; string inverters suit medium systems, microinverters optimize module-level performance, and central inverters scale for utility projects.",
        reasoning_framework="""
        Inverter selection depends on system size, layout, and performance goals. String inverters are cost-effective for residential and commercial systems, offering easy maintenance and moderate granularity. Microinverters provide module-level optimization, reducing shading losses and simplifying monitoring, but increase upfront cost and complexity. Central inverters are used in large utility-scale installations, offering high efficiency and centralized control, but require extensive maintenance and have lower fault tolerance. Hybrid solutions, such as power optimizers, combine benefits. System designers must evaluate site conditions, shading, redundancy needs, and maintenance capabilities.
        """,
        key_factors=["system size", "shading", "maintenance", "cost", "performance optimization"],
        primary_authority=["IEEE 1547", "UL 1741"],
        burden_holder="System Designer",
        adversary_position="Microinverters are too costly for most applications.",
        counter_arguments=["Microinverters reduce lifetime losses.", "Central inverters are more efficient at scale."],
        resolution_strategy="Conduct site-specific analysis and adhere to IEEE 1547.",
        entity_scope="PV system designers and installers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEEE 1547 Section 7"
    ),
    DoctrineBlock(
        topic="MPPT Algorithms - Perturb and Observe vs Incremental Conductance",
        keywords=["MPPT", "maximum power point tracking", "perturb and observe", "incremental conductance", "algorithm"],
        conclusion_template="Incremental conductance MPPT algorithms provide faster and more accurate tracking under rapidly changing irradiance compared to perturb and observe.",
        reasoning_framework="""
        Maximum Power Point Tracking (MPPT) algorithms optimize PV output by adjusting operating voltage/current. Perturb and Observe (P&O) is simple and widely used, but can oscillate around the MPP and respond slowly to rapid irradiance changes. Incremental Conductance (IncCond) calculates the slope of the power curve, enabling precise tracking and faster response. IncCond is preferred in environments with frequent shading or cloud cover, while P&O suffices for stable conditions. Hybrid algorithms and adaptive tuning further enhance performance. Algorithm selection impacts energy yield and inverter efficiency.
        """,
        key_factors=["irradiance variability", "algorithm complexity", "tracking speed", "energy yield", "inverter efficiency"],
        primary_authority=["IEEE Transactions on Power Electronics", "IEC 61727"],
        burden_holder="Inverter Manufacturer",
        adversary_position="P&O is sufficient and less complex.",
        counter_arguments=["IncCond improves yield in dynamic environments.", "Hybrid algorithms are feasible."],
        resolution_strategy="Require algorithm benchmarking and field validation.",
        entity_scope="Inverter manufacturers and system integrators",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Power Electronics Vol. 34"
    ),
    DoctrineBlock(
        topic="Solar Resource Assessment - GHI, DNI, DHI",
        keywords=["solar resource", "GHI", "DNI", "DHI", "irradiance", "assessment"],
        conclusion_template="Accurate solar resource assessment using GHI, DNI, and DHI is critical for PV system sizing and yield estimation.",
        reasoning_framework="""
        Solar resource assessment quantifies available irradiance using Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), and Diffuse Horizontal Irradiance (DHI). GHI measures total solar energy on a horizontal surface, DNI captures direct beam component, and DHI represents scattered light. Site-specific measurements, satellite data, and meteorological models inform system design and yield projections. Errors in assessment lead to undersized or oversized systems and financial risk. Standard protocols require at least one year of site data or validated satellite estimates. Uncertainty analysis and sensitivity studies improve confidence.
        """,
        key_factors=["irradiance measurement", "site data", "model accuracy", "uncertainty", "yield estimation"],
        primary_authority=["NREL Solar Resource Handbook", "IEC 61724"],
        burden_holder="Project Developer",
        adversary_position="Satellite data is sufficient for all projects.",
        counter_arguments=["Ground measurements improve accuracy.", "Uncertainty analysis is essential."],
        resolution_strategy="Mandate site-specific measurement for large projects.",
        entity_scope="Project developers and resource analysts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NREL Solar Resource Handbook Section 3"
    ),
    DoctrineBlock(
        topic="PV System Sizing Methodology - DC-to-AC Ratio",
        keywords=["system sizing", "DC-to-AC ratio", "oversizing", "inverter", "performance"],
        conclusion_template="Optimal DC-to-AC ratio balances inverter clipping losses and maximizes energy yield, typically ranging from 1.1 to 1.3 for commercial systems.",
        reasoning_framework="""
        The DC-to-AC ratio defines the relationship between PV array capacity and inverter rating. Oversizing the array increases energy yield during low irradiance but causes inverter clipping during peak production. Undersizing reduces yield and system value. Industry practice recommends ratios between 1.1 and 1.3 for commercial systems, with higher ratios for utility-scale projects in high irradiance regions. Factors influencing ratio selection include site irradiance profile, inverter efficiency, and economic analysis. Clipping losses are quantified and balanced against increased annual production. Regulatory constraints and warranty terms may limit allowable ratios.
        """,
        key_factors=["irradiance profile", "inverter efficiency", "clipping losses", "annual yield", "regulatory constraints"],
        primary_authority=["NREL PV System Design Guidelines", "IEC 61727"],
        burden_holder="System Designer",
        adversary_position="Higher DC-to-AC ratios lead to wasted energy.",
        counter_arguments=["Annual yield increases justify clipping losses.", "Economic analysis supports oversizing."],
        resolution_strategy="Perform site-specific modeling and adhere to guidelines.",
        entity_scope="PV system designers and project developers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NREL PV System Design Guidelines Section 5"
    ),
    DoctrineBlock(
        topic="Fixed-Tilt vs Single-Axis Tracker Systems",
        keywords=["fixed-tilt", "single-axis tracker", "system design", "energy yield", "maintenance"],
        conclusion_template="Single-axis trackers increase energy yield by 15-25% compared to fixed-tilt systems but require higher upfront cost and maintenance.",
        reasoning_framework="""
        Fixed-tilt PV systems are simpler, with lower installation and maintenance costs, but capture less irradiance throughout the day. Single-axis trackers follow the sun's path, increasing yield by 15-25% depending on latitude and site conditions. Trackers are more complex, requiring motors, sensors, and regular maintenance. The decision depends on land availability, project economics, and O&M capabilities. Trackers are favored in utility-scale projects with high irradiance and low land cost. Reliability improvements and predictive maintenance have reduced tracker downtime.
        """,
        key_factors=["energy yield", "maintenance", "upfront cost", "site conditions", "project economics"],
        primary_authority=["NREL Tracker Performance Reports", "IEC 62817"],
        burden_holder="Project Developer",
        adversary_position="Trackers are unreliable and costly.",
        counter_arguments=["Modern trackers have improved reliability.", "Yield gains offset maintenance costs."],
        resolution_strategy="Conduct lifecycle cost analysis and adhere to IEC 62817.",
        entity_scope="Project developers and EPC contractors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NREL Tracker Performance Reports Section 2"
    ),
    DoctrineBlock(
        topic="Concentrated Solar Power - Parabolic Trough vs Power Tower",
        keywords=["concentrated solar power", "parabolic trough", "power tower", "thermal storage", "efficiency"],
        conclusion_template="Power tower CSP systems achieve higher efficiency and storage integration compared to parabolic troughs, but require larger scale and higher capital investment.",
        reasoning_framework="""
        Concentrated Solar Power (CSP) technologies include parabolic troughs and power towers. Parabolic troughs use curved mirrors to focus sunlight onto a receiver tube, heating fluid for steam generation. Power towers employ heliostats to concentrate sunlight onto a central receiver, enabling higher operating temperatures and efficiency. Power towers integrate thermal storage more effectively, supporting dispatchable generation. However, they require larger land area and higher capital investment. Site selection, water availability, and grid integration are critical. Environmental impact assessments and permitting processes influence technology choice.
        """,
        key_factors=["efficiency", "thermal storage", "capital investment", "site requirements", "environmental impact"],
        primary_authority=["DOE CSP Reports", "IEA Technology Roadmap"],
        burden_holder="Project Developer",
        adversary_position="Parabolic troughs are proven and less risky.",
        counter_arguments=["Power towers offer superior performance.", "Storage integration supports grid stability."],
        resolution_strategy="Evaluate site suitability and perform comparative analysis.",
        entity_scope="CSP project developers and investors",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="DOE CSP Reports Section 4"
    ),
    DoctrineBlock(
        topic="Battery Storage Integration - Lithium-Ion vs Flow Batteries",
        keywords=["battery storage", "lithium-ion", "flow battery", "integration", "system design"],
        conclusion_template="Lithium-ion batteries dominate short-duration storage, while flow batteries offer scalability and longer discharge times for large-scale PV integration.",
        reasoning_framework="""
        Battery storage enhances PV system flexibility and supports grid stability. Lithium-ion batteries are widely adopted due to high energy density, rapid response, and declining costs. They are best suited for short-duration applications (1-4 hours). Flow batteries, such as vanadium redox, provide scalable capacity and longer discharge times, ideal for large-scale or long-duration storage. Flow batteries have lower energy density and higher upfront cost but offer extended cycle life and easier maintenance. System designers must match storage technology to application requirements, considering safety, lifecycle, and regulatory compliance.
        """,
        key_factors=["energy density", "discharge duration", "scalability", "cost", "cycle life"],
        primary_authority=["DOE Energy Storage Handbook", "UL 9540"],
        burden_holder="System Integrator",
        adversary_position="Lithium-ion is sufficient for all storage needs.",
        counter_arguments=["Flow batteries scale better for long-duration.", "Safety and cycle life favor flow batteries in some cases."],
        resolution_strategy="Perform application-specific analysis and adhere to UL 9540.",
        entity_scope="System integrators and storage providers",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Energy Storage Handbook Section 6"
    ),
    DoctrineBlock(
        topic="Grid-Tied vs Off-Grid System Design",
        keywords=["grid-tied", "off-grid", "system design", "interconnection", "reliability"],
        conclusion_template="Grid-tied systems offer higher reliability and economic benefits, while off-grid designs require robust storage and backup solutions.",
        reasoning_framework="""
        Grid-tied PV systems connect to the utility grid, enabling net metering and reducing reliance on storage. They are more cost-effective and reliable, leveraging grid backup during low production. Off-grid systems operate independently, requiring oversized arrays, battery storage, and backup generators to ensure continuous supply. Off-grid design must account for worst-case scenarios and seasonal variability. Regulatory requirements, site accessibility, and maintenance capabilities influence system choice. Hybrid systems combine features for remote or critical applications.
        """,
        key_factors=["reliability", "storage requirements", "cost", "regulatory compliance", "site accessibility"],
        primary_authority=["IEEE 1547", "UL 1741"],
        burden_holder="System Designer",
        adversary_position="Off-grid systems are more resilient.",
        counter_arguments=["Grid-tied systems offer economic advantages.", "Off-grid requires significant investment."],
        resolution_strategy="Evaluate site needs and regulatory context.",
        entity_scope="PV system designers and end users",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE 1547 Section 9"
    ),
    DoctrineBlock(
        topic="PV System Losses - Soiling, Shading, Mismatch, Temperature",
        keywords=["system losses", "soiling", "shading", "mismatch", "temperature", "performance"],
        conclusion_template="Mitigating soiling, shading, mismatch, and temperature losses is essential for maximizing PV system performance and yield.",
        reasoning_framework="""
        PV system losses arise from environmental and operational factors. Soiling reduces irradiance by dust and debris accumulation, requiring regular cleaning. Shading from nearby objects causes partial string losses and hot-spot risks. Mismatch losses occur when cells or modules operate at different points due to manufacturing tolerances or degradation. Temperature increases reduce cell efficiency, especially in high-irradiance regions. Loss quantification and mitigation strategies include site layout optimization, module selection, cleaning schedules, and thermal management. Monitoring systems detect and address losses in real time.
        """,
        key_factors=["soiling rate", "shading patterns", "module mismatch", "temperature effects", "maintenance"],
        primary_authority=["IEC 61724", "NREL Loss Analysis Reports"],
        burden_holder="System Operator",
        adversary_position="Losses are unavoidable and difficult to quantify.",
        counter_arguments=["Advanced monitoring enables loss detection.", "Mitigation strategies reduce impact."],
        resolution_strategy="Implement monitoring and maintenance protocols.",
        entity_scope="System operators and maintenance teams",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61724 Section 8"
    ),
    DoctrineBlock(
        topic="NEC Article 690 - Code Compliance",
        keywords=["NEC 690", "code compliance", "electrical safety", "PV system", "installation"],
        conclusion_template="Compliance with NEC Article 690 is mandatory for PV system safety, covering wiring, grounding, and disconnect requirements.",
        reasoning_framework="""
        NEC Article 690 governs electrical installation standards for PV systems in the United States. It addresses wiring methods, grounding, overcurrent protection, and disconnects to ensure safety and prevent fire hazards. Installers must follow prescribed cable types, labeling, and conduit requirements. Ground-fault protection and rapid shutdown provisions are enforced. Non-compliance results in inspection failure, liability, and increased risk. Regular training and certification are necessary for installers. Local amendments may apply, requiring site-specific review.
        """,
        key_factors=["wiring methods", "grounding", "overcurrent protection", "disconnects", "rapid shutdown"],
        primary_authority=["NEC Article 690", "UL 1703"],
        burden_holder="Installer",
        adversary_position="Code compliance increases installation cost.",
        counter_arguments=["Safety benefits outweigh cost.", "Non-compliance risks liability."],
        resolution_strategy="Require certified installers and inspection.",
        entity_scope="Installers and inspectors",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="NEC Article 690 Section 690.12"
    ),
    DoctrineBlock(
        topic="Bifacial Modules and Albedo",
        keywords=["bifacial module", "albedo", "energy yield", "ground reflectance", "system design"],
        conclusion_template="Bifacial modules increase energy yield by capturing reflected irradiance; system design must optimize albedo and module elevation.",
        reasoning_framework="""
        Bifacial modules generate power from both front and rear surfaces, leveraging ground reflectance (albedo) to boost yield. Albedo depends on ground cover, color, and moisture. Module elevation and tilt influence rear-side irradiance. System designers must model albedo accurately and select site materials to maximize performance. Bifacial gains range from 5-30% depending on site conditions. Monitoring and validation are required to confirm yield. Industry standards for bifacial testing and modeling are emerging.
        """,
        key_factors=["albedo", "module elevation", "ground cover", "tilt angle", "yield validation"],
        primary_authority=["IEC TS 60904-1-2", "NREL Bifacial Reports"],
        burden_holder="System Designer",
        adversary_position="Bifacial gains are uncertain and difficult to predict.",
        counter_arguments=["Advanced modeling improves prediction.", "Field validation confirms performance."],
        resolution_strategy="Require bifacial modeling and yield validation.",
        entity_scope="System designers and project developers",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="IEC TS 60904-1-2 Section 3"
    ),
    DoctrineBlock(
        topic="Agrivoltaics - Dual Use of Land",
        keywords=["agrivoltaics", "dual use", "land", "crop yield", "PV integration"],
        conclusion_template="Agrivoltaics enables dual land use, optimizing crop yield and PV generation, but requires site-specific analysis and stakeholder engagement.",
        reasoning_framework="""
        Agrivoltaics integrates PV systems with agricultural activities, enabling simultaneous crop cultivation and energy generation. System design must account for crop type, shading tolerance, and irrigation needs. PV array spacing, height, and orientation influence microclimate and yield. Stakeholder engagement, including farmers and local authorities, is critical for project success. Economic analysis considers land lease, crop value, and energy revenue. Pilot projects demonstrate benefits, but site-specific modeling and monitoring are necessary.
        """,
        key_factors=["crop type", "array spacing", "microclimate", "stakeholder engagement", "economic analysis"],
        primary_authority=["NREL Agrivoltaics Reports", "DOE Energy-Water Nexus"],
        burden_holder="Project Developer",
        adversary_position="PV arrays reduce crop yield and disrupt farming.",
        counter_arguments=["Proper design maintains or improves yield.", "Dual revenue streams benefit stakeholders."],
        resolution_strategy="Conduct pilot studies and engage stakeholders.",
        entity_scope="Project developers and agricultural partners",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="NREL Agrivoltaics Reports Section 2"
    ),
    DoctrineBlock(
        topic="Floating Solar (Floatovoltaics)",
        keywords=["floating solar", "floatovoltaics", "water body", "module cooling", "land use"],
        conclusion_template="Floating solar installations optimize land use and module cooling, but require robust anchoring and environmental assessment.",
        reasoning_framework="""
        Floating solar systems are deployed on water bodies, reducing land footprint and benefiting from module cooling, which improves efficiency. Design challenges include anchoring, mooring, and resistance to wind and wave forces. Environmental assessment addresses impacts on aquatic ecosystems, water quality, and local stakeholders. Maintenance protocols must account for accessibility and corrosion risks. Floatovoltaics are ideal for reservoirs, irrigation ponds, and industrial water bodies. Regulatory approval and site-specific engineering are mandatory.
        """,
        key_factors=["anchoring", "module cooling", "environmental impact", "maintenance", "regulatory approval"],
        primary_authority=["NREL Floating Solar Reports", "IEC 61215"],
        burden_holder="Project Developer",
        adversary_position="Floating systems are costly and environmentally risky.",
        counter_arguments=["Cooling improves efficiency.", "Environmental risks are mitigated by proper assessment."],
        resolution_strategy="Require environmental impact study and engineering review.",
        entity_scope="Project developers and site owners",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="NREL Floating Solar Reports Section 3"
    ),
    DoctrineBlock(
        topic="Solar + Storage Economics - ITC and PTC",
        keywords=["solar storage", "economics", "ITC", "PTC", "incentives", "project finance"],
        conclusion_template="Investment Tax Credit (ITC) and Production Tax Credit (PTC) significantly improve solar + storage project economics, requiring compliance with eligibility criteria.",
        reasoning_framework="""
        The ITC and PTC are federal incentives supporting solar and storage deployment. ITC provides a percentage-based credit on capital investment, while PTC rewards energy production. Eligibility depends on project size, storage integration, and compliance with prevailing wage and domestic content requirements. Financial modeling must account for incentive timing, depreciation, and tax equity structures. Regulatory changes and sunset provisions impact long-term economics. Developers must maintain documentation and engage tax advisors.
        """,
        key_factors=["incentive eligibility", "project finance", "regulatory compliance", "tax equity", "documentation"],
        primary_authority=["IRS Notice 2018-59", "DOE Incentive Reports"],
        burden_holder="Project Developer",
        adversary_position="Incentives are complex and uncertain.",
        counter_arguments=["Professional advisors simplify compliance.", "Incentives drive project viability."],
        resolution_strategy="Engage tax advisors and maintain compliance documentation.",
        entity_scope="Project developers and investors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2018-59 Section 4"
    ),
    DoctrineBlock(
        topic="Solar Thermal Systems - Flat Plate vs Evacuated Tube",
        keywords=["solar thermal", "flat plate", "evacuated tube", "collector", "efficiency"],
        conclusion_template="Evacuated tube collectors offer superior performance in cold and cloudy conditions, while flat plate collectors are cost-effective for moderate climates.",
        reasoning_framework="""
        Solar thermal collectors convert solar energy to heat for water or space heating. Flat plate collectors are simple, inexpensive, and effective in moderate climates. Evacuated tube collectors minimize heat loss, achieving higher efficiency in cold or cloudy environments. Tube design enables selective absorption and insulation. System designers must match collector type to climate, load profile, and budget. Maintenance and installation complexity differ between technologies. Regulatory standards ensure performance and safety.
        """,
        key_factors=["climate", "collector efficiency", "cost", "maintenance", "installation complexity"],
        primary_authority=["SRCC OG-100", "DOE Solar Thermal Reports"],
        burden_holder="System Designer",
        adversary_position="Flat plate collectors suffice for most applications.",
        counter_arguments=["Evacuated tubes excel in challenging climates.", "Long-term savings justify higher cost."],
        resolution_strategy="Perform climate-specific analysis and adhere to SRCC OG-100.",
        entity_scope="System designers and installers",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SRCC OG-100 Section 5"
    ),
    DoctrineBlock(
        topic="PV Module Recycling and End-of-Life Management",
        keywords=["module recycling", "end-of-life", "waste management", "environmental compliance", "circular economy"],
        conclusion_template="PV module recycling and end-of-life management are essential for environmental compliance and resource recovery, requiring adherence to regulatory standards.",
        reasoning_framework="""
        PV modules reach end-of-life after 25-30 years, necessitating recycling to recover valuable materials and minimize environmental impact. Regulatory frameworks, such as EU WEEE Directive, mandate collection and processing. Recycling technologies separate glass, silicon, metals, and encapsulants. Manufacturers and installers must plan for take-back programs and documentation. Environmental compliance reduces liability and supports circular economy goals. Industry standards are evolving for module recycling certification.
        """,
        key_factors=["recycling technology", "regulatory compliance", "resource recovery", "take-back programs", "documentation"],
        primary_authority=["EU WEEE Directive", "DOE PV Recycling Reports"],
        burden_holder="Module Manufacturer",
        adversary_position="Recycling increases cost and complexity.",
        counter_arguments=["Resource recovery offsets cost.", "Regulations mandate recycling."],
        resolution_strategy="Establish take-back programs and certify recycling partners.",
        entity_scope="Manufacturers, installers, and regulators",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="EU WEEE Directive Article 13"
    ),
    DoctrineBlock(
        topic="PV Module Warranty and Performance Guarantees",
        keywords=["module warranty", "performance guarantee", "degradation", "bankability", "insurance"],
        conclusion_template="Module warranties and performance guarantees protect project bankability, requiring clear terms on degradation rates and coverage.",
        reasoning_framework="""
        PV module warranties typically cover product defects (10-12 years) and performance (25 years). Performance guarantees specify allowable degradation rates, usually 0.5-0.7% per year. Clear warranty terms and insurance coverage support project financing and investor confidence. Manufacturers must document testing and certification. Disputes are resolved through independent testing and arbitration. Bankability depends on warranty credibility and insurer backing.
        """,
        key_factors=["warranty duration", "degradation rate", "insurance", "testing", "bankability"],
        primary_authority=["IEC 61215", "BloombergNEF Bankability Reports"],
        burden_holder="Module Manufacturer",
        adversary_position="Warranties are difficult to enforce.",
        counter_arguments=["Insurance and arbitration support enforcement.", "Industry standards mandate clear terms."],
        resolution_strategy="Require third-party certification and insurance.",
        entity_scope="Manufacturers, investors, and project developers",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="BloombergNEF Bankability Reports Section 7"
    ),
    DoctrineBlock(
        topic="PV System Monitoring and Data Analytics",
        keywords=["system monitoring", "data analytics", "performance", "O&M", "yield optimization"],
        conclusion_template="Advanced monitoring and data analytics enable real-time performance optimization and predictive maintenance for PV systems.",
        reasoning_framework="""
        PV system monitoring collects real-time data on production, losses, and faults. Data analytics identify trends, optimize yield, and support predictive maintenance. Monitoring platforms integrate sensors, communication, and cloud analytics. O&M teams use alerts and diagnostics to reduce downtime. Industry standards require minimum data points and reporting intervals. Analytics improve asset management and investor confidence.
        """,
        key_factors=["data quality", "analytics platform", "O&M", "predictive maintenance", "reporting"],
        primary_authority=["IEC 61724", "NREL Monitoring Reports"],
        burden_holder="System Operator",
        adversary_position="Monitoring adds cost and complexity.",
        counter_arguments=["Yield optimization offsets cost.", "Downtime reduction improves ROI."],
        resolution_strategy="Mandate monitoring for large projects and adhere to IEC 61724.",
        entity_scope="Operators, O&M teams, and investors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61724 Section 10"
    ),
    DoctrineBlock(
        topic="PV Module Fire Safety and Risk Mitigation",
        keywords=["fire safety", "risk mitigation", "module", "installation", "code compliance"],
        conclusion_template="PV module fire safety requires compliance with UL 1703 and local codes, including fire rating, installation practices, and risk mitigation.",
        reasoning_framework="""
        Fire safety is critical for PV installations. Modules must meet fire rating standards (UL 1703, IEC 61730) and be installed per code. Risk mitigation includes proper wiring, spacing, and rapid shutdown. Fire risk increases with poor installation or incompatible materials. Installers must train and certify to reduce liability. Fire departments require access and labeling. Insurance coverage depends on compliance.
        """,
        key_factors=["fire rating", "installation practices", "rapid shutdown", "insurance", "training"],
        primary_authority=["UL 1703", "IEC 61730"],
        burden_holder="Installer",
        adversary_position="Fire safety standards increase cost.",
        counter_arguments=["Insurance requires compliance.", "Risk mitigation protects assets."],
        resolution_strategy="Mandate certified installers and fire department coordination.",
        entity_scope="Installers, inspectors, and site owners",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="UL 1703 Section 11"
    ),
    DoctrineBlock(
        topic="PV Array Grounding and Lightning Protection",
        keywords=["grounding", "lightning protection", "array", "safety", "code compliance"],
        conclusion_template="Proper grounding and lightning protection are essential for PV array safety, requiring compliance with NEC and IEC standards.",
        reasoning_framework="""
        PV arrays are vulnerable to lightning and electrical faults. Grounding systems dissipate fault currents and protect equipment. Lightning protection includes surge arrestors, bonding, and grounding rods. NEC and IEC standards specify grounding methods and materials. Poor grounding increases risk of equipment damage and fire. Installers must document and inspect grounding systems. Insurance and warranty coverage depend on compliance.
        """,
        key_factors=["grounding method", "surge protection", "inspection", "documentation", "insurance"],
        primary_authority=["NEC Article 690", "IEC 62305"],
        burden_holder="Installer",
        adversary_position="Grounding adds complexity and cost.",
        counter_arguments=["Safety and insurance require grounding.", "Risk reduction justifies investment."],
        resolution_strategy="Require inspection and documentation.",
        entity_scope="Installers, inspectors, and site owners",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 62305 Section 8"
    ),
    DoctrineBlock(
        topic="PV System Commissioning and Acceptance Testing",
        keywords=["commissioning", "acceptance testing", "system performance", "quality assurance", "documentation"],
        conclusion_template="Commissioning and acceptance testing validate PV system performance and quality, requiring documentation and third-party verification.",
        reasoning_framework="""
        Commissioning ensures PV systems meet design and performance criteria. Acceptance testing includes visual inspection, electrical measurements, and functional tests. Documentation covers test results, as-built drawings, and certification. Third-party verification increases confidence and supports warranty claims. Quality assurance protocols reduce risk of early failures and performance issues. Industry standards specify minimum test requirements.
        """,
        key_factors=["test protocol", "documentation", "third-party verification", "quality assurance", "warranty"],
        primary_authority=["IEC 62446", "NREL Commissioning Guidelines"],
        burden_holder="Installer",
        adversary_position="Testing delays project completion.",
        counter_arguments=["Testing prevents costly failures.", "Documentation supports warranty and financing."],
        resolution_strategy="Mandate acceptance testing and third-party review.",
        entity_scope="Installers, owners, and investors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62446 Section 3"
    ),
    DoctrineBlock(
        topic="PV System Operations and Maintenance (O&M) Best Practices",
        keywords=["O&M", "operations", "maintenance", "best practices", "performance"],
        conclusion_template="O&M best practices maximize PV system performance and lifespan, requiring scheduled maintenance, monitoring, and documentation.",
        reasoning_framework="""
        Operations and Maintenance (O&M) protocols include scheduled inspections, cleaning, performance monitoring, and corrective actions. Best practices reduce downtime, optimize yield, and extend system lifespan. Documentation supports warranty claims and regulatory compliance. O&M teams require training and access to monitoring platforms. Industry standards specify minimum maintenance intervals and reporting requirements.
        """,
        key_factors=["maintenance schedule", "monitoring", "training", "documentation", "performance optimization"],
        primary_authority=["IEC 62446", "NREL O&M Reports"],
        burden_holder="System Operator",
        adversary_position="O&M increases operational cost.",
        counter_arguments=["Yield optimization offsets cost.", "Downtime reduction improves ROI."],
        resolution_strategy="Mandate O&M protocols and training.",
        entity_scope="Operators, O&M teams, and owners",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NREL O&M Reports Section 5"
    ),
    DoctrineBlock(
        topic="PV System Interconnection and Grid Compliance",
        keywords=["interconnection", "grid compliance", "utility", "regulatory", "system design"],
        conclusion_template="PV system interconnection requires compliance with utility and regulatory standards, including IEEE 1547 and local codes.",
        reasoning_framework="""
        Interconnection protocols ensure PV systems operate safely and reliably with the utility grid. Compliance includes voltage regulation, anti-islanding, and communication requirements. Utilities review interconnection applications and perform site inspections. Regulatory standards, such as IEEE 1547, specify technical criteria. Non-compliance results in rejection or operational restrictions. System designers must document and submit interconnection studies.
        """,
        key_factors=["voltage regulation", "anti-islanding", "communication", "documentation", "utility review"],
        primary_authority=["IEEE 1547", "UL 1741"],
        burden_holder="System Designer",
        adversary_position="Interconnection delays project deployment.",
        counter_arguments=["Compliance ensures safety and reliability.", "Documentation streamlines approval."],
        resolution_strategy="Engage utilities early and adhere to standards.",
        entity_scope="System designers, utilities, and regulators",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE 1547 Section 4"
    ),
    DoctrineBlock(
        topic="PV System Cybersecurity and Data Privacy",
        keywords=["cybersecurity", "data privacy", "system monitoring", "communication", "risk mitigation"],
        conclusion_template="PV system cybersecurity and data privacy require secure communication, access control, and compliance with data protection regulations.",
        reasoning_framework="""
        PV systems increasingly rely on networked monitoring and control platforms. Cybersecurity risks include unauthorized access, data breaches, and operational disruption. Best practices include secure communication protocols, access control, regular software updates, and incident response planning. Data privacy regulations, such as GDPR, require consent and protection of personal information. System operators must document security measures and train staff.
        """,
        key_factors=["secure communication", "access control", "regulatory compliance", "incident response", "training"],
        primary_authority=["NIST Cybersecurity Framework", "GDPR"],
        burden_holder="System Operator",
        adversary_position="Cybersecurity adds complexity and cost.",
        counter_arguments=["Risk mitigation protects assets and data.", "Regulations mandate compliance."],
        resolution_strategy="Implement cybersecurity protocols and training.",
        entity_scope="Operators, IT teams, and owners",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="NIST Cybersecurity Framework Section 2"
    ),
    DoctrineBlock(
        topic="PV System Financial Modeling and Bankability",
        keywords=["financial modeling", "bankability", "project finance", "risk assessment", "yield prediction"],
        conclusion_template="Robust financial modeling and bankability assessment are essential for PV project viability, requiring accurate yield prediction and risk analysis.",
        reasoning_framework="""
        Financial modeling quantifies project costs, revenue, and risks. Bankability assessment evaluates technology, warranties, and insurance. Yield prediction uses resource assessment and loss modeling. Investors require transparent documentation and third-party validation. Risk analysis covers technical, financial, and regulatory factors. Industry standards support consistent modeling and reporting.
        """,
        key_factors=["yield prediction", "risk assessment", "warranty", "insurance", "documentation"],
        primary_authority=["BloombergNEF Bankability Reports", "NREL Financial Modeling Guidelines"],
        burden_holder="Project Developer",
        adversary_position="Financial modeling is uncertain and subjective.",
        counter_arguments=["Industry standards improve consistency.", "Third-party validation increases confidence."],
        resolution_strategy="Mandate standardized modeling and validation.",
        entity_scope="Developers, investors, and lenders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="BloombergNEF Bankability Reports Section 2"
    ),
    DoctrineBlock(
        topic="PV System Environmental Impact Assessment",
        keywords=["environmental impact", "assessment", "site selection", "regulatory compliance", "stakeholder engagement"],
        conclusion_template="Environmental impact assessment is mandatory for large PV projects, requiring site analysis, regulatory compliance, and stakeholder engagement.",
        reasoning_framework="""
        Environmental impact assessment (EIA) evaluates PV project effects on land, water, wildlife, and communities. Regulatory frameworks mandate EIA for large or sensitive sites. Site analysis includes land use, habitat, water quality, and visual impact. Stakeholder engagement addresses concerns and supports permitting. Mitigation measures reduce adverse effects. Documentation and monitoring are required for compliance.
        """,
        key_factors=["site analysis", "regulatory compliance", "stakeholder engagement", "mitigation", "documentation"],
        primary_authority=["DOE Environmental Impact Guidelines", "EPA NEPA"],
        burden_holder="Project Developer",
        adversary_position="EIA delays project deployment.",
        counter_arguments=["Mitigation supports community acceptance.", "Regulations mandate EIA."],
        resolution_strategy="Engage stakeholders early and adhere to guidelines.",
        entity_scope="Developers, regulators, and communities",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="EPA NEPA Section 102"
    ),
    DoctrineBlock(
        topic="PV System Insurance and Risk Management",
        keywords=["insurance", "risk management", "project finance", "loss mitigation", "coverage"],
        conclusion_template="Comprehensive insurance and risk management protect PV projects from financial loss, requiring coverage for equipment, liability, and business interruption.",
        reasoning_framework="""
        PV project insurance covers equipment, liability, and business interruption. Risk management includes loss mitigation, documentation, and compliance. Insurers require project documentation, warranty terms, and maintenance records. Claims are supported by monitoring and incident reports. Risk assessment informs coverage selection and premium negotiation. Industry standards support consistent risk management.
        """,
        key_factors=["coverage", "documentation", "loss mitigation", "risk assessment", "premium negotiation"],
        primary_authority=["BloombergNEF Insurance Reports", "NREL Risk Management Guidelines"],
        burden_holder="Project Developer",
        adversary_position="Insurance increases project cost.",
        counter_arguments=["Insurance protects against catastrophic loss.", "Risk management reduces premiums."],
        resolution_strategy="Mandate insurance and risk management protocols.",
        entity_scope="Developers, insurers, and investors",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="BloombergNEF Insurance Reports Section 4"
    ),
    DoctrineBlock(
        topic="PV System Decommissioning and Site Restoration",
        keywords=["decommissioning", "site restoration", "end-of-life", "regulatory compliance", "environmental impact"],
        conclusion_template="PV system decommissioning and site restoration require regulatory compliance and environmental mitigation, including removal, recycling, and land rehabilitation.",
        reasoning_framework="""
        Decommissioning removes PV equipment and restores site conditions. Regulatory frameworks mandate removal, recycling, and environmental mitigation. Site restoration includes soil remediation, vegetation replanting, and documentation. Developers must plan for end-of-life and engage stakeholders. Industry standards support consistent decommissioning and restoration.
        """,
        key_factors=["removal", "recycling", "site restoration", "regulatory compliance", "documentation"],
        primary_authority=["DOE Decommissioning Guidelines", "EU WEEE Directive"],
        burden_holder="Project Developer",
        adversary_position="Decommissioning increases end-of-life cost.",
        counter_arguments=["Planning reduces cost and impact.", "Regulations mandate restoration."],
        resolution_strategy="Mandate decommissioning plans and stakeholder engagement.",
        entity_scope="Developers, regulators, and communities",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="DOE Decommissioning Guidelines Section 6"
    ),
    DoctrineBlock(
        topic="PV System Microgrid Integration",
        keywords=["microgrid", "integration", "PV system", "islanding", "resilience"],
        conclusion_template="PV system microgrid integration enhances resilience and supports islanding, requiring advanced controls and regulatory compliance.",
        reasoning_framework="""
        Microgrids integrate PV, storage, and other resources to operate independently or with the grid. Integration requires advanced controls, communication, and protection schemes. Islanding supports resilience during grid outages. Regulatory compliance includes IEEE 1547 and local codes. System designers must document integration protocols and engage stakeholders. Monitoring and testing support reliability.
        """,
        key_factors=["advanced controls", "islanding", "regulatory compliance", "monitoring", "stakeholder engagement"],
        primary_authority=["IEEE 1547", "DOE Microgrid Guidelines"],
        burden_holder="System Designer",
        adversary_position="Microgrid integration increases complexity.",
        counter_arguments=["Resilience benefits justify investment.", "Regulations mandate compliance."],
        resolution_strategy="Mandate integration protocols and testing.",
        entity_scope="Designers, operators, and regulators",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Microgrid Guidelines Section 3"
    ),
    DoctrineBlock(
        topic="PV System Emergency Response and Disaster Recovery",
        keywords=["emergency response", "disaster recovery", "PV system", "resilience", "protocols"],
        conclusion_template="PV system emergency response and disaster recovery protocols enhance resilience and support rapid restoration, requiring planning and training.",
        reasoning_framework="""
        Emergency response protocols address PV system incidents, including fire, flood, and grid outage. Disaster recovery supports rapid restoration and asset protection. Planning includes risk assessment, communication, and training. Regulatory frameworks mandate emergency protocols for large projects. Documentation and drills improve response effectiveness.
        """,
        key_factors=["risk assessment", "planning", "training", "communication", "documentation"],
        primary_authority=["DOE Emergency Response Guidelines", "NREL Disaster Recovery Reports"],
        burden_holder="System Operator",
        adversary_position="Emergency protocols increase operational cost.",
        counter_arguments=["Resilience benefits justify investment.", "Regulations mandate protocols."],
        resolution_strategy="Mandate planning and training.",
        entity_scope="Operators, O&M teams, and regulators",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Emergency Response Guidelines Section 2"
    ),
    DoctrineBlock(
        topic="PV System Workforce Development and Training",
        keywords=["workforce development", "training", "certification", "installer", "O&M"],
        conclusion_template="Workforce development and training ensure PV system quality and safety, requiring certification and ongoing education.",
        reasoning_framework="""
        Workforce development supports PV industry growth and quality. Training and certification ensure installers and O&M teams meet standards. Ongoing education addresses technology evolution and regulatory changes. Industry standards specify minimum training requirements. Certification supports project financing and investor confidence.
        """,
        key_factors=["training", "certification", "ongoing education", "quality assurance", "regulatory compliance"],
        primary_authority=["NABCEP Certification", "DOE Workforce Development Reports"],
        burden_holder="Installer",
        adversary_position="Training increases project cost.",
        counter_arguments=["Quality and safety benefits justify investment.", "Certification supports financing."],
        resolution_strategy="Mandate certification and ongoing education.",
        entity_scope="Installers, O&M teams, and owners",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NABCEP Certification Guidelines Section 4"
    ),
    DoctrineBlock(
        topic="PV System Innovation and Technology Adoption",
        keywords=["innovation", "technology adoption", "PV system", "emerging technology", "performance"],
        conclusion_template="Innovation and technology adoption drive PV system performance and cost reduction, requiring risk assessment and pilot testing.",
        reasoning_framework="""
        Innovation accelerates PV system performance and cost reduction. Technology adoption includes new materials, designs, and controls. Risk assessment and pilot testing validate performance and reliability. Industry standards support adoption and certification. Stakeholder engagement addresses concerns and supports financing.
        """,
        key_factors=["risk assessment", "pilot testing", "performance", "certification", "stakeholder engagement"],
        primary_authority=["DOE Innovation Reports", "NREL Technology Adoption Guidelines"],
        burden_holder="Project Developer",
        adversary_position="Innovation increases risk and uncertainty.",
        counter_arguments=["Pilot testing reduces risk.", "Certification supports adoption."],
        resolution_strategy="Mandate pilot testing and certification.",
        entity_scope="Developers, investors, and regulators",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="DOE Innovation Reports Section 5"
    ),
    DoctrineBlock(
        topic="PV System Policy and Regulatory Advocacy",
        keywords=["policy", "regulatory advocacy", "PV system", "incentives", "stakeholder engagement"],
        conclusion_template="Policy and regulatory advocacy support PV system deployment, requiring stakeholder engagement and compliance with evolving frameworks.",
        reasoning_framework="""
        Policy and regulatory advocacy influence PV system deployment and incentives. Stakeholder engagement supports policy development and compliance. Evolving frameworks require monitoring and adaptation. Documentation and communication improve advocacy effectiveness. Industry associations support advocacy and information sharing.
        """,
        key_factors=["stakeholder engagement", "policy monitoring", "documentation", "communication", "industry association"],
        primary_authority=["SEIA Policy Reports", "DOE Regulatory Guidelines"],
        burden_holder="Industry Association",
        adversary_position="Policy advocacy is costly and uncertain.",
        counter_arguments=["Advocacy supports industry growth.", "Compliance ensures project viability."],
        resolution_strategy="Engage stakeholders and monitor frameworks.",
        entity_scope="Industry associations, developers, and regulators",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="SEIA Policy Reports Section 2"
    ),
    DoctrineBlock(
        topic="PV System International Standards and Harmonization",
        keywords=["international standards", "harmonization", "PV system", "certification", "global deployment"],
        conclusion_template="International standards and harmonization facilitate PV system certification and global deployment, requiring compliance and documentation.",
        reasoning_framework="""
        International standards harmonize PV system certification and deployment. Compliance supports global market access and investor confidence. Documentation and testing ensure performance and safety. Industry associations support harmonization and information sharing. Regulatory frameworks evolve to support harmonization.
        """,
        key_factors=["compliance", "documentation", "testing", "industry association", "regulatory framework"],
        primary_authority=["IEC Standards", "IEA Harmonization Reports"],
        burden_holder="Manufacturer",
        adversary_position="Harmonization increases complexity and cost.",
        counter_arguments=["Global access offsets cost.", "Certification supports investor confidence."],
        resolution_strategy="Mandate compliance and documentation.",
        entity_scope="Manufacturers, developers, and regulators",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="IEC Standards Section 4"
    ),
    DoctrineBlock(
        topic="PV System Lifecycle Assessment and Sustainability",
        keywords=["lifecycle assessment", "sustainability", "PV system", "environmental impact", "resource recovery"],
        conclusion_template="Lifecycle assessment and sustainability support PV system environmental compliance and resource recovery, requiring documentation and mitigation.",
        reasoning_framework="""
        Lifecycle assessment evaluates PV system environmental impact from manufacturing to end-of-life. Sustainability includes resource recovery, recycling, and mitigation. Documentation supports compliance and investor confidence. Industry standards specify assessment protocols. Stakeholder engagement supports sustainability goals.
        """,
        key_factors=["assessment protocol", "resource recovery", "documentation", "mitigation", "stakeholder engagement"],
        primary_authority=["DOE Sustainability Reports", "EU WEEE Directive"],
        burden_holder="Manufacturer",
        adversary_position="Lifecycle assessment increases cost.",
        counter_arguments=["Sustainability supports compliance and investor confidence.", "Mitigation reduces impact."],
        resolution_strategy="Mandate assessment and documentation.",
        entity_scope="Manufacturers, developers, and regulators",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Sustainability Reports Section 3"
    ),
    DoctrineBlock(
        topic="PV System Data Interoperability and Communication Standards",
        keywords=["data interoperability", "communication standards", "PV system", "monitoring", "integration"],
        conclusion_template="Data interoperability and communication standards enable PV system integration and monitoring, requiring compliance and documentation.",
        reasoning_framework="""
        Data interoperability supports PV system integration and monitoring. Communication standards ensure compatibility and reliability. Compliance supports asset management and investor confidence. Documentation and testing validate interoperability. Industry standards evolve to support integration and monitoring.
        """,
        key_factors=["compliance", "documentation", "testing", "integration", "asset management"],
        primary_authority=["IEC 61850", "IEEE Communication Standards"],
        burden_holder="System Designer",
        adversary_position="Interoperability increases complexity and cost.",
        counter_arguments=["Integration supports asset management and investor confidence.", "Standards reduce risk."],
        resolution_strategy="Mandate compliance and documentation.",
        entity_scope="Designers, operators, and regulators",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="IEC 61850 Section 2"
    ),
    DoctrineBlock(
        topic="PV System Asset Management and Portfolio Optimization",
        keywords=["asset management", "portfolio optimization", "PV system", "performance", "risk assessment"],
        conclusion_template="Asset management and portfolio optimization maximize PV system performance and financial returns, requiring monitoring and risk assessment.",
        reasoning_framework="""
        Asset management supports PV system performance and financial returns. Portfolio optimization includes monitoring, risk assessment, and maintenance. Industry standards specify asset management protocols. Documentation supports investor confidence and regulatory compliance. Analytics improve optimization and risk mitigation.
        """,
        key_factors=["monitoring", "risk assessment", "maintenance", "documentation", "analytics"],
        primary_authority=["NREL Asset Management Reports", "BloombergNEF Portfolio Optimization Guidelines"],
        burden_holder="Asset Manager",
        adversary_position="Asset management increases operational cost.",
        counter_arguments=["Optimization improves returns and reduces risk.", "Standards support compliance."],
        resolution_strategy="Mandate asset management protocols and analytics.",
        entity_scope="Asset managers, investors, and owners",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="BloombergNEF Portfolio Optimization Guidelines Section 5"
    ),
    DoctrineBlock(
        topic="PV System Distributed Generation and Net Metering",
        keywords=["distributed generation", "net metering", "PV system", "policy", "grid integration"],
        conclusion_template="Distributed generation and net metering support PV system deployment and grid integration, requiring policy compliance and stakeholder engagement.",
        reasoning_framework="""
        Distributed generation enables PV system deployment at multiple sites. Net metering policies support grid integration and financial returns. Compliance with policy and stakeholder engagement support deployment. Industry standards specify interconnection and metering protocols. Documentation supports regulatory compliance and investor confidence.
        """,
        key_factors=["policy compliance", "stakeholder engagement", "interconnection", "metering", "documentation"],
        primary_authority=["SEIA Net Metering Reports", "IEEE 1547"],
        burden_holder="Project Developer",
        adversary_position="Net metering increases grid complexity.",
        counter_arguments=["Policy supports deployment and returns.", "Standards support integration."],
        resolution_strategy="Mandate compliance and stakeholder engagement.",
        entity_scope="Developers, utilities, and regulators",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="SEIA Net Metering Reports Section 3"
    ),
    DoctrineBlock(
        topic="PV System Smart Grid Integration and Demand Response",
        keywords=["smart grid", "demand response", "PV system", "integration", "communication"],
        conclusion_template="Smart grid integration and demand response optimize PV system performance and grid stability, requiring advanced communication and compliance.",
        reasoning_framework="""
        Smart grid integration supports PV system performance and grid stability. Demand response enables flexible operation and optimization. Advanced communication protocols support integration and reliability. Compliance with standards and documentation support asset management and investor confidence. Industry standards evolve to support smart grid and demand response.
        """,
        key_factors=["communication", "integration", "asset management", "compliance", "optimization"],
        primary_authority=["IEEE Smart Grid Standards", "NREL Demand Response Reports"],
        burden_holder="System Designer",
        adversary_position="Smart grid integration increases complexity.",
        counter_arguments=["Optimization improves performance and stability.", "Standards support integration."],
        resolution_strategy="Mandate advanced communication and compliance.",
        entity_scope="Designers, operators, and utilities",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="IEEE Smart Grid Standards Section 7"
    ),
    DoctrineBlock(
        topic="PV System Hybridization with Wind and Other Renewables",
        keywords=["hybridization", "wind", "renewables", "PV system", "integration"],
        conclusion_template="Hybridization with wind and other renewables enhances PV system performance and reliability, requiring integration protocols and compliance.",
        reasoning_framework="""
        Hybridization integrates PV with wind and other renewables to optimize performance and reliability. Integration protocols support compatibility and asset management. Compliance with standards and documentation support investor confidence and regulatory approval. Industry standards evolve to support hybridization and integration.
        """,
        key_factors=["integration protocols", "compatibility", "asset management", "compliance", "documentation"],
        primary_authority=["DOE Hybridization Reports", "IEC Standards"],
        burden_holder="Project Developer",
        adversary_position="Hybridization increases complexity and cost.",
        counter_arguments=["Performance and reliability benefits justify investment.", "Standards support integration."],
        resolution_strategy="Mandate integration protocols and compliance.",
        entity_scope="Developers, operators, and regulators",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Hybridization Reports Section 4"
    ),
    DoctrineBlock(
        topic="PV System Climate Adaptation and Resilience",
        keywords=["climate adaptation", "resilience", "PV system", "site selection", "design"],
        conclusion_template="Climate adaptation and resilience support PV system performance and longevity, requiring site-specific design and mitigation protocols.",
        reasoning_framework="""
        Climate adaptation addresses PV system risks from extreme weather, temperature, and environmental changes. Resilience protocols include site-specific design, material selection, and mitigation measures. Compliance with standards and documentation support investor confidence and regulatory approval. Industry standards evolve to support climate adaptation and resilience.
        """,
        key_factors=["site-specific design", "material selection", "mitigation", "compliance", "documentation"],
        primary_authority=["DOE Climate Adaptation Reports", "NREL Resilience Guidelines"],
        burden_holder="System Designer",
        adversary_position="Adaptation increases design complexity and cost.",
        counter_arguments=["Performance and longevity benefits justify investment.", "Standards support adaptation."],
        resolution_strategy="Mandate site-specific design and mitigation protocols.",
        entity_scope="Designers, operators, and regulators",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="DOE Climate Adaptation Reports Section 2"
    ),
    DoctrineBlock(
        topic="PV System Social Impact and Community Engagement",
        keywords=["social impact", "community engagement", "PV system", "stakeholder", "deployment"],
        conclusion_template="Social impact and community engagement support PV system deployment and acceptance, requiring stakeholder communication and mitigation protocols.",
        reasoning_framework="""
        Social impact assessment evaluates PV system effects on communities. Community engagement supports deployment and acceptance. Stakeholder communication addresses concerns and supports mitigation. Compliance with standards and documentation support regulatory approval and investor confidence. Industry standards evolve to support social impact and engagement.
        """,
        key_factors=["stakeholder communication", "mitigation", "compliance", "documentation", "acceptance"],
        primary_authority=["DOE Social Impact Reports", "NREL Community Engagement Guidelines"],
        burden_holder="Project Developer",
        adversary_position="Community engagement increases project complexity.",
        counter_arguments=["Acceptance supports deployment and returns.", "Standards support engagement."],
        resolution_strategy="Mandate stakeholder communication and mitigation protocols.",
        entity_scope="Developers, communities, and regulators",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="DOE Social Impact Reports Section 3"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    result = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            result.append(doctrine)
    return result

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]