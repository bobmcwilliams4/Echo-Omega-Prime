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
        topic="Crude Oil Assay & TBP Distillation",
        keywords=["crude oil", "assay", "TBP", "distillation", "refinery feedstock"],
        conclusion_template="The crude oil assay and TBP distillation data determine the suitability and yield profile for refinery processing.",
        reasoning_framework=(
            "The crude oil assay provides a comprehensive characterization of the feedstock, including API gravity, sulfur content, metals, and boiling range distribution. "
            "True Boiling Point (TBP) distillation curves are used to predict product yields and guide unit operations. "
            "Assay data is integrated into linear programming models for refinery optimization. "
            "Key considerations include compatibility with downstream units, product specification compliance, and environmental constraints. "
            "The accuracy of the TBP curve directly impacts yield forecasting and economic evaluation. "
            "Assay interpretation requires cross-validation with historical unit performance and laboratory results. "
            "Refiners must ensure that the assay data is current and representative of the crude batch. "
            "Variability in crude quality can affect unit stability, catalyst life, and emissions. "
            "TBP data is also critical for process simulation and heat integration studies. "
            "Assay results are benchmarked against industry databases and regulatory standards. "
            "The selection of crude blends is optimized to maximize margin while minimizing operational risks. "
            "Assay discrepancies must be resolved through retesting or statistical reconciliation. "
            "TBP distillation is the reference method for cut point determination in refinery planning. "
            "The burden of proof lies with the refinery technical team to validate and interpret assay data. "
            "Disputes over assay accuracy are resolved through third-party laboratories or arbitration."
        ),
        key_factors=[
            "API gravity", "sulfur content", "metals", "TBP curve", "product yields", "unit compatibility", "regulatory compliance"
        ],
        primary_authority=[
            "ASTM D2892", "UOP 375", "API Technical Data Book", "Refinery LP Models"
        ],
        burden_holder="Refinery Technical Team",
        adversary_position="Assay data is outdated or not representative of current crude batch.",
        counter_arguments=[
            "Recent sampling and testing confirm assay validity.",
            "Historical performance aligns with current assay data.",
            "Third-party validation available."
        ],
        resolution_strategy="Independent laboratory retesting and reconciliation with historical data.",
        entity_scope="Refinery Feedstock Evaluation",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASTM D2892 Standard Practice"
    ),
    DoctrineBlock(
        topic="Atmospheric Distillation Column Tray Efficiency",
        keywords=["atmospheric distillation", "tray efficiency", "Murphree efficiency", "column design", "separation"],
        conclusion_template="Tray efficiency in atmospheric distillation columns is a critical parameter for accurate simulation and product quality control.",
        reasoning_framework=(
            "Tray efficiency, typically expressed as Murphree efficiency, quantifies the effectiveness of mass transfer between vapor and liquid phases on each tray. "
            "It is influenced by tray design, vapor and liquid rates, weeping, entrainment, and fouling. "
            "Accurate estimation of tray efficiency is essential for process simulation, cut point control, and energy optimization. "
            "Empirical correlations (e.g., O'Connell, Fair) are used for initial estimates, but actual efficiency should be validated with plant data. "
            "Low tray efficiency leads to poor separation, off-spec products, and increased reboiler duty. "
            "Regular monitoring and maintenance are required to sustain efficiency, including tray inspections and cleaning. "
            "Process upsets, such as foaming or flooding, can temporarily reduce efficiency. "
            "Advanced control systems can compensate for minor efficiency losses but cannot fully correct for mechanical failures. "
            "The burden of demonstrating adequate tray efficiency lies with process engineering. "
            "Disputes regarding efficiency are resolved through test runs and gamma scanning. "
            "Industry standards and vendor guarantees provide baseline expectations for new columns."
        ),
        key_factors=[
            "Murphree efficiency", "tray design", "vapor/liquid rates", "fouling", "column hydraulics"
        ],
        primary_authority=[
            "API 560", "Perry's Chemical Engineers' Handbook", "UOP Design Guides"
        ],
        burden_holder="Process Engineering",
        adversary_position="Reported tray efficiency is overestimated, leading to simulation errors.",
        counter_arguments=[
            "Recent test runs confirm separation performance.",
            "Gamma scan results support efficiency estimates.",
            "Vendor guarantees align with observed data."
        ],
        resolution_strategy="Conduct tray-by-tray performance tests and gamma scans.",
        entity_scope="Atmospheric Distillation Unit",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 560 Design Practices"
    ),
    DoctrineBlock(
        topic="Vacuum Distillation Reduced Crude",
        keywords=["vacuum distillation", "reduced crude", "cut point", "unit operation"],
        conclusion_template="Vacuum distillation of reduced crude enables further separation of heavy fractions, optimizing downstream conversion unit feedstocks.",
        reasoning_framework=(
            "Vacuum distillation operates at pressures below atmospheric to lower boiling points and prevent thermal cracking of heavy fractions. "
            "The reduced crude from atmospheric distillation is charged to the vacuum column, where it is separated into vacuum gas oil (VGO), light vacuum gas oil (LVGO), and vacuum resid. "
            "Cut points are selected based on downstream unit requirements, such as FCC or hydrocracking feed quality. "
            "Column internals (e.g., packing, trays) and ejector system performance are critical for achieving target separations. "
            "Overheating must be avoided to minimize coke formation and fouling. "
            "Vacuum system reliability directly impacts unit throughput and product yields. "
            "Product quality is monitored via ASTM D1160 distillation and sulfur/metals analysis. "
            "The burden of proof for optimal operation lies with the unit operations team. "
            "Disputes over cut point selection are resolved through yield and quality optimization studies. "
            "Industry best practices dictate regular maintenance of vacuum systems and column internals."
        ),
        key_factors=[
            "operating pressure", "cut point selection", "overflash", "column internals", "vacuum system reliability"
        ],
        primary_authority=[
            "API Technical Data Book", "ASTM D1160", "UOP Process Guidelines"
        ],
        burden_holder="Unit Operations Team",
        adversary_position="Current cut points do not maximize VGO yield or meet FCC feed specs.",
        counter_arguments=[
            "Recent product assays confirm compliance.",
            "Simulation studies support current cut points.",
            "Operational constraints limit further optimization."
        ],
        resolution_strategy="Iterative cut point adjustment and product quality monitoring.",
        entity_scope="Vacuum Distillation Unit",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API Vacuum Distillation Guidelines"
    ),
    DoctrineBlock(
        topic="Gasoil",
        keywords=["gasoil", "middle distillate", "hydrocracking", "FCC", "diesel"],
        conclusion_template="Gasoil fractions are processed in FCC or hydrocracking units to maximize light product yields and meet diesel specifications.",
        reasoning_framework=(
            "Gasoil is a middle distillate fraction obtained from atmospheric or vacuum distillation. "
            "Its properties, such as sulfur content, aromatics, and cetane index, determine its suitability for FCC or hydrocracking. "
            "FCC units convert gasoil to lighter products (gasoline, LPG), while hydrocrackers produce high-quality diesel and jet fuel. "
            "Feed pretreatment (hydrotreating) is often required to reduce sulfur and nitrogen. "
            "Product blending strategies are developed to meet regulatory and market specifications. "
            "Gasoil quality impacts catalyst life, conversion rates, and emissions. "
            "The burden of proof for gasoil utilization lies with process planning and optimization teams. "
            "Disputes over allocation are resolved through LP modeling and economic analysis. "
            "Industry standards specify test methods for gasoil characterization."
        ),
        key_factors=[
            "sulfur content", "aromatics", "cetane index", "feed pretreatment", "product blending"
        ],
        primary_authority=[
            "ASTM D4052", "EN 590", "API Data Book"
        ],
        burden_holder="Process Planning Team",
        adversary_position="Gasoil allocation to FCC reduces diesel pool quality.",
        counter_arguments=[
            "LP model optimizes overall margin.",
            "Hydrocracking capacity is fully utilized.",
            "Diesel blending pool remains within specs."
        ],
        resolution_strategy="Rebalance gasoil allocation based on updated market and unit constraints.",
        entity_scope="Middle Distillate Processing",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EN 590 Diesel Specifications"
    ),
    DoctrineBlock(
        topic="Residuum",
        keywords=["residuum", "vacuum residue", "coking", "asphalt", "fuel oil"],
        conclusion_template="Residuum management strategies include coking, blending for fuel oil, or asphalt production, depending on refinery configuration and market demand.",
        reasoning_framework=(
            "Residuum (vacuum residue) is the heaviest fraction remaining after vacuum distillation. "
            "It contains high levels of asphaltenes, metals, and sulfur, limiting its direct use as fuel. "
            "Coking units thermally crack residuum into lighter products and petroleum coke. "
            "Alternatively, residuum can be blended into bunker fuel or processed into asphalt. "
            "Residuum disposition is influenced by market demand, environmental regulations, and refinery complexity. "
            "Metals and sulfur content must be managed to avoid catalyst poisoning and emissions violations. "
            "The burden of proof for optimal residuum utilization lies with refinery planning. "
            "Disputes over residuum value are resolved through economic modeling and market analysis. "
            "Industry standards govern fuel oil and asphalt specifications."
        ),
        key_factors=[
            "asphaltene content", "metals", "sulfur", "market demand", "unit configuration"
        ],
        primary_authority=[
            "ASTM D4294", "ISO 8217", "API Data Book"
        ],
        burden_holder="Refinery Planning",
        adversary_position="Residuum coking is uneconomic compared to fuel oil blending.",
        counter_arguments=[
            "Coking increases overall light product yield.",
            "Fuel oil market is limited by sulfur regulations.",
            "Asphalt demand is seasonal and variable."
        ],
        resolution_strategy="Dynamic residuum allocation based on margin and regulatory compliance.",
        entity_scope="Heavy Ends Management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 8217 Marine Fuel Standards"
    ),
    DoctrineBlock(
        topic="Fluid Catalytic Cracking (FCC) Conversion & Octane",
        keywords=["FCC", "conversion", "octane", "catalyst", "gasoline"],
        conclusion_template="FCC unit conversion and octane performance are optimized through catalyst selection, operating conditions, and feed quality management.",
        reasoning_framework=(
            "FCC units convert heavy gasoil into lighter products, primarily gasoline and LPG. "
            "Conversion rate is controlled by reactor temperature, catalyst-to-oil ratio, and feed quality. "
            "Catalyst formulation (zeolite type, rare earth content) impacts activity, selectivity, and octane. "
            "Higher conversion typically increases gasoline yield but may reduce octane due to increased cracking severity. "
            "Feed contaminants (metals, nitrogen) can poison catalyst and reduce performance. "
            "Octane is measured as RON and MON, with blending strategies to meet pool specifications. "
            "The burden of proof for FCC optimization lies with process engineering and catalyst vendors. "
            "Disputes over conversion targets are resolved through test runs and economic evaluation. "
            "Industry standards specify test methods for product quality and catalyst performance."
        ),
        key_factors=[
            "reactor temperature", "catalyst-to-oil ratio", "feed contaminants", "octane number", "catalyst formulation"
        ],
        primary_authority=[
            "ASTM D2699", "ASTM D2700", "UOP FCC Guidelines"
        ],
        burden_holder="Process Engineering",
        adversary_position="Current FCC operation prioritizes yield over octane, risking off-spec gasoline.",
        counter_arguments=[
            "Blending pool remains within octane specs.",
            "Catalyst reformulation is under evaluation.",
            "Economic analysis supports current operation."
        ],
        resolution_strategy="Optimize catalyst and operating conditions to balance yield and octane.",
        entity_scope="FCC Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D2699 RON Testing"
    ),
    DoctrineBlock(
        topic="Hydrocracking Diesel",
        keywords=["hydrocracking", "diesel", "middle distillate", "catalyst", "ultra-low sulfur"],
        conclusion_template="Hydrocracking units produce high-quality diesel by converting heavy fractions under hydrogen pressure using bifunctional catalysts.",
        reasoning_framework=(
            "Hydrocracking is a catalytic process that uses hydrogen to convert heavy gasoil into lighter, high-value products, primarily diesel and jet fuel. "
            "The process operates at high pressure and temperature, with bifunctional catalysts providing both acidic and hydrogenation activity. "
            "Feed pretreatment is required to remove sulfur, nitrogen, and metals. "
            "Product diesel meets ultra-low sulfur specifications (10-15 ppm) and high cetane index. "
            "Hydrocracking severity is adjusted to balance diesel yield and product quality. "
            "Catalyst life and selectivity are monitored through regular testing and performance tracking. "
            "The burden of proof for hydrocracking performance lies with process engineering and catalyst suppliers. "
            "Disputes over diesel quality are resolved through laboratory analysis and catalyst change-out schedules. "
            "Industry standards specify diesel product specifications and test methods."
        ),
        key_factors=[
            "hydrogen partial pressure", "catalyst activity", "feed pretreatment", "diesel yield", "product quality"
        ],
        primary_authority=[
            "EN 590", "ASTM D975", "UOP Hydrocracking Guidelines"
        ],
        burden_holder="Process Engineering",
        adversary_position="Hydrocracking operation is not achieving target diesel yield or sulfur specification.",
        counter_arguments=[
            "Catalyst performance is within expected range.",
            "Feed contaminants are within design limits.",
            "Operating conditions are being optimized."
        ],
        resolution_strategy="Adjust severity and monitor catalyst performance to achieve targets.",
        entity_scope="Hydrocracking Unit",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EN 590 Diesel Standard"
    ),
    DoctrineBlock(
        topic="Kerosene",
        keywords=["kerosene", "jet fuel", "cut point", "hydrotreating", "smoke point"],
        conclusion_template="Kerosene cut point selection and hydrotreating are essential for meeting jet fuel specifications and maximizing product value.",
        reasoning_framework=(
            "Kerosene is a middle distillate fraction used as jet fuel and in domestic applications. "
            "Cut point selection in atmospheric distillation impacts both kerosene and diesel yields. "
            "Hydrotreating is required to reduce sulfur, aromatics, and improve smoke point. "
            "Jet fuel specifications (ASTM D1655) require strict control of freezing point, flash point, and aromatics content. "
            "Product blending is used to achieve final specifications. "
            "The burden of proof for kerosene quality lies with product quality assurance and operations. "
            "Disputes over cut point selection are resolved through simulation and laboratory analysis. "
            "Industry standards govern jet fuel quality and test methods."
        ),
        key_factors=[
            "cut point selection", "hydrotreating severity", "aromatics content", "smoke point", "freezing point"
        ],
        primary_authority=[
            "ASTM D1655", "DEF STAN 91-91", "API Data Book"
        ],
        burden_holder="Product Quality Assurance",
        adversary_position="Kerosene cut point is too wide, resulting in off-spec jet fuel.",
        counter_arguments=[
            "Laboratory analysis confirms compliance.",
            "Blending strategies mitigate off-spec risk.",
            "Simulation supports current cut point."
        ],
        resolution_strategy="Refine cut point and hydrotreating severity based on product assays.",
        entity_scope="Jet Fuel Production",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM D1655 Jet Fuel Standard"
    ),
    DoctrineBlock(
        topic="Jet Fuel",
        keywords=["jet fuel", "kerosene", "hydrotreating", "specification", "aromatics"],
        conclusion_template="Jet fuel production requires precise control of kerosene cut point, hydrotreating, and blending to meet international specifications.",
        reasoning_framework=(
            "Jet fuel (primarily Jet A-1) is produced from kerosene fractions that meet strict specifications for freezing point, flash point, aromatics, and sulfur. "
            "Hydrotreating is essential to reduce sulfur and aromatics, improving combustion and emissions. "
            "Product blending is used to adjust final properties. "
            "Quality assurance relies on laboratory testing (ASTM D1655, DEF STAN 91-91). "
            "The burden of proof for jet fuel compliance lies with the refinery's product quality team. "
            "Disputes over specification compliance are resolved through retesting and third-party certification. "
            "International standards govern jet fuel quality, transportation, and storage."
        ),
        key_factors=[
            "aromatics content", "sulfur", "smoke point", "freezing point", "flash point"
        ],
        primary_authority=[
            "ASTM D1655", "DEF STAN 91-91", "IATA Guidelines"
        ],
        burden_holder="Product Quality Team",
        adversary_position="Jet fuel does not meet international freezing point or aromatics specifications.",
        counter_arguments=[
            "Recent laboratory results confirm compliance.",
            "Blending pool is adjusted to meet specs.",
            "Third-party certification available."
        ],
        resolution_strategy="Retest and adjust blending as necessary to ensure compliance.",
        entity_scope="Jet Fuel Pool",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASTM D1655"
    ),
    DoctrineBlock(
        topic="Reforming Catalytic Naphtha",
        keywords=["reforming", "catalytic", "naphtha", "octane", "aromatics"],
        conclusion_template="Catalytic reforming upgrades naphtha to high-octane gasoline blendstock and aromatics feedstock through dehydrogenation and isomerization.",
        reasoning_framework=(
            "Catalytic reforming is a key process for increasing gasoline octane and producing aromatics (benzene, toluene, xylene). "
            "Naphtha feed is pretreated to remove sulfur and nitrogen, protecting platinum-based catalysts. "
            "Reforming reactions include dehydrogenation of naphthenes, isomerization of paraffins, and hydrocracking. "
            "Operating severity is balanced to maximize octane and aromatics yield while minimizing coke formation. "
            "Hydrogen is produced as a byproduct and used in other refinery units. "
            "Catalyst regeneration is required to restore activity. "
            "The burden of proof for reformer performance lies with process engineering and catalyst suppliers. "
            "Disputes over octane or aromatics yield are resolved through test runs and catalyst analysis. "
            "Industry standards specify product quality and test methods."
        ),
        key_factors=[
            "feed pretreatment", "catalyst activity", "operating severity", "octane number", "aromatics yield"
        ],
        primary_authority=[
            "ASTM D2699", "UOP Platforming Guidelines", "API Data Book"
        ],
        burden_holder="Process Engineering",
        adversary_position="Reformer operation is not achieving target octane or aromatics yield.",
        counter_arguments=[
            "Catalyst regeneration is scheduled.",
            "Feed quality is within design limits.",
            "Operating conditions are being optimized."
        ],
        resolution_strategy="Adjust severity and schedule catalyst regeneration as needed.",
        entity_scope="Catalytic Reforming Unit",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="UOP Platforming Best Practices"
    ),
    DoctrineBlock(
        topic="Octane",
        keywords=["octane", "RON", "MON", "gasoline", "blending"],
        conclusion_template="Octane number is a critical gasoline quality parameter, managed through blending, reforming, and FCC operation.",
        reasoning_framework=(
            "Octane number (RON and MON) measures gasoline's resistance to knocking in spark-ignition engines. "
            "High-octane components are produced via catalytic reforming, isomerization, and FCC. "
            "Blending strategies are used to meet pool specifications while optimizing margin. "
            "Octane boosters (e.g., ethers, aromatics) are added as needed. "
            "Product quality is monitored through laboratory testing (ASTM D2699, D2700). "
            "The burden of proof for octane compliance lies with blending and product quality teams. "
            "Disputes over octane shortfall are resolved through reblending and component allocation. "
            "Industry standards specify test methods and minimum octane requirements."
        ),
        key_factors=[
            "RON", "MON", "blending pool", "reformer output", "FCC gasoline"
        ],
        primary_authority=[
            "ASTM D2699", "ASTM D2700", "EN 228"
        ],
        burden_holder="Blending Team",
        adversary_position="Gasoline pool octane is below specification.",
        counter_arguments=[
            "Reblending with high-octane components is feasible.",
            "Octane boosters are available.",
            "Current test results confirm compliance."
        ],
        resolution_strategy="Adjust blending ratios and reallocate components as needed.",
        entity_scope="Gasoline Blending",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM D2699"
    ),
    DoctrineBlock(
        topic="Aromatics",
        keywords=["aromatics", "benzene", "toluene", "xylene", "reforming", "specification"],
        conclusion_template="Aromatics management balances gasoline octane, environmental compliance, and petrochemical feedstock requirements.",
        reasoning_framework=(
            "Aromatics (benzene, toluene, xylene) are produced in catalytic reforming and are key contributors to gasoline octane. "
            "However, environmental regulations limit total aromatics and benzene content in gasoline due to health concerns. "
            "Aromatics are also valuable as petrochemical feedstocks. "
            "Blending strategies are developed to meet both fuel and chemical market requirements. "
            "Product quality is monitored through laboratory analysis (ASTM D5580, D3606). "
            "The burden of proof for aromatics compliance lies with blending and product quality assurance. "
            "Disputes over allocation are resolved through economic modeling and regulatory review. "
            "Industry standards specify limits and test methods."
        ),
        key_factors=[
            "aromatics content", "benzene limit", "octane requirement", "petrochemical demand", "regulatory compliance"
        ],
        primary_authority=[
            "ASTM D5580", "EN 228", "EPA Regulations"
        ],
        burden_holder="Blending and Quality Assurance",
        adversary_position="Aromatics content exceeds regulatory limits in gasoline.",
        counter_arguments=[
            "Blending pool is adjusted to reduce aromatics.",
            "Petrochemical sales are prioritized.",
            "Current test data confirms compliance."
        ],
        resolution_strategy="Rebalance blending and allocate excess aromatics to petrochemical pool.",
        entity_scope="Gasoline and Petrochemical Blending",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EN 228 Gasoline Standard"
    ),
    DoctrineBlock(
        topic="Alkylation HF/H2SO4 Isobutane Olefin",
        keywords=["alkylation", "HF", "H2SO4", "isobutane", "olefin", "alkylate"],
        conclusion_template="Alkylation units use HF or H2SO4 catalysts to react isobutane with olefins, producing high-octane alkylate for gasoline blending.",
        reasoning_framework=(
            "Alkylation is a key process for producing high-octane, low-RVP gasoline blendstock. "
            "Isobutane reacts with light olefins (propylene, butylene) in the presence of either hydrofluoric acid (HF) or sulfuric acid (H2SO4) catalyst. "
            "Process safety is paramount due to the hazardous nature of acid catalysts. "
            "Product alkylate has high octane and low aromatics, making it valuable for clean fuels. "
            "Feedstock purity and acid strength are critical for unit performance. "
            "The burden of proof for alkylation performance and safety lies with unit operations and HSE teams. "
            "Disputes over catalyst selection or acid losses are resolved through process audits and vendor consultation. "
            "Industry standards govern product quality and acid handling."
        ),
        key_factors=[
            "acid strength", "feedstock purity", "isobutane/olefin ratio", "product octane", "process safety"
        ],
        primary_authority=[
            "API 940", "UOP Alkylation Guidelines", "OSHA PSM"
        ],
        burden_holder="Unit Operations and HSE",
        adversary_position="HF alkylation poses unacceptable safety risks compared to H2SO4.",
        counter_arguments=[
            "HF mitigation systems are installed.",
            "Process audits confirm compliance.",
            "Alternative catalyst evaluation is ongoing."
        ],
        resolution_strategy="Conduct risk assessment and evaluate alternative technologies.",
        entity_scope="Alkylation Unit",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 940 Alkylation Safety"
    ),
    DoctrineBlock(
        topic="Isomerization Light Naphtha RON Improvement",
        keywords=["isomerization", "light naphtha", "RON", "paraffins", "catalyst"],
        conclusion_template="Isomerization of light naphtha increases RON by converting normal paraffins to isoparaffins using platinum-based catalysts.",
        reasoning_framework=(
            "Isomerization is used to upgrade light naphtha (C5/C6) to high-RON gasoline blendstock. "
            "The process converts normal paraffins (n-pentane, n-hexane) to isoparaffins (isopentane, isohexane) over platinum-based catalysts. "
            "Feed must be free of sulfur, water, and oxygenates to prevent catalyst poisoning. "
            "Hydrogen is used to suppress coke formation and extend catalyst life. "
            "Product RON is monitored through laboratory testing. "
            "The burden of proof for isomerization performance lies with process engineering and catalyst suppliers. "
            "Disputes over RON improvement are resolved through test runs and catalyst analysis. "
            "Industry standards specify product quality and test methods."
        ),
        key_factors=[
            "feed purity", "catalyst activity", "hydrogen partial pressure", "product RON", "operating severity"
        ],
        primary_authority=[
            "ASTM D2699", "UOP Isomerization Guidelines", "API Data Book"
        ],
        burden_holder="Process Engineering",
        adversary_position="Isomerization unit is not achieving target RON uplift.",
        counter_arguments=[
            "Feed contaminants are within design limits.",
            "Catalyst regeneration is scheduled.",
            "Operating conditions are being optimized."
        ],
        resolution_strategy="Optimize feed pretreatment and catalyst operation.",
        entity_scope="Isomerization Unit",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="UOP Isomerization Best Practices"
    ),
    DoctrineBlock(
        topic="Coking Delayed, Fluid, Flexicoking",
        keywords=["coking", "delayed coking", "fluid coking", "flexicoking", "residuum"],
        conclusion_template="Coking technologies thermally convert residuum into lighter products and solid coke, with process selection based on refinery configuration and product slate.",
        reasoning_framework=(
            "Coking is a thermal cracking process used to convert heavy residuum into lighter products (naphtha, gasoil) and petroleum coke. "
            "Delayed coking is the most common technology, operating in batch mode with drum switching. "
            "Fluid and flexicoking offer continuous operation and gasification of coke for fuel gas production. "
            "Process selection depends on refinery configuration, product slate, and market demand for coke. "
            "Coke quality (sulfur, metals) determines its suitability for fuel or anode markets. "
            "The burden of proof for coking performance lies with unit operations and planning. "
            "Disputes over coke disposition or yield are resolved through market analysis and operational optimization. "
            "Industry standards govern coke quality and environmental compliance."
        ),
        key_factors=[
            "feed quality", "operating severity", "coke yield", "coke quality", "unit reliability"
        ],
        primary_authority=[
            "API 941", "ASTM D6376", "UOP Coking Guidelines"
        ],
        burden_holder="Unit Operations and Planning",
        adversary_position="Coking operation produces excessive coke or off-spec product.",
        counter_arguments=[
            "Feed quality is within design limits.",
            "Operating conditions are being optimized.",
            "Alternative coke markets are being pursued."
        ],
        resolution_strategy="Optimize operation and diversify coke sales.",
        entity_scope="Coking Units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 941 Coking Practices"
    ),
    DoctrineBlock(
        topic="Conradson",
        keywords=["Conradson carbon", "residuum", "coking", "feedstock", "carbon residue"],
        conclusion_template="Conradson carbon residue is a key indicator of feedstock tendency to form coke during thermal and catalytic processing.",
        reasoning_framework=(
            "Conradson carbon residue (CCR) measures the amount of carbonaceous material left after evaporation and pyrolysis of an oil sample. "
            "High CCR indicates a greater tendency for coke formation in units such as FCC, hydrocracking, and coking. "
            "Feedstocks with high CCR require careful management to avoid fouling and catalyst deactivation. "
            "CCR is determined by ASTM D189 or D4530. "
            "The burden of proof for CCR compliance lies with feedstock evaluation and laboratory teams. "
            "Disputes over CCR impact are resolved through pilot testing and process simulation. "
            "Industry standards specify test methods and CCR limits for various units."
        ),
        key_factors=[
            "CCR value", "feedstock type", "unit susceptibility", "coke formation", "operating severity"
        ],
        primary_authority=[
            "ASTM D189", "ASTM D4530", "API Data Book"
        ],
        burden_holder="Feedstock Evaluation Team",
        adversary_position="High CCR feedstock increases fouling and reduces unit reliability.",
        counter_arguments=[
            "Feed blending reduces overall CCR.",
            "Unit operation is adjusted for high CCR.",
            "Pilot tests confirm manageable coke formation."
        ],
        resolution_strategy="Blend feedstocks and adjust operation to mitigate CCR impact.",
        entity_scope="Feedstock Management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D189"
    ),
    DoctrineBlock(
        topic="Hydrotreating Desulfurization HDS HDN HDM",
        keywords=["hydrotreating", "desulfurization", "HDS", "HDN", "HDM", "catalyst"],
        conclusion_template="Hydrotreating removes sulfur, nitrogen, and metals from refinery streams to protect downstream catalysts and meet product specifications.",
        reasoning_framework=(
            "Hydrotreating is a catalytic process that uses hydrogen to remove sulfur (HDS), nitrogen (HDN), and metals (HDM) from petroleum fractions. "
            "The process operates at moderate temperature and pressure over CoMo or NiMo catalysts. "
            "Feed pretreatment is essential for protecting downstream units such as reformers and hydrocrackers. "
            "Product quality is monitored through laboratory analysis for sulfur, nitrogen, and metals. "
            "Catalyst life and activity are tracked through performance monitoring. "
            "The burden of proof for hydrotreating performance lies with process engineering and catalyst suppliers. "
            "Disputes over product quality are resolved through retesting and catalyst change-out. "
            "Industry standards specify test methods and product limits."
        ),
        key_factors=[
            "sulfur content", "nitrogen content", "metals", "catalyst activity", "hydrogen partial pressure"
        ],
        primary_authority=[
            "ASTM D5453", "UOP Hydrotreating Guidelines", "API Data Book"
        ],
        burden_holder="Process Engineering",
        adversary_position="Hydrotreating is not achieving target sulfur or nitrogen removal.",
        counter_arguments=[
            "Catalyst performance is within expected range.",
            "Operating conditions are being optimized.",
            "Feed contaminants are within design limits."
        ],
        resolution_strategy="Adjust severity and schedule catalyst change-out as needed.",
        entity_scope="Hydrotreating Units",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM D5453"
    ),
    DoctrineBlock(
        topic="Hydrogen Plant SMR PSA Steam Methane Reforming",
        keywords=["hydrogen plant", "SMR", "PSA", "steam methane reforming", "hydrogen purity"],
        conclusion_template="Hydrogen production via SMR and purification by PSA is essential for refinery hydrotreating and hydrocracking operations.",
        reasoning_framework=(
            "Steam methane reforming (SMR) is the primary technology for hydrogen production in refineries. "
            "Natural gas reacts with steam over a nickel catalyst to produce synthesis gas (H2, CO, CO2). "
            "Pressure swing adsorption (PSA) is used to purify hydrogen to >99.9% purity. "
            "Hydrogen is critical for hydrotreating, hydrocracking, and other units. "
            "SMR operation is optimized for feedstock efficiency, catalyst life, and emissions control. "
            "PSA performance is monitored for recovery and purity. "
            "The burden of proof for hydrogen supply reliability lies with utilities and process engineering. "
            "Disputes over hydrogen purity or supply are resolved through performance testing and maintenance. "
            "Industry standards govern hydrogen quality and safety."
        ),
        key_factors=[
            "SMR efficiency", "PSA recovery", "hydrogen purity", "feedstock quality", "catalyst life"
        ],
        primary_authority=[
            "API 941", "UOP SMR Guidelines", "ISO 14687"
        ],
        burden_holder="Utilities and Process Engineering",
        adversary_position="Hydrogen supply is insufficient or below purity specification.",
        counter_arguments=[
            "PSA performance is within design limits.",
            "Feedstock supply is stable.",
            "Maintenance schedule is current."
        ],
        resolution_strategy="Optimize SMR operation and PSA cycles; schedule maintenance as needed.",
        entity_scope="Hydrogen Production",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 14687 Hydrogen Quality"
    ),
    DoctrineBlock(
        topic="Sulfur Recovery Claus Process Tail Gas Treating",
        keywords=["sulfur recovery", "Claus process", "tail gas treating", "emissions", "H2S"],
        conclusion_template="Claus process and tail gas treating units are required to achieve high sulfur recovery efficiency and meet environmental emission limits.",
        reasoning_framework=(
            "The Claus process converts H2S from acid gas streams into elemental sulfur. "
            "Tail gas treating units (TGTU) further reduce sulfur emissions by converting residual sulfur compounds to H2S for recycling. "
            "Overall sulfur recovery efficiency must exceed 99.9% to comply with environmental regulations. "
            "Process performance is monitored through continuous emissions monitoring systems (CEMS). "
            "The burden of proof for compliance lies with environmental and process engineering teams. "
            "Disputes over emissions are resolved through retesting, process optimization, and regulatory reporting. "
            "Industry standards specify test methods and emission limits."
        ),
        key_factors=[
            "sulfur recovery efficiency", "emissions", "Claus unit operation", "TGTU performance", "regulatory compliance"
        ],
        primary_authority=[
            "EPA 40 CFR 60 Subpart J", "API 931", "ASTM D5504"
        ],
        burden_holder="Environmental and Process Engineering",
        adversary_position="Sulfur recovery is below regulatory requirements.",
        counter_arguments=[
            "CEMS data confirms compliance.",
            "Process optimization is ongoing.",
            "Maintenance is scheduled."
        ],
        resolution_strategy="Optimize operation and schedule maintenance to restore performance.",
        entity_scope="Sulfur Recovery Units",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR 60 Subpart J"
    ),
    DoctrineBlock(
        topic="Amine Treating MEA DEA MDEA Acid Gas",
        keywords=["amine treating", "MEA", "DEA", "MDEA", "acid gas", "H2S", "CO2"],
        conclusion_template="Amine treating units remove H2S and CO2 from refinery gas streams using MEA, DEA, or MDEA solvents, ensuring compliance with downstream and environmental requirements.",
        reasoning_framework=(
            "Amine treating is a chemical absorption process for removing acid gases (H2S, CO2) from refinery streams. "
            "Monoethanolamine (MEA), diethanolamine (DEA), and methyldiethanolamine (MDEA) are common solvents, each with specific advantages. "
            "Solvent selection depends on acid gas composition, required removal efficiency, and operational considerations. "
            "Rich amine is regenerated by steam stripping. "
            "Solvent degradation, foaming, and corrosion are key operational challenges. "
            "The burden of proof for amine unit performance lies with process engineering and operations. "
            "Disputes over solvent selection or performance are resolved through laboratory analysis and vendor consultation. "
            "Industry standards govern acid gas removal efficiency and solvent management."
        ),
        key_factors=[
            "solvent selection", "acid gas loading", "regeneration efficiency", "corrosion control", "emissions"
        ],
        primary_authority=[
            "API 942", "UOP Amine Treating Guidelines", "ASTM D6313"
        ],
        burden_holder="Process Engineering and Operations",
        adversary_position="Current amine solvent is not achieving target H2S or CO2 removal.",
        counter_arguments=[
            "Solvent analysis confirms adequate strength.",
            "Regeneration system is operating within design.",
            "Alternative solvents are under evaluation."
        ],
        resolution_strategy="Optimize operation and evaluate solvent alternatives.",
        entity_scope="Amine Treating Units",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 942 Amine Treating Practices"
    ),
    DoctrineBlock(
        topic="Merox Sweetening Mercaptan Oxidation",
        keywords=["Merox", "sweetening", "mercaptan", "oxidation", "LPG", "naphtha"],
        conclusion_template="Merox units oxidize mercaptans to disulfides, sweetening LPG and naphtha streams to meet product specifications.",
        reasoning_framework=(
            "Merox sweetening is a catalytic oxidation process that converts mercaptans in LPG, naphtha, and jet fuel to disulfides, reducing odor and corrosivity. "
            "The process uses an aqueous caustic solution and proprietary catalyst. "
            "Product quality is monitored through mercaptan sulfur analysis (ASTM D3227, D3228). "
            "The burden of proof for sweetening performance lies with process engineering and product quality teams. "
            "Disputes over off-spec product are resolved through retesting and process adjustment. "
            "Industry standards specify product sulfur limits and test methods."
        ),
        key_factors=[
            "mercaptan sulfur", "oxidation efficiency", "caustic strength", "catalyst activity", "product quality"
        ],
        primary_authority=[
            "ASTM D3227", "ASTM D3228", "UOP Merox Guidelines"
        ],
        burden_holder="Process Engineering and Quality",
        adversary_position="Merox unit is not achieving target mercaptan removal.",
        counter_arguments=[
            "Caustic and catalyst are within specification.",
            "Process adjustments are being implemented.",
            "Product retesting confirms compliance."
        ],
        resolution_strategy="Optimize operation and schedule catalyst replacement as needed.",
        entity_scope="Merox Units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D3227"
    ),
    DoctrineBlock(
        topic="Blending Gasoline, Diesel, Jet Fuel Specifications",
        keywords=["blending", "gasoline", "diesel", "jet fuel", "specifications", "product pool"],
        conclusion_template="Product blending strategies ensure compliance with gasoline, diesel, and jet fuel specifications while maximizing refinery margin.",
        reasoning_framework=(
            "Blending is the process of combining refinery streams to meet product specifications for gasoline, diesel, and jet fuel. "
            "Key properties include octane, cetane, sulfur, aromatics, and volatility. "
            "Blending models (linear programming) are used to optimize component allocation and maximize margin. "
            "Product quality is verified through laboratory testing. "
            "The burden of proof for specification compliance lies with blending and quality assurance teams. "
            "Disputes over off-spec product are resolved through reblending and retesting. "
            "Industry standards specify product limits and test methods."
        ),
        key_factors=[
            "component properties", "blending models", "product specifications", "market demand", "regulatory compliance"
        ],
        primary_authority=[
            "ASTM D4814", "EN 590", "ASTM D1655"
        ],
        burden_holder="Blending and Quality Assurance",
        adversary_position="Blending pool does not meet all product specifications.",
        counter_arguments=[
            "Reblending strategies are available.",
            "Component properties are verified.",
            "Current test results confirm compliance."
        ],
        resolution_strategy="Adjust blending ratios and retest products as needed.",
        entity_scope="Product Blending",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM D4814"
    ),
    DoctrineBlock(
        topic="Crude Scheduling Linear Programming Optimization",
        keywords=["crude scheduling", "linear programming", "LP", "optimization", "refinery margin"],
        conclusion_template="Crude scheduling and linear programming optimization maximize refinery margin by aligning feedstock selection with unit constraints and market demand.",
        reasoning_framework=(
            "Crude scheduling involves selecting and sequencing crude oil receipts to optimize refinery operations. "
            "Linear programming (LP) models are used to allocate feedstocks, optimize unit operation, and maximize margin. "
            "Key constraints include unit capacities, product specifications, and market demand. "
            "LP models are updated regularly with assay data, unit performance, and market prices. "
            "The burden of proof for optimization lies with planning and economics teams. "
            "Disputes over scheduling or model assumptions are resolved through scenario analysis and reconciliation. "
            "Industry best practices recommend regular model validation and stakeholder review."
        ),
        key_factors=[
            "crude assay data", "unit constraints", "market prices", "LP model accuracy", "product demand"
        ],
        primary_authority=[
            "API Technical Data Book", "UOP LP Guidelines", "Refinery Economics Texts"
        ],
        burden_holder="Planning and Economics Team",
        adversary_position="Current crude schedule does not maximize margin or meet operational constraints.",
        counter_arguments=[
            "LP model is regularly updated.",
            "Scenario analysis supports current schedule.",
            "Operational feedback is incorporated."
        ],
        resolution_strategy="Update LP model and conduct scenario analysis for improved scheduling.",
        entity_scope="Refinery Planning",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="UOP LP Best Practices"
    ),
    DoctrineBlock(
        topic="Refinery Margin Crack Spread 3-2-1",
        keywords=["refinery margin", "crack spread", "3-2-1", "product yield", "economics"],
        conclusion_template="Refinery margin is commonly measured by the crack spread (e.g., 3-2-1), reflecting the difference between crude cost and product value.",
        reasoning_framework=(
            "Crack spread is a simplified economic indicator representing the margin from converting crude oil into products. "
            "The 3-2-1 crack spread assumes 3 barrels of crude yield 2 barrels of gasoline and 1 barrel of diesel. "
            "Actual refinery margins depend on product slate, yield, and market prices. "
            "Margin analysis informs crude selection, unit operation, and product blending. "
            "The burden of proof for margin calculation lies with economics and planning teams. "
            "Disputes over margin reporting are resolved through reconciliation with actual yields and market data. "
            "Industry standards specify margin calculation methodologies."
        ),
        key_factors=[
            "crude cost", "product prices", "yield", "operating costs", "market demand"
        ],
        primary_authority=[
            "EIA Methodology", "API Economics Guidelines", "Refinery Financial Reports"
        ],
        burden_holder="Economics and Planning Team",
        adversary_position="Reported crack spread does not reflect actual refinery performance.",
        counter_arguments=[
            "Actual yields are reconciled with model assumptions.",
            "Market prices are updated daily.",
            "Operating costs are included in margin analysis."
        ],
        resolution_strategy="Reconcile reported margin with actual performance and update assumptions.",
        entity_scope="Refinery Economics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EIA Crack Spread Methodology"
    ),
    DoctrineBlock(
        topic="Energy Integration Pinch Analysis Heat Exchanger Network",
        keywords=["energy integration", "pinch analysis", "heat exchanger network", "HEN", "utility savings"],
        conclusion_template="Pinch analysis and heat exchanger network optimization reduce refinery energy consumption and utility costs.",
        reasoning_framework=(
            "Pinch analysis is a systematic method for optimizing heat recovery and minimizing utility consumption in process plants. "
            "Heat exchanger networks (HEN) are designed to recover heat from hot process streams and preheat cold streams. "
            "Pinch point identification guides placement of exchangers and utility integration. "
            "Energy savings are achieved by reducing steam and cooling water demand. "
            "The burden of proof for energy integration lies with process engineering and utilities teams. "
            "Disputes over HEN design or performance are resolved through simulation and energy audits. "
            "Industry standards recommend regular HEN review and optimization."
        ),
        key_factors=[
            "pinch point", "heat recovery", "utility consumption", "HEN design", "energy audit"
        ],
        primary_authority=[
            "Linnhoff Pinch Technology", "API 560", "Process Integration Texts"
        ],
        burden_holder="Process Engineering and Utilities",
        adversary_position="Current HEN design does not achieve targeted energy savings.",
        counter_arguments=[
            "Energy audit confirms savings.",
            "Simulation supports current design.",
            "Further optimization is under review."
        ],
        resolution_strategy="Conduct energy audit and update HEN design as needed.",
        entity_scope="Refinery Utilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Linnhoff Pinch Analysis"
    ),
    DoctrineBlock(
        topic="Environmental Compliance SOx NOx VOC Wastewater",
        keywords=["environmental compliance", "SOx", "NOx", "VOC", "wastewater", "emissions"],
        conclusion_template="Refinery operations must comply with environmental regulations for SOx, NOx, VOC, and wastewater emissions through monitoring and control technologies.",
        reasoning_framework=(
            "Environmental compliance requires continuous monitoring and control of SOx, NOx, VOC, and wastewater emissions. "
            "Control technologies include scrubbers, selective catalytic reduction (SCR), flare gas recovery, and wastewater treatment. "
            "Emissions are reported to regulatory agencies and subject to periodic audits. "
            "The burden of proof for compliance lies with environmental and operations teams. "
            "Disputes over emission levels are resolved through retesting, process optimization, and regulatory engagement. "
            "Industry standards specify emission limits and test methods."
        ),
        key_factors=[
            "emission limits", "control technologies", "monitoring systems", "regulatory reporting", "audit results"
        ],
        primary_authority=[
            "EPA 40 CFR Parts 60/63", "API Environmental Guidelines", "ISO 14001"
        ],
        burden_holder="Environmental and Operations Teams",
        adversary_position="Emissions exceed permitted levels for SOx, NOx, VOC, or wastewater.",
        counter_arguments=[
            "Monitoring data confirms compliance.",
            "Control systems are operational.",
            "Corrective actions are implemented as needed."
        ],
        resolution_strategy="Retest emissions and optimize control systems.",
        entity_scope="Refinery Environmental Compliance",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR Parts 60/63"
    ),
    DoctrineBlock(
        topic="Turnaround Planning Maintenance Scheduling Critical Path",
        keywords=["turnaround", "maintenance", "scheduling", "critical path", "shutdown"],
        conclusion_template="Turnaround planning and maintenance scheduling use critical path analysis to minimize downtime and ensure safe, reliable refinery operation.",
        reasoning_framework=(
            "Turnarounds are planned shutdowns for maintenance, inspection, and upgrades of refinery units. "
            "Critical path analysis identifies the sequence of activities that determine overall turnaround duration. "
            "Effective scheduling minimizes downtime, controls costs, and ensures safety. "
            "Scope definition, resource allocation, and contingency planning are essential. "
            "The burden of proof for turnaround execution lies with maintenance and project management teams. "
            "Disputes over schedule or scope are resolved through critical path review and stakeholder engagement. "
            "Industry standards recommend post-turnaround reviews and lessons learned."
        ),
        key_factors=[
            "critical path", "scope definition", "resource allocation", "safety compliance", "cost control"
        ],
        primary_authority=[
            "API 570", "API 653", "Project Management Institute (PMI)"
        ],
        burden_holder="Maintenance and Project Management",
        adversary_position="Turnaround schedule is unrealistic or omits critical activities.",
        counter_arguments=[
            "Critical path analysis supports schedule.",
            "Resource plan is validated.",
            "Contingency plans are in place."
        ],
        resolution_strategy="Review and update schedule with stakeholder input.",
        entity_scope="Refinery Turnarounds",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 570/653"
    ),
    # Additional doctrines for coverage and depth
    DoctrineBlock(
        topic="FCC Catalyst Management and Regeneration",
        keywords=["FCC", "catalyst management", "regeneration", "activity", "selectivity"],
        conclusion_template="Effective FCC catalyst management and regeneration maintain activity, selectivity, and minimize environmental impact.",
        reasoning_framework=(
            "FCC catalyst deactivates due to coke deposition and metal contamination. "
            "Continuous or semi-regenerative systems restore catalyst activity by burning off coke in the regenerator. "
            "Catalyst addition and withdrawal rates are optimized to maintain equilibrium properties. "
            "Metals (Ni, V, Fe) are monitored to prevent excessive hydrogen and coke yields. "
            "Spent catalyst disposal complies with environmental regulations. "
            "The burden of proof for catalyst management lies with FCC operations and technical support. "
            "Disputes over catalyst performance are resolved through laboratory analysis and vendor support. "
            "Industry standards specify catalyst handling and disposal practices."
        ),
        key_factors=[
            "catalyst activity", "regeneration efficiency", "metal contamination", "coke yield", "environmental compliance"
        ],
        primary_authority=[
            "API 560", "UOP FCC Catalyst Guidelines", "EPA RCRA"
        ],
        burden_holder="FCC Operations and Technical Support",
        adversary_position="Catalyst management is insufficient, leading to off-spec products or environmental violations.",
        counter_arguments=[
            "Catalyst addition rates are optimized.",
            "Regeneration is operating within design.",
            "Spent catalyst disposal is compliant."
        ],
        resolution_strategy="Review catalyst management plan and engage vendor support.",
        entity_scope="FCC Unit",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="UOP FCC Catalyst Management"
    ),
    DoctrineBlock(
        topic="Diesel Cetane Index and Additives",
        keywords=["diesel", "cetane index", "additives", "combustion quality", "specification"],
        conclusion_template="Diesel cetane index is managed through feed selection, hydroprocessing, and additive use to meet combustion quality specifications.",
        reasoning_framework=(
            "Cetane index measures diesel fuel's ignition quality and is influenced by feed composition and processing severity. "
            "Hydroprocessing increases cetane by saturating aromatics and removing impurities. "
            "Additives are used to boost cetane when natural index is insufficient. "
            "Product quality is monitored through laboratory testing (ASTM D976, D4737). "
            "The burden of proof for cetane compliance lies with blending and quality assurance teams. "
            "Disputes over cetane shortfall are resolved through additive dosing and reblending. "
            "Industry standards specify minimum cetane index for diesel fuels."
        ),
        key_factors=[
            "cetane index", "feed composition", "hydroprocessing severity", "additive dosage", "product testing"
        ],
        primary_authority=[
            "ASTM D976", "ASTM D4737", "EN 590"
        ],
        burden_holder="Blending and Quality Assurance",
        adversary_position="Diesel pool does not meet minimum cetane index.",
        counter_arguments=[
            "Additives are available for dosing.",
            "Hydroprocessing severity can be increased.",
            "Product testing confirms compliance."
        ],
        resolution_strategy="Dose cetane improver and adjust blending as needed.",
        entity_scope="Diesel Pool",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EN 590 Cetane Specification"
    ),
    DoctrineBlock(
        topic="FCC Gasoline Desulfurization",
        keywords=["FCC gasoline", "desulfurization", "hydrotreating", "sulfur specification", "product pool"],
        conclusion_template="FCC gasoline desulfurization is required to meet ultra-low sulfur gasoline specifications without excessive octane loss.",
        reasoning_framework=(
            "FCC gasoline contains significant sulfur, primarily in thiophenic compounds. "
            "Hydrotreating is used to reduce sulfur content to meet regulatory limits (<10 ppm). "
            "Process severity is balanced to minimize octane loss. "
            "Catalyst selection and reactor conditions are optimized for selectivity. "
            "The burden of proof for desulfurization performance lies with process engineering and operations. "
            "Disputes over product quality are resolved through retesting and process adjustment. "
            "Industry standards specify sulfur limits and test methods."
        ),
        key_factors=[
            "sulfur content", "octane retention", "catalyst selectivity", "hydrotreating severity", "product testing"
        ],
        primary_authority=[
            "ASTM D5453", "EN 228", "UOP Hydrotreating Guidelines"
        ],
        burden_holder="Process Engineering and Operations",
        adversary_position="FCC gasoline hydrotreating causes excessive octane loss.",
        counter_arguments=[
            "Catalyst is optimized for selectivity.",
            "Severity is minimized to retain octane.",
            "Product testing confirms compliance."
        ],
        resolution_strategy="Optimize catalyst and operating conditions.",
        entity_scope="FCC Gasoline Pool",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EN 228 Gasoline Specification"
    ),
    DoctrineBlock(
        topic="Hydrocracker Fractionation and Product Routing",
        keywords=["hydrocracker", "fractionation", "product routing", "diesel", "jet fuel"],
        conclusion_template="Hydrocracker fractionation is optimized to maximize diesel and jet fuel yields while meeting product specifications.",
        reasoning_framework=(
            "Hydrocracker effluent is separated in a fractionation section to recover naphtha, jet fuel, diesel, and unconverted oil. "
            "Cut points are selected based on product specifications and market demand. "
            "Product routing is managed to maximize margin and ensure compliance. "
            "Fractionation performance is monitored through laboratory testing and simulation. "
            "The burden of proof for optimal routing lies with process engineering and planning. "
            "Disputes over product allocation are resolved through economic analysis and simulation. "
            "Industry standards specify product limits and test methods."
        ),
        key_factors=[
            "cut point selection", "fractionation efficiency", "product specifications", "market demand", "simulation"
        ],
        primary_authority=[
            "API Data Book", "UOP Hydrocracking Guidelines", "ASTM D975"
        ],
        burden_holder="Process Engineering and Planning",
        adversary_position="Current fractionation does not maximize diesel or jet fuel yield.",
        counter_arguments=[
            "Simulation supports current cut points.",
            "Product testing confirms compliance.",
            "Market analysis supports allocation."
        ],
        resolution_strategy="Review fractionation and routing strategy based on updated data.",
        entity_scope="Hydrocracker Unit",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="UOP Hydrocracking Best Practices"
    ),
    DoctrineBlock(
        topic="Naphtha Splitting and Benzene Management",
        keywords=["naphtha splitting", "benzene", "aromatics", "reforming", "specification"],
        conclusion_template="Naphtha splitting and benzene management are critical for meeting gasoline benzene limits and maximizing reformer feed quality.",
        reasoning_framework=(
            "Naphtha is split into light and heavy fractions to optimize reformer feed and control benzene content in gasoline. "
            "Benzene is regulated due to health concerns, with limits typically <1% in gasoline. "
            "Splitting cut points are chosen to direct benzene-rich streams to reforming or petrochemical units. "
            "The burden of proof for benzene compliance lies with blending and quality assurance teams. "
            "Disputes over benzene allocation are resolved through simulation and laboratory analysis. "
            "Industry standards specify benzene limits and test methods."
        ),
        key_factors=[
            "cut point selection", "benzene content", "aromatics management", "simulation", "product testing"
        ],
        primary_authority=[
            "ASTM D3606", "EN 228", "API Data Book"
        ],
        burden_holder="Blending and Quality Assurance",
        adversary_position="Gasoline pool exceeds benzene specification.",
        counter_arguments=[
            "Naphtha splitting is optimized.",
            "Benzene-rich streams are diverted.",
            "Product testing confirms compliance."
        ],
        resolution_strategy="Adjust splitting and blending to control benzene content.",
        entity_scope="Naphtha Pool",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EN 228 Benzene Specification"
    ),
    DoctrineBlock(
        topic="FCC Light Ends Recovery and LPG Specification",
        keywords=["FCC", "light ends", "LPG", "recovery", "specification"],
        conclusion_template="FCC light ends recovery systems are optimized to maximize LPG yield and meet product specifications for propylene and butylene.",
        reasoning_framework=(
            "FCC main fractionator overhead is processed in gas concentration units to recover LPG components (C3, C4). "
            "Product specifications include olefin content, vapor pressure, and sulfur. "
            "Recovery efficiency is influenced by absorber and stripper operation. "
            "The burden of proof for LPG quality lies with process engineering and product quality teams. "
            "Disputes over yield or specification are resolved through process optimization and laboratory analysis. "
            "Industry standards specify LPG limits and test methods."
        ),
        key_factors=[
            "recovery efficiency", "olefin content", "vapor pressure", "sulfur", "absorber/stripper operation"
        ],
        primary_authority=[
            "ASTM D2163", "API Data Book", "UOP FCC Guidelines"
        ],
        burden_holder="Process Engineering and Quality",
        adversary_position="LPG product does not meet specification or yield targets.",
        counter_arguments=[
            "Absorber/stripper operation is optimized.",
            "Product testing confirms compliance.",
            "Process adjustments are ongoing."
        ],
        resolution_strategy="Optimize recovery system and retest products.",
        entity_scope="FCC Gas Concentration",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D2163"
    ),
    DoctrineBlock(
        topic="Sour Water Stripping and Ammonia Management",
        keywords=["sour water", "stripping", "ammonia", "H2S", "wastewater"],
        conclusion_template="Sour water stripping removes ammonia and H2S from refinery wastewater, ensuring compliance with discharge and reuse standards.",
        reasoning_framework=(
            "Sour water from distillation and conversion units contains ammonia and H2S. "
            "Stripping removes these contaminants using steam in a dedicated column. "
            "Effluent water is monitored for ammonia and H2S to meet discharge or reuse standards. "
            "The burden of proof for compliance lies with environmental and operations teams. "
            "Disputes over effluent quality are resolved through retesting and process adjustment. "
            "Industry standards specify discharge limits and test methods."
        ),
        key_factors=[
            "ammonia content", "H2S content", "stripping efficiency", "steam rate", "effluent quality"
        ],
        primary_authority=[
            "EPA 40 CFR 419", "API Environmental Guidelines", "ASTM D1426"
        ],
        burden_holder="Environmental and Operations Teams",
        adversary_position="Sour water effluent exceeds ammonia or H2S discharge limits.",
        counter_arguments=[
            "Stripping efficiency is monitored.",
            "Process adjustments are ongoing.",
            "Effluent testing confirms compliance."
        ],
        resolution_strategy="Optimize stripping operation and retest effluent.",
        entity_scope="Wastewater Treatment",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR 419"
    ),
    DoctrineBlock(
        topic="Refinery Off-Gas Recovery and Utilization",
        keywords=["off-gas", "recovery", "utilization", "fuel gas", "flare minimization"],
        conclusion_template="Refinery off-gas recovery systems maximize fuel gas utilization and minimize flaring to improve energy efficiency and reduce emissions.",
        reasoning_framework=(
            "Off-gas streams from various units are collected, treated, and used as refinery fuel gas. "
            "Recovery systems remove contaminants (H2S, ammonia) and compress gas for distribution. "
            "Flaring is minimized to reduce emissions and energy loss. "
            "The burden of proof for off-gas utilization lies with utilities and process engineering. "
            "Disputes over flaring or gas quality are resolved through process optimization and maintenance. "
            "Industry standards specify flare minimization and gas quality requirements."
        ),
        key_factors=[
            "off-gas composition", "recovery efficiency", "fuel gas quality", "flare minimization", "emissions"
        ],
        primary_authority=[
            "API 521", "EPA Flare Regulations", "UOP Off-Gas Guidelines"
        ],
        burden_holder="Utilities and Process Engineering",
        adversary_position="Excessive flaring or off-gas losses reduce refinery efficiency.",
        counter_arguments=[
            "Recovery system is optimized.",
            "Flaring is monitored and minimized.",
            "Gas quality is within specification."
        ],
        resolution_strategy="Optimize recovery and monitor flare system.",
        entity_scope="Refinery Fuel Gas System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 521"
    ),
    DoctrineBlock(
        topic="Slop Oil Management and Recovery",
        keywords=["slop oil", "management", "recovery", "tankage", "reprocessing"],
        conclusion_template="Effective slop oil management recovers valuable hydrocarbons and minimizes environmental impact through segregation, treatment, and reprocessing.",
        reasoning_framework=(
            "Slop oil consists of off-spec, interface, and oily water streams collected during normal and upset operations. "
            "Segregation and treatment recover hydrocarbons for reprocessing in crude or coker units. "
            "Water and solids are removed via settling, centrifugation, or chemical treatment. "
            "The burden of proof for slop oil management lies with operations and environmental teams. "
            "Disputes over recovery efficiency or environmental compliance are resolved through audits and process optimization. "
            "Industry standards specify slop oil handling and recovery practices."
        ),
        key_factors=[
            "slop oil composition", "recovery efficiency", "tank management", "reprocessing", "environmental compliance"
        ],
        primary_authority=[
            "API 653", "EPA Oil Pollution Regulations", "Refinery Operations Manuals"
        ],
        burden_holder="Operations and Environmental Teams",
        adversary_position="Slop oil recovery is insufficient, leading to losses or environmental violations.",
        counter_arguments=[
            "Segregation and treatment are optimized.",
            "Recovery rates are monitored.",
            "Environmental compliance is verified."
        ],
        resolution_strategy="Audit slop oil management and optimize recovery systems.",
        entity_scope="Refinery Slop Oil System",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API 653"
    ),
    DoctrineBlock(
        topic="Refinery Steam System Optimization",
        keywords=["steam system", "optimization", "boilers", "condensate", "energy integration"],
        conclusion_template="Steam system optimization improves energy efficiency and reliability through boiler management, condensate recovery, and system integration.",
        reasoning_framework=(
            "Refinery steam systems supply process and utility steam at various pressure levels. "
            "Boiler operation is optimized for fuel efficiency and emissions. "
            "Condensate recovery reduces water and energy consumption. "
            "System integration with heat exchanger networks maximizes energy recovery. "
            "The burden of proof for steam system performance lies with utilities and process engineering. "
            "Disputes over efficiency or reliability are resolved through energy audits and maintenance. "
            "Industry standards specify steam system design and operation."
        ),
        key_factors=[
            "boiler efficiency", "condensate recovery", "system integration", "energy audit", "reliability"
        ],
        primary_authority=[
            "API 560", "ASME Boiler Code", "Energy Management Standards"
        ],
        burden_holder="Utilities and Process Engineering",
        adversary_position="Steam system losses or inefficiencies increase operating costs.",
        counter_arguments=[
            "Boiler operation is optimized.",
            "Condensate recovery is maximized.",
            "Energy audit supports current performance."
        ],
        resolution_strategy="Conduct energy audit and optimize steam system operation.",
        entity_scope="Refinery Steam System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASME Boiler Code"
    ),
    DoctrineBlock(
        topic="Desalter Operation and Crude Pretreatment",
        keywords=["desalter", "crude pretreatment", "salt removal", "emulsification", "corrosion"],
        conclusion_template="Desalter operation removes salts and water from crude oil to prevent corrosion and fouling in downstream units.",
        reasoning_framework=(
            "Desalters use electrostatic coalescence to separate water and dissolved salts from crude oil. "
            "Effective operation prevents corrosion, fouling, and catalyst poisoning in downstream units. "
            "Key parameters include wash water rate, mixing, and emulsion stability. "
            "The burden of proof for desalter performance lies with operations and technical support. "
            "Disputes over salt removal or emulsion issues are resolved through laboratory testing and process adjustment. "
            "Industry standards specify desalter operation and crude pretreatment practices."
        ),
        key_factors=[
            "salt content", "water content", "emulsion stability", "wash water rate", "corrosion control"
        ],
        primary_authority=[
            "API 650", "ASTM D3230", "Refinery Operations Manuals"
        ],
        burden_holder="Operations and Technical Support",
        adversary_position="Desalter is not removing sufficient salt or water.",
        counter_arguments=[
            "Wash water rate is optimized.",
            "Emulsion breakers are used.",
            "Product testing confirms compliance."
        ],
        resolution_strategy="Optimize desalter operation and adjust chemical dosing.",
        entity_scope="Crude Pretreatment",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 650"
    ),
    DoctrineBlock(
        topic="Refinery Tank Farm Management",
        keywords=["tank farm", "management", "inventory", "vapor control", "safety"],
        conclusion_template="Tank farm management ensures safe storage, inventory control, and vapor emission compliance for refinery products and intermediates.",
        reasoning_framework=(
            "Tank farms store crude oil, intermediates, and finished products. "
            "Inventory management tracks receipts, transfers, and deliveries. "
            "Vapor control systems (floating roofs, vapor recovery) minimize emissions. "
            "Safety practices include overfill prevention, fire protection, and regular inspection. "
            "The burden of proof for tank farm management lies with operations and HSE teams. "
            "Disputes over inventory or emissions are resolved through audits and reconciliation. "
            "Industry standards specify tank design, operation, and inspection."
        ),
        key_factors=[
            "inventory accuracy", "vapor control", "safety systems", "inspection", "regulatory compliance"
        ],
        primary_authority=[
            "API 650", "API 653", "EPA Storage Tank Regulations"
        ],
        burden_holder="Operations and HSE Teams",
        adversary_position="Tank farm inventory or vapor emissions are not compliant.",
        counter_arguments=[
            "Inventory is reconciled regularly.",
            "Vapor control systems are operational.",
            "Inspections are up to date."
        ],
        resolution_strategy="Audit inventory and emissions; update management practices.",
        entity_scope="Tank Farm",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 650/653"
    ),
    DoctrineBlock(
        topic="Refinery Utilities Reliability and Redundancy",
        keywords=["utilities", "reliability", "redundancy", "power", "steam", "water"],
        conclusion_template="Utilities systems are designed for reliability and redundancy to ensure continuous operation of critical refinery units.",
        reasoning_framework=(
            "Refinery utilities include power, steam, water, air, and nitrogen systems. "
            "Reliability is achieved through redundancy, backup systems, and preventive maintenance. "
            "Critical units have prioritized supply and emergency protocols. "
            "The burden of proof for utilities reliability lies with utilities and maintenance teams. "
            "Disputes over reliability or supply interruptions are resolved through root cause analysis and system upgrades. "
            "Industry standards specify utilities design and operation."
        ),
        key_factors=[
            "system redundancy", "preventive maintenance", "emergency protocols", "critical unit supply", "root cause analysis"
        ],
        primary_authority=[
            "API 554", "NFPA 70", "Refinery Utilities Manuals"
        ],
        burden_holder="Utilities and Maintenance Teams",
        adversary_position="Utilities system failures disrupt refinery operation.",
        counter_arguments=[
            "Redundancy is built into system design.",
            "Preventive maintenance is scheduled.",
            "Emergency protocols are in place."
        ],
        resolution_strategy="Upgrade systems and review maintenance practices.",
        entity_scope="Refinery Utilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 554"
    ),
    DoctrineBlock(
        topic="Refinery Laboratory Quality Assurance",
        keywords=["laboratory", "quality assurance", "testing", "product certification", "compliance"],
        conclusion_template="Refinery laboratory quality assurance ensures product compliance through standardized testing, certification, and data integrity.",
        reasoning_framework=(
            "Laboratory quality assurance involves standardized testing, calibration, and data management. "
            "Certified methods (ASTM, ISO) are used for product and feedstock analysis. "
            "Data integrity and traceability are maintained through LIMS. "
            "The burden of proof for product certification lies with laboratory and quality teams. "
            "Disputes over test results are resolved through retesting and third-party analysis. "
            "Industry standards specify laboratory practices and certification."
        ),
        key_factors=[
            "standardized methods", "calibration", "data integrity", "LIMS", "third-party certification"
        ],
        primary_authority=[
            "ASTM Standards", "ISO 17025", "API Laboratory Guidelines"
        ],
        burden_holder="Laboratory and Quality Teams",
        adversary_position="Product certification is disputed due to inconsistent test results.",
        counter_arguments=[
            "Methods are standardized and calibrated.",
            "Retesting is available.",
            "Third-party certification can be obtained."
        ],
        resolution_strategy="Retest and seek third-party analysis as needed.",
        entity_scope="Refinery Laboratory",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 17025"
    ),
    DoctrineBlock(
        topic="Refinery Emergency Response and Incident Management",
        keywords=["emergency response", "incident management", "safety", "HSE", "contingency planning"],
        conclusion_template="Refinery emergency response and incident management protocols ensure safety, regulatory compliance, and rapid recovery from incidents.",
        reasoning_framework=(
            "Emergency response plans address fires, spills, releases, and other incidents. "
            "Incident management includes notification, containment, investigation, and corrective action. "
            "Regular drills and training ensure readiness. "
            "The burden of proof for emergency preparedness lies with HSE and operations teams. "
            "Disputes over response adequacy are resolved through post-incident review and regulatory engagement. "
            "Industry standards specify emergency planning and response requirements."
        ),
        key_factors=[
            "emergency plans", "incident investigation", "training", "regulatory compliance", "corrective action"
        ],
        primary_authority=[
            "OSHA PSM", "API 754", "NFPA 30"
        ],
        burden_holder="HSE and Operations Teams",
        adversary_position="Emergency response was inadequate or non-compliant.",
        counter_arguments=[
            "Plans are current and regularly drilled.",
            "Incident investigation is thorough.",
            "Corrective actions are implemented."
        ],
        resolution_strategy="Conduct post-incident review and update plans as needed.",
        entity_scope="Refinery Emergency Management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA PSM"
    ),
    DoctrineBlock(
        topic="Refinery Digitalization and Advanced Process Control",
        keywords=["digitalization", "advanced process control", "APC", "automation", "optimization"],
        conclusion_template="Digitalization and advanced process control improve refinery efficiency, safety, and margin