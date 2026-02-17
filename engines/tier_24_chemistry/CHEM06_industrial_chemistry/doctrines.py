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
        topic="Haber-Bosch Process - Ammonia Synthesis",
        keywords=["ammonia", "nitrogen fixation", "catalyst", "iron catalyst", "high pressure", "high temperature", "industrial chemistry", "fertilizer production"],
        conclusion_template="The Haber-Bosch process efficiently synthesizes ammonia by combining nitrogen and hydrogen gases under high pressure and temperature in the presence of an iron catalyst, enabling large-scale fertilizer production.",
        reasoning_framework=(
            "The Haber-Bosch process is grounded in the principles of chemical equilibrium and catalysis. "
            "Nitrogen (N2) and hydrogen (H2) gases are combined in a 1:3 molar ratio. The reaction is exothermic: "
            "N2 + 3H2 ⇌ 2NH3. According to Le Chatelier's principle, high pressure favors ammonia formation due to the reduction in gas moles. "
            "However, high temperature favors the reverse reaction due to the exothermic nature. Thus, an optimal balance is maintained at approximately 400-500°C and 150-300 atm. "
            "An iron catalyst with promoters such as potassium and aluminum oxides lowers the activation energy, increasing the reaction rate without affecting equilibrium. "
            "The process is cyclic, with unreacted gases recycled to maximize yield. Industrial implementation requires robust reactor design to withstand harsh conditions. "
            "Environmental and economic factors also influence operational parameters."
        ),
        key_factors=[
            "Reaction equilibrium constants",
            "Catalyst activity and lifetime",
            "Operating pressure and temperature",
            "Gas purity and feedstock ratio",
            "Recycling of unreacted gases",
            "Energy consumption and cost",
            "Environmental impact"
        ],
        primary_authority=[
            "Fritz Haber, Carl Bosch",
            "Industrial Chemistry Textbooks (e.g., 'Industrial Chemical Process Design' by Douglas)",
            "Journal of Catalysis",
            "Ullmann's Encyclopedia of Industrial Chemistry"
        ],
        burden_holder="Proponent of the process efficiency and scalability",
        adversary_position="Critics citing high energy consumption and environmental footprint",
        counter_arguments=[
            "Advances in catalyst design reduce energy requirements",
            "Integration with renewable hydrogen sources mitigates carbon footprint",
            "Process optimization improves yield and reduces waste"
        ],
        resolution_strategy="Continuous research and development focusing on catalyst improvements and process integration with sustainable energy sources",
        entity_scope="Global industrial ammonia production facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Haber, F. (1909). Ammonia Synthesis Patent; Bosch, C. (1910). Industrial Implementation"
    ),
    DoctrineBlock(
        topic="Contact Process - Sulfuric Acid Production",
        keywords=["sulfuric acid", "contact process", "vanadium pentoxide catalyst", "sulfur dioxide oxidation", "industrial chemistry", "acid production", "catalysis"],
        conclusion_template="The Contact Process efficiently produces sulfuric acid by catalytic oxidation of sulfur dioxide to sulfur trioxide using vanadium pentoxide, followed by absorption in water.",
        reasoning_framework=(
            "The Contact Process involves three main steps: combustion of sulfur or sulfide ores to produce sulfur dioxide (SO2), catalytic oxidation of SO2 to sulfur trioxide (SO3), and absorption of SO3 in water to form sulfuric acid (H2SO4). "
            "The oxidation step is catalyzed by vanadium pentoxide (V2O5) on a silica support at 400-600°C. "
            "The reaction SO2 + 1/2 O2 ⇌ SO3 is exothermic and equilibrium-limited. High temperature reduces SO3 yield, so a compromise temperature is chosen to balance rate and conversion. "
            "High pressure is not economically justified as it does not significantly increase yield. "
            "The produced SO3 is absorbed into concentrated sulfuric acid to form oleum, which is then diluted to desired concentration. "
            "Process control involves temperature regulation, catalyst maintenance, and gas purification to remove impurities like dust and arsenic compounds that poison the catalyst."
        ),
        key_factors=[
            "Catalyst activity and poisoning",
            "Temperature control",
            "Gas purity",
            "Absorption efficiency",
            "Feedstock sulfur quality",
            "Environmental emission controls"
        ],
        primary_authority=[
            "Industrial Chemistry Texts (e.g., 'Chemical Engineering' by Perry and Green)",
            "Ullmann's Encyclopedia of Industrial Chemistry",
            "Environmental Protection Agency (EPA) guidelines on sulfur emissions"
        ],
        burden_holder="Operator ensuring catalyst integrity and process efficiency",
        adversary_position="Environmental concerns regarding SO2 emissions and acid mist",
        counter_arguments=[
            "Modern scrubbers and gas cleaning reduce emissions",
            "Catalyst regeneration techniques extend lifespan",
            "Process optimization minimizes waste and emissions"
        ],
        resolution_strategy="Implementation of best available technologies (BAT) and strict environmental regulations",
        entity_scope="Sulfuric acid plants worldwide",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Contact Process patents and industrial standards established in early 20th century"
    ),
    DoctrineBlock(
        topic="Chloralkali Process - Membrane Cell Technology",
        keywords=["chloralkali", "membrane cell", "electrolysis", "chlorine production", "caustic soda", "industrial electrochemistry", "membrane technology"],
        conclusion_template="Membrane cell technology in the chloralkali process enables efficient and environmentally friendly electrolysis of brine to produce chlorine and caustic soda with minimal mercury and asbestos usage.",
        reasoning_framework=(
            "The chloralkali process electrolyzes aqueous sodium chloride (brine) to produce chlorine gas, hydrogen gas, and sodium hydroxide (caustic soda). "
            "Membrane cell technology uses a selective ion-exchange membrane that allows sodium ions to pass from the anode to the cathode compartment while preventing hydroxide and chloride ions from mixing. "
            "This separation prevents the formation of unwanted byproducts and allows for higher purity products. "
            "Compared to mercury and diaphragm cells, membrane cells consume less energy and avoid toxic mercury emissions and asbestos use. "
            "The process operates at moderate temperatures (~70°C) and current densities optimized to balance production rate and membrane lifespan. "
            "Brine purification is critical to prevent membrane fouling and extend operational life. "
            "Environmental regulations drive adoption of membrane technology globally."
        ),
        key_factors=[
            "Membrane selectivity and durability",
            "Brine purity",
            "Operating current density and temperature",
            "Energy consumption",
            "Product purity",
            "Environmental compliance"
        ],
        primary_authority=[
            "Electrochemical Society publications",
            "Ullmann's Encyclopedia of Industrial Chemistry",
            "International Chlorine Council guidelines"
        ],
        burden_holder="Plant operator ensuring membrane integrity and process control",
        adversary_position="Concerns about membrane lifespan and replacement costs",
        counter_arguments=[
            "Advances in membrane materials improve durability",
            "Lower environmental and health risks justify investment",
            "Energy savings offset membrane replacement costs"
        ],
        resolution_strategy="Ongoing R&D in membrane materials and process optimization",
        entity_scope="Global chloralkali production facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Development and commercialization of Nafion and other ion-exchange membranes since 1960s"
    ),
    DoctrineBlock(
        topic="Catalytic Cracking in Petroleum Refining",
        keywords=["catalytic cracking", "petroleum refining", "zeolite catalyst", "hydrocarbon cracking", "fuel production", "industrial catalysis"],
        conclusion_template="Catalytic cracking uses zeolite catalysts to break down heavy hydrocarbons into lighter fractions, enhancing gasoline yield and quality in petroleum refining.",
        reasoning_framework=(
            "Catalytic cracking is a key step in petroleum refining that converts heavy hydrocarbon fractions into lighter, more valuable products such as gasoline and olefins. "
            "The process operates at 450-550°C and moderate pressure in the presence of solid acid catalysts, predominantly zeolites like faujasite. "
            "Zeolite catalysts provide high surface area and strong acid sites that facilitate carbocation intermediates, enabling carbon-carbon bond cleavage. "
            "The reaction mechanism involves protonation of hydrocarbons, β-scission, hydride transfer, and isomerization. "
            "Catalyst deactivation occurs due to coke deposition, necessitating periodic regeneration by burning off coke in air. "
            "Process parameters such as temperature, catalyst-to-oil ratio, and residence time are optimized to maximize desired product yields while minimizing coke and gas formation."
        ),
        key_factors=[
            "Catalyst acidity and pore structure",
            "Operating temperature and pressure",
            "Feedstock composition",
            "Catalyst regeneration cycles",
            "Product distribution control",
            "Energy efficiency"
        ],
        primary_authority=[
            "Petroleum refining handbooks",
            "Catalysis journals",
            "UOP LLC technical literature"
        ],
        burden_holder="Refinery process engineers",
        adversary_position="Concerns about catalyst deactivation and environmental emissions",
        counter_arguments=[
            "Advanced catalyst formulations reduce coke formation",
            "Emission controls mitigate environmental impact",
            "Process optimization improves catalyst life and efficiency"
        ],
        resolution_strategy="Continuous catalyst development and emission control technology integration",
        entity_scope="Petroleum refineries worldwide",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Zeolite catalyst development by Mobil Oil in 1960s"
    ),
    DoctrineBlock(
        topic="Steam Reforming of Methane for Hydrogen Production",
        keywords=["steam reforming", "methane", "hydrogen production", "nickel catalyst", "industrial chemistry", "syngas", "energy efficiency"],
        conclusion_template="Steam reforming of methane over nickel catalysts produces hydrogen and carbon monoxide efficiently, forming syngas for ammonia synthesis and other applications.",
        reasoning_framework=(
            "Steam reforming involves the reaction of methane (CH4) with steam (H2O) at 700-900°C over a nickel-based catalyst to produce hydrogen (H2) and carbon monoxide (CO). "
            "The primary reaction is CH4 + H2O ⇌ CO + 3H2, which is endothermic and requires high temperature and heat input. "
            "Subsequent water-gas shift reaction converts CO and steam to CO2 and additional hydrogen: CO + H2O ⇌ CO2 + H2. "
            "Catalyst activity depends on surface area, nickel dispersion, and resistance to coking. "
            "Feedstock purity and steam-to-carbon ratio are critical to prevent catalyst deactivation and carbon deposition. "
            "Process integration includes heat recovery and CO2 removal for efficient hydrogen production."
        ),
        key_factors=[
            "Catalyst composition and stability",
            "Operating temperature and pressure",
            "Steam-to-carbon ratio",
            "Feedstock purity",
            "Heat integration",
            "Carbon deposition control"
        ],
        primary_authority=[
            "Industrial Gas Technology publications",
            "Hydrogen production handbooks",
            "Ullmann's Encyclopedia of Industrial Chemistry"
        ],
        burden_holder="Process engineers optimizing catalyst and operating conditions",
        adversary_position="Concerns about CO2 emissions and catalyst deactivation",
        counter_arguments=[
            "Carbon capture technologies mitigate emissions",
            "Catalyst regeneration and improved formulations reduce downtime",
            "Process optimization enhances efficiency"
        ],
        resolution_strategy="Integration of carbon capture and catalyst R&D",
        entity_scope="Hydrogen production plants globally",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Steam reforming technology patents and industrial scale implementations since 1920s"
    ),
    DoctrineBlock(
        topic="Fischer-Tropsch Synthesis for Synthetic Fuels",
        keywords=["Fischer-Tropsch", "synthetic fuels", "cobalt catalyst", "iron catalyst", "gas-to-liquids", "industrial catalysis", "syngas conversion"],
        conclusion_template="Fischer-Tropsch synthesis converts syngas into liquid hydrocarbons using cobalt or iron catalysts, enabling production of synthetic fuels from coal, natural gas, or biomass.",
        reasoning_framework=(
            "Fischer-Tropsch (FT) synthesis converts carbon monoxide (CO) and hydrogen (H2) mixtures (syngas) into hydrocarbons via catalytic polymerization. "
            "The reaction occurs over cobalt or iron catalysts at 200-350°C and 20-40 atm. "
            "Cobalt catalysts favor long-chain paraffins and have higher activity but are sensitive to sulfur. Iron catalysts tolerate sulfur and promote water-gas shift reactions. "
            "The mechanism involves CO adsorption, dissociation, hydrogenation, and chain growth via surface carbene intermediates. "
            "Product distribution follows the Anderson-Schulz-Flory model, influenced by catalyst type and operating conditions. "
            "FT synthesis enables conversion of coal, natural gas, or biomass-derived syngas into diesel, kerosene, and waxes. "
            "Process economics depend on feedstock cost, catalyst life, and product upgrading."
        ),
        key_factors=[
            "Catalyst type and preparation",
            "Operating temperature and pressure",
            "Syngas composition and purity",
            "Product distribution control",
            "Catalyst deactivation mechanisms",
            "Process integration and upgrading"
        ],
        primary_authority=[
            "Fischer and Tropsch original publications",
            "Industrial catalysis textbooks",
            "Sasol and Shell FT technology documentation"
        ],
        burden_holder="Process developers and catalyst manufacturers",
        adversary_position="High capital costs and catalyst sensitivity",
        counter_arguments=[
            "Advances in catalyst design improve stability and selectivity",
            "Integration with renewable feedstocks reduces carbon footprint",
            "Scale-up and modular designs reduce capital expenditure"
        ],
        resolution_strategy="Continued catalyst R&D and process integration with sustainable feedstocks",
        entity_scope="Gas-to-liquids and coal-to-liquids plants worldwide",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Fischer-Tropsch patents and commercial plants since 1920s"
    ),
    DoctrineBlock(
        topic="Solvay Process for Sodium Carbonate Production",
        keywords=["Solvay process", "sodium carbonate", "ammonia recycling", "industrial chemistry", "carbonate production", "lime kiln"],
        conclusion_template="The Solvay process produces sodium carbonate by reacting sodium chloride, ammonia, and carbon dioxide, with ammonia recycled to minimize losses.",
        reasoning_framework=(
            "The Solvay process synthesizes sodium carbonate (Na2CO3) from brine (NaCl) and limestone (CaCO3) via ammonia recycling. "
            "Key steps include ammonia absorption into brine, carbon dioxide bubbling to precipitate sodium bicarbonate (NaHCO3), and calcination to sodium carbonate. "
            "Ammonia is recovered by treating calcium chloride byproduct with lime (CaO) to regenerate ammonia and precipitate calcium carbonate. "
            "The process is cyclic and designed to minimize ammonia loss, which is critical due to cost and environmental concerns. "
            "Control of temperature, concentration, and pH is essential to optimize yield and purity. "
            "Waste management involves handling calcium chloride effluent and lime kiln emissions."
        ),
        key_factors=[
            "Ammonia recovery efficiency",
            "Carbon dioxide purity and flow rate",
            "Temperature and pH control",
            "Feedstock quality",
            "Waste effluent management",
            "Energy consumption"
        ],
        primary_authority=[
            "Industrial chemistry references",
            "Ullmann's Encyclopedia of Industrial Chemistry",
            "Historical patents by Ernest Solvay"
        ],
        burden_holder="Plant operators managing process parameters and emissions",
        adversary_position="Environmental concerns over calcium chloride disposal",
        counter_arguments=[
            "Calcium chloride can be repurposed for de-icing and dust control",
            "Process optimization reduces waste generation",
            "Modern effluent treatment technologies mitigate impact"
        ],
        resolution_strategy="Sustainable waste management and process optimization",
        entity_scope="Sodium carbonate production plants globally",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Solvay process patents and industrial implementations since 1860s"
    ),
    DoctrineBlock(
        topic="Ziegler-Natta Catalysis for Polyolefin Production",
        keywords=["Ziegler-Natta", "polyolefins", "polymerization", "catalyst", "ethylene polymerization", "industrial catalysis"],
        conclusion_template="Ziegler-Natta catalysts enable stereospecific polymerization of olefins, producing high-density polyethylene and polypropylene with controlled properties.",
        reasoning_framework=(
            "Ziegler-Natta catalysts are transition metal complexes (typically titanium chlorides with organoaluminum co-catalysts) that facilitate coordination polymerization of alpha-olefins. "
            "The catalysts enable control over polymer stereochemistry, molecular weight, and branching, producing materials with tailored mechanical and thermal properties. "
            "Polymerization occurs via insertion of monomers into metal-carbon bonds on the catalyst surface. "
            "Process parameters such as temperature, pressure, and monomer concentration influence polymer properties. "
            "Catalyst design has evolved to support different polymer architectures, including isotactic, syndiotactic, and atactic polymers. "
            "Industrial implementation requires control of catalyst activity, selectivity, and deactivation mechanisms."
        ),
        key_factors=[
            "Catalyst composition and support",
            "Monomer purity and concentration",
            "Operating temperature and pressure",
            "Polymer molecular weight distribution",
            "Catalyst lifetime and deactivation",
            "Process scale-up"
        ],
        primary_authority=[
            "Ziegler and Natta Nobel lectures",
            "Polymer chemistry textbooks",
            "Industrial polymerization process literature"
        ],
        burden_holder="Catalyst manufacturers and polymer producers",
        adversary_position="Concerns about catalyst toxicity and polymer recyclability",
        counter_arguments=[
            "Catalyst residues are minimized in final products",
            "Research into biodegradable polymers complements polyolefin use",
            "Recycling technologies are advancing"
        ],
        resolution_strategy="Sustainable catalyst design and polymer lifecycle management",
        entity_scope="Global polyolefin production industry",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Ziegler-Natta catalyst patents and industrial adoption since 1950s"
    ),
    DoctrineBlock(
        topic="Electrochemical Reduction of CO2 to Fuels",
        keywords=["electrochemical reduction", "carbon dioxide", "CO2 conversion", "renewable energy", "catalysis", "fuel synthesis"],
        conclusion_template="Electrochemical reduction of CO2 converts carbon dioxide into value-added fuels and chemicals using renewable electricity and specialized catalysts.",
        reasoning_framework=(
            "Electrochemical CO2 reduction involves the conversion of CO2 to hydrocarbons, alcohols, or other chemicals at the cathode of an electrochemical cell. "
            "Catalysts such as copper, silver, or molecular complexes facilitate multi-electron transfer reactions with varying selectivity. "
            "The process is influenced by electrode material, electrolyte composition, applied potential, and cell design. "
            "Challenges include competing hydrogen evolution reaction, low current densities, and catalyst stability. "
            "Integration with renewable electricity sources enables carbon-neutral fuel production. "
            "Research focuses on improving catalyst efficiency, selectivity, and scalability."
        ),
        key_factors=[
            "Catalyst selectivity and stability",
            "Electrolyte composition",
            "Applied potential and current density",
            "Cell design and mass transport",
            "Renewable energy integration",
            "Product separation and purification"
        ],
        primary_authority=[
            "Journal of the American Chemical Society",
            "Energy & Environmental Science",
            "National Renewable Energy Laboratory (NREL) reports"
        ],
        burden_holder="Researchers and developers of CO2 electrolysis technology",
        adversary_position="Low efficiency and high cost compared to fossil fuels",
        counter_arguments=[
            "Ongoing catalyst and cell design improvements increase efficiency",
            "Carbon pricing and renewable mandates improve economics",
            "Scalability demonstrated in pilot projects"
        ],
        resolution_strategy="Continued R&D and policy support for renewable fuels",
        entity_scope="Emerging renewable fuel production sector",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="Recent advances in CO2 electrolysis catalysts and pilot demonstrations"
    ),
    DoctrineBlock(
        topic="Polymerase Chain Reaction (PCR) in Industrial Biotechnology",
        keywords=["PCR", "polymerase chain reaction", "biotechnology", "enzyme amplification", "industrial applications", "genetic engineering"],
        conclusion_template="PCR enables exponential amplification of DNA sequences, facilitating genetic engineering and industrial biotechnology applications.",
        reasoning_framework=(
            "PCR is a molecular biology technique that amplifies specific DNA sequences using thermostable DNA polymerase, primers, nucleotides, and thermal cycling. "
            "The process involves denaturation, annealing, and extension steps repeated cyclically to exponentially increase target DNA quantity. "
            "Industrial applications include strain development, genetic modification, diagnostics, and quality control. "
            "Optimization of reaction conditions such as primer design, annealing temperature, and cycle number is critical for specificity and yield. "
            "Automation and scaling of PCR enable high-throughput screening in industrial settings."
        ),
        key_factors=[
            "Primer specificity and design",
            "Polymerase fidelity and activity",
            "Thermal cycling parameters",
            "Template quality",
            "Contamination control",
            "Automation and throughput"
        ],
        primary_authority=[
            "Mullis and Faloona original publications",
            "Biotechnology protocols",
            "Industrial microbiology literature"
        ],
        burden_holder="Biotech process developers and quality control teams",
        adversary_position="Potential for contamination and amplification errors",
        counter_arguments=[
            "Strict laboratory protocols minimize contamination",
            "High-fidelity polymerases reduce errors",
            "Controls and validation ensure reliability"
        ],
        resolution_strategy="Standardization and automation of PCR workflows",
        entity_scope="Industrial biotechnology and molecular diagnostics",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="PCR invention and widespread adoption since 1980s"
    ),
    DoctrineBlock(
        topic="Electroplating Process Control and Optimization",
        keywords=["electroplating", "surface coating", "metal deposition", "current density", "bath chemistry", "industrial electrochemistry"],
        conclusion_template="Electroplating deposits metal coatings onto substrates by controlled electrochemical reduction, optimizing bath chemistry and current density for quality and efficiency.",
        reasoning_framework=(
            "Electroplating involves the deposition of metal ions from an electrolyte solution onto a conductive substrate by applying an electric current. "
            "Key parameters include current density, bath composition, temperature, agitation, and pH. "
            "Uniform deposition requires control of mass transport and avoidance of defects such as pitting or roughness. "
            "Additives in the plating bath influence grain size, brightness, and adhesion. "
            "Process monitoring includes measuring voltage, current efficiency, and bath composition. "
            "Environmental regulations govern waste treatment and heavy metal discharge."
        ),
        key_factors=[
            "Current density and distribution",
            "Bath chemistry and additives",
            "Temperature and agitation",
            "Substrate preparation",
            "Process monitoring and control",
            "Waste management"
        ],
        primary_authority=[
            "Electrochemical Society publications",
            "Industrial plating handbooks",
            "Environmental Protection Agency guidelines"
        ],
        burden_holder="Process engineers and quality control",
        adversary_position="Environmental concerns over heavy metal waste",
        counter_arguments=[
            "Closed-loop waste treatment reduces discharge",
            "Use of less toxic metals and additives",
            "Process optimization minimizes waste"
        ],
        resolution_strategy="Implementation of best environmental practices and continuous process improvement",
        entity_scope="Electroplating facilities worldwide",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Industrial electroplating standards and environmental regulations"
    ),
    DoctrineBlock(
        topic="Catalytic Hydrogenation in Fine Chemical Synthesis",
        keywords=["catalytic hydrogenation", "fine chemicals", "heterogeneous catalysis", "selectivity", "industrial chemistry"],
        conclusion_template="Catalytic hydrogenation selectively reduces unsaturated bonds in fine chemical synthesis using heterogeneous catalysts under controlled conditions.",
        reasoning_framework=(
            "Catalytic hydrogenation involves the addition of hydrogen to unsaturated organic compounds using metal catalysts such as palladium, platinum, or nickel. "
            "Selectivity is controlled by catalyst choice, temperature, pressure, solvent, and substrate structure. "
            "Heterogeneous catalysts provide ease of separation and reuse. "
            "Reaction mechanisms involve adsorption of substrate and hydrogen on catalyst surface, followed by stepwise hydrogen addition. "
            "Process optimization balances conversion, selectivity, and catalyst lifetime. "
            "Industrial applications include pharmaceuticals, agrochemicals, and fragrances."
        ),
        key_factors=[
            "Catalyst type and preparation",
            "Operating temperature and pressure",
            "Substrate and solvent effects",
            "Reaction time and mixing",
            "Catalyst deactivation and regeneration",
            "Product purification"
        ],
        primary_authority=[
            "Organic synthesis textbooks",
            "Catalysis journals",
            "Industrial fine chemical process literature"
        ],
        burden_holder="Process chemists and engineers",
        adversary_position="Concerns about catalyst cost and metal contamination",
        counter_arguments=[
            "Catalyst recycling and recovery minimize costs",
            "Metal contamination controlled by purification steps",
            "Alternative catalysts under development"
        ],
        resolution_strategy="Catalyst development and process optimization for sustainability",
        entity_scope="Fine chemical manufacturing plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Industrial hydrogenation patents and processes since early 20th century"
    ),
    DoctrineBlock(
        topic="Bayer Process for Alumina Production",
        keywords=["Bayer process", "alumina", "bauxite refining", "industrial chemistry", "aluminum production"],
        conclusion_template="The Bayer process refines bauxite ore to produce alumina (Al2O3) by digestion in sodium hydroxide, precipitation, and calcination.",
        reasoning_framework=(
            "The Bayer process involves digesting crushed bauxite ore in concentrated sodium hydroxide at high temperature and pressure to dissolve aluminum-containing minerals. "
            "Impurities such as iron oxides remain insoluble and are removed as red mud. "
            "The sodium aluminate solution is cooled and seeded to precipitate aluminum hydroxide crystals. "
            "These are filtered, washed, and calcined to produce alumina. "
            "Process control includes temperature, pressure, caustic concentration, and seed crystal quality. "
            "Waste management of red mud is a significant environmental challenge."
        ),
        key_factors=[
            "Bauxite ore quality",
            "Digestion conditions",
            "Seed crystal control",
            "Red mud handling",
            "Energy consumption",
            "Environmental compliance"
        ],
        primary_authority=[
            "Aluminum industry technical literature",
            "Ullmann's Encyclopedia of Industrial Chemistry",
            "Environmental regulations on mining waste"
        ],
        burden_holder="Refinery operators and environmental managers",
        adversary_position="Environmental impact of red mud disposal",
        counter_arguments=[
            "Research into red mud reuse and stabilization",
            "Improved process efficiency reduces waste",
            "Regulatory compliance and monitoring"
        ],
        resolution_strategy="Sustainable waste management and process optimization",
        entity_scope="Alumina refineries worldwide",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bayer patents and industrial implementations since late 19th century"
    ),
    DoctrineBlock(
        topic="Solvent Extraction in Hydrometallurgy",
        keywords=["solvent extraction", "hydrometallurgy", "metal recovery", "liquid-liquid extraction", "industrial chemistry"],
        conclusion_template="Solvent extraction selectively separates and recovers metals from aqueous solutions using organic solvents and complexing agents.",
        reasoning_framework=(
            "Solvent extraction in hydrometallurgy involves contacting an aqueous metal-containing solution with an immiscible organic solvent containing extractants that form complexes with target metals. "
            "The metal complexes transfer into the organic phase, separating them from impurities. "
            "Subsequent stripping recovers metals into a purified aqueous phase. "
            "Process parameters such as pH, temperature, phase ratio, and extractant concentration influence selectivity and efficiency. "
            "Applications include copper, uranium, nickel, and rare earth element recovery. "
            "Environmental considerations include solvent losses and organic waste management."
        ),
        key_factors=[
            "Extractant type and concentration",
            "Phase contact efficiency",
            "pH and temperature control",
            "Metal complex stability",
            "Solvent recovery and recycling",
            "Waste treatment"
        ],
        primary_authority=[
            "Hydrometallurgy textbooks",
            "Industrial mineral processing literature",
            "Environmental guidelines for solvent use"
        ],
        burden_holder="Process engineers and environmental compliance teams",
        adversary_position="Concerns over solvent toxicity and losses",
        counter_arguments=[
            "Use of less toxic, biodegradable solvents",
            "Closed-loop solvent recovery systems",
            "Process optimization to minimize solvent use"
        ],
        resolution_strategy="Sustainable solvent management and process control",
        entity_scope="Metal extraction and refining plants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Industrial solvent extraction patents and applications since mid-20th century"
    ),
    DoctrineBlock(
        topic="Steam Cracking for Olefin Production",
        keywords=["steam cracking", "olefins", "ethylene", "propylene", "industrial chemistry", "hydrocarbon cracking"],
        conclusion_template="Steam cracking thermally decomposes hydrocarbons at high temperature to produce olefins such as ethylene and propylene for petrochemical feedstocks.",
        reasoning_framework=(
            "Steam cracking involves heating hydrocarbon feedstocks (ethane, naphtha, gas oil) to 750-900°C in the presence of steam to prevent coke formation. "
            "The process produces a mixture of olefins, paraffins, and aromatics via free radical chain reactions. "
            "Residence time is short (milliseconds) to maximize olefin yield and minimize secondary reactions. "
            "Quenching rapidly cools the cracked gases to stop reactions. "
            "Feedstock composition, temperature, and steam-to-hydrocarbon ratio influence product distribution. "
            "Energy integration and furnace design are critical for process efficiency."
        ),
        key_factors=[
            "Feedstock type and quality",
            "Furnace temperature and design",
            "Steam dilution ratio",
            "Residence time control",
            "Quench system efficiency",
            "Energy recovery"
        ],
        primary_authority=[
            "Petrochemical industry handbooks",
            "Chemical engineering literature",
            "Ullmann's Encyclopedia of Industrial Chemistry"
        ],
        burden_holder="Process engineers optimizing yield and energy use",
        adversary_position="High energy consumption and CO2 emissions",
        counter_arguments=[
            "Energy integration reduces net consumption",
            "Use of renewable feedstocks under investigation",
            "Emission controls mitigate environmental impact"
        ],
        resolution_strategy="Process optimization and integration with sustainable technologies",
        entity_scope="Olefin production plants worldwide",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Steam cracking technology development since 1950s"
    ),
    DoctrineBlock(
        topic="Electrodialysis for Water Desalination",
        keywords=["electrodialysis", "water desalination", "ion exchange membranes", "industrial water treatment", "electrochemical separation"],
        conclusion_template="Electrodialysis uses ion-exchange membranes and electric potential to separate salts from water, enabling efficient desalination and water purification.",
        reasoning_framework=(
            "Electrodialysis employs alternating cation and anion exchange membranes between electrodes. "
            "When an electric potential is applied, ions migrate through selective membranes, concentrating salts in concentrate streams and producing desalinated water. "
            "Process efficiency depends on membrane selectivity, electrical current, flow rates, and feedwater composition. "
            "Electrodialysis is effective for brackish water and selective ion removal. "
            "Membrane fouling and scaling are challenges requiring pretreatment and cleaning protocols. "
            "Energy consumption is generally lower than thermal desalination methods."
        ),
        key_factors=[
            "Membrane selectivity and durability",
            "Feedwater quality",
            "Operating current and voltage",
            "Flow rate and hydrodynamics",
            "Fouling control and cleaning",
            "Energy efficiency"
        ],
        primary_authority=[
            "Water treatment engineering texts",
            "Journal of Membrane Science",
            "Environmental Protection Agency reports"
        ],
        burden_holder="Water treatment plant operators",
        adversary_position="Membrane fouling and replacement costs",
        counter_arguments=[
            "Advanced pretreatment reduces fouling",
            "Improved membrane materials extend lifespan",
            "Energy savings justify operational costs"
        ],
        resolution_strategy="Membrane R&D and process optimization",
        entity_scope="Industrial and municipal water treatment facilities",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Electrodialysis technology patents and commercial use since 1950s"
    ),
    DoctrineBlock(
        topic="Fluid Catalytic Cracking (FCC) in Refining",
        keywords=["fluid catalytic cracking", "FCC", "petroleum refining", "catalyst circulation", "gasoline production", "industrial catalysis"],
        conclusion_template="FCC converts heavy petroleum fractions into lighter hydrocarbons using a circulating catalyst system, enhancing gasoline and olefin production.",
        reasoning_framework=(
            "FCC employs a fluidized bed of fine catalyst particles circulated between a reactor and regenerator. "
            "Heavy hydrocarbons are vaporized and cracked over the catalyst at 500°C and low pressure. "
            "Catalyst deactivation by coke is reversed in the regenerator by burning coke deposits. "
            "The process produces gasoline, light olefins, and LPG. "
            "Catalyst composition, reactor temperature, and catalyst-to-oil ratio control product distribution. "
            "FCC units require complex heat and material balances and emission controls."
        ),
        key_factors=[
            "Catalyst activity and circulation rate",
            "Operating temperature and pressure",
            "Feedstock quality",
            "Regenerator efficiency",
            "Product separation and upgrading",
            "Emission controls"
        ],
        primary_authority=[
            "Refinery process engineering texts",
            "Catalysis journals",
            "Industrial FCC technology providers"
        ],
        burden_holder="Refinery process engineers",
        adversary_position="Emissions and catalyst attrition concerns",
        counter_arguments=[
            "Emission control technologies reduce pollutants",
            "Improved catalyst formulations increase lifespan",
            "Process optimization minimizes catalyst loss"
        ],
        resolution_strategy="Integrated process and environmental management",
        entity_scope="Petroleum refineries globally",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FCC technology development since 1940s"
    ),
    DoctrineBlock(
        topic="Ammonium Nitrate Production via Neutralization",
        keywords=["ammonium nitrate", "neutralization", "fertilizer production", "industrial chemistry", "acid-base reaction"],
        conclusion_template="Ammonium nitrate is produced by neutralizing nitric acid with ammonia, yielding a high-nitrogen fertilizer with controlled crystallization.",
        reasoning_framework=(
            "The production involves reacting gaseous ammonia with nitric acid in a neutralizer, forming ammonium nitrate solution. "
            "The exothermic reaction requires temperature control to prevent decomposition. "
            "The solution is concentrated and crystallized to produce prilled or granulated ammonium nitrate. "
            "Process parameters such as acid and ammonia purity, temperature, and concentration influence product quality. "
            "Safety considerations include handling of reactive materials and prevention of runaway reactions."
        ),
        key_factors=[
            "Purity of reactants",
            "Temperature and concentration control",
            "Crystallization parameters",
            "Safety protocols",
            "Product storage and handling",
            "Environmental regulations"
        ],
        primary_authority=[
            "Fertilizer industry handbooks",
            "Chemical safety guidelines",
            "Ullmann's Encyclopedia of Industrial Chemistry"
        ],
        burden_holder="Plant operators and safety managers",
        adversary_position="Risks of explosion and environmental impact",
        counter_arguments=[
            "Strict safety standards and monitoring",
            "Process automation reduces human error",
            "Environmental controls minimize emissions"
        ],
        resolution_strategy="Comprehensive safety management and process control",
        entity_scope="Fertilizer manufacturing plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Industrial ammonium nitrate production standards"
    ),
    DoctrineBlock(
        topic="Hydroformylation (Oxo Process) in Chemical Industry",
        keywords=["hydroformylation", "oxo process", "aldehyde synthesis", "catalysis", "industrial chemistry"],
        conclusion_template="Hydroformylation converts alkenes into aldehydes using syngas and transition metal catalysts, facilitating production of alcohols and plasticizers.",
        reasoning_framework=(
            "Hydroformylation involves the addition of a formyl group and hydrogen to an alkene in the presence of cobalt or rhodium catalysts under pressure and moderate temperature. "
            "The reaction produces linear and branched aldehydes, which can be further processed into alcohols or acids. "
            "Catalyst ligands influence regioselectivity and activity. "
            "Process parameters such as pressure, temperature, and syngas ratio affect conversion and selectivity. "
            "Industrial applications include plasticizer and detergent intermediate production."
        ),
        key_factors=[
            "Catalyst type and ligand design",
            "Operating pressure and temperature",
            "Syngas composition",
            "Alkene feedstock purity",
            "Product separation",
            "Catalyst recovery"
        ],
        primary_authority=[
            "Industrial catalysis literature",
            "Chemical engineering process texts",
            "Patent literature on hydroformylation"
        ],
        burden_holder="Process chemists and engineers",
        adversary_position="Catalyst cost and selectivity challenges",
        counter_arguments=[
            "Ligand design improves selectivity and turnover",
            "Catalyst recycling reduces cost",
            "Process optimization enhances yields"
        ],
        resolution_strategy="Catalyst development and process integration",
        entity_scope="Chemical manufacturing plants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Hydroformylation patents and industrial applications since 1930s"
    ),
    DoctrineBlock(
        topic="Methanol Synthesis from Syngas",
        keywords=["methanol synthesis", "syngas", "catalysis", "industrial chemistry", "hydrogenation"],
        conclusion_template="Methanol is synthesized from syngas over copper-based catalysts under high pressure and moderate temperature, serving as a chemical feedstock and fuel.",
        reasoning_framework=(
            "Methanol synthesis involves catalytic hydrogenation of carbon monoxide and carbon dioxide mixtures at 50-100 atm and 200-300°C. "
            "Copper-zinc oxide catalysts supported on alumina facilitate the reaction CO + 2H2 → CH3OH and CO2 + 3H2 → CH3OH + H2O. "
            "Catalyst activity and selectivity depend on preparation, surface area, and promoter presence. "
            "Process control includes feed gas composition, temperature, pressure, and removal of byproducts. "
            "Methanol serves as a feedstock for formaldehyde, acetic acid, and fuels."
        ),
        key_factors=[
            "Catalyst composition and preparation",
            "Operating pressure and temperature",
            "Feed gas purity and ratio",
            "Reaction kinetics",
            "Product separation",
            "Catalyst deactivation"
        ],
        primary_authority=[
            "Industrial catalysis texts",
            "Methanol Institute publications",
            "Ullmann's Encyclopedia of Industrial Chemistry"
        ],
        burden_holder="Plant operators and catalyst manufacturers",
        adversary_position="Catalyst sensitivity to poisons and process complexity",
        counter_arguments=[
            "Feed purification reduces catalyst poisoning",
            "Catalyst regeneration extends life",
            "Process optimization improves robustness"
        ],
        resolution_strategy="Integrated catalyst and process development",
        entity_scope="Methanol production facilities worldwide",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Methanol synthesis patents and industrial scale plants since 1920s"
    ),
    DoctrineBlock(
        topic="Biodiesel Production via Transesterification",
        keywords=["biodiesel", "transesterification", "vegetable oil", "catalysis", "renewable fuels"],
        conclusion_template="Biodiesel is produced by transesterification of vegetable oils or animal fats with methanol using alkaline or enzymatic catalysts.",
        reasoning_framework=(
            "Transesterification converts triglycerides in oils or fats into methyl esters (biodiesel) and glycerol by reaction with methanol. "
            "Alkaline catalysts such as sodium hydroxide or potassium hydroxide are commonly used for high reaction rates. "
            "Enzymatic catalysts offer milder conditions and higher specificity but at higher cost. "
            "Process parameters include molar ratio of methanol to oil, temperature, catalyst concentration, and reaction time. "
            "Purification steps remove glycerol, catalyst residues, and unreacted methanol. "
            "Feedstock quality affects yield and product properties."
        ),
        key_factors=[
            "Catalyst type and concentration",
            "Methanol to oil ratio",
            "Reaction temperature and time",
            "Feedstock free fatty acid content",
            "Purification and separation",
            "Environmental impact"
        ],
        primary_authority=[
            "Renewable energy journals",
            "Industrial biodiesel production manuals",
            "Environmental Protection Agency reports"
        ],
        burden_holder="Biodiesel producers and quality control",
        adversary_position="Feedstock variability and process waste",
        counter_arguments=[
            "Feedstock pretreatment improves consistency",
            "Glycerol valorization reduces waste",
            "Process optimization enhances efficiency"
        ],
        resolution_strategy="Sustainable feedstock sourcing and process integration",
        entity_scope="Biodiesel production industry",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Industrial biodiesel production methods since early 2000s"
    ),
    DoctrineBlock(
        topic="Catalytic Reforming in Refinery Operations",
        keywords=["catalytic reforming", "naphtha upgrading", "platinum catalyst", "aromatics production", "industrial chemistry"],
        conclusion_template="Catalytic reforming converts low-octane naphtha into high-octane gasoline components and aromatics using platinum-based catalysts.",
        reasoning_framework=(
            "Catalytic reforming involves dehydrogenation, isomerization, and cyclization reactions over platinum or platinum-rhenium catalysts at 450-520°C and moderate pressure. "
            "The process increases octane number by producing branched and aromatic hydrocarbons. "
            "Catalyst deactivation by coke formation requires periodic regeneration. "
            "Operating parameters such as temperature, pressure, and hydrogen partial pressure influence product yield and catalyst life. "
            "Hydrogen produced is recycled to suppress coke formation and used in other refinery processes."
        ),
        key_factors=[
            "Catalyst composition and regeneration",
            "Operating temperature and pressure",
            "Hydrogen partial pressure",
            "Feedstock composition",
            "Product quality control",
            "Energy consumption"
        ],
        primary_authority=[
            "Petroleum refining textbooks",
            "Industrial catalysis literature",
            "Refinery process standards"
        ],
        burden_holder="Refinery process engineers",
        adversary_position="Catalyst cost and deactivation issues",
        counter_arguments=[
            "Catalyst improvements extend life",
            "Process optimization reduces coke formation",
            "Hydrogen recycling enhances efficiency"
        ],
        resolution_strategy="Catalyst R&D and process control",
        entity_scope="Petroleum refineries worldwide",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Catalytic reforming patents and industrial use since 1940s"
    ),
    DoctrineBlock(
        topic="Electrochemical Synthesis of Ammonia",
        keywords=["electrochemical ammonia synthesis", "nitrogen reduction", "green ammonia", "catalysis", "renewable energy"],
        conclusion_template="Electrochemical nitrogen reduction offers a sustainable alternative to Haber-Bosch by producing ammonia at ambient conditions using renewable electricity.",
        reasoning_framework=(
            "Electrochemical ammonia synthesis reduces nitrogen to ammonia at the cathode of an electrochemical cell under ambient temperature and pressure. "
            "Catalysts such as transition metal nitrides or single-atom catalysts facilitate nitrogen adsorption and activation. "
            "Challenges include competing hydrogen evolution reaction, low current density, and catalyst stability. "
            "Integration with renewable energy sources enables carbon-neutral ammonia production. "
            "Research focuses on catalyst development, cell design, and process scalability."
        ),
        key_factors=[
            "Catalyst activity and selectivity",
            "Electrolyte composition",
            "Applied potential and current density",
            "Cell design and mass transport",
            "Renewable energy integration",
            "Product separation"
        ],
        primary_authority=[
            "Journal of Catalysis",
            "Energy & Environmental Science",
            "National Renewable Energy Laboratory reports"
        ],
        burden_holder="Researchers and developers",
        adversary_position="Low efficiency and scalability challenges",
        counter_arguments=[
            "Ongoing catalyst improvements increase efficiency",
            "Pilot projects demonstrate feasibility",
            "Policy support for green ammonia"
        ],
        resolution_strategy="Continued R&D and commercialization efforts",
        entity_scope="Emerging green ammonia production sector",
        confidence=0.70,
        confidence_zone="Medium",
        controlling_precedent="Recent advances in electrochemical nitrogen reduction"
    ),
    DoctrineBlock(
        topic="Catalytic Dehydrogenation of Alkanes",
        keywords=["catalytic dehydrogenation", "alkanes", "olefins", "industrial catalysis", "hydrocarbon processing"],
        conclusion_template="Catalytic dehydrogenation converts alkanes to olefins using metal catalysts under high temperature, providing key petrochemical feedstocks.",
        reasoning_framework=(
            "Catalytic dehydrogenation removes hydrogen from alkanes to form olefins, essential intermediates in petrochemical industry. "
            "Common catalysts include platinum or chromium oxides supported on alumina. "
            "The endothermic reaction requires temperatures of 500-700°C and low pressure to favor olefin formation. "
            "Side reactions include cracking and coke formation, which deactivate catalysts. "
            "Process design includes catalyst regeneration and heat integration. "
            "Feedstock purity and operating conditions influence selectivity and yield."
        ),
        key_factors=[
            "Catalyst composition and stability",
            "Operating temperature and pressure",
            "Feedstock quality",
            "Coke formation and catalyst regeneration",
            "Heat management",
            "Product separation"
        ],
        primary_authority=[
            "Industrial catalysis literature",
            "Petrochemical process textbooks",
            "Patent literature"
        ],
        burden_holder="Process engineers and catalyst suppliers",
        adversary_position="Catalyst deactivation and energy intensity",
        counter_arguments=[
            "Advanced catalysts reduce coke formation",
            "Heat integration improves energy efficiency",
            "Catalyst regeneration extends life"
        ],
        resolution_strategy="Catalyst development and process optimization",
        entity_scope="Petrochemical plants",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Industrial catalytic dehydrogenation patents and processes"
    ),
    DoctrineBlock(
        topic="Hydrodesulfurization in Petroleum Refining",
        keywords=["hydrodesulfurization", "HDS", "catalysis", "sulfur removal", "industrial chemistry"],
        conclusion_template="Hydrodesulfurization removes sulfur compounds from petroleum fractions using cobalt-molybdenum catalysts under hydrogen pressure, reducing emissions.",
        reasoning_framework=(
            "HDS involves catalytic hydrogenation of sulfur-containing compounds to hydrogen sulfide and hydrocarbons over Co-Mo or Ni-Mo catalysts supported on alumina. "
            "Operating conditions are typically 300-400°C and 30-130 atm hydrogen pressure. "
            "The process reduces sulfur content to meet environmental regulations and prevent catalyst poisoning in downstream units. "
            "Catalyst activity depends on metal dispersion and support properties. "
            "Feedstock pretreatment and process control optimize sulfur removal and minimize hydrocarbon saturation."
        ),
        key_factors=[
            "Catalyst composition and preparation",
            "Operating temperature and pressure",
            "Hydrogen availability",
            "Feedstock sulfur content",
            "Catalyst deactivation",
            "Environmental compliance"
        ],
        primary_authority=[
            "Petroleum refining literature",
            "Catalysis journals",
            "Environmental regulations"
        ],
        burden_holder="Refinery operators and environmental managers",
        adversary_position="Catalyst cost and process complexity",
        counter_arguments=[
            "Catalyst improvements increase activity and lifespan",
            "Process optimization reduces operational costs",
            "Compliance with regulations is mandatory"
        ],
        resolution_strategy="Catalyst R&D and process control",
        entity_scope="Petroleum refineries worldwide",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="HDS technology patents and industrial use since 1950s"
    ),
    DoctrineBlock(
        topic="Ammonia Oxidation in Nitric Acid Production",
        keywords=["ammonia oxidation", "nitric acid", "platinum catalyst", "industrial chemistry", "catalysis"],
        conclusion_template="Ammonia oxidation over platinum-rhodium catalysts produces nitric oxide, a key intermediate in nitric acid manufacturing.",
        reasoning_framework=(
            "Ammonia oxidation is the first step in the Ostwald process for nitric acid production. "
            "Ammonia is oxidized to nitric oxide (NO) over platinum-rhodium gauze catalysts at 900-950°C. "
            "The reaction is highly exothermic and requires precise temperature control to prevent catalyst damage and side reactions. "
            "NO is subsequently converted to nitrogen dioxide and absorbed in water to form nitric acid. "
            "Catalyst durability and selectivity are critical for process efficiency and longevity."
        ),
        key_factors=[
            "Catalyst composition and structure",
            "Operating temperature and flow rate",
            "Ammonia purity",
            "Catalyst deactivation",
            "Heat management",
            "Product downstream processing"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Catalysis journals",
            "Nitric acid production standards"
        ],
        burden_holder="Process engineers and catalyst manufacturers",
        adversary_position="Catalyst degradation and process hazards",
        counter_arguments=[
            "Advanced catalyst materials improve durability",
            "Process control systems enhance safety",
            "Regular maintenance extends catalyst life"
        ],
        resolution_strategy="Catalyst innovation and rigorous process control",
        entity_scope="Nitric acid plants globally",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Ostwald process patents and industrial applications"
    ),
    DoctrineBlock(
        topic="Phenol Production via Cumene Process",
        keywords=["phenol", "cumene process", "industrial chemistry", "catalysis", "acetone production"],
        conclusion_template="The cumene process produces phenol and acetone by oxidation of cumene and acid-catalyzed cleavage of cumene hydroperoxide.",
        reasoning_framework=(
            "Cumene (isopropylbenzene) is oxidized with air to cumene hydroperoxide, which is then cleaved by acid catalysts to yield phenol and acetone. "
            "The process involves careful control of oxidation conditions to maximize hydroperoxide formation and minimize byproducts. "
            "Acid catalysis requires precise temperature and pH control to optimize cleavage and product yield. "
            "Phenol and acetone are separated by distillation. "
            "Process safety is critical due to the reactive and potentially explosive nature of hydroperoxides."
        ),
        key_factors=[
            "Oxidation reaction conditions",
            "Catalyst type and concentration",
            "Temperature and pH control",
            "Product separation efficiency",
            "Safety protocols",
            "Byproduct management"
        ],
        primary_authority=[
            "Industrial chemistry literature",
            "Chemical engineering process texts",
            "Safety standards for peroxide handling"
        ],
        burden_holder="Plant operators and safety managers",
        adversary_position="Safety risks and process complexity",
        counter_arguments=[
            "Strict safety management and monitoring",
            "Process automation reduces risks",
            "Continuous process improvements enhance safety"
        ],
        resolution_strategy="Comprehensive safety and process control",
        entity_scope="Phenol production plants worldwide",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Cumene process patents and industrial use since 1940s"
    ),
    DoctrineBlock(
        topic="Hydrogen Peroxide Production via Anthraquinone Process",
        keywords=["hydrogen peroxide", "anthraquinone process", "industrial chemistry", "catalysis", "oxidation-reduction"],
        conclusion_template="Hydrogen peroxide is produced by cyclic hydrogenation and oxidation of anthraquinone derivatives, enabling large-scale industrial synthesis.",
        reasoning_framework=(
            "The anthraquinone process involves hydrogenating an anthraquinone derivative to anthrahydroquinone, which is then oxidized by air to regenerate the quinone and produce hydrogen peroxide. "
            "The process is cyclic and uses organic solvents and catalysts to facilitate reactions. "
            "Hydrogen peroxide is extracted from the organic phase by water washing and purified. "
            "Process control includes temperature, pressure, and catalyst activity. "
            "Environmental considerations involve solvent recovery and waste management."
        ),
        key_factors=[
            "Catalyst activity and selectivity",
            "Operating temperature and pressure",
            "Solvent system",
            "Extraction efficiency",
            "Solvent recovery",
            "Environmental compliance"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Chemical engineering literature",
            "Environmental regulations"
        ],
        burden_holder="Process engineers and environmental managers",
        adversary_position="Solvent losses and environmental impact",
        counter_arguments=[
            "Closed-loop solvent recovery minimizes losses",
            "Process optimization reduces waste",
            "Compliance with environmental standards"
        ],
        resolution_strategy="Sustainable process design and control",
        entity_scope="Hydrogen peroxide production facilities",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Anthraquinone process patents and industrial use since 1930s"
    ),
    DoctrineBlock(
        topic="Catalytic Isomerization of Hydrocarbons",
        keywords=["catalytic isomerization", "hydrocarbons", "refining", "platinum catalyst", "industrial chemistry"],
        conclusion_template="Catalytic isomerization rearranges hydrocarbon molecules to improve octane rating of gasoline using platinum catalysts under controlled conditions.",
        reasoning_framework=(
            "Isomerization converts straight-chain hydrocarbons into branched isomers with higher octane numbers. "
            "Platinum or chlorided alumina catalysts are used at 100-200°C and moderate pressure with hydrogen to prevent coke formation. "
            "Process parameters control conversion, selectivity, and catalyst life. "
            "Feedstock purity and hydrogen partial pressure are critical. "
            "Isomerate is blended into gasoline to improve performance."
        ),
        key_factors=[
            "Catalyst composition and activity",
            "Operating temperature and pressure",
            "Hydrogen partial pressure",
            "Feedstock quality",
            "Catalyst regeneration",
            "Product quality control"
        ],
        primary_authority=[
            "Petroleum refining literature",
            "Catalysis journals",
            "Industrial process standards"
        ],
        burden_holder="Refinery process engineers",
        adversary_position="Catalyst cost and deactivation",
        counter_arguments=[
            "Catalyst improvements extend life",
            "Process optimization reduces costs",
            "Hydrogen management improves efficiency"
        ],
        resolution_strategy="Catalyst development and process control",
        entity_scope="Petroleum refineries",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Isomerization technology patents and industrial use"
    ),
    DoctrineBlock(
        topic="Ethylene Oxide Production via Direct Oxidation",
        keywords=["ethylene oxide", "direct oxidation", "silver catalyst", "industrial chemistry", "ethylene oxidation"],
        conclusion_template="Ethylene oxide is produced by direct oxidation of ethylene over silver catalysts, serving as a precursor for ethylene glycol and other chemicals.",
        reasoning_framework=(
            "Ethylene is oxidized to ethylene oxide using oxygen over porous silver catalysts at 200-300°C and moderate pressure. "
            "The reaction is highly exothermic and requires precise temperature control to avoid combustion. "
            "Selectivity towards ethylene oxide is influenced by catalyst morphology, promoters, and operating conditions. "
            "Ethylene oxide is hydrolyzed to ethylene glycol or used in other chemical syntheses. "
            "Process safety and catalyst management are critical due to reaction exothermicity and toxicity."
        ),
        key_factors=[
            "Catalyst composition and structure",
            "Operating temperature and pressure",
            "Feedstock purity",
            "Reaction selectivity",
            "Heat management",
            "Safety protocols"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Catalysis journals",
            "Safety standards"
        ],
        burden_holder="Process engineers and safety managers",
        adversary_position="Safety risks and catalyst deactivation",
        counter_arguments=[
            "Advanced catalyst formulations improve selectivity",
            "Process automation enhances safety",
            "Regular catalyst regeneration"
        ],
        resolution_strategy="Comprehensive process control and safety management",
        entity_scope="Ethylene oxide production plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Ethylene oxide production patents and industrial use"
    ),
    DoctrineBlock(
        topic="Catalytic Oxidation of Propylene to Acrolein",
        keywords=["propylene oxidation", "acrolein", "catalysis", "industrial chemistry", "oxidation process"],
        conclusion_template="Propylene is oxidized over mixed metal oxide catalysts to acrolein, an intermediate for acrylic acid production.",
        reasoning_framework=(
            "Selective oxidation of propylene to acrolein occurs over bismuth molybdate-based catalysts at 300-400°C. "
            "The process requires precise control of oxygen concentration and temperature to maximize yield and minimize byproducts. "
            "Catalyst composition and surface properties influence activity and selectivity. "
            "Acrolein is further oxidized to acrylic acid or used in other chemical syntheses. "
            "Catalyst deactivation by coking necessitates regeneration cycles."
        ),
        key_factors=[
            "Catalyst composition and surface area",
            "Operating temperature and oxygen concentration",
            "Feedstock purity",
            "Catalyst regeneration",
            "Product separation",
            "Environmental controls"
        ],
        primary_authority=[
            "Industrial catalysis literature",
            "Chemical engineering texts",
            "Patent literature"
        ],
        burden_holder="Process engineers and catalyst manufacturers",
        adversary_position="Catalyst deactivation and selectivity challenges",
        counter_arguments=[
            "Catalyst improvements enhance stability",
            "Process optimization improves selectivity",
            "Regeneration cycles maintain activity"
        ],
        resolution_strategy="Catalyst development and process control",
        entity_scope="Chemical manufacturing plants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Industrial propylene oxidation patents and applications"
    ),
    DoctrineBlock(
        topic="Phenol-Formaldehyde Resin Synthesis",
        keywords=["phenol-formaldehyde", "resin synthesis", "thermosetting polymers", "industrial chemistry", "polymerization"],
        conclusion_template="Phenol-formaldehyde resins are synthesized by condensation polymerization of phenol and formaldehyde under acidic or basic conditions, yielding thermosetting plastics.",
        reasoning_framework=(
            "Phenol reacts with formaldehyde in the presence of acid or base catalysts to form resols or novolacs. "
            "Resols are synthesized under basic conditions with excess formaldehyde, leading to self-curing resins. "
            "Novolacs are produced under acidic conditions with excess phenol and require curing agents. "
            "Polymerization involves electrophilic aromatic substitution and condensation reactions forming methylene and ether bridges. "
            "Process parameters such as pH, temperature, and molar ratios influence resin properties. "
            "Applications include adhesives, coatings, and molded products."
        ),
        key_factors=[
            "Catalyst type and concentration",
            "Molar ratios of reactants",
            "Temperature and reaction time",
            "Polymer molecular weight",
            "Curing conditions",
            "Product application requirements"
        ],
        primary_authority=[
            "Polymer chemistry textbooks",
            "Industrial polymer synthesis literature",
            "Material safety data sheets"
        ],
        burden_holder="Polymer chemists and process engineers",
        adversary_position="Formaldehyde toxicity and resin brittleness",
        counter_arguments=[
            "Process controls minimize free formaldehyde",
            "Additives improve resin toughness",
            "Safety protocols reduce exposure"
        ],
        resolution_strategy="Process optimization and safety management",
        entity_scope="Polymer manufacturing industry",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Phenol-formaldehyde resin patents and industrial use since early 20th century"
    ),
    DoctrineBlock(
        topic="Catalytic Oxidation of Ammonia to Nitric Oxide",
        keywords=["ammonia oxidation", "nitric oxide", "platinum catalyst", "industrial chemistry", "Ostwald process"],
        conclusion_template="Ammonia is catalytically oxidized to nitric oxide over platinum-rhodium gauze catalysts at high temperature, initiating nitric acid production.",
        reasoning_framework=(
            "Ammonia oxidation is a highly exothermic reaction performed at 900-950°C over platinum-rhodium catalysts. "
            "The reaction converts NH3 and O2 to NO and water. "
            "Precise temperature control is essential to prevent catalyst damage and side reactions producing N2O or NO2. "
            "Catalyst design focuses on maximizing surface area and durability. "
            "The produced NO is further oxidized and absorbed to form nitric acid."
        ),
        key_factors=[
            "Catalyst composition and structure",
            "Operating temperature and flow rate",
            "Ammonia and oxygen purity",
            "Catalyst deactivation",
            "Heat management",
            "Downstream processing"
        ],
        primary_authority=[
            "Industrial chemistry references",
            "Catalysis journals",
            "Nitric acid production standards"
        ],
        burden_holder="Process engineers and catalyst manufacturers",
        adversary_position="Catalyst degradation and process hazards",
        counter_arguments=[
            "Advanced catalyst materials improve durability",
            "Process control enhances safety and efficiency",
            "Regular maintenance extends catalyst life"
        ],
        resolution_strategy="Catalyst innovation and rigorous process control",
        entity_scope="Nitric acid production facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Ostwald process patents and industrial implementations"
    ),
    DoctrineBlock(
        topic="Hydrocyanation of Olefins for Nitrile Production",
        keywords=["hydrocyanation", "olefins", "nitriles", "catalysis", "industrial chemistry"],
        conclusion_template="Hydrocyanation adds hydrogen cyanide to olefins over nickel catalysts, producing nitriles used in plastics and pharmaceuticals.",
        reasoning_framework=(
            "Hydrocyanation involves the addition of HCN to olefins catalyzed by nickel complexes under moderate temperature and pressure. "
            "The reaction proceeds via coordination of olefin to the catalyst, insertion of HCN, and reductive elimination. "
            "Selectivity and activity depend on catalyst ligand environment and operating conditions. "
            "Nitriles produced are intermediates for acrylonitrile and other chemicals. "
            "Process safety is critical due to HCN toxicity."
        ),
        key_factors=[
            "Catalyst composition and ligand design",
            "Operating temperature and pressure",
            "HCN purity and handling",
            "Reaction selectivity",
            "Safety protocols",
            "Product separation"
        ],
        primary_authority=[
            "Industrial catalysis literature",
            "Chemical engineering texts",
            "Safety standards for HCN"
        ],
        burden_holder="Process engineers and safety managers",
        adversary_position="HCN toxicity and process hazards",
        counter_arguments=[
            "Strict safety protocols and monitoring",
            "Process automation reduces risks",
            "Catalyst development improves selectivity"
        ],
        resolution_strategy="Comprehensive safety and process control",
        entity_scope="Chemical manufacturing plants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Hydrocyanation patents and industrial use"
    ),
    DoctrineBlock(
        topic="Catalytic Oxidation of Ammonia to Nitric Acid",
        keywords=["ammonia oxidation", "nitric acid", "platinum catalyst", "industrial chemistry", "Ostwald process"],
        conclusion_template="Ammonia is oxidized catalytically to nitric oxide, the key intermediate in nitric acid production, using platinum-rhodium gauze catalysts.",
        reasoning_framework=(
            "The Ostwald process converts ammonia to nitric acid via catalytic oxidation to nitric oxide, followed by further oxidation and absorption. "
            "Ammonia oxidation occurs at 900-950°C over platinum-rhodium gauzes, producing NO and water. "
            "Temperature control is critical to prevent catalyst sintering and unwanted side reactions. "
            "Catalyst design focuses on maximizing surface area and durability. "
            "The process is exothermic and requires heat management."
        ),
        key_factors=[
            "Catalyst composition and structure",
            "Operating temperature and flow rate",
            "Ammonia and oxygen purity",
            "Catalyst deactivation",
            "Heat management",
            "Downstream processing"
        ],
        primary_authority=[
            "Industrial chemistry references",
            "Catalysis journals",
            "Nitric acid production standards"
        ],
        burden_holder="Process engineers and catalyst manufacturers",
        adversary_position="Catalyst degradation and process hazards",
        counter_arguments=[
            "Advanced catalyst materials improve durability",
            "Process control enhances safety and efficiency",
            "Regular maintenance extends catalyst life"
        ],
        resolution_strategy="Catalyst innovation and rigorous process control",
        entity_scope="Nitric acid production facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Ostwald process patents and industrial implementations"
    ),
    DoctrineBlock(
        topic="Industrial Production of Ethylene Glycol",
        keywords=["ethylene glycol", "ethylene oxide hydrolysis", "industrial chemistry", "catalysis", "polyethylene terephthalate"],
        conclusion_template="Ethylene glycol is produced by hydrolysis of ethylene oxide, serving as a key raw material for polyester production.",
        reasoning_framework=(
            "Ethylene oxide reacts with water in the presence of acid or base catalysts to produce ethylene glycol. "
            "The reaction conditions are controlled to minimize byproducts such as diethylene glycol. "
            "Catalyst choice and temperature influence selectivity and yield. "
            "Ethylene glycol is used in antifreeze formulations and as a monomer for polyethylene terephthalate (PET). "
            "Process design includes purification and recycling of unreacted materials."
        ),
        key_factors=[
            "Catalyst type and concentration",
            "Temperature and reaction time",
            "Water to ethylene oxide ratio",
            "Product purification",
            "Byproduct control",
            "Process safety"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Chemical engineering literature",
            "Material safety data sheets"
        ],
        burden_holder="Process engineers and safety managers",
        adversary_position="Byproduct formation and safety risks",
        counter_arguments=[
            "Process optimization reduces byproducts",
            "Safety protocols minimize hazards",
            "Continuous monitoring ensures quality"
        ],
        resolution_strategy="Process control and safety management",
        entity_scope="Chemical manufacturing plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Ethylene glycol production patents and industrial use"
    ),
    DoctrineBlock(
        topic="Catalytic Decomposition of Hydrogen Peroxide",
        keywords=["hydrogen peroxide", "catalytic decomposition", "industrial chemistry", "safety", "catalysis"],
        conclusion_template="Hydrogen peroxide decomposes catalytically into water and oxygen, requiring controlled conditions to prevent hazards in industrial settings.",
        reasoning_framework=(
            "Hydrogen peroxide decomposes exothermically into water and oxygen, catalyzed by metals, metal oxides, and impurities. "
            "In industrial settings, decomposition is controlled to prevent runaway reactions and explosions. "
            "Catalyst poisoning and stabilizers are used to manage decomposition rates. "
            "Storage and handling protocols minimize risk. "
            "Decomposition is also harnessed for oxygen generation and wastewater treatment."
        ),
        key_factors=[
            "Catalyst presence and activity",
            "Temperature control",
            "Stabilizer use",
            "Storage conditions",
            "Safety protocols",
            "Process monitoring"
        ],
        primary_authority=[
            "Industrial safety guidelines",
            "Chemical engineering literature",
            "Material safety data sheets"
        ],
        burden_holder="Plant safety managers and operators",
        adversary_position="Risk of uncontrolled decomposition and explosion",
        counter_arguments=[
            "Strict safety protocols and monitoring",
            "Use of stabilizers and inhibitors",
            "Process automation reduces risks"
        ],
        resolution_strategy="Comprehensive safety management and process control",
        entity_scope="Hydrogen peroxide production and handling facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Industrial safety standards for hydrogen peroxide"
    ),
    DoctrineBlock(
        topic="Industrial Production of Sodium Hypochlorite",
        keywords=["sodium hypochlorite", "chlorination", "industrial chemistry", "disinfection", "bleaching"],
        conclusion_template="Sodium hypochlorite is produced by chlorination of sodium hydroxide, serving as a disinfectant and bleaching agent.",
        reasoning_framework=(
            "Sodium hypochlorite is synthesized by reacting chlorine gas with sodium hydroxide solution at controlled temperature and concentration. "
            "The reaction produces NaOCl and sodium chloride. "
            "Process control includes temperature management to prevent decomposition and side reactions. "
            "Product concentration and purity are adjusted for intended applications. "
            "Storage stability is enhanced by controlling pH and temperature."
        ),
        key_factors=[
            "Chlorine and sodium hydroxide purity",
            "Temperature control",
            "Reaction stoichiometry",
            "Product concentration",
            "Storage conditions",
            "Safety protocols"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Chemical safety guidelines",
            "Water treatment manuals"
        ],
        burden_holder="Process engineers and safety managers",
        adversary_position="Chlorine handling hazards and product stability",
        counter_arguments=[
            "Strict safety procedures for chlorine",
            "Process automation reduces risks",
            "Stabilizers improve product shelf life"
        ],
        resolution_strategy="Safety management and process optimization",
        entity_scope="Chemical manufacturing plants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Industrial sodium hypochlorite production standards"
    ),
    DoctrineBlock(
        topic="Industrial Production of Butadiene via Dehydrogenation",
        keywords=["butadiene", "dehydrogenation", "industrial chemistry", "catalysis", "synthetic rubber"],
        conclusion_template="Butadiene is produced by catalytic dehydrogenation of butenes or butanes, serving as a monomer for synthetic rubber.",
        reasoning_framework=(
            "Catalytic dehydrogenation removes hydrogen from butenes or butanes over metal oxide catalysts at high temperature. "
            "The process is endothermic and requires heat input and careful temperature control. "
            "Catalyst selectivity and resistance to coking are critical. "
            "Butadiene is a key feedstock for synthetic rubber and plastics. "
            "Process design includes catalyst regeneration and product separation."
        ),
        key_factors=[
            "Catalyst composition and stability",
            "Operating temperature and pressure",
            "Feedstock purity",
            "Coke formation and catalyst regeneration",
            "Heat management",
            "Product purification"
        ],
        primary_authority=[
            "Petrochemical industry literature",
            "Catalysis journals",
            "Industrial process patents"
        ],
        burden_holder="Process engineers and catalyst suppliers",
        adversary_position="Catalyst deactivation and energy consumption",
        counter_arguments=[
            "Advanced catalysts reduce coke formation",
            "Heat integration improves energy efficiency",
            "Catalyst regeneration extends life"
        ],
        resolution_strategy="Catalyst development and process optimization",
        entity_scope="Petrochemical plants",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Industrial butadiene production patents and processes"
    ),
    DoctrineBlock(
        topic="Industrial Production of Sulfuric Acid via Lead Chamber Process",
        keywords=["sulfuric acid", "lead chamber process", "industrial chemistry", "acid production"],
        conclusion_template="The lead chamber process produces sulfuric acid by oxidizing sulfur dioxide in large chambers with nitrogen oxides as catalysts.",
        reasoning_framework=(
            "The lead chamber process involves burning sulfur or pyrites to produce SO2, which is oxidized to SO3 in the presence of nitrogen oxides within large lead-lined chambers. "
            "SO3 reacts with water to form sulfuric acid. "
            "This older process operates at atmospheric pressure and lower concentrations compared to the contact process. "
            "Process control involves managing gas flows, temperature, and nitrogen oxide recycling. "
            "Environmental concerns and efficiency limitations have led to replacement by the contact process."
        ),
        key_factors=[
            "Gas composition and flow rates",
            "Temperature control",
            "Nitrogen oxide catalyst recycling",
            "Chamber maintenance",
            "Product concentration",
            "Environmental emissions"
        ],
        primary_authority=[
            "Historical industrial chemistry texts",
            "Chemical engineering literature",
            "Environmental regulations"
        ],
        burden_holder="Plant operators and environmental managers",
        adversary_position="Low efficiency and environmental impact",
        counter_arguments=[
            "Process replaced by more efficient contact process",
            "Used historically for low concentration acid",
            "Environmental controls mitigate emissions"
        ],
        resolution_strategy="Transition to contact process and environmental compliance",
        entity_scope="Historical sulfuric acid production facilities",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="Lead chamber process historical patents and usage"
    ),
    DoctrineBlock(
        topic="Industrial Production of Phosphoric Acid via Wet Process",
        keywords=["phosphoric acid", "wet process", "industrial chemistry", "phosphate rock", "acid production"],
        conclusion_template="Phosphoric acid is produced by reacting phosphate rock with sulfuric acid in the wet process, yielding phosphoric acid and gypsum byproduct.",
        reasoning_framework=(
            "The wet process involves digestion of phosphate rock with concentrated sulfuric acid, producing phosphoric acid and calcium sulfate (gypsum) as a byproduct. "
            "Reaction conditions are controlled to optimize acid concentration and minimize impurities. "
            "Phosphoric acid is used in fertilizers and industrial applications. "
            "Waste management of gypsum and impurities is a key environmental concern."
        ),
        key_factors=[
            "Phosphate rock quality",
            "Sulfuric acid concentration",
            "Reaction temperature and time",
            "Impurity control",
            "Gypsum handling",
            "Environmental compliance"
        ],
        primary_authority=[
            "Industrial chemistry texts",
            "Fertilizer industry literature",
            "Environmental regulations"
        ],
        burden_holder="Plant operators and environmental managers",
        adversary_position="Waste gypsum disposal and impurities",
        counter_arguments=[
            "Gypsum reuse in construction materials",
            "Process optimization reduces impurities",
            "Environmental monitoring and controls"
        ],
        resolution_strategy="Sustainable waste management and process control",
        entity_scope="Phosphoric acid production plants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Wet process patents and industrial use"
    ),
    DoctrineBlock(
        topic="Industrial Production of Formaldehyde via Methanol Oxidation",
        keywords=["formaldehyde", "methanol oxidation", "industrial chemistry", "catalysis"],
        conclusion_template="Formaldehyde is produced by catalytic oxidation of methanol over silver or iron-molybdenum catalysts, serving as a precursor for